#!/usr/bin/env python3
"""
Context Engine API - Constellation Queries for Commons OS

This API exposes the pattern graph for:
1. Jekyll website (JavaScript fetch)
2. CustomGPTs (via Actions)
3. Direct API consumers

Endpoints:
- GET /constellations - Query patterns by archetype, stage, domain
- GET /patterns/{id}/related - Get related patterns
- GET /archetypes - List all archetypes with pattern counts
- GET /stages - List all stages
- GET /domains - List all domains
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.db.init_kuzu import get_connection

app = FastAPI(
    title="Commons OS Context Engine",
    description="Pattern constellation queries for context-aware discovery",
    version="1.0.0"
)

# CORS for Jekyll site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
db, conn = get_connection()


class PatternResult(BaseModel):
    title: str
    strength: Optional[float] = None
    importance: Optional[float] = None
    specificity: Optional[str] = None
    score: Optional[float] = None


class ConstellationResponse(BaseModel):
    archetype: str
    stage: Optional[str] = None
    domain: Optional[str] = None
    patterns: List[PatternResult]
    total: int


class ArchetypeInfo(BaseModel):
    name: str
    pattern_count: int
    avg_strength: float


class RelatedPattern(BaseModel):
    title: str
    relationship_type: str
    shared_contexts: Optional[int] = None


@app.get("/")
def root():
    """API health check and info."""
    return {
        "service": "Commons OS Context Engine",
        "version": "1.0.0",
        "endpoints": [
            "/constellations",
            "/patterns/{title}/related",
            "/archetypes",
            "/stages",
            "/domains"
        ]
    }


@app.get("/constellations", response_model=ConstellationResponse)
def get_constellation(
    archetype: str = Query(..., description="Organizational archetype (e.g., Startup, Enterprise, City)"),
    stage: Optional[str] = Query(None, description="Journey stage (e.g., Validation, Growth, Transformation)"),
    domain: Optional[str] = Query(None, description="Domain (e.g., Technology, Finance, Healthcare)"),
    min_strength: float = Query(0.5, description="Minimum archetype fit strength"),
    limit: int = Query(50, description="Maximum patterns to return")
):
    """
    Query pattern constellations by context.
    
    Examples:
    - /constellations?archetype=Startup&stage=Validation&domain=Finance
    - /constellations?archetype=Enterprise&stage=Transformation
    - /constellations?archetype=City&domain=Governance
    """
    try:
        if stage and domain:
            query = f'''
                MATCH (p:Pattern)-[s:SUITED_FOR]->(a:Archetype {{name: "{archetype}"}})
                MATCH (p)-[st:APPLIES_AT]->(stage:Stage {{name: "{stage}"}})
                MATCH (p)-[d:RELEVANT_FOR]->(dom:Domain {{name: "{domain}"}})
                WHERE s.strength >= {min_strength}
                RETURN p.title, s.strength, st.importance, d.specificity
                ORDER BY s.strength * st.importance DESC
                LIMIT {limit}
            '''
        elif stage:
            query = f'''
                MATCH (p:Pattern)-[s:SUITED_FOR]->(a:Archetype {{name: "{archetype}"}})
                MATCH (p)-[st:APPLIES_AT]->(stage:Stage {{name: "{stage}"}})
                WHERE s.strength >= {min_strength}
                RETURN p.title, s.strength, st.importance, null
                ORDER BY s.strength * st.importance DESC
                LIMIT {limit}
            '''
        elif domain:
            query = f'''
                MATCH (p:Pattern)-[s:SUITED_FOR]->(a:Archetype {{name: "{archetype}"}})
                MATCH (p)-[d:RELEVANT_FOR]->(dom:Domain {{name: "{domain}"}})
                WHERE s.strength >= {min_strength}
                RETURN p.title, s.strength, null, d.specificity
                ORDER BY s.strength DESC
                LIMIT {limit}
            '''
        else:
            query = f'''
                MATCH (p:Pattern)-[s:SUITED_FOR]->(a:Archetype {{name: "{archetype}"}})
                WHERE s.strength >= {min_strength}
                RETURN p.title, s.strength, null, null
                ORDER BY s.strength DESC
                LIMIT {limit}
            '''
        
        result = conn.execute(query)
        patterns = []
        while result.has_next():
            row = result.get_next()
            score = row[1] * (row[2] if row[2] else 1.0)
            patterns.append(PatternResult(
                title=row[0],
                strength=row[1],
                importance=row[2],
                specificity=row[3],
                score=score
            ))
        
        return ConstellationResponse(
            archetype=archetype,
            stage=stage,
            domain=domain,
            patterns=patterns,
            total=len(patterns)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/patterns/{title}/related")
def get_related_patterns(
    title: str,
    limit: int = Query(20, description="Maximum related patterns")
):
    """Get patterns related to a specific pattern through shared contexts and direct relationships."""
    try:
        related = []
        
        # Direct relationships (ENABLES, REQUIRES, TENSIONS_WITH)
        for rel_type in ["ENABLES", "REQUIRES", "TENSIONS_WITH"]:
            query = f'''
                MATCH (p1:Pattern {{title: "{title}"}})-[r:{rel_type}]->(p2:Pattern)
                RETURN p2.title, "{rel_type}"
            '''
            result = conn.execute(query)
            while result.has_next():
                row = result.get_next()
                related.append(RelatedPattern(
                    title=row[0],
                    relationship_type=row[1]
                ))
        
        # Shared archetypes
        query = f'''
            MATCH (p1:Pattern {{title: "{title}"}})-[:SUITED_FOR]->(a:Archetype)<-[:SUITED_FOR]-(p2:Pattern)
            WHERE p1 <> p2
            WITH p2.title AS related, COUNT(DISTINCT a) AS shared
            ORDER BY shared DESC
            LIMIT {limit}
            RETURN related, shared
        '''
        result = conn.execute(query)
        while result.has_next():
            row = result.get_next()
            related.append(RelatedPattern(
                title=row[0],
                relationship_type="SHARED_ARCHETYPES",
                shared_contexts=row[1]
            ))
        
        return {"pattern": title, "related": related[:limit]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/archetypes", response_model=List[ArchetypeInfo])
def list_archetypes():
    """List all archetypes with pattern counts."""
    query = '''
        MATCH (a:Archetype)<-[s:SUITED_FOR]-(p:Pattern)
        RETURN a.name AS name, COUNT(p) AS count, AVG(s.strength) AS avg_str
        ORDER BY count DESC
    '''
    result = conn.execute(query)
    archetypes = []
    while result.has_next():
        row = result.get_next()
        archetypes.append(ArchetypeInfo(
            name=row[0],
            pattern_count=row[1],
            avg_strength=row[2]
        ))
    return archetypes


@app.get("/stages")
def list_stages():
    """List all stages with pattern counts."""
    query = '''
        MATCH (s:Stage)<-[a:APPLIES_AT]-(p:Pattern)
        RETURN s.name AS name, s.sequence AS seq, COUNT(p) AS count
        ORDER BY seq
    '''
    result = conn.execute(query)
    stages = []
    while result.has_next():
        row = result.get_next()
        stages.append({"name": row[0], "sequence": row[1], "pattern_count": row[2]})
    return stages


@app.get("/domains")
def list_domains():
    """List all domains with pattern counts."""
    query = '''
        MATCH (d:Domain)<-[r:RELEVANT_FOR]-(p:Pattern)
        RETURN d.name AS name, COUNT(p) AS count
        ORDER BY count DESC
    '''
    result = conn.execute(query)
    domains = []
    while result.has_next():
        row = result.get_next()
        domains.append({"name": row[0], "pattern_count": row[1]})
    return domains


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
