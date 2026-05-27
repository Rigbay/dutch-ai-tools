// Affiliate links for Dutch AI Tools site
// Live networks: beehiiv (50-60%), Taskade (20% lifetime), Writesonic (30% lifetime)
// Closed: Notion (Dec 2025), Copy.ai (Fullcast acquisition), Anyword (enterprise pivot)
// Pending: Jasper (Impact.com — not signed up), Rytr (not signed up)
// Updated: 2026-05-26 — removed stale Notion application language

export const AFFILIATE_MAP: Record<string, string> = {
  BEEHIIV_AFF: 'https://www.beehiiv.com/?via=anonymous-operator',
  TASKADE_AFF: 'https://www.taskade.com/?via=aitoolsnl',
  WRITESONIC_AFF: 'https://writesonic.com/?via=aitoolsnl',
  OUTLIERKIT_AFF: 'https://outlierkit.com/?ref=aitoolsnl',
  ZAPIER_AFF: 'https://zapier.com/?ref=aitoolsnl',
  MAKE_AFF: 'https://www.make.com/en/register?pc=aitoolsnl',
  SEMRUSH_AFF: 'https://www.semrush.com/?ref=aitoolsnl',
  JASPER_AFF: 'https://www.jasper.ai/?ref=aitoolsnl',
  SURFER_AFF: 'https://surferseo.com/?ref=aitoolsnl',
  GRAMMARLY_AFF: 'https://www.grammarly.com/?ref=aitoolsnl',
};

export function resolveAffiliate(key: string): string {
  return AFFILIATE_MAP[key] || key;
}
