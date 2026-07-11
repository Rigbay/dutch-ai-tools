import { readFileSync } from 'fs';
import { join } from 'path';

// Use committed registry copy (sync from ~/.hermes/affiliates/merchants.json before deploy).
// During Astro prerender, import.meta.url may point at compiled dist chunks, so keep
// the source-path lookup anchored to the repository root instead of the output dir.
const REGISTRY_PATH = join(process.cwd(), 'src/data/merchants.json');

let cachedRegistry: any = null;
let domainIndex: Record<string, string> | null = null;

export type MerchantStatus =
  | 'active'
  | 'pending'
  | 'rejected'
  | 'pending_review'
  | 'dead'
  | 'inactive';

export interface PerSiteEntry {
  status: MerchantStatus;
  affiliateId: string | null;
}

export interface Merchant {
  name: string;
  program: string;
  status: MerchantStatus;
  perSite?: Record<string, PerSiteEntry>;
  commission?: { rate: number; type: string; notes?: string } | null;
  cookieDurationHours?: number | null;
  linkTemplate?: string | null;
  fallbackUrl?: string | null;
  lastVerified?: string;
  notes?: string;
  domainHints?: string[];
}

export interface Registry {
  meta?: {
    version: string;
    lastUpdated: string;
    updatedBy: string;
    source: string;
  };
  merchants: Record<string, Merchant>;
}

export function loadRegistry(): Registry {
  if (cachedRegistry) return cachedRegistry;

  try {
    const raw = readFileSync(REGISTRY_PATH, 'utf-8');
    cachedRegistry = JSON.parse(raw);
    // Build domain→merchantId index
    domainIndex = {};
    for (const [id, merchant] of Object.entries(cachedRegistry.merchants)) {
      const m = merchant as Merchant;
      if (m.domainHints) {
        for (const hint of m.domainHints) {
          domainIndex[hint] = id;
        }
      }
    }
    return cachedRegistry;
  } catch (err) {
    console.warn(
      `[affiliateRegistry] Failed to load registry at ${REGISTRY_PATH}: ${err}`
    );
    return { merchants: {} };
  }
}

export function getMerchant(id: string): Merchant | null {
  const reg = loadRegistry();
  return reg.merchants?.[id] ?? null;
}

export function detectMerchant(url: string): string | null {
  loadRegistry(); // ensure domainIndex is built
  if (!domainIndex) return null;
  const lower = url.toLowerCase();
  for (const [domain, id] of Object.entries(domainIndex)) {
    if (lower.includes(domain)) return id;
  }
  return null;
}

export function merchantMatchesTool(merchantId: string, toolName: string): boolean {
  const merchant = getMerchant(merchantId);
  if (!merchant || !toolName) return false;

  const normalize = (value: string) => value
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, '');

  const normalizedMerchant = normalize(merchant.name);
  const normalizedTool = normalize(toolName);
  const brand = normalize(merchant.name.split(/[.\s]/)[0] || '');

  return normalizedTool === normalizedMerchant
    || normalizedTool.includes(normalizedMerchant)
    || normalizedMerchant.includes(normalizedTool)
    || (brand.length >= 4 && normalizedTool.includes(brand));
}

export function canRenderAffiliate(merchantId: string, siteId: string): boolean {
  const merchant = getMerchant(merchantId);
  if (!merchant) return false;

  const perSite = merchant.perSite?.[siteId];
  if (!perSite) return false;

  const status = perSite.status;
  if (['rejected', 'dead', 'inactive'].includes(status)) {
    return false;
  }

  const template = merchant.linkTemplate || merchant.fallbackUrl || '';
  if (!template) return false;

  const affiliateId = perSite.affiliateId?.trim() || '';
  const resolvedTemplate = template.replace(/\{affiliateId\}/g, affiliateId);
  if (/\{[^}]+\}/.test(resolvedTemplate)) return false;

  // A program/account can be active while its public URL is deliberately
  // direct and unattributed (for example while a personal slug is disabled).
  // Only render AffiliateLink — and therefore emit affiliate_outbound_click —
  // when the resolved URL carries an actual tracking signal.
  return /[?&](?:via|ref|tag|fp_ref|pc)=[^&]+/i.test(resolvedTemplate)
    || /(?:awin1\.com|pxf\.io|sjv\.io)\//i.test(resolvedTemplate);
}

export function resolveAffiliateUrl(
  merchantId: string,
  siteId: string,
  params: Record<string, string> = {}
): string | null {
  if (!canRenderAffiliate(merchantId, siteId)) {
    return null;
  }

  const merchant = getMerchant(merchantId)!;
  const perSite = merchant.perSite?.[siteId];
  const affiliateId = perSite?.affiliateId ?? '';

  let template = merchant.linkTemplate || merchant.fallbackUrl || '';
  if (!template) {
    return null;
  }

  // Inject affiliateId (common placeholder)
  template = template.replace(/\{affiliateId\}/g, affiliateId);

  // Inject caller-provided params (asin, productId, targetUrl, etc.)
  for (const [key, value] of Object.entries(params)) {
    if (!value) continue;
    const re = new RegExp(`\\{${key}\\}`, 'g');
    template = template.replace(re, value);
  }

  if (/\{[^}]+\}/.test(template)) {
    return null;
  }

  return template;
}
