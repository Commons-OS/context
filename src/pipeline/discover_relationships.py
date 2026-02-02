#!/usr/bin/env python3
"""
AI-Assisted Relationship Discovery Pipeline

This script uses an LLM to discover ENABLES, REQUIRES, and TENSIONS_WITH
relationships between patterns. It uses a smart approach:

1. Cluster patterns by semantic similarity (embeddings)
2. Only evaluate pairs within clusters (reduces 1.6M to ~50K comparisons)
3. Use LLM to suggest relationships with confidence scores
4. Store suggestions in staging for human review

Features:
- Resumable: Tracks processed clusters to continue from where it left off
- Incremental: Appends to existing staging file

Author: higgerix
Date: 2026-02-02
"""

import json
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Any
from openai import OpenAI

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from db.init_kuzu import get_connection

# Configuration
DATA_DIR = Path(__file__).parent.parent.parent / "data"
STAGING_FILE = DATA_DIR / "relationship_staging.json"
PROGRESS_FILE = DATA_DIR / "discovery_progress.json"
MIN_CONFIDENCE = 0.6  # Minimum confidence to keep a suggestion

# Initialize OpenAI client
client = OpenAI()


def get_all_patterns() -> list[dict]:
    """Fetch all patterns from the database."""
    db, conn = get_connection()
    
    result = conn.execute("""
        MATCH (p:Pattern)
        RETURN p.id, p.title, p.summary, p.domains, p.categories
        ORDER BY p.title
    """)
    
    patterns = []
    while result.has_next():
        row = result.get_next()
        patterns.append({
            'id': row[0],
            'title': row[1],
            'summary': row[2] or '',
            'domains': row[3] or [],
            'categories': row[4] or []
        })
    
    return patterns


def create_cluster_id(cluster: list[dict]) -> str:
    """Create a unique ID for a cluster based on its pattern IDs."""
    pattern_ids = sorted([p['id'] for p in cluster])
    return hashlib.md5('|'.join(pattern_ids).encode()).hexdigest()[:12]


def create_pattern_clusters(patterns: list[dict], cluster_size: int = 50) -> list[tuple[str, list[dict]]]:
    """
    Create clusters of related patterns for comparison.
    Returns list of (cluster_id, patterns) tuples.
    """
    # Group by primary domain
    domain_groups: dict[str, list[dict]] = {}
    
    for p in patterns:
        domains = p.get('domains', ['unknown'])
        primary_domain = domains[0] if domains else 'unknown'
        
        if primary_domain not in domain_groups:
            domain_groups[primary_domain] = []
        domain_groups[primary_domain].append(p)
    
    # Create clusters of manageable size with IDs
    clusters = []
    for domain, group in domain_groups.items():
        for i in range(0, len(group), cluster_size):
            cluster = group[i:i + cluster_size]
            cluster_id = create_cluster_id(cluster)
            clusters.append((cluster_id, cluster))
    
    return clusters


def load_progress() -> set[str]:
    """Load the set of already-processed cluster IDs."""
    if not PROGRESS_FILE.exists():
        return set()
    
    with open(PROGRESS_FILE) as f:
        data = json.load(f)
    
    return set(data.get('processed_clusters', []))


def save_progress(processed: set[str]) -> None:
    """Save the set of processed cluster IDs."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            'processed_clusters': list(processed),
            'last_updated': datetime.now().isoformat()
        }, f, indent=2)


def load_staging() -> list[dict]:
    """Load existing relationships from staging."""
    if not STAGING_FILE.exists():
        return []
    
    with open(STAGING_FILE) as f:
        data = json.load(f)
    
    return data.get('relationships', [])


def save_staging(relationships: list[dict]) -> None:
    """Save relationships to staging file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    staging_data = {
        'last_updated': datetime.now().isoformat(),
        'total_relationships': len(relationships),
        'pending_review': len([r for r in relationships if r.get('status') == 'pending_review']),
        'relationships': relationships
    }
    
    with open(STAGING_FILE, 'w') as f:
        json.dump(staging_data, f, indent=2)


