# GitHub Publishing Checklist

Use these settings before making the repository public.

## Repository description

```text
Codex skill for safe LLM model migrations across prompts, agents, API callers, tests, rollout plans, and rollback paths.
```

## Recommended GitHub topics

```text
llm
model-migration
prompt-engineering
ai-agents
codex
openai
anthropic
gemini
developer-tools
llmops
prompt-migration
model-upgrade
```

## Social preview

```text
Headline: ModelPort
Subhead: Safe LLM upgrades for prompts, agents, and production code
Visual: old model -> compatibility map -> validated rollout
```

Use `assets/social-preview.svg` as the starting social preview artwork.

## First-screen README copy

```text
Most model migrations fail after the model ID changes.

ModelPort treats migration as a behavior-preservation problem, not a
search-and-replace task. It separates required compatibility fixes from optional
prompt and agent tuning, then ends every migration with validation evidence and
rollback notes.
```

## Release tags

- `v0.1.0`: first public release with skill workflow, references, examples, and CI.
- `v0.2.0`: provider deep dives and migration regression fixtures.
- `v1.0.0`: stable migration workflow with validated examples across providers.
