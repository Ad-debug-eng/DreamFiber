# DreamFiber SEO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add complete on-page SEO (unique meta, structured data, OG/Twitter, canonical, robots, sitemap) to the 9-page DreamFiber static site and ship an off-page action guide, so DreamFiber ranks for Chakan-area internet searches.

**Architecture:** A config-driven Python injector (`apply_seo.py`) writes repetitive SEO `<head>` blocks into each HTML page between idempotent markers, sourcing per-page values from `seo/seo_config.py` and business constants from `seo/seo_data.py`. A standalone `seo_check.py` validation harness asserts every SEO invariant and is our red/green test loop (stdlib only — no pip installs). robots.txt + sitemap.xml are generated from the same config.

**Tech Stack:** Static HTML/CSS/JS, Python 3 (stdlib: `re`, `json`, `xml.etree.ElementTree`, `pathlib`), Git.

**Conventions:**
- Domain: `https://dreamservices.in`
- Idempotent injection markers: `<!-- SEO:START -->` … `<!-- SEO:END -->` inside `<head>`.
- All Python is stdlib-only and run from the project root.
- Run validation after every task: `python seo_check.py` (exit 0 = all pass).

---

## File Structure

**Create:**
- `seo/seo_data.py` — business constants (NAP, brands, services, geo) + JSON-LD builders.
- `seo/seo_config.py` — per-page dict (title, description, canonical, og, breadcrumb, faq flag).
- `apply_seo.py` — injects the SEO head block into each HTML page (idempotent).
- `gen_sitemap.py` — writes `sitemap.xml` + `robots.txt` from the page list.
- `seo_check.py` — validation harness (our tests).
- `robots.txt`, `sitemap.xml` — generated outputs (committed).
- `SEO-ACTION-PLAN.md` — off-page guide (Google Business Profile, reviews, citations).

**Modify:**
- `index.html`, `about.html`, `contact.html`, `services.html`, `broadband.html`,
  `broadband-ott.html`, `ott.html`, `iptv.html`, `enterprise-solution.html`
  — receive injected SEO block; footer NAP standardized; FAQ content where applicable.

**Page list (PAGES constant, reused everywhere):**
```
index.html, about.html, contact.html, services.html, broadband.html,
broadband-ott.html, ott.html, iptv.html, enterprise-solution.html
```

---

## Task 1: Initialize Git for safety

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Init repo and add ignore file**

Create `.gitignore`:
```
__pycache__/
*.pyc
.DS_Store
```

- [ ] **Step 2: Baseline commit of current site**

```bash
git init
git add -A
git commit -m "chore: baseline before SEO work"
```
Expected: commit succeeds listing the existing HTML/CSS/JS/py files.

---

## Task 2: Business data + JSON-LD builders

**Files:**
- Create: `seo/seo_data.py`

- [ ] **Step 1: Write the data module**

