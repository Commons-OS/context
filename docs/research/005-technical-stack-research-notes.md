# Technical Stack Research Notes

**Date**: 2026-02-02  
**Sources**: Kuzu benchmarks, Neo4j documentation, HybridRAG research, DuckDB graph extensions

---

## 1. Graph Database Options

The Context Engine requires a graph database that can handle pattern relationships, entity connections, and context-aware traversals. Based on the research, here are the primary options:

### 1.1 Comparison Matrix

| Feature | Kuzu | Neo4j | DuckDB + Extensions | File-based (JSON) |
|---------|------|-------|---------------------|-------------------|
| **Architecture** | Embedded | Client-server | Embedded | None |
| **Query Language** | Cypher | Cypher | SQL + Graph | Custom |
| **Performance** | Excellent | Good | Good for simple | Poor |
| **Scalability** | 100M+ edges | Billions | Millions | Thousands |
| **Deployment** | Zero-config | Server required | Zero-config | Zero-config |
| **Cost** | Free (MIT) | Enterprise license | Free | Free |
| **Python Integration** | Native | Client library | Native | Native |
| **Vector Support** | Via extension | Native (5.x) | Via extension | Manual |

### 1.2 Kuzu: The Embedded Graph Database

Kuzu stands out as the most promising option for the Context Engine. It is designed to be the "DuckDB of graph databases" - an embedded, high-performance graph database that runs in-process with the application.

**Key Technical Advantages:**

**Vectorized Execution**: Kuzu stores data in a column-oriented manner and processes queries in batches, enabling CPU optimizations via SIMD (Single Instruction, Multiple Data). This is the same approach used by DuckDB and ClickHouse for analytical workloads.

**Morsel-Driven Parallelism**: Query workloads are divided into small parts (morsels) that are dynamically distributed between threads during runtime. Each thread processes its morsel independently, only synchronizing when necessary.

**Worst-Case Optimal Joins (WCOJ)**: For queries involving cyclic patterns (common in knowledge graphs), Kuzu uses WCOJ algorithms that evaluate joins column-at-a-time rather than table-at-a-time. This provides massive speedups for graph pattern matching.

**Factorized Execution**: When evaluating many-to-many joins, Kuzu compresses intermediate results exponentially, reducing memory usage and improving performance for multi-hop traversals.

**Benchmark Results (vs Neo4j):**
- Simple queries: 2-5x faster
- Multi-hop traversals: 10-50x faster
- Cyclic pattern queries: 100x+ faster

### 1.3 Neo4j Considerations

Neo4j remains the industry standard for graph databases and offers mature tooling, but has drawbacks for the Context Engine:

| Advantage | Disadvantage |
|-----------|--------------|
| Mature ecosystem | Requires server deployment |
| Native vector search (5.x) | Enterprise features require license |
| Excellent visualization tools | Heavier resource footprint |
| Large community | Client-server latency |

### 1.4 DuckDB with Graph Extensions

DuckDB now supports graph queries through extensions, making it a viable option for simpler graph workloads. However, it lacks the sophisticated graph algorithms and optimizations of dedicated graph databases.

---

## 2. Vector Database Options

For semantic search and context-aware retrieval, the Context Engine needs vector storage and similarity search capabilities.

### 2.1 Comparison Matrix

| Feature | LanceDB | Pinecone | Weaviate | Chroma |
|---------|---------|----------|----------|--------|
| **Architecture** | Embedded | Cloud | Self-hosted/Cloud | Embedded |
| **Scalability** | Billions | Billions | Millions | Millions |
| **Cost** | Free | Usage-based | Free/Enterprise | Free |
| **Integration** | Python native | API | API | Python native |
| **Hybrid Search** | Yes | Yes | Yes | Limited |

### 2.2 LanceDB: The Embedded Vector Database

LanceDB complements Kuzu as an embedded vector database, following the same philosophy of zero-config, in-process operation.

**Key Features:**
- Native Python integration
- Columnar storage (Lance format)
- Hybrid search (vector + metadata filtering)
- No server required
- Scales to billions of vectors

### 2.3 Hybrid Approach: Graph + Vector

The HybridRAG research (Sarmah et al. 2024) demonstrates that combining knowledge graphs with vector retrieval outperforms either approach alone:

