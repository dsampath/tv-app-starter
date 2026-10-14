# Get it running on Apple TV

Let’s start in a simulator. It gives you somewhere to experiment before dealing with a real TV’s signing and pairing setup.

## Your toolkit

You’ll need a Mac, Xcode with the tvOS SDK and a tvOS simulator runtime, and Python 3. In Xcode, check Settings → Components for the tvOS runtime if no simulator is available. The sample targets tvOS 17 or later.

Run commands from your app’s root folder. If you cloned the starter, its Xcode project is already included. If you used the generator to create your own app, make the project first:

```sh
python3 generate-project.py
```

## Your first launch

Open `FamilyTV.xcodeproj` in Xcode. Choose the `FamilyTV` scheme, select a tvOS simulator as the destination, and press Run.

You should see the dashboard with three cards. Use the simulator’s remote controls to move between them, select one, and return with Back/Menu. Explore Practice and Settings as well.

The project and scheme retain the `FamilyTV` names even when your app has a custom bundle ID. That’s the sample’s internal project name; you can rename it as your app takes shape.

## Build from the terminal

These commands test the shared Swift logic and compile the simulator app:

```sh
swift test
xcodebuild -project FamilyTV.xcodeproj -scheme FamilyTV \
  -configuration Debug -sdk appletvsimulator \
  -destination 'generic/platform=tvOS Simulator' \
  -derivedDataPath build CODE_SIGNING_ALLOWED=NO build
```

A successful terminal build compiles the app. Use Xcode’s Run action to launch it in a simulator.

## Put it on your Apple TV

Pair your Apple TV with Xcode using its Devices and Simulators window and the TV’s remote-device pairing settings. Select the paired TV as the run destination.

In the target’s Signing & Capabilities settings, choose your Apple development team and an app bundle ID you can sign. Run the app from Xcode. Your account, provisioning, and device setup determine which installation options are available.

Keep signing details local. The project generator intentionally creates a project without a signing team, so running it again resets team settings you added in Xcode. Reapply those settings locally when needed.

For a compilation check against the device SDK:

```sh
xcodebuild -project FamilyTV.xcodeproj -scheme FamilyTV \
  -configuration Debug -sdk appletvos \
  -destination 'generic/platform=tvOS' \
  -derivedDataPath build-device CODE_SIGNING_ALLOWED=NO build
```

That unsigned build checks compilation; it isn’t a signed app you can install on your TV.

## Where to make changes

- `FamilyTV/FamilyTVApp.swift`: dashboard, cards, navigation, detail screens, and colors.
- `Core/FamilyState.swift`: sample data, check-offs, countdowns, and local request logic.
- `Tests/FamilyStateTests.swift`: checks for the shared logic.

Run `python3 generate-project.py` after adding Swift source files so the Xcode project picks them up. Try each change with the remote: reach every control, open and leave a detail screen, and check light and dark appearance. Appearance is saved locally; practice check-offs are in memory.

If something won’t build, check that Xcode’s command-line tools point to the full Xcode installation and that the tvOS SDK is installed. If a device won’t run the app, check pairing and Signing & Capabilities first.

[Back to the walkthrough](../README.md) · [Validation notes](VALIDATION.md)
