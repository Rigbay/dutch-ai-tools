import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  inspectThinSensitiveArticle,
  minimumSensitiveBodyWords
} from './thin-sensitive-page-rules.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const articlesDir =
  process.env.THIN_SENSITIVE_ARTICLES_DIR ||
  join(root, 'src', 'content', 'articles');
const files = readdirSync(articlesDir)
  .filter((name) => name.endsWith('.md'))
  .sort();
const articles = files.map((file) =>
  inspectThinSensitiveArticle(
    file,
    readFileSync(join(articlesDir, file), 'utf8')
  )
);
const findings = articles
  .filter((article) => article.finding)
  .map(({ file, slug, title, wordCount, sensitiveRuleIds }) => ({
    file,
    slug,
    title,
    wordCount,
    sensitiveRuleIds,
    action: 'draft_or_rebuild_from_current_sources'
  }));
const result = {
  schema: 'dutch-ai-tools-thin-sensitive-page-audit-v0.1',
  rule:
    'Published sensitive-topic comparisons must contain at least 150 body words.',
  minimumSensitiveBodyWords,
  scope: {
    articles: articles.length,
    published: articles.filter((article) => !article.draft).length,
    drafts: articles.filter((article) => article.draft).length,
    sensitivePublished: articles.filter(
      (article) => !article.draft && article.sensitiveRuleIds.length > 0
    ).length
  },
  findings,
  passed: findings.length === 0
};

console.log(JSON.stringify(result, null, 2));
process.exitCode = result.passed ? 0 : 1;
