#!/usr/bin/env python3
"""
Load patterns from the patterns repository into the Kuzu database.

This script reads all pattern markdown files, extracts their YAML frontmatter,
and inserts them into the Pattern node table.

Author: higgerix
Date: 2026-02-02
"""

import kuzu
import yaml
import re
from pathlib import Path
from datetime import datetime
from typing import Any

from init_kuzu import get_connection, DB_PATH

# Path to patterns repository
PATTERNS_REPO = Path("/home/ubuntu/work/patterns-repo")
PATTERNS_DIR = PATTERNS_REPO / "_patterns"


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2)
    
    return frontmatter, body


def extract_summary(body: str) -> str:
    """Extract the first meaningful paragraph as summary."""
    # Skip headers and find first paragraph
    lines = body.strip().split('\n')
    paragraph = []
    in_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                break
            continue
        if stripped.startswith('#'):
            continue
        in_paragraph = True
        paragraph.append(stripped)
    
    summary = ' '.join(paragraph)
    # Truncate to ~200 chars
    if len(summary) > 200:
        summary = summary[:197] + '...'
    
    return summary


def load_patterns() -> int:
    """Load all patterns into the database."""
    
    db, conn = get_connection()
    
    pattern_files = list(PATTERNS_DIR.glob("*.md"))
    print(f"Found {len(pattern_files)} pattern files")
    
    loaded = 0
    errors = 0
    
    for filepath in pattern_files:
        try:
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = parse_frontmatter(content)
            
            if not frontmatter.get('id'):
                print(f"  ⚠ Skipping {filepath.name}: no id")
                continue
            
            # Extract fields
            pattern_id = frontmatter.get('id', '')
            slug = frontmatter.get('slug', filepath.stem)
            title = frontmatter.get('title', '')
            summary = extract_summary(body)
            
            # Handle domains - can be in classification.commons_domain or directly
            classification = frontmatter.get('classification', {})
            domains = classification.get('commons_domain', [])
            if isinstance(domains, str):
                domains = [domains]
            
            # Handle categories
            categories = classification.get('category', [])
            if isinstance(categories, str):
                categories = [categories]
            
            # Handle timestamps
            created = frontmatter.get('created', datetime.now())
            if isinstance(created, str):
                try:
                    created = datetime.fromisoformat(created.replace('Z', '+00:00'))
                except:
                    created = datetime.now()
            
            modified = frontmatter.get('modified', created)
            if isinstance(modified, str):
                try:
                    modified = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                except:
                    modified = created
            
            # Get contributors
            contributors = frontmatter.get('contributors', ['unknown'])
            created_by = contributors[0] if contributors else 'unknown'
            
            # Get source URL
            source_url = ''
            sources = frontmatter.get('sources', [])
            if sources and isinstance(sources, list) and len(sources) > 0:
                source_url = str(sources[0])
            
            # Insert into database
            conn.execute("""
                MERGE (p:Pattern {id: $id})
                SET p.slug = $slug,
                    p.title = $title,
                    p.summary = $summary,
                    p.content = $content,
                    p.domains = $domains,
                    p.categories = $categories,
                    p.confidence = $confidence,
                    p.source_url = $source_url,
                    p.created_at = $created_at,
                    p.updated_at = $updated_at,
                    p.created_by = $created_by
            """, parameters={
                'id': pattern_id,
                'slug': slug,
                'title': title,
                'summary': summary,
                'content': body[:10000],  # Truncate very long content
                'domains': domains,
                'categories': categories,
                'confidence': 0.8,
                'source_url': source_url,
                'created_at': created,
                'updated_at': modified,
                'created_by': created_by
            })
            
            loaded += 1
            
        except Exception as e:
            print(f"  ✗ Error loading {filepath.name}: {e}")
            errors += 1
    
    print(f"\n✓ Loaded {loaded} patterns ({errors} errors)")
    return loaded


def verify_load() -> None:
    """Verify patterns were loaded correctly."""
    db, conn = get_connection()
    
    # Count patterns
    result = conn.execute("MATCH (p:Pattern) RETURN count(p) AS count")
    count = result.get_next()[0]
    print(f"Total patterns in database: {count}")
    
    # Sample pattern
    result = conn.execute("MATCH (p:Pattern) RETURN p.title, p.domains, p.categories LIMIT 5")
    print("\nSample patterns:")
    while result.has_next():
        row = result.get_next()
        print(f"  - {row[0]} | domains: {row[1]} | categories: {row[2]}")


if __name__ == "__main__":
    load_patterns()
    verify_load()
