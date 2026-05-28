# ModelPort

[![CI](https://github.com/forkxp/migration-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/forkxp/migration-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827)](SKILL.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Status: Alpha](https://img.shields.io/badge/Status-v0.1_Alpha-blue)](docs/PUBLISHING.md)

![ModelPort social preview](assets/social-preview.svg)

**Production-grade LLM migrations: Swap models safely across agents, prompts, and code.**

An AI agent skill for safe, production-grade LLM model migrations. Automate behavior-preserving upgrades across prompts, agents, API callers, and tests.

**The Problem:** Most model migrations fail after you change the model ID because search-and-replace breaks tool calling, parser behavior, and orchestration.  
**The Solution:** ModelPort treats migration as a behavior-preservation problem: it maps callers, separates required compatibility fixes from optional tuning, and mandates validation before finishing.

## Why teams use it

- Replace deprecated model IDs without breaking runtime calls.
- Preserve output contracts, parser behavior, and tool calling.
- Separate required compatibility fixes from optional prompt tuning.
- Choose direct swap, adapter, shadow mode, canary, or phased rollout.
- Produce validation evidence and rollback notes.

## Quick start

Clone:

```bash
git clone https://github.com/forkxp/migration-skill.git
cd migration-skill
```

Install as a local Codex skill with a symlink:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)" ~/.codex/skills/modelport-skill
```

Or copy directly:

```bash
mkdir -p ~/.codex/skills/modelport-skill
cp -R . ~/.codex/skills/modelport-skill
```

Then ask Codex:

```text
Use $modelport-skill and the starter prompt template to migrate
services/assistant from Model A to Model B. Keep tool behavior stable, separate
required fixes from optional tuning, and include validation evidence plus
rollback notes.
```

For detailed migration requests, start from
[templates/migration-starter-prompt.md](templates/migration-starter-prompt.md).

## What it helps migrate

| Area | Migration support |
| --- | --- |
| API callers | Model IDs, request parameters, response contracts, SDK usage |
| Prompts | System prompts, templates, output contracts, brittle prompt hacks |
| Agents | Tool policy, orchestration behavior, autonomy, handoff instructions |
| Tools | Schemas, descriptions, validation rules, guardrails |
| Config | Model registries, routers, feature flags, rollout controls |
| Tests and docs | Fixtures, assertions, examples, migration notes |

## Built for real migrations

- Scope lock before edits to avoid accidental repo-wide churn.
- Discovery pass across API calls, prompts, agents, tools, tests, and docs.
- File classification before modification.
- Migration-pattern selection across direct swap, adapters, shadow mode, canary,
  and expand-contract changes.
- Required fixes and optional tuning reported separately.
- Explicit coordination checks for work another agent has already started.
- Validation-first completion criteria with tests, smoke checks, and rollback
  notes.

## Example migration prompts

- "Migrate all model usage in `src/agents/` from our old model config to the new
  release, keep tool behavior stable, and give me a rollback plan."
- "Upgrade this codebase from provider A to provider B and adjust prompts so
  output format remains identical."
- "Replace deprecated model parameters in our API callers and verify tests still
  pass."
- "Do a phased migration in `services/search` with side-by-side support for old
  and new models."

More examples are in [examples/example-prompts.md](examples/example-prompts.md).

## Expected output

The skill guides Codex to produce a migration report with:

- Migration summary
- Scope and files changed
- Existing work and remaining work
- Required compatibility fixes
- Prompt and agent behavior tuning
- Validation results
- Proof evidence
- Risks and follow-up recommendations
- Rollback notes

See [examples/example-output.md](examples/example-output.md) for a sample report.

## Repository structure

```text
.
├── .markdownlint-cli2.yaml
├── SKILL.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── assets/
│   └── social-preview.svg
├── scripts/
│   └── validate_skill.py
├── templates/
│   └── migration-starter-prompt.md
├── references/
│   ├── migration-patterns.md
│   ├── migration-playbook.md
│   ├── prompt-template-research.md
│   ├── provider-checklists.md
│   └── validation-proof.md
├── examples/
│   ├── example-prompts.md
│   └── example-output.md
├── agents/
│   └── openai.yaml
├── docs/
│   └── PUBLISHING.md
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── pull_request_template.md
    └── workflows/ci.yml
```

## Validate locally

```bash
python3 scripts/validate_skill.py .
npx markdownlint-cli2 "**/*.md"
```

## Open-source readiness

- MIT license included.
- CI validates Markdown and skill structure.
- Issue templates cover bugs, features, and migration case studies.
- PR template asks contributors to classify migration relevance.
- Security reporting process included via GitHub Security Advisories.
- Skill UI metadata included in `agents/openai.yaml`.

## Roadmap

- Add provider-specific deep dives for OpenAI, Anthropic, Gemini, and
  self-hosted models.
- Add regression fixtures for prompt, tool, and structured-output migrations.
- Add benchmark examples for latency, token usage, and output contract drift.
- Add real-world before/after migration case studies.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

MIT - see [LICENSE](LICENSE).
