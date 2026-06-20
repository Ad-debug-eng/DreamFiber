"""Single source of truth for DreamFiber business facts and JSON-LD builders."""
import json

DOMAIN = "https://dreamfiber.in"

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
