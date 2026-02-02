# Schema Design Research Notes

**Date**: 2026-02-02  
**Source**: Neo4j, Ontology Design Patterns, Academic Research

---

## 1. Key Findings from Neo4j

### Knowledge Graph Components
1. **Nodes** - Data entities (the things)
2. **Relationships** - Connections between nodes (how things relate)
3. **Organizing Principles** - Conceptual framework (categories, hierarchies, ontologies)

### Property Graph vs Triple Store

| Aspect | Property Graph | Triple Store (RDF) |
|--------|---------------|-------------------|
| Structure | Nodes + Relationships + Properties | Subject-Predicate-Object triples |
| Flexibility | Add relationships/nodes anytime without schema change | Reification required for complex relationships |
| Complexity | Intuitive, matches mental models | Explodes into many triples |
| Best for | Highly connected data, evolving schemas | Ontology management, metadata |

**Recommendation**: Property Graph model is better suited for Context Engine due to:
- Native relationship support
- Schema flexibility (living ontology requirement)
- Intuitive modeling of patterns and entities

### Graph Data Modeling Process
1. **Analyze domain** - Define questions the graph needs to answer
2. **Identify nodes** - Main objects (patterns, entities, concepts)
3. **Define labels** - Purpose, role, or type of node
4. **Define relationships** - How entities interact (enables, requires, tensions_with)
5. **Add properties** - Additional detail on nodes and relationships

### Organizing Principles
- **Simple**: Taxonomy (categories, hierarchies)
- **Complex**: Ontology (systematic mapping to semantic network)
- **Recommendation**: Start simple, add ontology complexity only when needed

---

## 2. Ontology Design Patterns (ODPs)

From academic research (Gangemi 2005, cited 745 times):

### Types of ODPs
1. **Content Patterns** - Reusable domain-independent conceptual structures
2. **Structural Patterns** - Architectural patterns for ontology organization
3. **Presentation Patterns** - How to present ontology to users
4. **Correspondence Patterns** - Mapping between ontologies

### Key Content Patterns Relevant to Context Engine

| Pattern | Description | Application |
|---------|-------------|-------------|
| **Part-Whole** | Modeling composition relationships | Commons Entity scale hierarchy |
| **Participation** | Entities participating in events/processes | Pattern adoption by entities |
| **Classification** | Categorizing instances | Multi-domain tagging |
| **Situation** | Context-dependent descriptions | User context modeling |
| **Information Realization** | Abstract concepts realized in concrete forms | Pattern → Implementation |

### Design Principles
- **Minimal ontological commitment** - Don't over-specify
- **Modularity** - Compose from smaller patterns
- **Reusability** - Design for multiple contexts
- **Extensibility** - Allow growth without breaking changes

---

## 3. Schema Design Best Practices

### From Enterprise Knowledge Graph Design

1. **Start with use cases** - What questions must the graph answer?
2. **Model for queries** - Structure should support common traversals
3. **Balance normalization** - Don't over-normalize (graph traversal cost)
4. **Version the schema** - Track changes over time
5. **Document decisions** - ADRs for schema choices

### Node Design Principles
- Use **labels** for categorization (can have multiple)
- Use **properties** for attributes
- Avoid putting relationships in properties (use actual relationships)

### Relationship Design Principles
- **Directional** - Relationships have direction (but can traverse both ways)
- **Typed** - Use specific relationship types (ENABLES vs generic RELATES_TO)
- **Properties on relationships** - Weight, confidence, provenance, temporal validity

---

## 4. Implications for Context Engine Schema

### Proposed Node Types
```
Pattern          - Documented pattern
CommonsEntity    - Fractal value-creating system (individual → ecosystem)
Concept          - Abstract idea or principle
Source           - Reference, book, authority
Domain           - Commons domain (business, startup, city, etc.)
```

### Proposed Relationship Types
```
ENABLES          - Pattern enables another pattern
REQUIRES         - Pattern requires another pattern
TENSIONS_WITH    - Pattern creates tension with another
SPECIALIZES      - Pattern is a specialization of another
GENERALIZES      - Pattern is a generalization of another
ADOPTED_BY       - Pattern adopted by entity
INSPIRED_BY      - Entity inspired by another entity
PART_OF          - Entity is part of larger entity (fractal)
AUTHORED_BY      - Pattern authored by source
BELONGS_TO       - Pattern belongs to domain
```

### Relationship Properties
```
weight           - Strength of relationship (0.0-1.0)
confidence       - Certainty about this relationship
provenance       - Source (human, AI, usage)
valid_from       - When relationship became valid
valid_to         - When relationship expired (null = current)
decision_trace   - History of changes
```

### CommonsEntity Properties
```
scale            - Fractal level (individual, team, org, city, ecosystem)
type             - Specific type (human, startup, cooperative, municipality)
context          - Current situation (idea-stage, growth, transition)
created_at       - When entity was added
updated_at       - Last modification
```

---

## 5. Open Questions

1. **How to model temporal evolution?** - Patterns and relationships change over time
2. **How to handle conflicting perspectives?** - Different users may see different relationships
3. **How to balance schema stability with living ontology?** - Need evolution without chaos
4. **File-based vs database?** - Can we achieve this with JSON/YAML or need Neo4j?

---

## 6. Next Research Areas

- [ ] Governance models for evolving ontologies
- [ ] Context modeling and persona-based retrieval
- [ ] Technical stack evaluation (Neo4j, Kuzu, file-based)
- [ ] Vector embeddings for semantic search


---

## 7. Modular Ontology Modeling (MOMo) - Shimizu, Hammar, Hitzler 2021

### Key Problems Addressed
1. **Differing representational granularity** - Different levels of detail in ontologies
2. **Lack of conceptual clarity** - Potentially reusable ontologies unclear
3. **Lack of adherence to good modeling principles**
4. **Lack of reuse emphasis** in available ontology engineering tooling

### MOMo Methodology
- Builds on eXtreme Design methodology
- Emphasizes **modular development** and **design pattern reuse**
- Uses **graphical schema diagrams** as vehicles for knowledge elicitation
- Provides **CoModIDE** tool support

### Key Concepts

**Representational Granularity**: Modeling choices that determine level of detail
- One model may simply refer to temperatures at specific space-time locations
- Another may record uncertainty intervals
- A third may record measurement instrument information
- Fourth may record calibration data

**Modularization**: Breaking ontology into reusable components
- Each module addresses a specific concern
- Modules can be composed to build larger ontologies
- Reduces complexity and improves maintainability

### Implications for Context Engine
- Use **modular patterns** for different aspects (patterns, entities, relationships)
- Define **clear granularity levels** for different use cases
- Create **reusable modules** that can be composed
- Support **multiple levels of detail** based on context

