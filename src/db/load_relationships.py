#!/usr/bin/env python3
"""
Load Approved Relationships into Kuzu Graph Database

This script reads approved relationships from the review workflow
and creates edges in the Kuzu graph database.

Author: higgerix
Date: 2026-02-02
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from db.init_kuzu import get_connection

# Configuration
DATA_DIR = Path(__file__).parent.parent.parent / "data"
APPROVED_FILE = DATA_DIR / "relationships_approved.json"


def load_approved_relationships() -> list[dict]:
    """Load approved relationships from file."""
    if not APPROVED_FILE.exists():
        print(f"Error: {APPROVED_FILE} not found")
        return []
    
    with open(APPROVED_FILE) as f:
        data = json.load(f)
    
    return data.get('relationships', [])


def create_relationship_tables(conn) -> None:
    """Create relationship tables if they don't exist."""
    # ENABLES relationship
    try:
        conn.execute("""
            CREATE REL TABLE IF NOT EXISTS ENABLES (
                FROM Pattern TO Pattern,
                confidence DOUBLE,
                evidence STRING,
                discovered_by STRING,
                reviewed_by STRING,
                created_at STRING
            )
        """)
    except Exception as e:
        if "already exists" not in str(e).lower():
            print(f"Warning creating ENABLES: {e}")
    
    # REQUIRES relationship
    try:
        conn.execute("""
            CREATE REL TABLE IF NOT EXISTS REQUIRES (
                FROM Pattern TO Pattern,
                confidence DOUBLE,
                evidence STRING,
                discovered_by STRING,
                reviewed_by STRING,
                created_at STRING
            )
        """)
    except Exception as e:
        if "already exists" not in str(e).lower():
            print(f"Warning creating REQUIRES: {e}")
    
    # TENSIONS_WITH relationship
    try:
        conn.execute("""
            CREATE REL TABLE IF NOT EXISTS TENSIONS_WITH (
                FROM Pattern TO Pattern,
                confidence DOUBLE,
                evidence STRING,
                discovered_by STRING,
                reviewed_by STRING,
                created_at STRING
            )
        """)
    except Exception as e:
        if "already exists" not in str(e).lower():
            print(f"Warning creating TENSIONS_WITH: {e}")


def load_relationships_to_kuzu(relationships: list[dict]) -> dict:
    """Load relationships into Kuzu database."""
    db, conn = get_connection()
    
    # Create relationship tables
    print("Creating relationship tables...")
    create_relationship_tables(conn)
    
    # Track results
    results = {
        'loaded': 0,
        'skipped': 0,
        'errors': 0,
        'by_type': {'ENABLES': 0, 'REQUIRES': 0, 'TENSIONS_WITH': 0}
    }
    
    print(f"\nLoading {len(relationships)} relationships...")
    
    for i, rel in enumerate(relationships):
        source_id = rel['source_id']
        target_id = rel['target_id']
        rel_type = rel['relationship_type']
        confidence = rel.get('confidence', 0.5)
        evidence = rel.get('evidence', '').replace("'", "''")  # Escape quotes
        discovered_by = rel.get('discovered_by', 'unknown')
        reviewed_by = rel.get('reviewed_by', 'unknown')
        created_at = datetime.now().isoformat()
        
        # Build the query based on relationship type
        try:
            query = f"""
                MATCH (s:Pattern {{id: '{source_id}'}}), (t:Pattern {{id: '{target_id}'}})
                CREATE (s)-[:{rel_type} {{
                    confidence: {confidence},
                    evidence: '{evidence}',
                    discovered_by: '{discovered_by}',
                    reviewed_by: '{reviewed_by}',
                    created_at: '{created_at}'
                }}]->(t)
            """
            conn.execute(query)
            results['loaded'] += 1
            results['by_type'][rel_type] = results['by_type'].get(rel_type, 0) + 1
            
        except Exception as e:
            error_str = str(e).lower()
            if "cannot find node" in error_str or "no match" in error_str:
                results['skipped'] += 1
            else:
                results['errors'] += 1
                if results['errors'] <= 5:  # Only show first 5 errors
                    print(f"  Error loading {source_id} -> {target_id}: {e}")
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(relationships)}...")
    
    return results


def verify_relationships() -> dict:
    """Verify relationships were loaded correctly."""
    db, conn = get_connection()
    
    counts = {}
    
    for rel_type in ['ENABLES', 'REQUIRES', 'TENSIONS_WITH']:
        try:
            result = conn.execute(f"MATCH ()-[r:{rel_type}]->() RETURN COUNT(r)")
            if result.has_next():
                counts[rel_type] = result.get_next()[0]
        except:
            counts[rel_type] = 0
    
    return counts


def main():
    """Main function to load relationships."""
    print("=" * 50)
    print("LOADING RELATIONSHIPS INTO KUZU")
    print("=" * 50)
    
    # Load approved relationships
    relationships = load_approved_relationships()
    
    if not relationships:
        print("No approved relationships to load.")
        return
    
    print(f"\nFound {len(relationships)} approved relationships")
    
    # Load into Kuzu
    results = load_relationships_to_kuzu(relationships)
    
    # Verify
    print("\nVerifying loaded relationships...")
    counts = verify_relationships()
    
    # Summary
    print("\n" + "=" * 50)
    print("LOADING COMPLETE")
    print("=" * 50)
    print(f"\nResults:")
    print(f"  Loaded:  {results['loaded']}")
    print(f"  Skipped: {results['skipped']} (patterns not found)")
    print(f"  Errors:  {results['errors']}")
    
    print(f"\nBy Type:")
    for rel_type, count in results['by_type'].items():
        print(f"  {rel_type}: {count}")
    
    print(f"\nVerification (edges in graph):")
    for rel_type, count in counts.items():
        print(f"  {rel_type}: {count}")


if __name__ == "__main__":
    main()
