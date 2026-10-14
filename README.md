# TV App Starter

Build your own native **Apple TV** or **Android TV / Google TV** app with Codex or Claude Code. Two offline samples, no accounts, no backend, and no personal configuration required. MIT licensed; currently private for owner review before public release.

Inspired by building custom TV apps with Codex, this starter provides a dashboard, remote navigation, detail screens, practice check-offs, and a saved dark/light appearance preference. It runs as a regular TV app. Physical-device installation uses your own signing or developer setup.

## Screenshots

Fresh captures of the sample apps, using fictional content:

### Apple TV
![Apple TV sample dashboard](docs/screenshots/apple-tv.png)

### Android TV
![Android TV sample dashboard](docs/screenshots/android-tv.png)

## Start your custom app

Requires Python 3. Apple TV development requires a Mac with Xcode and the tvOS SDK. Android builds require JDK 17, Android SDK platform 35 and build-tools 35.0.0. No third-party runtime libraries are used.

```sh
git clone https://github.com/dsampath/tv-app-starter.git
cd tv-app-starter
python3 skills/build-tv-app/scripts/new_app.py ../my-tv-app --bundle-id org.example.myapp
cd ../my-tv-app
```

The generator refuses to overwrite a directory and copies only sample sources and tooling. It never copies Git history, build products or credentials.

## Apple TV

```sh
python3 generate-project.py
swift test
xcodebuild -project FamilyTV.xcodeproj -scheme FamilyTV   -configuration Debug -sdk appletvsimulator   -destination 'generic/platform=tvOS Simulator'   -derivedDataPath build CODE_SIGNING_ALLOWED=NO build
```

Open `FamilyTV.xcodeproj`, choose the `FamilyTV` scheme and a tvOS simulator, then Run. For a real Apple TV, set your own bundle ID and signing team in Xcode, pair your TV, and select it as the run destination. Do not commit your signing configuration. Regenerating the project intentionally removes local signing settings.

Customize `FamilyTV/FamilyTVApp.swift` for layout, navigation, cards, colors and detail screens. `Core/FamilyState.swift` contains fictional data and date/check-off logic; `Tests/FamilyStateTests.swift` covers midnight changes, streaks, daylight-saving arithmetic and request validation. Run the project generator after adding Swift files.

## Android TV / Google TV (including compatible TCL models)

For quick testing, download `TVStarter.apk` from the private [v0.1.0 preview release](https://github.com/dsampath/tv-app-starter/releases/tag/v0.1.0), then install it with `adb -s YOUR_DEVICE_SERIAL install -r TVStarter.apk`. This is a debug build for local testing.

Set `ANDROID_SDK_ROOT` to your SDK directory and `JAVA_HOME` to your JDK 17 directory locally. Use Android Studio's SDK Manager to install Android SDK Platform 35 and Android SDK Build-Tools 35.0.0, plus Platform-Tools for `adb`.

```sh
python3 AndroidTV/build.py
adb devices
adb -s YOUR_DEVICE_SERIAL install -r AndroidTV/build/TVStarter.apk
adb -s YOUR_DEVICE_SERIAL shell am start -n org.example.tvstarter/.MainActivity
```

Enable developer options and USB/network debugging on your TV and authorize your own computer. Select the exact device serial shown by `adb devices`. This sample does not scan your network or connect to TVs automatically. The generated debug key stays in ignored `AndroidTV/build/`; keep it locally if you want to install updates. Use separate release signing for distribution.

Customize `AndroidTV/src/org/example/tvstarter/MainActivity.java`. When changing the package, update its declaration, source path and `AndroidManifest.xml` together (the starter generator does this for you). The Android sample has no Internet permission and declares Leanback launch support without requiring touch input.

## Use with Codex or Claude Code

**Codex:** launch Codex in this checkout. `.agents/skills/build-tv-app` points to the bundled skill. Invoke `$build-tv-app` with a request such as:

> Build an Apple TV app for my reading list, with big remote-focusable cards and an offline demo. Create it in a new directory.

**Claude Code:** load the local plugin from the repository root:

```sh
claude --plugin-dir .
```

Then invoke `/tv-app-starter:build-tv-app` with your app idea and platform. Validate packaging with `claude plugin validate .`.

The shared skill is at `skills/build-tv-app/SKILL.md`; it can create a fresh starter using the bundled script. Codex currently uses repository skill discovery; this is not a published Codex marketplace package. Claude Code has a local plugin manifest. No remote code service, telemetry, device credentials or model API keys are bundled.

Packaging references: [official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference).

## Test before putting it on your TV

Use a fresh simulator or Android TV emulator. Navigate to every card and tab with the remote/D-pad, select a card, use Back, toggle practice tasks, change appearance, and relaunch. Appearance is saved locally; practice check-offs are deliberately in memory in these UI samples. The two implementations demonstrate the same flow with native controls; layouts need not be pixel-identical.

See [validation notes](docs/VALIDATION.md) for checks completed on this version. No claim of App Store/Play Store readiness or system screensaver replacement is made.

## Privacy and contributions

This repository starts with fresh Git history and an allowlisted export. Original deployment configurations, bridge services, account data, home network addresses, device identifiers, signing identities, personal photos and screenshots, logs, and unrelated apps were excluded. All included imagery consists of newly created generic icons and fresh sample captures.

Before committing, run:

```sh
python3 scripts/check_privacy.py
```

The scanner checks tracked files for common secrets, local paths, private network addresses and private/generated file types. It complements secret scanning and visual review; it cannot prove that arbitrary user-added content contains no personal information. Keep local integrations and signing files ignored, and review every new screenshot before sharing.

See [contribution guidelines](CONTRIBUTING.md). Source code, icons and screenshots are covered by the MIT license.
