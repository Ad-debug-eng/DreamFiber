# DreamFiber SEO — Design Spec

**Date:** 2026-06-17
**Site:** https://dreamservices.in/ (static HTML, 9 pages, no framework)
**Goal:** Make **DreamFiber** the dominant, ownable brand on Google for Chakan-area
internet searches, capture brand searches for the legal entity, and clearly
separate this business from the uncle's "Dream Cable" Akurdi Google listing.

---

## Business facts (source of truth for NAP & content)

- **Legal name:** Dream Cable and Internet Services Private Limited
- **Marketing brands (alternateName):** DreamFiber, Dream Services, Dream Internet Services
- **In business since:** 2006
- **Location:** Chakan, Pune
- **Service area:** Chakan + Chakan MIDC
- **Phones (keep ALL, do not remove):**
  - Primary (also WhatsApp action): **8788536698**
  - Secondary call: **9228172558**
  - WhatsApp (footer): **9272162704**
- **Services:** Lease Line, Business Broadband, Home Broadband, Premium OTT bundles, IPTV

## Target keywords

Brand: DreamFiber, Dream Services, Dream Internet Services, Dream WIFI,
Dream Cable and Internet Services Private Limited Chakan.
Local/intent: wifi near me, best wifi in Chakan, leaseline in Chakan,
lease line in Chakan MIDC, home user wifi, best internet for business,
fiber broadband Chakan, IPTV Chakan, OTT bundles Chakan.

---

## Current state (audit findings)

- Only basic `<title>` + `<meta description>` per page. Nothing else.
- **Duplicate titles:** `services.html`, `broadband.html`, `iptv.html`,
  `broadband-ott.html` all use identical `"Plans & Pricing | Dream IPTV & Internet"`.
- No structured data (JSON-LD), no Open Graph / Twitter cards, no canonical tags.
- No `robots.txt`, no `sitemap.xml`.
- Brand mismatch: site reads "Dream IPTV & Internet"; target brand is DreamFiber.
- NAP inconsistency across pages (numbers vary). Resolution: keep all numbers
  but display the SAME set consistently on every page.

---

## Scope

In scope: **on-page code changes** to the website files + an **off-page action
guide** doc. Out of scope: full visual rebrand (logo/design stays), backend,
form handling changes.

---

## Workstream A — On-page code changes

### A1. Per-page unique titles + meta descriptions
Rewrite all 9 titles/descriptions to be unique and keyword-rich, leading with
DreamFiber + Chakan intent. Examples:
- `index.html` → `DreamFiber | Best WiFi & Fiber Broadband in Chakan (Since 2006)`
- `broadband.html` → `Home Broadband Plans in Chakan | DreamFiber WiFi`
- `broadband-ott.html` → `Broadband + OTT Bundles in Chakan | DreamFiber`
- `enterprise-solution.html` → `Lease Line & Business Internet in Chakan MIDC | DreamFiber`
- `iptv.html` → `IPTV Plans & Channels in Chakan | DreamFiber`
- `ott.html` → `Premium OTT Bundles (Netflix, Prime & more) | DreamFiber`
- `services.html` → `Internet, IPTV & OTT Plans in Chakan | DreamFiber`
- `about.html` → `About DreamFiber | Internet & Cable in Chakan Since 2006`
- `contact.html` → `Contact DreamFiber | WiFi & Lease Line in Chakan`

### A2. Structured data (JSON-LD) — biggest local-SEO lever
- Sitewide `InternetServiceProvider` / `LocalBusiness` block: legal name,
  `alternateName` [DreamFiber, Dream Services, Dream Internet Services],
  `foundingDate` 2006, NAP, `areaServed` [Chakan, Chakan MIDC], geo-coordinates,
  `openingHours`, `url`, `sameAs` (social/GBP once available).
- `Service` entries: Lease Line, Business Broadband, Home Broadband, OTT, IPTV.
- `BreadcrumbList` per page.
- `FAQPage` with real Q&As (FAQ is currently a "coming soon" alert — replace
  with a small set of real questions: coverage areas, installation time,
  plans, OTT included, business lease line).

### A3. Open Graph + Twitter cards
Add `og:title/description/image/url/type` + `twitter:card` to all 9 pages.
Use `assets/hero_bg.png` (or a dedicated share image) as `og:image`.

### A4. Canonical tags
Self-referencing canonical on every page → `https://dreamservices.in/<page>.html`.

### A5. robots.txt + sitemap.xml
- `robots.txt` allowing all + pointing to sitemap.
- `sitemap.xml` listing all 9 pages with the live domain.

### A6. Content / heading tweaks (light)
- Ensure each page's H1 naturally includes brand + location intent.
- Add a keyword-rich, NAP-consistent footer line mentioning DreamFiber,
  the legal name, Chakan, and "since 2006" — present on all pages.
- Standardize displayed phone numbers (same set everywhere).

### A7. Technical basics
- `preconnect`/`dns-prefetch` for Google Fonts + ionicons CDN.
- `alt` text on key images.
- Favicon link (use existing asset or note if one must be created).
- `lang="en"` already present — keep.

---

## Workstream B — Off-page action guide (`SEO-ACTION-PLAN.md`)

A non-code, step-by-step doc the owner executes:
1. **Google Business Profile** — create/claim a profile as **DreamFiber** at the
   Chakan address (distinct name + address from the Akurdi listing). Categories:
   Internet service provider, Cable company. Set service area Chakan + Chakan MIDC.
2. **The Akurdi problem** — you cannot remove the uncle's listing; you out-rank
   and out-distinguish it with your own strong, correctly-named Chakan profile +
   reviews. Explain why distinct NAP matters.
3. **Reviews flow** — WhatsApp "leave us a review" link/template to collect
   Google reviews steadily.
4. **Citations** — consistent listings on JustDial, Sulekha, IndiaMART, Bing
   Places, Google Maps, with identical NAP.
5. **Brand-search domination** — internal linking, consistent brand usage so
   "DreamFiber" / "Dream Services" reliably surface this site.

---

## Success criteria

- All 9 pages have unique titles/descriptions, canonical, OG, and JSON-LD.
- `robots.txt` + `sitemap.xml` valid and reference the live domain.
- Structured data validates (Google Rich Results / Schema.org validator).
- NAP identical across all pages.
- Owner has a clear off-page checklist to execute.

## Open questions / assumptions

- Geo-coordinates for the Chakan address: will use an approximate Chakan
  centroid unless the owner provides exact lat/long.
- `og:image` / favicon: will reuse existing assets unless told otherwise.
- Social profile URLs (`sameAs`): left as placeholders until provided.
