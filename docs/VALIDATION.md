# Validation

Validated October 13, 2026 against the sanitized sample:

- Four Swift core tests pass: daily practice history/streaks, daylight-saving countdowns, invalid request isolation, and state/request round trips.
- tvOS simulator and physical-device SDK builds pass with signing disabled. The sample launches in a fresh tvOS simulator; the dashboard screenshot was visually reviewed.
- Android APK builds and passes signature verification with a newly generated generic debug key. Installed and launched on a fresh Android TV API 34 emulator.
- Android D-pad smoke checks cover tab navigation, selecting a detail card, Back, practice check-offs, appearance switching and relaunch. Light appearance persistence was checked from a fresh screen capture. The active tab retains focus after screen reconstruction.
- Starter generation succeeds with a custom bundle/package ID. Its Android APK builds. A generated starter can itself generate another starter. Existing directories and invalid IDs are rejected.
- Shared skill frontmatter and Claude Code plugin manifest pass their respective validators. This verifies package structure; full model-driven customization and Codex marketplace publishing have not been tested.
- Tracked-text privacy scan passes, and Gitleaks finds no secrets. All committed images were created for this sample and visually reviewed. Only the intended GitHub repository/account references identify the repository owner; no home or account deployment configuration was exported.

Still to verify during owner review: full tvOS remote traversal/Select/Back behavior, light/dark appearance on Apple TV, real-TV installation/signing, TCL-specific firmware behavior, longer-running use and accessibility with actual remotes. Compilation with signing disabled does not constitute an installable Apple TV release. Neither store distribution nor firmware/screensaver replacement is implemented.
