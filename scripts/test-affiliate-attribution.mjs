import assert from 'node:assert/strict';

const {
  canRenderAffiliate,
  hasAffiliateTrackingSignal,
  resolveAffiliateUrl,
  resolveSafeDirectProviderUrl,
} = await import(
  '../src/lib/affiliateRegistry.ts'
);

assert.equal(
  canRenderAffiliate('beehiiv', 'dutch-ai-tools'),
  false,
  'an active program with a direct, unattributed URL must not render as affiliate',
);
assert.equal(resolveAffiliateUrl('beehiiv', 'dutch-ai-tools'), null);

assert.equal(canRenderAffiliate('taskade', 'dutch-ai-tools'), true);
assert.match(
  resolveAffiliateUrl('taskade', 'dutch-ai-tools') || '',
  /[?&]via=55nfr2(?:&|$)/,
);

assert.equal(
  canRenderAffiliate('frase', 'dutch-ai-tools'),
  false,
  'a pending template with a missing affiliate ID must not render as attributable',
);
assert.equal(canRenderAffiliate('amazon-nl', 'dutch-ai-tools'), false);

assert.equal(canRenderAffiliate('synthesia', 'dutch-ai-tools'), true);
assert.equal(hasAffiliateTrackingSignal('https://example.test/?affiliate_id=123'), true);
assert.equal(hasAffiliateTrackingSignal('https://example.test/?utm_medium=affiliate&utm_source=partner'), true);

assert.equal(
  resolveSafeDirectProviderUrl('https://afas.com/?ref=aitoolsnl'),
  'https://afas.com/',
  'unverified attribution must be removed while retaining the official provider destination',
);
assert.equal(
  resolveSafeDirectProviderUrl('https://www.etoro.com/en/trade/stocks/?affiliate_id=1004&affiliates_link=1&utm_source=aitoolsnl&utm_medium=affiliate&utm_campaign=test'),
  'https://www.etoro.com/en/trade/stocks/',
);
assert.equal(resolveSafeDirectProviderUrl('https://www.example.com/tool'), null);
assert.equal(resolveSafeDirectProviderUrl('https://usemotion.pxf.io/c/unverified'), null);
assert.equal(resolveSafeDirectProviderUrl('None'), null);
assert.equal(
  resolveSafeDirectProviderUrl('https://www.notion.so/product/ai'),
  'https://www.notion.so/product/ai',
  'ordinary direct provider links must remain unchanged',
);

console.log('Affiliate attribution contract tests passed.');
