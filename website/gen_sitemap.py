"""Generate sitemap.xml and robots.txt from the page config. Stdlib only."""
import sys, pathlib

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "seo"))
import seo_config as cfg
import seo_data as data

LASTMOD = "2026-06-20"  # bump when content changes


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
