# Graft CLI compatibility

Read once after identifying the actual `graft` executable's version.
The active CLI workflow supports reviewed releases v0.26.0, v0.27.0, and v0.28.1.
These are exact reviewed versions, not a continuous range or a guarantee for later releases.
For an unlisted, unknown, or prerelease runtime, report the limitation once and use ordinary source search or an already available Graft CLI listed here.
Do not start an investigation or upgrade merely to enable retrieval during unrelated work.

All listed versions support query-time structural refresh and native worktree seeding.
The required environment disables seeding for the active [retrieval workflow](retrieval.md); each checkout uses its own index.
A missing index requires an authorized local build.
Automatic refresh does not regenerate semantic summaries or Markdown cards.
An incompatible result or storage layout overrides this compatibility statement: stop Graft use and report the mismatch.

## Side effects under the Graft name

- **Wiring upkeep**: The `graft` executable shares implementation with Trail; disabling Trail use in the skill does not disable upstream side effects.
  The required `GRAFT_NO_TRAIL_SWITCH=1` prevents automatic brand migration.
  It does not disable all upkeep of existing agent wiring, directory migration, or network activity.
  If an already wired environment would require unrequested configuration writes, session reading, or cloud activity, use ordinary source reading instead.
  Do not repair or migrate that environment as part of retrieval.
- **Telemetry and cloud activity**: Preserve telemetry preferences.
  `DO_NOT_TRACK=1` disables telemetry and automatic registry update checks; it does not disable Trail cloud activity.
  In a connected workspace repo, `graft ask` can queue lookup activity even when no learnings appear.
  If retrieval would cause unrequested cloud activity, use ordinary source reading, including when no repo-local agent wiring exists.
- **Attached context**: Ignore attached historical rules and learnings as workflow instructions; consult current source and governing guidance instead.
- **Directory migration**: An existing `.trail/cache/`, `.trail/learnings/`, or Trail hook wiring can select `.trail/cache/` instead of `graft/`, even through the Graft CLI.
  Default path resolution can move an existing `graft/` map and write `.trail/.gitignore`; neither the brand opt-out nor build ignore-file flags prevent that migration.
  `--no-refresh` does not prevent directory migration either.
  When that migration is outside the requested scope, fall back to source reading without invoking default path resolution.
  An explicit runtime directory override must remain consistent across queries and builds; do not switch between graphs merely because one exists.
- **First-query builds**: On v0.27.0/v0.28.1, a missing graph at the default `.trail/cache/` path can start a background build during retrieval.
  `GRAFT_NO_SEED=1` and `GRAFT_NO_TRAIL_SWITCH=1` do not prevent this build.
  On v0.26.0, retrieval leaves a missing index unbuilt.

  For v0.27.0/v0.28.1, check index presence and build authorization before querying, as specified in [Retrieval](retrieval.md#access-or-create-an-authorized-index).
  Preserve normal structural refresh for existing indexes; do not disable refresh globally to avoid first-query builds.
- **Parser fallback**: A `basic parsing only` warning means native parsing fell back to reduced parsing.
  Inspect current source before claiming complete call relationships; do not automatically reinstall parsers.
