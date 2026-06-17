import re
import os
import glob

# 1. Update services.html cards
card_style = """<style>
.krishi-cards-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 4rem;
}
@media (min-width: 768px) {
    .krishi-cards-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (min-width: 1200px) {
    .krishi-cards-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

.k-card {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    position: relative;
}
.k-card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #f3f4f6;
}
.k-card-title {
    color: #111827;
    font-size: 1.6rem;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 0.5rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.k-card-title b {
    font-weight: 900;
    font-size: 1.8rem;
}
.k-best-seller {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #fff;
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
    border-radius: 50px;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.k-card-subtitle {
    color: #4b5563;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    font-weight: 500;
}
.k-badges {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.k-badge {
    padding: 0.4rem 0.6rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid transparent;
}
.k-badge-speed {
    color: #059669;
    border-color: #a7f3d0;
    background: #ecfdf5;
}
.k-badge-data {
    color: #2563eb;
    border-color: #bfdbfe;
    background: #eff6ff;
}
.k-badge-ott {
    color: #374151;
    border-color: #e5e7eb;
    background: #f9fafb;
}
.k-badge-tv {
    color: #b91c1c;
    border-color: #fecaca;
    background: #fef2f2;
}
.k-note {
    border-left: 3px solid #10b981;
    padding: 1rem;
    color: #4b5563;
    font-size: 0.85rem;
    background: #f8fafc;
    border-radius: 0 8px 8px 0;
    font-weight: 500;
}
.k-card-body {
    padding: 1.5rem;
    flex-grow: 1;
}
.k-ott-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.k-ott-title {
    color: #6b7280;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.k-ott-bundle-text {
    color: #1d4ed8;
    font-size: 0.75rem;
    font-weight: 700;
}
.k-ott-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.k-ott-icon {
    width: 46px;
    height: 46px;
    border-radius: 10px;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}
.k-ott-icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.k-ott-icon span {
    font-size: 0.5rem;
    color: #111827;
    font-weight: 700;
    text-align: center;
    line-height: 1.1;
    padding: 2px;
}
.k-more-btn {
    width: 46px;
    height: 46px;
    border-radius: 10px;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px dashed #93c5fd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}
.k-more-btn:hover {
    background: #dbeafe;
}
.k-card-footer {
    padding: 1.5rem;
    border-top: 1px solid #f3f4f6;
    background: #fafafa;
}
.k-actions {
    display: flex;
    gap: 0.8rem;
}
.k-btn {
    flex: 1;
    text-align: center;
    padding: 0.7rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    transition: all 0.2s;
}
.k-btn-new {
    background: #10b981;
    color: #fff;
    border: none;
}
.k-btn-new:hover {
    background: #059669;
}
.k-btn-exist {
    background: #fff;
    color: #1d4ed8;
    border: 1px solid #1d4ed8;
}
.k-btn-exist:hover {
    background: #eff6ff;
}
.k-dropdown {
    display: none;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed #e5e7eb;
}
.k-dropdown.active {
    display: block;
}

/* Premium Card Styles (Delicate Aesthetic) */
.k-card-premium {
    background: linear-gradient(145deg, #1f2937 0%, #111827 100%);
    border: 1px solid #374151;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
.k-card-premium .k-card-header {
    border-bottom-color: rgba(255,255,255,0.1);
}
.k-card-premium .k-card-title {
    color: #facc15;
}
.k-card-premium .k-card-subtitle {
    color: #9ca3af;
}
.k-card-premium .k-badge-speed {
    background: rgba(250, 204, 21, 0.15);
    color: #facc15;
    border-color: #ca8a04;
}
.k-card-premium .k-badge-data {
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border-color: #0284c7;
}
.k-card-premium .k-badge-ott {
    background: rgba(255, 255, 255, 0.1);
    color: #e5e7eb;
    border-color: rgba(255,255,255,0.2);
}
.k-card-premium .k-badge-tv {
    background: rgba(248, 113, 113, 0.15);
    color: #f87171;
    border-color: #dc2626;
}
.k-card-premium .k-note {
    background: rgba(255,255,255,0.05);
    border-left-color: #facc15;
    color: #d1d5db;
}
.k-card-premium .k-ott-title {
    color: #9ca3af;
}
.k-card-premium .k-ott-bundle-text {
    color: #facc15;
}
.k-card-premium .k-ott-icon {
    background: rgba(0,0,0,0.3);
    border-color: rgba(255,255,255,0.1);
}
.k-card-premium .k-ott-icon span {
    color: #e5e7eb;
}
.k-card-premium .k-more-btn {
    background: rgba(250, 204, 21, 0.1);
    color: #facc15;
    border-color: rgba(250, 204, 21, 0.4);
}
.k-card-premium .k-more-btn:hover {
    background: rgba(250, 204, 21, 0.2);
}
.k-card-premium .k-card-footer {
    border-top-color: rgba(255,255,255,0.1);
    background: rgba(0,0,0,0.2);
}
.k-card-premium .k-btn-new {
    background: #eab308;
    color: #000;
}
.k-card-premium .k-btn-new:hover {
    background: #ca8a04;
}
.k-card-premium .k-btn-exist {
    background: transparent;
    color: #facc15;
    border-color: #facc15;
}
.k-card-premium .k-btn-exist:hover {
    background: rgba(250, 204, 21, 0.1);
}
.k-card-premium .k-dropdown {
    border-top-color: rgba(255,255,255,0.1);
}
</style>"""

