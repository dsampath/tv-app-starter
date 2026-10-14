# Keep the sample shareable

The starter uses generic content so you can try it without handing it your household data. As you make it yours, keep personal configuration separate from the code you share.

## What went into this repository

The starter was exported into fresh Git history using a selected set of sample sources. Original deployment configuration, bridge services and their data, home network addresses, device identifiers, signing identities, account data, personal photos and screenshots, logs, and unrelated apps were excluded.

The included icons were created for this sample, and the screenshots were captured from fresh sample simulator/emulator sessions. Repository links intentionally identify the GitHub account hosting the project; personal deployment details are not included.

## Before you commit

Stage the files you intend to share, then run this from the repository root:

```sh
python3 scripts/check_privacy.py
```

The scanner reads the current working-tree contents of paths Git tracks, including newly staged files. It checks for common secret patterns, local paths, private network addresses, signing identities, and private/generated file types. It complements secret scanning and visual review. It cannot prove that arbitrary content you add is free of personal information.

Review `git diff --cached` to see exactly what your commit includes, and look at every new screenshot. If you edit a file after staging it, stage the updated version before committing. Keep keys, device settings, account data, personal photos, logs, and signing files local. Check `.gitignore` before adding a new configuration format. Use fictional data when capturing examples for documentation.

If you add a network integration, keep provider credentials on a backend and make connections explicit. Never turn a local setup file into a shared default.

See the [validation notes](VALIDATION.md) for checks completed on the starter, and the [contribution guide](../CONTRIBUTING.md) for sharing changes.

[Back to the walkthrough](../README.md)
