import re

card_style = """<style>
.krishi-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
    margin-bottom: 4rem;
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
    font-size: 1.8rem;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 0.5rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: space-between;
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
    font-size: 1rem;
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
    padding: 0.4rem 0.8rem;
    border-radius: 50px;
    font-size: 0.8rem;
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
    font-size: 0.9rem;
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
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.k-ott-bundle-text {
    color: #1d4ed8;
    font-size: 0.8rem;
    font-weight: 700;
}
.k-ott-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
}
.k-ott-icon {
    width: 52px;
    height: 52px;
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
    font-size: 0.55rem;
    color: #111827;
    font-weight: 700;
    text-align: center;
    line-height: 1.1;
    padding: 2px;
}
.k-more-btn {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px dashed #93c5fd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1rem;
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
    gap: 1rem;
}
.k-btn {
    flex: 1;
    text-align: center;
    padding: 0.8rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.95rem;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
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

/* Premium Card Styles */
.k-card-premium {
    grid-column: 1 / -1;
    background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 100%);
    border: 1px solid #312e81;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
@media (min-width: 1024px) {
    .k-card-premium {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
    }
    .k-card-premium .k-card-header {
        border-bottom: none;
        border-right: 1px solid rgba(255,255,255,0.1);
        grid-row: 1 / 3;
    }
    .k-card-premium .k-card-body {
        grid-row: 1 / 2;
    }
    .k-card-premium .k-card-footer {
        grid-row: 2 / 3;
        border-top: 1px solid rgba(255,255,255,0.1);
        background: rgba(0,0,0,0.2);
    }
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
            <h2 class="k-card-title">{name} {best_seller_html}</h2>
            <p class="k-card-subtitle">{subtitle}</p>
            <div class="k-badges">
                <span class="k-badge k-badge-speed">{speed}</span>
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
                <a href="https://wa.me/918552059393?text=Hi+Dream+Fiber%21+I+need+a+new+connection+for+the+{name}+{speed}+plan." class="k-btn k-btn-new" target="_blank">
                    <ion-icon name="logo-whatsapp"></ion-icon> New
                </a>
                <a href="https://wa.me/918552059393?text=Hi+Dream+Fiber%21+I+am+an+existing+customer+and+want+to+upgrade+to+the+{name}+{speed}+plan." class="k-btn k-btn-exist" target="_blank">
                    Existing customer
                </a>
            </div>
        </div>
    </div>
    """
    return html

cards_html = f"""
{card_style}
<div class="krishi-cards-grid">
    {make_card("Mini", "50 Mbps", "Starter plan for basic use", "Starter plan for basic use. Smart TV or multi-device homes should choose a higher speed.")}
    {make_card("Basic", "100 Mbps", "Standard streaming & browsing", "Ideal for small families, smooth HD streaming on multiple devices.", best_seller=True)}
    {make_card("Standard", "200 Mbps", "High-speed family entertainment", "Recommended for families who want smooth multi-screen streaming without buffering.")}
    {make_card("Premium", "300 Mbps", "Premium streaming & gaming", "Ideal for Smart TV, WFH, online classes and uninterrupted OTT on multiple screens.", is_premium=True)}
</div>

            <!-- Office CTA -->
"""

with open("services.html", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '<style>\n.krishi-cards-grid'
end_marker = '</div>\n\n            <!-- Office CTA -->'

pattern = re.compile(re.escape('<style>\n.krishi-cards-grid') + r'.*?' + re.escape('</div>\n\n            <!-- Office CTA -->'), re.DOTALL)

new_content = pattern.sub(cards_html, content)

with open("services.html", "w", encoding="utf-8") as f:
    f.write(new_content)
