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

Complete the [Required global configuration](#required-global-configuration) before using the skill.
Start with [SKILL.md](skills/gr-gr/SKILL.md), then load [Compatibility](skills/gr-gr/references/compatibility.md) and [Retrieval](skills/gr-gr/references/retrieval.md) when using Graft.

The active CLI workflow supports reviewed Graft releases v0.26.0, v0.27.0, and v0.28.1.
An unavailable, unlisted, or incompatible runtime falls back to ordinary source search without automatic upgrades.
Modern Graft shares implementation with Trail, so the compatibility guidance retains side-effect checks even though Trail use is inactive.
On v0.27.0/v0.28.1, inspect the checkout's index before querying so upstream's first-query build cannot bypass index-creation authorization.

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

## Required global configuration

The user must complete this setup before using the skill and maintain it for every runtime used with the skill.
The skill assumes these prerequisites are satisfied; it does not routinely inspect or repair them.
Use an already available, reviewed `graft` CLI; do not run either init command.

Set the following variables in the environment inherited by the agent and CLI, and by any explicitly enabled MCP server or Trail runtime:

| Variable | Required value | Effect |
| --- | --- | --- |
| `GRAFT_NO_GITIGNORE` | `1` | Suppresses normal build-time `.gitignore` updates |
| `GRAFT_NO_IGNORE` | `1` | Suppresses normal build-time `.ignore` updates |
| `GRAFT_NO_SEED` | `1` | Disables cross-checkout/worktree index seeding |
| `GRAFT_NO_TRAIL_SWITCH` | `1` | Prevents automatic brand migration from Graft to Trail |

Exclude both `/graft/` and `/.trail/cache/` from Git while retaining `.trail/` learnings and shared hooks.
The platform examples append to an existing `core.excludesFile`, or Git's default global ignore file when that setting is absent.

These settings do not prevent directory migration, all existing wiring upkeep, or cloud activity.
They also do not prevent first-query builds in v0.27.0/v0.28.1.
The skill retains the corresponding checks in [Compatibility](skills/gr-gr/references/compatibility.md) and [Retrieval](skills/gr-gr/references/retrieval.md).

### Linux

Add these exports to the environment used to launch the agent and CLI, for example `~/.profile` for a login shell.
For WSL, configure the Linux environment where Graft runs; Windows user variables alone do not establish these prerequisites.

```bash
export GRAFT_NO_GITIGNORE=1
export GRAFT_NO_IGNORE=1
export GRAFT_NO_SEED=1
export GRAFT_NO_TRAIL_SWITCH=1
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

Run the following in PowerShell to register the global ignore entries and persistent user environment variables:

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
[Environment]::SetEnvironmentVariable("GRAFT_NO_TRAIL_SWITCH", "1", "User")
```

### Verify the setup

Complete these checks once after setup and after changing the runtime launcher or its environment:

1. Restart the shell, agent launcher, and any explicitly enabled MCP server so they inherit the configured values.
1. Confirm that all four variables equal `1` in each runtime's actual environment.
   A shell profile or persistent Windows user value alone does not prove that an already running process inherited it.
1. Confirm that the effective global Git ignore file contains `/graft/` and `/.trail/cache/`.

These prerequisites do not authorize index creation, optional capabilities, API use, or configuration changes during ordinary retrieval.

## AI assistance

This skill was developed with assistance from OpenAI Codex.

## License

This project is dedicated to the public domain under [CC0 1.0 Universal](LICENSE.txt).
