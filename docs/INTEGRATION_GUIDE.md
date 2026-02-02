# Context Engine Integration Guide

This guide explains how to integrate the Commons OS Context Engine with:
1. The Jekyll website (pattern discovery)
2. Commons Suite CustomGPTs
3. Direct API consumers

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Commons OS Ecosystem                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Jekyll     │    │  CustomGPTs  │    │  External Apps   │  │
│  │   Website    │    │  (ChatGPT)   │    │  (Lighthouse)    │  │
│  └──────┬───────┘    └──────┬───────┘    └────────┬─────────┘  │
│         │                   │                      │            │
│         └───────────────────┼──────────────────────┘            │
│                             │                                    │
│                             ▼                                    │
│              ┌──────────────────────────────┐                   │
│              │   Context Engine API         │                   │
│              │   /constellations            │                   │
│              │   /patterns/{id}/related     │                   │
│              │   /archetypes, /stages       │                   │
│              └──────────────┬───────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│              ┌──────────────────────────────┐                   │
│              │   Kuzu Graph Database        │                   │
│              │   12,128 relationships       │                   │
│              │   1,279 patterns             │                   │
│              └──────────────────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Graph Schema

### Nodes
- **Pattern** (1,279): Organizational patterns with title, summary, content
- **Archetype** (25): Organizational types (Startup, Enterprise, City, etc.)
- **Stage** (10): Journey stages (Ideation → Exit/Succession)
- **Domain** (27): Industry sectors (Technology, Finance, Healthcare, etc.)

### Relationships
- **SUITED_FOR** (4,178): Pattern → Archetype (with strength, rationale)
- **APPLIES_AT** (3,624): Pattern → Stage (with importance, rationale)
- **RELEVANT_FOR** (3,756): Pattern → Domain (with specificity, rationale)
- **ENABLES** (365): Pattern → Pattern
- **REQUIRES** (99): Pattern → Pattern
- **TENSIONS_WITH** (106): Pattern → Pattern

## Integration Options

### Option 1: Jekyll Website Integration

Add a context-aware pattern discovery widget to the Jekyll site.

**JavaScript Example:**
```javascript
// Pattern Discovery Widget
async function discoverPatterns(archetype, stage, domain) {
  const params = new URLSearchParams({
    archetype,
    ...(stage && { stage }),
    ...(domain && { domain }),
    limit: 20
  });
  
  const response = await fetch(
    `https://context-engine.commonsos.org/api/v1/constellations?${params}`
  );
  const data = await response.json();
  
  return data.patterns.map(p => ({
    title: p.title,
    score: p.score,
    url: `/patterns/${slugify(p.title)}`
  }));
}

// Usage
const patterns = await discoverPatterns('Startup', 'Validation', 'Finance');
```

**Jekyll Include (_includes/pattern-discovery.html):**
```html
<div id="pattern-discovery">
  <h3>Find Patterns For Your Context</h3>
  
  <select id="archetype-select">
    <option value="">Select your organization type...</option>
    <option value="Startup">Startup</option>
    <option value="Enterprise">Enterprise</option>
    <option value="City">City</option>
    <!-- etc -->
  </select>
  
  <select id="stage-select">
    <option value="">Select your stage...</option>
    <option value="Ideation">Ideation</option>
    <option value="Validation">Validation</option>
    <!-- etc -->
  </select>
  
  <select id="domain-select">
    <option value="">Select your domain...</option>
    <option value="Technology">Technology</option>
    <option value="Finance">Finance</option>
    <!-- etc -->
  </select>
  
  <button onclick="findPatterns()">Discover Patterns</button>
  
  <div id="results"></div>
</div>

<script>
async function findPatterns() {
  const archetype = document.getElementById('archetype-select').value;
  const stage = document.getElementById('stage-select').value;
  const domain = document.getElementById('domain-select').value;
  
  if (!archetype) {
    alert('Please select an organization type');
    return;
  }
  
  const patterns = await discoverPatterns(archetype, stage, domain);
  
  const html = patterns.map(p => `
    <div class="pattern-card">
      <a href="${p.url}">${p.title}</a>
      <span class="score">${(p.score * 100).toFixed(0)}% match</span>
    </div>
  `).join('');
  
  document.getElementById('results').innerHTML = html;
}
</script>
```

### Option 2: CustomGPT Integration

Create a CustomGPT Action using the OpenAPI spec.

**Steps:**
1. Go to ChatGPT → My GPTs → Create/Edit
2. Add Action → Import from URL or paste OpenAPI spec
3. Use the spec from `docs/openapi-customgpt.yaml`

**CustomGPT System Prompt:**
```
You are the Commons OS Pattern Navigator. You help users discover organizational patterns from the Commons OS library based on their context.

