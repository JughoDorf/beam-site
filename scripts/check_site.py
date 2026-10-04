"""Check staged website links and public download metadata before Pages deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

root = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids = set(); self.links = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            assert data['id'] not in self.ids, 'Duplicate id: ' + data['id']
            self.ids.add(data['id'])
        for name in ['href', 'src']:
            if data.get(name): self.links.append(data[name])

pages = {path.name: Page(path.read_text(encoding='utf-8')) for path in root.glob('*.html')}
for filename, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme == 'https' and url.netloc == 'github.com', link
            assert url.path.startswith('/JughoDorf/beam-site'), 'Unexpected repository: ' + link
            continue
        path = root / unquote(url.path or filename)
        if path.is_dir(): path = path / 'index.html'
        assert path.exists(), (filename, link)
        assert path.resolve().is_relative_to(root), 'Outside website: ' + link
        if url.fragment and path.suffix == '.html':
            assert url.fragment in pages[path.name].ids, (filename, link)

metadata = json.loads((root/'downloads.json').read_text(encoding='utf-8'))
assert len(metadata['files']) == 7
for item in metadata['files']:
    assert re.fullmatch(r'[a-f0-9]{64}', item['sha256']), item['name']
    assert item['bytes'] > 1000000, item['name']
    assert item['url'].startswith('https://github.com/JughoDorf/beam-site/releases/download/'), item['name']
    assert item['url'].endswith('/'+item['name']), item['name']
assert 'JughoDorf/Beam/releases/' not in (root/'index.html').read_text(encoding='utf-8')
print('PASS: local resources, navigation, seven downloads, SHA-256 metadata, public repository links')
