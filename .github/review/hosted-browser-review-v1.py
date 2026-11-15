#!/usr/bin/env python3
"""Independent, bounded browser review of homepage candidate 134a7e94.

Run only on the isolated hosted runner after an exact checkout and build.
Requires Python 3, Chrome and ChromeDriver already present on the runner.
Outputs public-page screenshots as size-capped, hashed log chunks.
"""
import base64
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

CANDIDATE = "134a7e94cd3e037cf561e72b59c0e8014dcfebf4"
PARENT = "5e37f02d118b84d300c022d63cd4a2d30813d469"
OLD_PATH = "/beste-ai-automation-tools-2026/"
NEW_PATH = "/n8n-vs-make-vs-zapier-2026/"
OLD_TEXT = "Kies tussen Make, Zapier, n8n en Pipedream voor je terugkerende werk."
NEW_TEXT = "Kies tussen n8n, Make en Zapier op werkstroom, beheer en verbruik."
CONTROL = "https://dutchaitools.nl/"
TEST_HOST = "review.dutchaitools.test"
MAX_IMAGE_BYTES = 400_000
MAX_TOTAL_BYTES = 1_400_000
LOG_CHUNK_CHARS = 3000

checks = []
screens = []
driver = None
httpd = None

def check(name, passed, detail=None):
    checks.append({"name": name, "pass": bool(passed), "detail": detail})
    if not passed:
        raise AssertionError(name + ": " + str(detail))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def wait_for(predicate, seconds=12):
    until = time.monotonic() + seconds
    last = None
    while time.monotonic() < until:
        try:
            last = predicate()
            if last:
                return last
        except (OSError, ValueError, urllib.error.URLError):
            pass
        time.sleep(0.15)
    raise TimeoutError("Timed out waiting for " + str(last))

def request(method, url, body=None):
    payload = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            obj = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError("WebDriver HTTP " + str(exc.code) + " " +
                           exc.read().decode("utf-8", "replace")[:1500]) from exc
    value = obj.get("value")
    if isinstance(value, dict) and value.get("error"):
        raise RuntimeError("WebDriver " + json.dumps(value)[:1500])
    return value

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

class Browser:
    def __init__(self, port, binary, mobile):
        self.base = "http://127.0.0.1:" + str(port)
        options = {"args": [
            "--headless=new", "--no-sandbox", "--disable-dev-shm-usage",
            "--disable-gpu", "--disable-extensions", "--no-proxy-server",
            "--host-resolver-rules=MAP " + TEST_HOST + " 127.0.0.1",
            "--window-size=1440,900",
        ]}
        if binary:
            options["binary"] = binary
        session = request("POST", self.base + "/session", {
            "capabilities": {"alwaysMatch": {
                "browserName": "chrome",
                "goog:chromeOptions": options,
                "goog:loggingPrefs": {"performance": "ALL", "browser": "ALL"},
            }}
        })
        self.sid = session["sessionId"]
        self.api = self.base + "/session/" + self.sid
        self.call("POST", "/goog/cdp/execute", {"cmd": "Network.enable", "params": {}})
        if mobile:
            self.call("POST", "/goog/cdp/execute", {
                "cmd": "Emulation.setDeviceMetricsOverride",
                "params": {"width": 390, "height": 844,
                           "deviceScaleFactor": 1, "mobile": True,
                           "screenWidth": 390, "screenHeight": 844}
            })
        else:
            self.call("POST", "/window/rect", {"width": 1440, "height": 900})

    def call(self, method, path, body=None):
        return request(method, self.api + path, body)

    def go(self, url):
        self.call("POST", "/url", {"url": url})
        wait_for(lambda: self.js("return document.readyState === 'complete';"))

    def js(self, script, args=None):
        return self.call("POST", "/execute/sync", {"script": script, "args": args or []})

    def press(self, key):
        self.call("POST", "/actions", {"actions": [{"type": "key", "id": "keyboard",
            "actions": [{"type": "keyDown", "value": key},
                        {"type": "keyUp", "value": key}]}]})

    def logs(self):
        try:
            return self.call("POST", "/se/log", {"type": "performance"})
        except RuntimeError:
            return self.call("POST", "/log", {"type": "performance"})

    def screenshot(self, label):
        encoded = self.call("GET", "/screenshot")
        raw = base64.b64decode(encoded, validate=True)
        check(label + "_screenshot_is_bounded_png",
              raw.startswith(b"\x89PNG\r\n\x1a\n") and len(raw) <= MAX_IMAGE_BYTES,
              {"bytes": len(raw)})
        screens.append({"label": label, "raw": raw, "sha256": digest(raw)})

    def close(self):
        try:
            self.call("DELETE", "")
        except Exception:
            pass

