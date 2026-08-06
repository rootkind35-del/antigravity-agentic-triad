# Dynamic Model Switching & FrugalGPT Cascade Mechanics

Grounded in **FrugalGPT (Chen et al., Stanford 2023, arXiv:2305.05176)** and **Google Antigravity Dynamic Model Switching**:

## 1. Supported Model Tiers in Antigravity

| Tier Name | Tool Value | Primary Model | Latency | Token Cost | FrugalGPT Target |
|---|---|---|---|---|---|
| **Lite** | `flash_lite` | Gemini Flash Lite | Ultra-Fast ($<1\text{s}$) | Low ($1\times$) | Static linting, schema validation, quick file checks |
| **Flash** | `flash` | Gemini 3.6 Flash | Fast ($1\text{--}3\text{s}$) | Moderate ($3\times$) | Routine Worker (boilerplate, formatting, simple bug fixes) |
| **Pro** | `pro` | Gemini Pro | Deep ($5\text{--}15\text{s}$) | High ($10\times$) | Complex Worker (core algorithms, multi-file edits) & Reviewer |
| **Inherit** | `inherit` | Parent Model | Variable | Variable | Default fallback |

---

## 2. FrugalGPT Model Cascade & Dynamic Escalation

To maximize accuracy while bounding token expenditure under budget $b$:

$$\max_{\pi} \mathbb{E}_{q \sim Q} [r(\hat{a}, a)] \quad \text{s.t.} \quad \mathbb{E}_{q \sim Q} [c(\pi, q)] \le b$$

### Protocol Steps
1. **Initial Cascade ($f_1 = \text{flash}$)**: Attempt 1 routine tasks run on `Model: flash` ($10\%$ token cost of `pro`).
2. **Verification Trigger ($v(q)$)**: Sol Reviewer evaluates output.
3. **Model Cascade ($f_2 = \text{pro}$)**: If Reviewer returns `fix-first`, the Architect **automatically escalates Attempt 2 to `Model: pro`** to leverage deep reasoning capability.
4. **Reviewer Context Isolation**: Sol Reviewer **ALWAYS** operates on `Model: pro` in a **fresh subagent conversation ID**.
