# Context Engine Schema Specification

**Version**: 1.0  
**Date**: 2026-02-02  
**Author**: higgerix  
**Status**: Draft

---

## 1. Overview

This document provides a formal specification of the Context Engine's data schema. It defines all node types, properties, and relationship types that constitute the living semantic graph.

### 1.1. Design Principles

1.  **Explicit over Implicit**: All relationships should be explicitly stated, not inferred at query time, to ensure predictability and auditability.
2.  **Provenance Tracking**: Every fact and relationship must have provenance metadata (who created it, when, and why).
3.  **Fractal Abstraction**: The `CommonsEntity` abstraction applies uniformly across all scales (individual, team, organization, city, ecosystem).
4.  **Bidirectional Awareness**: Relationships are stored directionally but can be queried in both directions.
5.  **Evolution-Ready**: The schema includes versioning and temporal metadata to support the living ontology model.

---

## 2. Node Types

### 2.1. Pattern

A **Pattern** is a reusable solution to a recurring problem in a given context. It is the core knowledge unit of the Commons OS.

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | `TypeID` | Yes | Unique identifier (UUID7-based). Example: `pat_01HQXYZ...` |
| `slug` | `String` | Yes | URL-friendly identifier. Example: `lean-startup-ries` |
| `title` | `String` | Yes | Human-readable name. Example: `Lean Startup (Ries)` |
| `summary` | `String` | Yes | One-sentence description of the pattern. |
| `content` | `Markdown` | Yes | Full pattern content (problem, solution, context, etc.). |
| `domains` | `String[]` | Yes | Classification domains. Example: `["business", "startup"]` |
| `categories` | `String[]` | No | Sub-classification categories. Example: `["validation"]` |
| `confidence` | `Float` | No | Confidence score (0.0 to 1.0). Default: `0.8`. |
| `source_url` | `URL` | No | Original source of the pattern. |
| `created_at` | `Timestamp` | Yes | When the pattern was created. |
| `updated_at` | `Timestamp` | Yes | When the pattern was last modified. |
| `created_by` | `String` | Yes | Author or contributor. |

**Cypher Definition:**
```cypher
CREATE NODE TABLE Pattern (
  id STRING PRIMARY KEY,
  slug STRING,
  title STRING,
  summary STRING,
  content STRING,
  domains STRING[],
  categories STRING[],
  confidence FLOAT DEFAULT 0.8,
  source_url STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  created_by STRING
);
```

---

### 2.2. CommonsEntity

A **CommonsEntity** is any value-creating system that can adopt patterns. It is the unified abstraction for individuals, teams, organizations, cities, and ecosystems.

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | `TypeID` | Yes | Unique identifier. Example: `ent_01HQABC...` |
| `name` | `String` | Yes | Human-readable name. Example: `Buurtzorg` |
| `type` | `Enum` | Yes | Entity type. See `EntityType` enum below. |
| `scale` | `Enum` | Yes | Entity scale. See `EntityScale` enum below. |
| `description` | `String` | No | Brief description of the entity. |
| `context` | `JSON` | No | Structured context data (industry, location, etc.). |
| `created_at` | `Timestamp` | Yes | When the entity was added to the graph. |
| `updated_at` | `Timestamp` | Yes | When the entity was last modified. |

**EntityType Enum:**
-   `individual`: A single person.
-   `team`: A small group working together.
-   `organization`: A formal organization (company, cooperative, NGO).
-   `network`: A federation or consortium of organizations.
-   `city`: A municipal or urban entity.
-   `region`: A geographic region or bioregion.
-   `ecosystem`: An ecological or industrial ecosystem.

**EntityScale Enum:**
-   `micro`: 1-10 people.
-   `small`: 11-50 people.
-   `medium`: 51-250 people.
-   `large`: 251-1000 people.
-   `enterprise`: 1001+ people.
-   `city`: City-scale population.
-   `regional`: Regional-scale population.
-   `global`: Global-scale impact.