def make_card(name, speed, subtitle, note, is_premium=False, best_seller=False):
    card_class = "k-card k-card-premium" if is_premium else "k-card"
    best_seller_html = '<span class="k-best-seller">BEST SELLER</span>' if best_seller else ''
    
    html = f"""
    <div class="{card_class}">
        <div class="k-card-header">
            <h2 class="k-card-title"><span>{name} <b>{speed}</b></span> {best_seller_html}</h2>
            <p class="k-card-subtitle">{subtitle}</p>
            <div class="k-badges">
                <span class="k-badge k-badge-data">Unlimited Internet</span>
                <span class="k-badge k-badge-tv">450+ LIVE TV Channels</span>
                <span class="k-badge k-badge-ott">25 OTT apps</span>
            </div>
            <div class="k-note">
                {note}
            </div>
        </div>
        <div class="k-card-body">
            <div class="k-ott-header">
                <div class="k-ott-title">MAIN OTT APPS</div>
                <div class="k-ott-bundle-text">Dream bundle</div>
            </div>
            <div class="k-ott-grid">
                <div class="k-ott-icon"><img src="assets/ott/netflix.png" alt="Netflix" onerror="this.outerHTML='<span>Netflix<br>(Basic)</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/amazonlite.png" alt="Amazon" onerror="this.outerHTML='<span>Amazon<br>(Lite)</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/jiohotstar.png" alt="JioHotstar" onerror="this.outerHTML='<span>JioHotstar</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/zee5.png" alt="ZEE5" onerror="this.outerHTML='<span>ZEE5</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/sonyliv.png" alt="SonyLIV" onerror="this.outerHTML='<span>SonyLIV</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/discoveryplus.png" alt="Discovery+" onerror="this.outerHTML='<span>Discovery+</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/fancode.png" alt="Fancode" onerror="this.outerHTML='<span>Fancode</span>'"></div>
                <div class="k-ott-icon"><img src="assets/ott/jiosaavn.png" alt="Jio Saavn" onerror="this.outerHTML='<span>Jio Saavn</span>'"></div>
                <button class="k-more-btn" onclick="toggleOtt(this)">+17</button>
            </div>
            <div class="k-dropdown">
                <div class="k-ott-grid">
                    <div class="k-ott-icon"><img src="assets/ott/aha.png" alt="Aha Tamil" onerror="this.outerHTML='<span>Aha Tamil</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/chanajor.png" alt="Chana Jor" onerror="this.outerHTML='<span>Chana Jor</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/chaupal.png" alt="Chaupal" onerror="this.outerHTML='<span>Chaupal</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/dangalplay.png" alt="Dangal Play" onerror="this.outerHTML='<span>Dangal Play</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/distrotv.png" alt="DistroTV" onerror="this.outerHTML='<span>DistroTV</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/etvwin.png" alt="ETV Win" onerror="this.outerHTML='<span>ETV Win</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/hungama.png" alt="Hungama" onerror="this.outerHTML='<span>Hungama</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/kanccha.png" alt="Kanccha Lannka" onerror="this.outerHTML='<span>Kanccha<br>Lannka</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/omtv.png" alt="OM TV" onerror="this.outerHTML='<span>OM TV</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/rajdigital.png" alt="Raj Digital" onerror="this.outerHTML='<span>Raj Digital</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/shemaroo.png" alt="Shemaroo" onerror="this.outerHTML='<span>Shemaroo</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/shortstv.png" alt="Shorts Tv" onerror="this.outerHTML='<span>Shorts Tv</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/shucaeflim.png" alt="Shucae Flim" onerror="this.outerHTML='<span>Shucae<br>Flim</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/stage.png" alt="Stage" onerror="this.outerHTML='<span>Stage</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/sunnxt.png" alt="SunNXT" onerror="this.outerHTML='<span>SunNXT</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/travelxp.png" alt="TravelXP" onerror="this.outerHTML='<span>TravelXP</span>'"></div>
                    <div class="k-ott-icon"><img src="assets/ott/waves.png" alt="Waves" onerror="this.outerHTML='<span>Waves</span>'"></div>
                </div>
            </div>
        </div>
        <div class="k-card-footer">
            <div class="k-actions">
                <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I+need+a+new+connection+for+the+{name}+{speed}+plan." class="k-btn k-btn-new" target="_blank">
                    <ion-icon name="logo-whatsapp"></ion-icon> Chat
                </a>
                <a href="tel:+918788536698" class="k-btn k-btn-exist">
                    <ion-icon name="call-outline"></ion-icon> Call
                </a>
            </div>
        </div>
    </div>
    """
    return html

