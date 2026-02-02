# Reasoning Models Research Notes

**Date**: 2026-02-02
**Source**: Sebastian Raschka's "Understanding Reasoning LLMs" and related research

---

## Key Definitions

**Reasoning Model**: An LLM specialized to excel at complex tasks requiring multi-step generation with intermediate steps (puzzles, advanced math, coding challenges).

**Chain-of-Thought (CoT)**: The process of including intermediate reasoning steps in the response, revealing the "thought process."

---

## When to Use Reasoning Models vs Standard LLMs

| Task Type | Best Model Type | Why |
|-----------|-----------------|-----|
| Complex puzzles, math proofs | Reasoning Model | Requires multi-step reasoning |
| Coding challenges | Reasoning Model | Benefits from step-by-step problem decomposition |
| Summarization | Standard LLM | Reasoning adds unnecessary overhead |
| Translation | Standard LLM | Direct task, no intermediate steps needed |
| Knowledge Q&A | Standard LLM | Factual retrieval, not reasoning |
| **Pattern synthesis** | **Reasoning Model** | Requires understanding relationships |
| **Blueprint analysis** | **Reasoning Model** | Multi-scale, systemic thinking |

---

## Strengths and Weaknesses of Reasoning Models

### Strengths
- Better at complex, multi-step tasks
- Can show reasoning traces (explainability)
- More accurate on challenging problems
- Can backtrack and self-correct

### Weaknesses
- **More expensive** (more tokens generated)
- **Slower** (longer inference time)
- **More verbose** (sometimes unnecessarily)
- **Can "overthink"** simple tasks
- **Higher VRAM** for longer reasoning chains

---

## The DeepSeek R1 Family

Three variants released:
1. **DeepSeek-R1-Zero**: Pure RL-trained reasoning (671B base)
2. **DeepSeek-R1**: RL + supervised fine-tuning for better formatting
3. **DeepSeek-R1-Distill**: Smaller models (7B-70B) distilled from R1

### Key Insight: Distillation Works
The distilled models (based on Llama and Qwen) retain much of the reasoning capability at a fraction of the size. This is highly relevant for Commons OS.

---

## Four Approaches to Building Reasoning Models

1. **Reinforcement Learning (RL)**: Train model to develop reasoning through reward signals
2. **Supervised Fine-Tuning (SFT)**: Train on datasets with explicit reasoning traces
3. **Distillation**: Transfer reasoning capability from large to small models
4. **Prompting/Inference-time techniques**: Use CoT prompting without model changes

---

## Implications for Commons Language Model

1. **We don't need to train from scratch**: Distilled reasoning models exist
2. **DeepSeek-R1-Distill-Qwen-32B** could be our base model
3. **Reasoning is essential** for pattern synthesis and blueprint analysis
4. **Cost trade-off**: Reasoning models use more tokens, but we need the capability
5. **Hybrid approach**: Use standard LLM for simple queries, reasoning model for complex synthesis

---

## VRAM Implications

From DR-CoT research: Chain-of-Thought increases VRAM usage by ~2.75GB on average due to:
- Longer context from reasoning traces
- KV cache growth during extended generation
- Multiple inference passes for verification

For 32B reasoning model with 128k context:
- Base model: ~20GB (Q4 quantized)
- KV cache at full context: ~30-40GB additional
- **Total**: 50-60GB VRAM for full blueprint analysis

This confirms the need for M3 Ultra (64GB+) or 2x RTX 4090 for enterprise-scale blueprints.