**Cypher Definition:**
```cypher
CREATE NODE TABLE CommonsEntity (
  id STRING PRIMARY KEY,
  name STRING,
  type STRING,
  scale STRING,
  description STRING,
  context STRING,  -- JSON stored as string
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

---

### 2.3. Concept

A **Concept** is an abstract idea or topic that patterns can be associated with. It enables thematic grouping and discovery.

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | `TypeID` | Yes | Unique identifier. Example: `con_01HQDEF...` |
| `name` | `String` | Yes | Human-readable name. Example: `Product-Market Fit` |
| `definition` | `String` | No | Definition of the concept. |
| `aliases` | `String[]` | No | Alternative names or synonyms. |
| `created_at` | `Timestamp` | Yes | When the concept was created. |

**Cypher Definition:**
```cypher
CREATE NODE TABLE Concept (
  id STRING PRIMARY KEY,
  name STRING,
  definition STRING,
  aliases STRING[],
  created_at TIMESTAMP
);
```

---

### 2.4. Source

A **Source** is a reference to an external document, book, or website that provides evidence for a pattern or relationship.

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | `TypeID` | Yes | Unique identifier. Example: `src_01HQGHI...` |
| `title` | `String` | Yes | Title of the source. |
| `url` | `URL` | No | URL of the source. |
| `author` | `String` | No | Author of the source. |
| `publication_date` | `Date` | No | Date of publication. |
| `type` | `Enum` | Yes | Source type: `book`, `article`, `website`, `paper`, `video`. |

**Cypher Definition:**
```cypher
CREATE NODE TABLE Source (
  id STRING PRIMARY KEY,
  title STRING,
  url STRING,
  author STRING,
  publication_date DATE,
  type STRING
);
```

---

## 3. Relationship Types

### 3.1. Pattern-to-Pattern Relationships

These relationships define how patterns interact with each other.

#### 3.1.1. ENABLES

Pattern A **enables** Pattern B if adopting A makes it easier or possible to adopt B.

| Property | Type | Required | Description |
|---|---|---|---|
| `strength` | `Float` | Yes | Strength of the enabling relationship (0.0 to 1.0). |
| `evidence` | `String` | No | Textual evidence or reasoning. |
| `source_id` | `TypeID` | No | Reference to a `Source` node. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |
| `created_by` | `String` | Yes | Who created the relationship. |

**Cypher Definition:**
```cypher
CREATE REL TABLE ENABLES (
  FROM Pattern TO Pattern,
  strength FLOAT,
  evidence STRING,
  source_id STRING,
  created_at TIMESTAMP,
  created_by STRING
);
```

#### 3.1.2. REQUIRES

Pattern A **requires** Pattern B if B is a prerequisite for A.

| Property | Type | Required | Description |
|---|---|---|---|
| `strength` | `Float` | Yes | Strength of the requirement (0.0 to 1.0). |
| `evidence` | `String` | No | Textual evidence or reasoning. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |
| `created_by` | `String` | Yes | Who created the relationship. |

**Cypher Definition:**
```cypher
CREATE REL TABLE REQUIRES (
  FROM Pattern TO Pattern,
  strength FLOAT,
  evidence STRING,
  created_at TIMESTAMP,
  created_by STRING
);
```

#### 3.1.3. TENSIONS_WITH

Pattern A **tensions with** Pattern B if adopting both creates a trade-off or conflict.

| Property | Type | Required | Description |
|---|---|---|---|
| `description` | `String` | Yes | Description of the tension. |
| `resolution_hint` | `String` | No | How to resolve or manage the tension. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |
| `created_by` | `String` | Yes | Who created the relationship. |

**Cypher Definition:**
```cypher
CREATE REL TABLE TENSIONS_WITH (
  FROM Pattern TO Pattern,
  description STRING,
  resolution_hint STRING,
  created_at TIMESTAMP,
  created_by STRING
);
```

#### 3.1.4. RELATED_TO

Pattern A is **related to** Pattern B in a general sense (e.g., same topic, same author).

| Property | Type | Required | Description |
|---|---|---|---|
| `relation_type` | `String` | No | Type of relation: `same_topic`, `same_author`, `similar`, `complementary`. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |

**Cypher Definition:**
```cypher
CREATE REL TABLE RELATED_TO (
  FROM Pattern TO Pattern,
  relation_type STRING,
  created_at TIMESTAMP
);
```

---

### 3.2. Pattern-to-Entity Relationships

#### 3.2.1. ADOPTED_BY

Pattern is **adopted by** a CommonsEntity.

| Property | Type | Required | Description |
|---|---|---|---|
| `since` | `Date` | No | When the entity started using the pattern. |
| `success_level` | `Enum` | No | `high`, `medium`, `low`, `unknown`. |
| `evidence` | `String` | No | Evidence of adoption (case study, interview, etc.). |
| `source_id` | `TypeID` | No | Reference to a `Source` node. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |

**Cypher Definition:**
```cypher
CREATE REL TABLE ADOPTED_BY (
  FROM Pattern TO CommonsEntity,
  since DATE,
  success_level STRING,
  evidence STRING,
  source_id STRING,
  created_at TIMESTAMP
);
```

---

### 3.3. Pattern-to-Concept Relationships

#### 3.3.1. BELONGS_TO

Pattern **belongs to** a Concept.

| Property | Type | Required | Description |
|---|---|---|---|
| `relevance` | `Float` | No | Relevance score (0.0 to 1.0). |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |

**Cypher Definition:**
```cypher
CREATE REL TABLE BELONGS_TO (
  FROM Pattern TO Concept,
  relevance FLOAT,
  created_at TIMESTAMP
);
```

---

### 3.4. Entity-to-Entity Relationships

#### 3.4.1. INSPIRED_BY

CommonsEntity A was **inspired by** CommonsEntity B.

| Property | Type | Required | Description |
|---|---|---|---|
| `description` | `String` | No | Description of the inspiration. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |

**Cypher Definition:**
```cypher
CREATE REL TABLE INSPIRED_BY (
  FROM CommonsEntity TO CommonsEntity,
  description STRING,
  created_at TIMESTAMP
);
```

#### 3.4.2. PART_OF

CommonsEntity A is **part of** CommonsEntity B (e.g., a team is part of an organization).

| Property | Type | Required | Description |
|---|---|---|---|
| `role` | `String` | No | Role of A within B. |
| `since` | `Date` | No | When A became part of B. |
| `created_at` | `Timestamp` | Yes | When the relationship was created. |

**Cypher Definition:**
```cypher
CREATE REL TABLE PART_OF (
  FROM CommonsEntity TO CommonsEntity,
  role STRING,
  since DATE,
  created_at TIMESTAMP
);
```

---

## 4. Schema Diagram

```
                    ┌─────────────┐
                    │   Source    │
                    └──────┬──────┘
                           │ (evidence)
                           ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Concept   │◄────│   Pattern   │────►│CommonsEntity│
