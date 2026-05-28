# Prompt Template Research

Use this reference when designing prompts for model, prompt, agent, or codebase
migrations. It explains the default starter prompt in
`templates/migration-starter-prompt.md`.

## Recommended Starter Structure

Use a migration brief with these sections:

1. **Outcome**: source model, target model, and the behavior/cost/quality goal.
2. **Scope**: exact files or directories; no ambiguous "whole project" wording.
3. **Current system context**: runtime callers, prompts, tools, parsers, tests,
   and existing migration work.
4. **Constraints**: output shape, tool behavior, safety, latency, cost, rollout,
   and rollback.
5. **Instructions**: classify first, preserve baseline, separate required fixes
   from tuning, and verify official provider facts.
6. **Proof gates**: tests, smoke checks, evals, tool traces, and rollout metrics.
7. **Report format**: required compatibility fixes, optional tuning, evidence,
   risks, and rollback.

This shape is better for migrations than a generic persona prompt because it
forces the agent to reason over system boundaries, evidence, and rollout risk.

## Techniques to Integrate

### Put instructions first and separate context

OpenAI guidance recommends putting instructions at the beginning and using clear
separators for context. In a migration prompt, this means keeping the goal,
scope, and required behavior separate from pasted prompts, logs, file lists, or
eval examples.

### Preserve a baseline before prompt tuning

OpenAI's prompt migration guidance for newer models recommends changing one
thing at a time: switch model/config first, align reasoning effort or equivalent
runtime controls, run evals, then tune the prompt only if regressions appear.
This avoids hiding whether a behavior change came from the model or from a
prompt rewrite.

### Prefer context engineering over clever wording

Karpathy's context-engineering framing is useful for this skill: the important
work is deciding what the model sees for the next step, not inventing a magical
sentence. For migrations, that means providing the right current artifacts:
model callers, prompt templates, output contracts, eval examples, provider docs,
and evidence from prior attempts. Avoid stuffing irrelevant docs into context.

### Use iterative proof loops

Research on AI-assisted coding workflows finds that developers alternate between
prompting, evaluating generated code, testing the result, and refining the
request. The safe version for this migration skill is the diagnose-patch-retry
loop in `references/validation-proof.md`.

### Make acceptance criteria operational

The prompt must state how success will be checked: schema validation, tool-call
trace, smoke request, unit/integration tests, before/after samples, or canary
metrics. "Improve performance" is not enough unless performance means a named
metric such as latency, token usage, pass rate, tool precision, or output
contract compliance.

### Keep optional tuning opt-in and reviewable

Newer models may follow instructions more literally or differ in verbosity,
tool-use frequency, or reasoning depth. Prompt edits should be explicit,
reviewable, and labeled as tuning unless they fix a hard compatibility failure.

## Anti-Patterns

- One huge prompt with mixed instructions, context, logs, docs, and examples.
- Rewriting prompts and changing model/runtime parameters in the same baseline
  step.
- Asking for "better performance" without metrics or representative examples.
- Copying old prompt hacks forward without checking whether the new model still
  needs them.
- Treating a generated test as the only evidence that migration succeeded.
- Leaving scope, rollback, or target model unspecified.

## Source URLs

- OpenAI prompt engineering best practices:
  <https://help.openai.com/en/articles/6654000-prompt-engineering-best-practices-for-chatgpt>
- OpenAI API prompting guide:
  <https://developers.openai.com/api/docs/guides/prompting>
- OpenAI Cookbook prompt migration guide:
  <https://developers.openai.com/cookbook/examples/prompt_migration_guide>
- OpenAI Cookbook GPT-5.2 prompting and migration guide:
  <https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide>
- Context engineering summary citing Andrej Karpathy:
  <https://madplay.github.io/en/post/context-engineering>
- Vibe coding empirical study:
  <https://arxiv.org/abs/2506.23253>
