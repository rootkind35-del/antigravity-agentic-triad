# Antigravity Agentic Triad Role Contracts & Dynamic Model Routing

Grounded in **MetaGPT (Hong et al., ICLR 2024)** role specialization, **Reflexion (Shinn et al., 2023)** memory isolation, and **Google Antigravity Dynamic Model Switching**:

## 1. Routine Worker (Initial Attempt)
- **Model Parameter**: `flash` (Gemini 3.6 Flash) via `invoke_subagent`.
- **Purpose**: Fast execution ($1\text{--}3\text{s}$) of routine, well-specified, mechanical changes.

## 2. Complex Worker (Initial Attempt)
- **Model Parameter**: `pro` (Gemini Pro) via `invoke_subagent`.
- **Purpose**: Deep reasoning ($5\text{--}15\text{s}$) for complex, multi-file, or security-sensitive features.

## 3. Escalated Worker (Retry Attempt 2+)
- **Model Parameter**: `pro` (Gemini Pro) via `invoke_subagent`.
- **Trigger**: Automatically invoked when a `flash` worker receives a `fix-first` verdict from the Reviewer. Escalates reasoning capabilities to resolve subtle logic flaws.

## 4. Independent Reviewer (All Attempts)
- **Model Parameter**: `pro` (Gemini Pro) in a **fresh subagent conversation ID**.
- **Purpose**: Strict, unbiased verification. Checks:
  1. File ownership bounds (`git diff` vs `Files/Ownership`).
  2. Verification command adequacy (flags trivial or ineffective assertions).
  3. Returns `ship`, `fix-first`, or `rethink`.