Create `seo/seo_data.py`:
```python
"""Single source of truth for DreamFiber business facts and JSON-LD builders."""
import json

DOMAIN = "https://dreamservices.in"

LEGAL_NAME = "Dream Cable and Internet Services Private Limited"
ALT_NAMES = ["DreamFiber", "Dream Services", "Dream Internet Services", "Dream WIFI"]
FOUNDING_YEAR = "2006"

# Keep ALL numbers. Primary is the WhatsApp action number.
PHONE_PRIMARY = "+918788536698"
PHONES = ["+918788536698", "+919228172558", "+919272162704"]
WHATSAPP = "918788536698"

ADDRESS = {
    "streetAddress": "Chakan",
    "addressLocality": "Chakan",
    "addressRegion": "Maharashtra",
    "postalCode": "410501",
    "addressCountry": "IN",
}
# Approx Chakan centroid. TODO(owner): replace with exact office lat/long.
GEO = {"latitude": 18.7606, "longitude": 73.8636}
AREA_SERVED = ["Chakan", "Chakan MIDC"]

SERVICES = [
    "Lease Line", "Business Broadband", "Home Broadband",
    "Premium OTT Bundles", "IPTV",
]

# Filled by owner later; left empty so JSON-LD stays valid.
SAME_AS = []


def local_business_jsonld():
    """LocalBusiness / ISP block included on every page."""
    data = {
        "@context": "https://schema.org",
        "@type": ["InternetServiceProvider", "LocalBusiness"],
        "@id": f"{DOMAIN}/#business",
        "name": "DreamFiber",
        "legalName": LEGAL_NAME,
        "alternateName": ALT_NAMES,
        "url": DOMAIN + "/",
        "foundingDate": FOUNDING_YEAR,
        "telephone": PHONE_PRIMARY,
        "address": {"@type": "PostalAddress", **ADDRESS},
        "geo": {"@type": "GeoCoordinates", **GEO},
        "areaServed": [{"@type": "Place", "name": a} for a in AREA_SERVED],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "09:00", "closes": "21:00",
        }],
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": p, "contactType": "customer service",
            "areaServed": "IN", "availableLanguage": ["en", "hi", "mr"],
        } for p in PHONES],
        "makesOffer": [{
            "@type": "Offer",
            "itemOffered": {"@type": "Service", "name": s},
        } for s in SERVICES],
    }
    if SAME_AS:
        data["sameAs"] = SAME_AS
    return data


def breadcrumb_jsonld(crumbs):
    """crumbs = list of (name, url_path) tuples."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1, "name": name,
            "item": DOMAIN + path,
        } for i, (name, path) in enumerate(crumbs)],
    }


def faq_jsonld(qa_pairs):
    """qa_pairs = list of (question, answer) tuples."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in qa_pairs],
    }


def dumps(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)
```

- [ ] **Step 2: Smoke-test it imports and builds valid JSON**

Run:
```bash
python -c "import sys; sys.path.insert(0,'seo'); import seo_data; import json; json.loads(seo_data.dumps(seo_data.local_business_jsonld())); print('OK')"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add seo/seo_data.py
git commit -m "feat(seo): add business data and JSON-LD builders"
```

---

## Task 3: Per-page SEO config

**Files:**
- Create: `seo/seo_config.py`

- [ ] **Step 1: Write per-page config**

