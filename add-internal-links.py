#!/usr/bin/env python3
"""Add internal cross-links between Dutch AI Tools articles."""

import os, re, random

ARTICLES_DIR = "/tmp/dutch-ai-tools/src/content/articles"

# Read all article slugs and metadata
articles = []
for fn in sorted(os.listdir(ARTICLES_DIR)):
    if not fn.endswith('.md'):
        continue
    path = os.path.join(ARTICLES_DIR, fn)
    with open(path) as f:
        content = f.read()
    
    # Extract slug and title
    slug_match = re.search(r'^slug:\s*(.+?)\s*$', content, re.MULTILINE)
    title_match = re.search(r"^title:\s*'?(.+?)'?\s*$", content, re.MULTILINE)
    cat_match = re.search(r'^category:\s*(.+?)\s*$', content, re.MULTILINE)
    
    if slug_match and title_match:
        slug = slug_match.group(1).strip()
        title = title_match.group(1).strip().rstrip("'").lstrip("'")
        category = cat_match.group(1).strip() if cat_match else ""
        articles.append({
            'slug': slug,
            'title': title,
            'category': category,
            'path': path
        })

print(f"Found {len(articles)} articles")

# Build category index
by_category = {}
for a in articles:
    by_category.setdefault(a['category'], []).append(a)

# Add internal links to each article
linked = 0
for article in articles:
    path = article['path']
    with open(path) as f:
        content = f.read()
    
    # Skip if already has "Gerelateerde artikelen" section
    if "Gerelateerde artikelen" in content or "Lees ook" in content:
        continue
    
    # Find related articles (same category preferred, then random)
    same_cat = [a for a in by_category.get(article['category'], []) if a['slug'] != article['slug']]
    other = [a for a in articles if a['slug'] != article['slug'] and a not in same_cat]
    
    picks = same_cat[:2]
    if len(picks) < 3:
        picks += other[:3 - len(picks)]
    
    if not picks:
        continue
    
    # Build the "Lees ook" section
    links = "\n".join([
        f"- [{p['title']}](/{p['slug']}/)"
        for p in picks[:3]
    ])
    
    section = f"""
---
## Lees ook

Verdiep je verder in AI tools:

{links}
"""
    
    # Insert before any existing "---" at end of file, or at the end
    content = content.rstrip() + section
    
    with open(path, 'w') as f:
        f.write(content)
    
    linked += 1

print(f"Added internal links to {linked} articles")
