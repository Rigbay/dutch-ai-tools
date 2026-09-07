import { analyticsPolicy, analyticsReady } from './analyticsPolicy';
const MEASUREMENT_ID = 'G-P1DQLR76C6';
const STORAGE_KEY = 'dat_analytics_consent';
const WITHDRAWAL_KEY = 'dat_analytics_withdrawn';
const VERSION = analyticsPolicy.consentVersion;
const LIFETIME_MS = 180 * 24 * 60 * 60 * 1000;
type Choice = 'granted' | 'denied';
type Consent = { version: number; choice: Choice; savedAt: number; expiresAt: number };

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: (...args: unknown[]) => void;
    __orbitAnalyticsSuppressed?: boolean;
    'ga-disable-G-P1DQLR76C6'?: boolean;
  }
}

export function initializeAnalyticsConsent() {
  const panel = document.querySelector<HTMLElement>('[data-consent-panel]');
  if (!panel || panel.dataset.initialized) return;
  panel.dataset.initialized = 'true';
  const status = panel.querySelector<HTMLElement>('[data-consent-status]')!;
  const heading = panel.querySelector<HTMLElement>('#consent-heading')!;
  let opener: HTMLElement | null = null;
  let storageAvailable = true;
  let active = false;
  let tag: HTMLScriptElement | null = null;
  let expiryTimer: ReturnType<typeof setTimeout> | undefined;
  let inMemoryChoice: Choice | null = null;
  let sessionWithdrawn = false;
  window['ga-disable-G-P1DQLR76C6'] = true;

  // Storage failures must never turn the QA exclusion into an ordinary visit.
  let qaSuppressed = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  try {
    const qaParameter = new URLSearchParams(location.search).get('orbit_qa');
    if (qaParameter === '1') sessionStorage.setItem('orbit_analytics_qa', '1');
    if (qaParameter === '0') sessionStorage.removeItem('orbit_analytics_qa');
    qaSuppressed ||= sessionStorage.getItem('orbit_analytics_qa') === '1';
    sessionWithdrawn = sessionStorage.getItem(WITHDRAWAL_KEY) === '1';
  } catch {
    qaSuppressed = true;
  }
  window.__orbitAnalyticsSuppressed = qaSuppressed;

  function readConsent(): Consent | null {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      // Verify writes too: a readable old grant is insufficient if choices cannot be saved.
      if (raw !== null) localStorage.setItem(STORAGE_KEY, raw);
      if (!raw) return null;
      const record = JSON.parse(raw);
      const now = Date.now();
      if (record.version !== VERSION || !['granted', 'denied'].includes(record.choice) ||
          !Number.isFinite(record.savedAt) || !Number.isFinite(record.expiresAt) ||
          record.savedAt > now || record.expiresAt <= now ||
          record.expiresAt - record.savedAt !== LIFETIME_MS) return null;
      storageAvailable = true;
      return record;
    } catch {
      storageAvailable = false;
      return null;
    }
  }

  function saveConsent(choice: Choice): boolean {
    const savedAt = Date.now();
    const record = JSON.stringify({ version: VERSION, choice, savedAt, expiresAt: savedAt + LIFETIME_MS });
    try {
      localStorage.setItem(STORAGE_KEY, record);
      storageAvailable = localStorage.getItem(STORAGE_KEY) === record;
    } catch { storageAvailable = false; }
    return storageAvailable;
  }

  function clearAnalyticsCookies() {
    let cookieString = '';
    try { cookieString = document.cookie; } catch { return; }
    const names = cookieString.split(';').map(cookie => cookie.split('=')[0].trim())
      .filter(name => /^(_ga($|_)|_gid$|_gat($|_))/.test(name));
    const hostParts = location.hostname.split('.');
    const domains = ['', ...hostParts.map((_, index) => hostParts.slice(index).join('.'))];
    const segments = location.pathname.split('/').filter(Boolean);
    const paths = ['/', ...segments.map((_, index) => '/' + segments.slice(0, index + 1).join('/'))];
    for (const name of names) for (const domain of domains) for (const path of paths) {
      try {
        document.cookie = `${name}=; Max-Age=0; Path=${path}; SameSite=Lax${domain ? `; Domain=${domain}` : ''}`;
      } catch { /* A browser may forbid cookies; analytics stays disabled. */ }
    }
  }

  function stopAnalytics(reload: boolean) {
    const wasActive = active;
    active = false;
    window['ga-disable-G-P1DQLR76C6'] = true;
    window.gtag = () => {};
    window.dataLayer = [];
    tag?.remove();
    clearTimeout(expiryTimer);
    clearAnalyticsCookies();
    // End Google's existing execution context as well as disabling future events.
    // Do not send a denied consent-mode update: that can itself send a ping.
    if (wasActive && reload) location.reload();
  }

  function startAnalytics(record: Consent) {
    if (!analyticsReady || sessionWithdrawn || active || qaSuppressed || !storageAvailable || record.choice !== 'granted') return;
    active = true;
    window['ga-disable-G-P1DQLR76C6'] = false;
    window.dataLayer = [];
    window.gtag = function (..._args: unknown[]) {
      if (active && !window['ga-disable-G-P1DQLR76C6']) window.dataLayer!.push(arguments);
    };
    window.gtag('consent', 'default', {
      analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    });
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: LIFETIME_MS / 1000,
      cookie_update: false,
      page_location: location.origin + location.pathname,
      page_referrer: document.referrer ? new URL(document.referrer).origin + new URL(document.referrer).pathname : '',
    });
    tag = document.createElement('script');
    tag.async = true;
    tag.dataset.consentAnalytics = 'true';
    tag.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
    document.head.appendChild(tag);
    // Recheck long-lived tabs in bounded intervals (setTimeout has a 32-bit limit).
    expiryTimer = setTimeout(reconcile, Math.min(record.expiresAt - Date.now(), 60_000));
  }

  function updateStatus() {
    if (!analyticsReady) {
      status.textContent = 'De site en partnerlinks blijven werken. Er wordt geen toestemming voor statistieken opgeslagen.';
    } else if (!storageAvailable) {
      status.textContent = 'Je browser kan de keuze niet opslaan. Statistieken blijven uit. Je kunt de site gewoon gebruiken.';
    } else if (inMemoryChoice === 'granted') {
      status.textContent = 'Je hebt statistieken toegestaan. Met “Statistieken weigeren” trek je die toestemming in.';
    } else if (inMemoryChoice === 'denied') {
      status.textContent = 'Je hebt statistieken geweigerd. Google Analytics staat uit.';
    } else {
      status.textContent = 'Je hebt nog geen keuze gemaakt. Statistieken staan uit.';
    }
  }

  function closePanel() {
    panel!.hidden = true;
    opener?.focus();
  }

  function choose(choice: Choice) {
    if (!analyticsReady) return;
    inMemoryChoice = choice;
    const saved = saveConsent(choice);
    if (choice === 'denied') {
      // A failed overwrite must not reload a stale grant and re-enable analytics.
      sessionWithdrawn = true;
      let withdrawalRemembered = saved;
      try {
        sessionStorage.setItem(WITHDRAWAL_KEY, '1');
        withdrawalRemembered ||= sessionStorage.getItem(WITHDRAWAL_KEY) === '1';
      } catch { /* Remain disabled in this document if neither store can save. */ }
      if (!saved) try {
        localStorage.removeItem(STORAGE_KEY);
        withdrawalRemembered ||= localStorage.getItem(STORAGE_KEY) === null;
      } catch { /* No reload into a stale grant. */ }
      stopAnalytics(withdrawalRemembered);
    } else if (!saved) {
      stopAnalytics(false);
    } else {
      try {
        sessionStorage.removeItem(WITHDRAWAL_KEY);
        sessionWithdrawn = sessionStorage.getItem(WITHDRAWAL_KEY) === '1';
      } catch { sessionWithdrawn = true; storageAvailable = false; }
      const record = readConsent();
      if (record?.choice === 'granted') startAnalytics(record);
    }
    updateStatus();
    if (saved) closePanel();
  }

  function reconcile() {
    clearTimeout(expiryTimer);
    if (!analyticsReady) { stopAnalytics(false); return; }
    const record = readConsent();
    if (sessionWithdrawn || !record || record.choice !== 'granted') {
      inMemoryChoice = record?.choice ?? null;
      stopAnalytics(storageAvailable);
      if (!record) panel!.hidden = false;
      updateStatus();
      return;
    }
    if (active) expiryTimer = setTimeout(reconcile, Math.min(record.expiresAt - Date.now(), 60_000));
    // Consent from another tab never starts analytics in this tab without navigation.
  }

  document.querySelectorAll<HTMLElement>('[data-consent-open]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      opener = button;
      updateStatus();
      panel.hidden = false;
      heading.focus();
    });
  });
  panel.querySelector('[data-consent-accept]')!.addEventListener('click', () => choose('granted'));
  panel.querySelector('[data-consent-reject]')!.addEventListener('click', () => choose('denied'));
  panel.querySelector('[data-consent-close]')!.addEventListener('click', closePanel);
  panel.addEventListener('keydown', event => { if (event.key === 'Escape') closePanel(); });
  window.addEventListener('storage', event => { if (event.key === STORAGE_KEY || event.key === null) reconcile(); });
  window.addEventListener('pageshow', event => { if (event.persisted) reconcile(); });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) reconcile(); });
  document.addEventListener('click', event => {
    if (!active || qaSuppressed || window['ga-disable-G-P1DQLR76C6']) return;
    const record = readConsent();
    if (!record || record.choice !== 'granted') { stopAnalytics(storageAvailable); return; }
    const target = event.target;
    if (!(target instanceof Element)) return;
    const link = target.closest<HTMLAnchorElement>('a[data-affiliate-merchant]');
    if (!link) return;
    const destination = new URL(link.href, location.href);
    window.gtag?.('event', 'affiliate_outbound_click', {
      affiliate_merchant: link.dataset.affiliateMerchant || 'unknown',
      affiliate_site: link.dataset.affiliateSite || 'dutch-ai-tools',
      link_domain: destination.hostname,
      link_url: destination.origin + destination.pathname,
      page_location: location.origin + location.pathname,
      transport_type: 'beacon',
    });
  });

  const initial = analyticsReady ? readConsent() : null;
  inMemoryChoice = sessionWithdrawn ? 'denied' : initial?.choice ?? null;
  if (!sessionWithdrawn && initial?.choice === 'granted') startAnalytics(initial);
  else stopAnalytics(false);
  panel.hidden = !analyticsReady || sessionWithdrawn || !!initial;
  updateStatus();
}
