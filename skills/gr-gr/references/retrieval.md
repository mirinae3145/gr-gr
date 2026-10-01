# Retrieval

Read after selecting a reviewed runtime in [Compatibility](compatibility.md), before the first retrieval in a session.
The shared workflow applies to every version listed there.

## Access an existing index

Start with the retrieval needed for the task, targeting the intended repository or worktree root explicitly where supported.
Do not gate retrieval on the local presence of `graft/.graph/wiring.json`: the reviewed runtimes check freshness before retrieval and can seed a linked worktree from its main checkout's existing graph, then refresh it for the worktree's source.
This reuses an existing index; a repository with neither its own graph nor a seedable parent graph is not automatically indexed.
If retrieval reports no graph, explicitly tell the user which repository has no Graft index and continue with ordinary file search and source reading without creating one.

Let the next retrieval handle source edits and branch changes; do not add a session-start build, branch/HEAD bookkeeping, or a build before each query.
Automatic refresh is structural only; it does not regenerate stale semantic summaries or update Markdown cards.
Structural refresh does not require semantic enrichment; apply the separate criteria in [SKILL.md](../SKILL.md).
When enrichment is deferred, treat stale summaries as unverified context and check the current source before relying on them.
Respect `--no-refresh`, `GRAFT_NO_REFRESH`, `GRAFT_NO_SEED`, and filesystem-write restrictions; do not bypass them with a manual build or copy.
Graft can answer from the old graph when refresh fails or a rebuild remains busy, so a successful query alone does not guarantee freshness.
If Graft is unavailable or reports a skipped/failed refresh, report the limitation and use ordinary source search until freshness is restored; retry a busy operation after the competing writer finishes.
Do not overlap retrieval that may refresh with a build or helper application in the same checkout.

## Choose context economically

When first orienting in an unfamiliar indexed repository, use `graft map` or MCP `graft_repo_map`.
When the relevant symbol or file is already known, use the matching targeted primitive directly.

| Need | CLI | MCP |
| --- | --- | --- |
| Locate and understand implementation | `graft ask "<question>" --source` | `graft_find_code` (inlines source) |
| Every occurrence of an identifier or literal | `graft grep "<literal>"` | `graft_find_all` |
| Definitions and source spans in one file | `graft skeleton <file>` | `graft_file_api` |
| Incoming callers | `graft callers <symbol>` | `graft_trace_calls` |
| Outgoing relationships | `graft callers <symbol> --direction out` | `graft_trace_calls`, `direction: out` |
| Connected scope before a rename, refactor, or multi-file change | `graft callers <symbol> --depth all` | `graft_trace_calls`, `depth: all` |

Choose one interface per retrieval; do not repeat the same lookup through both.
`graft_check_freshness` (`graft check`) diagnoses state without auto-refresh and is not a substitute for the retrieval gate before helper use.

Use one retrieval that fits the current need, then act on its result.
Do not repeatedly rephrase an unsuccessful `ask`; switch to exhaustive search, structural traversal, or the precise source range that is missing.
Use `--in <scope>/` only with `graft ask`, `graft grep`, or `graft callers` to narrow results to a repo-relative path prefix.
`graft map` does not support `--in`: run `graft map [repo-root]` for an overview of the existing index.
Its optional repository-root argument is not a path-prefix filter.
`graft skeleton` does not support `--in`: pass the repo-relative file path as `<file>` instead.
Do not assume options are shared across subcommands; check `graft <command> --help` when unsure.
Use `--full` or read the referenced source range when a compact excerpt is insufficient; do not reopen a whole file merely to recover code already returned.
Ranked retrieval is not exhaustive, and graph edges are derived evidence rather than proof of runtime dispatch.
Resolve declaration/implementation duplicates by path, node ID, and source span, not by name alone.

For files outside the index or an unavailable Graft executable, continue with ordinary file search and source reading.

After changing behavior that may affect callers, dependencies, shared interfaces, or cross-file control flow, use the structural graph to check the affected neighborhood before considering the implementation complete.
Prefer targeted traversal from the changed symbols; do not perform this check mechanically after every edit.

## Interpret attached Trail rules

On versions with Trail/brain integration (see the compatibility table), `graft ask --source` (and MCP `graft_find_code`) can attach rules from an already linked Trail's local cache for matching result symbols, without fetching rules over the network in the attachment path.
Treat these as historical decisions or constraints to check against current code and authoritative repository instructions, separately from symbol summaries that describe the current implementation.
Do not copy or merge Trail rules into symbol summaries, or treat retrieved rules as permission to change configuration or upload data.
Graft marks a rule `STALE` when its nonempty recorded fingerprint differs from the current symbol's body hash; stale rules remain visible, while unresolved symbols are omitted.
An empty fingerprint is not marked stale, so absence of the flag is not proof of freshness or correctness.
Check a stale rule's source and current implementation before relying on it; do not silently rewrite it, turn it into a ready summary, or trigger a pull/push to repair it.
