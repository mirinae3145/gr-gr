# Native deep enrichment

Read only after explicit activation through [Optional capabilities](README.md).
First select a reviewed runtime via [Compatibility](compatibility.md), then follow [Retrieval](../retrieval.md) to access the target checkout's graph before a deep build.
If retrieval is already complete and the source and checkout are unchanged, reuse it.
The examples retain `graft`; a reviewed `trail` runtime can use the corresponding code-map commands under [Compatibility](compatibility.md#trail-code-v0220).
On v0.22.0/v0.23.0, learnings in `.trail/learnings/` or the personal Trail home are separate from symbol summaries; do not use `trail note`, `trail learn`, or skill folding as an enrichment substitute.

## Choose a route

| Situation | Route |
| --- | --- |
| Native deep enrichment explicitly requested and API use authorized | Graft's native `graft build --deep` |
| No usable API configuration for a requested deep pass | Report the limitation and continue structural retrieval |
| Native API enrichment fails | Preserve completed results, report the failure, and continue the development task with the available index |

Use the native deep pass for explicitly requested initial or broader semantic enrichment when the API route is authorized.
Let Graft generate and cache file summaries, concept maps, and symbol-level meaning according to its own implementation.
Do not suppress those outputs, invent per-file or per-concept value thresholds, or implement a parallel API summarizer in this skill.

## Honor authorization

Honor existing user authorization and provider/model preferences without asking again.
Credentials being present do not by themselves establish authorization to transmit source or incur API charges.
Use Graft's existing provider configuration and diagnostics; do not require API setup to perform ordinary Graft-assisted work.
When API use requires a new user decision, identify the intended repository scope and native command, and continue unrelated work while that decision is pending.

## Run a deep pass

If enrichment is the first operation, use `graft map` once to enter the local refresh path.
Proceed only with a graph belonging to that checkout and no unresolved freshness failure; never use or copy the parent checkout's graph.
Keep any runtime directory override on the build too, following [v0.23.0 directory selection](compatibility.md#trail-code-v0230) when applicable.

Run from the target repository:

```sh
graft build --deep
```

A deep pass is a native enrichment operation, not a mandatory step after every source edit.
Let retrieval handle ordinary structural freshness; reserve explicit normal builds for authorized missing-index creation under [Retrieval](../retrieval.md) or when current Markdown projections are actually needed.
Respect native caching and failure reporting; do not clear ready summaries or replace the provider merely to force recomputation.
Do not infer discounted Batch API pricing from the `--deep` flag.
