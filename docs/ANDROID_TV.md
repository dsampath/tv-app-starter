# Get it running on Android TV

You can try the ready-made APK first, or build your own copy. Both routes give you the same offline sample to explore with a remote.

## Try the preview APK

Download `TVStarter.apk` from the [preview release](https://github.com/dsampath/tv-app-starter/releases/tag/v0.1.0). While the repository is private, you’ll need repository access to download it.

Install Android SDK Platform-Tools to get `adb`. On your own Android TV or Google TV, enable developer options and debugging, connect using your device’s supported USB or network-debugging method, and authorize your computer on the TV. The exact settings vary by manufacturer and firmware. TCL TVs need to run Android TV or Google TV for this sample.

Find your device:

```sh
adb devices
```

Copy its serial from that output. From the folder containing your downloaded APK, replace `YOUR_DEVICE_SERIAL` in these commands:

```sh
adb -s YOUR_DEVICE_SERIAL install -r TVStarter.apk
adb -s YOUR_DEVICE_SERIAL shell am start -n org.example.tvstarter/.MainActivity
```

You should see TV Starter in the app launcher and its dashboard on screen. This preview uses a generic development signing key and is intended for local testing.

## Build your own copy

You’ll need Python 3, JDK 17, and an Android SDK with:

- Android SDK Platform 35.
- Android SDK Build-Tools 35.0.0.
- Android SDK Platform-Tools for installation and debugging.

Android Studio’s SDK Manager can install the SDK packages. Set `ANDROID_SDK_ROOT` to your SDK directory and `JAVA_HOME` to your JDK 17 directory in your local shell. You can also use `ANDROID_HOME` for the SDK path.

From the app’s root folder:

```sh
python3 AndroidTV/build.py
```

The builder compiles the native Java app, signs it with a local debug key, and verifies the APK. Look for `Built and verified` and the output at `AndroidTV/build/TVStarter.apk`.

Install it on your selected TV or emulator:

```sh
adb devices
adb -s YOUR_DEVICE_SERIAL install -r AndroidTV/build/TVStarter.apk
adb -s YOUR_DEVICE_SERIAL shell am start -n org.example.tvstarter/.MainActivity
```

**Created an app with a custom ID?** Use that ID in the launch command. For the reading-list example in the README:

```sh
adb -s YOUR_DEVICE_SERIAL shell am start -n org.example.readingroom/.MainActivity
```

The APK filename remains `TVStarter.apk` even when you change the app’s package ID.

## Prefer an emulator?

In Android Studio’s Device Manager, create an Android TV virtual device with a compatible system image. Start it, then use the emulator serial listed by `adb devices` in the install commands above. The sample supports Android 8.0 / API 26 and later; its preview was checked on an Android TV API 34 emulator.

Use D-pad controls to visit each tab and card. Select a card, press Back, toggle a practice task, then change appearance and relaunch. Appearance should stick; practice check-offs are in memory.

## Where to make changes

The UI lives in `AndroidTV/src/org/example/tvstarter/MainActivity.java`. In a generated app, the folder follows your package ID instead. Start with the `titles` and `details` arrays to give the dashboard your own content.

`AndroidTV/AndroidManifest.xml` declares the package and TV launcher support. The starter generator updates the package declaration, Java source path, and manifest together. Keep those aligned if you rename a package manually.

The sample uses native Android controls, supports the TV launcher, and requires neither touch input nor Internet permission.

## A couple of useful fixes

If `adb devices` says `unauthorized`, approve the debugging request on your TV. If it lists several devices, choose the intended serial explicitly with `-s`.

If installation reports a signature mismatch, you may be installing over a copy signed with a different debug key. Use a distinct package ID, or uninstall the old sample if you’re happy to lose its local settings. Keep your generated `AndroidTV/build/debug.keystore` locally for future updates; the build directory is ignored by Git. The downloaded preview and a locally built copy use different keys.

Release signing and Play Store distribution need a separate setup when you’re ready to ship.

[Back to the walkthrough](../README.md) · [Validation notes](VALIDATION.md)
