#!/usr/bin/env python3
"""Fix dead affiliate links + add missing active codes in Dutch AI Tools articles.

Dead → informational non-affiliate URLs (no tracking):
  - notion.so → https://www.notion.so (no affiliate program exists)
  - copy.ai → https://www.copy.ai (no affiliate program exists)

Missing active codes → add:
  - synthesia.io without ?via=hermes → add it
  - beehiiv.com without ?via=anonymous-operator → add it
  - Notion articles where beehiiv top-level affiliate is missing → add
"""

import re
import os
from pathlib import Path

ARTICLES_DIR = Path("src/content/articles")

# Dead patterns → replacement (strip affiliate param, keep as info)
DEAD_REPLACEMENTS = {
    "notion.so": "https://www.notion.so",  # strip any stray params
    "copy.ai": "https://www.copy.ai",
}

# Missing code patterns
SYNTHESIA_CORRECT = "https://www.synthesia.io?via=hermes"
BEEHIIV_CORRECT = "https://www.beehiiv.com/?via=anonymous-operator"

stats = {
    "notion_fixed": 0,
    "copyai_fixed": 0,
    "synthesia_added": 0,
    "beehiiv_added": 0,
    "files_touched": 0,
}

for md_file in sorted(ARTICLES_DIR.glob("*.md")):
    content = md_file.read_text(encoding="utf-8")
    original = content
    changed = False

    # Fix 1: Handle notion.so affiliate links
    # Pattern: affiliateLink: https://www.notion.so (possibly with params)
    def fix_notion(m):
        stats["notion_fixed"] += 1
        return "affiliateLink: https://www.notion.so"
    content, n = re.subn(
        r'affiliateLink:\s*https?://[^\s]*notion\.so\S*',
        fix_notion,
        content
    )

    # Also fix top-level affiliateLinks list entries
    def fix_notion_top(m):
        stats["notion_fixed"] += 1
        return "- https://www.notion.so"
    content, n2 = re.subn(
        r'-\s*https?://[^\s]*notion\.so\S*',
        fix_notion_top,
        content
    )
    
    if n > 0 or n2 > 0:
        changed = True

    # Fix 2: Handle copy.ai affiliate links  
    def fix_copyai(m):
        stats["copyai_fixed"] += 1
        return "affiliateLink: https://www.copy.ai"
    content, n = re.subn(
        r'affiliateLink:\s*https?://[^\s]*copy\.ai\S*',
        fix_copyai,
        content
    )

    def fix_copyai_top(m):
        stats["copyai_fixed"] += 1
        return "- https://www.copy.ai"
    content, n2 = re.subn(
        r'-\s*https?://[^\s]*copy\.ai\S*',
        fix_copyai_top,
        content
    )

    if n > 0 or n2 > 0:
        changed = True

    # Fix 3: synthesia.io without via=hermes
    def fix_synthesia(m):
        stats["synthesia_added"] += 1
        return f"affiliateLink: {SYNTHESIA_CORRECT}"
    content, n = re.subn(
        r'affiliateLink:\s*https?://[^\s]*synthesia\.io(?!\S*\?via=hermes)\S*',
        fix_synthesia,
        content
    )

    def fix_synthesia_top(m):
        stats["synthesia_added"] += 1
        return f"- {SYNTHESIA_CORRECT}"
    content, n2 = re.subn(
        r'-\s*https?://[^\s]*synthesia\.io(?!\S*\?via=hermes)\S*',
        fix_synthesia_top,
        content
    )

    if n > 0 or n2 > 0:
        changed = True

    # Fix 4: beehiiv.com without via=anonymous-operator
    def fix_beehiiv(m):
        stats["beehiiv_added"] += 1
        return f"affiliateLink: {BEEHIIV_CORRECT}"
    content, n = re.subn(
        r'affiliateLink:\s*https?://[^\s]*beehiiv\.com(?!\S*\?via=anonymous-operator)\S*',
        fix_beehiiv,
        content
    )

    def fix_beehiiv_top(m):
        stats["beehiiv_added"] += 1
        return f"- {BEEHIIV_CORRECT}"
    content, n2 = re.subn(
        r'-\s*https?://[^\s]*beehiiv\.com(?!\S*\?via=anonymous-operator)\S*',
        fix_beehiiv_top,
        content
    )

    if n > 0 or n2 > 0:
        changed = True

    if changed:
        md_file.write_text(content, encoding="utf-8")
        stats["files_touched"] += 1
        print(f"  Fixed: {md_file.name}")

print(f"\n=== SUMMARY ===")
print(f"Files touched: {stats['files_touched']}")
print(f"notion.so links fixed: {stats['notion_fixed']}")
print(f"copy.ai links fixed: {stats['copyai_fixed']}")
print(f"synthesia codes added: {stats['synthesia_added']}")
print(f"beehiiv codes added: {stats['beehiiv_added']}")
