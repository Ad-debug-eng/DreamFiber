import re

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
    transition: transform 0.2s;
}
.k-card:hover {
    transform: translateY(-5px);
}
.k-card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #f3f4f6;
}
.k-card-title {
    margin-bottom: 0.5rem;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}
.k-title-wrap {
    display: flex;
    flex-direction: column;
}
.k-plan-name {
    color: #111827;
    font-size: 1.8rem;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    line-height: 1.2;
}
.k-plan-speed {
    color: #4b5563;
    font-size: 1.25rem;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    margin-top: 0.2rem;
}
.k-best-seller {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #fff;
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
    border-radius: 50px;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.k-card-subtitle {
    color: #6b7280;
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

/* Premium Card Styles - Same as others but with website color border */
.k-card-premium {
    border: 2px solid var(--primary);
    box-shadow: 0 10px 30px -5px rgba(200, 32, 138, 0.15); /* Soft primary shadow */
}

/* Add a subtle highlight to the premium header just to make the border look intended */
.k-card-premium .k-card-header {
    background: linear-gradient(to right, rgba(200, 32, 138, 0.03), transparent);
}
</style>"""

def make_card(name, speed, subtitle, note, is_premium=False, best_seller=False):
    card_class = "k-card k-card-premium" if is_premium else "k-card"
    best_seller_html = '<span class="k-best-seller">BEST SELLER</span>' if best_seller else ''
    
    html = f"""
    <div class="{card_class}">
        <div class="k-card-header">
            <h2 class="k-card-title">
                <div class="k-title-wrap">
                    <span class="k-plan-name">{name}</span>
                    <span class="k-plan-speed">{speed}</span>
                </div>
                {best_seller_html}
            </h2>
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
    
    with open("services.html", "w", encoding="utf-8") as f:
        f.write(new_content)
except Exception as e:
    print(f"Error updating services.html: {e}")

print("Done")
