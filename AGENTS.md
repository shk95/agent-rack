# Agent Rack development

Agent Rack supplies small, optional utilities for existing agent harnesses.
Keep each plugin independently usable. Use English for source documentation
and skill instructions. User-facing conversation may use the user's language.

Canonical instructions live in `plugins/<plugin>/skills/<skill>/SKILL.md`.
Host manifests are discovery adapters, not copies of workflows. Keep plugin
identity and version consistent across manifests. Do not activate these skills
merely because you are editing their source.

Keep target repository policy out of reusable skills: no fixed branch names,
private paths, host identities or assumptions about installed project tools.
Read policy from the target when a workflow is invoked. A skill grants no
permissions and supplies no missing runtime capabilities.

Record imported source revisions and adaptations in `docs/sources.md`.
Import updates explicitly; do not fetch private sources at installation time.
Keep operational connection files, checkpoints and local settings untracked.
Never copy another repository's complete agent guidance into this one.

Run `python3 tools/validate.py` after package edits. Report structural checks,
host validation, actual discovery and behavioral use as separate evidence.
Do not claim a harness supports an adapter without testing that harness.
