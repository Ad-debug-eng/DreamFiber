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
