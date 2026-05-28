# Caveman Output Style

When running a migration with the `ModelPort` skill, the default output mode is "caveman style". This ensures that the agent consumes the bare minimum number of tokens when reporting progress, saving cost and time.

## Rules of Caveman Style

1. **No Conversational Filler**: Never start with "Here is your report" or end with "Let me know if you need anything else."
2. **Dense Bullet Points**: Omit verbs where possible. Use `->` to indicate state transitions (e.g. `GPT-4 -> Claude-3`).
3. **No Padding**: State only what changed, why it changed, and what was validated.
4. **Code Diffs Only**: Only output the exact lines that were modified. Do not reprint entire files.

## Example Comparison

**Non-Caveman:**
> "I have successfully migrated the `client.py` file to use the new destination model. As part of this, I replaced the deprecated `max_tokens_to_sample` parameter with `max_tokens`. Let me know if you want to proceed to the next file!"

**Caveman:**
>
> - `client.py`: Model ID -> target model
> - `client.py`: `max_tokens_to_sample` -> `max_tokens`
