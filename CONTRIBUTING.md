# Contributing

Keep examples offline and generic. Use a separate branch, describe the observable behavior, and include build/test evidence for the platform you change. Preserve TV remote focus, Back navigation and couch-readable text. New network features need opt-in configuration and no embedded credentials.

Run `swift test`, build the affected native app, test the relevant remote flow, and run `python3 scripts/check_privacy.py` after staging. Review media visually and keep logs, binaries, signing keys, real device IDs and personal content out of commits. Supply screenshots from a clean simulator or emulator. Do not change repository visibility as part of an ordinary contribution.