└─────────────┘     └─────────────┘     └─────────────┘
   BELONGS_TO            │  │               ADOPTED_BY
                         │  │               INSPIRED_BY
                    ENABLES │ REQUIRES      PART_OF
                  TENSIONS_WITH
                    RELATED_TO
                         │  │
                         ▼  ▼
                    ┌─────────────┐
                    │   Pattern   │
                    └─────────────┘
```

---

## 5. Versioning and Evolution

### 5.1. Schema Versioning

The schema itself is versioned using semantic versioning (MAJOR.MINOR.PATCH).

-   **MAJOR**: Breaking changes to node or relationship structure.
-   **MINOR**: New node types, relationship types, or properties.
-   **PATCH**: Bug fixes or documentation updates.

### 5.2. Data Versioning

All nodes and relationships include `created_at` and (where applicable) `updated_at` timestamps. This enables:

-   **Temporal Queries**: "What did the graph look like on date X?"
-   **Audit Trails**: "Who added this relationship and when?"
-   **Evolution Tracking**: "How has this pattern's relationships changed over time?"

---

## 6. Validation Rules

### 6.1. Node Validation

| Rule | Description |
|---|---|
| `id` must be unique | No two nodes of the same type can have the same `id`. |
| `slug` must be unique (Pattern) | No two patterns can have the same `slug`. |
| `domains` must not be empty (Pattern) | Every pattern must have at least one domain. |
| `type` must be valid (CommonsEntity) | Must be one of the defined `EntityType` values. |

### 6.2. Relationship Validation

| Rule | Description |
|---|---|
| No self-loops | A pattern cannot `ENABLE`, `REQUIRE`, or `TENSION_WITH` itself. |
| `strength` must be in range | Must be between 0.0 and 1.0. |
| `created_by` must not be empty | All relationships must have an author. |

---

## 7. Future Extensions

This schema is designed to be extensible. Planned future additions include:

1.  **`Question` Node**: Questions that patterns answer (e.g., "How do I validate my idea?").
2.  **`Journey` Node**: A sequence of patterns representing a user's path.
3.  **`ANSWERS` Relationship**: Connects patterns to questions.
4.  **`FOLLOWS` Relationship**: Connects patterns in a journey sequence.
5.  **Vector Embeddings**: Adding an `embedding` property to `Pattern` for semantic search.

---

## Appendix A: Full Cypher Schema

```cypher
-- Node Tables
CREATE NODE TABLE Pattern (
  id STRING PRIMARY KEY,
  slug STRING,
  title STRING,
  summary STRING,
  content STRING,
  domains STRING[],
  categories STRING[],
  confidence FLOAT DEFAULT 0.8,
  source_url STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  created_by STRING
);

