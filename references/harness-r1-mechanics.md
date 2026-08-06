# Harness-R1: Evolutionary Agent Harness Optimization

This document outlines the integration of the concepts from the **Harness-R1** research paper (*arXiv:2608.02276, Shao et al.*) into the Antigravity Agentic Triad workflow.

## 1. The Core Problem: Static Harnesses

Most multi-agent systems rely on a static "Agent Harness" (the code and instructions that construct context, mediate tools, validate actions, and recover from failures). When a target agent repeatedly fails a task, the standard approach is to rely on verbal feedback (Reflexion) or update the LLM weights (Fine-Tuning).
However:
- Verbal feedback struggles with complex structural failures.
- Fine-tuning model weights is expensive and degrades general capabilities.

## 2. The Harness-R1 Solution

**Harness-R1** introduces a 4th role: the **Harness Engineer**.
Rather than editing the model, the Engineer edits the *Executable Runtime Harness*.

The workflow operates in a continuous loop:
1. **Failure Trajectories**: Collect batches of observations, tool calls, and outcomes from target-agent failures during rollout.
2. **Harness Engineer (Trainable)**: A dedicated subagent (e.g., Gemini Pro) that analyzes these failures and generates an *Executable Patch* for the harness. In the Triad, this means dynamically editing the `Interfaces`, `Constraints`, or `Verification` rules inside the SOP Task Packet.
3. **Target Agent Runtime**: The Target Agent retries the task within the newly edited, optimized harness.
4. **Environment Reward**: If the patch leads to task success, the Harness Engineer is rewarded (in a production system via GRPO - Group Relative Policy Optimization; in our triad via architectural promotion of the modified SOP).

## 3. Integration into the Antigravity Agentic Triad

We elevate the Triad to a 4-role system:

- **1. Architect**: Scopes and creates the initial SOP Task Packet.
- **2. Worker Fleet (Flash/Pro)**: The "Target Agent Runtime" that executes the code.
- **3. Independent Reviewer**: Checks the diff and tests, acting as the "Environment Reward" gate.
- **4. Harness Engineer [NEW]**: When the Triad reaches the `rethink` phase (after max `fix-first` retries are exhausted), the **Harness Engineer** is invoked. It analyzes the failure trajectories and rewrites the SOP Task Packet (the harness) to provide stricter constraints, better action mediation, or recovery logic, allowing the Worker to succeed on the next attempt.

### Empirical Validation

Across benchmarks like WebShop, ALFWorld, and DBBench, Harness-R1 raises baseline success by up to **+9.3 percentage points**. In our simulated benchmarks (`scripts/simulate_harness_r1.py`), we consistently see similar jumps in task completion when the Engineer dynamically patches overly loose SOP constraints.
