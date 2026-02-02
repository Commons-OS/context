# Context Engine

**A Living Semantic Graph for Commons OS**

The Context Engine is the intelligence layer that powers pattern discovery, relationship mapping, and context-aware retrieval across the Commons OS ecosystem. It is powered by the **Commons Language Model (CLM)**, a domain-specific AI fine-tuned on the collective knowledge of the commons.

## The Nested Identity

The Context Engine exists within a nested conceptual hierarchy. Understanding this relationship is foundational to the architecture.

| Layer | What It Is | Role |
|-------|------------|------|
| **Commons OS** | The entire ecosystem | Patterns, lighthouses, tools, community, philosophy |
| **Context Engine** | The intelligence layer | Graph, RAG, APIs, retrieval |
| **CLM** | The AI model | The "brain" that reasons and synthesizes |

> These are not separate entities but **nested expressions of the same intelligence** at different levels of abstraction. See [010-conceptual-hierarchy.md](docs/010-conceptual-hierarchy.md) for the full explanation.

## Vision

Transform the pattern library from a static collection of documents into a dynamic, interconnected knowledge system that understands **context** and **perspective**.

> "Context IS the network of relationships. Putting something in perspective means understanding its position within a web of connections."

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Living Ontology** | The graph evolves based on persistent explanatory failures, not just manual updates |
| **Context Graph** | Extends knowledge graphs with operational metadata: lineage, decisions, temporal context |
| **Persona-Driven** | User context influences retrieval; different personas see different perspectives |
| **Fractal Sovereignty** | Local-first design; users can run the full stack on their own hardware |

## Status

🔬 **Research & Specification Phase** - We have completed deep research and are now defining the technical specifications for the Commons Language Model.

## Key Documents

| Document | Description |
|----------|-------------|
| [004-commons-os-philosophy.md](docs/004-commons-os-philosophy.md) | The Third Path manifesto |
| [005-context-engine-specification-v2.md](docs/005-context-engine-specification-v2.md) | Context Engine architecture |
| [006-clm-technical-specification-v2.md](docs/006-clm-technical-specification-v2.md) | CLM model and hardware requirements |
| [009-clm-service-model-architecture.md](docs/009-clm-service-model-architecture.md) | Hybrid Federated inference model |
| [010-conceptual-hierarchy.md](docs/010-conceptual-hierarchy.md) | The nested identity of Commons OS, Context Engine, and CLM |

## Repository Structure

```
context-engine/
├── README.md           # This file
├── docs/
│   ├── 00x-*.md        # Core specification documents
│   ├── adr/            # Architecture Decision Records
│   └── research/       # Research findings and analysis
│       ├── deep/       # Deep research notes
│       └── frontier/   # Cutting-edge research (LLMs, reasoning models)
├── spec/               # Formal specifications (future)
└── src/                # Implementation (future)
```

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
