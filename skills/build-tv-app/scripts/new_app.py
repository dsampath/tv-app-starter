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
# Generated apps link to upstream guides rather than copying repository screenshots.
readme = destination / 'README.md'
readme.write_text(f"""# Your TV app

Hello, big screen. This is your own copy of TV App Starter, ready for an idea.

Your app ID is `{a.bundle_id}`. Start by changing the dashboard cards, then
build and try the result with a remote.

## Apple TV

From this folder, run:

```sh
python3 generate-project.py
```

Open `FamilyTV.xcodeproj` in Xcode, choose the `FamilyTV` scheme and a tvOS
simulator, then Run. Edit `FamilyTV/FamilyTVApp.swift` to make it yours.
The shared logic tests run with `swift test`.

[Apple TV setup](https://github.com/dsampath/tv-app-starter/blob/main/docs/APPLE_TV.md)
walks through build tools and installation on a real TV.

## Android TV

Set `ANDROID_SDK_ROOT` and `JAVA_HOME` for your Android SDK and JDK 17, then run:

```sh
python3 AndroidTV/build.py
adb devices
adb -s YOUR_DEVICE_SERIAL install -r AndroidTV/build/TVStarter.apk
adb -s YOUR_DEVICE_SERIAL shell am start -n {a.bundle_id}/.MainActivity
```

Replace `YOUR_DEVICE_SERIAL` with your selected TV or emulator's serial.
Edit `AndroidTV/src/{'/'.join(a.bundle_id.split('.'))}/MainActivity.java` for the UI.

[Android TV setup](https://github.com/dsampath/tv-app-starter/blob/main/docs/ANDROID_TV.md)
explains the SDK, debugging, and local signing keys.

## Keep going

Open this folder in Codex and ask `$build-tv-app` to help with your next change.
For the Claude Code plugin, load the original starter checkout with
`claude --plugin-dir <starter-folder>` and use `/tv-app-starter:build-tv-app`.

Keep personal settings and keys local, and use fictional data in shared examples.
See the [starter walkthrough](https://github.com/dsampath/tv-app-starter) for ideas,
[privacy notes](https://github.com/dsampath/tv-app-starter/blob/main/docs/PRIVACY.md),
and the [MIT license](LICENSE).
""")
print('Created sample:', destination)
