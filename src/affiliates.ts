// Affiliate placeholder map for Dutch AI Tools site
// Replace placeholders with real affiliate links when anonymous-operator signs up

export const AFFILIATE_MAP: Record<string, string> = {
  NOTION_AFF: 'https://affiliate.notion.so/...',
  BEEHIIV_AFF: 'https://www.beehiiv.com/?via=aitoolsnl',
  OUTLIERKIT_AFF: 'https://outlierkit.com/?ref=aitoolsnl',
  ZAPIER_AFF: 'https://zapier.com/?ref=aitoolsnl',
  MAKE_AFF: 'https://www.make.com/en/register?pc=aitoolsnl',
  SEMRUSH_AFF: 'https://www.semrush.com/?ref=aitoolsnl',
  JASPER_AFF: 'https://www.jasper.ai/?ref=aitoolsnl',
  SURFER_AFF: 'https://surferseo.com/?ref=aitoolsnl',
  COPY_AI_AFF: 'https://www.copy.ai/?via=aitoolsnl',
  GRAMMARLY_AFF: 'https://www.grammarly.com/?ref=aitoolsnl',
};

export function resolveAffiliate(key: string): string {
  return AFFILIATE_MAP[key] || key;
}
