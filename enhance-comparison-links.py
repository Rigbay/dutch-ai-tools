#!/usr/bin/env python3
"""Enhance internal linking: add links from regular articles to comparison articles.

Strategy: match articles to their most relevant comparison articles by category
and keyword overlap, then add contextual link suggestions.
"""

import os
import re
import random

ARTICLES_DIR = "src/content/articles"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get all articles
all_files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.md')]
comparison_slugs = [f.replace('.md', '') for f in all_files if '-vs-' in f or '-versus-' in f]
regular_slugs = [f.replace('.md', '') for f in all_files if not ('-vs-' in f or '-versus-' in f)]

# Category → comparison articles mapping
category_comparisons = {}
for comp in comparison_slugs:
    path = os.path.join(ARTICLES_DIR, f"{comp}.md")
    with open(path) as f:
        content = f.read()
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    cat = cat_match.group(1) if cat_match else 'unknown'
    category_comparisons.setdefault(cat, []).append(comp)

# Add to broader categories
category_comparisons.setdefault('business', []).extend(category_comparisons.get('business', []))
category_comparisons.setdefault('marketing', []).extend(category_comparisons.get('marketing', []))
category_comparisons.setdefault('productiviteit', []).extend(category_comparisons.get('productiviteit', []))
category_comparisons.setdefault('creatie', []).extend(category_comparisons.get('creatie', []))
category_comparisons.setdefault('development', []).extend(category_comparisons.get('development', []))

# Link templates in Dutch (contextual, not keyword-stuffed)
templates = [
    "Lees ook onze uitgebreide vergelijking: [{title}](/{slug}/).",
    "Benieuwd hoe de tools zich tot elkaar verhouden? Bekijk [{title}](/{slug}/).",
    "Zie ook onze directe vergelijking: [{title}](/{slug}/).",
    "Wil je weten welke het beste is? Lees [{title}](/{slug}/).",
    "Twijfel je tussen opties? Vergelijk ze in [{title}](/{slug}/).",
    "Verdiep je in de verschillen: [{title}](/{slug}/).",
]

links_added = 0
modified = 0

for slug in regular_slugs:
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path) as f:
        content = f.read()

    # Get category
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    cat = cat_match.group(1) if cat_match else None

    # Find existing links to avoid duplicates
    existing_links = set(re.findall(r'\(/([^)]+)/\)', content))

    # Get candidates: same-category comparisons not already linked
    candidates = []
    if cat:
        candidates = [c for c in category_comparisons.get(cat, []) if c not in existing_links]

    # Also add cross-category popular ones
    popular = ['chatgpt-vs-gemini-vs-claude-nederlands-2026', 'perplexity-vs-chatgpt-vs-claude-2026',
               'midjourney-vs-dall-e-3-vs-stable-diffusion-2026', 'zapier-central-vs-make-ai-vs-relevance-ai-2026']
    for p in popular:
        if p not in existing_links and p not in candidates:
            candidates.append(p)

    if not candidates:
        continue

    # Pick 2-3 candidates
    chosen = random.sample(candidates, min(3, len(candidates)))

    # Find the FAQ section or the last paragraph to append links after
    faq_match = re.search(r'(^## FAQ.*?)(^## |\Z)', content, re.MULTILINE | re.DOTALL)
    if faq_match:
        # Insert before FAQ
        faq_pos = faq_match.start()
        lines_before = content[:faq_pos].rstrip()
        links_text = ""
        for c in chosen:
            c_path = os.path.join(ARTICLES_DIR, f"{c}.md")
            with open(c_path) as f:
                c_content = f.read()
            title_match = re.search(r"^title:\s*'([^']+)'", c_content, re.MULTILINE)
            short_title = title_match.group(1) if title_match else c
            # Shorten title for link text
            if ':' in short_title:
                short_title = short_title.split(':')[0].strip()
            template = random.choice(templates)
            links_text += f"\n\n{template.format(title=short_title, slug=c)}"

        before = content[:faq_pos].rstrip()
        after = content[faq_pos:]
        content = before + links_text + "\n\n" + after
        links_added += len(chosen)
        modified += 1

        with open(path, 'w') as f:
            f.write(content)
        print(f"  ✓ {slug} → {len(chosen)} links: {', '.join(chosen[:2])}")

print(f"\n✅ Enhanced internal linking: {links_added} links in {modified} articles")
