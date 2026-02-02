# Context Modeling Research Notes

**Date**: 2026-02-02  
**Sources**: PersonaRAG (Zerhoudi & Granitzer 2024), Context-Aware Retrieval research

---

## 1. PersonaRAG: User-Centric Retrieval

PersonaRAG represents the state-of-the-art in user-centric retrieval systems, achieving over 5% improvement in accuracy by incorporating user context into the retrieval process. The key insight is that retrieval must adapt to the user's specific informational and contextual needs, not just the query text.

### Core Architecture

PersonaRAG introduces a three-step pipeline that transforms static retrieval into dynamic, context-aware retrieval:

| Step | Function | Description |
|------|----------|-------------|
| **Retrieval** | Initial document retrieval | Standard RAG retrieval based on query |
| **User Interaction Analysis** | Understand user behavior | Analyze engagement, preferences, context, feedback |
| **Cognitive Dynamic Adaptation** | Refine results | Adjust responses based on user profile |

### The Five Agents

PersonaRAG uses a multi-agent architecture where specialized agents handle different aspects of personalization:

| Agent | Role | Context Engine Application |
|-------|------|---------------------------|
| **User Profile Agent** | Maintains user preferences and history | Commons Entity profile (scale, type, goals) |
| **Context Retrieval Agent** | Initial retrieval based on query | Pattern search with domain filtering |
| **Session Analysis Agent** | Tracks current session behavior | Navigation path through patterns |
| **Document Ranking Agent** | Re-ranks results based on user context | Weight patterns by entity relevance |
| **Feedback Agent** | Incorporates explicit/implicit feedback | Learn from pattern adoption signals |

### Key Concepts

**Cognitive Dynamic Adaptation**: The system mimics human learning behaviors by treating retrieval as a cognitive structure that receives, interprets, and acts upon user feedback. This is directly applicable to the Context Engine's "living ontology" concept.

**Transparent Personalization**: Users are aware of how their information is used to tailor results. This aligns with Commons OS values of transparency and user agency.

---

## 2. Context Dimensions for Commons Entities

Based on the research, we can define the key dimensions that constitute "context" for a Commons Entity:

### 2.1 Static Context (Slow-changing)

These properties define the entity's fundamental nature and change infrequently:

| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Scale** | Fractal level of the entity | Individual, team, organization, city, ecosystem |
| **Type** | Specific entity classification | Startup, cooperative, municipality, watershed |
| **Domain Interests** | Primary domains of concern | Business, startup, security, ecology |
| **Values** | Core principles and priorities | Sustainability, profit, community, innovation |

### 2.2 Dynamic Context (Fast-changing)

These properties reflect the entity's current situation and change frequently:

| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Stage** | Current lifecycle phase | Idea, validation, growth, maturity, transition |
| **Goals** | Active objectives | Raise funding, hire team, expand market |
| **Constraints** | Current limitations | Budget, time, expertise, regulatory |
| **Recent Activity** | Navigation and adoption history | Patterns viewed, adopted, bookmarked |

### 2.3 Relational Context

These properties define the entity's position in the graph:

| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Similar Entities** | Entities with similar profiles | Other startups at same stage |
| **Aspirational Entities** | Entities the user wants to emulate | Successful lighthouses |
| **Network** | Connected entities | Partners, investors, community |
| **Pattern Adoption** | Patterns already adopted | Current governance, funding models |

---

## 3. Context as Graph Position

The research confirms our ADR-013 hypothesis: context can be represented as a position within the graph. This position is defined by:

1. **Activated Nodes**: Which patterns, concepts, and entities are relevant to this user
2. **Weighted Edges**: How strongly each relationship matters from this perspective
3. **Traversal History**: The path the user has taken through the graph
4. **Proximity**: Distance from the user's position to other nodes

### Query Transformation

When a user queries the system, their context transforms the query:

```
Raw Query: "governance patterns"

Context-Aware Query:
- User is a startup (scale: organization, type: startup)
- User is in growth stage (stage: growth)
- User has adopted Sociocracy (pattern_adoption: sociocracy)
- User is interested in cooperatives (aspirational: cooperative)

Transformed Query: "governance patterns for growth-stage startups 
                   compatible with Sociocracy, used by cooperatives"
```

---

## 4. Implementing Context in the Context Engine

### 4.1 Context Profile Schema

Each Commons Entity should have a context profile stored as part of their node properties:

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

1. **Parse Query**: Extract intent and keywords
2. **Load Context**: Retrieve user's context profile
3. **Expand Query**: Add context-relevant terms and filters
4. **Retrieve**: Get initial results from graph + vector search
5. **Re-rank**: Adjust ranking based on context weights
6. **Present**: Show results with context-relevant explanations

### 4.3 Context Evolution

Context is not static—it evolves based on:

| Signal | What It Indicates | How to Update |
|--------|-------------------|---------------|
| Pattern adoption | User found pattern valuable | Add to adopted_patterns |
| Navigation patterns | User's interests | Update domain weights |
| Explicit feedback | User's preferences | Adjust context directly |
| Time | Stage progression | Prompt for stage update |
| Lighthouse similarity | Aspirational alignment | Update aspires_to |

---

## 5. Implications for Context Engine

### 5.1 Required Components

Based on this research, the Context Engine needs:

1. **Entity Profile Store**: Persistent storage of context profiles
2. **Context Inference Engine**: Derive context from behavior when not explicit
3. **Query Expansion Module**: Transform queries based on context
4. **Re-ranking Module**: Adjust results based on context weights
5. **Feedback Loop**: Update context based on user signals

### 5.2 Privacy Considerations

PersonaRAG emphasizes transparent personalization. The Context Engine should:

- Allow users to view their context profile
- Enable users to edit/correct their profile
- Provide opt-out for personalization
- Explain why results were ranked as they were

### 5.3 Cold Start Problem

New entities have no context history. Solutions:

1. **Explicit Onboarding**: Ask users to define their context
2. **Similar Entity Inference**: Use similar entities' contexts as starting point
3. **Default Profiles**: Pre-defined profiles for common entity types
4. **Gradual Learning**: Start generic, refine with interaction

---

## 6. Open Questions

1. How much context is too much? (Privacy vs. relevance trade-off)
2. How do we handle conflicting contexts? (User vs. organization)
3. How do we represent temporal context? (Past vs. present vs. future goals)
4. How do we balance personalization with serendipity? (Filter bubbles)
5. How do we handle multi-stakeholder queries? (Team with diverse contexts)
