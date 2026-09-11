# Grasp Graft

`gr-gr` is a coding-agent skill for finding relevant code through an existing Graft index and preserving useful understanding as symbol summaries.
It combines targeted code retrieval with incremental enrichment during ordinary development work.

## Graft versions

This skill was developed with Graft 0.16.0, with basic operation confirmed through practical use.
The 0.18.0 release was reviewed against 0.16.0 for compatibility; no breaking changes were found in the commands or summary-storage behavior this skill relies on, but an end-to-end run was not performed.
These observations are not a compatibility guarantee.

## Purpose

Help agents choose the right Graft query, avoid redundant source reading, and reuse summaries grounded in implementations they have inspected.
The included helper validates and applies summary updates without changing the graph's structural data.
An API key is optional: agents can maintain symbol summaries themselves, while broader API-backed enrichment uses Graft's native `graft build --deep`.

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
