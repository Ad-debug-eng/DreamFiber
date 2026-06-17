"""SEO validation harness. Exit 0 = all checks pass. Stdlib only."""
import sys, re, json, pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "seo"))
import seo_config as cfg
import seo_data as data

PAGES = list(cfg.PAGES.keys())
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def jsonld_blocks(html):
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    out = []
    for b in blocks:
        try:
            out.append(json.loads(b))
        except json.JSONDecodeError as e:
            failures.append(f"invalid JSON-LD: {e}")
    return out


# Per-page checks
titles = []
for page in PAGES:
    html = read(page)
    meta = cfg.PAGES[page]

    m = re.search(r"<title>(.*?)</title>", html, re.S)
    check(m and m.group(1).strip() == meta["title"], f"{page}: title mismatch")
    if m:
        titles.append(m.group(1).strip())

    check(f'rel="canonical"' in html and data.DOMAIN in html,
          f"{page}: missing canonical to domain")
    check('property="og:title"' in html, f"{page}: missing og:title")
    check('property="og:image"' in html, f"{page}: missing og:image")
    check('name="twitter:card"' in html, f"{page}: missing twitter:card")

    d = re.search(r'<meta name="description" content="(.*?)"', html)
    check(d is not None, f"{page}: missing meta description")
    if d:
        ln = len(d.group(1))
        check(50 <= ln <= 165, f"{page}: description length {ln} out of 50-165")

    blocks = jsonld_blocks(html)
    types = [b.get("@type") for b in blocks]
    has_lb = any(("LocalBusiness" in t if isinstance(t, list) else t == "LocalBusiness")
                 for t in types)
    check(has_lb, f"{page}: missing LocalBusiness JSON-LD")
    check(data.PHONE_PRIMARY.replace("+", "") in html.replace("+", "") or
          data.PHONE_PRIMARY in html, f"{page}: primary phone not present")

check(len(titles) == len(set(titles)), "duplicate <title> across pages")

# Sitewide files
check((ROOT / "robots.txt").exists(), "robots.txt missing")
sm = ROOT / "sitemap.xml"
check(sm.exists(), "sitemap.xml missing")
if sm.exists():
    try:
        tree = ET.parse(sm)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = [e.text for e in tree.iter(f"{ns}loc")]
        for page in PAGES:
            path = cfg.PAGES[page]["path"]
            url = data.DOMAIN + path
            check(url in locs, f"sitemap missing {url}")
    except ET.ParseError as e:
        failures.append(f"sitemap.xml invalid XML: {e}")

if failures:
    print(f"FAIL ({len(failures)} issues):")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print(f"PASS: all SEO checks passed across {len(PAGES)} pages")
