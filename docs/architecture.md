# Composition

The repository is a collection of independently usable plugin directories.
Each owns its skill instructions, supporting references, manifests and version.
The root marketplace provides discovery. It does not impose a workflow on a
consumer repository.

Use `plugins/<name>/skills/<skill>/SKILL.md` for canonical instructions. Add
deterministic scripts or MCP integrations only when a demonstrated workflow
requires them, inside the owning plugin. Host adapters expose capabilities;
they do not become their authority. There is no shared orchestration runtime.

Repository policy belongs to the repository being worked on. Branch names,
required checks, release rules and authorization are resolved there at use time.
Missing capabilities must be reported rather than treated as available
because a skill exists.

Public packages contain their complete skill sources. A fresh clone needs no
private repository access. Updates are deliberate source changes,
with provenance and package versions reviewed together.

## Distribution and activation

GitHub `shk95/agent-rack` is the public distribution source. Codex is primary:
`.agents/plugins/marketplace.json` exposes independently selectable packages.
The secondary `.claude-plugin/marketplace.json` maps to the same directories;
Claude runtime verification is deferred. Neither catalog installs an internal
framework. Consumers select plugins and store activation in host settings.

Use independent plugin versions with synchronized portable/host manifests.
Review source updates and run packaging checks before pushing. Git catalog
refresh and installed-client activation are separate operations. Add release
refs when a stable versioning cadence is established; do not introduce a second
installer while native Codex marketplace management supplies the needed flow.
