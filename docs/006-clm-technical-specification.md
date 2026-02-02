# Commons Language Model: Technical Specification

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Overview

This document provides the technical specification for building and deploying the **Commons Language Model (CLM)**, a domain-specialized language model that can run on consumer-grade hardware. The CLM is designed to embody the principle of **Fractal Sovereignty**: intelligence that lives where the user is, not in a distant cloud.

---

## 2. Hardware Requirements

### Target Hardware Profiles

The CLM must be deployable across a range of consumer hardware. We define three target profiles:

| Profile | Hardware | VRAM/RAM | Target Model Size | Use Case |
|---------|----------|----------|-------------------|----------|
| **Minimal** | M2 MacBook Air, RTX 3060 | 8-12GB | 3-7B parameters | Basic pattern retrieval, simple queries |
| **Standard** | M3 Pro Mac, RTX 4070 | 16-18GB | 7-14B parameters | Full CLM capabilities, fine-tuning |
| **Advanced** | M3 Max Mac, RTX 4090 | 24-48GB | 14-32B parameters | Extended context, complex reasoning |

### Key Insight: Unified Memory Advantage

Apple Silicon's unified memory architecture is particularly well-suited for local LLMs. An M3 Pro with 36GB unified memory can run models that would require a $2,000+ GPU on a PC. This makes Macs an excellent target platform for the CLM.

---

## 3. Base Model Selection

### Evaluation Criteria

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Size** | High | Must fit in consumer VRAM |
| **Quality** | High | Must produce coherent, accurate responses |
| **License** | High | Must be permissively licensed (Apache 2.0, MIT) |
| **Fine-tunability** | Medium | Must support efficient fine-tuning (QLoRA) |
| **Ecosystem** | Medium | Should have good tooling support |

### Recommended Base Models

| Model | Parameters | License | VRAM (Inference) | VRAM (Fine-tuning) | Notes |
|-------|-----------|---------|------------------|-------------------|-------|
| **Phi-4** | 14B | MIT | ~10GB | ~15GB | Excellent reasoning, Microsoft-backed |
| **Qwen 2.5** | 7B/14B | Apache 2.0 | 6-10GB | 10-15GB | Strong multilingual, Alibaba-backed |
| **Llama 3.3** | 8B/70B | Llama 3 | 6-40GB | 10-60GB | Industry standard, Meta-backed |
| **Mistral Small** | 22B | Apache 2.0 | ~14GB | ~20GB | Good balance of size and quality |
| **Gemma 3** | 9B/27B | Gemma | 8-18GB | 12-24GB | Google-backed, strong performance |

### Primary Recommendation: Phi-4 (14B)

For the initial CLM, we recommend **Phi-4** as the base model:

1. **Size**: 14B parameters fits comfortably on standard consumer hardware.
2. **Quality**: State-of-the-art reasoning for its size class.
3. **License**: MIT license allows unrestricted use and modification.
4. **Fine-tuning**: Well-supported by Unsloth and other tools.
5. **Quantization**: Excellent performance when quantized to 4-bit.

**Fallback**: Qwen 2.5-7B for minimal hardware profiles.

---

## 4. Fine-Tuning Approach

### Method: QLoRA (Quantized Low-Rank Adaptation)

QLoRA enables fine-tuning of large models on consumer hardware by:
1. Quantizing the base model to 4-bit precision.
2. Training only small "adapter" layers (LoRA).
3. Keeping the base model frozen.

**Memory Savings**: QLoRA reduces fine-tuning memory requirements by 3-4x compared to full fine-tuning.

### Tooling: Unsloth

