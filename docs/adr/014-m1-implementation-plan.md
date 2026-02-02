# ADR-014: M1 Implementation Plan - Relationship Navigator

**Status:** Proposed
**Date:** 2026-02-02
**Author:** higgerix

---

## 1. Context

This ADR documents the implementation plan for **Milestone 1 (M1): Relationship Navigator**, as defined in the [Architectural Runway (v2)](011-architectural-runway.md). The core decision is to build the Context Engine foundation on the **new, richer schema** defined in the [Context Engine Specification](005-context-engine-specification-v2.md), rather than the legacy `graph.json` data.

This approach prioritizes building the right foundation over a quick win, ensuring that M1 is a direct step toward the full vision of a sovereign, embodied CLM.

---

## 2. Decision

M1 will be implemented as a **foundational build-out** of the Context Engine, focusing on the new schema and AI-assisted relationship discovery. The legacy `graph.json` will be deprecated and replaced.

### 2.1. Key Implementation Choices

| Component | Decision | Rationale |
|---|---|---|
| **Database** | **Kuzu** | Implements the new schema from the specification, including `Pattern`, `CommonsEntity`, `Concept`, and `Source` nodes, and richly-typed relationships. |
| **Relationship Discovery** | **AI-Assisted Pipeline** | An LLM (GPT-4.1-mini) will be used to suggest `ENABLES`, `REQUIRES`, and `TENSIONS_WITH` relationships between all 1,282 patterns. |
| **Relationship Approval** | **Human Review Workflow** | AI-suggested relationships will be stored in a staging area (e.g., a JSON file) and require human approval before being committed to the main graph. |
| **Retrieval Pipeline** | **Hybrid (Vector + Graph)** | Queries will leverage both semantic search (vectors) and relationship traversal (graph) to provide context-aware answers. |
| **LLM for Answers** | **External LLM (GPT-4.1-mini)** | For M1, we will continue to use an external LLM for generating natural language answers. The focus is on the retrieval pipeline, not the generation model. |

---

## 3. Consequences

### Positive
-   **Builds the right foundation**: We are not building on a legacy system we intend to replace.
-   **Enables valuable relationships**: The graph will immediately contain the most valuable `ENABLES` and `REQUIRES` relationships.
-   **Creates a virtuous cycle**: The human review process will generate high-quality training data for M2 (fine-tuning the CLM).
-   **Direct path to sovereignty**: Each component is a step toward a fully sovereign system.

### Negative
-   **Slower time to value**: This approach will take longer than simply using the existing `graph.json` (4-6 weeks vs. 1-2 weeks).
-   **Requires human-in-the-loop**: The human review workflow is a bottleneck, but a necessary one for quality.
-   **Initial cost**: There will be a one-time cost for the AI-assisted relationship discovery (estimated at ~$20-50 for 1.6M pattern pairs).

---

## 4. Implementation Steps

1.  **Schema Implementation** (1 week): Create Kuzu database with the new schema.
2.  **AI Relationship Discovery** (1 week): Build and run the script to generate suggested relationships.
3.  **Human Review UI** (1 week): Create a simple web interface for reviewing and approving relationships.
4.  **Hybrid Retrieval Pipeline** (2 weeks): Build the query logic that combines vector and graph search.
5.  **API Endpoint** (1 week): Create a simple API for the web presence to query.

---

## 5. Alternatives Considered

### Alternative 1: Use Legacy `graph.json`
-   **Description**: Build Kuzu on the existing `graph.json` data.
-   **Reason for Rejection**: This would build on an insufficient schema and delay the inevitable migration. The most valuable relationships (`enables`/`requires`) are missing.

### Alternative 2: Manual Curation Only
-   **Description**: Manually define all relationships without AI assistance.
-   **Reason for Rejection**: With 1.6 million potential pairwise relationships, this is not feasible. AI provides the necessary scale, with humans ensuring quality.

