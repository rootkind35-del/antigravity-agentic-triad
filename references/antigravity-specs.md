# Antigravity Technical Integration Specs

Google Antigravity provides native multi-agent capabilities via the `invoke_subagent` and `define_subagent` tools.

## Subagent Mechanics in Antigravity

- **Session Isolation**: Spawning a subagent creates a separate conversation ID with its own system prompt and tools.
- **Fresh Review Context**: Spawning Independent Reviewer with `invoke_subagent` ensures the reviewer does not carry over the worker's intermediate thoughts or conversations, eliminating self-validation bias.
- **Model Selection**:
  - `Model: flash` -> Gemini 3.6 Flash (Fast routine worker)
  - `Model: pro` -> Gemini Pro (Deep reasoning worker / Reviewer)
