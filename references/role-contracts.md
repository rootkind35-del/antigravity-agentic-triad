# Antigravity Agentic Triad Role Contracts

Grounded in **MetaGPT (Hong et al., ICLR 2024)** role specialization and **Reflexion (Shinn et al., 2023)** Actor-Evaluator-Reflection memory architectures:

## 1. Routine Worker
- **Model**: Gemini Flash (`Model: flash`) via `invoke_subagent`.
- **Purpose**: Fast execution of routine, well-specified, mechanical changes.

## 2. Complex Worker
- **Model**: Gemini Pro (`Model: pro`) via `invoke_subagent`.
- **Purpose**: Deep reasoning for complex, multi-file, or security-sensitive features.

## 3. Independent Reviewer
- **Model**: Gemini Pro (`Model: pro`) in a **fresh subagent conversation context**.
- **Purpose**: Independent evaluation without credit assignment or self-approval bias. Checks:
  1. File ownership bounds (`git diff` vs `Files/Ownership`).
  2. Verification command adequacy (flags trivial or ineffective assertions).
  3. Returns `ship`, `fix-first`, or `rethink`.