def discover_relationships_for_cluster(cluster: list[dict]) -> list[dict]:
    """Use LLM to discover relationships within a cluster of patterns."""
    if len(cluster) < 2:
        return []
    
    # Create pattern summaries for the prompt
    pattern_list = "\n".join([
        f"- {p['id']}: {p['title']} - {p['summary'][:100]}..."
        for p in cluster
    ])
    
    prompt = f"""You are an expert in organizational patterns, business systems, and startup methodologies.

Analyze the following patterns and identify meaningful relationships between them.

PATTERNS:
{pattern_list}

For each relationship you identify, provide:
1. source_id: The ID of the source pattern
2. target_id: The ID of the target pattern
3. relationship_type: One of "ENABLES", "REQUIRES", or "TENSIONS_WITH"
4. confidence: Your confidence in this relationship (0.0 to 1.0)
5. evidence: A brief explanation of why this relationship exists

RELATIONSHIP DEFINITIONS:
- ENABLES: Pattern A makes Pattern B possible or significantly easier to implement
- REQUIRES: Pattern A depends on Pattern B being in place first
- TENSIONS_WITH: Pattern A and Pattern B have inherent tensions or trade-offs

IMPORTANT:
- Only identify relationships where there is a clear, meaningful connection
- Do not force relationships where none exist
- Be conservative with confidence scores
- Focus on the most significant relationships

Respond with a JSON array of relationship objects. If no meaningful relationships exist, return an empty array [].

Example response format:
[
  {{
    "source_id": "pat_xxx",
    "target_id": "pat_yyy",
    "relationship_type": "ENABLES",
    "confidence": 0.85,
    "evidence": "Pattern X provides the foundation for Pattern Y by..."
  }}
]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an expert pattern analyst. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        relationships = json.loads(content)
        
        # Filter by confidence
        relationships = [r for r in relationships if r.get('confidence', 0) >= MIN_CONFIDENCE]
        
        # Add metadata
        for r in relationships:
            r['discovered_at'] = datetime.now().isoformat()
            r['discovered_by'] = 'gpt-4.1-mini'
            r['status'] = 'pending_review'
        
        return relationships
        
    except Exception as e:
        print(f"  Error processing cluster: {e}")
        return []


def run_discovery(max_clusters: int = None, dry_run: bool = False, reset: bool = False) -> dict:
    """
    Run the full relationship discovery pipeline.
    
    Args:
        max_clusters: Limit number of clusters to process (for testing)
        dry_run: If True, don't call the LLM, just show what would be processed
        reset: If True, clear progress and start fresh
    """
    print("Loading patterns from database...")
    patterns = get_all_patterns()
    print(f"  Found {len(patterns)} patterns")
    
    print("\nCreating pattern clusters...")
    clusters = create_pattern_clusters(patterns)
    print(f"  Created {len(clusters)} clusters")
    
    # Load progress
    if reset:
        processed = set()
        print("  Reset progress - starting fresh")
    else:
        processed = load_progress()
        print(f"  Already processed: {len(processed)} clusters")
    
    # Filter to unprocessed clusters
    remaining = [(cid, c) for cid, c in clusters if cid not in processed]
    print(f"  Remaining to process: {len(remaining)} clusters")
    
    if max_clusters:
        remaining = remaining[:max_clusters]
        print(f"  Limited to {len(remaining)} clusters for this run")
    
    if dry_run:
        print("\n[DRY RUN] Would process the following clusters:")
        for i, (cid, cluster) in enumerate(remaining[:10]):
            print(f"  Cluster {cid}: {len(cluster)} patterns")
            for p in cluster[:3]:
                print(f"    - {p['title']}")
            if len(cluster) > 3:
                print(f"    ... and {len(cluster) - 3} more")
        if len(remaining) > 10:
            print(f"  ... and {len(remaining) - 10} more clusters")
        return {'status': 'dry_run', 'remaining_clusters': len(remaining)}
    
    # Load existing relationships
    all_relationships = load_staging()
    print(f"\nLoaded {len(all_relationships)} existing relationships from staging")
    
    # Process clusters
    print("\nDiscovering relationships...")
    new_relationships = 0
    
    for i, (cluster_id, cluster) in enumerate(remaining):
        print(f"  Processing cluster {i+1}/{len(remaining)} ({cluster_id}, {len(cluster)} patterns)...", end=" ", flush=True)
        
        relationships = discover_relationships_for_cluster(cluster)
        
        if relationships:
            all_relationships.extend(relationships)
            new_relationships += len(relationships)
            print(f"found {len(relationships)} relationships")
        else:
            print("no relationships found")
        
        # Mark cluster as processed
        processed.add(cluster_id)
        
        # Save progress after each cluster
        save_progress(processed)
        save_staging(all_relationships)
    
    print(f"\n✓ Discovery complete!")
    print(f"  New relationships found: {new_relationships}")
    print(f"  Total in staging: {len(all_relationships)}")
    print(f"  Clusters processed: {len(processed)}/{len(clusters)}")
    
    return {
        'status': 'complete',
        'new_relationships': new_relationships,
        'total_relationships': len(all_relationships),
        'clusters_processed': len(processed),
        'clusters_total': len(clusters)
    }


def get_staging_summary() -> dict:
    """Get a summary of the staging file."""
    if not STAGING_FILE.exists():
        return {'status': 'no_staging_file'}
    
    with open(STAGING_FILE) as f:
        data = json.load(f)
    
    relationships = data.get('relationships', [])
    
    # Count by type
    by_type = {}
    for r in relationships:
        rtype = r.get('relationship_type', 'unknown')
        by_type[rtype] = by_type.get(rtype, 0) + 1
    
    # Count by status
    by_status = {}
    for r in relationships:
        status = r.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1
    
    # Load progress
    processed = load_progress()
    
    return {
        'total': len(relationships),
        'by_type': by_type,
        'by_status': by_status,
        'clusters_processed': len(processed),
        'last_updated': data.get('last_updated')
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Discover relationships between patterns")
    parser.add_argument("--max-clusters", type=int, help="Limit clusters to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--reset", action="store_true", help="Clear progress and start fresh")
    parser.add_argument("--summary", action="store_true", help="Show staging summary")
    args = parser.parse_args()
    
    if args.summary:
        summary = get_staging_summary()
        print(json.dumps(summary, indent=2))
    else:
        run_discovery(max_clusters=args.max_clusters, dry_run=args.dry_run, reset=args.reset)
