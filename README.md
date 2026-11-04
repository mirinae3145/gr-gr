# Grasp Graft

`gr-gr` is a coding-agent skill for understanding code through the Graft CLI.
It selects targeted code searches and structural queries while keeping agent guidance outside the target repository.
Use it for implementation understanding, symbol or call relationships, and behavior changes; ordinary file search is sufficient for work needing no implementation understanding.

## Default workflow

The active workflow uses `graft ask`, `grep`, `skeleton`, `callers`, and `map`, with query-time structural refresh of the target checkout's own index.
Cross-checkout/worktree seeding is disabled with `GRAFT_NO_SEED=1`; another checkout's graph is not copied or used as a substitute.
A normal local `graft build` can create a missing index when the request or governing instructions authorize it.
Neither `graft init` nor `trail init` is part of this workflow.
Existing summaries remain usable as generated context, but the skill does not write or regenerate semantic content by default.

Start with [SKILL.md](skills/gr-gr/SKILL.md), then load [Compatibility](skills/gr-gr/references/compatibility.md) and [Retrieval](skills/gr-gr/references/retrieval.md) when using Graft.
The reviewed Graft CLI releases are v0.16.0, v0.18.0, v0.19.0, v0.20.0, v0.21.0, v0.21.1, v0.22.0, v0.23.0, and v0.28.1.
An unavailable, unreviewed, or incompatible runtime falls back to ordinary source search without automatic upgrades.
Modern Graft shares implementation with Trail, so the compatibility guidance retains side-effect checks even though Trail use is inactive.
On v0.28.1, inspect the checkout's index before querying so upstream's first-query build cannot bypass index-creation authorization.

## Optional capabilities

Native `build --deep`, MCP, and Trail use are inactive by default.
Their procedures, setup example, and detailed compatibility evidence are preserved together in [Optional capabilities](skills/gr-gr/references/optional/README.md).
Only an explicit request to use or review a named capability opens that guidance; installed tools, credentials, and existing summaries do not activate it.
Reviewing a capability does not authorize execution, and requesting one does not activate the others.
This changes the skill's behavior, not installed programs or connected MCP server configuration.

## Development background

The skill's motivation is to avoid repository-local agent-file generation.
Upstream supports direct builds and queries without initialization; this skill supplies external guidance and explicit boundaries for index creation and runtime side effects.
See [Contributing](CONTRIBUTING.md) for how changes assess both upstream compatibility and the value of this separate strategy.

## Recommended global configuration

This section is user-responsibility, not AI's.
Use an already available, reviewed `graft` CLI; do not run either init command.

Exclude both `/graft/` and `/.trail/cache/` from Git while retaining `.trail/` learnings and shared hooks.
The examples append to an existing `core.excludesFile`, or Git's default global ignore file when that setting is absent.
`GRAFT_NO_GITIGNORE=1` disables normal build-time ignore-file updates; it does not prevent v0.23.0/v0.28.1 directory migration from writing `.trail/.gitignore`.

`GRAFT_NO_SEED=1` disables cross-checkout/worktree index seeding for queries and builds.
It does not disable v0.28.1's first-query build; follow the index check in [Retrieval](skills/gr-gr/references/retrieval.md#access-or-create-an-authorized-index).
After changing persistent environment settings, start a new shell and agent process so they inherit the values.

### Linux

Add below in the shell environment (e.g., `~/.profile`).

```bash
export GRAFT_NO_GITIGNORE=1
export GRAFT_NO_IGNORE=1
export GRAFT_NO_SEED=1
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
[Environment]::SetEnvironmentVariable("GRAFT_NO_SEED", "1", "User")
```

## AI assistance

This skill was developed with assistance from OpenAI Codex.

## License

This project is dedicated to the public domain under [CC0 1.0 Universal](LICENSE.txt).
