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
