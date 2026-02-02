#!/usr/bin/env python3
"""
Extract archetype, stage, and domain relationships for patterns.
V2: More robust with better error handling and progress tracking.
"""

import os
import sys
import json
import yaml
import time
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openai import OpenAI

# Configuration
PATTERNS_DIR = Path("/home/ubuntu/work/patterns-repo/_patterns")
OUTPUT_DIR = Path("/home/ubuntu/work/context-engine/data/archetype_extractions")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

EXTRACTION_PROMPT = """Analyze this pattern and extract classifications.

PATTERN: {name}
DESCRIPTION: {description}

Return JSON with this structure:
{{
  "archetypes": [{{"name": "Startup", "strength": 0.9, "rationale": "Brief reason"}}],
  "stages": [{{"name": "Validation", "importance": 0.8, "rationale": "Brief reason"}}],
  "domains": [{{"name": "Technology", "specificity": "general", "rationale": "Brief reason"}}]
}}

Archetypes: {archetypes}
Stages: {stages}
Domains: {domains}

Rules:
- Only include where pattern genuinely applies
- strength/importance: 0.9-1.0=core, 0.7-0.9=strong, 0.5-0.7=moderate
- specificity: core/specific/general
- Keep rationales to 1 sentence
- Return ONLY valid JSON"""


def load_pattern(pattern_path: Path) -> Optional[dict]:
    """Load a pattern file."""
    try:
        content = pattern_path.read_text(encoding='utf-8')
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                return {
                    'id': frontmatter.get('id', pattern_path.stem),
                    'name': frontmatter.get('title', pattern_path.stem),
                    'description': frontmatter.get('description', '')[:500],
                    'path': str(pattern_path)
                }
    except Exception as e:
        pass
    return None


def extract_for_pattern(client: OpenAI, pattern: dict) -> dict:
    """Extract classifications for a single pattern."""
    prompt = EXTRACTION_PROMPT.format(
        name=pattern['name'],
        description=pattern['description'],
        archetypes=", ".join(ARCHETYPES),
        stages=", ".join(STAGES),
        domains=", ".join(DOMAINS)
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a pattern analyst. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up JSON
        if result_text.startswith('```'):
            lines = result_text.split('\n')
            result_text = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
        
        result = json.loads(result_text)
        result['pattern_id'] = pattern['id']
        result['pattern_name'] = pattern['name']
        return result
        
    except json.JSONDecodeError as e:
        return {'pattern_id': pattern['id'], 'pattern_name': pattern['name'], 'error': f'JSON: {str(e)[:50]}'}
    except Exception as e:
        return {'pattern_id': pattern['id'], 'pattern_name': pattern['name'], 'error': str(e)[:100]}


# Progress tracking
progress_lock = threading.Lock()
progress_count = 0
total_count = 0


def process_pattern(args):
    """Process a single pattern (for thread pool)."""
    global progress_count
    client, pattern = args
    result = extract_for_pattern(client, pattern)
    
    with progress_lock:
        progress_count += 1
        if progress_count % 20 == 0:
            print(f"Progress: {progress_count}/{total_count} ({100*progress_count/total_count:.1f}%)", flush=True)
    
    return result


def run_extraction(limit: int = None, resume: bool = True, workers: int = 5):
    """Run extraction with parallel processing."""
    global progress_count, total_count
    
    print("=" * 60)
    print("ARCHETYPE EXTRACTION PIPELINE V2")
    print("=" * 60)
    
    # Load patterns
    pattern_files = list(PATTERNS_DIR.glob("*.md"))
    print(f"Found {len(pattern_files)} pattern files")
    
    # Check existing
    existing_file = OUTPUT_DIR / "all_extractions.json"
    existing_ids = set()
    existing_results = []
    
    if resume and existing_file.exists():
        with open(existing_file) as f:
            existing_results = json.load(f)
            existing_ids = {r['pattern_id'] for r in existing_results if 'error' not in r}
        print(f"Found {len(existing_ids)} existing successful extractions")
    
    # Load new patterns
    patterns = []
    for pf in pattern_files:
        pattern = load_pattern(pf)
        if pattern and pattern['id'] not in existing_ids:
            patterns.append(pattern)
    
    if limit:
        patterns = patterns[:limit]
    
    total_count = len(patterns)
    progress_count = 0
    print(f"Processing {total_count} patterns with {workers} workers")
    
    if not patterns:
        print("No new patterns to process")
        return existing_results
    
    # Process with thread pool
    client = OpenAI()
    results = []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_pattern, (client, p)) for p in patterns]
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error: {e}")
    
    # Combine with existing
    all_results = existing_results + results
    
    # Save
    with open(existing_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    
    successful = [r for r in all_results if 'error' not in r]
    errors = [r for r in all_results if 'error' in r]
    
    total_archetypes = sum(len(r.get('archetypes', [])) for r in successful)
    total_stages = sum(len(r.get('stages', [])) for r in successful)
    total_domains = sum(len(r.get('domains', [])) for r in successful)
    
    print(f"Total patterns: {len(all_results)}")
    print(f"Successful: {len(successful)}")
    print(f"Errors: {len(errors)}")
    print(f"Archetype relations: {total_archetypes}")
    print(f"Stage relations: {total_stages}")
    print(f"Domain relations: {total_domains}")
    print(f"TOTAL RELATIONSHIPS: {total_archetypes + total_stages + total_domains}")
    
    return all_results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Limit patterns')
    parser.add_argument('--workers', type=int, default=5, help='Parallel workers')
    parser.add_argument('--no-resume', action='store_true', help='Start fresh')
    args = parser.parse_args()
    
    run_extraction(limit=args.limit, resume=not args.no_resume, workers=args.workers)
