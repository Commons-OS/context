# Wikidata Ontology Structure - Deep Research Notes

**Date**: 2026-02-02  
**Source**: Wikidata WikiProject Ontology/Modelling

---

## 1. Core Ontological Primitives

Wikidata's ontology is built on four fundamental constructs:

| Construct | Wikidata ID | Purpose |
|-----------|-------------|---------|
| **class** | Q16889133 | The class of all classes |
| **entity** | Q35120 | The class of all items (root of everything) |
| **instance of** | P31 | Relates an item to its class |
| **subclass of** | P279 | Relates a class to a more general class |

### Key Insight: Two Fundamental Relationships

Wikidata distinguishes clearly between:
- **instance of (P31)**: "Angela Merkel is an instance of human"
- **subclass of (P279)**: "human is a subclass of person"

This is the classic class-instance vs class-class distinction from formal ontology.

---

## 2. Class Hierarchy Design

### Transitive Inheritance

Wikidata uses **implicit transitive inheritance**:
- If `human` subclass_of `person` AND `person` subclass_of `animal`
- Then `human` is implicitly a subclass of `animal`
- **No need to explicitly state** the transitive closure

This is critical for scalability - you don't need to maintain all transitive relationships explicitly.

### Instance Inheritance

Similarly for instances:
- If `Angela Merkel` instance_of `human` AND `human` subclass_of `animal`
- Then `Angela Merkel` is implicitly an instance of `animal`
- **No need to explicitly state** instance relationships to parent classes

---

## 3. Metaclasses

Wikidata has a sophisticated metaclass system:

| Level | Example | Description |
|-------|---------|-------------|
| Instance | Angela Merkel | A specific thing |
| First-order class | human | A class whose instances are things |
| Metaclass | automobile model | A class whose instances are classes |
| Meta-metaclass | metaclass | The class of all metaclasses |

### Example: Honda Accord
- `Honda Accord` is an **instance of** `automobile model`
- `automobile model` is a **metaclass** (its instances are classes)
- Individual Honda Accords would be instances of `Honda Accord`

This three-level structure (instance → class → metaclass) is powerful but can be confusing.

---

## 4. Design Guidelines

### What Should Be a Class?

Classes in Wikidata:
- Do NOT need to have instances (e.g., `quark` has no instances in Wikidata)
- Do NOT need to have physical objects as instances (e.g., `unicorn`, `set`)
- CAN be instances of other classes (metaclass pattern)

### Anti-Patterns to Avoid

1. **Don't mix instance and subclass of the same class**
   - BAD: `white` is both subclass_of AND instance_of `color`
   - Exception: `class` and `metaclass` can be instances of themselves

2. **Don't mix groups and individuals in the same class hierarchy**
   - BAD: `color` having subclasses `white` (a color) AND `primary color` (a group of colors)

---

## 5. Implications for Context Engine

### What to Adopt

1. **Two-relationship model**: Clear distinction between `instance_of` and `subclass_of`
2. **Implicit transitive closure**: Don't store redundant relationships
3. **Root entity**: Have a top-level class that everything inherits from
4. **Metaclass support**: Allow patterns to be instances of pattern types

### Potential Schema

```
Pattern (instance) → PatternType (class) → PatternCategory (metaclass)

Example:
- "Lean Startup" instance_of "Methodology Pattern"
- "Methodology Pattern" subclass_of "Pattern"
- "Pattern" is the root class

CommonsEntity (instance) → EntityType (class) → EntityScale (metaclass)

Example:
- "Buurtzorg" instance_of "Healthcare Organization"
- "Healthcare Organization" subclass_of "Organization"
- "Organization" subclass_of "CommonsEntity"
```

### Key Difference from Wikidata

Wikidata is **descriptive** (modeling the world as it is).
Context Engine is **prescriptive** (providing guidance for action).

This means our relationships need to include:
- `enables` (Pattern A enables Pattern B)
- `requires` (Pattern A requires Pattern B)
- `tensions_with` (Pattern A creates tension with Pattern B)
- `adopted_by` (Pattern adopted by Entity)

These are not in Wikidata's model because they're domain-specific.

---

## 6. Open Questions

1. Should we use Wikidata's Q-number style IDs or human-readable slugs?
2. How do we handle the "same pattern, different context" problem?
3. Should patterns be able to be both instances and classes (like Wikidata allows)?
4. How do we version the ontology as it evolves?

---

## 7. Sources to Explore Further

- [ ] Wikidata property constraints system
- [ ] How Wikidata handles ontology evolution
- [ ] Wikidata's approach to conflicting classifications
- [ ] SPARQL query patterns for Wikidata


---

# Roam Research Data Structure - Deep Research Notes