cards_html = f"""
{card_style}
<div class="krishi-cards-grid">
    {make_card("Mini", "50 Mbps", "Starter plan for basic use", "Smart TV or multi-device homes should choose a higher speed.")}
    {make_card("Basic", "100 Mbps", "Standard streaming & browsing", "Ideal for small families, smooth HD streaming on multiple devices.", best_seller=True)}
    {make_card("Standard", "200 Mbps", "High-speed family entertainment", "Recommended for families who want smooth multi-screen streaming without buffering.")}
    {make_card("Premium", "300 Mbps", "Premium streaming & gaming", "Ideal for Smart TV, WFH, online classes and uninterrupted OTT on multiple screens.", is_premium=True)}
</div>

            <!-- Office CTA -->
"""

try:
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    start_marker = '<style>\n.krishi-cards-grid'
    end_marker = '</div>\n\n            <!-- Office CTA -->'
    pattern = re.compile(re.escape(start_marker) + r'.*?' + re.escape(end_marker), re.DOTALL)
    new_content = pattern.sub(cards_html, content)
    
    # 2. Update numbers in services.html
    new_content = new_content.replace('918552059393', '918788536698')
    new_content = new_content.replace('8552059393', '+91 87885 36698')
    new_content = new_content.replace('8408069393', '')
    new_content = new_content.replace('9689395547', '')
    new_content = new_content.replace('<p>📞  / </p>', '')
    new_content = new_content.replace('<p>📞 +91 87885 36698 / </p>', '<p>📞 +91 87885 36698</p>')
    new_content = new_content.replace('<p>📞 </p>', '')

    # Fix empty paragraphs if they were created
    new_content = re.sub(r'<p>📞\s*</p>', '', new_content)
    
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(new_content)
except Exception as e:
    print(f"Error updating services.html: {e}")

# Process other HTML files
html_files = glob.glob("*.html")
for filepath in html_files:
    if filepath == "services.html":
        continue # Already processed
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace('918552059393', '918788536698')
        
        # Replace specific footer blocks using regex if needed, or simple string replace
        content = content.replace('8552059393 / 8408069393', '+91 87885 36698')
        content = content.replace('<p>📞 9689395547</p>', '')
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Process JS files
js_files = glob.glob("js/*.js")
for filepath in js_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('918552059393', '918788536698')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Done")
