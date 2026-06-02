#!/usr/bin/env python3
"""
Scrub dead affiliate links from Dutch AI Tools articles.

Based on merchants.json:
- notion: DEAD — replace affiliate.notion.so links with plain notion.so
- copy-ai: DEAD — replace copy.ai affiliate links with plain copy.ai
"""

import os, re

ARTICLES_DIR = "src/content/articles"

REPLACEMENTS = {
    # Notion: remove affiliate parameter, use plain domain
    r'https://affiliate\.notion\.so/\?via=aitoolsnl': 'https://www.notion.so',
    r'affiliate\.notion\.so': 'www.notion.so',
    # Copy ai: remove affiliate refs
    r'https://www\.copy\.ai/\?via=aitoolsnl': 'https://www.copy.ai',
    r'https://copy\.ai\?ref=aitoolsnl': 'https://copy.ai',
}

def scrub_file(path):
    """Apply all replacements to a file. Return True if modified."""
    with open(path) as f:
        content = f.read()
    
    original = content
    
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    notion_files = []
    copyai_files = []
    
    for f in sorted(os.listdir(ARTICLES_DIR)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(ARTICLES_DIR, f)
        with open(path) as fp:
            content = fp.read()
        
        if 'affiliate.notion.so' in content or 'notion.so/?via' in content:
            notion_files.append(f)
        if 'copy.ai' in content and ('ref=aitoolsnl' in content or 'via=aitoolsnl' in content):
            copyai_files.append(f)
    
    print(f"Found {len(notion_files)} articles with dead Notion links")
    print(f"Found {len(copyai_files)} articles with dead Copy.ai links")
    
    modified = 0
    for f_list, label in [(notion_files, "Notion"), (copyai_files, "Copy.ai")]:
        for f in f_list:
            path = os.path.join(ARTICLES_DIR, f)
            if scrub_file(path):
                modified += 1
                print(f"  Fixed {label}: {f}")
    
    print(f"\nTotal modified: {modified}")

if __name__ == "__main__":
    main()