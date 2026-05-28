# Claude Opus 4.6

Released: February 5, 2026
Model ID: `claude-opus-4-6`
Pricing: $5 / $25 per million input / output tokens

## Key features

- **1M token context window**: Process entire codebases, long documents, or
  multi-file analysis in a single session. 76–78.3% retrieval accuracy on
  MRCR v2 benchmarks.
- **Adaptive thinking**: Replaced manual extended thinking with dynamic
  reasoning depth calibration. Four effort levels:
  - **Low** — speed-optimized, simple tasks
  - **Medium** — balanced for moderate complexity
  - **High** (default) — deep reasoning for production workloads
  - **Max** — spare-no-expense for hardest problems (complex debugging, novel
    research)
- **Agent teams** (research preview): Claude Code orchestrates multiple
  parallel agents. A lead agent decomposes tasks, assigns to specialist
  teammate agents, synthesizes results.
- **Context compaction**: Automated API summarizes older conversation parts
  when nearing context limits. Prevents degradation in extended sessions.
- **128k output tokens**: Generate entire documents or large code
  implementations in a single pass.
- **Computer use improvements**: Higher accuracy navigating software
  interfaces — clicking, typing, managing browser tabs.

## Migration notes

### From Opus 4.5 or earlier

| Area | Change required |
| :--- | :-------------- |
| Extended thinking | Replace `budget_tokens` config with adaptive thinking (`{type: "adaptive"}`). Set `effort` parameter. |
| Context window | 1M tokens available — review whether you need context management strategies or can simplify. |
| Output length | 128k output tokens now supported — remove chunking workarounds if applicable. |
| Agent workflows | Agent teams available — consider decomposing complex migrations into parallel subtasks. |
| Computer use | If using computer use, retest — behavior and accuracy changed significantly. |

### From Opus 4 / 4.1

All of the above, plus:

- Re-check prompt templates — Opus 4.6 follows instructions more literally.
- Verify tool schemas — stricter validation on tool definitions.
- Update model ID from `claude-opus-4-*` to `claude-opus-4-6`.

## Quirks and best practices

- **Effort level tuning**: Start with `high` (default). Drop to `medium` for
  high-throughput, low-complexity workloads. Use `max` sparingly — it consumes
  significantly more tokens.
- **Context compaction awareness**: For long-running agentic sessions, the
  model auto-compacts older context. If your workflow depends on exact recall
  of early messages, structure important information as system-level
  instructions rather than early user turns.
- **Agent team decomposition**: When using agent teams, keep subtask
  descriptions self-contained. Each teammate agent has its own context — don't
  assume shared state between teammates.
- **Literal instruction following**: More literal than Opus 4.5. Prompts that
  relied on the model "reading between the lines" may need explicit
  reformulation.
- **Long-context retrieval**: Despite 1M context, retrieval accuracy can vary
  by position. Place critical information at the start (system prompt) or end
  (recent messages) of the context — middle positions have lower recall.
- **Output planning**: With 128k output capacity, the model can over-generate.
  Set explicit length or format constraints in your prompts when concise output
  is needed.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Opus 4.8 | `claude-opus-4-8` | Current (GA) |
| Opus 4.7 | `claude-opus-4-7` | Active |
| Opus 4.6 | `claude-opus-4-6` | Active |
| Opus 4.5 | `claude-opus-4-5` | Active |
