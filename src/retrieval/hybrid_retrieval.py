#!/usr/bin/env python3
"""
Hybrid Retrieval Pipeline for Context Engine

Combines vector similarity search with graph traversal to provide
context-aware pattern recommendations.

Author: higgerix
Date: 2026-02-02
"""

import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.init_kuzu import get_connection

DATA_DIR = Path(__file__).parent.parent.parent / "data"


class HybridRetriever:
    """Hybrid retrieval combining vector search and graph traversal."""
    
    def __init__(self):
        self.db, self.conn = get_connection()
    
    def graph_neighbors(self, pattern_id: str) -> list[dict]:
        """Get related patterns via graph traversal."""
        results = []
        
        for rel_type, direction in [
            ('ENABLES', 'out'), ('ENABLES', 'in'),
            ('REQUIRES', 'out'), ('REQUIRES', 'in'),
            ('TENSIONS_WITH', 'both')
        ]:
            try:
                if direction == 'out':
                    query = f'MATCH (p:Pattern {{id: "{pattern_id}"}})-[r:{rel_type}]->(t:Pattern) RETURN t.id, t.title, r.strength'
                    rel_label = rel_type.lower()
                elif direction == 'in':
                    query = f'MATCH (s:Pattern)-[r:{rel_type}]->(p:Pattern {{id: "{pattern_id}"}}) RETURN s.id, s.title, r.strength'
                    rel_label = f'{rel_type.lower()}_by'
                else:
                    query = f'MATCH (p:Pattern {{id: "{pattern_id}"}})-[r:{rel_type}]-(t:Pattern) RETURN t.id, t.title, 0.5'
                    rel_label = rel_type.lower()
                
                result = self.conn.execute(query)
                while result.has_next():
                    row = result.get_next()
                    results.append({
                        'pattern_id': row[0],
                        'title': row[1],
                        'strength': row[2] or 0.5,
                        'relationship': rel_label
                    })
            except:
                pass
        
        return results
    
    def get_pattern_info(self, pattern_id: str) -> Optional[dict]:
        """Get pattern information from the graph."""
        try:
            result = self.conn.execute(f'MATCH (p:Pattern {{id: "{pattern_id}"}}) RETURN p.title, p.summary')
            if result.has_next():
                row = result.get_next()
                return {'id': pattern_id, 'title': row[0], 'summary': row[1]}
        except:
            pass
        return None
    
    def search_by_title(self, query: str, limit: int = 10) -> list[dict]:
        """Search patterns by title."""
        results = []
        try:
            result = self.conn.execute(f'''
                MATCH (p:Pattern)
                WHERE p.title CONTAINS "{query}"
                RETURN p.id, p.title, p.summary
                LIMIT {limit}
            ''')
            while result.has_next():
                row = result.get_next()
                results.append({'pattern_id': row[0], 'title': row[1], 'summary': row[2]})
        except:
            pass
        return results
    
    def get_relationship_stats(self) -> dict:
        """Get statistics about relationships in the graph."""
        stats = {}
        for rel_type in ['ENABLES', 'REQUIRES', 'TENSIONS_WITH']:
            try:
                result = self.conn.execute(f'MATCH ()-[r:{rel_type}]->() RETURN COUNT(r)')
                if result.has_next():
                    stats[rel_type] = result.get_next()[0]
            except:
                stats[rel_type] = 0
        return stats
    
    def get_most_connected(self, limit: int = 10) -> list[dict]:
        """Get patterns with most relationships."""
        results = []
        try:
            result = self.conn.execute(f'''
                MATCH (p:Pattern)-[r]-()
                RETURN p.id, p.title, COUNT(r) as connections
                ORDER BY connections DESC
                LIMIT {limit}
            ''')
            while result.has_next():
                row = result.get_next()
                results.append({'pattern_id': row[0], 'title': row[1], 'connections': row[2]})
        except:
            pass
        return results


def demo():
    """Demonstrate the hybrid retrieval system."""
    print("=" * 60)
    print("HYBRID RETRIEVAL DEMO")
    print("=" * 60)
    
    retriever = HybridRetriever()
    
    # Stats
    print("\n1. Relationship Statistics")
    print("-" * 40)
    stats = retriever.get_relationship_stats()
    for rel, count in stats.items():
        print(f"  {rel}: {count}")
    
    # Most connected
    print("\n2. Most Connected Patterns")
    print("-" * 40)
    connected = retriever.get_most_connected(10)
    for p in connected:
        print(f"  {p['connections']:3} connections: {p['title']}")
    
    # Search example
    print("\n3. Search for 'Lean'")
    print("-" * 40)
    results = retriever.search_by_title("Lean", 5)
    for r in results:
        print(f"  {r['title']}")
        neighbors = retriever.graph_neighbors(r['pattern_id'])
        if neighbors:
            print(f"    -> {len(neighbors)} related patterns")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
