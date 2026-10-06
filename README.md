# Agent Rack

Small, personal tools for existing agent harnesses. Each plugin adds an
optional workflow to the environment you already use. Start with one plugin
or one skill.

## Collection

Plugins are added as independent packages under `plugins/`.

## Use the source

Ask your agent to read the selected `SKILL.md` at its checkout path and provide
the target repository and outcome. This requires a harness that can read local
files. Use an absolute source path when the session is anchored elsewhere.
Merely reading a skill does not install tools or change the harness environment.

The default distribution branch is `master`.

## Distribution

Codex is the primary host. The `.agents/plugins/marketplace.json` catalog
discovers independently selectable packages. The secondary Claude Code catalog
is `.claude-plugin/marketplace.json`. Host manifests are discovery adapters;
canonical instructions live in each plugin's `skills/` directory.
Consumers install selected packages and control activation in host settings.

## Development

```sh
python3 tools/validate.py
```

`tools/validate.py` checks package structure, manifest consistency and contained
references using the Python standard library. It does not certify host discovery
or execution behavior. Imported sources and update responsibilities are recorded
in [sources](docs/sources.md); design boundaries are in [architecture](docs/architecture.md).

See [verification status](docs/verification.md).