Create `seo/seo_config.py`:
```python
"""Per-page SEO values. Titles are unique (fixes duplicate-title problem)."""

# faq: optional list of (question, answer) tuples for FAQPage schema.
FAQ_HOME = [
    ("Which areas does DreamFiber cover?",
     "DreamFiber provides fiber broadband, IPTV and OTT in Chakan and Chakan MIDC, with service since 2006."),
    ("How fast is installation?",
     "In most serviceable areas of Chakan we install within 24-48 hours of feasibility confirmation."),
    ("Do you provide lease lines for business?",
     "Yes. DreamFiber offers dedicated lease lines and business broadband across Chakan MIDC."),
    ("Are OTT apps included with broadband?",
     "Yes, we offer Broadband + OTT bundles that include premium OTT subscriptions."),
]

PAGES = {
    "index.html": {
        "title": "DreamFiber | Best WiFi & Fiber Broadband in Chakan (Since 2006)",
        "description": "DreamFiber offers high-speed fiber broadband, IPTV and OTT bundles in Chakan & Chakan MIDC. Trusted internet & cable since 2006. Get WiFi near you today.",
        "path": "/",
        "breadcrumb": [("Home", "/")],
        "faq": FAQ_HOME,
    },
    "broadband.html": {
        "title": "Home Broadband Plans in Chakan | DreamFiber WiFi",
        "description": "Affordable home broadband and WiFi plans in Chakan from DreamFiber. High-speed fiber internet with quick installation and local support.",
        "path": "/broadband.html",
        "breadcrumb": [("Home", "/"), ("Home Broadband", "/broadband.html")],
        "faq": None,
    },
    "broadband-ott.html": {
        "title": "Broadband + OTT Bundles in Chakan | DreamFiber",
        "description": "Get fiber broadband bundled with premium OTT apps in Chakan from DreamFiber. One plan for fast internet and your favourite streaming.",
        "path": "/broadband-ott.html",
        "breadcrumb": [("Home", "/"), ("Broadband + OTT", "/broadband-ott.html")],
        "faq": None,
    },
    "ott.html": {
        "title": "Premium OTT Bundles (Netflix, Prime & more) | DreamFiber",
        "description": "Add premium OTT subscriptions to your DreamFiber connection in Chakan. Stream more for less with bundled OTT packs.",
        "path": "/ott.html",
        "breadcrumb": [("Home", "/"), ("OTT", "/ott.html")],
        "faq": None,
    },
    "iptv.html": {
        "title": "IPTV Plans & Channels in Chakan | DreamFiber",
        "description": "DreamFiber IPTV brings live TV channels over fiber in Chakan & Chakan MIDC. Crisp picture, reliable streaming and local support.",
        "path": "/iptv.html",
        "breadcrumb": [("Home", "/"), ("IPTV", "/iptv.html")],
        "faq": None,
    },
    "enterprise-solution.html": {
        "title": "Lease Line & Business Internet in Chakan MIDC | DreamFiber",
        "description": "Dedicated lease lines and business broadband for offices and factories in Chakan MIDC. Enterprise-grade uptime from DreamFiber since 2006.",
        "path": "/enterprise-solution.html",
        "breadcrumb": [("Home", "/"), ("Business / Lease Line", "/enterprise-solution.html")],
        "faq": None,
    },
    "services.html": {
        "title": "Internet, IPTV & OTT Plans in Chakan | DreamFiber",
        "description": "Browse all DreamFiber plans in Chakan: home broadband, business lease lines, IPTV and OTT bundles. Best internet for home and business.",
        "path": "/services.html",
        "breadcrumb": [("Home", "/"), ("Plans & Services", "/services.html")],
        "faq": None,
    },
    "about.html": {
        "title": "About DreamFiber | Internet & Cable in Chakan Since 2006",
        "description": "DreamFiber (Dream Cable and Internet Services Pvt. Ltd.) has provided internet and cable TV in Chakan since 2006. Learn about our local service.",
        "path": "/about.html",
        "breadcrumb": [("Home", "/"), ("About", "/about.html")],
        "faq": None,
    },
    "contact.html": {
        "title": "Contact DreamFiber | WiFi & Lease Line in Chakan",
        "description": "Contact DreamFiber for new WiFi, broadband, IPTV or lease line in Chakan & Chakan MIDC. Call or WhatsApp for a quick feasibility check.",
        "path": "/contact.html",
        "breadcrumb": [("Home", "/"), ("Contact", "/contact.html")],
        "faq": None,
    },
}

OG_IMAGE = "/assets/hero_bg.png"  # TODO(owner): swap for a 1200x630 share image if available.
```

- [ ] **Step 2: Verify all titles are unique and pages match the site**

Run:
```bash
python -c "import sys; sys.path.insert(0,'seo'); import seo_config as c; t=[p['title'] for p in c.PAGES.values()]; assert len(t)==len(set(t)), 'DUP TITLES'; print(len(c.PAGES),'pages, all titles unique')"
```
Expected: prints `9 pages, all titles unique`.

- [ ] **Step 3: Commit**

```bash
git add seo/seo_config.py
git commit -m "feat(seo): add per-page SEO config with unique titles"
```

---

## Task 4: Validation harness (our tests)

**Files:**
- Create: `seo_check.py`

- [ ] **Step 1: Write the harness — it will FAIL against the current site**

Create `seo_check.py`:
```python
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
```

- [ ] **Step 2: Run it to confirm it fails (red)**

Run:
```bash
python seo_check.py
```
Expected: FAIL — lists missing canonical/og/twitter/JSON-LD on every page, plus robots.txt and sitemap.xml missing.

- [ ] **Step 3: Commit**

```bash
git add seo_check.py
git commit -m "test(seo): add validation harness (currently failing)"
```

---

## Task 5: SEO injector — head block on every page

**Files:**
- Create: `apply_seo.py`
- Modify: all 9 HTML files (via the script)

- [ ] **Step 1: Write the injector**

