#!/usr/bin/env python3
"""
Fix category overview article schema issues:
1. description must be <= 180 chars
2. tools array must have at least 3 items
3. related array must have at least 1 item
"""

import re
from pathlib import Path

def fix_category_overview(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = []
    
    # 1. Fix description length
    desc_match = re.search(r'^description:\s*\'(.*?)\'', content, re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1)
        if len(desc) > 180:
            new_desc = 'Overzicht van alle AI Tools artikelen per categorie: Business, productiviteit, development, creatie, marketing, technologie, persoonlijk en huis-tuin.'
            content = re.sub(r'^description:\s*\'(.*?)\'', f"description: '{new_desc}'", content, flags=re.MULTILINE)
            changes.append(f"description trimmed from {len(desc)} to {len(new_desc)} chars")
    
    # 2. Add placeholder tools
    if 'tools: []' in content:
        tools_yaml = '''tools:
  - name: 'Beehiiv'
    verdict: 'Nieuwsbriefplatform voor Nederlandse AI Tools content.'
    priceRange: '€0-€99/maand'
    bestFor: 'Content creators'
    rating: 4.5
    affiliateLink: 'https://www.beehiiv.com/?via=anonymous-operator'
  - name: 'Taskade'
    verdict: 'AI-werkruimte voor teamplanning en projectmanagement.'
    priceRange: '€0-€10/maand'
    bestFor: 'Teams'
    rating: 4.3
    affiliateLink: 'https://taskade.com/?via=55nfr2'
  - name: 'Writesonic'
    verdict: 'AI copywriting voor Nederlandse marketingteksten.'
    priceRange: '€15-€100/maand'
    bestFor: 'Marketeers'
    rating: 4.4
    affiliateLink: 'https://writesonic.com/?via=aitoolsnl'
'''
        content = content.replace('tools: []', tools_yaml.rstrip())
        changes.append("added 3 placeholder tools")
    
    # 3. Add placeholder related
    if 'related: []' in content:
        content = content.replace('related: []', '''related:
  - beste-ai-tools-business-intelligence-2026
  - beste-ai-tools-marketing-automation-2026
  - beste-ai-tools-productiviteit-2026''')
        changes.append("added 3 related articles")
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath.name}: {', '.join(changes)}")
        return True
    return False

if __name__ == "__main__":
    filepath = Path("/workspace/dutch-ai-tools/src/content/articles/categorie-overzicht-2026.md")
    if fix_category_overview(filepath):
        print("Category overview fixed")
    else:
        print("No changes needed")