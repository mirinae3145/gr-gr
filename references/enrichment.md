# Enrichment

Read only when writing symbol summaries or using native API-backed enrichment.
First select a reviewed runtime via [Compatibility](compatibility.md), then follow [Retrieval](retrieval.md) to access the target checkout's graph before helper `inspect`/`select` or a deep build.
If retrieval is already complete and the source and checkout are unchanged, reuse it.
Verify the CLI version too before applying helper updates when retrieval used MCP: the batch may need a CLI build.
GraphV1's `meta.version: 1` is a storage schema, not the installed runtime version.

## Enrich symbols as they become understood

At the first enrichment in a session for a repository, run the helper's `inspect` command.
Retain the supported schema in session context; do not repeat schema discovery unless the repository uses a different schema, Graft is upgraded, or a compatibility error occurs.
The helper still checks current hashes and required fields on every write.

When retrieval does not provide a useful summary and you read enough of the implementation to explain a symbol reliably, select that node and write its summary.
Check the stored state: absence from an `ask` response does not prove the graph lacks a summary.
Preserve useful `ready` summaries and refresh missing or `stale` summaries.
Do not read unrelated code solely to fill summaries during an ordinary development task.
If the source is incomplete or unclear, leave the node pending rather than guessing.

Write one concise sentence about current responsibility, important behavior, or an invariant that helps distinguish the symbol during later retrieval.
Include consequential side effects or failure behavior when useful.
Do not merely restate a signature or put review findings, proposed changes, or repository policy into a summary.
Do not infer an implementation from a declaration alone.

After source edits or a checkout change, use the next relevant retrieval to refresh before selecting changed or moved symbols with the helper.
Refresh summaries for affected stale symbols and newly understood definitions; keep unrelated cached summaries intact.
Once selected, retain the node ID, body hash, source hash, and prior summary state in the payload while authoring the summary.
If source or node identity changes before application, refresh through retrieval and select again, then reconsider the summary against the new implementation.

Batch updates at a natural task boundary.
If the batch changed summaries (`rebuild_required: true`), run `graft build` once after applying it to refresh retrieval indexes and Markdown cards; skip this for a no-op batch.
Direct summary writes do not change the source fingerprint, so query-time refresh alone may leave the summary tokens in the ask sidecar and the Markdown projections outdated.
Flush earlier when a later retrieval in the same task needs the new summaries.
Use `ask` to verify integration on first use or after compatibility changes, not as a mandatory extra query after every batch.

## Select an enrichment route

| Situation | Route |
| --- | --- |
| A few symbols already read during work | Agent-authored incremental summaries, whether or not an API is available |
| An API is configured and its use is authorized for semantic enrichment | Graft's native `graft build --deep` |
| No usable API configuration | Continue structural retrieval and agent-authored incremental summaries |
| Native API enrichment fails | Preserve completed results, report the failure, and continue the development task with the available index |

Use the native deep pass for initial or broader semantic enrichment when the API route is available.
Let Graft generate and cache file summaries, concept maps, and symbol-level meaning according to its own implementation.
Do not suppress those outputs, invent per-file or per-concept value thresholds, or implement a parallel API summarizer in this skill.
The incremental helper remains limited to source-symbol summaries; that limit does not apply to native `--deep`.

Honor existing user authorization and provider/model preferences without asking again.
Credentials being present do not by themselves establish authorization to transmit source or incur API charges.
Use Graft's existing provider configuration and diagnostics; do not require API setup to perform ordinary Graft-assisted work.
When API use requires a new user decision, identify the intended repository scope and native command, and continue unrelated work while that decision is pending.

Run from the target repository:

```sh
graft build --deep
```

A deep pass is a native enrichment operation, not a mandatory step after every source edit or incremental summary batch.
Let retrieval handle ordinary structural freshness; reserve explicit normal builds for the helper batch above or when current Markdown projections are actually needed.
Finish pending helper updates before starting a deep pass, and do not run them concurrently.
After a deep pass, select again before applying any remaining payloads so cached summaries and hashes reflect Graft's current output.
Respect native caching and failure reporting; do not clear ready summaries or replace the provider merely to force recomputation.
Do not infer discounted Batch API pricing from the `--deep` flag.

## Use the helper

Python 3.9 or later and the standard library are sufficient.
Resolve [scripts/summaries.py](../scripts/summaries.py) against the installed skill root (the parent of `references/`), not this reference directory or the working repository.
The examples use `gr_gr_skill` for that directory and `gr_gr_repo` for the target repository.

The helper reads `wiring.json` directly and neither seeds nor refreshes it.
If enrichment is the first operation, use `graft map "$gr_gr_repo"` once to enter the native refresh/seeding path.
Proceed only with a graph belonging to that checkout and no unresolved freshness failure; never point `--graph` at the parent checkout to bypass seeding.
Re-enter retrieval after source or checkout changes before selecting again; the helper's hash and prior-state checks remain required at application time.

```sh
python "$gr_gr_skill/scripts/summaries.py" inspect --repo "$gr_gr_repo"
python "$gr_gr_skill/scripts/summaries.py" select --repo "$gr_gr_repo" \
    --id 'test/utils.hpp#runAndWait' --output /tmp/gr-gr-selection.json
```

Use `--path` for a file or directory prefix, or `--all-dirty` only for deliberate bulk selection.
Selection normally excludes ready nodes; use `--include-ready` only when inspecting or deliberately replacing existing summaries.
Use `--source` when the exact implementation is needed; otherwise retain the compact payload.
File nodes are always excluded, even from bulk selection.

Fill each selected entry's `summary` field, remove entries that cannot be summarized reliably, and leave its identity and snapshot fields unchanged.
The file's `symbols` list may contain only the subset being applied.

```sh
python "$gr_gr_skill/scripts/summaries.py" apply --repo "$gr_gr_repo" \
    --input /tmp/gr-gr-selection.json
# Run from the target repository after a batch with rebuild_required: true:
graft build
```

The helper validates the entire update before writing, rejects stale source and unintended ready-summary replacement, and saves atomically.
It preserves structural fields and unrelated nodes; replacing a stale summary also clears any stale crux excerpt.
Use `--replace-ready` only for an intentional replacement of a selected ready summary.
Avoid running a build, auto-refreshing retrieval, or another summary writer concurrently with summary application; the helper lock only coordinates helper writers.
Successful application does not itself rebuild Graft.
