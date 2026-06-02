#!/usr/bin/env python3
"""
Fix ALL 181 Dutch AI Tools articles: add related links automagically.

Strategy:
1. Group articles by category
2. Within each category, match by keyword overlap (title words, featuredTool)
3. Also cross-link comparison articles ('-vs-') to relevant niche articles
4. Each article gets 2-3 related slugs that don't include itself
"""

import os, re, json
from collections import defaultdict

ARTICLES_DIR = "src/content/articles"
OUT_DIR = ARTICLES_DIR  # in-place

STOPWORDS = {
    'beste', 'ai', 'tools', 'voor', 'van', 'in', 'de', 'het', 'en', '2026',
    'top', 'vergeleken', 'deze', 'die', 'met', 'een', 'op', 'tot', 'bij',
    'aan', 'te', 'al', 'maar', 'of', 'ook', 'welke', 'vs', 'dan', 'niet',
    'is', 'zijn', 'nog', 'meer', 'zich', 'uit', 'naar', 'over', 'door',
    'dat', 'dit', 'kan', 'wordt', 'hebben', 'hier', 'nederlands', 'nederlandse',
    'markt', 'onder', 'na', 'want', 'wie', 'waarom', 'hoe', 'wat', 'elke',
    'alle', 'onze', 'meeste', 'meest', 'zijn', 'vooral', 'grootste', 'nieuwe',
    'markt', 'weer', 'toch', 'nooit', 'altijd', 'soms', 'vaak', 'heel',
    'beter', 'goed', 'snel', 'echt', 'net', 'pas', 'zelfs', 'wel', 'nog',
    'dan', 'nog', 'al', 'er', 'om', 'bij', 'naar', 'op', 'af', 'uit',
    'door', 'over', 'onder', 'langs', 'tegen', 'zonder', 'binnen', 'buiten',
}

def extract_keywords_from_title(title):
    """Extract meaningful keywords from article title."""
    title = title.lower().strip("'\"")
    words = re.findall(r'[a-z0-9]+', title)
    return set(w for w in words if w not in STOPWORDS and len(w) > 2)

def extract_tool_names(tools_section):
    """Extract tool names from tools list in frontmatter."""
    names = set()
    for match in re.finditer(r'^\s*-\s*name:\s*(.+)', tools_section, re.MULTILINE):
        name = match.group(1).strip().strip("'\"").lower()
        names.add(name)
    return names

def read_article(slug):
    """Read an article and return its frontmatter fields."""
    path = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(path) as f:
        content = f.read()

    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None

    fm = m.group(1)

    title_m = re.search(r'^title:\s*(.+?)$', fm, re.MULTILINE)
    title = title_m.group(1).strip().strip("'\"") if title_m else slug

    cat_m = re.search(r'^category:\s*(\S+)', fm, re.MULTILINE)
    cat = cat_m.group(1) if cat_m else 'unknown'

    ft_m = re.search(r'^featuredTool:\s*(.+?)$', fm, re.MULTILINE)
    ft = ft_m.group(1).strip().strip("'\"") .lower() if ft_m else ''

    # Tools section
    tools_match = re.search(r'^tools:\n(.*?)(?:\n\w|$)', content, re.DOTALL)
    tool_names = extract_tool_names(tools_match.group(1)) if tools_match else set()
    if ft:
        tool_names.add(ft)

    existing_related = re.search(r'^related:\s*\[(.*?)\]', fm, re.MULTILINE)
    has_related = existing_related is not None and existing_related.group(1).strip()

    is_comparison = '-vs-' in slug or '-versus-' in slug

    return {
        'slug': slug,
        'title': title,
        'category': cat,
        'keywords': extract_keywords_from_title(title),
        'tool_names': tool_names,
        'is_comparison': is_comparison,
        'has_related': bool(has_related),
    }

def score_match(a, b):
    """
    Score how relevant article B is as a related link for article A.
    Higher = more relevant.
    """
    score = 0

    # Same category bonus
    if a['category'] == b['category']:
        score += 5

    # Keyword overlap
    overlap = a['keywords'] & b['keywords']
    score += len(overlap) * 3

    # Tool name matches
    tool_overlap = a['tool_names'] & b['tool_names']
    score += len(tool_overlap) * 4

    # Comparison vs regular: cross-link them
    if a['is_comparison'] != b['is_comparison']:
        score += 2  # good to mix comparison and regular articles

    # Featured tool appears in other article's title/tools
    for ft in a['tool_names']:
        if ft in b['keywords']:
            score += 3

    return score


def main():
    # Load all articles
    all_slugs = sorted(f.replace('.md', '') for f in os.listdir(ARTICLES_DIR) if f.endswith('.md'))
    print(f"Total articles: {len(all_slugs)}")

    articles = {}
    for slug in all_slugs:
        data = read_article(slug)
        if data:
            articles[slug] = data

    print(f"Parsed: {len(articles)} articles")

    # Count before
    before_empty = sum(1 for a in articles.values() if not a['has_related'])
    print(f"Articles with empty related before: {before_empty}")

    # For each article, pick best related links
    modified = 0
    for slug, article in articles.items():
        if article['has_related']:
            continue  # skip already-filled

        # Score all other articles
        scored = []
        for other_slug, other in articles.items():
            if other_slug == slug:
                continue
            score = score_match(article, other)
            if score > 0:
                scored.append((score, other_slug))

        # Sort by score descending, take top 3
        scored.sort(key=lambda x: -x[0])
        best = [s[1] for s in scored[:3]]

        if not best:
            # Fallback: pick random articles from same category
            same_cat = [s for s in all_slugs if s != slug
                        and articles.get(s, {}).get('category') == article['category']]
            best = same_cat[:3]

        # Format: [slug1, slug2, slug3]
        related_str = "\n" + " " * 2 + "[" + ", ".join(f"\"{s}\"" for s in best) + "]"

        # Read file and replace
        path = os.path.join(ARTICLES_DIR, f"{slug}.md")
        with open(path) as f:
            content = f.read()

        # Find related line and replace
        new_content = re.sub(
            r'^related:\s*\[.*?\]',
            f'related:{related_str}',
            content,
            count=1,
            flags=re.MULTILINE
        )

        with open(path, 'w') as f:
            f.write(new_content)

        modified += 1

        if modified <= 10:
            print(f"  {slug}: → [{', '.join(best)}] (score={scored[0][0] if scored else 0})")

    print(f"\nModified: {modified} articles")
    print(f"Remaining empty: {sum(1 for a in articles.values() if not a['has_related'])}")

    # Summary by category
    cat_mods = defaultdict(int)
    for slug, article in articles.items():
        for other_slug, other in articles.items():
            if other_slug == slug:
                continue
            s = score_match(article, other)
            if s > 0:
                cat_mods[article['category']] += 1

    print("\nRelated link opportunities by category:")
    for cat, count in sorted(cat_mods.items(), key=lambda x: -x[1]):
        articles_in_cat = sum(1 for a in articles.values() if a['category'] == cat)
        print(f"  {cat}: {articles_in_cat} articles, {count} possible links")

if __name__ == "__main__":
    main()