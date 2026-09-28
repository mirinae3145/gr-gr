# Compatibility

Read once after identifying the actual CLI or connected MCP runtime as instructed in [SKILL.md](../SKILL.md).
Use the matching row below and load the task guidance it names; do not load enrichment instructions for a retrieval-only task.
These are exact reviewed releases, not an inferred continuous version range or a guarantee for every newer release.

## Select the workflow

| Runtime | Workflow | Version-specific differences |
| --- | --- | --- |
| v0.16.0 | Shared [retrieval](retrieval.md) and, when needed, [enrichment](enrichment.md) | No linked Trail rule attachment or `brain`/`trail` CLI commands in this tag |
| v0.18.0 | Same shared workflow | Linked rules attach to source answers; commands use `graft brain` and `init --brain` |
| v0.19.0 | Same shared workflow | Still uses `graft brain` and `init --brain`; push can open signup for an unlinked repository |
| v0.20.0 | Same shared workflow | Commands use `graft trail` and `init --trail`; old spellings remain aliases; interactive push can invoke init in an unwired repository |
| Unlisted, unknown, or prerelease | Ordinary file search and source reading, or an already available reviewed runtime | Report the version or uncertainty once; do not guess compatibility from the version number or GraphV1 schema |

An unreviewed runtime does not stop the user's development task or authorize an upgrade.
Do not start a compatibility investigation during ordinary code work merely to enable Graft; review another version when that is part of the user's task, then extend this table using source and test evidence.
If CLI and MCP use different reviewed releases, apply each runtime's row to its own operations.
An incompatible result or storage layout overrides the table: stop Graft use and report the mismatch.

## Shared lifecycle

All four reviewed tags already run the freshness gate before CLI/MCP retrieval and can seed a linked worktree from its main checkout's existing graph.
They do not automatically build a graph for an ordinary repository that has none.
There is no legacy session-start or branch-switch build workflow to restore for these versions.
Let retrieval refresh structural state before helper selection; after a changed helper batch, retain one explicit normal build for the ask sidecar and Markdown cards.

The GraphV1 fields used by the helper (`meta.version`, `nodes`, `edges`, `body_hash`, `summary_state`, `summary`, `crux`, and `span`) and its source-symbol kinds match these tags.
Keep the helper's schema, identity, hash, prior-summary, and atomic-write safeguards on every application.
Do not maintain per-version helper copies for this shared format.

## Trail command boundaries

On v0.18.0/v0.19.0 the upload, connection, and rule-pull commands are `graft brain push`, `graft brain connect`, and `graft brain pull`; on v0.20.0 they are `graft trail push`, `graft trail connect`, and `graft trail pull`.
All require explicit user opt-in to their side effects under the shared skill policy.
Pull fetches rules and rewrites agent instruction files; upload and connection are not ordinary retrieval operations.
In v0.20.0, interactive push in an unwired repository can invoke init, including graph creation, agent configuration, hooks, and global settings; non-interactive push can still upload without initializing.
Do not use either command spelling to bypass the initialization prohibition.
The init flag names in the table describe compatibility, not permission to invoke init.

## Evidence and verification limits

The shared lifecycle and helper contract were compared directly in `trailhq/Graft` tags v0.16.0 (`aa1e2bb`), v0.18.0 (`de8456e`), v0.19.0 (`597d82f`), and v0.20.0 (`80692e5`).
`src/graph/refresh.ts`, `src/graph/seed.ts`, `src/graph/types.ts`, `src/graph/build.ts`, `src/graph/enrich.ts`, and `src/ask/index-file.ts` are unchanged between these four tags.
The CLI dispatch, MCP tools, and Trail rule attachment were also inspected to establish the differences above.

Basic v0.16.0 operation was historically confirmed through practical use.
Each of v0.16.0, v0.18.0, and v0.19.0 passed 73 focused upstream tests for refresh, seeding, graph serialization, ask indexes, and MCP tools, plus current-helper checks for summary preservation, stale-source rejection, stale-crux clearing, and projection rebuilds.
Cached rule attachment and stale flags were also checked on v0.18.0 and v0.19.0.
These runs used tagged sources in temporary directories with locally available dependencies and `tsx`, not clean installations of each historical release.
Focused installed v0.20.0 CLI/MCP checks passed for missing-index behavior, refresh and worktree seeding, helper summary preservation and projection rebuilds, and cached Trail rule attachment; 77 selected upstream tests passed as well.
Live Trail service operations and API-backed deep enrichment were not validated end to end.
These observations cover the skill's workflow, not every command or integration in each release.
