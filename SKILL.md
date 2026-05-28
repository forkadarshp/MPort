---
name: modelport-skill
description: Use when the user asks to migrate, upgrade, or port prompts, agents, tools, or codebases from one LLM model or provider version to another. Also use when auditing or continuing migration work started by another agent. Covers API calls, prompt assets, agent configs, tool definitions, tests, docs, runtime settings, rollout plans, and handoff coordination.
---

# ModelPort Skill

Production-grade LLM migrations. Swap models safely across agents, prompts,
and code.

## Default Output Mode

Every response from this skill is hyper-concise. No exceptions unless the user
explicitly requests verbose output.

- No conversational filler, no pleasantries, no intro/outro.
- Dense bullet points. Omit verbs where possible.
- `->` for state transitions (e.g. `GPT-4 -> Claude-3`).
- Code diffs only — never reprint entire files.
- State only: what changed, why, what was validated.
- Every token must earn its place.

## Operating Principles

Adapted from the Karpathy guidelines for AI coding agents, applied to
migration work.

### Think before editing

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly. If uncertain, ask.
- Multiple interpretations exist → present them, don't pick silently.
- Scope ambiguous → ask one scope-selection question, wait.
- Check existing work: branch/PR context, issue notes, handoff files,
  another agent's partial implementation. Understand before editing.

### Simplicity first

Minimum change that solves the migration. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use paths.
- No "flexibility" that wasn't requested.
- If you wrote 50 lines and it could be 10 diffs, rewrite.

### Surgical changes

Touch only what must change. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Required fixes ≠ optional tuning — never mix, always label.
- Preserve backward-compatible paths unless user says remove them.

### Goal-driven execution

Define success criteria before writing code. Loop until verified.

- Transform vague tasks into verifiable goals.
- "Migrate X" → tests pass + smoke request succeeds + contract holds.
- Run validation after each meaningful change.
- If a check fails: diagnose → patch narrowly → retry the failed check.
- Don't claim completion without proof evidence.

### Iterative & targeted

Plan thoroughly, execute in phases.

- Research the codebase fully before implementation starts.
- Pick a targeted section (e.g., one component, one workflow) — no whole-repo big bangs.
- Implement and validate phase-by-phase.

## Inputs

Collect before editing:

- Source model/provider/version → destination model/provider/version
- Scope: exact files, directories, or whole repo
- Migration mode:
  - In-place replacement
  - Side-by-side dual-model support
  - Phased rollout with feature flags
- Constraints: latency, cost, output format, safety/compliance
- Success criteria: quality, speed, token/cost, compatibility
- Evidence requirements: unit tests, evals, live smoke checks, rollout metrics

If source or target matches a model with a dedicated guide in
`references/models/`, read that guide before proceeding. Model guides contain
changelogs, breaking changes, migration steps, and version-specific quirks.

Scope not explicit → ask once, wait.

## Workflow

### Phase 0: Scope lock

Define exactly what will be migrated. Narrow down to a targeted section. Establish current state.

- Inspect VCS status, branch/PR context, issue notes, migration plans,
  handoff files.
- Separate: done vs. needs-validation vs. in-progress vs. not-started.
- Identify work that appears unrelated, incomplete, or owned by another agent.
- Do not edit until scope is confirmed, targeted, and current state is understood.

### Phase 1: Discovery scan

Map the migration surface:

- API call sites: SDK/client usage, model IDs, request params
- Prompt assets: system prompts, templates, chains
- Agent configs: tool policy, autonomy/delegation behavior
- Tool definitions: schemas, descriptions, guardrails
- Registries/config/tests/docs referencing model names

Read:

- `references/migration-playbook.md`
- `references/provider-checklists.md`
- `references/models/<model>.md` — when source or target matches a model with
  a dedicated guide (e.g. `claude-opus-4-8.md`, `claude-opus-4-6.md`,
  `claude-sonnet-4-5.md`, `gpt-5-5.md`)
