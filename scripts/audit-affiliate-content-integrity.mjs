#!/usr/bin/env node

import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(SCRIPT_DIR, '..');
const ARTICLES_DIR = join(REPO_ROOT, 'src', 'content', 'articles');
const REGISTRY_PATH = join(REPO_ROOT, 'src', 'data', 'merchants.json');
const SITE_ID = 'dutch-ai-tools';

const registry = JSON.parse(readFileSync(REGISTRY_PATH, 'utf8'));
const merchants = registry.merchants || {};

const domainIndex = [];
for (const [merchantId, merchant] of Object.entries(merchants)) {
  for (const hint of merchant.domainHints || []) {
    domainIndex.push({ merchantId, hint: String(hint).toLowerCase() });
  }
}
domainIndex.sort((a, b) => b.hint.length - a.hint.length);

function splitFrontmatter(source, file) {
  if (!source.startsWith('---')) {
    throw new Error(`${file}: missing opening frontmatter delimiter`);
  }

  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) {
    throw new Error(`${file}: missing closing frontmatter delimiter`);
  }

  return {
    data: parse(match[1]) || {},
    body: source.slice(match[0].length),
  };
}

function parseUrl(raw) {
  const value = String(raw || '').trim();
  const urlCount = (value.match(/https?:\/\//gi) || []).length;
  if (urlCount !== 1) {
    return { ok: false, reason: urlCount > 1 ? 'multiple_urls_in_value' : 'missing_http_url' };
  }

  try {
    const url = new URL(value);
    if (!['http:', 'https:'].includes(url.protocol)) {
      return { ok: false, reason: 'unsupported_protocol' };
    }
    return { ok: true, url };
  } catch {
    return { ok: false, reason: 'invalid_url' };
  }
}

function normalizeUrl(raw) {
  const parsed = parseUrl(raw);
  if (!parsed.ok) return null;
  const url = new URL(parsed.url.toString());
  url.hash = '';
  if (url.pathname.length > 1) {
    url.pathname = url.pathname.replace(/\/+$/, '');
  }
  return url.toString();
}

function detectMerchant(raw) {
  const parsed = parseUrl(raw);
  if (!parsed.ok) return null;

  const host = parsed.url.hostname.toLowerCase();
  for (const entry of domainIndex) {
    const hintHost = entry.hint.replace(/^https?:\/\//, '').split('/')[0];
    if (host === hintHost || host.endsWith(`.${hintHost}`)) {
      return entry.merchantId;
    }
  }
  return null;
}

function normalizeName(value) {
  return String(value || '')
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, '');
}

function merchantMatchesTool(merchantId, toolName) {
  const merchant = merchants[merchantId];
  if (!merchant || !toolName) return false;

  const normalizedMerchant = normalizeName(merchant.name);
  const normalizedTool = normalizeName(toolName);
  const brand = normalizeName(String(merchant.name || '').split(/[.\s]/)[0] || '');

  return normalizedTool === normalizedMerchant
    || normalizedTool.includes(normalizedMerchant)
    || normalizedMerchant.includes(normalizedTool)
    || (brand.length >= 4 && normalizedTool.includes(brand));
}

function statusFor(merchantId) {
  const merchant = merchants[merchantId];
  return merchant?.perSite?.[SITE_ID]?.status || merchant?.status || 'unknown';
}

function bodyUrls(body) {
  const values = body.match(/https?:\/\/[^\s)>'"]+/gi) || [];
  return new Set(values.map(normalizeUrl).filter(Boolean));
}

function looksAffiliateLike(raw) {
  const parsed = parseUrl(raw);
  if (!parsed.ok) return false;
  const keys = [...parsed.url.searchParams.keys()].map((key) => key.toLowerCase());
  return keys.some((key) => ['via', 'ref', 'pc', 'tag', 'aff', 'affiliate', 'partner'].includes(key));
}

function placeholderReason(tool) {
  const name = String(tool?.name || '').trim();
  const verdict = String(tool?.verdict || '').trim();
  if (/^(?:ai\s*)?tool\s*[a-z0-9]+$/i.test(name)) return 'placeholder_tool_name';
  if (/^extra\s+.+tool\b/i.test(verdict)) return 'placeholder_tool_verdict';
  return null;
}

const findings = [];
const counters = {
  articleFiles: 0,
  publishedArticles: 0,
  draftArticles: 0,
  frontmatterAffiliateLinks: 0,
  toolLinks: 0,
};

function addFinding(file, type, severity, details = {}) {
  findings.push({ file, type, severity, ...details });
}

const files = readdirSync(ARTICLES_DIR)
  .filter((name) => name.endsWith('.md'))
  .sort();

for (const name of files) {
  counters.articleFiles += 1;
  const fullPath = join(ARTICLES_DIR, name);
  const file = relative(REPO_ROOT, fullPath).replaceAll('\\', '/');
  const source = readFileSync(fullPath, 'utf8');

  let parsed;
  try {
    parsed = splitFrontmatter(source, file);
  } catch (error) {
    addFinding(file, 'frontmatter_parse_error', 'error', { reason: error.message });
    continue;
  }

  const { data, body } = parsed;
  if (data.draft === true) {
    counters.draftArticles += 1;
    continue;
  }
  counters.publishedArticles += 1;

  const bodyLinkSet = bodyUrls(body);
  const tools = Array.isArray(data.tools) ? data.tools : [];
  const toolLinkSet = new Set();
  const toolNames = tools.map((tool) => String(tool?.name || '').trim()).filter(Boolean);

  const wrapperPattern = /^\s*(?:absoluut|zeker|natuurlijk|ok[eé])[!,.]?\s+hier\s+is\b/im;
  if (wrapperPattern.test(body) || wrapperPattern.test(String(data.description || ''))) {
    addFinding(file, 'model_wrapper_preamble', 'error');
  }

  const bodyH1Count = (body.match(/^#\s+.+$/gm) || []).length;
  if (bodyH1Count > 0) {
    addFinding(file, 'body_h1_duplicates_layout_title', 'warning', { count: bodyH1Count });
  }

  for (const tool of tools) {
    const toolName = String(tool?.name || '').trim();
    const placeholder = placeholderReason(tool);
    if (placeholder) {
      addFinding(file, placeholder, 'error', { toolName });
    }

    const raw = String(tool?.affiliateLink || '').trim();
    if (!raw) continue;
    counters.toolLinks += 1;

    const parsedUrl = parseUrl(raw);
    if (!parsedUrl.ok) {
      addFinding(file, 'malformed_tool_link', 'error', { toolName, reason: parsedUrl.reason });
      continue;
    }

    toolLinkSet.add(normalizeUrl(raw));
    const merchantId = detectMerchant(raw);
    if (!merchantId) {
      if (looksAffiliateLike(raw)) {
        addFinding(file, 'unregistered_affiliate_like_tool_link', 'error', {
          toolName,
          host: parsedUrl.url.hostname,
          queryKeys: [...parsedUrl.url.searchParams.keys()].sort(),
        });
      }
      continue;
    }

    if (!merchantMatchesTool(merchantId, toolName)) {
      addFinding(file, 'tool_merchant_mismatch', 'error', { merchantId, toolName });
    }

    const status = statusFor(merchantId);
    if (['rejected', 'dead', 'inactive'].includes(status)) {
      addFinding(file, 'tool_cta_hidden_by_registry', 'warning', {
        merchantId,
        toolName,
        status,
      });
    }
  }

  const affiliateLinks = Array.isArray(data.affiliateLinks) ? data.affiliateLinks : [];
  const seenTopLinks = new Set();
  for (const rawValue of affiliateLinks) {
    counters.frontmatterAffiliateLinks += 1;
    const raw = String(rawValue || '').trim();
    const parsedUrl = parseUrl(raw);
    if (!parsedUrl.ok) {
      addFinding(file, 'malformed_frontmatter_affiliate_link', 'error', {
        reason: parsedUrl.reason,
      });
      continue;
    }

    const normalized = normalizeUrl(raw);
    if (seenTopLinks.has(normalized)) {
      addFinding(file, 'duplicate_frontmatter_affiliate_link', 'warning');
      continue;
    }
    seenTopLinks.add(normalized);

    const merchantId = detectMerchant(raw);
    if (merchantId) {
      const matchesAnyTool = toolNames.some((toolName) => merchantMatchesTool(merchantId, toolName));
      if (!matchesAnyTool) {
        addFinding(file, 'frontmatter_merchant_unrelated_to_tools', 'error', { merchantId });
      }

      const status = statusFor(merchantId);
      if (['rejected', 'dead', 'inactive'].includes(status)) {
        addFinding(file, 'inactive_frontmatter_affiliate_metadata', 'warning', {
          merchantId,
          status,
        });
      }
    } else if (looksAffiliateLike(raw)) {
      addFinding(file, 'unregistered_affiliate_like_frontmatter_link', 'error', {
        host: parsedUrl.url.hostname,
        queryKeys: [...parsedUrl.url.searchParams.keys()].sort(),
      });
    }

    if (!toolLinkSet.has(normalized) && !bodyLinkSet.has(normalized)) {
      addFinding(file, 'orphan_frontmatter_affiliate_metadata', 'warning', {
        merchantId: merchantId || 'unregistered',
      });
    }
  }
}

const byType = {};
const bySeverity = {};
const affectedFiles = new Set();
const filesByType = {};
const filesBySeverity = {};
for (const finding of findings) {
  byType[finding.type] = (byType[finding.type] || 0) + 1;
  bySeverity[finding.severity] = (bySeverity[finding.severity] || 0) + 1;
  affectedFiles.add(finding.file);
  filesByType[finding.type] ||= new Set();
  filesByType[finding.type].add(finding.file);
  filesBySeverity[finding.severity] ||= new Set();
  filesBySeverity[finding.severity].add(finding.file);
}

const affectedFilesByType = Object.fromEntries(
  Object.entries(filesByType).map(([type, fileSet]) => [type, fileSet.size])
);
const affectedFilesBySeverity = Object.fromEntries(
  Object.entries(filesBySeverity).map(([severity, fileSet]) => [severity, fileSet.size])
);

const result = {
  schemaVersion: '1.0',
  observedAt: new Date().toISOString(),
  repository: REPO_ROOT,
  siteId: SITE_ID,
  mode: 'read-only',
  privacy: 'Tracking values are not emitted; findings use merchant IDs, tool names, hosts, and query-key names only.',
  counters,
  summary: {
    findings: findings.length,
    affectedFiles: affectedFiles.size,
    bySeverity,
    affectedFilesBySeverity,
    byType,
    affectedFilesByType,
  },
  findings,
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);

if (process.argv.includes('--fail-on-errors') && (bySeverity.error || 0) > 0) {
  process.exitCode = 1;
}
