# Context Engine

**A Living Semantic Graph for Commons OS**

The Context Engine is the knowledge infrastructure that powers pattern discovery, relationship mapping, and context-aware retrieval across the Commons OS ecosystem.

## Vision

Transform the pattern library from a static collection of documents into a dynamic, interconnected knowledge system that understands **context** and **perspective**.

> "Context IS the network of relationships. Putting something in perspective means understanding its position within a web of connections."

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Living Ontology** | The graph evolves based on persistent explanatory failures, not just manual updates |
| **Context Graph** | Extends knowledge graphs with operational metadata: lineage, decisions, temporal context |
| **Persona-Driven** | User context influences retrieval; different personas see different perspectives |
| **Rhizomatic Structure** | Non-hierarchical network where any point can connect to any other |

## Status

🔬 **Research Phase** - We are currently conducting deep research to define the schema, governance model, and implementation roadmap.

See [ADR-013](https://github.com/Commons-OS/patterns/blob/main/docs/adr/013-context-engine-living-semantic-graph.md) in the patterns repository for the full decision record.

## Repository Structure

```
context-engine/
├── README.md           # This file
├── docs/
│   ├── adr/            # Architecture Decision Records
│   └── research/       # Research findings and analysis
├── spec/               # Formal specifications
│   ├── schema/         # Node and edge type definitions
│   └── api/            # Query API specifications
└── src/                # Implementation (future)
```

## Research Questions

The current research phase aims to answer:

1. **Schema Definition**: What are the node types, edge types, and their properties?
2. **Evolution Governance**: How does the graph evolve? Who has authority?
3. **Context Modeling**: How do we represent user context as a graph position?
4. **Technical Stack**: What technologies best support this vision?
5. **Implementation Roadmap**: What is the path from current state to Context Engine?

## Related Repositories

- [patterns](https://github.com/Commons-OS/patterns) - The pattern library (primary data source)
- [lighthouses](https://github.com/Commons-OS/lighthouses) - Organization case studies
- [personas](https://github.com/Commons-OS/personas) - Human and digital persona definitions

## Contributing

This is an active research project. We welcome contributions in the form of:

- Research findings and references
- Schema proposals
- Technical architecture suggestions
- Use case scenarios

## License

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