[Unsloth](https://unsloth.ai) is the recommended fine-tuning framework:

- **2x faster training** than standard implementations.
- **70% less VRAM** usage.
- **3GB VRAM minimum** for small models.
- **Native support** for Phi-4, Qwen, Llama, Gemma.
- **Mac support** via Unsloth-MLX.

### Fine-Tuning Configuration

```python
# Recommended QLoRA configuration for CLM
lora_config = {
    "r": 16,                    # LoRA rank
    "lora_alpha": 32,           # LoRA alpha
    "lora_dropout": 0.05,       # Dropout rate
    "target_modules": [         # Modules to adapt
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    "bias": "none",
    "task_type": "CAUSAL_LM"
}

training_args = {
    "per_device_train_batch_size": 2,
    "gradient_accumulation_steps": 4,
    "num_train_epochs": 3,
    "learning_rate": 2e-4,
    "fp16": True,               # Use FP16 for training
    "logging_steps": 10,
    "save_strategy": "epoch"
}
```

---

## 5. Inference Architecture

### Local Inference Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Runtime** | llama.cpp / Ollama | Efficient local inference |
| **Format** | GGUF | Optimized model format for CPU/GPU |
| **Quantization** | Q4_K_M or Q5_K_M | Balance of quality and speed |
| **API** | OpenAI-compatible | Standard interface for applications |

### Deployment Options

1. **Ollama** (Recommended for ease of use)
   - Simple installation and model management.
   - OpenAI-compatible API.
   - Cross-platform (Mac, Linux, Windows).

2. **llama.cpp** (Recommended for performance)
   - Maximum inference speed.
   - Fine-grained control over parameters.
   - Supports all quantization formats.

3. **Jan.ai** (Recommended for end-users)
   - Beautiful desktop application.
   - Built on llama.cpp.
   - No technical knowledge required.

---

## 6. Hybrid RAG Architecture

The CLM is not just a fine-tuned model; it's a hybrid system that combines:

### Component 1: Fine-Tuned Language Model

The base model fine-tuned on:
- Pattern definitions and descriptions.
- Relationship reasoning examples.
- Q&A pairs about patterns.

### Component 2: Vector Store (LanceDB)

Embedded vector database for semantic search:
- All patterns embedded using a local embedding model.
- Enables "find similar patterns" queries.
- Runs locally, no external API calls.

### Component 3: Knowledge Graph (Kuzu)

Embedded graph database for relationship traversal:
- Explicit pattern relationships (ENABLES, REQUIRES, etc.).
- CommonsEntity adoption data.
- Enables "what patterns does Buurtzorg use?" queries.

### Query Pipeline

```
User Query
    │
    ▼
┌─────────────────┐
│ Query Analysis  │ ← LLM classifies query type
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Vector │ │ Graph │ ← Parallel retrieval
│Search │ │Traverse│
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│ Context Fusion  │ ← Combine results
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Generation  │ ← Generate response with context
└────────┬────────┘
         │
         ▼
    Response
```

---

## 7. Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Inference Speed** | >10 tokens/sec | Usable interactive experience |
| **First Token Latency** | <2 seconds | Responsive feel |
| **Memory Usage** | <12GB | Fits on standard hardware |
| **Pattern Retrieval Accuracy** | >90% | Correct pattern for query |
| **Relationship Reasoning** | >80% | Correct relationship identification |

---

## 8. Development Phases

### Phase 1: Minimum Viable Model (4 weeks)

- [ ] Prepare training dataset from patterns.
- [ ] Fine-tune Phi-4 using QLoRA.
- [ ] Export to GGUF format.
- [ ] Deploy via Ollama.
- [ ] Basic CLI interface.

### Phase 2: Hybrid RAG (4 weeks)

- [ ] Embed all patterns using local embedding model.
- [ ] Build LanceDB vector store.
- [ ] Build Kuzu knowledge graph.
- [ ] Implement query pipeline.
- [ ] Integrate with fine-tuned model.

### Phase 3: Polish & Distribution (4 weeks)

- [ ] Desktop application (Jan.ai integration or custom).
- [ ] Documentation and tutorials.
- [ ] Model hosting on Hugging Face.
- [ ] Community testing and feedback.

---

## 9. Open Questions

1. **Embedding Model**: Which local embedding model to use? (Candidates: nomic-embed-text, bge-small, e5-small)
2. **Context Window**: How much context is needed? (8K vs 32K vs 128K)
3. **Multi-turn Memory**: How to handle conversation history efficiently?
4. **Update Mechanism**: How to update the model as patterns are added?

---

## 10. Conclusion

The Commons Language Model is technically feasible on consumer hardware today. With Phi-4 as the base model, QLoRA for fine-tuning, and a hybrid RAG architecture, we can build a domain-specialized intelligence that runs locally and embodies the principle of Fractal Sovereignty.

The next step is to prepare the training data from our pattern corpus.
