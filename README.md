# Grasp Graft

`gr-gr` is a coding-agent skill for finding relevant code through an existing Graft index and preserving useful understanding as symbol summaries.
It combines targeted code retrieval with incremental enrichment during ordinary development work.

## Purpose

Help agents choose the right Graft query, avoid redundant source reading, and reuse summaries grounded in implementations they have inspected.
The included helper validates and applies summary updates without changing the graph's structural data.
An API key is optional: agents can maintain symbol summaries themselves, while broader API-backed enrichment uses Graft's native `graft build --deep`.

## Development background

The skill grew out of experiments with a Graft-based workflow during a refactor of a library.
The experiments highlighted an opportunity to retain understanding gained from reading code, along with the repetitive work involved in updating graph metadata manually.
`gr-gr` packages that workflow as a reusable skill and automates the mechanical update steps.
File summaries and concept maps remain the responsibility of Graft's native deep enrichment.

## Usage

See [SKILL.md](SKILL.md) for the workflow and helper commands.
The helper requires Python 3.9 or later and uses only the standard library.

## AI assistance

This skill was developed with assistance from OpenAI Codex.
