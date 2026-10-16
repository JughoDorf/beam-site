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
assert len(metadata['files']) == 10
stable = metadata['stable']
assert stable['version'] == '2.2.4' and stable['status'] == 'stable'
assert stable['windows_version'] == '2.2.4' and stable['android_version'] == '2.2.4'
assert stable['module_version'] == '0.1.6'
assert stable['brand'] == 'Project Beam' and stable['application'] == 'Beam'
assert stable['wan_video_tested'] is False and stable['media_pipeline_changed'] is False
assert re.fullmatch(r'[a-f0-9]{40}', stable['source_commit'])
assert len(set(stable['sources'])) == 3
stable_sources = [x for x in metadata['sources'] if x['name'] in stable['sources']]
assert len(stable_sources) == 3
for item in stable_sources:
    module = item['name'].startswith('BeamConnect-')
    assert item['source_commit'] == stable['module_source_commit' if module else 'source_commit']
    assert item['tag'] == (stable['module_tag'] if module else stable['tag'])
    assert item['file_count'] > 100
assert set(x['name'] for x in stable_sources) == {'Beam-Windows-2.2.4-source.tar.gz','Beam-Android-2.2.4-source.tar.gz','BeamConnect-0.1.6-source.tar.gz'}
preview = metadata['preview']
assert preview['status'] == 'prerelease' and preview['wan_video_tested'] is False
assert len(preview['files']) == 10 and len(preview['sources']) == 3
assert re.fullmatch(r'[a-f0-9]{40}', preview['source_commit'])
assert preview['release_url'] == 'https://github.com/JughoDorf/beam-site/releases/tag/' + preview['tag']
current = metadata['files'] + preview['files'] + preview['sources'] + stable_sources
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
known_downloads.update([preview['instructions_url'], stable['instructions_url'], stable['checksums_url']])
dns = json.loads((root/'beamdns-downloads.json').read_text(encoding='utf-8'))
assert dns['product'] == 'BeamDNS' and dns['brand'] == 'Project Beam'
assert dns['status'] == 'beta' and dns['version'] == '0.9.0-beta.4'
assert dns['tag'] == 'beamdns-v0.9.0-beta.4' and dns['signed'] is False
assert len(dns['files']) == 6 and len({x['name'] for x in dns['files']}) == 6
for item in dns['files']:
    assert item['tag'] == dns['tag'] and item['bytes'] > 0
    assert re.fullmatch(r'[a-f0-9]{64}', item['sha256']), item['name']
    assert item['url'] == 'https://github.com/JughoDorf/beam-site/releases/download/' + dns['tag'] + '/' + item['name']
known_downloads.update(item['url'] for item in dns['files'])
dns_installer = next(x for x in dns['files'] if x['name'].endswith('.exe'))
assert dns_installer['name'] == 'BeamDNS-Setup-0.9.0-beta.4-win-x64.exe' and dns_installer['bytes'] == 5305856
assert dns_installer['url'] in (root/'beamdns.html').read_text(encoding='utf-8')
assert set(pages) == {'index.html', 'beam.html', 'beamdns.html', 'sources.html'}
assert 'Project Beam — программы' in (root/'index.html').read_text(encoding='utf-8')
assert 'BeamSetup-2.2.4.exe' in (root/'beam.html').read_text(encoding='utf-8')
for filename, page in pages.items():
    for link in page.links:
        if '/releases/download/' in link:
            assert link in known_downloads, (filename, 'Missing download metadata', link)
preview_prefix = 'https://github.com/JughoDorf/beam-site/releases/download/' + preview['tag'] + '/'
assert preview['checksums_url'] == preview_prefix + 'SHA256SUMS.txt'
assert preview['instructions_url'] == preview_prefix + 'INSTALL-EASYTIER-ru.md'
assert set(x['name'] for x in preview['files']) == {
    'BeamServerSetup-2.2.1.exe', 'BeamClientSetup-2.2.1.exe', 'BeamSetup-2.2.1.exe',
    'BeamEasyTierSetup-0.1.4.exe', 'BeamEasyTier-0.1.4-windows-x64.zip',
    *('BeamAndroid-2.2.1-' + abi + '.apk' for abi in ['arm32','arm64','universal','x86','x86_64'])}
assert set(x['name'] for x in preview['sources']) == {
    'Beam-Windows-2.2.1-source.tar.gz', 'Beam-Android-2.2.1-source.tar.gz', 'BeamEasyTier-0.1.4-source.tar.gz'}
assert set(x['name'] for x in metadata['files']) == {
    'BeamSetup-2.2.4.exe', 'BeamServerSetup-2.2.4.exe', 'BeamClientSetup-2.2.4.exe',
    'BeamConnectSetup-0.1.6.exe', 'BeamConnect-0.1.6-windows-x64.zip',
    *('BeamAndroid-2.2.4-' + abi + '.apk' for abi in ['arm32','arm64','universal','x86','x86_64'])}
assert 'JughoDorf/Beam/releases/' not in (root/'index.html').read_text(encoding='utf-8')
catalog = (root/'easytier-nodes.txt').read_text(encoding='ascii')
nodes = catalog.split()
assert len(catalog.encode("ascii")) <= 65536 and 2 <= len(nodes) <= 256 and len(set(nodes)) == len(nodes)
for node in nodes:
    address = urlsplit(node)
    assert address.scheme in ('tcp', 'udp') and address.hostname and address.port
    assert address.path == '' and not address.username and not address.password
    assert '.' in address.hostname and not address.hostname.endswith('.local')
    assert not re.fullmatch(r'[0-9.]+', address.hostname)
    assert 1 <= address.port <= 65535
assert 'public.easytier.cn' not in nodes
print('PASS: four product/brand pages, 10 stable / 10 preview Beam files, independent BeamDNS beta, source links and SHA-256')
