# Governance Research Notes

**Date**: 2026-02-02  
**Sources**: Javed et al. 2013, Collaborative Ontology Evolution research

---

## 1. Four-Phase Ontology Change Management (Javed et al.)

The most comprehensive framework for ontology evolution governance comes from Javed, Abgaz, and Pahl's 2013 paper, which proposes a four-phase system covering the full lifecycle of ontology changes.

### Phase 1: Change Operationalization

This phase defines the building blocks of ontology evolution through layered change operators. The framework recognizes that changes occur at different levels of granularity and domain-specificity.

| Layer | Type | Description | Examples |
|-------|------|-------------|----------|
| Layer 1 | Atomic | Generic, low-level operations | Add node, Delete edge, Rename property |
| Layer 2 | Composite | Generic higher-level operations | Merge nodes, Split concept, Move subtree |
| Layer 3 | Domain-Specific | Patterns specific to a domain | Add pattern relationship, Create entity hierarchy |

The key insight is that atomic changes alone cannot capture the **semantic intent** behind modifications. Higher-level change patterns describe more meaningful semantics.

### Phase 2: Change Representation

Changes must be explicitly represented in a way that captures both the operation and its context. The paper proposes **layered change logs** using a graph-based approach.

| Component | Purpose |
|-----------|---------|
| Change Log | Sequential record of all changes |
| Graph Representation | Enables pattern recognition and querying |
| Provenance Metadata | Who made the change, when, why |

### Phase 3: Change Semantic Capturing

This phase identifies **composite change patterns** that cannot be captured by simple queries on atomic change logs. The goal is to understand the **intent** behind changes, not just the mechanics.

For example, a series of atomic changes (add node, add edge, add property, add edge) might represent a single semantic operation: "Create new pattern with relationship to existing concept."

### Phase 4: Change Pattern Discovery

The discovery of domain-specific change patterns enables:
- Reusable change patterns that can be implemented in knowledge management systems
- Pattern-driven ontology evolution
- Learning from historical changes to predict future needs

---

## 2. Governance Principles for Living Ontologies

Based on the research, effective governance for an evolving knowledge system requires:

### 2.1 Authority Levels

| Authority | Role | Scope |
|-----------|------|-------|
| **Curators** | Expert human oversight | Schema changes, relationship types |
| **Community** | Collective validation | Pattern content, relationship weights |
| **AI Agents** | Automated suggestions | Gap detection, inconsistency flagging |
| **Usage Signals** | Implicit feedback | Relationship strengthening, relevance |

### 2.2 Change Types and Approval Requirements

| Change Type | Risk Level | Approval Required |
|-------------|------------|-------------------|
| Add new pattern | Low | Single curator |
| Add relationship | Low | Single curator or AI + validation |
| Modify relationship weight | Low | Automated based on usage |
| Add new node type | High | Multiple curators |
| Modify schema | High | ADR + community review |
| Delete pattern | High | Multiple curators + deprecation period |

### 2.3 Evolution Triggers

The research identifies several triggers for ontology evolution:

1. **External triggers**: Changes in the domain being modeled
2. **Internal triggers**: Inconsistencies or gaps discovered within the ontology
3. **Usage triggers**: Patterns of use that suggest missing or incorrect relationships
4. **Persistent explanatory failure**: When the system consistently fails to answer user queries

---

## 3. Collaborative Ontology Evolution

From research on DBpedia, Schema.org, PROV-O, and FOAF evolution:

### Key Findings

These major ontologies evolved through different governance models:

| Ontology | Governance Model | Evolution Pattern |
|----------|-----------------|-------------------|
| DBpedia | Community-driven | Rapid, sometimes inconsistent |
| Schema.org | Corporate-led (Google, etc.) | Controlled, backward-compatible |
| PROV-O | Standards body (W3C) | Slow, highly deliberate |
| FOAF | Single maintainer | Sporadic, personality-dependent |

### Lessons for Context Engine

1. **Hybrid governance** works best: Combine expert curation with community input
2. **Backward compatibility** is crucial: Never break existing queries
3. **Versioning** enables evolution without disruption
4. **Documentation** of changes is essential for trust

---

## 4. Implications for Context Engine Governance

### Proposed Governance Framework

**Tier 1: Schema Governance** (High ceremony)
- Changes to node types, edge types, core properties
- Requires ADR, community review, deprecation period
- Managed through GitHub PRs with approval workflow

**Tier 2: Content Governance** (Medium ceremony)
- New patterns, new entities, new relationships
- Single curator approval or AI suggestion + validation
- Quality checks automated via GitHub Actions

**Tier 3: Weight/Metadata Governance** (Low ceremony)
- Relationship weights, confidence scores, usage metrics
- Automated based on usage signals
- Human override available

### Change Proposal Process

```
1. Proposal → 2. Validation → 3. Review → 4. Implementation → 5. Propagation
     ↑              ↑             ↑              ↑                 ↑
   Human/AI      Automated     Human/AI      Automated         Automated
```

### Persistent Explanatory Failure Detection

The Context Engine should track:
- Queries that return no results
- User feedback on relevance
- Patterns that are frequently accessed together but not linked
- Entities that adopt similar patterns but aren't connected

When failures persist above a threshold, the system should:
1. Flag for human review
2. Suggest potential schema/relationship changes
3. Create a change proposal for curator review

---

## 5. Open Questions

1. How do we balance stability with adaptability?
2. What metrics indicate "persistent explanatory failure"?
3. How do we handle conflicting perspectives on relationships?
4. What is the right deprecation period for schema changes?
5. How do we incentivize community participation in governance?
