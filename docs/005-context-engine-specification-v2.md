# The Commons Language Model: A Specification

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. Introduction: An Engine for the Third Path

This document specifies the architecture for the **Commons Language Model (CLM)**, the core intelligence of the Commons OS. It is not merely a knowledge graph or a search engine; it is the technical manifestation of our philosophy: **The Third Path**.

- **Fractal Sovereignty** is achieved through a local-first, embedded architecture.
- **Symbiotic Co-Creation** is realized through a system that augments, rather than replaces, human intelligence.
- **Living Knowledge** is enabled by a dynamic graph that evolves with community use and contribution.

This specification translates these principles into a concrete technical design.

---

## 2. The Architecture of Symbiosis: A Hybrid Model

The CLM is a hybrid system that combines the strengths of three distinct technologies:

| Component | Technology | Role | Principle |
|-----------|------------|------|-----------|
| **Knowledge Graph** | Embedded Graph DB (Kuzu) | Stores explicit, structured relationships between patterns and entities. | Living Knowledge |
| **Language Model** | Fine-Tuned SLM (e.g., Phi-4) | Understands nuance, generates insights, and reasons about unstructured text. | Symbiotic Co-Creation |
| **Vector Store** | Embedded Vector DB (LanceDB) | Enables semantic search and similarity-based retrieval. | Symbiotic Co-Creation |

These components work in concert, orchestrated by a **Graph-Augmented Generation (GraphRAG)** pipeline. This is not just RAG; it's RAG that understands the explicit structure of our knowledge commons.

---

## 3. The Schema of the Fractal Commons

The knowledge graph is the backbone of the CLM. Its schema is designed to model the Fractal Commons insight.

### Node Types

| Node Type | Description | Example |
|-----------|-------------|---------|
| **Pattern** | A specific, reusable solution to a recurring problem. | `pattern:steward-ownership` |
| **CommonsEntity** | A value-creating system that adopts patterns. This is the core fractal abstraction. | `entity:buurtzorg`, `entity:jane-doe`, `entity:city-of-barcelona` |
| **Concept** | An abstract idea that connects multiple patterns or entities. | `concept:decentralization`, `concept:value-flow` |
| **Source** | The origin of a piece of knowledge (a book, an article, a person). | `source:reinventing-organizations` |

### The `CommonsEntity` Abstraction

This is the key to modeling the fractal nature of the commons. Every `CommonsEntity` node has properties that define its position in the fractal:

```yaml
properties:
  name: "Buurtzorg"
  scale: "organization" # individual, team, organization, network, city, region, ecosystem
  type: "cooperative"
  domain: "healthcare"
```

### Relationship Types (Edges)

Relationships are first-class citizens, with properties for provenance and weight.

| Relationship | Description | Example |
|--------------|-------------|---------|
| `ADOPTS` | An entity uses a pattern. | `(buurtzorg)-[:ADOPTS]->(self-managing-teams)` |
| `ENABLES` | One pattern makes another possible. | `(self-managing-teams)-[:ENABLES]->(holistic-care)` |
| `REQUIRES` | One pattern depends on another. | `(steward-ownership)-[:REQUIRES]->(legal-framework)` |
| `TENSIONS_WITH` | Two patterns have conflicting goals. | `(rapid-growth)-[:TENSIONS_WITH]->(sustainable-pace)` |
| `PART_OF` | An entity is a component of a larger one. | `(team-alpha)-[:PART_OF]->(buurtzorg)` |
| `INSPIRED_BY` | An entity draws inspiration from another. | `(new-coop)-[:INSPIRED_BY]->(mondragon)` |

---

## 4. The Governance of Living Knowledge

The CLM's knowledge base is not static. It evolves through a process inspired by the **Guardian Lattice** and the **S-Curve of Quality**.

### AI-Assisted Curation (The Guardians)

- **Sentinels**: Automated agents that monitor the graph for anomalies (e.g., conflicting relationships, isolated patterns) and flag them for review.
- **Advisors**: LLM-based agents that analyze new contributions (patterns, lighthouses) and suggest relationships, classifications, and quality scores.
- **Human Curators**: The ultimate authority. They review the suggestions from Advisors and approve changes to the graph.

### The S-Curve of Quality

Every pattern and lighthouse contribution moves through a quality progression:

1.  **Bronze (Community Contributed)**: A new submission. Visible in the graph but flagged as unvetted.
2.  **Silver (Expert Reviewed)**: Reviewed by a domain expert for coherence, clarity, and accuracy.
3.  **Gold (Evidence-Backed)**: Validated with real-world evidence from one or more Lighthouse entities.

This process ensures that the graph remains both open to contribution and trustworthy in its core.

---

## 5. The Architecture of Fractal Sovereignty

The CLM is designed to run locally on consumer-grade hardware. This is a non-negotiable architectural principle.

### The Local-First Stack

- **Application Layer**: A simple CLI and API, built with Python, that can be run locally.
- **Intelligence Layer**: The fine-tuned SLM, quantized for efficient inference (e.g., using GGUF format).
- **Knowledge Layer**: The embedded databases (Kuzu for graph, LanceDB for vectors) that live as files on the user's machine.
- **Data Layer**: The source-of-truth Markdown files for patterns and entities.

### The Synchronization Model

The local CLM instance can be updated from the main Commons OS repository via a simple `git pull`. A build script then re-indexes the graph and vector stores from the updated Markdown files. This federated model allows for both global coherence and local sovereignty.

---

## 6. Conclusion: From Specification to Implementation

This specification provides the blueprint for a Commons Language Model that is not just powerful, but principled. It is an engine for thought, a tool for co-creation, and a testament to the power of the Third Path.

The next step is to translate this specification into a concrete implementation roadmap.
