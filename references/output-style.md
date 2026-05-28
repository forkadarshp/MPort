# Output Style

The default output mode for this skill is hyper-concise. This file is a quick
reference. The authoritative rules are in `SKILL.md`.

## Rules

1. No conversational filler. No pleasantries. No intro/outro.
2. Dense bullet points. Omit verbs where possible.
3. `->` for state transitions (e.g. `GPT-4 -> Claude-3`).
4. Code diffs only — never reprint entire files.
5. State only: what changed, why, what was validated.

## Example

**Verbose:**
> "I have successfully migrated the `client.py` file to use the new destination model. As part of this, I replaced the deprecated `max_tokens_to_sample` parameter with `max_tokens`. Let me know if you want to proceed to the next file!"

**Concise (default):**
>
> - `client.py`: Model ID -> target model
> - `client.py`: `max_tokens_to_sample` -> `max_tokens`
