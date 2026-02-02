# Schema.org Evolution and Governance - Deep Research Notes

**Date**: 2026-02-02  
**Source**: Schema.org Official Documentation

---

## 1. Organizational Structure

Schema.org is a collaboration between major search engines (Google, Microsoft, Yahoo, Yandex) with community participation through W3C.

### Governance Layers

| Layer | Role | Responsibility |
|-------|------|----------------|
| **Steering Group** | Final approval | Reviews releases, resolves disputes |
| **W3C Community Group** | Discussion forum | Proposes changes, debates design |
| **Project Webmaster** | Operational | Maintains staging, publishes releases |
| **External Contributors** | Proposals | Submit issues, examples, use cases |

### Key Insight: Unanimous Steering Group Approval

> "All changes to the project have been through unanimous agreement of the Steering Group membership, strongly informed by the opinions, contributions and discussions in the wider community."

This is a high bar - it ensures stability but can slow evolution.

---

## 2. Release Process

### Multi-Stage Pipeline

```
Community Discussion (GitHub/W3C)
         ↓
staging.schema.org (work-in-progress)
         ↓
pending.schema.org (new vocabulary proposals)
         ↓
Release Candidate (snapshot of consensus)
         ↓
Steering Group Review (10 business days)
         ↓
schema.org (official release)
```

### Release Types

| Type | Description | Speed |
|------|-------------|-------|
| **Full Release** | Named versions (e.g., "2.1") | Every few weeks |
| **Early Access Fixes** | Bug fixes, typos, examples | Fast-tracked |
| **Pending** | New vocabulary proposals | Immediate to staging |

### Versioning

- Simple URLs recommended: `https://schema.org/Place`
- Dated snapshots available for precision
- `schemaVersion` property for documents to declare intent

---

## 3. Schema Structure

### What Schema.org Defines

| Element | Example | Description |
|---------|---------|-------------|
| **Types** | Event | Categories of things |
| **Properties** | workPerformed | Attributes of types |
| **Enumerated Values** | ReservationCancelled | Fixed value options |

### What Schema.org Does NOT Define

> "Schema.org does not define any notion of 'mandatory' property."

This is crucial - different sites have different data available. Schema.org provides vocabulary, not validation rules.

### Hierarchy

- Single-rooted type hierarchy (Thing at root)
- Types can have multiple supertypes (rare)
- Properties can have super-properties
- Inverse property pairs (alumni/alumniOf, isPartOf/hasPart)

---

## 4. Extension Mechanisms

### Three Types of Extensions

| Type | Location | Governance |
|------|----------|------------|
| **Core** | schema.org | Steering Group |
| **Hosted** | subdomain (bib.schema.org) | Dedicated community groups |
| **External** | Other websites (gs1.org) | External organizations |

### Pending Extension

The `pending` extension is particularly interesting:

> "A 'live' hosted extension dedicated to 'pending' new vocabulary proposals... can be updated immediately, rather than waiting for a full official release."

This allows experimentation without polluting the core vocabulary.

### Extension Design Principles

1. **Backwards compatible** - Never break existing markup
2. **Minimal commitment** - Don't over-specify
3. **Community consensus** - Rough agreement before release
4. **Practical focus** - Driven by real use cases

---

## 5. Change Types

Schema.org releases can include:

| Change Type | Example | Risk Level |
|-------------|---------|------------|
| Bug fixes | Typos, markup errors | Low |
| New examples | Additional markup samples | Low |
| Description adjustments | Clarifying text | Low |
| New types/properties | Adding vocabulary | Medium |
| Type hierarchy changes | Reparenting | High |
| Deprecation | supersededBy | High |

### Deprecation Strategy

> "Occasionally we make changes that are not backwards compatible. We try to minimize these and to document them when they occur."

Uses `supersededBy` property to indicate deprecated terms.

---

## 6. Technical Infrastructure

### Key Properties for Schema Management

| Property | Purpose |
|----------|---------|
| `domainIncludes` | Types that can use this property |
| `rangeIncludes` | Expected value types |
| `supersededBy` | Deprecation pointer |
| `partOf` | Which extension (auto, bib, etc.) |

### Machine-Readable Formats

- RDFa (schema_org_rdfa.html)
- JSON-LD context file
- GitHub repository

---

## 7. Implications for Context Engine

### What to Adopt

1. **Multi-stage release pipeline**: staging → pending → release
2. **Steering group approval**: High bar for stability
3. **Pending extension**: Safe space for experimentation
4. **No mandatory properties**: Flexibility over strictness
5. **Backwards compatibility**: Never break existing patterns

### What to Adapt

| Schema.org | Context Engine |
|------------|----------------|
| Search engine driven | Community driven |
| Vocabulary only | Vocabulary + relationships |
| No validation | Quality validation |
| Unanimous approval | Tiered governance |

### Governance Model Inspiration

```
Tier 1: Schema Changes (high bar, steering group)
  - New node/edge types
  - Property definitions
  - Deprecations

Tier 2: Content Changes (medium bar, curator review)
  - New patterns
  - New entities
  - Relationship additions

Tier 3: Metadata Changes (low bar, automated)
  - Relationship weights
  - Usage statistics
  - Confidence scores
```

---

## 8. Key Quotes

> "We do not attempt to reach consensus at schema.org on what an ideal description of some type ought to contain - this makes consensus significantly easier to achieve."

This is wisdom - don't over-specify, let usage patterns emerge.

> "The information needs of consuming services may also vary."

Different contexts need different views of the same data.

---

## 9. Open Questions

1. How do we balance Schema.org's stability-first approach with our "living ontology" vision?
2. Should we adopt the pending extension model for experimental patterns?
3. How do we handle the tension between unanimous approval and rapid evolution?
4. What's our equivalent of the "steering group"?