def route_details(browser):
    return browser.js("""
      const matches = [...document.querySelectorAll('nav.task-list a')]
        .filter(a => a.querySelector('strong')?.textContent.trim() === 'Werk automatiseren');
      const a = matches[0], r = a?.getBoundingClientRect();
      return {count:matches.length, href:a?.getAttribute('href'),
        text:a?.querySelector('span')?.textContent.trim(),
        title:a?.querySelector('strong')?.textContent.trim(),
        navLabel:a?.closest('nav')?.getAttribute('aria-label'),
        viewport:{width:innerWidth,height:innerHeight},
        documentWidth:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),
        rect:r ? {x:r.x,y:r.y,width:r.width,height:r.height} : null};
    """)

def center_route(browser):
    browser.js("""
      const a = [...document.querySelectorAll('nav.task-list a')]
        .find(x => x.querySelector('strong')?.textContent.trim() === 'Werk automatiseren');
      if (a) a.scrollIntoView({block:'center',inline:'nearest'});
    """)
    time.sleep(0.4)

def emitted_requests(logs):
    found = []
    for row in logs:
        try:
            item = json.loads(row["message"])["message"]
            if item.get("method") == "Network.requestWillBeSent":
                found.append(item["params"]["request"]["url"])
        except (KeyError, ValueError, TypeError):
            continue
    return found

def exercise(label, mobile, driver_port, chrome, origin):
    browser = Browser(driver_port, chrome, mobile)
    try:
        browser.go(CONTROL)
        control = route_details(browser)
        check(label + "_control_is_expected_parent_route",
              control["count"] == 1 and control["href"] == OLD_PATH and
              control["text"] == OLD_TEXT, control)
        center_route(browser)
        browser.screenshot(label + "_control")

        # Clear public-control network events before testing the isolated candidate.
        browser.logs()
        browser.go(origin + "/")
        # Install a valid old grant on a production-like non-loopback hostname.
        # The candidate's localhost QA suppression would otherwise mask privacy failures.
        browser.js("""
          const now=Date.now(), lifetime=180*24*60*60*1000;
          localStorage.setItem('dat_analytics_consent', JSON.stringify(
            {version:1,choice:'granted',savedAt:now,expiresAt:now+lifetime}));
          sessionStorage.removeItem('orbit_analytics_qa');
          sessionStorage.removeItem('dat_analytics_withdrawn');
        """)
        browser.logs()
        browser.go(origin + "/")
        route = route_details(browser)
        check(label + "_candidate_route_exact",
              route["count"] == 1 and route["href"] == NEW_PATH and
              route["text"] == NEW_TEXT and route["navLabel"] == "Begin bij je taak", route)
        check(label + "_layout_has_no_page_horizontal_overflow",
              route["documentWidth"] <= route["viewport"]["width"] + 1, route)
        check(label + "_route_has_size", route["rect"] and
              route["rect"]["width"] > 100 and route["rect"]["height"] > 20, route)
        privacy = browser.js("""
          return {hostname:location.hostname, suppressed:window.__orbitAnalyticsSuppressed,
            gaDisabled:window['ga-disable-G-P1DQLR76C6'],
            stored:JSON.parse(localStorage.getItem('dat_analytics_consent')||'null'),
            heading:document.querySelector('#consent-heading')?.textContent.trim()};
        """)
        check(label + "_privacy_nonloopback_stale_grant_stays_disabled",
              privacy["hostname"] == TEST_HOST and privacy["suppressed"] is False and
              privacy["gaDisabled"] is True and
              privacy["stored"] and privacy["stored"]["choice"] == "granted" and
              privacy["heading"] == "Statistieken staan uit", privacy)
        center_route(browser)
        browser.screenshot(label + "_candidate")

        # Reload so Tab begins from a fresh page, then use real keyboard actions.
        browser.go(origin + "/")
        focused = None
        for i in range(80):
            browser.press("\ue004")  # WebDriver Tab
            focused = browser.js("""
              const a=document.activeElement;
              return {tag:a?.tagName, href:a?.getAttribute('href'),
                      title:a?.querySelector('strong')?.textContent.trim()};
            """)
            if focused and focused.get("title") == "Werk automatiseren":
                break
        check(label + "_keyboard_tab_reaches_route",
              focused and focused.get("tag") == "A" and
              focused.get("href") == NEW_PATH, {"focus": focused, "tabs": i + 1})
        browser.press("\ue007")  # WebDriver Enter
        url = wait_for(lambda: (u if urllib.parse.urlparse(
            u := browser.call("GET", "/url")).path == NEW_PATH else None))
        check(label + "_keyboard_enters_existing_guide",
              urllib.parse.urlparse(url).path == NEW_PATH, {"url": url})
        dest = browser.js("""
          const t=document.body.innerText;
          let schemas=[]; let parseErrors=0;
          for (const e of document.querySelectorAll('script[type="application/ld+json"]')) {
            try {const j=JSON.parse(e.textContent);schemas.push(j['@type']);} catch {parseErrors++;}
          }
          return {title:document.title, h1:document.querySelector('h1')?.innerText,
            disclosure:t.includes('Advertentie-informatie.') && t.includes('partnerlinks'),
            faq:!!document.querySelector('.faq-list details summary'),
            schemas,parseErrors,
            viewport:{width:innerWidth,height:innerHeight},
            documentWidth:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)};
        """)
        check(label + "_guide_title_and_disclosure",
              "n8n" in (dest["h1"] or "") and dest["disclosure"], dest)
        check(label + "_guide_schema_and_faq",
              dest["faq"] and dest["parseErrors"] == 0 and
              "Article" in dest["schemas"] and "FAQPage" in dest["schemas"], dest)
        check(label + "_guide_no_page_horizontal_overflow",
              dest["documentWidth"] <= dest["viewport"]["width"] + 1, dest)
        requests = emitted_requests(browser.logs())
        hosts = sorted({urllib.parse.urlparse(u).hostname or "" for u in requests})
        forbidden = [u for u in requests if any(x in u.lower() for x in
                     ("googletagmanager.com", "google-analytics.com", "analytics.google.com"))]
        check(label + "_network_logging_observed_local_requests",
              any(urllib.parse.urlparse(u).hostname == TEST_HOST for u in requests),
              {"count": len(requests), "hosts": hosts})
        check(label + "_no_google_analytics_requests_with_stale_grant",
              not forbidden, {"forbidden_count": len(forbidden), "hosts": hosts})
    finally:
        browser.close()