| Approach | Retrieval Accuracy | Generation Quality |
|----------|-------------------|-------------------|
| VectorRAG only | Good | Prone to hallucination |
| GraphRAG only | Structured | Missing semantic nuance |
| HybridRAG | Best | Most accurate |

**Implementation Strategy:**
1. Store pattern content as vectors in LanceDB
2. Store pattern relationships in Kuzu
3. Query both: vector similarity for semantic matching, graph traversal for relationships
4. Merge and re-rank results based on context

---

## 3. Recommended Architecture

Based on the research, the Context Engine should adopt a **dual-embedded database architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                    Context Engine                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐              ┌──────────────┐         │
│  │    Kuzu      │              │   LanceDB    │         │
│  │  (Graph DB)  │◄────────────►│  (Vector DB) │         │
│  │              │   Hybrid     │              │         │
│  │ - Patterns   │   Query      │ - Embeddings │         │
│  │ - Entities   │   Engine     │ - Semantic   │         │
│  │ - Relations  │              │   Search     │         │
│  └──────────────┘              └──────────────┘         │
│         │                              │                 │
│         └──────────────┬───────────────┘                 │
│                        │                                 │
│                        ▼                                 │
│              ┌──────────────────┐                        │
│              │  Query Processor │                        │
│              │  - Context-aware │                        │
│              │  - Re-ranking    │                        │
│              │  - Explanation   │                        │
│              └──────────────────┘                        │
│                        │                                 │
│                        ▼                                 │
│              ┌──────────────────┐                        │
│              │   Results API    │                        │
│              └──────────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

### 3.1 Why Embedded?

The embedded architecture aligns with Commons OS principles:

| Principle | How Embedded Supports It |
|-----------|-------------------------|
| **Simplicity** | No server deployment, zero-config |
| **Portability** | Runs anywhere Python runs |
| **Cost** | No infrastructure costs |
| **Privacy** | Data stays local |
| **Hackability** | Easy to modify and extend |

### 3.2 Data Flow

1. **Pattern Files** (Markdown + YAML) → Source of truth
2. **Build Process** → Generates Kuzu graph + LanceDB vectors
3. **Query Time** → Hybrid search across both databases
4. **Results** → Merged, ranked, explained

---

## 4. File-Based Fallback

For simpler deployments or when databases are overkill, the Context Engine should support a file-based fallback using the existing `graph.json` and `search_index.json`:

| Scenario | Recommended Stack |
|----------|-------------------|
| GitHub Pages static site | File-based (JSON) |
| Local development | Kuzu + LanceDB |
| Production API | Kuzu + LanceDB |
| Offline/Edge | Kuzu + LanceDB |

---

## 5. Implementation Considerations

### 5.1 Embedding Generation

Pattern embeddings should be generated from:
- Pattern title and description
- Problem and solution sections
- Related pattern titles
- Classification tags

**Recommended Model**: OpenAI `text-embedding-3-small` or open-source `all-MiniLM-L6-v2`

### 5.2 Graph Schema

```cypher
// Node types
(:Pattern {id, title, slug, domains[], categories[]})
(:Entity {id, name, type, scale})
(:Concept {id, name, definition})

// Edge types
(:Pattern)-[:ENABLES]->(:Pattern)
(:Pattern)-[:REQUIRES]->(:Pattern)
(:Pattern)-[:TENSIONS_WITH]->(:Pattern)
(:Pattern)-[:RELATED_TO]->(:Pattern)
(:Entity)-[:ADOPTS]->(:Pattern)
(:Entity)-[:SIMILAR_TO]->(:Entity)
(:Pattern)-[:BELONGS_TO]->(:Concept)
```

### 5.3 Build Pipeline

```bash
# 1. Parse pattern files
python scripts/parse_patterns.py

# 2. Generate embeddings
python scripts/generate_embeddings.py

# 3. Build Kuzu graph
python scripts/build_kuzu_graph.py

# 4. Build LanceDB index
python scripts/build_lancedb_index.py

# 5. Validate
python scripts/validate_context_engine.py
```

---

## 6. Open Questions

1. How do we handle incremental updates without full rebuilds?
2. What is the optimal embedding dimension for pattern search?
3. How do we version the graph schema?
4. Should we support distributed deployment for scale?
5. How do we handle multi-language patterns?