Create `apply_seo.py`:
```python
"""Inject SEO <head> block into each HTML page between idempotent markers.
Re-running replaces the block (does not duplicate). Stdlib only."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "seo"))
import seo_config as cfg
import seo_data as data

START = "<!-- SEO:START -->"
END = "<!-- SEO:END -->"


def build_block(page):
    meta = cfg.PAGES[page]
    canonical = data.DOMAIN + meta["path"]
    og_image = data.DOMAIN + cfg.OG_IMAGE
    desc = meta["description"].replace('"', "&quot;")
    title = meta["title"].replace('"', "&quot;")

    jsonld = [data.local_business_jsonld(),
              data.breadcrumb_jsonld(meta["breadcrumb"])]
    if meta.get("faq"):
        jsonld.append(data.faq_jsonld(meta["faq"]))
    scripts = "\n".join(
        f'    <script type="application/ld+json">\n{data.dumps(j)}\n    </script>'
        for j in jsonld)

    return f"""{START}
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="index, follow">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://unpkg.com">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="DreamFiber">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{og_image}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{og_image}">
{scripts}
    {END}"""


def apply(page):
    path = ROOT / page
    html = path.read_text(encoding="utf-8")
    meta = cfg.PAGES[page]

    # 1. Replace <title>
    html = re.sub(r"<title>.*?</title>",
                  f"<title>{meta['title']}</title>", html, count=1, flags=re.S)

    # 2. Replace <meta name="description">
    new_desc = f'<meta name="description" content="{meta["description"]}">'
    if re.search(r'<meta name="description"[^>]*>', html):
        html = re.sub(r'<meta name="description"[^>]*>', new_desc, html, count=1)
    else:
        html = re.sub(r"(</title>)", r"\1\n    " + new_desc, html, count=1)

    # 3. Insert/replace SEO block before </head>
    block = build_block(page)
    if START in html:
        html = re.sub(re.escape(START) + r".*?" + re.escape(END), block,
                      html, count=1, flags=re.S)
    else:
        html = html.replace("</head>", f"    {block}\n</head>", 1)

    path.write_text(html, encoding="utf-8")
    print("updated", page)


if __name__ == "__main__":
    for p in cfg.PAGES:
        apply(p)
```

- [ ] **Step 2: Run the injector**

Run:
```bash
python apply_seo.py
```
Expected: prints `updated <page>` for all 9 pages.

- [ ] **Step 3: Run validation (sitemap/robots still missing — expected)**

Run:
```bash
python seo_check.py
```
Expected: FAIL reduced to only `robots.txt missing` and `sitemap.xml missing` (all per-page checks now PASS). If any per-page check still fails, fix `apply_seo.py` and re-run.

- [ ] **Step 4: Commit**

```bash
git add apply_seo.py *.html
git commit -m "feat(seo): inject meta, canonical, OG/Twitter and JSON-LD into all pages"
```

---

## Task 6: robots.txt + sitemap.xml

**Files:**
- Create: `gen_sitemap.py`, `robots.txt`, `sitemap.xml`

- [ ] **Step 1: Write the generator**

Create `gen_sitemap.py`:
```python
"""Generate sitemap.xml and robots.txt from the page config. Stdlib only."""
import sys, pathlib

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "seo"))
import seo_config as cfg
import seo_data as data

LASTMOD = "2026-06-17"  # bump when content changes


def gen_sitemap():
    urls = []
    for page in cfg.PAGES:
        loc = data.DOMAIN + cfg.PAGES[page]["path"]
        prio = "1.0" if cfg.PAGES[page]["path"] == "/" else "0.8"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            f"    <priority>{prio}</priority>\n  </url>")
    body = "\n".join(urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{body}\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("wrote sitemap.xml")


def gen_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n\n"
           f"Sitemap: {data.DOMAIN}/sitemap.xml\n")
    (ROOT / "robots.txt").write_text(txt, encoding="utf-8")
    print("wrote robots.txt")


if __name__ == "__main__":
    gen_sitemap()
    gen_robots()
```

- [ ] **Step 2: Generate the files**

