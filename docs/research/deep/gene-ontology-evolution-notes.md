# Gene Ontology Evolution - Deep Research Notes

**Date**: 2026-02-02  
**Source**: PMC3166943 - "How the Gene Ontology Evolves" (Leonelli et al., 2011)

---

## 1. Background

The Gene Ontology (GO) was created in 1999 and is one of the longest-running bio-ontologies. This paper examines how GO has evolved to represent biological knowledge over time.

### Key Definition: Ontology Shifts

> "Ontology shifts are defined as changes to the biological content of GO, including changes in the definitions of GO terms, the order in which GO terms are situated in the network hierarchy, the relations used to link these terms and the links made between terms and data and/or meta-data."

---

## 2. Five Types of Ontology Shifts

The paper identifies five circumstances that warrant changes:

### Type 1: Dealing with Anomalies

**Trigger**: Mismatch between GO representation and reality discovered.

**Example**: "Serotonin secretion" was initially placed as a subtype of both "hormone secretion" AND "neurotransmitter secretion". When "serotonin secretion during acute inflammatory response" was added, curators realized this was incorrect - in inflammatory responses, serotonin acts on non-neuronal cells.

**Resolution**: Restructured the hierarchy to separate the different roles of serotonin.

**Key Insight**: Anomalies often emerge when new terms are added that expose hidden assumptions in existing structure.

---

### Type 2: Expanding Scope

**Trigger**: GO needs to cover new research fields, biological issues, or species.

**Three sub-types**:

| Sub-type | Example |
|----------|---------|
| New field | Adding immunological terms |
| New biological issue | Plant-microbe interactions |
| New species | Pathogen-specific processes |

**Example**: The PAMGO (Plant-Associated Microbe Gene Ontology) project extended GO to cover host-pathogen interactions. This required:
- New terms for pathogen-specific processes
- New relations (e.g., "participates_in")
- Careful integration with existing terms

**Key Insight**: Scope expansion often reveals that existing terms were implicitly scoped to certain organisms or contexts.

---

### Type 3: Divergent Terminology Across Communities

**Trigger**: Different user communities use the same term differently.

**Example**: "Immune response" vs "defense response"
- Initially treated as synonymous
- But regulatory immune responses (e.g., tolerance to food antigens) are NOT defense responses
- Required splitting into separate terms with common ancestor

**Key Insight**: Biological terminology is often context-dependent. What seems like a synonym may have important distinctions in different research communities.

---

### Type 4: New Discoveries Changing Meaning

**Trigger**: Scientific discoveries change understanding of biological entities or processes.

**Example**: Discovery of new molecular mechanisms that change how a process should be classified.

**Key Insight**: The ontology must evolve as scientific knowledge evolves. This is not a bug - it's the core purpose.

---

### Type 5: Extending Relations

**Trigger**: Need for new types of relationships between terms.

**Example**: Adding "regulates" and "part_of" relations in addition to "is_a".

**Key Insight**: The expressiveness of the ontology depends on having appropriate relation types. Too few relations = loss of important distinctions.

---

## 3. Governance and Curation Process

### Curator Expertise

> "It is important that trained curators with technical expertise in the scientific field(s) in question are involved in supervising ontology shifts and identifying inaccuracies."

Curators need:
- Domain expertise (biology)
- Ontology engineering skills
- Understanding of how scientific knowledge is produced

### Feedback Mechanisms

GO established mechanisms for users to report:
- Discrepancies between GO and their field's understanding
- Missing terms or relations
- Incorrect classifications

### Community Meetings

Major shifts are discussed at GO consortium meetings (e.g., the TIGR meeting in November 2005 that resolved the immune/defense response issue).

---

## 4. Key Principles for Ontology Evolution

### 1. Faithful Representation

> "Ontology curation aims to produce a faithful representation of knowledge domains as they keep developing."

The ontology should reflect current scientific understanding, not historical assumptions.

### 2. Translation of General Guidelines

> "This requires the translation of general guidelines into specific representations of reality."

Abstract ontology principles must be instantiated in domain-specific ways.

### 3. Understanding Knowledge Production

> "An understanding of how scientific knowledge is produced and constantly updated."

Curators must understand that scientific knowledge is provisional and evolving.

---

## 5. Implications for Context Engine

### What to Adopt

1. **Five-type framework**: Use similar categories for tracking why changes occur
2. **Anomaly detection**: Build mechanisms to surface inconsistencies
3. **Community feedback**: Enable users to report discrepancies
4. **Expert curation**: Involve domain experts in reviewing changes
5. **Scope awareness**: Track what domains/contexts each pattern applies to

### Governance Model Inspiration

| GO Practice | Context Engine Adaptation |
|-------------|---------------------------|
| Consortium meetings | Steering group reviews |
| User feedback channels | GitHub issues, community forum |
| Curator expertise | Domain-specific reviewers |
| Anomaly resolution | Automated consistency checks + human review |

### Evolution Tracking

GO tracks WHY changes were made, not just WHAT changed. This is crucial for:
- Understanding the history of the ontology
- Learning from past decisions
- Communicating changes to users

---

## 6. Key Quotes

> "Maintaining a bio-ontology in the long term requires improving and updating its contents so that it adequately captures what is known about biological phenomena."

> "The capability of bio-ontologies such as GO to reflect new developments as they arise has been highlighted as key to their increasing popularity."

> "GO was created in 1999 and is thus one of the longest-running ontologies within the Open Biomedical Ontologies (OBO)."

---

## 7. Open Questions

1. How do we detect anomalies automatically vs relying on human discovery?
2. How do we handle scope expansion without breaking existing relationships?
3. How do we resolve terminology conflicts between different user communities?
4. How do we version the ontology to track evolution over time?
5. What's the right balance between stability and evolution?
