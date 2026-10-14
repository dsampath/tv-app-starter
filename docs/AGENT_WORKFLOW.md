# Build with Codex or Claude Code

The shared workflow lives in `skills/build-tv-app/SKILL.md`. It points your agent toward the native samples, the starter generator, and the platform build commands. Give it an idea and somewhere new to build, then work through the result together.

## Codex

Open the repository root in Codex. `.agents/skills/build-tv-app` links to the shared skill, so it can be discovered from this checkout. Invoke it with `$build-tv-app` and describe your platform and app idea.

This uses local repository skill discovery. It is not a published Codex marketplace package. Keep the checkout available: the skill uses the sample sources at its repository root.

## Claude Code

From the repository root:

```sh
claude --plugin-dir .
```

The manifest at `.claude-plugin/plugin.json` loads the local plugin. Invoke `/tv-app-starter:build-tv-app` with your request. Check the package structure with:

```sh
claude plugin validate .
```

## A good first request

Ask for one platform, a small offline experience, fictional content, and a fresh destination folder. For example, a reading-list dashboard with three books and a synopsis behind each card.

After the first build, ask for one change at a time: a finished-reading button, larger text, or a different color palette. Try each change with the remote. Your agent can help with implementation and builds; real-device installation still needs your own developer setup and selected device.

The generator copies sample sources and tooling into a new project without original Git history, build products, or credentials. Generated apps include the repository-discovered Codex skill; to load the Claude Code plugin, continue using the original starter checkout with `--plugin-dir`.

For the sibling `reading-room` app from the README, start Claude Code in that
app folder while loading the plugin from the original checkout:

```sh
cd ../reading-room
claude --plugin-dir ../tv-app-starter
```

Then try: `/tv-app-starter:build-tv-app Update the existing app in this folder.
Replace the three dashboard cards with fictional books. Keep its current app ID.`
That tells the agent which project to edit and avoids creating another copy.

The sample includes no model API integration, backend, telemetry, or device credentials. The agent runs in your own Codex or Claude Code environment.

See the [official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference) for host-specific details.

[Back to the walkthrough](../README.md)
