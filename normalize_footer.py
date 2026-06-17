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
    new, n = re.subn(r'<div class="footer-contact">.*?</div>',
                     FOOTER_CONTACT, html, count=1, flags=re.S)
    path.write_text(new, encoding="utf-8")
    print(f"{page}: footer updated ({n} replaced)")
    return n


if __name__ == "__main__":
    for p in cfg.PAGES:
        apply(p)
