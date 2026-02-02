# Context Engine Research Brief

**Document**: 001-research-brief  
**Date**: 2026-02-02  
**Status**: Active

---

## 1. Research Objective

Define the architecture, schema, and governance model for the Context Engine—a living semantic graph that will power context-aware pattern discovery across the Commons OS ecosystem.

## 2. Background

The Commons OS Pattern Library contains 1,200+ patterns across multiple domains (business, startup, security). The current classification system (ADR-012) supports multi-value tagging but lacks:

- Rich relationships between patterns
- Context-aware retrieval based on user persona
- Mechanisms for graph evolution
- Temporal and provenance metadata

## 3. Key Research Areas

### 3.1 Schema Definition

**Questions:**
- What node types are needed? (Pattern, Persona, Concept, Source, Organization, Domain)
- What edge types capture meaningful relationships? (enables, requires, tensions_with, specializes, etc.)
- What properties should nodes and edges have?
- How do we model multi-domain membership?

**Deliverable:** Formal schema specification in JSON Schema or similar format

### 3.2 Evolution Governance

**Questions:**
- What triggers graph evolution? (Persistent explanatory failure, human judgment, AI suggestion, usage patterns)
- Who has authority to modify the graph? (Curators, community, AI agents)
- How do we balance stability with adaptability?
- What is the change proposal and validation process?

**Deliverable:** Governance framework document

### 3.3 Context Modeling

**Questions:**
- How do we represent a persona's "context" as a position in the graph?
- What dimensions define context? (Role, goals, stage, constraints, history)
- How does context change over time?
- How do we handle multiple simultaneous contexts?

**Deliverable:** Context model specification

### 3.4 Technical Stack

**Questions:**
- Graph database vs. file-based storage?
- Vector embeddings for semantic search?
- Query language (Cypher, SPARQL, custom)?
- Visualization tools for graph exploration?
- Integration with existing Jekyll site?

**Deliverable:** Technology recommendation with trade-off analysis

### 3.5 Implementation Roadmap

**Questions:**
- What is the Minimum Viable Graph (MVG)?
- How do we migrate from current system?
- What are the phases and milestones?
- How do we maintain backward compatibility?

**Deliverable:** Phased implementation plan

## 4. Research Sources

### Academic & Industry

- Living Ontology concepts (Jinchun Chen)
- Context Graph vs Knowledge Graph (Atlan)
- GraphRAG design patterns (Gradient Flow)
- PersonaRAG for user-centric retrieval (arXiv)
- Rhizomatic structures (Deleuze & Guattari)

### Existing Systems to Study

- Roam Research / Obsidian (bidirectional linking)
- Wikipedia categories (polyhierarchy)
- Wikidata (structured knowledge graph)
- Neo4j / Kuzu (graph databases)
- Pinecone / Weaviate (vector databases)

### Internal Sources

- Current pattern relationships (graph.json)
- Pattern classification schema (PATTERN_SPEC.md)
- Existing ADRs (001-012)

## 5. Success Criteria

The research phase is complete when we can confidently answer:

1. ✅ What is the schema? (Documented and validated)
2. ✅ How does it evolve? (Governance model defined)
3. ✅ How do we model context? (Specification complete)
4. ✅ What technology do we use? (Decision made with rationale)
5. ✅ What is the roadmap? (Phases defined with milestones)

## 6. Timeline

| Phase | Duration | Focus |
|-------|----------|-------|
| Research | 2-4 weeks | Answer key questions, produce deliverables |
| Design | 2-3 weeks | Detailed specifications, prototypes |
| MVG Build | 4-6 weeks | Minimum Viable Graph implementation |
| Iteration | Ongoing | Continuous improvement based on usage |

## 7. Next Steps

1. Conduct deep research on each area
2. Document findings in `/docs/research/`
3. Propose schema in `/spec/schema/`
4. Create ADRs for key decisions
5. Build MVG prototype
