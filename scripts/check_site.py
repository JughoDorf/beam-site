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
preview = metadata['preview']
assert preview['status'] == 'prerelease' and preview['wan_video_tested'] is False
assert len(preview['files']) == 10 and len(preview['sources']) == 3
assert re.fullmatch(r'[a-f0-9]{40}', preview['source_commit'])
assert preview['release_url'] == 'https://github.com/JughoDorf/beam-site/releases/tag/' + preview['tag']
current = metadata['files'] + preview['files'] + preview['sources']
assert len({item['name'] for item in current}) == len(current)
for item in current:
    assert re.fullmatch(r'[a-f0-9]{64}', item['sha256']), item['name']
    assert item['bytes'] > 1000000, item['name']
    assert item['url'].startswith('https://github.com/JughoDorf/beam-site/releases/download/'), item['name']
    assert item['url'].endswith('/'+item['name']), item['name']
    assert item['url'].split('/')[-2] == item['tag'], item['name']
known_downloads = {item['url'] for item in current}
known_downloads.update(item['url'] for item in metadata['sources'] if 'url' in item)
known_downloads.update('https://github.com/JughoDorf/beam-site/releases/download/' + item['tag'] + '/SHA256SUMS.txt' for item in current)
known_downloads.add(preview['instructions_url'])
for filename, page in pages.items():
    for link in page.links:
        if '/releases/download/' in link:
            assert link in known_downloads, (filename, 'Missing download metadata', link)
preview_prefix = 'https://github.com/JughoDorf/beam-site/releases/download/' + preview['tag'] + '/'
assert preview['checksums_url'] == preview_prefix + 'SHA256SUMS.txt'
assert preview['instructions_url'] == preview_prefix + 'INSTALL-EASYTIER-ru.md'
assert set(x['name'] for x in preview['files']) == {
    'BeamServerSetup-2.1.3.exe', 'BeamClientSetup-2.1.7.exe', 'BeamSetup-2.1.7.exe',
    'BeamEasyTierSetup-0.1.2.exe', 'BeamEasyTier-0.1.2-windows-x64.zip',
    *('BeamAndroid-0.4.0-' + abi + '.apk' for abi in ['arm32','arm64','universal','x86','x86_64'])}
assert set(x['name'] for x in preview['sources']) == {
    'Beam-Windows-2.1.7-source.tar.gz', 'Beam-Android-0.4.0-source.tar.gz', 'BeamEasyTier-0.1.2-source.tar.gz'}
assert set(x['name'] for x in metadata['files']) == {
    'BeamServerSetup-2.0.11.exe', 'BeamClientSetup-2.0.8.exe',
    *('BeamAndroid-0.3.1-' + abi + '.apk' for abi in ['arm32','arm64','universal','x86','x86_64'])}
assert 'JughoDorf/Beam/releases/' not in (root/'index.html').read_text(encoding='utf-8')
catalog = (root/'easytier-nodes.txt').read_text(encoding='ascii')
nodes = catalog.split()
assert len(catalog) <= 2048 and 2 <= len(nodes) <= 8 and len(set(nodes)) == len(nodes)
for node in nodes:
    address = urlsplit(node)
    assert address.scheme in ('tcp', 'udp') and address.hostname and address.port
    assert address.path == '' and not address.username and not address.password
    assert '.' in address.hostname and not address.hostname.endswith('.local')
    assert not re.fullmatch(r'[0-9.]+', address.hostname)
    assert 1 <= address.port <= 65535
assert 'public.easytier.cn' not in nodes
print('PASS: resources, navigation, 7 stable / 10 preview downloads, 3 preview sources, SHA-256, public links')