CREATE NODE TABLE CommonsEntity (
  id STRING PRIMARY KEY,
  name STRING,
  type STRING,
  scale STRING,
  description STRING,
  context STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE NODE TABLE Concept (
  id STRING PRIMARY KEY,
  name STRING,
  definition STRING,
  aliases STRING[],
  created_at TIMESTAMP
);

CREATE NODE TABLE Source (
  id STRING PRIMARY KEY,
  title STRING,
  url STRING,
  author STRING,
  publication_date DATE,
  type STRING
);

-- Relationship Tables
CREATE REL TABLE ENABLES (
  FROM Pattern TO Pattern,
  strength FLOAT,
  evidence STRING,
  source_id STRING,
  created_at TIMESTAMP,
  created_by STRING
);

CREATE REL TABLE REQUIRES (
  FROM Pattern TO Pattern,
  strength FLOAT,
  evidence STRING,
  created_at TIMESTAMP,
  created_by STRING
);

CREATE REL TABLE TENSIONS_WITH (
  FROM Pattern TO Pattern,
  description STRING,
  resolution_hint STRING,
  created_at TIMESTAMP,
  created_by STRING
);

CREATE REL TABLE RELATED_TO (
  FROM Pattern TO Pattern,
  relation_type STRING,
  created_at TIMESTAMP
);

CREATE REL TABLE ADOPTED_BY (
  FROM Pattern TO CommonsEntity,
  since DATE,
  success_level STRING,
  evidence STRING,
  source_id STRING,
  created_at TIMESTAMP
);

CREATE REL TABLE BELONGS_TO (
  FROM Pattern TO Concept,
  relevance FLOAT,
  created_at TIMESTAMP
);

CREATE REL TABLE INSPIRED_BY (
  FROM CommonsEntity TO CommonsEntity,
  description STRING,
  created_at TIMESTAMP
);

CREATE REL TABLE PART_OF (
  FROM CommonsEntity TO CommonsEntity,
  role STRING,
  since DATE,
  created_at TIMESTAMP
);
```