Run:
```bash
python gen_sitemap.py
```
Expected: prints `wrote sitemap.xml` and `wrote robots.txt`.

- [ ] **Step 3: Run full validation — should PASS now (green)**

Run:
```bash
python seo_check.py
```
Expected: `PASS: all SEO checks passed across 9 pages`.

- [ ] **Step 4: Commit**

```bash
git add gen_sitemap.py robots.txt sitemap.xml
git commit -m "feat(seo): generate robots.txt and sitemap.xml"
```

---

## Task 7: Real FAQ content on the homepage

The homepage currently has an `onclick="alert('FAQs coming soon!')"` link. The
FAQPage JSON-LD (added in Task 5 via `FAQ_HOME`) needs matching visible content,
or Google may flag schema without on-page text.

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Add a visible FAQ section before the footer**

In `index.html`, locate `<footer>` and insert immediately before it. Use the
exact same 4 Q&As as `FAQ_HOME` in `seo/seo_config.py`:
```html
    <section class="section container" id="faq" style="max-width: 800px; margin: 0 auto;">
        <h2 class="text-gradient" style="text-align:center; margin-bottom:2rem;">Frequently Asked Questions</h2>
        <div class="faq-item" style="margin-bottom:1.5rem;">
            <h3 style="font-size:1.1rem;">Which areas does DreamFiber cover?</h3>
            <p style="color:var(--text-muted);">DreamFiber provides fiber broadband, IPTV and OTT in Chakan and Chakan MIDC, with service since 2006.</p>
        </div>
        <div class="faq-item" style="margin-bottom:1.5rem;">
            <h3 style="font-size:1.1rem;">How fast is installation?</h3>
            <p style="color:var(--text-muted);">In most serviceable areas of Chakan we install within 24-48 hours of feasibility confirmation.</p>
        </div>
        <div class="faq-item" style="margin-bottom:1.5rem;">
            <h3 style="font-size:1.1rem;">Do you provide lease lines for business?</h3>
            <p style="color:var(--text-muted);">Yes. DreamFiber offers dedicated lease lines and business broadband across Chakan MIDC.</p>
        </div>
        <div class="faq-item" style="margin-bottom:1.5rem;">
            <h3 style="font-size:1.1rem;">Are OTT apps included with broadband?</h3>
            <p style="color:var(--text-muted);">Yes, we offer Broadband + OTT bundles that include premium OTT subscriptions.</p>
        </div>
    </section>
```

- [ ] **Step 2: Verify the FAQ text matches the schema and site still validates**

