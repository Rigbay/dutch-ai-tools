import assert from 'node:assert/strict';

const { canRenderAffiliate, resolveAffiliateUrl } = await import(
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

console.log('Affiliate attribution contract tests passed.');
