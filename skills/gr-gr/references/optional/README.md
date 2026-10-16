# Optional capabilities

Incremental summary enrichment, native `build --deep`, MCP, and Trail are inactive by default.
Read this bundle only when the user explicitly requests one of these capabilities or asks to review it.
An installed tool, API key, existing graph summary, attached learning, or generic request to use Graft is not activation.
A review request authorizes inspection, not execution; enabling one capability does not enable the others.
For the requested capability only, the relevant optional guidance replaces the default inactivity boundary.
Keep the default [Graft CLI workflow](../../SKILL.md) for everything outside that request.
Do not change installations, persistent settings, or agent wiring merely to activate a workflow.
Neither `graft init` nor `trail init` is allowed.
Cross-checkout seeding remains disabled when an optional capability is requested; historical seeding support in the retained compatibility evidence does not activate it.
Keep `GRAFT_NO_SEED=1` on CLI operations and any explicitly requested MCP server; do not assume an existing server inherited it.
If that server's seeding configuration cannot be verified, use the verified CLI or ordinary source search.

| Explicit request | Read |
| --- | --- |
| Maintain symbol summaries incrementally | [Enrichment](enrichment.md) and the relevant [compatibility](compatibility.md) entry |
| Use native `build --deep` | [Enrichment](enrichment.md#select-an-enrichment-route) and the relevant [compatibility](compatibility.md) entry |
| Use MCP | [Optional retrieval](retrieval.md) and the actual server's [compatibility](compatibility.md) entry |
| Use Trail CLI or review its integrations | [Compatibility](compatibility.md) and, for retrieval, [Optional retrieval](retrieval.md) |

Trail learning storage, skill folding, session/PR reading, and cloud operations have no general execution recipe here.
For a request involving them, inspect the current upstream behavior and establish the requested operation's scope; code-map authorization alone is insufficient.
Credentials do not authorize source transmission or API charges.
Preserve the user's provider/model choices and existing authorization.

## Incremental enrichment criteria

These criteria apply only after incremental enrichment has been explicitly requested.
Structural retrieval and semantic enrichment are separate decisions; reading or editing a symbol does not by itself require summary maintenance.
Update summaries when the task yields reusable understanding of a symbol's responsibility, important behavior, or invariant, or reveals that an existing summary misrepresents the current implementation.
For a local edit that adds no such understanding and leaves the summary's meaning unchanged, skip enrichment, including helper inspection and explicit builds for summary maintenance.
Choose by semantic value and accuracy, not the number of functions or lines changed; missing or `stale` state alone does not require enrichment.

## Retained setup example

Only for an explicitly requested MCP setup; preserve an existing verified configuration.
For Codex, a user-level server can be declared as follows:

```toml
[mcp_servers.graft]
command = "graft"
args = ["mcp"]
```

For a separately requested, reviewed Trail runtime, `command = "trail"` exposes the corresponding tools.
Runtime setup is distinct from enabling use in this skill.
