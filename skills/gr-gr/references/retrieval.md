# Retrieval

Read after selecting a reviewed runtime in [Compatibility](compatibility.md), before the first retrieval in a session.
The shared code-map workflow applies to every version listed there.
Only the `graft` CLI is active by default.

## Access or create an authorized index

Before retrieval, establish the checkout's index and permission to create it:

1. First check the [directory migration boundary](compatibility.md#side-effects-under-the-graft-name); even path resolution can move the map and update `.trail/.gitignore`.
1. On v0.27.0/v0.28.1, before the checkout's first retrieval, inspect the filesystem for `<map-dir>/.graph/wiring.json` without invoking Graft's path resolver or a query.
   Use the existing directory override when configured; otherwise determine whether `graft/` or `.trail/cache/` applies under the directory migration boundary.
   If the effective path is unclear or would require an unrequested migration, use ordinary source reading.
   If the graph is missing, apply the build-authorization rule before any query; do not let retrieval start the first build.
1. If the filesystem check or retrieval reports no graph, check the index-creation authorization defined in [Shared boundaries](../SKILL.md#shared-boundaries).
   When authorized for this repository, run one normal `graft build <repo-root>` with a reviewed CLI runtime, then retry the needed retrieval.

   The required environment suppresses normal build-time ignore-file writes, but not directory migration.
   Do not use either init command or add `--deep` under local-index authorization.
   If authorization is absent or creation cannot complete, explicitly tell the user which repository lacks a usable Graft index.
   In either case, continue with ordinary file search and source reading.

Start with the retrieval needed for the task, targeting the intended repository or worktree root explicitly where supported.
Let retrieval check freshness of the target checkout's own index.
Cross-checkout seeding is disabled even when the main checkout has a usable graph; do not copy it or redirect retrieval to it.

## Keep the index fresh

After an index is available, let the next retrieval handle source edits and branch changes.
Do not add a session-start build, branch/HEAD bookkeeping, or a build before each query.
Automatic refresh is structural only; it does not regenerate stale semantic summaries or update Markdown cards.
Semantic enrichment is inactive in the default workflow.
Treat stale summaries as unverified context and check the current source before relying on them.

Respect `--no-refresh`, `GRAFT_NO_REFRESH`, and filesystem-write restrictions; do not bypass a refresh restriction with a manual build.
An authorized new local build with seeding disabled is allowed; copying or seeding another checkout's graph is not.
Graft can answer from the old graph when refresh fails or a rebuild remains busy, so a successful query alone does not guarantee freshness.
If Graft is unavailable or reports a skipped/failed refresh, report the limitation and use ordinary source search until freshness is restored.
Retry a busy operation after the competing writer finishes.

Do not overlap retrieval that may refresh with a build or another graph writer in the same checkout.

## Choose context economically

When first orienting in an unfamiliar indexed repository, use `graft map`.
When the relevant symbol or file is already known, use the matching targeted primitive directly.

| Need | CLI |
| --- | --- |
| Locate and understand implementation | `graft ask "<question>" --source` |
| Every occurrence of a literal | `graft grep "<literal>" --fixed` |
| Definitions and source spans in one file | `graft skeleton <file>` |
| Incoming callers | `graft callers <symbol>` |
| Outgoing relationships | `graft callers <symbol> --direction out` |
| Connected scope before a rename, refactor, or multi-file change | `graft callers <symbol> --depth all` |

`graft check` diagnoses freshness without auto-refresh; it does not replace retrieval's freshness gate.

Use one retrieval that fits the current need, then act on its result.
Do not repeatedly rephrase an unsuccessful `ask`; switch to exhaustive search, structural traversal, or the precise source range that is missing.

## Check each command's options

Use `--in <scope>/` only with `graft ask`, `graft grep`, or `graft callers` to narrow results to a repo-relative path prefix.
`graft map` does not support `--in`: run `graft map [repo-root]` for an overview of the existing index.
Its optional repository-root argument is not a path-prefix filter.
`graft skeleton` does not support `--in`: pass the repo-relative file path as `<file>` instead.
Do not assume options are shared across subcommands; check `graft <command> --help` when unsure.

## Interpret results and fall back

Use `--full` or read the referenced source range when a compact excerpt is insufficient; do not reopen a whole file merely to recover code already returned.
Ranked retrieval is not exhaustive, and graph edges are derived evidence rather than proof of runtime dispatch.
A `basic parsing only` warning means a language fell back from native parsing; do not infer complete or precise call coverage from a successful build.
Resolve declaration/implementation duplicates by path, node ID, and source span, not by name alone.

A zero-hit text response from `grep` can name Git-ignored code that was not searched.
Use ordinary source search in relevant omitted paths; do not change ignore rules or expand the index just to follow that diagnostic.
For files outside the index or an unavailable Graft executable, continue with ordinary file search and source reading.

## Check the affected neighborhood

After changing behavior that may affect callers, dependencies, shared interfaces, or cross-file control flow, use the structural graph to check the affected neighborhood.
Do this before considering the implementation complete.
Prefer targeted traversal from the changed symbols; do not perform this check mechanically after every edit.
