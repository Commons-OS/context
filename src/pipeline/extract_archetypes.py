#!/usr/bin/env python3
"""
Extract archetype, stage, and domain relationships for patterns.

This pipeline analyzes each pattern and determines:
1. Which organizational archetypes it suits (with rationale and strength)
2. Which stages it applies to (with importance score)
3. Which domains it's relevant for (with specificity)

Uses OpenAI API for fast processing, with batching for efficiency.
"""

import os
import sys
import json
import yaml
import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openai import OpenAI

# Configuration
PATTERNS_DIR = Path("/home/ubuntu/work/patterns-repo/_patterns")
OUTPUT_DIR = Path("/home/ubuntu/work/context-engine/data/archetype_extractions")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Archetypes, Stages, Domains (must match Kuzu seed data)
ARCHETYPES = [
    "Individual", "Family", "Team", "Startup", "Scaleup", "SME", "Enterprise",
    "Cooperative", "NGO", "Government", "City", "Village", "Region", "Network", "Ecosystem"
]

STAGES = [
    "Ideation", "Discovery", "Validation", "MVP", "Product-Market Fit",
    "Growth", "Expansion", "Maturity", "Transformation", "Exit/Succession"
]

DOMAINS = [
    "Technology", "Finance", "Healthcare", "Education", "Energy",
    "Manufacturing", "Retail", "Agriculture", "Governance", "Social"
]

EXTRACTION_PROMPT = """Analyze this pattern from Commons OS and extract its multi-dimensional classification.

PATTERN: {name}
DESCRIPTION: {description}
CONTENT SUMMARY: {content_summary}

ORGANIZATIONAL ARCHETYPES (select ALL that apply with strength 0.0-1.0):
{archetypes}

STAGES (select ALL that apply with importance 0.0-1.0):
{stages}

DOMAINS (select ALL that apply):
{domains}

Return a JSON object with this exact structure:
{{
  "archetypes": [
    {{"name": "Startup", "strength": 0.9, "rationale": "Why this pattern suits startups"}}
  ],
  "stages": [
    {{"name": "Validation", "importance": 0.8, "rationale": "Why this pattern matters at validation stage"}}
  ],
  "domains": [
    {{"name": "Technology", "specificity": "general|specific|core", "rationale": "Why relevant"}}
  ]
}}

Rules:
- Include ONLY archetypes/stages/domains where the pattern genuinely applies
- Strength/importance: 0.9-1.0 = core fit, 0.7-0.9 = strong fit, 0.5-0.7 = moderate fit, <0.5 = weak fit
- Specificity: "core" = essential for this domain, "specific" = particularly relevant, "general" = broadly applicable
- Rationale should be 1-2 sentences explaining the fit
- Most patterns will have 3-8 archetypes, 2-5 stages, 1-4 domains
- Be generous but not indiscriminate - we want rich connections

Return ONLY the JSON object, no other text."""


@dataclass
class ArchetypeRelation:
    pattern: str
    archetype: str
    strength: float
    rationale: str


@dataclass
class StageRelation:
    pattern: str
    stage: str
    importance: float
    rationale: str


@dataclass
class DomainRelation:
    pattern: str
    domain: str
    specificity: str
    rationale: str


def load_pattern(pattern_path: Path) -> Optional[dict]:
    """Load a pattern file and extract key information."""
    try:
        content = pattern_path.read_text(encoding='utf-8')
        
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
            else:
                return None
        else:
            return None
        
        # Extract key fields
        name = frontmatter.get('title', pattern_path.stem)
        description = frontmatter.get('description', '')
        
        # Get first 500 chars of body as summary
        content_summary = body[:500] if body else ''
        
        return {
            'id': frontmatter.get('id', pattern_path.stem),
            'name': name,
            'description': description,
            'content_summary': content_summary,
            'path': str(pattern_path)
        }
    except Exception as e:
        print(f"Error loading {pattern_path}: {e}")
        return None


