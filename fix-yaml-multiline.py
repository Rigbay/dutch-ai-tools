#!/usr/bin/env python3
"""Fix YAML frontmatter with broken multiline strings."""

import os, sys, re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for frontmatter
    if not content.startswith('---'):
        return False
    
    # Find end of frontmatter
    end = content.find('\n---', 4)
    if end == -1:
        return False
    
    front = content[4:end]
    body = content[end+4:]
    
    lines = front.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        # Fix title and description fields
        if line.startswith('title: "') or line.startswith('description: "'):
            key = line.split(':')[0]
            # Collect multiline string
            parts = [line]
            j = i + 1
            while j < len(lines) and not lines[j].rstrip().endswith('"'):
                parts.append(lines[j])
                j += 1
            if j < len(lines):
                parts.append(lines[j])
                i = j
            
            # Reconstruct
            full = '\n'.join(parts)
            # Extract text between first and last quote
            match = re.search(r'^' + key + r':\s*"(.*?)"$', full, re.DOTALL)
            if match:
                text = match.group(1).strip()
                # Remove extra quotes and line continuation spaces
                text = re.sub(r'\n\s+', ' ', text)
                text = ' '.join(text.split())
                # Truncate if too long for description
                if key == 'description' and len(text) > 180:
                    text = text[:177] + '...'
                fixed_lines.append(f'{key}: >-')
                fixed_lines.append(f'  {text}')
            else:
                # Fallback
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        i += 1
    
    new_front = '\n'.join(fixed_lines)
    new_content = '---\n' + new_front + '\n---' + body
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    ARTICLES_DIR = "/workspace/dutch-ai-tools/src/content/articles"
    count = 0
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith('.md'):
            path = os.path.join(ARTICLES_DIR, fname)
            try:
                if fix_file(path):
                    print(f"Fixed: {fname}")
                    count += 1
            except Exception as e:
                print(f"Error fixing {fname}: {e}")
    print(f"\nTotal fixed: {count}")

if __name__ == '__main__':
    main()