- `references/prompt-template-research.md` — when creating or improving a
  migration prompt or reusable migration request
- `references/migration-patterns.md` — when choosing rollout strategy,
  adapters, feature flags, or side-by-side support
- `references/validation-proof.md` — when planning proof gates, evals,
  smoke tests, or diagnose-patch-retry loops

### Phase 2: Classify before editing

Classify each hit:

- **Runtime caller** — code that sends model requests
- **Definer/registry** — model catalogs, routing, capability maps
- **Prompt/behavior layer** — prompt templates, safety policy
- **Agent/tool layer** — tool specs, usage policy, orchestration hints
- **Reference/test/docs** — assertions, docs, examples, fixtures

Choose action per category:

- Replace
- Add alongside
- Keep and annotate
- Regenerate (generated files only)

### Phase 3: Migration design

Thoroughly plan and research before implementation starts. Compact migration spec:

- What is already implemented (by whom, if known)
- What remains
- Which pattern: direct swap, branch-by-abstraction, strangler routing,
  expand-contract, shadow mode, canary rollout
- Breakdown of iterative phases for implementation
- Required to prevent breakage
- Optional tuning for better performance
- Validation plan: tests + runtime checks + regression checks + proof
- Rollback strategy

Provider-specific unknowns → flag and ask before risky edits.
Do not start Phase 4 until this design is complete and phase boundaries are clear.

### Phase 4: Implementation

Apply in order:

1. Runtime/API compatibility edits
2. Prompt and behavior tuning
3. Agent and tool behavior updates
4. Config, registry, tests, docs synchronization

Precise edits only. No repo-wide blind search-and-replace.

### Phase 5: Validation

Run:

- Unit/integration tests for modified files
- Lint/type-check where applicable
- At least one real smoke test on destination model
- Output-contract or prompt-eval checks when prompts/parsers changed

Verify:

- Request success (no parameter/model errors)
- Expected stop/finish behavior
- Tool invocation still aligned
- Output shape/format still satisfied
- Observability signals defined for staged rollout when production risk exists

Failure → diagnose root cause → patch smallest responsible surface → retry
failed check before claiming completion.

### Phase 6: Report

Hyper-concise report. These sections, nothing else:

1. Migration Summary
2. Scope and Files Changed
3. Existing Work and Remaining Work
4. Required Compatibility Fixes
5. Prompt/Agent Behavior Tuning
6. Validation Results
7. Proof Evidence
8. Risks and Follow-up Recommendations
9. Rollback Notes

Format per `examples/example-output.md`.

## Anti-Patterns

- Blind global model-ID replacement
- Guessing model IDs, parameters, pricing, limits, or deprecation dates
- Editing generated files manually instead of regenerating
- Treating registry/definer files like runtime callers
- Overwriting another agent's partial implementation without checking intent
- Mixing required fixes with optional tuning without labeling
- Skipping validation and claiming complete
- Treating a synthetic test as proof without a real smoke check, eval, trace,
  or before/after comparison

## References

- Migration strategy: `references/migration-playbook.md`
- Provider checklists: `references/provider-checklists.md`
- Model-specific guides: `references/models/` (per-version changelogs, quirks,
  migration steps)
- Prompt design research: `references/prompt-template-research.md`
- Migration patterns: `references/migration-patterns.md`
- Validation proof gates: `references/validation-proof.md`
- Starter prompt: `templates/migration-starter-prompt.md`
- Example prompts: `examples/example-prompts.md`
- Example report: `examples/example-output.md`

## Validation Checklist

- [ ] Scope explicitly confirmed
- [ ] Existing/parallel agent work checked and summarized
- [ ] Discovery scan covered API, prompts, agents, tools, tests, docs
- [ ] Files classified before edits
- [ ] Required compatibility fixes applied
- [ ] Optional tuning clearly marked as optional
- [ ] Tests and smoke checks executed
- [ ] Proof evidence captured or gap stated
- [ ] Report returned in concise format