def emit_screens():
    total = sum(len(s["raw"]) for s in screens)
    if total > MAX_TOTAL_BYTES:
        print("EVIDENCE_IMAGES_REJECTED " + json.dumps({"total_bytes": total}))
        return False
    for item in screens:
        raw = item.pop("raw")
        b64 = base64.b64encode(raw).decode("ascii")
        parts = [b64[i:i + LOG_CHUNK_CHARS] for i in range(0, len(b64), LOG_CHUNK_CHARS)]
        print("EVIDENCE_IMAGE_META " + json.dumps({
            "label": item["label"], "bytes": len(raw), "sha256": item["sha256"],
            "chunks": len(parts)}), flush=True)
        for index, part in enumerate(parts, 1):
            print("EVIDENCE_IMAGE_CHUNK " + item["label"] + " " +
                  str(index) + "/" + str(len(parts)) + " " + part, flush=True)
    return True

def main():
    global driver, httpd
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist").resolve()
    check("candidate_head", git("rev-parse", "HEAD") == CANDIDATE, git("rev-parse", "HEAD"))
    check("candidate_parent", git("rev-parse", "HEAD^") == PARENT, git("rev-parse", "HEAD^"))
    check("candidate_source_unchanged_after_build",
          not git("diff", "--name-only", "HEAD", "--", "src", "public",
                  "package.json", "package-lock.json", "astro.config.mjs"))
    homepage = dist / "index.html"
    guide = dist / NEW_PATH.strip("/") / "index.html"
    check("built_home_and_guide_exist", homepage.is_file() and guide.is_file(),
          {"home": str(homepage), "guide": str(guide)})
    print("REVIEW_BUILD_IDENTITY " + json.dumps({
        "candidate": CANDIDATE, "parent": PARENT,
        "test_sha256": digest(Path(__file__).read_bytes()),
        "home_sha256": digest(homepage.read_bytes()),
        "guide_sha256": digest(guide.read_bytes()),
        "python": sys.version.split()[0]}), flush=True)
    handler = functools.partial(QuietHandler, directory=str(dist))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    origin = "http://" + TEST_HOST + ":" + str(httpd.server_address[1])
    chromedriver = shutil.which("chromedriver")
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    check("runner_browser_available", bool(chromedriver and chrome),
          {"chromedriver": chromedriver, "chrome": chrome})
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        driver_port = sock.getsockname()[1]
    driver = subprocess.Popen([chromedriver, "--port=" + str(driver_port)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for(lambda: request("GET", "http://127.0.0.1:" + str(driver_port) + "/status"))
    exercise("desktop", False, driver_port, chrome, origin)
    exercise("phone", True, driver_port, chrome, origin)

error = None
try:
    main()
except Exception as exc:
    error = type(exc).__name__ + ": " + str(exc)
finally:
    if httpd:
        httpd.shutdown()
        httpd.server_close()
    if driver:
        driver.terminate()
        try:
            driver.wait(timeout=5)
        except subprocess.TimeoutExpired:
            driver.kill()
            driver.wait(timeout=5)
    try:
        images_ok = emit_screens()
    except Exception as exc:
        images_ok = False
        error = error or ("Evidence transport: " + str(exc))
    status = "PASS" if error is None and images_ok and len(screens) == 4 else "HOLD"
    print("REVIEW_BROWSER_RESULT " + json.dumps({
        "status": status, "error": error, "checks": checks,
        "screen_labels": [s["label"] for s in screens],
        "transport": "public screenshots only; bounded SHA256-checked chunks",
        "limits": "Automated checks and screenshots require independent receipt and visual inspection."
    }), flush=True)
if error is not None or not images_ok or len(screens) != 4:
    sys.exit(1)
