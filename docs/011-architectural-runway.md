# Architectural Runway for the Context Engine (v2)

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Executive Summary

This document outlines the revised architectural runway for the Context Engine, acknowledging that a basic RAG capability already exists via the Commons Suit Lean CustomGPTs. This runway therefore begins from our actual starting point and charts a direct path toward a sovereign, embodied Commons Language Model (CLM).

Our approach is **progressive sovereignty**—incrementally moving capabilities from external dependencies to our own infrastructure.

---

## 2. The Four Milestones (Revised)

We will progress through four distinct milestones, each delivering a significant upgrade in capability and sovereignty.

| Milestone | Name | Core Capability | Time to Value | Key Tech |
|---|---|---|---|---|
| **M0** | **CustomGPTs** | Basic Q&A | **Existing** | RAG + OpenAI |
| **M1** | **Relationship Navigator** | Graph-Aware Retrieval | 4-6 weeks | Graph DB + RAG |
| **M2** | **Domain Expert** | Fine-Tuned Reasoning | 8-10 weeks | CLM-7B (Fine-tuned) |
| **M3** | **Fractal Architect** | Full Blueprint Synthesis | 16-20 weeks | CLM-32B (Embodied) |

---

## 3. Milestone 0: CustomGPTs (The Baseline)

-   **Status**: Already implemented and providing value.
-   **Capability**: Answers "what is X?" questions based on the pattern library.
-   **Limitation**: Relies on OpenAI, lacks relationship awareness, no sovereignty.

---

## 4. Milestone 1: Relationship Navigator (The First Step to Sovereignty)

-   **Goal**: Go beyond simple retrieval to understand and explain relationships between patterns, building the first piece of our own infrastructure.
-   **User Experience**: The assistant can now answer "how" and "why" questions about pattern connections.
-   **Architecture**:
    -   **Graph DB**: Kuzu, populated with `ENABLERS`, `REQUIRES`, `TENSIONS_WITH` relationships.
    -   **Pipeline**: Hybrid RAG that queries both a vector store and the graph database.
    -   **LLM**: Can still use an external LLM (GPT-4.1-mini) for this phase, but the retrieval logic is now ours.
-   **Value Delivered**: Answers "how" questions. (e.g., "How does Customer Discovery enable Product-Market Fit?")
-   **Timeline**: 4-6 weeks.

---

## 5. Milestone 2: Domain Expert (Embodying Knowledge)

-   **Goal**: Replace the generic external LLM with a fine-tuned Commons Language Model that understands the *language* of our domain.
-   **User Experience**: Answers are more nuanced, use correct terminology, and demonstrate deeper understanding.
-   **Architecture**:
    -   **LLM**: **CLM-7B**, a small model fine-tuned on the pattern corpus and Q&A pairs.
    -   **Deployment**: Hosted on the Commons Inference Service (cloud).
-   **Value Delivered**: Deeper domain expertise, lower reliance on external APIs, increased sovereignty.
-   **Dependencies**: M1 must be complete. Training data pipeline must be built.

---

## 6. Milestone 3: Fractal Architect (The Full Vision)

-   **Goal**: Achieve the full vision of a locally-runnable, blueprint-aware Fractal Architecture Engine.
-   **User Experience**: Users can load entire organizational blueprints for deep, systemic analysis on their local machines.
-   **Architecture**:
    -   **LLM**: **CLM-32B**, the full Medium Language Model.
    -   **Deployment**: Local-first via Ollama/LM Studio.
    -   **Context**: Hierarchical context compression for >128k token blueprints.
-   **Value Delivered**: Holistic synthesis, contradiction detection, emergent pattern identification, full sovereignty.
-   **Dependencies**: M2 must be complete. Local deployment stack must be finalized.

---

## 7. Conclusion

This revised runway provides a clear, iterative path that builds on our existing capabilities. It prioritizes the most valuable next step—**relationship awareness**—and charts a direct course toward a sovereign, embodied, and fractal intelligence for the commons.