When a user describes their situation, use the Context Engine API to find relevant patterns:

1. Identify their archetype (Startup, Enterprise, City, Cooperative, etc.)
2. Identify their stage (Ideation, Validation, Growth, Transformation, etc.)
3. Identify their domain (Technology, Finance, Healthcare, Governance, etc.)
4. Call getPatternConstellation with these parameters
5. Present the top patterns with brief explanations

Example interaction:
User: "I'm building a FinTech startup and trying to validate our idea"
→ Call: getPatternConstellation(archetype="Startup", stage="Validation", domain="Finance")
→ Present: Business Model Canvas, Lean Startup, Customer Discovery, etc.

Always explain WHY each pattern is relevant to their specific context.
```

### Option 3: Lighthouse Engine Integration

For programmatic integration with the Lighthouse Engine:

```python
import requests

class ContextEngine:
    def __init__(self, base_url="https://context-engine.commonsos.org/api/v1"):
        self.base_url = base_url
    
    def get_constellation(self, archetype, stage=None, domain=None, limit=50):
        """Get patterns for a specific organizational context."""
        params = {
            "archetype": archetype,
            "limit": limit
        }
        if stage:
            params["stage"] = stage
        if domain:
            params["domain"] = domain
        
        response = requests.get(f"{self.base_url}/constellations", params=params)
        return response.json()
    
    def get_related(self, pattern_title, limit=20):
        """Get patterns related to a specific pattern."""
        response = requests.get(
            f"{self.base_url}/patterns/{pattern_title}/related",
            params={"limit": limit}
        )
        return response.json()

# Usage
engine = ContextEngine()

# Find patterns for a startup in validation
patterns = engine.get_constellation(
    archetype="Startup",
    stage="Validation",
    domain="Technology"
)

# Find patterns related to Lean Startup
related = engine.get_related("Lean Startup (Ries)")
```

## Deployment Options

### Option A: Static Export (Recommended for Jekyll)
Export constellation data as JSON files during build:

```python
# scripts/export_constellations.py
import json
from itertools import product

archetypes = ["Startup", "Enterprise", "City", ...]
stages = ["Ideation", "Validation", "Growth", ...]
domains = ["Technology", "Finance", "Healthcare", ...]

for arch in archetypes:
    data = get_constellation(arch)
    with open(f"_data/constellations/{arch.lower()}.json", "w") as f:
        json.dump(data, f)
```

Then access in Jekyll:
```liquid
{% assign patterns = site.data.constellations.startup.patterns %}
```

### Option B: Serverless Function
Deploy the API as a serverless function (Vercel, Netlify, AWS Lambda):

```python
# api/constellations.py (Vercel)
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query params and return constellation
        ...
```

### Option C: Self-Hosted API
Run the FastAPI server on your infrastructure:

```bash
# Docker
docker build -t context-engine .
docker run -p 8000:8000 context-engine

# Or direct
uvicorn src.api.constellation_api:app --host 0.0.0.0 --port 8000
```

## API Reference

### GET /constellations
Query patterns by organizational context.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| archetype | string | Yes | Organization type |
| stage | string | No | Journey stage |
| domain | string | No | Industry domain |
| min_strength | float | No | Minimum fit (default: 0.5) |
| limit | int | No | Max results (default: 50) |

**Example:**
```
GET /constellations?archetype=Startup&stage=Validation&domain=Finance&limit=10
```

### GET /patterns/{title}/related
Get patterns related to a specific pattern.

**Example:**
```
GET /patterns/Lean%20Startup%20(Ries)/related
```

### GET /archetypes
List all archetypes with pattern counts.

### GET /stages
List all journey stages with pattern counts.

### GET /domains
List all domains with pattern counts.

## Next Steps

1. **Deploy API**: Choose deployment option and set up hosting
2. **Add to Jekyll**: Integrate pattern discovery widget
3. **Create CustomGPT**: Import OpenAPI spec and configure
4. **Connect Lighthouse**: Use Python client for programmatic access
5. **Monitor Usage**: Track which constellations are most queried
