#!/usr/bin/env node

import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  canRenderAffiliate,
  detectMerchant,
  hasAffiliateTrackingSignal,
  resolveAffiliateUrl,
} from '../src/lib/affiliateRegistry.ts';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(SCRIPT_DIR, '..');
const ARTICLES_DIR = join(REPO_ROOT, 'src', 'content', 'articles');
const SITE_ID = 'dutch-ai-tools';

const findings = [];
let articleFiles = 0;
let trackedBodyUrls = 0;

function splitBody(source, file) {
  const match = source.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/);
  if (!match) {
    findings.push({ file, type: 'frontmatter_boundary_missing' });
    return '';
  }
  return source.slice(match[0].length);
}

function normalizeUrl(raw) {
  try {
    const url = new URL(raw);
    url.hash = '';
    return url.toString();
  } catch {
    return null;
  }
}

function attributeValue(tag, name) {
  const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = tag.match(new RegExp(`\\b${escapedName}=(?:"([^"]*)"|'([^']*)')`, 'i'));
  return match ? (match[1] ?? match[2] ?? '') : null;
}

for (const name of readdirSync(ARTICLES_DIR).filter((file) => file.endsWith('.md')).sort()) {
  articleFiles += 1;
  const fullPath = join(ARTICLES_DIR, name);
  const file = relative(REPO_ROOT, fullPath).replaceAll('\\', '/');
  const body = splitBody(readFileSync(fullPath, 'utf8'), file);

  const compliantAnchors = [];
  const anchorPattern = /<a\b[^>]*\bhref=(?:"([^"]+)"|'([^']+)')[^>]*>/gi;
  for (const match of body.matchAll(anchorPattern)) {
    const url = normalizeUrl(match[1] ?? match[2] ?? '');
    if (!url) continue;
    compliantAnchors.push({ tag: match[0], url });
  }

  const urlPattern = /https?:\/\/[^\s)"'<>|]+/gi;
  for (const match of body.matchAll(urlPattern)) {
    const raw = match[0];
    if (!hasAffiliateTrackingSignal(raw)) continue;
    trackedBodyUrls += 1;

    const normalized = normalizeUrl(raw);
    const merchantId = detectMerchant(raw);
    if (!normalized || !merchantId || !canRenderAffiliate(merchantId, SITE_ID)) {
      findings.push({ file, type: 'unverified_tracking_in_rendered_body', merchantId: merchantId || 'unregistered' });
      continue;
    }

    const canonicalAffiliateUrl = normalizeUrl(resolveAffiliateUrl(merchantId, SITE_ID) || '');
    if (normalized !== canonicalAffiliateUrl) {
      findings.push({ file, type: 'noncanonical_tracking_in_rendered_body', merchantId });
      continue;
    }

    const anchor = compliantAnchors.find((candidate) => candidate.url === normalized);
    if (!anchor) {
      findings.push({ file, type: 'unlabeled_tracking_in_rendered_body', merchantId });
      continue;
    }

    const rel = (attributeValue(anchor.tag, 'rel') || '').toLowerCase().split(/\s+/).filter(Boolean);
    const labeledMerchant = attributeValue(anchor.tag, 'data-affiliate-merchant');
    const labeledSite = attributeValue(anchor.tag, 'data-affiliate-site');
    if (!rel.includes('sponsored') || !rel.includes('nofollow') || labeledMerchant !== merchantId || labeledSite !== SITE_ID) {
      findings.push({ file, type: 'incomplete_affiliate_label_in_rendered_body', merchantId });
    }
  }
}

const result = {
  schemaVersion: '1.0',
  repository: REPO_ROOT,
  siteId: SITE_ID,
  mode: 'read-only',
  privacy: 'Tracking values are not emitted; findings contain only file paths, finding types, and merchant IDs.',
  counters: { articleFiles, trackedBodyUrls, findings: findings.length },
  findings,
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
if (findings.length > 0) process.exitCode = 1;
