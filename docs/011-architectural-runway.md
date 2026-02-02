# Architectural Runway for the Context Engine

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Executive Summary

This document outlines the architectural runway for the Context Engine, providing a phased implementation path from a simple, high-value RAG system to the full vision of an embodied Commons Language Model (CLM). This runway ensures that each development cycle delivers tangible value while building foundational capabilities for the next phase.

Our approach is **incremental enhancement**, not a monolithic build.

---

## 2. The Four Milestones

We will progress through four distinct milestones, each delivering a significant upgrade in capability.

| Milestone | Name | Core Capability | Time to Value | Key Tech |
|---|---|---|---|---|
| **M1** | **Pattern Assistant** | Semantic Search & Q&A | 2-3 weeks | RAG + External LLM |
| **M2** | **Relationship Navigator** | Graph-Aware Retrieval | 4-6 weeks | Graph DB + RAG |
| **M3** | **Domain Expert** | Fine-Tuned Reasoning | 8-10 weeks | CLM-7B (Fine-tuned) |
| **M4** | **Fractal Architect** | Full Blueprint Synthesis | 16-20 weeks | CLM-32B (Embodied) |

---

## 3. Milestone 1: Pattern Assistant (The Quick Win)

-   **Goal**: Provide immediate value to the web presence with a smart search and Q&A assistant.
-   **User Experience**: A chat widget on the patterns website that answers questions based on the pattern library.
-   **Architecture**:
    -   **Embeddings**: `nomic-embed-text` (local) or `text-embedding-3-small` (cloud).
    -   **Vector Store**: LanceDB.
    -   **LLM**: GPT-4.1-mini or Claude Haiku (via API).
    -   **Pipeline**: Simple RAG.
-   **Value Delivered**: Answers "what" questions. (e.g., "What is a steward-ownership model?")
-   **Timeline**: 2-3 weeks.

---

## 4. Milestone 2: Relationship Navigator (Adding Context)

-   **Goal**: Go beyond simple retrieval to understand and explain relationships between patterns.
-   **User Experience**: The assistant can now answer "how" and "why" questions about pattern connections.
-   **Architecture**:
    -   **Graph DB**: Kuzu, populated with `ENABLERS`, `REQUIRES`, `TENSIONS_WITH` relationships.
    -   **Pipeline**: Hybrid RAG that queries both the vector store (for semantic similarity) and the graph database (for explicit relationships).
-   **Value Delivered**: Answers "how" questions. (e.g., "How does Customer Discovery enable Product-Market Fit?")
-   **Dependencies**: M1 must be complete. Graph relationship data must be populated.

---

## 5. Milestone 3: Domain Expert (Embodying Knowledge)

-   **Goal**: Replace the generic external LLM with a fine-tuned Commons Language Model that understands the *language* of our domain.
-   **User Experience**: Answers are more nuanced, use correct terminology, and demonstrate deeper understanding.
-   **Architecture**:
    -   **LLM**: **CLM-7B**, a small model fine-tuned on the pattern corpus and Q&A pairs.
    -   **Deployment**: Hosted on the Commons Inference Service (cloud).
-   **Value Delivered**: Deeper domain expertise, lower reliance on external APIs.
-   **Dependencies**: M2 must be complete. Training data pipeline must be built.

---

## 6. Milestone 4: Fractal Architect (The Full Vision)

-   **Goal**: Achieve the full vision of a locally-runnable, blueprint-aware Fractal Architecture Engine.
-   **User Experience**: Users can load entire organizational blueprints for deep, systemic analysis on their local machines.
-   **Architecture**:
    -   **LLM**: **CLM-32B**, the full Medium Language Model.
    -   **Deployment**: Local-first via Ollama/LM Studio.
    -   **Context**: Hierarchical context compression for >128k token blueprints.
-   **Value Delivered**: Holistic synthesis, contradiction detection, emergent pattern identification.
-   **Dependencies**: M3 must be complete. Local deployment stack must be finalized.

---

## 7. Conclusion

This architectural runway provides a clear, iterative path to realizing the full vision of the Context Engine. It prioritizes delivering value quickly (M1) while ensuring that each step is a deliberate move toward the ultimate goal of a sovereign, embodied, and fractal intelligence for the commons (M4).

