# Antigravity Agentic Triad Role Contracts

## 1. Routine Worker
- **Model**: Gemini Flash (`Model: flash`) via `invoke_subagent`.
- **Purpose**: Fast execution of routine, well-specified, mechanical changes.

## 2. Complex Worker
- **Model**: Gemini Pro (`Model: pro`) via `invoke_subagent`.
- **Purpose**: Deep reasoning for complex, multi-file, or security-sensitive features.

## 3. Independent Reviewer
- **Model**: Gemini Pro (`Model: pro`) in a **fresh subagent conversation context**.
- **Purpose**: Strict verification of work. Checks:
  1. File ownership bounds (`git diff` vs `Files/Ownership`).
  2. Verification command adequacy (flags trivial or ineffective tests).
  3. Returns `ship`, `fix-first`, or `rethink`.
