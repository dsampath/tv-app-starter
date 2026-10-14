"""Copy an offline TV starter into a NEW directory (Python standard library only)."""
import argparse
import re
import shutil
from pathlib import Path
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('destination', type=Path)
p.add_argument('--bundle-id', default='org.example.myapp')
a = p.parse_args()
if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,}', a.bundle_id):
    p.error('bundle-id must have at least three lowercase Java-compatible segments')
root = Path(__file__).resolve().parents[3]
destination = a.destination.expanduser().resolve()
if destination.exists(): p.error('destination exists; choose a new directory')
if root == destination or root in destination.parents: p.error('choose a destination outside the plugin repository')
destination.mkdir(parents=True)
ignore = shutil.ignore_patterns('build', '.build', '__pycache__', 'xcuserdata', '*.xcuserstate')
for name in ['FamilyTV', 'Core', 'Tests', 'AndroidTV', 'skills', 'scripts']:
    shutil.copytree(root / name, destination / name, ignore=ignore)
for name in ['Package.swift', 'generate-project.py', '.gitignore', 'LICENSE', 'README.md']:
    shutil.copy2(root / name, destination / name)
current_id = re.search(r'package="([^"]+)"', (destination / 'AndroidTV/AndroidManifest.xml').read_text()).group(1)
for path in destination.rglob('*'):
    if path.is_file() and (path.suffix in {'.java', '.xml'} or path.name == 'generate-project.py'):
        path.write_text(path.read_text().replace(current_id, a.bundle_id))
source = next((destination / 'AndroidTV/src').rglob('MainActivity.java'))
target = destination / 'AndroidTV/src' / Path(*a.bundle_id.split('.')) / 'MainActivity.java'
if source != target:
    target.parent.mkdir(parents=True, exist_ok=True)
    source.rename(target)
(destination / '.agents/skills').mkdir(parents=True)
(destination / '.agents/skills/build-tv-app').symlink_to('../../skills/build-tv-app', target_is_directory=True)
# Paths in the copied README refer to upstream screenshots and documentation.
readme = destination / 'README.md'
readme.write_text('# Your TV app\n\nStart with `python3 generate-project.py` and `swift test` for Apple TV, or `python3 AndroidTV/build.py` for Android TV.\n\nSee https://github.com/dsampath/tv-app-starter for setup and customization documentation.\n')
print('Created sample:', destination)
