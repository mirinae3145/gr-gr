# Grasp Graft

`gr-gr` is a coding-agent skill for finding relevant code through an existing Graft index and preserving useful understanding as symbol summaries.
Graft is now the code-map component of Trail-code; this skill retains its name and focuses on that map and its symbol summaries.
It combines targeted code retrieval with incremental enrichment during ordinary development work.
Use it when a task requires implementation understanding, symbol or call relationships, or behavior changes.
Tasks that require no implementation understanding can use ordinary file search and comparison; see [SKILL.md](skills/gr-gr/SKILL.md) for the scope guidance.

## Graft versions

At the session's first Graft use, the skill checks the actual CLI or connected MCP server version and selects the corresponding reviewed behavior.
The current compatibility table covers v0.16.0, v0.18.0, v0.19.0, v0.20.0, v0.21.0, v0.21.1, v0.22.0, and v0.23.0; all reviewed releases support query-time refresh and worktree seeding.
An unlisted or unverifiable runtime is reported once, and work continues through ordinary source search without automatic upgrades or initialization.
See [Compatibility](skills/gr-gr/references/compatibility.md) for version-specific differences, evidence, and verification limits.

## Progressive loading

[SKILL.md](skills/gr-gr/SKILL.md) contains the shared boundaries and selects the guidance needed for the task.
Agents read [Compatibility](skills/gr-gr/references/compatibility.md) at first use, [Retrieval](skills/gr-gr/references/retrieval.md) when querying code, and [Enrichment](skills/gr-gr/references/enrichment.md) only when writing summaries or using native deep enrichment.
Shared behavior has one maintained definition; version differences are recorded in the compatibility table rather than separate copies of the skill or helper.

## Purpose

Help agents choose the right Graft query, avoid redundant source reading, and reuse summaries grounded in implementations they have inspected.
The included helper validates and applies summary updates without changing the graph's structural data.
An API key is optional: agents can maintain symbol summaries themselves, while broader API-backed enrichment uses Graft's native `graft build --deep`.

The reviewed Graft versions handle structural freshness, including source edits and branch switches, and can seed a linked worktree from its main checkout's existing graph.
The skill lets retrieval run before the helper reads the graph, without a local-index precheck or a redundant session-start build.
Running or recommending `graft init` or `trail init` is prohibited.
If neither a local nor a seedable index is available, the agent may create a local index with a normal build when the current user request or applicable instructions authorize it for that repository.
Authorization can come from global, workspace, repository, or task-specific guidance, subject to its scope and the governing instruction hierarchy; existing authorization does not need to be repeated in the prompt.
Without authorization, the agent reports the missing index and continues with ordinary source search without suggesting creation or requesting initialization permission.
See [Retrieval](skills/gr-gr/references/retrieval.md) for the build procedure; local-index authorization does not include deep API enrichment, uploads, or configuration changes.
Automatic refresh does not regenerate stale semantic summaries or update Markdown cards; a changed helper summary batch still needs one normal `graft build` for the retrieval index and cards.

Historical Trail/brain upload, connection, and rule-pull commands require explicit user opt-in because they transmit data or rewrite configuration.
On v0.21.0/v0.21.1, `graft trail pull` also applies accepted changes to agent context files; those command groups are absent in v0.22.0/v0.23.0.
In v0.22.0/v0.23.0, `@nanonets/graft` provides `graft` and `@trailhq/trail-code` provides `trail`.
Both expose the code map, but `graft check` maps to `trail build --check`; `trail check` checks changes against learnings and skills.
The MCP server advertises `graft_*` or `trail_*` tools according to its entrypoint.
Rules and local learnings attached to retrieval results are checked separately from implementation summaries and are never copied into them.
Learning storage, skill folding, automatic wiring migration, and cloud synchronization remain outside ordinary code-map retrieval and summary enrichment; see [Compatibility](skills/gr-gr/references/compatibility.md#trail-code-v0220) for the boundaries.

In v0.23.0, Trail repositories use `.trail/cache/` for the code map and can move an existing `graft/` map there during retrieval.
Use the helper's explicit `--graph` option for that location; see [v0.23.0 compatibility](skills/gr-gr/references/compatibility.md#trail-code-v0230) for directory selection and migration boundaries.

## Development background

The skill grew out of experiments with a Graft-based workflow during a refactor of a library.
The experiments highlighted an opportunity to retain understanding gained from reading code, along with the repetitive work involved in updating graph metadata manually.
`gr-gr` packages that workflow as a reusable skill and automates the mechanical update steps.
File summaries and concept maps remain the responsibility of Graft's native deep enrichment.

## Recommended global configuration

This section is user-responsibility, not AI's.

Do not run `graft init` or `trail init`; instead, apply the following snippet or equivalent form based on your environment and agent.

```toml
[mcp_servers.graft]
command = "graft"
args = ["mcp"]
```

Example above is for Codex (`~/.codex/config.toml`).
Keep an existing verified configuration; the renamed package does not require replacing it.
For a user-selected `trail` installation, `command = "trail"` with `args = ["mcp"]` exposes the corresponding `trail_*` tools.

Exclude both `/graft/` and `/.trail/cache/` from Git while retaining `.trail/` learnings and shared hooks.
The examples append to an existing `core.excludesFile`, or Git's default global ignore file when that setting is absent.
`GRAFT_NO_GITIGNORE=1` disables normal build-time ignore-file updates; it does not prevent v0.23.0 directory migration from writing `.trail/.gitignore`.

### Linux

Add below in the shell environment (e.g., `~/.profile`).

```bash
export GRAFT_NO_GITIGNORE=1
export GRAFT_NO_IGNORE=1
```

Then run:

```bash
gr_gr_ignore=$(git config --global --path --get core.excludesFile)
if [ -z "$gr_gr_ignore" ]; then
    gr_gr_ignore="${XDG_CONFIG_HOME:-$HOME/.config}/git/ignore"
fi
mkdir -p "$(dirname "$gr_gr_ignore")"
printf '\n/graft/\n/.trail/cache/\n' >> "$gr_gr_ignore"
```

### Windows

```powershell
$grGrIgnore = git config --global --path --get core.excludesFile
if (-not $grGrIgnore) {
    $grGrConfig = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }
    $grGrIgnore = Join-Path $grGrConfig "git/ignore"
}
New-Item -ItemType Directory -Force (Split-Path -Parent $grGrIgnore) | Out-Null
Add-Content -Path $grGrIgnore -Value "`n/graft/`n/.trail/cache/"

[Environment]::SetEnvironmentVariable("GRAFT_NO_GITIGNORE", "1", "User")
[Environment]::SetEnvironmentVariable("GRAFT_NO_IGNORE", "1", "User")
```

## AI assistance

This skill was developed with assistance from OpenAI Codex.
