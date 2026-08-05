# Dynamic Model Switching & Runtime Intervention Mechanics in Google Antigravity

In Google Antigravity, subagent invocations allow runtime manipulation of the underlying LLM engine via the `Model` argument in `invoke_subagent`.

## 1. Supported Model Tiers in Antigravity

| Tier Name | Tool Value | Primary Model | Latency | Token Cost | Optimal Use Case |
|---|---|---|---|---|---|
| **Lite** | `flash_lite` | Gemini Flash Lite | Ultra-Fast ($<1\text{s}$) | Low ($1\times$) | Static linting, schema validation, quick file checks |
| **Flash** | `flash` | Gemini 3.6 Flash | Fast ($1\text{--}3\text{s}$) | Moderate ($3\times$) | Routine Worker (boilerplate, formatting, simple bug fixes) |
| **Pro** | `pro` | Gemini Pro | Deep ($5\text{--}15\text{s}$) | High ($10\times$) | Complex Worker (core algorithms, multi-file edits) & Reviewer |
| **Inherit** | `inherit` | Parent Model | Variable | Variable | Default fallback |

---

## 2. Dynamic Model Escalation Protocol (Runtime Intervention)

To balance token budget and response latency with zero degradation in code quality, the **Architect** uses dynamic escalation:

```text
[Task Received] ──► Architect Evaluates Complexity
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    [Routine / Well-Scoped]       [Complex / Wide Impact]
     Model: flash (Attempt 1)     Model: pro (Attempt 1)
             │                           │
             ▼                           ▼
      [Sol Reviewer]              [Sol Reviewer]
       (Model: pro)                (Model: pro)
             │                           │
     ┌───────┴───────┐           ┌───────┴───────┐
     ▼               ▼           ▼               ▼
  [ship]       [fix-first]    [ship]       [fix-first]
  (Done)       (Attempt 2)    (Done)       (Attempt 2)
                   │                           │
                   ▼                           ▼
            ESCALATE MODEL              RETRY MODEL
            Model: pro                  Model: pro
                   │                           │
                   ▼                           ▼
            [Sol Reviewer]              [Sol Reviewer]
             (Model: pro)                (Model: pro)
```

### Escalation Triggers
- **Attempt 1 (Routine)**: Dispatch to `flash`. High throughput, low cost.
- **Trigger**: If Reviewer returns `fix-first` on Attempt 1, the failure may indicate subtle logic errors beyond `flash` reasoning.
- **Intervention (Attempt 2)**: Architect dynamically escalates `Model` from `flash` to `pro` for Attempt 2.
- **Reviewer Isolation**: Independent Reviewer **ALWAYS** runs on `Model: pro` in a **fresh subagent conversation ID**.