Run:
```bash
python seo_check.py
```
Expected: `PASS: all SEO checks passed across 9 pages`.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat(seo): add visible FAQ section matching FAQPage schema"
```

---

## Task 8: Standardize footer NAP across all pages

Footers currently vary (e.g. some show only some numbers). Local SEO needs an
identical name + address + phones on every page. Keep ALL numbers.

**Files:**
- Modify: all 9 HTML files (via a small script)

- [ ] **Step 1: Write a footer-contact normalizer**

Create `normalize_footer.py`:
```python
"""Make the footer contact block identical across all pages. Stdlib only."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "seo"))
import seo_config as cfg

FOOTER_CONTACT = """<div class="footer-contact">
                <h4>Support</h4>
                <p>DreamFiber (Dream Cable and Internet Services Pvt. Ltd.)</p>
                <p>Chakan & Chakan MIDC, Pune — Since 2006</p>
                <p>Call: 8788536698, 9228172558</p>
                <p>WhatsApp: 9272162704</p>
            </div>"""


def apply(page):
    path = ROOT / page
    html = path.read_text(encoding="utf-8")
    new, n = re.subn(
        r'<div class="footer-contact">.*?</div>\s*(?=</div>\s*<div class="footer-bottom"|</div>\s*</footer>|<div class="footer-bottom")',
        FOOTER_CONTACT + "\n        ", html, count=1, flags=re.S)
    if n == 0:
        # Fallback: replace the first footer-contact block up to its closing </div>
        new, n = re.subn(r'<div class="footer-contact">.*?</div>',
                         FOOTER_CONTACT, html, count=1, flags=re.S)
    path.write_text(new, encoding="utf-8")
    print(f"{page}: footer updated ({n} replaced)")


if __name__ == "__main__":
    for p in cfg.PAGES:
        apply(p)
```

- [ ] **Step 2: Run it and manually verify one page**

Run:
```bash
python normalize_footer.py
```
Expected: prints `footer updated (1 replaced)` for each page. Then open
`contact.html` and confirm the footer-contact block renders the standardized
name, area, and all numbers, with no broken `</div>` nesting.

- [ ] **Step 3: Re-validate**

Run:
```bash
python seo_check.py
```
Expected: `PASS: all SEO checks passed across 9 pages`.

- [ ] **Step 4: Commit**

```bash
git add normalize_footer.py *.html
git commit -m "feat(seo): standardize footer NAP across all pages"
```

---

## Task 9: Off-page action guide

**Files:**
- Create: `SEO-ACTION-PLAN.md`

- [ ] **Step 1: Write the guide**

Create `SEO-ACTION-PLAN.md` with these sections (write full prose for each):

1. **Why on-page alone won't beat the Akurdi listing** — explain the map pack /
   Google Business Profile is the dominant factor for "Dream Cable" / "near me".
2. **Set up your own Google Business Profile** — create/claim as **DreamFiber** at
   the Chakan address (distinct from Akurdi). Primary category: *Internet service
   provider*; secondary: *Cable company*, *Telecommunications service provider*.
   Set service area = Chakan + Chakan MIDC. Add phones (8788536698 primary,
   9228172558, WhatsApp 9272162704), website https://dreamservices.in, hours,
   photos, and the services list.
3. **Make it clearly distinct from the uncle's listing** — different name
   (DreamFiber), different address, different phone. You cannot remove his
   listing; you out-rank it with completeness + reviews.
4. **Reviews flow** — share this Google review link via WhatsApp after each
   install: template message provided. Aim for steady, genuine 5-star reviews.
5. **Citations / directories** — list on JustDial, Sulekha, IndiaMART, Bing
   Places, Google Maps with IDENTICAL name/address/phone (NAP) to the website.
6. **Verify the on-page work** — submit sitemap in Google Search Console
   (`https://dreamservices.in/sitemap.xml`), test pages in the Rich Results Test,
   and request indexing for the homepage.
7. **Owner to-fill checklist** — exact office lat/long, social profile URLs
   (update `seo/seo_data.py` `SAME_AS` and `GEO`), optional 1200x630 share image.

- [ ] **Step 2: Commit**

```bash
git add SEO-ACTION-PLAN.md
git commit -m "docs(seo): add off-page action plan for Google Business Profile and citations"
```

---

## Task 10: Final verification

- [ ] **Step 1: Full validation passes**

Run:
```bash
python seo_check.py
```
Expected: `PASS: all SEO checks passed across 9 pages`.

- [ ] **Step 2: Confirm idempotency (re-running injectors changes nothing)**

Run:
```bash
python apply_seo.py && python gen_sitemap.py && git status --porcelain
```
Expected: `git status --porcelain` prints nothing (no diff) — proves the
injectors are idempotent and safe to re-run after future edits.

- [ ] **Step 3: Manual external validation (owner / reviewer)**

- Open `index.html` in a browser; confirm FAQ renders and page looks unchanged otherwise.
- Paste the homepage source into Google Rich Results Test; confirm LocalBusiness,
  Breadcrumb, and FAQ are detected with no errors.
- Confirm `https://dreamservices.in/sitemap.xml` and `/robots.txt` will resolve once deployed.

---

## Notes for the implementer

- **Stdlib only.** Do not `pip install` anything.
- **Idempotent by design.** `apply_seo.py`, `gen_sitemap.py`, and
  `normalize_footer.py` can all be re-run safely; they replace, not append.
- **The harness is the contract.** If you change page structure, keep
  `python seo_check.py` green.
- **Owner TODOs** are marked `TODO(owner)` in `seo/seo_data.py` and
  `seo/seo_config.py` (exact geo, share image, social links) — non-blocking.
