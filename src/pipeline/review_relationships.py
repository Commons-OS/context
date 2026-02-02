#!/usr/bin/env python3
"""
Human Review Workflow for Relationship Approval

This script provides a CLI interface for reviewing AI-discovered relationships.
Reviewers can approve, reject, or modify relationships before they're loaded
into the graph database.

Features:
- Interactive CLI for reviewing relationships one by one
- Batch review mode for bulk operations
- Export approved relationships for loading into Kuzu
- Statistics and progress tracking

Author: higgerix
Date: 2026-02-02
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from db.init_kuzu import get_connection

# Configuration
DATA_DIR = Path(__file__).parent.parent.parent / "data"
STAGING_FILE = DATA_DIR / "relationship_staging.json"
APPROVED_FILE = DATA_DIR / "relationships_approved.json"


def load_staging() -> dict:
    """Load the staging file."""
    if not STAGING_FILE.exists():
        return {'relationships': []}
    
    with open(STAGING_FILE) as f:
        return json.load(f)


def save_staging(data: dict) -> None:
    """Save the staging file."""
    data['last_updated'] = datetime.now().isoformat()
    with open(STAGING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_approved() -> list[dict]:
    """Load approved relationships."""
    if not APPROVED_FILE.exists():
        return []
    
    with open(APPROVED_FILE) as f:
        return json.load(f).get('relationships', [])


def save_approved(relationships: list[dict]) -> None:
    """Save approved relationships."""
    with open(APPROVED_FILE, 'w') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'total': len(relationships),
            'relationships': relationships
        }, f, indent=2)


def get_pattern_title(pattern_id: str) -> str:
    """Look up pattern title from database."""
    try:
        db, conn = get_connection()
        result = conn.execute(f"""
            MATCH (p:Pattern {{id: '{pattern_id}'}})
            RETURN p.title
        """)
        if result.has_next():
            return result.get_next()[0]
    except:
        pass
    return pattern_id


def display_relationship(rel: dict, index: int, total: int) -> None:
    """Display a relationship for review."""
    source_title = get_pattern_title(rel['source_id'])
    target_title = get_pattern_title(rel['target_id'])
    
    print("\n" + "=" * 70)
    print(f"Relationship {index + 1} of {total}")
    print("=" * 70)
    print(f"\n  Source: {source_title}")
    print(f"          ({rel['source_id']})")
    print(f"\n  Target: {target_title}")
    print(f"          ({rel['target_id']})")
    print(f"\n  Type:       {rel['relationship_type']}")
    print(f"  Confidence: {rel.get('confidence', 'N/A')}")
    print(f"\n  Evidence:")
    print(f"    {rel.get('evidence', 'No evidence provided')}")
    print(f"\n  Discovered: {rel.get('discovered_at', 'N/A')}")
    print(f"  By:         {rel.get('discovered_by', 'N/A')}")
    print()


def interactive_review() -> None:
    """Interactive CLI for reviewing relationships one by one."""
    data = load_staging()
    relationships = data.get('relationships', [])
    
    # Filter to pending only
    pending = [r for r in relationships if r.get('status') == 'pending_review']
    
    if not pending:
        print("No relationships pending review.")
        return
    
    print(f"\n{len(pending)} relationships pending review.")
    print("\nCommands:")
    print("  a = approve")
    print("  r = reject")
    print("  s = skip (review later)")
    print("  e = edit type (change relationship type)")
    print("  q = quit")
    print()
    
    approved = load_approved()
    approved_count = 0
    rejected_count = 0
    
    for i, rel in enumerate(pending):
        display_relationship(rel, i, len(pending))
        
        while True:
            choice = input("Your decision [a/r/s/e/q]: ").strip().lower()
            
            if choice == 'a':
                rel['status'] = 'approved'
                rel['reviewed_at'] = datetime.now().isoformat()
                rel['reviewed_by'] = 'human'
                approved.append(rel)
                approved_count += 1
                print("✓ Approved")
                break
            elif choice == 'r':
                rel['status'] = 'rejected'
                rel['reviewed_at'] = datetime.now().isoformat()
                rel['reviewed_by'] = 'human'
                rejected_count += 1
                print("✗ Rejected")
                break
            elif choice == 's':
                print("→ Skipped")
                break
            elif choice == 'e':
                print("\nRelationship types:")
                print("  1 = ENABLES")
                print("  2 = REQUIRES")
                print("  3 = TENSIONS_WITH")
                type_choice = input("New type [1/2/3]: ").strip()
                type_map = {'1': 'ENABLES', '2': 'REQUIRES', '3': 'TENSIONS_WITH'}
                if type_choice in type_map:
                    rel['relationship_type'] = type_map[type_choice]
                    rel['modified_by'] = 'human'
                    print(f"Type changed to {type_map[type_choice]}")
            elif choice == 'q':
                print("\nSaving progress...")
                save_staging(data)
                save_approved(approved)
                print(f"\nSession summary:")
                print(f"  Approved: {approved_count}")
                print(f"  Rejected: {rejected_count}")
                return
            else:
                print("Invalid choice. Use a/r/s/e/q")
    
    # Save at the end
    save_staging(data)
    save_approved(approved)
    print(f"\nReview complete!")
    print(f"  Approved: {approved_count}")
    print(f"  Rejected: {rejected_count}")


def batch_approve_by_confidence(min_confidence: float = 0.85) -> None:
    """Batch approve all relationships above a confidence threshold."""
    data = load_staging()
    relationships = data.get('relationships', [])
    
    pending = [r for r in relationships if r.get('status') == 'pending_review']
    high_confidence = [r for r in pending if r.get('confidence', 0) >= min_confidence]
    
    print(f"\n{len(high_confidence)} relationships with confidence >= {min_confidence}")
    
    if not high_confidence:
        print("No relationships meet the threshold.")
        return
    
    confirm = input(f"Approve all {len(high_confidence)} relationships? [y/N]: ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    approved = load_approved()
    
    for rel in high_confidence:
        rel['status'] = 'approved'
        rel['reviewed_at'] = datetime.now().isoformat()
        rel['reviewed_by'] = 'batch_confidence'
        approved.append(rel)
    
    save_staging(data)
    save_approved(approved)
    
    print(f"✓ Approved {len(high_confidence)} relationships")


def batch_approve_by_type(rel_type: str) -> None:
    """Batch approve all relationships of a specific type."""
    data = load_staging()
    relationships = data.get('relationships', [])
    
    pending = [r for r in relationships if r.get('status') == 'pending_review']
    matching = [r for r in pending if r.get('relationship_type') == rel_type]
    
    print(f"\n{len(matching)} pending {rel_type} relationships")
    
    if not matching:
        print("No matching relationships.")
        return
    
    # Show sample
    print("\nSample (first 5):")
    for rel in matching[:5]:
        source = get_pattern_title(rel['source_id'])
        target = get_pattern_title(rel['target_id'])
        print(f"  {source[:30]:30} → {target[:30]:30} ({rel.get('confidence', 'N/A')})")
    
    confirm = input(f"\nApprove all {len(matching)} {rel_type} relationships? [y/N]: ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    approved = load_approved()
    
    for rel in matching:
        rel['status'] = 'approved'
        rel['reviewed_at'] = datetime.now().isoformat()
        rel['reviewed_by'] = f'batch_type_{rel_type.lower()}'
        approved.append(rel)
    
    save_staging(data)
    save_approved(approved)
    
    print(f"✓ Approved {len(matching)} relationships")


def show_statistics() -> None:
    """Show review statistics."""
    data = load_staging()
    relationships = data.get('relationships', [])
    approved = load_approved()
    
    # Count by status
    status_counts = {}
    for r in relationships:
        status = r.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Count by type
    type_counts = {}
    for r in relationships:
        rtype = r.get('relationship_type', 'unknown')
        type_counts[rtype] = type_counts.get(rtype, 0) + 1
    
    # Confidence distribution
    confidences = [r.get('confidence', 0) for r in relationships]
    high_conf = len([c for c in confidences if c >= 0.85])
    med_conf = len([c for c in confidences if 0.7 <= c < 0.85])
    low_conf = len([c for c in confidences if c < 0.7])
    
    print("\n" + "=" * 50)
    print("RELATIONSHIP REVIEW STATISTICS")
    print("=" * 50)
    
    print("\nBy Status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status:20} {count:5}")
    
    print("\nBy Type:")
    for rtype, count in sorted(type_counts.items()):
        print(f"  {rtype:20} {count:5}")
    
    print("\nBy Confidence:")
    print(f"  High (>= 0.85):      {high_conf:5}")
    print(f"  Medium (0.7-0.85):   {med_conf:5}")
    print(f"  Low (< 0.7):         {low_conf:5}")
    
    print(f"\nApproved (ready for graph): {len(approved)}")
    print()


def export_for_kuzu() -> None:
    """Export approved relationships in a format ready for Kuzu loading."""
    approved = load_approved()
    
    if not approved:
        print("No approved relationships to export.")
        return
    
    export_file = DATA_DIR / "relationships_for_kuzu.json"
    
    # Simplify for loading
    export_data = []
    for rel in approved:
        export_data.append({
            'source_id': rel['source_id'],
            'target_id': rel['target_id'],
            'type': rel['relationship_type'],
            'confidence': rel.get('confidence', 0.5),
            'evidence': rel.get('evidence', '')
        })
    
    with open(export_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"✓ Exported {len(export_data)} relationships to {export_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Review AI-discovered relationships")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive review mode")
    parser.add_argument("--batch-confidence", type=float, metavar="MIN", help="Batch approve by confidence threshold")
    parser.add_argument("--batch-type", type=str, metavar="TYPE", help="Batch approve by relationship type")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--export", action="store_true", help="Export approved for Kuzu")
    args = parser.parse_args()
    
    if args.stats:
        show_statistics()
    elif args.interactive:
        interactive_review()
    elif args.batch_confidence:
        batch_approve_by_confidence(args.batch_confidence)
    elif args.batch_type:
        batch_approve_by_type(args.batch_type.upper())
    elif args.export:
        export_for_kuzu()
    else:
        # Default: show stats
        show_statistics()
