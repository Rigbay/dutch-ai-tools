import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { extractInternalArticleLinks } from './model-freshness-links.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const articlesDir =
  process.env.MODEL_FRESHNESS_ARTICLES_DIR ||
  join(root, 'src', 'content', 'articles');
const files = readdirSync(articlesDir).filter((name) => name.endsWith('.md')).sort();

const retiredGenerationPattern =
  /GPT-3\.5|GPT-4o|GPT-4\.5|(?<![\w.])GPT-4(?![\w.])|Claude\s+3(?:\.5)?(?:\s+(?:Opus|Sonnet|Haiku))?|Gemini\s+(?:1\.5(?:\s+Pro)?|Pro|Ultra)/gi;
const placeholderNamePattern =
  /^\s*-\s+name:\s*['"]?((?:AI\s*)?Tool\s*[A-Za-z0-9]+)['"]?\s*$/gmi;

const frontmatter = (text) => text.split('---')[1] || '';
const field = (yaml, name) => {
  const match = yaml.match(new RegExp(`^${name}:\\s*['"]?([^\\r\\n'"]+)`, 'mi'));
  return match?.[1]?.trim() || null;
};
const isDraft = (yaml) => /^draft:\s*true\s*$/mi.test(yaml);

const articles = files.map((file) => {
  const text = readFileSync(join(articlesDir, file), 'utf8');
  const yaml = frontmatter(text);
  return {
    file,
    text,
    yaml,
    slug: field(yaml, 'slug') || file.replace(/\.md$/, ''),
    draft: isDraft(yaml)
  };
});

const bySlug = new Map(articles.map((article) => [article.slug, article]));
const retiredGenerationFindings = [];
const placeholderFindings = [];
const linksToDrafts = [];

for (const article of articles.filter((item) => !item.draft)) {
  const lines = article.text.split(/\r?\n/);

  lines.forEach((line, index) => {
    const retiredMatches = [...line.matchAll(retiredGenerationPattern)].map((match) => match[0]);
    retiredGenerationPattern.lastIndex = 0;
    if (retiredMatches.length) {
      retiredGenerationFindings.push({
        file: article.file,
        line: index + 1,
        terms: [...new Set(retiredMatches)],
        excerpt: line.trim()
      });
    }

    const placeholderMatches = [...line.matchAll(placeholderNamePattern)].map((match) => match[1].trim());
    placeholderNamePattern.lastIndex = 0;
    if (placeholderMatches.length) {
      placeholderFindings.push({
        file: article.file,
        line: index + 1,
        entries: placeholderMatches
      });
    }
  });

  for (const link of extractInternalArticleLinks(article.text)) {
    const target = bySlug.get(link.slug);
    if (target?.draft) {
      const line = article.text.slice(0, link.index).split(/\r?\n/).length;
      linksToDrafts.push({
        file: article.file,
        line,
        target: target.slug
      });
    }
  }
}

const result = {
  schema: 'dutch-ai-tools-model-freshness-audit-v1',
  officialSources: [
    'https://help.openai.com/en/articles/20001051',
    'https://help.openai.com/en/articles/6825453-chatgpt-release-notes',
    'https://platform.claude.com/docs/en/docs/about-claude/model-deprecations',
    'https://ai.google.dev/gemini-api/docs/deprecations'
  ],
  scope: {
    articles: articles.length,
    published: articles.filter((article) => !article.draft).length,
    drafts: articles.filter((article) => article.draft).length
  },
  findings: {
    retiredGenerationFindings,
    placeholderFindings,
    linksToDrafts
  },
  passed:
    retiredGenerationFindings.length === 0 &&
    placeholderFindings.length === 0 &&
    linksToDrafts.length === 0
};

console.log(JSON.stringify(result, null, 2));
process.exitCode = result.passed ? 0 : 1;
