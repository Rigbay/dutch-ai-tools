#!/usr/bin/env python3
"""
Fix 5 Dutch AI Tools comparison articles where all tool affiliateLinks
point to notion.so (AI generation placeholder bug).

Strategy: Replace with correct tool homepage URLs. No affiliate revenue 
lost because notion.so program is dead. This is a site quality fix.
"""

import os
import re
import sys

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'src', 'content', 'articles')

# Per-article tool-to-correct-URL mapping
# Each entry: slug -> { tool_name: correct_affiliate_url }
CORRECTIONS = {
    'airtable-vs-google-sheets-vs-notion-databases-2026': {
        'Airtable': 'https://airtable.com',
        'Google Sheets': 'https://workspace.google.com/products/sheets/',
        'Notion Databases': 'https://www.notion.so',
    },
    'figma-vs-sketch-vs-adobe-xd-2026': {
        'Figma': 'https://www.figma.com',
        'Adobe XD': 'https://www.adobe.com/products/xd.html',
        'Sketch': 'https://www.sketch.com',
    },
    'shopify-vs-woocommerce-vs-wix-ecommerce-2026': {
        'Shopify': 'https://www.shopify.com',
        'WooCommerce': 'https://woocommerce.com',
        'Wix': 'https://www.wix.com',
    },
    'stripe-vs-mollie-vs-adyen-2026': {
        'Stripe': 'https://stripe.com',
        'Mollie': 'https://www.mollie.com',
        'Adyen': 'https://www.adyen.com',
    },
    'zoom-vs-google-meet-vs-teams-2026': {
        'Zoom': 'https://zoom.us',
        'Google Meet': 'https://meet.google.com',
        'Microsoft Teams': 'https://www.microsoft.com/microsoft-teams/group-chat-software',
    },
}

def fix_article(slug, tool_urls, dry_run=True):
    """Fix one article's tool affiliateLinks."""
    fpath = os.path.join(ARTICLES_DIR, f'{slug}.md')
    if not os.path.exists(fpath):
        print(f"  [SKIP] File not found: {fpath}")
        return 0
    
    with open(fpath) as f:
        content = f.read()
    
    changes = 0
    
    for tool_name, correct_url in tool_urls.items():
        # Pattern: find the tool block and its affiliateLink
        # We look for: - name: "ToolName" ... affiliateLink: "https://www.notion.so"
        pattern = re.compile(
            r'(  - name: "' + re.escape(tool_name) + r'"\n(?:.*\n)*?  )'
            r'affiliateLink: "https://www\.notion\.so"',
            re.MULTILINE
        )
        
        def make_replacement(m):
            return m.group(1) + f'affiliateLink: "{correct_url}"'
        
        new_content, count = pattern.subn(make_replacement, content)
        if count > 0:
            changes += count
            content = new_content
            if dry_run:
                print(f"  {slug} / {tool_name}: notion.so -> {correct_url}")
    
    if changes > 0 and not dry_run:
        with open(fpath, 'w') as f:
            f.write(content)
    
    return changes

def main():
    dry_run = '--live' not in sys.argv
    
    if dry_run:
        print("=== DRY RUN (pass --live to apply) ===\n")
    
    total_changes = 0
    for slug, tool_urls in CORRECTIONS.items():
        changes = fix_article(slug, tool_urls, dry_run=dry_run)
        total_changes += changes
        status = f"{changes} link(s) fixed" if changes > 0 else "no notion.so links found"
        print(f"  [{status}]")
    
    print(f"\nTotal changes: {total_changes}")
    
    if not dry_run:
        print("\n✅ Changes applied to disk.")
    
    return 0 if total_changes > 0 else (2 if dry_run else 0)

if __name__ == '__main__':
    sys.exit(main())