# CLM Technical Specification v2

**Date**: 2026-02-02
**Author**: higgerix
**Status**: Updated based on MLM Feasibility Report

---

## 1. Core Model Selection

Based on the requirement to handle "Full Context" organizational blueprints and perform complex, multi-scale reasoning, we are upgrading our target model from the 14B to the 27B-32B parameter range. This is the sweet spot for Medium Language Models (MLMs).

-   **Primary Choice**: **Qwen2.5-32B**. Excellent multilingual capabilities and strong reasoning, with a growing community.
-   **Secondary Choice**: **Gemma 2 (27B)**. Strong backing from Google, good performance, but potentially more restrictive licensing.
-   **Efficiency Choice**: **Mistral Small (22B)**. Highly optimized for reasoning and structured data, but may struggle with the largest contexts.

**Rationale**: Models in this range provide near-frontier reasoning capabilities while remaining small enough for prosumer hardware, avoiding the "attention collapse" issues seen in smaller models on long documents.

---

## 2. Hardware Tiers for Deployment

We will officially support three tiers of hardware, reflecting the different scales of Commons Entities.

| Tier | Target User | Blueprint Size | Recommended Hardware | VRAM | Expected Performance |
|---|---|---|---|---|---|
| **1. Prosumer** | Startup Founder, Researcher | < 40k tokens | M3 Max (64GB) or 1x RTX 4090 (24GB) | 24-64GB | Interactive, near real-time |
| **2. Professional** | Mid-Size Org, Urban Planner | < 100k tokens | M3 Ultra (128GB) or 2x RTX 4090 (48GB) | 64-128GB | Smooth, handles full context |
| **3. Enterprise** | Large Enterprise, City Gov | > 128k tokens | 4x RTX 4090 or Cloud GPU (H100) | > 128GB | Required for full blueprint synthesis |

**The VRAM Hard Boundary**: The critical factor is the KV cache size, which scales with context length. If the context exceeds available VRAM, performance will degrade by 5x-20x. Our hardware recommendations are designed to keep the full context in VRAM.

---

## 3. Fine-Tuning and Quantization

-   **Fine-Tuning Method**: **QLoRA via Unsloth**. This is non-negotiable. It allows us to fine-tune a 32B model on a single 24GB GPU, making the project feasible for community contributors.
-   **Quantization**: **4-bit (GGUF Q4_K_M)**. This offers the best balance of performance and model quality, reducing VRAM usage by ~75% with minimal perplexity loss.

---

## 4. Context Management Strategy

To mitigate the "Lost-in-the-Middle" problem with long contexts, we will implement a **Hierarchical Context Compression** strategy.

1.  **High-Resolution Window**: The most recent timeslices and the active vision of a blueprint are kept in full detail.
2.  **Anchor Summaries**: Older timeslices or less relevant sections are recursively summarized by the CLM itself.
3.  **Graph-Based Linking**: The summaries are linked back to the full-text versions in the knowledge graph, allowing the model to "zoom in" on details when required.

This approach allows us to handle contexts that exceed even the 128k token window by managing the model's attention effectively.

---

## 5. Local Deployment Stack

-   **Inference Engine**: **Ollama** and **llama.cpp**. These are the community standards for local inference, providing broad hardware support and ease of use.
-   **Vector Store**: **LanceDB**. Embedded, zero-copy, and highly efficient for local RAG.
-   **Graph Database**: **Kuzu**. Embedded, fast, and designed for local graph analysis.

**Principle**: The entire stack must be runnable locally without requiring external servers or cloud services, ensuring data sovereignty.

---

## 6. Conclusion

By targeting the 32B parameter MLM sweet spot and designing for prosumer-class hardware, we can create a powerful Fractal Architecture Engine that is both accessible and sovereign. The combination of a larger model, sophisticated context management, and a local-first stack provides a clear technical path to realizing the vision of the Commons Language Model.
