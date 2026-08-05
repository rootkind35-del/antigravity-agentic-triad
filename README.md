# Antigravity Agentic Triad

An evidence-backed agentic orchestration workflow for **Google Antigravity**, featuring **Dynamic Model Switching & Escalation** at runtime. Grounded in peer-reviewed AI Agent literature (**MetaGPT**, Hong et al., ICLR 2024; **Reflexion**, Shinn et al., 2023).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Antigravity](https://img.shields.io/badge/Platform-Google%20Antigravity-blue.svg)](https://antigravity.google)
[![Dynamic Model Switching](https://img.shields.io/badge/Runtime-Dynamic%20Model%20Escalation-blueviolet.svg)](references/dynamic-model-switching.md)
[![Research Grounded](https://img.shields.io/badge/Research-ICLR%202024%20%7C%20Reflexion-green.svg)](references/research-foundation.md)

When an AI coding assistant writes code and tests its own work within the same conversation context, it almost always self-approves. It misses subtle edge cases because its assumptions bleed into its verification. 

**Antigravity Agentic Triad** solves this by strictly separating responsibilities into three distinct roles: **Architect**, **Worker (with Dynamic Model Escalation)**, and **Fresh Independent Reviewer**.

---

## ⚡ Dynamic Model Switching Mechanics

Antigravity allows dynamic runtime selection of LLM model tiers via `invoke_subagent`:

```mermaid
flowchart TD
    Architect[1. Architect Session\nMain Agent - Directs Flow] -->|Task Decomposition| Router{Dynamic Model Switcher}
    
    Router -->|Routine Edits: Model: flash| RoutineWorker[2a. Routine Worker\nGemini 3.6 Flash]
    Router -->|Complex Logic: Model: pro| ComplexWorker[2b. Complex Worker\nGemini Pro]
    Router -->|Retry Escalation: Model: pro| EscalatedWorker[2c. Escalated Worker\nGemini Pro - Auto Escalated]
    
    RoutineWorker -->|Implementation| Reviewer[3. Independent Reviewer\nModel: pro - Clean Context]
    ComplexWorker -->|Implementation| Reviewer
    EscalatedWorker -->|Implementation| Reviewer
    
    Reviewer -->|Audit Gate| Verdict{Verdict: ship / fix-first / rethink}
    
    Verdict -->|fix-first (Attempt 1 Flash)| EscalatedWorker
    Verdict -->|ship| Complete[4. Complete]
```

---

## 🔬 Scientific Foundation

This workflow is mathematically and empirically grounded in recent AI multi-agent research:

1. **MetaGPT (Hong et al., ICLR 2024)**: Demonstrates that replacing raw chat with **Standardized Operating Procedures (SOPs)** and **structured document handovers** eliminates cascading hallucinations and boosts code pass rates to over 87%.
2. **Reflexion (Shinn et al., 2023)**: Proves that **verbal self-reflection** combined with **Actor-Evaluator memory isolation** enables language agents to learn rapidly from trial and error without model finetuning (reaching 91% on HumanEval).

For detailed scientific proofs and citations, read [`references/research-foundation.md`](references/research-foundation.md) and [`references/dynamic-model-switching.md`](references/dynamic-model-switching.md).

---

## ⚡ Role Breakdown

| Role | Responsibility | Antigravity Engine Mapping | Dynamic Escalation Trigger |
|---|---|---|---|
| **Architect** | Primary chat session. Owns requirements, architecture, 5-part task packets, and final acceptance. | Primary Session Agent | N/A |
| **Routine Worker** | Handles repetitive, well-defined, mechanical tasks. | `invoke_subagent` (`Model: flash`) | Attempt 1 |
| **Complex Worker** | Handles logic-heavy, complex tasks, security-sensitive work, or broad refactors. | `invoke_subagent` (`Model: pro`) | Attempt 1 |
| **Escalated Worker** | Re-executes failed tasks with enhanced reasoning capability. | `invoke_subagent` (`Model: pro`) | Attempt 2 (if `flash` receives `fix-first`) |
| **Independent Reviewer** | Spawns in a **fresh subagent session** without previous conversation memory. Audits file scope bounds and test adequacy. | `invoke_subagent` (`Model: pro` in fresh subagent) | All Attempts |

---

## 🛡 Hard Safety Constraints

- **Scope Boundary Enforcement**: The Independent Reviewer compares the actual `git diff` against declared `Files/Ownership`. Modifying files outside the declared list triggers an immediate `fix-first` verdict.
- **Verification Adequacy Audit**: The Reviewer checks whether tests actually evaluate edge cases before trusting test output. Trivial or passing-stub tests return `fix-first` with `"verification insufficient"`.
- **Loop Caps**:
  - Max **3 consecutive `fix-first` retries** per task before escalating to `rethink`.
  - Max **2 consecutive `rethink` cycles** before hard-stopping to ask the user.

---

## 📦 Directory Structure

```text
antigravity-agentic-triad/
├── SKILL.md                     # Main Antigravity Skill definition & workflow rules
├── README.md                    # Repository documentation
├── LICENSE                      # MIT License
├── scripts/                     # Tooling & validation scripts
│   ├── model_switch_matrix.py   # Cost & speed matrix benchmark tool
│   ├── validate_skill.py        # Schema, link & guardrail validator
│   └── run_verification.py      # Workflow simulation & gate tester
├── references/                  # Reference guides
│   ├── dynamic-model-switching.md# Dynamic model switching mechanics & triggers
│   ├── research-foundation.md   # Peer-reviewed literature & paper citations
│   ├── architect-guide.md       # Architect guidelines & SOP packet drafting
│   ├── role-contracts.md        # Worker & Reviewer contracts
│   └── antigravity-specs.md     # Antigravity subagent routing mechanics
├── examples/                    # Real-world samples
│   ├── task-packet-sample.md    # 5-part task packet example
│   └── review-outcomes-sample.md# Ship / Fix-First / Rethink verdict examples
└── assets/                      # Reusable templates
    ├── task-packet-template.md  # 5-part task packet template
    └── review-report-template.md# Independent Reviewer audit report template
```

---

## 📥 Installation

Copy the `antigravity-agentic-triad` folder into your global Google Antigravity skills directory:

```bash
# Copy skill package to Antigravity global config
cp -r antigravity-agentic-triad ~/.gemini/config/skills/antigravity_agentic_triad
```

---

## 🚀 How to Use

In your Antigravity chat, trigger the workflow by requesting:

> *"Use the Antigravity Agentic Triad workflow to build feature X."*

---

## 🧪 Validation & Benchmarking

Run the included validator, cost matrix estimator, and simulator scripts:

```bash
python scripts/model_switch_matrix.py
python scripts/validate_skill.py .
python scripts/run_verification.py
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
