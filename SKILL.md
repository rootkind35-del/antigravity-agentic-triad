---
name: antigravity-agentic-triad
description: "Implements the research-backed Antigravity Agentic Triad orchestration workflow with Dynamic Model Switching (grounded in 20 arXiv papers including MetaGPT, Reflexion, FrugalGPT, LATS, SWE-agent, ReAct, and ToT). Separates concerns into Architect (Primary Agent), Routine Worker (Flash Subagent), Complex Worker (Pro Subagent), Escalated Worker (Pro on retry), and Independent Reviewer (Fresh Pro Subagent) to eliminate self-validation loops."
---

# Antigravity Agentic Triad Workflow

**Antigravity Agentic Triad** is a research-backed Agentic Skill designed for **Google Antigravity**, featuring **Dynamic Model Switching & Escalation** at runtime. Grounded in 20 peer-reviewed AI agent research papers (**MetaGPT**, **Reflexion**, **FrugalGPT**, **LATS**, **SWE-agent**, **ReAct**, **Tree of Thoughts**, **SWE-bench**, **RouteLLM**, etc.).

As the primary agent, you act as the **Architect**. You do not write implementation code directly. Instead, you delegate work via structured Standard Operating Procedure (SOP) packets and mandate a fresh, independent review process.

## 🔬 Grounding in Research Papers & Reddit Pain Points Solved

| Reddit Developer Pain Point | AI Coding Flaw | Triad Solution | Scientific Grounding Paper |
|---|---|---|---|
| **1. Silent Hallucinations & Stubs** | Writing empty `// TODO` blocks | Independent Test Adequacy Audit | **CRITIC** (*ICLR 2024*) & **Reflexion** (*2023*) |
| **2. Out-of-Scope Code Pollution** | Modifying unrelated files | ACI Guardrails & `git diff` checking | **SWE-agent** (*NeurIPS 2024*) |
| **3. Cascading Chat Hallucinations** | Chat dialogue causing logic drift | SOP 5-part task packet artifacts | **MetaGPT** (*ICLR 2024*) & **ChatDev** (*ACL 2024*) |
| **4. Token & Cost Explosion** | Querying heavy models for simple edits | Dynamic Model Cascade (`flash` -> `pro`) | **FrugalGPT** (*Stanford 2023*) & **RouteLLM** (*LMSYS 2024*) |
| **5. Infinite Retry Loops** | Repeatedly trying broken fixes | Episodic memory ($\Omega \le 3$) & MCTS pruning | **LATS** (*ICML 2024*) & **Self-Refine** (*NeurIPS 2023*) |
| **6. Context Blindness** | Missing multi-file imports | Explicit public interface contracts | **RepoCoder** (*EMNLP 2023*) & **InterCode** (*NeurIPS 2023*) |

---

## Workflow Rules & Dynamic Escalation

When a user asks you to implement a feature using the Agentic Triad workflow, follow these 4 phases strictly:

### 1. Specification Phase (SOP Handoff)
Before delegating any work, define a complete 5-part task packet (see `assets/task-packet-template.md` and `examples/task-packet-sample.md`):
1. **Goal**: What needs to be achieved.
2. **Files/Ownership**: Explicit list of files the worker is permitted to edit.
3. **Interfaces**: How the new code interacts with existing code.
4. **Constraints**: Non-functional requirements, performance rules, or style guidelines.
5. **Verification**: Exact terminal commands (unit tests, linters, build checks) that prove correctness.

### 2. Delegation & Dynamic Model Routing Phase
Use `invoke_subagent`:
- **Routine tasks**: set `Model: flash` (Routine Worker).
- **Complex tasks**: set `Model: pro` (Complex Worker).
Pass the complete 5-part task packet as the prompt. Wait for implementation completion.

### 3. Review Phase (Mandatory & Independent)
Once the worker claims completion, spawn a fresh reviewer subagent with `invoke_subagent` (`Model: pro`, Role: `Independent Reviewer`).

Provide the reviewer with:
- The original goal and declared `Files/Ownership` list.
- Instructions to explicitly compare `git diff` against `Files/Ownership` (out-of-scope edits fail automatically as `fix-first`).
- Instructions to judge verification command adequacy (flagging trivial assertions or stubbed tests; return `fix-first` with `"verification insufficient"` if inadequate).
- Instructions to run verification commands (if adequate).
- Return exactly one verdict: `ship`, `fix-first`, or `rethink`.

### 4. Acceptance & Model Escalation Phase
- **ship**: Report completion with verification evidence.
- **fix-first**: Read verbal feedback, update task packet, and delegate fixes back to worker.
  - **DYNAMIC MODEL ESCALATION**: If the failed worker ran on `flash` on Attempt 1, **escalate Attempt 2 to `Model: pro`** (Escalated Worker) to resolve complex logic errors.
  - **HARD CAP**: Maximum **3 consecutive `fix-first` verdicts** allowed. After 3 cycles, escalate to `rethink`.
- **rethink**: Return to Specification Phase and adjust architecture.
  - **HARD CAP**: Maximum **2 consecutive `rethink` verdicts** allowed. After 2 cycles, stop immediately and surface to user.

---

## Subdocumentation & Technical References

- **Scientific Foundation Synthesis**: `references/research-foundation.md`
- **Dynamic Model Switching Mechanics**: `references/dynamic-model-switching.md`
- **Architect Guide**: `references/architect-guide.md`
- **Role Contracts**: `references/role-contracts.md`
- **Antigravity Specs**: `references/antigravity-specs.md`
- **Scripts**: `scripts/generate_diagram.py`, `scripts/model_switch_matrix.py`, `scripts/validate_skill.py`, `scripts/run_verification.py`
