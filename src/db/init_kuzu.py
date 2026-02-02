#!/usr/bin/env python3
"""
Initialize the Kuzu database with the Context Engine schema.

This script creates the database and defines all node and relationship tables
according to the schema specification (002-context-engine-schema-specification.md).

Author: higgerix
Date: 2026-02-02
"""

import kuzu
import os
import shutil
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent.parent / "data" / "context_engine.db"


def create_schema(conn: kuzu.Connection) -> None:
    """Create all node and relationship tables."""
    
    print("Creating node tables...")
    
    # Pattern node
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Pattern (
            id STRING PRIMARY KEY,
            slug STRING,
            title STRING,
            summary STRING,
            content STRING,
            domains STRING[],
            categories STRING[],
            confidence DOUBLE DEFAULT 0.8,
            source_url STRING,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ Pattern table created")
    
    # CommonsEntity node
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS CommonsEntity (
            id STRING PRIMARY KEY,
            name STRING,
            entity_type STRING,
            scale STRING,
            description STRING,
            context STRING,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)
    print("  ✓ CommonsEntity table created")
    
    # Concept node
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Concept (
            id STRING PRIMARY KEY,
            name STRING,
            definition STRING,
            aliases STRING[],
            created_at TIMESTAMP
        )
    """)
    print("  ✓ Concept table created")
    
    # Source node
    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Source (
            id STRING PRIMARY KEY,
            title STRING,
            url STRING,
            author STRING,
            publication_date DATE,
            source_type STRING
        )
    """)
    print("  ✓ Source table created")
    
    print("\nCreating relationship tables...")
    
    # Pattern-to-Pattern relationships
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS ENABLES (
            FROM Pattern TO Pattern,
            strength DOUBLE,
            evidence STRING,
            source_id STRING,
            created_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ ENABLES relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS REQUIRES (
            FROM Pattern TO Pattern,
            strength DOUBLE,
            evidence STRING,
            created_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ REQUIRES relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS TENSIONS_WITH (
            FROM Pattern TO Pattern,
            description STRING,
            resolution_hint STRING,
            created_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ TENSIONS_WITH relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS RELATED_TO (
            FROM Pattern TO Pattern,
            relation_type STRING,
            created_at TIMESTAMP
        )
    """)
    print("  ✓ RELATED_TO relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS GENERALIZES (
            FROM Pattern TO Pattern,
            created_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ GENERALIZES relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS SPECIALIZES (
            FROM Pattern TO Pattern,
            created_at TIMESTAMP,
            created_by STRING
        )
    """)
    print("  ✓ SPECIALIZES relationship created")
    
    # Pattern-to-CommonsEntity relationships
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS ADOPTED_BY (
            FROM Pattern TO CommonsEntity,
            since DATE,
            success_level STRING,
            evidence STRING,
            source_id STRING,
            created_at TIMESTAMP
        )
    """)
    print("  ✓ ADOPTED_BY relationship created")
    
    # Pattern-to-Concept relationships
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS BELONGS_TO (
            FROM Pattern TO Concept,
            relevance DOUBLE,
            created_at TIMESTAMP
        )
    """)
    print("  ✓ BELONGS_TO relationship created")
    
    # CommonsEntity-to-CommonsEntity relationships
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS INSPIRED_BY (
            FROM CommonsEntity TO CommonsEntity,
            description STRING,
            created_at TIMESTAMP
        )
    """)
    print("  ✓ INSPIRED_BY relationship created")
    
    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS PART_OF (
            FROM CommonsEntity TO CommonsEntity,
            role STRING,
            since DATE,
            created_at TIMESTAMP
        )
    """)
    print("  ✓ PART_OF relationship created")


def init_database(force_recreate: bool = False) -> kuzu.Database:
    """Initialize the Kuzu database."""
    
    if force_recreate and DB_PATH.exists():
        print(f"Removing existing database at {DB_PATH}...")
        shutil.rmtree(DB_PATH)
    
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Initializing Kuzu database at {DB_PATH}...")
    db = kuzu.Database(str(DB_PATH))
    conn = kuzu.Connection(db)
    
    create_schema(conn)
    
    print("\n✓ Database initialized successfully!")
    return db


def get_connection() -> tuple[kuzu.Database, kuzu.Connection]:
    """Get a connection to the existing database."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run init_database() first.")
    
    db = kuzu.Database(str(DB_PATH))
    conn = kuzu.Connection(db)
    return db, conn


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize the Context Engine Kuzu database")
    parser.add_argument("--force", action="store_true", help="Force recreate the database")
    args = parser.parse_args()
    
    init_database(force_recreate=args.force)
