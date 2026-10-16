# Contributing

Read the [README](README.md) for the project's purpose and [SKILL.md](skills/gr-gr/SKILL.md) for the current workflow.

## Keep the strategy justified

`gr-gr` has two motivations: use the code map without generating repository-local agent instructions, skills, or hooks, and reuse implementation understanding acquired during ordinary work as symbol summaries.
It keeps agent guidance in a separately managed skill and uses upstream retrieval and structural refresh directly.
Generated graph caches are distinct from agent configuration; avoiding the latter does not mean avoiding all local generated files.
These motivations are reasons to reassess the strategy, not permanent requirements to remain different from upstream.

When reviewing an upstream release or changing the workflow, distinguish two questions:

- Does the current strategy still work with the upstream implementation?
- Does it still offer enough benefit over upstream's recommended workflow to justify its extra procedures, helper, and compatibility guidance?

Passing compatibility checks answers the first question, not the second.
Compare the relevant upstream approach with the problem this skill is intended to solve; use source inspection and practical examples where the answer depends on behavior.
Distinguish upstream's recommended setup from its available capabilities: check whether direct commands or a user-level integration already meet the need without repository-local agent files.
Explain which differences remain useful and which can be simplified or removed.
If the strategic comparison is incomplete, state that limit rather than treating compatibility as evidence of continued advantage.

## Active and optional workflows

The default workflow is Graft CLI structural retrieval and authorized normal local builds.
Each checkout uses its own index; keep `GRAFT_NO_SEED=1` on runtime invocations and do not substitute a main checkout's graph.
Incremental summary enrichment, native deep enrichment, MCP, and Trail use are preserved in the [optional bundle](skills/gr-gr/references/optional/README.md), but require an explicit request before their guidance is loaded.

These capabilities and cross-checkout index seeding are disabled by default because the maintainer currently considers the potential side effects to outweigh the benefits they have personally experienced.
This is entirely the maintainer's subjective judgment, not an empirical finding that these features are ineffective or harmful in general.
The decision is provisional: the maintainer may reactivate them later, individually or together.
Preserve the retained procedures and rationale so that reassessment does not require reconstructing the strategy.

Keep dormant procedures out of the default reading path; retain only the side-effect boundaries that still apply to the active Graft executable.
Reviewing or enabling one optional capability must not silently enable another.
An explicit request to use an optional capability does not change the default policy or enable cross-checkout seeding; those require a separate decision to change the policy.