**Date**: 2026-02-02  
**Source**: Zsolt Viczián's Deep Dive

---

## 1. Datomic Database Foundation

Roam is built on **Datomic**, a database designed by Rich Hickey (creator of Clojure). The fundamental unit is a **Datom** - an individual fact consisting of four elements:

| Element | Description |
|---------|-------------|
| **Entity ID** | Internal identifier for the block |
| **Attribute** | The property being described (e.g., `:block/string`) |
| **Value** | The value of that property |
| **Transaction ID** | When this fact was recorded |

### Key Insight: Everything is a Fact

Unlike traditional databases with tables and rows, Datomic stores **individual facts**. This enables:
- Time-travel queries (see data as it was at any point)
- Transactional consistency across devices
- Complex undo operations

---

## 2. Block-Based Architecture

### Core Concept: Pages are Blocks

In Roam, a **page** is just a special type of **block**. Both are treated identically in most respects. This is a crucial design decision that enables:
- Uniform querying
- Consistent linking behavior
- Transclusion (embedding blocks anywhere)

### Two ID Systems

| ID Type | Description | Example |
|---------|-------------|---------|
| **Entity ID** | Internal database ID (hidden) | 5 |
| **Public ID** | User-visible reference | `((GGv3cyL6Y))` or `[[Page Title]]` |

---

## 3. Tree Structure (Forest Model)

> "The Roam database is like a forest. Each page is a tree. The root is the page, branches are higher-level paragraphs, leaves are deepest nested blocks."

### Parent-Child Relationships

Roam maintains **bidirectional pointers**:

| Attribute | Direction | Scope |
|-----------|-----------|-------|
| `:block/children` | Parent → Child | Immediate children only |
| `:block/parents` | Child → Parent | ALL ancestors (transitive) |

This asymmetry is interesting:
- Children only list immediate descendants
- Parents list the ENTIRE ancestry chain

### Block Attributes

**Common to all blocks:**
- `:block/uid` - Public ID
- `:create/email`, `:create/time` - Creation metadata
- `:edit/email`, `:edit/time` - Edit metadata

**Page-only:**
- `:node/title` - The page title (how you identify pages)

**Paragraph-only:**
- `:block/page` - Reference to containing page
- `:block/order` - Sequence within parent
- `:block/string` - The actual content
- `:block/parents` - Ancestor chain

---

## 4. References and Backlinks

### Reference Types

| Attribute | Description |
|-----------|-------------|
| `:block/refs` | Outgoing references (pages/blocks this block links to) |
| `:block/_refs` | Incoming references (backlinks - who links to this) |

The underscore prefix (`_refs`) is Datomic's convention for **reverse lookups**.

### Bidirectional Linking

When you create `[[Page Link]]` or `((block-ref))`:
1. The source block gets the target in `:block/refs`
2. The target automatically gets the source in `:block/_refs`
3. No manual maintenance required

---

## 5. Implications for Context Engine

### What to Adopt

1. **Datom-style facts**: Consider storing relationships as individual facts with provenance
2. **Bidirectional pointers**: Automatically maintain reverse relationships
3. **Block as universal unit**: Patterns could be "blocks" that can be embedded/linked anywhere
4. **Transaction history**: Track when relationships were created/modified

### Key Differences

| Roam | Context Engine |
|------|----------------|
| Personal knowledge | Shared knowledge commons |
| Free-form content | Structured patterns |
| Single user | Community governance |
| Implicit structure | Explicit ontology |

### Schema Inspiration

```
Pattern:
  :pattern/id - TypeID
  :pattern/title - Human-readable name
  :pattern/slug - URL-friendly identifier
  :pattern/content - Markdown body
  :pattern/refs - Outgoing pattern references
  :pattern/_refs - Incoming references (auto-computed)
  :pattern/domains - Classification tags
  :pattern/parents - Ancestry (for pattern hierarchies)
  :pattern/children - Sub-patterns
  :create/time, :edit/time - Temporal metadata
```

---

## 6. Querying Patterns

Roam uses **Datalog** for queries, which is declarative and pattern-based:

```datalog
[:find ?title ?uid
 :where
 [?p :node/title ?title]
 [?p :block/uid ?uid]]
```

This finds all pages with their titles and UIDs.

For Context Engine, we could support similar queries:
```
[:find ?pattern ?related
 :where
 [?pattern :pattern/title "Lean Startup"]
 [?pattern :pattern/enables ?related]]
```

---

## 7. Open Questions

1. Should we adopt Datomic/Datalog or use a more accessible query language?
2. How do we handle the "forest" vs "graph" tension (Roam is trees, we need arbitrary graphs)?
3. Can we achieve bidirectional linking with file-based storage?
4. How do we version facts over time?
