#!/usr/bin/env python3
"""Fix article frontmatter: replace YAML-breaking placeholders with clean values."""

import os
import re

ARTICLES_DIR = "/workspace/agent-workspace/scripts/missions/passive-income/dutch-ai-tools-comparison/src/content/articles"

# Mapping of slug to appropriate tool names (extracted from article topics)
TOOL_NAMES = {
    "beste-ai-tools-zzpers-2026": ["Notion AI", "ChatGPT", "Jasper AI", "Make", "Grammarly", "Copy.ai", "Canva AI"],
    "beste-ai-tools-kleine-ondernemers-2026": ["ChatGPT", "Notion AI", "Zapier", "Canva AI", "beehiiv", "HubSpot AI", "Grammarly Business"],
    "beste-ai-marketing-tools-2026": ["Semrush", "Jasper AI", "HubSpot AI", "beehiiv", "Surfer SEO", "Copy.ai", "MarketMuse"],
    "beste-ai-schrijftools-nederlands-2026": ["ChatGPT", "Claude", "Jasper AI", "Copy.ai", "DeepL Write", "Grammarly", "Rytr"],
    "beste-ai-tools-content-creators-2026": ["Canva AI", "Descript", "Midjourney", "ChatGPT", "CapCut AI", "Adobe Firefly", "Runway ML"],
    "beste-ai-image-generators-2026": ["Midjourney", "DALL-E 3", "Adobe Firefly", "Stable Diffusion", "Leonardo AI", "Canva AI", "Ideogram"],
    "beste-ai-video-tools-2026": ["Runway ML", "HeyGen", "Synthesia", "Descript", "CapCut AI", "Pika", "Opus Clip"],
    "beste-ai-chatbots-2026": ["ChatGPT", "Google Gemini", "Claude", "Perplexity AI", "Microsoft Copilot", "Poe", "DeepSeek"],
    "chatgpt-vs-gemini-vs-claude-nederlands-2026": ["ChatGPT", "Claude", "Google Gemini"],
    "beste-ai-tools-email-marketing-2026": ["beehiiv", "Mailchimp AI", "GetResponse AI", "ActiveCampaign", "ConvertKit", "HubSpot AI"],
    "beste-ai-tools-social-media-2026": ["Buffer AI", "Hootsuite", "Later", "Canva", "Jasper AI", "Ocoya", "Predis.ai"],
    "beste-ai-tools-programmeren-2026": ["GitHub Copilot", "Cursor", "Claude Code", "Tabnine", "Cody", "Replit AI", "CodeWhisperer"],
    "beste-ai-tools-studenten-2026": ["ChatGPT", "Notion AI", "Grammarly", "Quizlet AI", "Perplexity", "Otter.ai", "Wolfram Alpha"],
    "notion-ai-review-nederlands-2026": ["Notion AI", "Coda AI", "Craft", "Obsidian", "ClickUp AI", "Anytype", "Notion Calendar"],
    "beste-gratis-ai-tools-2026": ["ChatGPT Free", "Claude Free", "Perplexity Free", "Canva Free", "Google Gemini", "CapCut Free", "Grammarly Free", "Copy.ai Free"],
    "beste-ai-tools-administratie-2026": ["Moneybird", "Exact Online", "e-Boekhouden", "Jortt", "Informer", "Yuki", "SnelStart"],
    "beste-ai-automation-tools-2026": ["Zapier", "Make", "n8n", "Pipedream", "IFTTT", "Tray.io"],
}

AFFILIATE_MAP = {
    "BEEHIIV_AFF": "https://www.beehiiv.com/",
    "OUTLIERKIT_AFF": "https://outlierkit.com/?ref=aitoolsnl",
    "ZAPIER_AFF": "https://zapier.com/?ref=aitoolsnl",
    "MAKE_AFF": "https://www.make.com/?ref=aitoolsnl",
    "SEMRUSH_AFF": "https://www.semrush.com/?ref=aitoolsnl",
}

def fix_frontmatter(content: str, slug: str) -> str:
    """Fix frontmatter YAML issues."""
    # Find frontmatter bounds
    if not content.startswith("---"):
        return content

    end_match = re.search(r"\n---\n", content[3:])
    if not end_match:
        return content

    fm_end = 3 + end_match.start() + len("\n---\n")
    fm_text = content[:fm_end]
    body = content[fm_end:]

    # Get proper tool names
    tools = TOOL_NAMES.get(slug, ["AI Tool A", "AI Tool B", "AI Tool C", "AI Tool D", "AI Tool E", "AI Tool F", "AI Tool G"])
    first_tool = tools[0]

    # Replace placeholders
    fm_text = fm_text.replace("{{TOOL_1}}", first_tool)
    fm_text = fm_text.replace("{{BEEHIIV_AFF}}", AFFILIATE_MAP["BEEHIIV_AFF"])

    # Replace other tool placeholders
    for i, tool in enumerate(tools):
        idx = i + 1
        fm_text = fm_text.replace(f"TOOL_{idx}", tool)
        fm_text = fm_text.replace(f"{{{{TOOL_{idx}}}}}", tool)

    # Fix featuredTool - it was "{{TOOL_1}}"
    fm_text = fm_text.replace(f'featuredTool: "{first_tool}"', f'featuredTool: "{first_tool}"')
    fm_text = fm_text.replace(f'featuredTool: "{{TOOL_1}}"', f'featuredTool: "{first_tool}"')

    # Fix tool names in tools list
    for i, tool in enumerate(tools):
        idx = i + 1
        fm_text = fm_text.replace(f'name: "{{{{TOOL_{idx}}}}}"', f'name: "{tool}"')
        fm_text = fm_text.replace(f'name: "{{{{TOOL_{idx}}}}}"', f'name: "{tool}"')

    return fm_text + body


def main():
    count = 0
    for fname in os.listdir(ARTICLES_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(ARTICLES_DIR, fname)
        slug = fname.replace(".md", "")

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        fixed = fix_frontmatter(content, slug)

        if fixed != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(fixed)
            count += 1
            print(f"Fixed: {fname}")

    print(f"\nFixed {count} files")


if __name__ == "__main__":
    main()
