---
name: modelport-skill
description: Use when the user asks to migrate, upgrade, or port prompts, agents, tools, or codebases from one LLM model or provider version to another. Also use when auditing or continuing migration work started by another agent. Covers API calls, prompt assets, agent configs, tool definitions, tests, docs, runtime settings, rollout plans, and handoff coordination.
---

# ModelPort Skill

Production-grade LLM migrations: Swap models safely across agents, prompts, and code.

## Purpose

Deliver end-to-end migration outcomes, not just string replacement. Preserve
behavior where needed, improve behavior where possible, and validate that the
new model integration is correct, stable, and measurable.

## Production Standards

Before implementing:

1. Scan relevant files and architecture first.
2. State assumptions explicitly.
3. Check existing work, open changes, issue/PR notes, and handoff artifacts when
   available.
4. Ask for clarification when scope is ambiguous.

When implementing:

1. Make minimal, targeted edits.
2. Follow repository conventions and coding style.
3. Preserve backward-compatible paths unless the user asks to remove them.

Quality:

1. Distinguish required fixes from optional tuning.
2. Validate runtime behavior with tests and smoke checks.
3. Provide a clear migration report with risks, remaining work, and follow-ups.

## Inputs Required

Collect these before editing:

- Source model/provider and destination model/provider
- Scope (exact files, directories, or whole repo)
- Migration mode:
  - In-place replacement
  - Side-by-side dual-model support
  - Phased rollout with feature flags
- Constraints (latency, cost, output format, safety/compliance)
- Success criteria (quality, speed, token/cost, compatibility)
- Evidence requirements (unit tests, evals, live smoke checks, rollout metrics)

If scope is not explicit, ask a single scope-selection question and wait.

## Workflow

### Phase 0: Scope and coordination lock

Define exactly what will be migrated:

- Entire repository
- Specific directories
- Specific file list

Also establish the current implementation state:

- Inspect version control status, branch/PR context, issue notes, migration plans,
  and local handoff files when available.
- Separate changes already implemented from changes still needed.
- Identify work that appears unrelated, incomplete, or owned by another agent
  before editing nearby files.

Do not edit code until scope is confirmed and the current work state is understood.

### Phase 1: Discovery scan

Map the migration surface:

- API call sites (SDK/client usage, model IDs, request params)
- Prompt assets (system prompts, templates, chains)
- Agent configs (tool policy, autonomy/delegation behavior)
- Tool definitions (schemas, descriptions, guardrails)
- Registries/config/tests/docs referencing model names

Read:

- `references/migration-playbook.md`
- `references/provider-checklists.md`
- `references/prompt-template-research.md` when creating or improving a
  migration prompt, prompt rewrite process, or reusable migration request.
- `references/migration-patterns.md` when choosing rollout strategy,
  compatibility adapters, feature flags, or side-by-side support.
- `references/validation-proof.md` when planning proof gates, evals,
  smoke tests, or diagnose-patch-retry loops.

### Phase 2: File classification

Classify each hit before editing:

- **Runtime caller**: code that sends model requests
- **Definer/registry**: model catalogs, routing, capability maps
- **Prompt and behavior layer**: prompt templates and safety policy
- **Agent/tool layer**: tool specs, usage policy, orchestration hints
- **Reference/test/docs**: assertions, docs, examples, fixtures

For each category, choose the right action:

- Replace
- Add alongside
- Keep and annotate
- Regenerate (if generated files)

### Phase 3: Migration design

Create a compact migration spec:

- What appears already implemented and by whom if known
- What remains to be implemented
- Which migration pattern applies, such as direct swap, branch-by-abstraction,
  strangler-style routing, expand-contract, shadow mode, or canary rollout
- What is required to prevent breakage
- What is optional tuning for better performance
- Validation plan (tests + runtime checks + regression checks + proof evidence)
- Rollback strategy

If provider-specific unknowns exist, flag them and ask before risky edits.

### Phase 4: Implementation

Apply changes in this order:

1. Runtime/API compatibility edits
2. Prompt and behavior tuning
3. Agent and tool behavior updates
4. Config, registry, tests, docs synchronization

Use precise edits. Avoid repo-wide blind search-and-replace.

### Phase 5: Validation

Run:

- Unit/integration tests relevant to modified files
- Lint/type-check where applicable
- At least one real request smoke test on the destination model
- Output-contract or prompt-eval checks when prompts/parsers changed

Verify:

- Request success (no parameter/model errors)
- Expected stop/finish behavior
- Tool invocation behavior still aligned
- Output shape/format requirements still satisfied
- Observability signals are defined for staged rollout when production risk exists

If validation fails, enter a diagnose-patch-retry loop. Identify the observed
root cause, patch the smallest responsible surface, then re-run the failed
check before claiming completion.

### Phase 6: Migration report

Return a concise report with:

- Scope migrated
- Existing work found
- Required changes made
- Remaining work, if any
- Optional improvements applied
- Validation results
- Proof evidence and commands or checks run
- Risks and recommended next steps

Use the format in `examples/example-output.md`.

## Required Output Format (Caveman Style)

To minimize token usage and latency during complex migrations, you MUST use the hyper-concise "caveman" style.

- No conversational filler, no pleasantries, no intro/outro.
- Use ultra-dense bullet points.
- Provide only actionable diffs and hard validation evidence.

Produce a report with these sections, strictly adhering to caveman mode:

1. Migration Summary
2. Scope and Files Changed
3. Existing Work and Remaining Work
4. Required Compatibility Fixes
5. Prompt/Agent Behavior Tuning
6. Validation Results
7. Proof Evidence
8. Risks and Follow-up Recommendations
9. Rollback Notes

## Anti-Patterns to Avoid

- Blind global model-ID replacement
- Guessing model IDs, parameters, pricing, limits, or deprecation dates
- Editing generated files manually instead of regenerating
- Treating registry/definer files like runtime callers
- Overwriting another agent's partial implementation without checking intent
- Mixing mandatory compatibility fixes with optional tuning without labeling
- Skipping validation and claiming migration complete
- Treating a synthetic test written during migration as proof without a real
  smoke check, eval, trace, or before/after comparison

## References and Examples

- Migration strategy and decision framework: `references/migration-playbook.md`
- Provider-specific checklists: `references/provider-checklists.md`
- Starter migration prompt and prompt-design research:
  `templates/migration-starter-prompt.md` and
  `references/prompt-template-research.md`
- Migration patterns and rollout strategy: `references/migration-patterns.md`
- Validation proof gates: `references/validation-proof.md`
- Example user prompts: `examples/example-prompts.md`
- Example migration report: `examples/example-output.md`

## Validation Checklist

- [ ] Scope was explicitly confirmed
- [ ] Existing or parallel agent work was checked and summarized
- [ ] Discovery scan covered API, prompts, agents, tools, tests, and docs
- [ ] Files were classified before edits
- [ ] Required compatibility fixes were applied
- [ ] Optional tuning was clearly marked as optional
- [ ] Tests and smoke checks were executed
- [ ] Proof evidence was captured or skipped with a stated reason
- [ ] Migration report was returned in required format
