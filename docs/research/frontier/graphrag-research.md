# GraphRAG Research Notes - Frontier Knowledge Systems

**Date**: 2026-02-02
**Author**: higgerix

---

## 1. The Core Insight

> "Retrieval alone isn't reasoning."

Traditional RAG retrieves text chunks. GraphRAG retrieves **entities and relationships** - enabling:
- **Connected** context
- **Multi-hop** reasoning
- **Traceable** answers
- **Structurally grounded** responses

---

## 2. When GraphRAG Excels

Traditional RAG struggles when answers require:

| Challenge | Example |
|-----------|---------|
| **Multi-hop reasoning** | A relates to B which triggers C |
| **Cross-document synthesis** | Policy + ticket + runbook + architecture notes |
| **Entity-centric questions** | "Which customers were impacted by services that depend on X?" |
| **Global thematic questions** | "What patterns repeat across incidents?" |

---

## 3. GraphRAG Landscape (2026)

### Microsoft GraphRAG
- **Architecture**: Local search (entity-based) + Global search (community-report summarization)
- **Strength**: Clean separation of concerns, Azure ecosystem integration
- **Trade-off**: Requires tuning effort for extraction, chunking, hierarchy

### LightRAG (HKU)
- **Architecture**: Dual-level retrieval (low-level factual + high-level conceptual)
- **Strength**: Research-backed, active open-source
- **Trade-off**: Still requires data cleaning and extraction tuning

### fast-graphrag
- **Architecture**: Personalized PageRank for graph exploration
- **Strength**: Developer-friendly, fast prototyping
- **Trade-off**: Toolkit, not platform - need to build governance around it

### EcphoryRAG
- **Architecture**: Cue-based activation + multi-hop expansion
- **Strength**: Best benchmark results (0.392 → 0.474 Exact Match)
- **Trade-off**: Research system, productionization effort needed

---

## 4. Evaluation Criteria for GraphRAG

| Dimension | Question |
|-----------|----------|
| **Reasoning depth** | Can it support multi-hop retrieval while staying auditable? |
| **Indexing/governance** | How painful is entity extraction, incremental updates, permissioning? |
| **Ecosystem fit** | Does it integrate with your LLM stack? |
| **Cost/latency** | Graph construction can get expensive - does it scale? |
| **Build vs buy** | Open-source for experimentation, commercial for time-to-value |

---

## 5. Implications for Commons OS

### Why GraphRAG Matters for Context Engine

The Commons OS pattern library is **inherently connected**:
- Patterns ENABLE other patterns
- Patterns REQUIRE other patterns
- Patterns TENSION_WITH other patterns
- Lighthouses ADOPT patterns
- Entities INSPIRE other entities

This is exactly the use case where GraphRAG excels over traditional RAG.

### Proposed Architecture

```
User Query
    ↓
[Context Understanding] - Identify user's context (persona, scale, domain)
    ↓
[Graph Traversal] - Find relevant patterns via relationship paths
    ↓
[Community Summarization] - Synthesize thematic insights
    ↓
[LLM Generation] - Generate contextual response
```

### Key Components

1. **Entity Extraction**: Patterns, Lighthouses, Concepts as nodes
2. **Relationship Modeling**: ENABLES, REQUIRES, TENSIONS_WITH as edges
3. **Community Detection**: Cluster related patterns for thematic queries
4. **Hybrid Retrieval**: Graph traversal + vector similarity

---

## 6. Open Questions

1. Should we use Microsoft GraphRAG, LightRAG, or build custom?
2. How do we handle incremental updates as new patterns are added?
3. What's the right balance between graph structure and vector embeddings?
4. How do we make the graph traversal explainable to users?
