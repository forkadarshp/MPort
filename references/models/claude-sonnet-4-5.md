# Claude Sonnet 4.5

Released: September 29, 2025
Model ID: `claude-sonnet-4-5`
Pricing: $3 / $15 per million input / output tokens

## Key features

- **Best-in-class coding** (at launch): Substantial gains in reasoning,
  mathematics, and software engineering benchmarks.
- **Computer use**: Industry-leading autonomous interface navigation — click,
  type, manage tabs, execute multi-step UI workflows.
- **Extended thinking**: Supports hybrid modes — near-instant responses for
  simple tasks, deep reasoning mode for complex problems. Model alternates
  between thinking and tool use.
- **Parallel tool use**: Execute multiple tool calls simultaneously.
- **Claude Code 2.0**: Checkpoints (rollback state), native VS Code extension,
  enhanced terminal interfaces.
- **Agent SDK**: Anthropic's internal agent-building primitives exposed for
  external developers.
- **New API capabilities**:
  - Code execution tool — model runs code directly
  - MCP (Model Context Protocol) connectors — simplified external tool
    integration
  - Files API — improved file upload and handling
  - Prompt caching — cache prompts for up to 1 hour

## Migration notes

### From Sonnet 4 (May 2025)

Drop-in replacement. Same API surface.

| Area | Notes |
| :--- | :---- |
| Model ID | Update to `claude-sonnet-4-5` |
| Extended thinking | New capability — opt in via `thinking` config for complex tasks |
| Tool use | Parallel tool calls now available — existing serial tool use still works |
| Prompt caching | New — add `cache_control` to reduce costs on repeated prompts |
| MCP connectors | New — optional, no migration required |

### From Sonnet 3.7 or earlier

| Area | Change required |
| :--- | :-------------- |
| Model ID | Update to `claude-sonnet-4-5` |
| API version | Update to latest API version — some request/response fields changed |
| Tool schemas | Verify tool definitions — Sonnet 4.5 has stricter schema validation |
| System prompts | Review — model follows instructions more literally than 3.7 |
| Output parsing | Re-test parsers — output formatting and stop behavior may differ |
| Beta headers | Remove legacy beta headers (`anthropic-beta`) if no longer needed |

## Quirks and best practices

### Agentic workflows

- **Verification loops**: Always provide the agent a way to verify its own
  work — tests, linters, output comparisons. Don't trust self-reported
  completion.
- **Bash-first tooling**: Shell access is often more reliable than complex
  custom tool APIs. Prefer `bash` for file system operations and command
  execution.
- **Sub-agent delegation**: For complex projects, decompose into sub-agents
  with focused scopes. Prevents context overload and improves reliability.
- **Plan before code**: Force the agent to output a step-by-step plan before
  executing changes. Catch faulty reasoning before destructive edits.

### Context management

- **Aggressive context hygiene**: Performance degrades as context fills. Pipe
  only necessary file contents. Use prompt caching where available.
- **Context reset pattern**: For very long tasks, plan in one session, save
  the plan as a markdown file, start a fresh session for execution using only
  that plan.
- **CLAUDE.md rules**: Maintain a concise rules file (< 200 lines) in your
  repo. Define coding styles, commit formats, constraints. The model relies
  on these for behavioral alignment.

### Prompt engineering

- **Explicit instructions**: Sonnet 4.5 follows instructions more literally
  than 3.7. Be explicit about format, verbosity, and scope.
- **XML structure**: Use structured XML tags (`<document>`, `<instruction>`)
  to help the model separate input parts clearly.
- **Define the finish line**: Always specify verifiable acceptance criteria.
  Without them, the model may hallucinate completion.

### Security

- **Least privilege**: Provide only the tools and file system access the agent
  needs.
- **Human review for auth**: Any action involving authentication or access
  control should require manual human review.
- **No secrets in prompts**: Treat all prompts as logs. Never include API keys
  or credentials in instructions.

## Model ID reference

| Version | Model ID | Status |
| :------ | :------- | :----- |
| Sonnet 4.6 | `claude-sonnet-4-6` | Current (GA) |
| Sonnet 4.5 | `claude-sonnet-4-5` | Active |
| Sonnet 4 | `claude-sonnet-4-20250514` | Active |
| Sonnet 3.7 | `claude-3-7-sonnet-20250219` | Deprecated soon |
