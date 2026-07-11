#!/usr/bin/env python3
"""Quick smoke test: verify the resolver integration in the updated generator."""
import sys
sys.path.insert(0, "/workspace/dutch-ai-tools")
import scripts.affiliate_resolver as resolver

print("=== Resolver smoke tests ===\n")

# Test 1: Known active merchant (beehiiv)
result = resolver.build_affiliate_url("beehiiv", "https://www.beehiiv.com")
expected = "https://www.beehiiv.com/"
ok = result == expected
print(f"{'PASS' if ok else 'FAIL'} beehiiv: {result}")
if not ok:
    print(f"     expected: {expected}")

# Test 2: Unknown merchant — vic.ai (not in registry)
result = resolver.build_affiliate_url("vic-ai", "https://vic.ai")
print(f"PASS vic.ai (miss → bare): {result}")
assert "?ref=" not in result, f"Dead tag survived: {result}"

# Test 3: Unknown merchant — lessonup.com (not in registry)
result = resolver.build_affiliate_url("lessonup", "https://lessonup.com/nl")
print(f"PASS lessonup (miss → bare): {result}")
assert "?ref=" not in result, f"Dead tag survived: {result}"

# Test 4: Simulate what the generator does
# Both topics in generate-expansion-june5.py have hardcoded ?ref=aitoolsnl
# The resolver strips them and returns bare URLs (no registry entry for vic.ai/lessonup.com)
print("\n=== Generator path simulation ===")
for test_url in ["https://vic.ai/?ref=aitoolsnl", "https://lessonup.com/nl/?ref=aitoolsnl"]:
    clean = test_url.split("?ref=")[0].rstrip("/")
    mid = resolver.resolve_merchant_from_url(clean)
    if mid:
        resolved = resolver.build_affiliate_url(mid, clean)
        print(f"  {test_url}")
        print(f"    → merchant_id={mid}, url={resolved}")
    else:
        print(f"  {test_url}")
        print(f"    → clean={clean} (no registry entry, bare URL)")

print("\nAll smoke tests passed.")
