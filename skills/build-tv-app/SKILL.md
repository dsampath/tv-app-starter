---
name: build-tv-app
description: Build and customize native Apple TV (tvOS) or Android TV apps from the bundled offline TV Starter samples, including remote navigation and local build/install workflows.
---

Build the user's requested TV app using this repository's sample, rather than modifying firmware or replacing a system screensaver. Resolve the plugin repository from this file's real location: two directories above this skill directory. Templates are at that repository root.

If creating a new app, run `python3 <skill-directory>/scripts/new_app.py <new-directory> --bundle-id org.example.myapp`. This copies a clean starter without Git history, credentials, binaries, or existing local data. Never overwrite an existing destination. Ask for platform, app idea, and target device only when missing and consequential; progress on generic UI while awaiting device details.

Apple TV: edit `FamilyTV/FamilyTVApp.swift` and `Core/FamilyState.swift`. After adding Swift files, run `python3 generate-project.py`. Use native SwiftUI focusable buttons and `.onExitCommand`, large couch-readable type, and reduced-motion-friendly behavior. Run `swift test` and the simulator build documented in README. Device installation requires the user's own signing team and an explicitly selected paired Apple TV in Xcode. Never embed their team ID in the shared sample.

Android TV: edit `AndroidTV/src/.../MainActivity.java`. Use native focusable controls, visible focus outlines, D-pad traversal, Back navigation, a Leanback launcher entry, and no touchscreen requirement. Set local `ANDROID_SDK_ROOT` and `JAVA_HOME`; run `python3 AndroidTV/build.py`. Run `adb devices` and require an explicitly chosen serial for install: `adb -s <serial> install -r AndroidTV/build/TVStarter.apk`. Preserve local signing keys for updates; release signing is separate. Never automatically connect to discovered network TVs.

Start offline with fictional data. Add network integrations only when the requested app needs them, keep provider credentials on a backend, and keep device addresses/configuration local and ignored. Do not bundle the user's photos, calendars, schools, account names, tokens, logs, recordings, or home network data. Use fresh simulator/emulator screenshots for documentation.

Validate Select, Back, navigation reachability, light/dark appearance, lifecycle changes, and relaunch. Report what was actually built and tested and any remaining physical-device checks. Run `python3 scripts/check_privacy.py` on staged/tracked files before sharing. Publishing or changing repository visibility requires the user's explicit request.