def extract_for_pattern(client: OpenAI, pattern: dict) -> dict:
    """Use LLM to extract archetype/stage/domain relationships."""
    prompt = EXTRACTION_PROMPT.format(
        name=pattern['name'],
        description=pattern['description'],
        content_summary=pattern['content_summary'],
        archetypes=", ".join(ARCHETYPES),
        stages=", ".join(STAGES),
        domains=", ".join(DOMAINS)
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a pattern analyst for Commons OS, a library of organizational patterns. Extract structured classifications accurately."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Parse JSON (handle markdown code blocks)
        if result_text.startswith('```'):
            result_text = result_text.split('```')[1]
            if result_text.startswith('json'):
                result_text = result_text[4:]
        
        result = json.loads(result_text)
        result['pattern_id'] = pattern['id']
        result['pattern_name'] = pattern['name']
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error for {pattern['name']}: {e}")
        return {'pattern_id': pattern['id'], 'pattern_name': pattern['name'], 'error': str(e)}
    except Exception as e:
        print(f"API error for {pattern['name']}: {e}")
        return {'pattern_id': pattern['id'], 'pattern_name': pattern['name'], 'error': str(e)}


def process_batch(patterns: list, batch_num: int, total_batches: int) -> list:
    """Process a batch of patterns with progress tracking."""
    import sys
    client = OpenAI()  # Uses OPENAI_API_KEY from env
    results = []
    
    for i, pattern in enumerate(patterns):
        result = extract_for_pattern(client, pattern)
        results.append(result)
        
        # Progress - print every pattern
        print(f"  [{batch_num}/{total_batches}] {i+1}/{len(patterns)}: {pattern['name'][:40]}...", flush=True)
        sys.stdout.flush()
        
        # Rate limiting
        time.sleep(0.05)
    
    return results


def run_extraction(limit: int = None, resume: bool = True):
    """Run the full extraction pipeline."""
    print("=" * 60)
    print("ARCHETYPE EXTRACTION PIPELINE")
    print("=" * 60)
    
    # Load all patterns
    pattern_files = list(PATTERNS_DIR.glob("*.md"))
    print(f"Found {len(pattern_files)} pattern files")
    
    # Check for existing extractions
    existing_file = OUTPUT_DIR / "all_extractions.json"
    existing_ids = set()
    existing_results = []
    
    if resume and existing_file.exists():
        with open(existing_file) as f:
            existing_results = json.load(f)
            existing_ids = {r['pattern_id'] for r in existing_results if 'error' not in r}
        print(f"Found {len(existing_ids)} existing extractions")
    
    # Load patterns
    patterns = []
    for pf in pattern_files:
        pattern = load_pattern(pf)
        if pattern and pattern['id'] not in existing_ids:
            patterns.append(pattern)
    
    if limit:
        patterns = patterns[:limit]
    
    print(f"Processing {len(patterns)} new patterns")
    
    if not patterns:
        print("No new patterns to process")
        return existing_results
    
    # Process in batches
    batch_size = 50
    batches = [patterns[i:i+batch_size] for i in range(0, len(patterns), batch_size)]
    
    all_results = existing_results.copy()
    
    for batch_num, batch in enumerate(batches, 1):
        print(f"\nProcessing batch {batch_num}/{len(batches)} ({len(batch)} patterns)...")
        batch_results = process_batch(batch, batch_num, len(batches))
        all_results.extend(batch_results)
        
        # Save after each batch
        with open(existing_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"  Saved {len(all_results)} total extractions")
    
    # Summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    
    successful = [r for r in all_results if 'error' not in r]
    errors = [r for r in all_results if 'error' in r]
    
    total_archetypes = sum(len(r.get('archetypes', [])) for r in successful)
    total_stages = sum(len(r.get('stages', [])) for r in successful)
    total_domains = sum(len(r.get('domains', [])) for r in successful)
    
    print(f"Successful extractions: {len(successful)}")
    print(f"Errors: {len(errors)}")
    print(f"Total archetype relations: {total_archetypes}")
    print(f"Total stage relations: {total_stages}")
    print(f"Total domain relations: {total_domains}")
    print(f"TOTAL NEW RELATIONSHIPS: {total_archetypes + total_stages + total_domains}")
    
    return all_results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Limit number of patterns to process')
    parser.add_argument('--no-resume', action='store_true', help='Start fresh, ignore existing')
    args = parser.parse_args()
    
    run_extraction(limit=args.limit, resume=not args.no_resume)
