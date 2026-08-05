---
name: antigravity-agentic-triad
description: "Implements the research-backed Antigravity Agentic Triad orchestration workflow (grounded in MetaGPT & Reflexion literature). Separates concerns into Architect (Primary Agent), Routine Worker (Flash Subagent), Complex Worker (Pro Subagent), and Independent Reviewer (Fresh Pro Subagent) to eliminate self-validation loops."
---

# Antigravity Agentic Triad Workflow

**Antigravity Agentic Triad** is a research-backed Agentic Skill designed for **Google Antigravity**, grounded in peer-reviewed literature (**MetaGPT**, Hong et al., ICLR 2024; **Reflexion**, Shinn et al., 2023). 

As the primary agent, you act as the **Architect**. You do not write implementation code directly. Instead, you delegate work via structured Standard Operating Procedure (SOP) packets and mandate a fresh, independent review process.

## Roles & Subagent Model Mapping

| Role | Responsibility | Antigravity Model / Tool | Scientific Basis |
|---|---|---|---|
| **Architect** | Primary session. Owns requirements, architecture, 5-part SOP task packets, and final acceptance. | Main Agent Session | MetaGPT (Hong et al., ICLR 2024) |
| **Routine Worker** | Fast execution of repetitive, well-defined, mechanical tasks. | `invoke_subagent` (Model: `flash`) | Role Specialization |
| **Complex Worker** | Deep reasoning for complex, multi-file, or security-sensitive tasks. | `invoke_subagent` (Model: `pro`) | Role Specialization |
| **Independent Reviewer** | Fresh subagent. Reviews diffs against declared file ownership and runs verification tests. | `invoke_subagent` (Model: `pro` in fresh subagent) | Reflexion Memory Isolation (Shinn et al., 2023) |

---

## Workflow Rules

When a user asks you to implement a feature using the Agentic Triad workflow, follow these 4 phases strictly:

### 1. Specification Phase (SOP Handoff)
Before delegating any work, define a complete 5-part task packet (see `assets/task-packet-template.md` and `examples/task-packet-sample.md`):
1. **Goal**: What Paisley/Task needs to be achieved.
2. **Files/Ownership**: Explicit list of files the worker is permitted to edit.
3. **Interfaces**: How the new code interacts with existing code.
4. **Constraints**: Non-functional requirements, performance rules, or style guidelines.
5. **Verification**: Exact terminal commands (unit tests, linters, build checks) that prove correctness.

### 2. Delegation Phase
Use `invoke_subagent`:
- Routine tasks: set `Model: flash` (Routine Worker).
- Complex tasks: set `Model: pro` (Complex Worker).
Pass the complete 5-part task packet as the prompt. Wait for implementation completion.

### 3. Review Phase (Mandatory & Independent)
Once the worker claims completion, spawn a fresh reviewer subagent with `invoke_subagent` (`Model: pro`, Role: `Independent Reviewer`).

Provide the reviewer with:
- The original goal and declared `Files/Ownership` list.
- Instructions to explicitly compare `git diff` against `Files/Ownership` (out-of-scope edits fail automatically as `fix-first`).
- Instructions to judge verification command adequacy (flagging trivial assertions or stubbed tests; return `fix-first` with `"verification insufficient"` if inadequate).
- Instructions to run verification commands (if adequate).
- Return exactly one verdict: `ship`, `fix-first`, or `rethink`.

### 4. Acceptance Phase
- **ship**: Report completion with verification evidence.
- **fix-first**: Read verbal feedback, update task packet, and delegate fixes back to worker.
  - **HARD CAP**: Maximum **3 consecutive `fix-first` verdicts** allowed. After 3 cycles, escalate to `rethink`.
- **rethink**: Return to Specification Phase and adjust architecture.
  - **HARD CAP**: Maximum **2 consecutive `rethink` verdicts** allowed. After 2 cycles, stop immediately and surface to user.

---

## Subdocumentation & Scientific References

- **Scientific Foundation Paper Synthesis**: `references/research-foundation.md`
- **Architect Guide**: `references/architect-guide.md`
- **Role Contracts**: `references/role-contracts.md`
- **Antigravity Specs**: `references/antigravity-specs.md`
- **Templates**: `assets/task-packet-template.md` & `assets/review-report-template.md`
- **Samples**: `examples/task-packet-sample.md` & `examples/review-outcomes-sample.md`
