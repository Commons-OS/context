# CLM Service Model Architecture

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Executive Summary

This document defines the service model architecture for the Commons Language Model (CLM). It addresses the strategic challenge of providing inference capabilities across multiple contexts—local user machines, public websites, and agent-based systems—while upholding our core principles of sovereignty, performance, and cost-effectiveness.

Our recommended approach is a **Hybrid Federated Model**, where inference is pushed to the edge (local-first) whenever possible, with a centralized, community-funded inference service for shared workloads.

---

## 2. The Four Inference Contexts

We must design for four distinct use cases, each with different requirements:

| Context | Primary User | Key Requirement | Recommended Model |
|---|---|---|---|
| **1. Local Blueprinting** | Commons Engineer | Sovereignty, full context | Local MLM (32B) |
| **2. Public Website** | General Public | Low latency, high concurrency | Cloud SLM (7B) |
| **3. Agent Assistance** | Digital Agents (e.g., Manus) | Reasoning, API access | Cloud MLM (32B) |
| **4. CLM Training** | Dev Team | High throughput, GPU power | Cloud GPU (A100/H100) |

---

## 3. The Hybrid Federated Architecture

This model balances local control with the practicality of shared infrastructure.

### Tier 1: Local-First Inference (The Edge)

-   **Use Case**: Local Blueprinting, individual research.
-   **Model**: CLM-32B (4-bit quantized) running via Ollama/LM Studio.
-   **Hardware**: User-owned prosumer hardware (M3 Max, 2x RTX 4090).
-   **Data Flow**: All data remains on the user's machine. No network calls for inference.
-   **Funding**: User bears the hardware cost, ensuring full sovereignty.

### Tier 2: Commons Inference Service (The Cloud)

-   **Use Case**: Public website Q&A, agent assistance, community tools.
-   **Model**: A dual-model endpoint:
    -   **CLM-7B (SLM)**: For fast, low-cost queries (e.g., website search).
    -   **CLM-32B (MLM)**: For complex reasoning tasks (e.g., agent synthesis).
-   **Infrastructure**: Hosted on a pay-per-use inference provider like Together.ai, Replicate, or Groq.
-   **Data Flow**: Queries are sent to the cloud service. Anonymized and subject to a strict privacy policy.
-   **Funding**: Community-funded through a co-op model, grants, or donations. Transparent cost and usage reporting.

### Tier 3: External LLM Fallback (The Frontier)

-   **Use Case**: Tasks beyond the CLM's capabilities (e.g., general knowledge, advanced coding).
-   **Model**: GPT-4.1, Claude 3.1, etc.
-   **Infrastructure**: Accessed via standard API calls.
-   **Data Flow**: User is explicitly notified that their query is being sent to a third-party service.
-   **Funding**: User provides their own API key or uses a metered, pay-per-use system.

---

## 4. The Strategic Role of RAG and Fine-Tuning

Our architecture uses a sophisticated hybrid approach, not just one or the other.

| Layer | Technique | Purpose |
|---|---|---|
| **Foundation** | **Fine-Tuning** | Teaches the CLM the *language* of patterns, relationships, and commons thinking. Builds deep domain understanding. |
| **Context** | **RAG (Vector + Graph)** | Injects *real-time*, specific information (the user's query, their blueprint, relevant patterns) into the prompt. |
| **Reasoning** | **Chain-of-Thought** | The fine-tuned model uses the RAG-provided context to perform multi-step reasoning and generate a synthesized answer. |

**Analogy**: Fine-tuning is like sending the model to university to become an expert. RAG is like giving the expert a specific case file to analyze. Chain-of-Thought is the expert showing their work.

---

## 5. Cost Analysis and Funding Model

### Local Inference
-   **Upfront Cost**: ~$5,000 - $10,000 for prosumer hardware.
-   **Ongoing Cost**: Electricity.
-   **Breakeven**: For heavy users, on-prem hardware can be 30-50% cheaper than cloud over 3 years.

### Commons Inference Service (Estimated)

-   **Assumptions**: Using Together.ai pricing for a shared endpoint.
-   **CLM-7B (SLM)**: ~$0.10 per 1M tokens. Suitable for high-volume, low-cost queries.
-   **CLM-32B (MLM)**: ~$0.70 per 1M tokens. Reserved for reasoning tasks.
-   **Estimated Monthly Cost**: **$500 - $2,000** to serve a moderately active community and website.
-   **Funding Strategy**: A co-op model where community members can contribute to a shared inference pool, supplemented by grants for public access.

---

## 6. Implementation Plan

1.  **Phase 1 (Local First)**: Focus entirely on creating the fine-tuned CLM-32B and optimizing it for local deployment via Ollama. This delivers on the core sovereignty promise.
2.  **Phase 2 (Commons Service)**: Once the local model is stable, deploy 7B and 32B versions to a cloud provider. Build the API and integrate it with the public website.
3.  **Phase 3 (Agent Integration)**: Develop the API and authentication for digital agents to access the Commons Inference Service for reasoning tasks.

---

## 7. Conclusion

This Hybrid Federated Model provides a clear, strategic path forward. It allows us to:

-   **Empower individuals** with sovereign, local-first AI.
-   **Serve the community** with a shared, cost-effective inference service.
-   **Leverage the frontier** by integrating with external LLMs when necessary.

By separating the inference contexts and using a tiered approach, we can build a powerful and sustainable intelligence for the commons.
