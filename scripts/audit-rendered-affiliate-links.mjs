#!/usr/bin/env node

import assert from 'node:assert/strict';
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
const URL_PATTERN = /https?:\/\/[^\s)"'<>|]+|(?<![a-z0-9_:/.-])\/\/[^\s)"'<>|]+/gi;

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

function decodeHtmlCharacterReferences(value) {
  const named = {
    amp: '&',
    colon: ':',
    equals: '=',
    percnt: '%',
    quest: '?',
    sol: '/',
  };

  return value.replace(
    /&(?:#(\d+)|#x([0-9a-f]+)|([a-z][a-z0-9]+));/gi,
    (entity, decimal, hexadecimal, name) => {
      if (name) return named[name.toLowerCase()] ?? entity;

      const codePoint = Number.parseInt(decimal ?? hexadecimal, decimal ? 10 : 16);
      if (!Number.isInteger(codePoint) || codePoint < 0 || codePoint > 0x10ffff) {
        return entity;
      }

      try {
        return String.fromCodePoint(codePoint);
      } catch {
        return entity;
      }
    },
  );
}

function normalizeUrl(raw) {
  try {
    const decoded = decodeHtmlCharacterReferences(raw);
    const url = new URL(decoded.startsWith('//') ? `https:${decoded}` : decoded);
    url.hash = '';
    return url.toString();
  } catch {
    return null;
  }
}

function urlOccurrencesIn(body) {
  return [...body.matchAll(URL_PATTERN)].map((match) => ({
    decoded: decodeHtmlCharacterReferences(match[0]),
    index: match.index,
    raw: match[0],
  }));
}

function attributeValue(tag, name) {
  const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = tag.match(new RegExp(`\\b${escapedName}=(?:"([^"]*)"|'([^']*)')`, 'i'));
  return match ? (match[1] ?? match[2] ?? '') : null;
}

function anchorsIn(body) {
  const anchors = [];
  const anchorPattern = /<a\b[^>]*\bhref=(?:"([^"]+)"|'([^']+)')[^>]*>/gi;
  for (const match of body.matchAll(anchorPattern)) {
    const url = normalizeUrl(match[1] ?? match[2] ?? '');
    if (!url || match.index === undefined) continue;
    anchors.push({
      start: match.index,
      end: match.index + match[0].length,
      tag: match[0],
      url,
    });
  }
  return anchors;
}

function anchorForOccurrence(anchors, normalizedUrl, occurrenceIndex) {
  return anchors.find((candidate) =>
    candidate.url === normalizedUrl
    && candidate.start <= occurrenceIndex
    && occurrenceIndex < candidate.end
  );
}

const syntheticUrl = 'https://www.synthesia.io?via=hermes';
const syntheticBody = `<a href="${syntheticUrl}" rel="sponsored nofollow">labeled</a> [unlabeled](${syntheticUrl})`;
const syntheticAnchors = anchorsIn(syntheticBody);
const syntheticOccurrences = urlOccurrencesIn(syntheticBody);
assert.equal(syntheticOccurrences.length, 2);
assert.ok(anchorForOccurrence(syntheticAnchors, normalizeUrl(syntheticOccurrences[0].decoded), syntheticOccurrences[0].index));
assert.equal(anchorForOccurrence(syntheticAnchors, normalizeUrl(syntheticOccurrences[1].decoded), syntheticOccurrences[1].index), undefined);

const encodedUrl = 'https://www.synthesia.io?via&#61;hermes';
const encodedBody = `<a href="${encodedUrl}" rel="sponsored nofollow">encoded</a>`;
const encodedOccurrence = urlOccurrencesIn(encodedBody)[0];
assert.equal(encodedOccurrence.decoded, syntheticUrl);
assert.equal(hasAffiliateTrackingSignal(encodedOccurrence.decoded), true);
assert.ok(anchorForOccurrence(anchorsIn(encodedBody), normalizeUrl(encodedOccurrence.decoded), encodedOccurrence.index));
for (const variant of [
  'https://www.synthesia.io?via&#x3d;hermes',
  'https://www.synthesia.io?via&equals;hermes',
  'https://www.synthesia.io?source=article&amp;via&#61;hermes',
]) {
  const occurrence = urlOccurrencesIn(variant)[0];
  assert.equal(hasAffiliateTrackingSignal(occurrence.decoded), true);
}

const protocolRelativeUrl = '//www.synthesia.io?via=hermes';
const protocolRelativeBody = `<a href="${protocolRelativeUrl}" rel="sponsored nofollow">protocol relative</a>`;
const protocolRelativeOccurrence = urlOccurrencesIn(protocolRelativeBody)[0];
assert.equal(urlOccurrencesIn(`<a href="${syntheticUrl}">absolute</a>`).length, 1);
assert.equal(urlOccurrencesIn('local/path//not-a-url?via=hermes').length, 0);
assert.equal(urlOccurrencesIn('ftp://www.synthesia.io?via=hermes').length, 0);
assert.equal(protocolRelativeOccurrence.raw, protocolRelativeUrl);
assert.equal(hasAffiliateTrackingSignal(protocolRelativeOccurrence.decoded), true);
assert.equal(normalizeUrl(protocolRelativeOccurrence.decoded), normalizeUrl(syntheticUrl));
assert.ok(anchorForOccurrence(
  anchorsIn(protocolRelativeBody),
  normalizeUrl(protocolRelativeOccurrence.decoded),
  protocolRelativeOccurrence.index,
));
const bareProtocolRelativeBody = `[unlabeled](${protocolRelativeUrl})`;
const bareProtocolRelativeOccurrence = urlOccurrencesIn(bareProtocolRelativeBody)[0];
assert.equal(anchorForOccurrence(
  anchorsIn(bareProtocolRelativeBody),
  normalizeUrl(bareProtocolRelativeOccurrence.decoded),
  bareProtocolRelativeOccurrence.index,
), undefined);

for (const name of readdirSync(ARTICLES_DIR).filter((file) => file.endsWith('.md')).sort()) {
  articleFiles += 1;
  const fullPath = join(ARTICLES_DIR, name);
  const file = relative(REPO_ROOT, fullPath).replaceAll('\\', '/');
  const body = splitBody(readFileSync(fullPath, 'utf8'), file);

  const compliantAnchors = anchorsIn(body);

  for (const occurrence of urlOccurrencesIn(body)) {
    const decoded = occurrence.decoded;
    if (!hasAffiliateTrackingSignal(decoded)) continue;
    trackedBodyUrls += 1;

    const normalized = normalizeUrl(decoded);
    const merchantId = detectMerchant(decoded);
    if (!normalized || !merchantId || !canRenderAffiliate(merchantId, SITE_ID)) {
      findings.push({ file, type: 'unverified_tracking_in_rendered_body', merchantId: merchantId || 'unregistered' });
      continue;
    }

    const canonicalAffiliateUrl = normalizeUrl(resolveAffiliateUrl(merchantId, SITE_ID) || '');
    if (normalized !== canonicalAffiliateUrl) {
      findings.push({ file, type: 'noncanonical_tracking_in_rendered_body', merchantId });
      continue;
    }

    const anchor = anchorForOccurrence(compliantAnchors, normalized, occurrence.index);
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
