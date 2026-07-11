#!/usr/bin/env python3
"""
Shared affiliate URL resolver for Dutch AI Tools generator scripts.

Reads src/data/merchants.json at runtime and builds properly routed
affiliate URLs instead of hardcoding dead ?ref=aitoolsnl tags.

Usage:
    from affiliate_resolver import build_affiliate_url

    # Registry hit — active merchant with affiliate ID
    url = build_affiliate_url("beehiiv", "https://www.beehiiv.com")
    # → "https://www.beehiiv.com/"

    # Registry miss — merchant not in registry
    url = build_affiliate_url("some-new-tool", "https://somenewtool.com")
    # → "https://somenewtool.com"  (bare URL, no dead ?ref= tag)

    # Dead merchant — program was rejected or shut down
    url = build_affiliate_url("notion", "https://www.notion.so")
    # → "https://www.notion.so"  (bare URL, program is dead)

    # Resolve a domain to its merchant ID
    mid = resolve_merchant_from_url("https://www.beehiiv.com/features")
    # → "beehiiv"
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "src" / "data" / "merchants.json"

_registry: Optional[Dict[str, Any]] = None


def _load_registry() -> dict:
    """Load merchants.json, cached in memory for the process lifetime."""
    global _registry
    if _registry is None:
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            data = json.load(f)
            _registry = data
    return _registry  # type: ignore[return-value]


def _reload_registry() -> dict:
    """Force-reload the registry (useful in tests after registry updates)."""
    global _registry
    _registry = None
    return _load_registry()


def _find_merchant(merchant_id: str) -> Optional[dict]:
    """Case-insensitive merchant lookup in the registry."""
    registry = _load_registry()
    merchants = registry.get("merchants", {})

    # Direct hit
    if merchant_id in merchants:
        return merchants[merchant_id]

    # Case-insensitive scan
    lower_id = merchant_id.lower()
    for key, val in merchants.items():
        if key.lower() == lower_id:
            return val

    return None


def build_affiliate_url(
    merchant_id: str,
    product_url: str,
    site: str = "dutch-ai-tools",
    **extra_vars: str,
) -> str:
    """
    Build an affiliate-tracked URL for a merchant.

    If the merchant is registered, active, and has an affiliate ID for the
    target site, the linkTemplate is used. Otherwise the bare product_url
    is returned — no dead ?ref= tags.

    Args:
        merchant_id: Registry merchant ID (case-insensitive).
        product_url: The tool's canonical URL — returned as-is on miss.
        site: Per-site config key (default: "dutch-ai-tools").
        **extra_vars: Additional template placeholders
                      (e.g. asin="B0XYZ" for Amazon).

    Returns:
        Affiliate URL if the merchant is active + registered;
        otherwise the bare product_url.
    """
    if not product_url:
        return product_url

    merchant = _find_merchant(merchant_id)

    if merchant is None:
        return product_url

    # Only active merchants get affiliate links.
    # "pending" means we're waiting on approval — no link yet.
    status = merchant.get("status", "inactive")
    if status not in ("active",):
        return product_url

    per_site = merchant.get("perSite", {}).get(site, {})
    affiliate_id = per_site.get("affiliateId")

    if not affiliate_id:
        return product_url

    template = merchant.get("linkTemplate")
    if not template:
        return product_url

    # Build substitution dict
    vars_dict: Dict[str, str] = {
        "affiliateId": affiliate_id,
        "targetUrl": product_url,
    }
    vars_dict.update(extra_vars)

    # Try to format the template.
    # If any placeholder is left behind, fall back to the bare URL.
    try:
        result = template.format(**vars_dict)
        if "{" in result:
            return product_url
        return result
    except (KeyError, ValueError):
        return product_url


def resolve_merchant_from_url(url: str) -> Optional[str]:
    """
    Map a product URL to a merchant ID via domainHints.

    Returns the first merchant whose domainHints list contains
    a domain that appears in the URL's netloc.

    Args:
        url: A tool's website URL (e.g. "https://www.beehiiv.com/features").

    Returns:
        Merchant ID string if matched, None otherwise.
    """
    if not url:
        return None

    try:
        netloc = urlparse(url).netloc.lower()
    except Exception:
        return None

    registry = _load_registry()
    merchants = registry.get("merchants", {})

    for mid, merchant in merchants.items():
        for hint in merchant.get("domainHints", []):
            if hint.lower() in netloc:
                return mid

    return None


# ── inline tests (run: python3 scripts/affiliate_resolver.py) ──────────

def _run_tests() -> int:
    """Run unit tests. Returns exit code (0 = pass, 1 = fail)."""
    failures = 0
    total = 0

    def check(name: str, got: str, want: str) -> None:
        nonlocal failures, total
        total += 1
        ok = got == want
        tag = "PASS" if ok else "FAIL"
        print(f"  {tag}  {name}")
        if not ok:
            failures += 1
            print(f"        want: {want!r}")
            print(f"        got:  {got!r}")

    print("affiliate_resolver.py — unit tests\n")

    # ── 1. Registry hit: active merchant ──────────────────────────
    want = "https://www.beehiiv.com/"
    got = build_affiliate_url("beehiiv", "https://www.beehiiv.com")
    check("registry hit — beehiiv", got, want)

    # ── 2. Registry miss: unknown merchant ────────────────────────
    want = "https://vic.ai"
    got = build_affiliate_url("vic-ai", "https://vic.ai")
    check("registry miss — vic-ai", got, want)

    # ── 3. Dead merchant: program rejected / shut down ────────────
    want = "https://www.notion.so"
    got = build_affiliate_url("notion", "https://www.notion.so")
    check("dead merchant — notion", got, want)

    # ── 4. Empty product URL ──────────────────────────────────────
    got = build_affiliate_url("beehiiv", "")
    check("empty URL", got, "")

    # ── 5. Case-insensitive merchant ID ───────────────────────────
    want = "https://www.beehiiv.com/"
    got = build_affiliate_url("BEEHIIV", "https://www.beehiiv.com")
    check("case-insensitive — BEEHIIV", got, want)

    # ── 6. Pending merchant (no link until approved) ──────────────
    want = "https://www.coolblue.nl"
    got = build_affiliate_url("coolblue", "https://www.coolblue.nl")
    check("pending merchant — coolblue", got, want)

    # ── 7. Rejected merchant ──────────────────────────────────────
    want = "https://www.bol.com"
    got = build_affiliate_url("bol-com", "https://www.bol.com")
    check("rejected merchant — bol.com", got, want)

    # ── 8. resolve_merchant_from_url — hit ────────────────────────
    want_mid = "beehiiv"
    got_mid = resolve_merchant_from_url("https://www.beehiiv.com/features")
    ok = got_mid == want_mid
    total += 1
    tag = "PASS" if ok else "FAIL"
    print(f"  {tag}  resolve_merchant_from_url — beehiiv domain")
    if not ok:
        failures += 1
        print(f"        want: {want_mid!r}")
        print(f"        got:  {got_mid!r}")

    # ── 9. resolve_merchant_from_url — miss ───────────────────────
    got_none = resolve_merchant_from_url("https://unknown-tool.xyz")
    ok = got_none is None
    total += 1
    tag = "PASS" if ok else "FAIL"
    print(f"  {tag}  resolve_merchant_from_url — unknown domain")
    if not ok:
        failures += 1
        print(f"        want: None")
        print(f"        got:  {got_none!r}")

    # ── 10. resolve_merchant_from_url — empty ─────────────────────
    got_none2 = resolve_merchant_from_url("")
    ok = got_none2 is None
    total += 1
    tag = "PASS" if ok else "FAIL"
    print(f"  {tag}  resolve_merchant_from_url — empty URL")
    if not ok:
        failures += 1
        print(f"        want: None")
        print(f"        got:  {got_none2!r}")

    print(f"\n{total - failures}/{total} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(_run_tests())
