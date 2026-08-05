---
name: antigravity-agentic-triad
description: "Implements the Antigravity Agentic Triad orchestration workflow. Separates concerns into Architect (Primary Agent), Routine Worker (Flash Subagent), Complex Worker (Pro Subagent), and Independent Reviewer (Fresh Pro Subagent) to eliminate self-validation loops."
---

# Antigravity Agentic Triad Workflow

**Antigravity Agentic Triad** is an Agentic Skill designed specifically for **Google Antigravity**. As the primary agent, you act as the **Architect**. You do not write implementation code directly. Instead, you delegate work to specialized subagents and mandate a strict, fresh review process before accepting any deliverable.

## Roles & Subagent Model Mapping

| Role | Responsibility | Antigravity Model / Tool |
|---|---|---|
| **Architect** | Primary session. Handles requirements, architecture, breakdown, 5-part task packets, and final acceptance. | Main Agent Session |
| **Routine Worker** | Handles repetitive, well-defined, mechanical tasks. | `invoke_subagent` (Model: `flash`) |
| **Complex Worker** | Handles logic-heavy, complex tasks, security-sensitive work, or wide refactors. | `invoke_subagent` (Model: `pro`) |
| **Independent Reviewer** | Fresh subagent. Reviews diffs against declared file ownership and runs verification tests. | `invoke_subagent` (Model: `pro` in fresh subagent) |

---

## Workflow Rules

When a user asks you to implement a feature using the Agentic Triad workflow, follow these 4 phases strictly:

### 1. Specification Phase
Before delegating any work, define a complete 5-part task packet (see `assets/task-packet-template.md` and `examples/task-packet-sample.md` for guidance):
1. **Goal**: What exactly needs to be achieved.
2. **Files/Ownership**: Explicit list of files the worker is permitted to edit.
3. **Interfaces**: How the new code interacts with existing code.
4. **Constraints**: Non-functional requirements, performance rules, or style guidelines.
5. **Verification**: Exact terminal commands (unit tests, linters, build checks) that prove correctness.

### 2. Delegation Phase
Use the `invoke_subagent` tool to dispatch work:
- Routine or well-scoped tasks: set `Model: flash` (Routine Worker).
- Complex, architectural, or multi-file tasks: set `Model: pro` (Complex Worker).
Pass the complete 5-part task packet as the prompt.
Wait for the subagent to report implementation completion.

### 3. Review Phase (Mandatory)
Once the worker subagent claims completion, you **MUST** spawn a fresh reviewer subagent with `invoke_subagent` (`Model: pro`, Role: `Independent Reviewer`).

Provide the reviewer with:
- The original goal and declared `Files/Ownership` list.
- Instructions to explicitly compare `git diff` / modified files against `Files/Ownership`. Any file modified outside declared scope is treated as a `fix-first` issue.
- Instructions to first judge whether verification commands actually test the stated goal (flagging trivial assertions, stubbed tests, or missing edge cases). If inadequate, return `fix-first` with `"verification insufficient"`.
- Instructions to run the verification commands (if deemed adequate).
- Requirement to return exactly one verdict: `ship`, `fix-first`, or `rethink`.

### 4. Acceptance Phase
- **ship**: Report completion with verification evidence to the user.
- **fix-first**: Read feedback, update task packet, and delegate fixes back to worker.
  - **HARD CAP**: Maximum **3 consecutive `fix-first` verdicts** allowed. After 3 cycles on the same task, stop delegating fixes and escalate to `rethink` (return to Specification Phase).
- **rethink**: Return to Specification Phase and adjust architecture/packet.
  - **HARD CAP**: Maximum **2 consecutive `rethink` verdicts** allowed. After 2 cycles, stop immediately and surface the situation directly to the user.

---

## Subdocumentation & Resources

For detailed specifications and templates, refer to:
- **Architect Guide**: `references/architect-guide.md`
- **Role Contracts**: `references/role-contracts.md`
- **Antigravity Specs**: `references/antigravity-specs.md`
- **Task Packet Template**: `assets/task-packet-template.md`
- **Review Report Template**: `assets/review-report-template.md`
- **Samples**: `examples/task-packet-sample.md` & `examples/review-outcomes-sample.md`
