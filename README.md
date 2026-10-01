# Grasp Graft

`gr-gr` is a coding-agent skill for finding relevant code through an existing Graft index and preserving useful understanding as symbol summaries.
It combines targeted code retrieval with incremental enrichment during ordinary development work.
Use it when a task requires implementation understanding, symbol or call relationships, or behavior changes.
Tasks that require no implementation understanding can use ordinary file search and comparison; see [SKILL.md](skills/gr-gr/SKILL.md) for the scope guidance.

## Graft versions

At the session's first Graft use, the skill checks the actual CLI or connected MCP server version and selects the corresponding reviewed behavior.
The current compatibility table covers v0.16.0, v0.18.0, v0.19.0, v0.20.0, v0.21.0, and v0.21.1; all reviewed releases support query-time refresh and worktree seeding.
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
Running or recommending `graft init` is prohibited.
If neither a local nor a seedable index is available, the agent explicitly reports this and continues with ordinary source search without creating an index, suggesting creation, or requesting initialization permission.
Automatic refresh does not regenerate stale semantic summaries or update Markdown cards; a changed helper summary batch still needs one normal `graft build` for the retrieval index and cards.

Trail upload, connection, and rule-pull commands require explicit user opt-in because they transmit data or rewrite configuration; interactive `trail push` can also run the init flow in an unwired repository.
On v0.21.0/v0.21.1, `trail pull` also applies accepted changes to agent context files, including instructions, rules, and skills; `claude-md pull` delegates to the same broader operation.
Rules attached to retrieval results are checked separately from implementation summaries and are never copied into them.

## Development background

The skill grew out of experiments with a Graft-based workflow during a refactor of a library.
The experiments highlighted an opportunity to retain understanding gained from reading code, along with the repetitive work involved in updating graph metadata manually.
`gr-gr` packages that workflow as a reusable skill and automates the mechanical update steps.
File summaries and concept maps remain the responsibility of Graft's native deep enrichment.

## Recommended global configuration

This section is user-responsibility, not AI's.

Do not run `graft init` things; instead, apply the following snippet or equivalent form based on your environment and agent.

```toml
[mcp_servers.graft]
command = "graft"
args = ["mcp"]
```

Example above is for Codex (`~/.codex/config.toml`).

### Linux

Add below in the shell environment (e.g., `~/.profile`).

```bash
export GRAFT_NO_GITIGNORE=1
export GRAFT_NO_IGNORE=1
```

Then run:

```bash
mkdir -p ~/.config/git
printf '/graft/\n' >> ~/.config/git/ignore
```

### Windows

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\git" | Out-Null
Add-Content "$HOME\.config\git\ignore" "/graft/"

git config --global core.excludesFile "$HOME/.config/git/ignore"

[Environment]::SetEnvironmentVariable("GRAFT_NO_GITIGNORE", "1", "User")
[Environment]::SetEnvironmentVariable("GRAFT_NO_IGNORE", "1", "User")
```

## AI assistance

This skill was developed with assistance from OpenAI Codex.
