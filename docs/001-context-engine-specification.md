# Context Engine Specification v0.1

**Date**: 2026-02-02  
**Status**: Draft  
**Authors**: Manus AI

---

## 1. Introduction

This document provides the technical specification for the Commons OS Context Engine, a living semantic graph designed to connect patterns, entities, and perspectives. It synthesizes findings from deep research into schema design, governance, context modeling, and technical stack options, as outlined in ADR-013.

### 1.1 Vision

The Context Engine transforms the pattern library from a static collection of documents into a dynamic, context-aware knowledge graph. Its purpose is to answer the question: **"Given who I am and what I'm trying to achieve, what patterns are most relevant to me right now?"**

### 1.2 Core Principles

| Principle | Description |
|-----------|-------------|
| **Living Ontology** | The graph evolves based on usage and feedback, not just manual curation. |
| **Fractal Abstraction** | A unified `CommonsEntity` node type represents value-creating systems at all scales. |
| **Context-Aware Retrieval** | Queries are transformed by the user's context to provide personalized, relevant results. |
| **Hybrid Search** | Combines the structured relationships of a graph with the semantic nuance of vector search. |
| **Transparent Governance** | A tiered governance model balances stability with adaptability. |
| **Embedded First** | The default architecture prioritizes simplicity, portability, and privacy. |

---

## 2. Schema Definition

The Context Engine uses a property graph model composed of nodes, relationships, and properties.

### 2.1 Node Types

| Node Label | Description | Key Properties |
|------------|-------------|----------------|
| `Pattern` | A documented pattern for value creation. | `id`, `title`, `slug`, `domains`, `categories` |
| `CommonsEntity` | A value-creating system at any scale. | `id`, `name`, `type`, `scale`, `context_profile` |
| `Concept` | An abstract idea or principle. | `id`, `name`, `definition` |
| `Source` | A reference, book, or authority. | `id`, `title`, `author`, `url` |
| `Domain` | A high-level commons domain. | `id`, `name`, `description` |

### 2.2 Relationship Types

| Relationship Type | Description | Properties |
|-------------------|-------------|------------|
| `ENABLES` | Pattern enables another pattern. | `weight`, `confidence`, `provenance` |
| `REQUIRES` | Pattern requires another pattern. | `weight`, `confidence`, `provenance` |
| `TENSIONS_WITH` | Pattern creates tension with another. | `weight`, `confidence`, `provenance` |
| `SPECIALIZES` | Pattern is a specialization of another. | `weight`, `confidence`, `provenance` |
| `ADOPTED_BY` | Pattern is adopted by a CommonsEntity. | `timestamp`, `decision_trace` |
| `INSPIRED_BY` | CommonsEntity is inspired by another. | `weight` |
| `PART_OF` | CommonsEntity is part of a larger one. | `weight` |
| `AUTHORED_BY` | Pattern is authored by a Source. | | 
| `BELONGS_TO` | Pattern belongs to a Domain. | | 

### 2.3 Relationship Properties

| Property | Type | Description |
|----------|------|-------------|
| `weight` | Float | Strength of the relationship (0.0-1.0). |
| `confidence` | Float | Certainty about the relationship's existence. |
| `provenance` | String | Source of the relationship (human, AI, usage). |
| `valid_from` | DateTime | When the relationship became valid. |
| `valid_to` | DateTime | When the relationship expired (null if current). |
| `decision_trace` | String | History of changes to this relationship. |

---

## 3. Governance Model

The Context Engine employs a tiered governance model to balance stability and adaptability.

### 3.1 Governance Tiers

| Tier | Scope | Approval Process |
|------|-------|------------------|
| **Tier 1: Schema** | Node/edge types, core properties | ADR + community review + deprecation period |
| **Tier 2: Content** | New patterns, entities, relationships | Single curator or AI suggestion + validation |
| **Tier 3: Metadata** | Relationship weights, confidence scores | Automated based on usage signals |

### 3.2 Evolution Triggers

| Trigger | Description |
|---------|-------------|
| **External** | Changes in the domain being modeled. |
| **Internal** | Inconsistencies or gaps discovered within the graph. |
| **Usage** | Patterns of use that suggest missing or incorrect relationships. |
| **Persistent Explanatory Failure** | The system consistently fails to answer user queries. |

---

## 4. Context Modeling

Context is modeled as a profile associated with each `CommonsEntity`.

### 4.1 Context Profile Schema

```yaml
context_profile:
  static:
    scale: organization
    type: startup
    domains: [business, startup]
    values: [sustainability, community]
  dynamic:
    stage: growth
    goals: [scale_team, expand_market]
    constraints: [limited_budget, time_pressure]
  relational:
    similar_to: [entity_123, entity_456]
    aspires_to: [buurtzorg, mondragon]
    adopted_patterns: [sociocracy, lean_startup]
```

### 4.2 Context-Aware Retrieval Process

1. **Parse Query**: Extract intent and keywords.
2. **Load Context**: Retrieve user's context profile.
3. **Expand Query**: Add context-relevant terms and filters.
4. **Retrieve**: Get initial results from graph + vector search.
5. **Re-rank**: Adjust ranking based on context weights.
6. **Present**: Show results with context-relevant explanations.

---

## 5. Technical Stack

The Context Engine uses a dual-embedded database architecture for simplicity, portability, and performance.

### 5.1 Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Graph Database** | Kuzu | Stores structured relationships between nodes. |
| **Vector Database** | LanceDB | Stores pattern embeddings for semantic search. |
| **Query Engine** | Custom Python | Orchestrates hybrid queries and context-aware re-ranking. |

### 5.2 Data Flow

1. **Source of Truth**: Markdown files in the `patterns-repo`.
2. **Build Process**: A CI/CD pipeline parses files, generates embeddings, and builds the Kuzu and LanceDB databases.
3. **Query Time**: The Query Engine performs a hybrid search across both databases.
4. **Results**: Merged, ranked, and explained results are returned via an API.

### 5.3 File-Based Fallback

For static deployments (e.g., GitHub Pages), the build process will also generate `graph.json` and `search_index.json` files to enable basic client-side search without a database backend.

---

## 6. Open Questions & Future Work

This specification is a living document. Key open questions to be addressed in future research and development include:

- Incremental updates without full rebuilds.
- Optimal embedding models and dimensions.
- Schema versioning and migration strategies.
- Handling of conflicting perspectives and temporal context.
- Incentivizing community participation in governance.

---

## 7. References

[1] Zerhoudi, S., & Granitzer, M. (2024). *PersonaRAG: Enhancing Retrieval-Augmented Generation Systems with User-Centric Agents*. arXiv. https://arxiv.org/abs/2407.09394

[2] Javed, M., Abgaz, Y. M., & Pahl, C. (2013). *Ontology Change Management and Identification of Change Patterns*. Journal on Data Semantics, 2(2-3), 119–143. https://doi.org/10.1007/s13740-013-0024-2

[3] Shimizu, C., Hammar, K., & Hitzler, P. (2021). *Modular Ontology Modeling*. Semantic Web, 12(5), 795-820. https://www.semantic-web-journal.net/system/files/swj2806.pdf

[4] Sarmah, B., et al. (2024). *HybridRAG: Integrating Knowledge Graphs and Vector Retrieval Augmented Generation for Efficient Information Extraction*. Proceedings of the 5th International Conference on Document Analysis and Recognition.

[5] Jin, C., et al. (2023). *Kùzu Graph Database Management System*. CIDR 2023.
