import re

# We will define the new tabs and grid HTML for Broadband vs Broadband + OTT.
style_and_tabs = """<style>
.krishi-tabs-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2.5rem;
}
.k-tab-bar {
    display: flex;
    background: #f1f5f9;
    padding: 0.35rem;
    border-radius: 50px;
    border: 1px solid #e2e8f0;
}
.k-tab-btn {
    padding: 0.65rem 2rem;
    border-radius: 50px;
    border: none;
    background: transparent;
    color: #475569;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}
.k-tab-btn.active {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: #fff;
    box-shadow: 0 4px 10px rgba(200, 32, 138, 0.2);
}

.krishi-cards-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1.5rem;
    margin-top: 1rem;
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
    color: #000000;
    font-size: 1.35rem;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-style: italic;
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

/* Premium Card Styles */
.k-card-premium {
    border: 2px solid var(--primary);
    box-shadow: 0 10px 30px -5px rgba(200, 32, 138, 0.15);
}
.k-card-premium .k-card-header {
    background: linear-gradient(to right, rgba(200, 32, 138, 0.03), transparent);
}

.plan-section {
    display: none;
}
.plan-section.active {
    display: block;
}
</style>

<div class="krishi-tabs-container">
    <div class="k-tab-bar">
        <button class="k-tab-btn" id="btn-tab-broadband" onclick="switchMainTab('broadband')">Broadband</button>
        <button class="k-tab-btn active" id="btn-tab-broadband-ott" onclick="switchMainTab('broadband-ott')">Broadband + OTT</button>
    </div>
</div>
"""

file_map = {
    "Aha Tamil": "ott-ahatamil.png",
    "Chana Jor": "ott-chanajor.png",
    "Chaupal": "ott-chaupal.jpg",
    "Dangal Play": "ott-dangalplay.jpg",
    "Discovery+": "ott-discovery.png",
    "DistroTV": "ott-distrotv.jpg",
    "ETV Win": "ott-etvwin.png",
    "Fancode": "ott-fancode.png",
    "JioHotstar": "ott-hotstar.jpg",
    "Hungama": "ott-hungama.png",
    "Jio Saavn": "ott-jiosaavn.webp",
    "Kanccha Lannka": "ott-kancchalannka.jpg",
    "OM TV": "ott-omtv.jpg",
    "Amazon": "ott-prime.png",
    "Raj DigitalTV": "ott-rajtv.png",
    "Shemaroo": "ott-shemaroome.png",
    "Shorts Tv": "ott-shorts.png",
    "Shucae Flim": "ott-shucaefilm.jpg",
    "SonyLIV": "ott-sonyliv.png",
    "Stage": "ott-stage.png",
    "SunNXT": "ott-sunnxt.png",
    "TravelXP": "ott-travelxp.png",
    "Waves": "ott-waves.jpg",
    "ZEE5": "ott-zee5.png",
    "Netflix": "ott-netflix.png"
}

def get_image_name(app):
    return file_map.get(app, "placeholder.png")

def get_display_name(app):
    display_name = app
    if app == "Netflix": display_name = "Netflix<br>(Basic)"
    elif app == "Amazon": display_name = "Amazon<br>(Lite)"
    elif app == "Kanccha Lannka": display_name = "Kanccha<br>Lannka"
    elif app == "Shucae Flim": display_name = "Shucae<br>Flim"
    return display_name

def make_ott_html(apps):
    html = ""
    for app in apps:
        html += f"""<div class="k-ott-icon"><img src="assets/ott/{get_image_name(app)}" alt="{app}" onerror="this.outerHTML='<span>{get_display_name(app)}</span>'"></div>\n                """
    return html

def make_ott_card(name, speed, subtitle, note, main_apps, drop_apps, total_otts, is_premium=False, best_seller=False):
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
                <span class="k-badge k-badge-ott">{total_otts} OTT apps</span>
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
                {make_ott_html(main_apps)}
                <button class="k-more-btn" onclick="toggleOtt(this)">+{len(drop_apps)}</button>
            </div>
            <div class="k-dropdown">
                <div class="k-ott-grid">
                    {make_ott_html(drop_apps)}
                </div>
            </div>
        </div>
        <div class="k-card-footer">
            <div class="k-actions">
                <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I+need+a+new+connection+for+the+Broadband+%2B+OTT+{name}+{speed}+plan." class="k-btn k-btn-new" target="_blank">
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

def make_broadband_card(name, speed, subtitle, note, prices, best_seller=False):
    card_class = "k-card k-card-premium" if best_seller else "k-card"
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
            </div>
            <div class="k-note">
                {note}
            </div>
        </div>
        <div class="k-card-body" style="padding: 0; flex-grow: 1;">
        </div>
        <div class="k-card-footer">
            <div class="k-actions">
                <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I+need+a+new+connection+for+the+Broadband-only+{name}+{speed}+plan." class="k-btn k-btn-new" target="_blank">
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

# Definitions
mini_main = ["JioHotstar", "ZEE5", "SonyLIV", "Discovery+", "Fancode", "Jio Saavn"]
mini_drop = ["Aha Tamil", "Chaupal", "Dangal Play", "ETV Win", "Hungama", "Kanccha Lannka", "OM TV", "Raj DigitalTV", "Shemaroo", "Shorts Tv", "Shucae Flim", "Stage", "SunNXT", "TravelXP", "Waves"]

basic_std_main = ["Amazon", "JioHotstar", "ZEE5", "SonyLIV", "Discovery+", "Fancode", "Jio Saavn"]
basic_std_drop = ["Aha Tamil", "Chana Jor", "Chaupal", "Dangal Play", "DistroTV", "ETV Win", "Hungama", "Kanccha Lannka", "OM TV", "Raj DigitalTV", "Shemaroo", "Shorts Tv", "Shucae Flim", "Stage", "SunNXT", "TravelXP", "Waves"]

premium_main = ["Netflix", "Amazon", "JioHotstar", "ZEE5", "SonyLIV", "Discovery+", "Fancode", "Jio Saavn"]
premium_drop = basic_std_drop

# Render Sections
broadband_ott_html = f"""
<div id="section-broadband-ott" class="plan-section active">
    <div class="krishi-cards-grid">
        {make_ott_card("Mini", "50 Mbps", "Starter plan with OTT bundles", "Smart TV or multi-device homes should choose a higher speed.", mini_main, mini_drop, 21)}
        {make_ott_card("Basic", "100 Mbps", "Standard streaming & browsing", "Ideal for small families, smooth HD streaming on multiple devices.", basic_std_main, basic_std_drop, 24, best_seller=True)}
        {make_ott_card("Standard", "200 Mbps", "High-speed family entertainment", "Recommended for families who want smooth multi-screen streaming without buffering.", basic_std_main, basic_std_drop, 24)}
        {make_ott_card("Premium", "300 Mbps", "Premium streaming & gaming", "Ideal for Smart TV, WFH, online classes and uninterrupted OTT on multiple screens.", premium_main, premium_drop, 25, is_premium=True)}
    </div>
</div>
"""

broadband_prices_mini = [("1 Month", "499", None), ("3 Months", "1,300", "₹197"), ("6 Months", "2,500", "₹494"), ("12 Months", "5,000", "₹988")]
broadband_prices_basic = [("1 Month", "699", None), ("3 Months", "1,700", "₹397"), ("6 Months", "3,500", "₹694"), ("12 Months", "6,200", "₹2,188")]
broadband_prices_std = [("1 Month", "899", None), ("3 Months", "2,300", "₹397"), ("6 Months", "5,000", "₹394"), ("12 Months", "9,000", "₹1,788")]
broadband_prices_premium = [("1 Month", "1,300", None), ("3 Months", "3,500", "₹400"), ("6 Months", "7,000", "₹800"), ("12 Months", "13,000", "₹2,600")]

broadband_html = f"""
<div id="section-broadband" class="plan-section">
    <div class="krishi-cards-grid">
        {make_broadband_card("Mini", "50 Mbps", "Starter plan for basic use", "Smart TV or multi-device homes should choose a higher speed.", broadband_prices_mini)}
        {make_broadband_card("Basic", "100 Mbps", "Standard streaming & browsing", "Ideal for small families, smooth HD streaming on multiple devices.", broadband_prices_basic)}
        {make_broadband_card("Standard", "200 Mbps", "High-speed family entertainment", "Recommended for families who want smooth multi-screen streaming without buffering.", broadband_prices_std, best_seller=True)}
        {make_broadband_card("Premium", "300 Mbps", "Premium streaming & gaming", "Ideal for Smart TV, WFH, online classes and high-speed downloading.", broadband_prices_premium)}
    </div>
</div>
"""

full_broadband_section = f"""
{style_and_tabs}
{broadband_html}
{broadband_ott_html}

            <!-- Office CTA -->
"""

# Now write the IPTV Section with dynamic rendering code.
# The IPTV controls are arranged in one line, styled to fit the website theme, and contain only IPTV channels (no OTT apps).
iptv_section_replacement = """<!-- IPTV Section -->
            <div class="iptv-section" id="iptv">
                <style>
                    .iptv-section {
                        background: radial-gradient(circle at top right, rgba(200, 32, 138, 0.1), transparent), 
                                    radial-gradient(circle at bottom left, rgba(106, 43, 155, 0.1), transparent), 
                                    #0f172a;
                        background-size: cover;
                        padding: 5rem 0;
                        color: #fff;
                        margin-top: 3rem;
                        border-radius: 20px;
                    }
                    .iptv-header {
                        text-align: center;
                        margin-bottom: 3rem;
                    }
                    .iptv-header h2 {
                        font-size: 2.5rem;
                        color: #fff;
                        margin-bottom: 0.5rem;
                    }
                    .iptv-header p {
                        color: #94a3b8;
                        font-size: 1.1rem;
                    }
                    .iptv-controls {
                        background: #fff;
                        border-radius: 50px;
                        padding: 0.4rem 1.5rem 0.4rem 0.4rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        max-width: 1100px;
                        margin: 0 auto 3rem;
                        box-shadow: 0 10px 30px rgba(200, 32, 138, 0.15);
                        border: 2px solid rgba(200, 32, 138, 0.2);
                        flex-wrap: nowrap;
                        gap: 1.5rem;
                        overflow-x: auto;
                    }
                    .iptv-controls::-webkit-scrollbar {
                        display: none;
                    }
                    .iptv-controls {
                        -ms-overflow-style: none;  /* IE and Edge */
                        scrollbar-width: none;  /* Firefox */
                    }
                    .iptv-tabs {
                        display: flex;
                        gap: 0.25rem;
                        flex-wrap: nowrap;
                    }
                    .iptv-tab {
                        padding: 0.65rem 1.25rem;
                        border-radius: 50px;
                        font-size: 0.85rem;
                        font-weight: 700;
                        color: var(--text-muted);
                        background: transparent;
                        border: none;
                        cursor: pointer;
                        transition: var(--transition-smooth);
                        white-space: nowrap;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    .iptv-tab.active {
                        background: linear-gradient(135deg, var(--primary), var(--secondary));
                        color: #fff;
                    }
                    .iptv-tab:hover:not(.active) {
                        background: rgba(200, 32, 138, 0.05);
                        color: var(--primary);
                    }
                    .iptv-search {
                        position: relative;
                        width: 250px;
                        flex-shrink: 0;
                    }
                    .iptv-search input {
                        width: 100%;
                        padding: 0.65rem 1rem 0.65rem 2.5rem;
                        border-radius: 50px;
                        border: 1.5px solid var(--border-light);
                        font-size: 0.9rem;
                        outline: none;
                        transition: var(--transition-smooth);
                    }
                    .iptv-search input:focus {
                        border-color: var(--primary);
                        box-shadow: 0 0 0 3px rgba(200, 32, 138, 0.15);
                    }
                    .iptv-search ion-icon {
                        position: absolute;
                        left: 1rem;
                        top: 50%;
                        transform: translateY(-50%);
                        color: #94a3b8;
                        font-size: 1.2rem;
                    }
                    .iptv-content {
                        background: #fff;
                        border-radius: 16px;
                        padding: 2.5rem 2rem;
                        max-width: 1100px;
                        margin: 0 auto;
                        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.1);
                    }
                    .iptv-channels-grid {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 1.2rem;
                        justify-content: center;
                        margin-top: 1rem;
                    }
                    .iptv-channel-card {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        background: #fff;
                        border: 1.5px solid #f1f5f9;
                        border-radius: 12px;
                        padding: 0.8rem;
                        width: 130px;
                        height: 130px;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
                        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                        cursor: default;
                    }
                </style>
                <div class="iptv-header">
                    <h2>Channel Guide</h2>
                    <p>Browse over 100+ high-definition IPTV channels.</p>
                </div>
                <div class="iptv-controls">
                    <div class="iptv-tabs">
                        <button class="iptv-tab active">All</button>
                        <button class="iptv-tab">Movies</button>
                        <button class="iptv-tab">General Entertainment</button>
                        <button class="iptv-tab">Sports</button>
                        <button class="iptv-tab">News</button>
                        <button class="iptv-tab">Infotainment</button>
                        <button class="iptv-tab">Music</button>
                        <button class="iptv-tab">Kids</button>
                    </div>
                    <div class="iptv-search">
                        <ion-icon name="search-outline"></ion-icon>
                        <input type="text" placeholder="Find channel...">
                    </div>
                </div>
                <div class="iptv-content">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 1rem;">
                        <h3 style="color:#1f2937; font-size:1.2rem; display:flex; align-items:center; gap:0.5rem; font-family:'Outfit', sans-serif;">
                            <span style="width:10px; height:10px; background:var(--primary); border-radius:50%; display:inline-block;"></span> 
                            IPTV Channels <span style="background:rgba(200, 32, 138, 0.1); color:var(--primary); padding:0.2rem 0.7rem; border-radius:50px; font-size:0.8rem; font-weight:800;" id="channel-counter">0</span>
                        </h3>
                    </div>
                    <div class="iptv-channels-grid">
                        <!-- Loaded Dynamically -->
                    </div>
                </div>
                
                <script>
                    const channels = [
                        // Movies
                        { name: "Colors Cineplex Superhits", category: "Movies", logo: "<img src='assets/iptv/Colors_Cineplex_Superhits_logo.png' alt='Colors Cineplex Superhits' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Colors Cineplex HD", category: "Movies", logo: "<img src='assets/iptv/colors cineplex.png' alt='Colors Cineplex HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Colors Cineplex Bollywood", category: "Movies", logo: "<img src='assets/iptv/colors ciniplex bollywood.jpg' alt='Colors Cineplex Bollywood' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Max HD", category: "Movies", logo: "<img src='assets/iptv/SONY MAX HD.png' alt='Sony Max HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Max 2", category: "Movies", logo: "<img src='assets/iptv/Sony Max 2.jpg' alt='Sony Max 2' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Cinema HD", category: "Movies", logo: "<img src='assets/iptv/ZEE Cenema HD.png' alt='Zee Cinema HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Action", category: "Movies", logo: "<img src='assets/iptv/Zee_Action_2023_logo.png' alt='Zee Action' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Classic", category: "Movies", logo: "<img src='assets/iptv/Zeeclassic_new.webp' alt='Zee Classic' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Anmol Cinema", category: "Movies", logo: "<img src='assets/iptv/Zee_Anmol_Cinema_logo.png' alt='Zee Anmol Cinema' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Pix HD", category: "Movies", logo: "<img src='assets/iptv/SONY Pix HD.png' alt='Sony Pix HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Bollywood", category: "Movies", logo: "<img src='assets/iptv/Zee_bollywood_21AUg2018.webp' alt='Zee Bollywood' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Talkies HD", category: "Movies", logo: "<img src='assets/iptv/Zee_talkies_hd.webp' alt='Zee Talkies HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Utsav Movies", category: "Movies", logo: "<img src='assets/iptv/Starutsavmovies.jpg' alt='Star Utsav Movies' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Gold Thrills", category: "Movies", logo: "<img src='assets/iptv/025656-star-gold-thrills-logo-white-bg.png' alt='Star Gold Thrills' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Caf'e HD", category: "Movies", logo: "<img src='assets/iptv/Zcafe HD.jpg' alt='Zee Caf\'e HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Gold HD", category: "Movies", logo: "<img src='assets/iptv/Star-Gold-HD.png' alt='Star Gold HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Movies Select HD", category: "Movies", logo: "<img src='assets/iptv/Star-Movies-Select.png' alt='Star Movies Select HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Gold 2 HD", category: "Movies", logo: "<img src='assets/iptv/Star-Gold-2-HD-1.png' alt='Star Gold 2 HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Gold Romance", category: "Movies", logo: "<img src='assets/iptv/Star_Gold_Romance.webp' alt='Star Gold Romance' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Movies HD", category: "Movies", logo: "<img src='assets/iptv/Star Movies HD.png' alt='Star Movies HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Gold select HD", category: "Movies", logo: "<img src='assets/iptv/Star-Gold-Select-HD.png' alt='Star Gold select HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nazara", category: "Movies", logo: "<img src='assets/iptv/nazara-technologies-logo-png_seeklogo-400001.png' alt='Nazara' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "MNX HD", category: "Movies", logo: "<img src='assets/iptv/mnxhd.jpg' alt='MNX HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Big Magic", category: "Movies", logo: "<img src='assets/iptv/BIG_Magic_Logo.jpg' alt='Big Magic' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "MN+ HD", category: "Movies", logo: "<img src='assets/iptv/MN+ HD.png' alt='MN+ HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Show Box", category: "Movies", logo: "<img src='assets/iptv/Showbox_logo.webp' alt='Show Box' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Pravah Picture HD", category: "Movies", logo: "PRAVAH<br>Picture", color: "#b91c1c" },
                        { name: "Colors Infinity HD", category: "Movies", logo: "<img src='assets/iptv/COLORS-INFINITY-HD.png' alt='Colors Infinity HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "&flix HD", category: "Movies", logo: "<img src='assets/iptv/flix-hd-logo-png_seeklogo-432038.png' alt='&flix HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Movies Now HD", category: "Movies", logo: "<img src='assets/iptv/Movies_Now_logo.png' alt='Movies Now HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "&prive HD", category: "Movies", logo: "<img src='assets/iptv/&privé_HD.svg.png' alt='&prive HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "&pictures HD", category: "Movies", logo: "<img src='assets/iptv/pictures-hd-logo-png_seeklogo-457044.png' alt='&pictures HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Filamchi", category: "Movies", logo: "<img src='assets/iptv/Filamchi_eng.webp' alt='Filamchi' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Fox Life HD", category: "Movies", logo: "<img src='assets/iptv/Fox_Life_HD.svg' alt='Fox Life HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Comedy Central HD", category: "Movies", logo: "<img src='assets/iptv/Comedy_Central_2018.svg.png' alt='Comedy Central HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // General Entertainment
                        { name: "Star Bharat HD", category: "General Entertainment", logo: "<img src='assets/iptv/STAR-BHARAT-HD.png' alt='Star Bharat HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Utsav", category: "General Entertainment", logo: "<img src='assets/iptv/Star Utsav.jpg' alt='Star Utsav' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "&tv HD", category: "General Entertainment", logo: "<img src='assets/iptv/TV-HD-1-2.jpg' alt='&tv HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Pravah HD", category: "General Entertainment", logo: "<img src='assets/iptv/Star_Pravah_HD_2019.webp' alt='Star Pravah HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Anmol", category: "General Entertainment", logo: "<img src='assets/iptv/Zee_Anmol_logo.png' alt='Zee Anmol' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee TV HD", category: "General Entertainment", logo: "<img src='assets/iptv/zee-removebg-preview.png' alt='Zee TV HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Marathi HD", category: "General Entertainment", logo: "<img src='assets/iptv/Zee Marathi.jpg' alt='Zee Marathi HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Yuva", category: "General Entertainment", logo: "<img src='assets/iptv/Zee_Yuva_logo.png' alt='Zee Yuva' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Colors HD", category: "General Entertainment", logo: "<img src='assets/iptv/9a4c602bafac400c6583560569ad1ddc.png' alt='Colors HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Colors Marathi HD", category: "General Entertainment", logo: "<img src='assets/iptv/4b38c9cd6fb499e07fe19677035a5c02.png' alt='Colors Marathi HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Colors Rishtey", category: "General Entertainment", logo: "<img src='assets/iptv/0d90ff274603286bd0469eea3f672af320aab30c8859ffa669c422498818d25d.png' alt='Colors Rishtey' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Yay", category: "General Entertainment", logo: "<img src='assets/iptv/SONY_YAY_2022_Logo.png' alt='Sony Yay' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Marathi", category: "General Entertainment", logo: "<img src='assets/iptv/Sony Marathi.jpg' alt='Sony Marathi' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Sab HD", category: "General Entertainment", logo: "<img src='assets/iptv/70954ffc9bae055e09e48393b47570ea.png' alt='Sony Sab HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony HD", category: "General Entertainment", logo: "<img src='assets/iptv/b02e7be82b9b488e5a79b0f7e8f7ca1c.png' alt='Sony HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Pal", category: "General Entertainment", logo: "<img src='assets/iptv/sony pal.jpg' alt='Sony Pal' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Wah", category: "General Entertainment", logo: "<img src='assets/iptv/SonyWAH.png' alt='Sony Wah' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Bindass", category: "General Entertainment", logo: "<img src='assets/iptv/Bindass_2010.webp' alt='Bindass' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // Sports
                        { name: "Star Sports HD 1", category: "Sports", logo: "<img src='assets/iptv/Star-Sports-1-hd.avif' alt='Star Sports HD 1' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports HD 2", category: "Sports", logo: "<img src='assets/iptv/491483410_1095578502613934_189478736713524881_n.jpg' alt='Star Sports HD 2' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports 1 HD Hindi", category: "Sports", logo: "<img src='assets/iptv/image-Content-60-j5fdr6a0-m1.4pi4jxp1lme0.webp' alt='Star Sports 1 HD Hindi' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports 3", category: "Sports", logo: "<img src='assets/iptv/Star-Sports-3-1.png' alt='Star Sports 3' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports First", category: "Sports", logo: "<img src='assets/iptv/STAR-SPORTS-FIRST.webp' alt='Star Sports First' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sports 18-2", category: "Sports", logo: "<img src='assets/iptv/Sports18_logo.svg.png' alt='Sports 18-2' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Euro Sports", category: "Sports", logo: "<img src='assets/iptv/112604-110070-Eurosport.avif' alt='Euro Sports' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports select 1 Hd", category: "Sports", logo: "<img src='assets/iptv/Star-Sports-Select-HD-1-1-1200x675.png' alt='Star Sports select 1 Hd' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Star Sports select 2 Hd", category: "Sports", logo: "<img src='assets/iptv/Star-Sports-Select-HD-2-1.png' alt='Star Sports select 2 Hd' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony Sports Ten 1 HD", category: "Sports", logo: "SONY TEN 1<br>HD", color: "#0284c7" },
                        { name: "Sony Sports Ten 2 HD", category: "Sports", logo: "SONY TEN 2<br>HD", color: "#0284c7" },
                        { name: "Sony Sports Ten 3 HD", category: "Sports", logo: "SONY TEN 3<br>HD", color: "#0f766e" },
                        { name: "Sony Sports Ten 5 HD", category: "Sports", logo: "<img src='assets/iptv/181x0-icon.png' alt='Sony Sports Ten 5 HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // News
                        { name: "Aaj Tak HD", category: "News", logo: "<img src='assets/iptv/aaj tak HD.jpg' alt='Aaj Tak HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "ET Now", category: "News", logo: "<img src='assets/iptv/ET-now.webp' alt='ET Now' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "ET Now Swadesh", category: "News", logo: "<img src='assets/iptv/AJpMZIv.png' alt='ET Now Swadesh' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "CNN International", category: "News", logo: "<img src='assets/iptv/CNNinternational-logo.png' alt='CNN International' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "CNBC Awaz", category: "News", logo: "<img src='assets/iptv/cnbc.png' alt='CNBC Awaz' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "CNBC TV 18", category: "News", logo: "<img src='assets/iptv/CNBC_TV18_2025.svg' alt='CNBC TV 18' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "CNBC TV 18 Prime HD", category: "News", logo: "<img src='assets/iptv/cnbc-tv18-prime-hd.webp' alt='CNBC TV 18 Prime HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "News 18 Lokmat", category: "News", logo: "<img src='assets/iptv/News18_Lokmat_Logo.svg.png' alt='News 18 Lokmat' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "News 18 India", category: "News", logo: "<img src='assets/iptv/News18_India.svg.png' alt='News 18 India' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "GNT", category: "News", logo: "<img src='assets/iptv/GNT.png' alt='GNT' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "India Today", category: "News", logo: "<img src='assets/iptv/16536-1592_import.png' alt='India Today' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Mirror Now", category: "News", logo: "<img src='assets/iptv/Mirror_Now.svg.png' alt='Mirror Now' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Times Now World HD", category: "News", logo: "<img src='assets/iptv/0d6b26a327dc627646f558d3797a4f2b.png' alt='Times Now World HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Times Now Navbharat HD", category: "News", logo: "<img src='assets/iptv/Times_Now_Navbharat_2022.webp' alt='Times Now Navbharat HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "CNN News 18", category: "News", logo: "<img src='assets/iptv/CNN-News18.svg.png' alt='CNN News 18' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // Infotainment
                        { name: "Discovery Kids", category: "Infotainment", logo: "<img src='assets/iptv/2016_Discovery_Kids_logo.svg.png' alt='Discovery Kids' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Discovery ID HD", category: "Infotainment", logo: "<img src='assets/iptv/Discovery ID HD.webp' alt='Discovery ID HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Discovery Science HD", category: "Infotainment", logo: "<img src='assets/iptv/discovery-science-hd-discovery-science-channel-logo-11563265312wbidfsxg71.png' alt='Discovery Science HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "& Xplor HD", category: "Infotainment", logo: "<img src='assets/iptv/%26xplor_HD.webp' alt='& Xplor HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Sony BBC Earth HD", category: "Infotainment", logo: "BBC Earth<br>HD", color: "#0284c7" },
                        { name: "Animal Planet HD", category: "Infotainment", logo: "<img src='assets/iptv/107-1076403_animal-planet-png-animal-planet-logo-2019-transparent.png' alt='Animal Planet HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "National Geographic HD", category: "Infotainment", logo: "<img src='assets/iptv/national geographic channel hd.png' alt='National Geographic HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "TLC HD", category: "Infotainment", logo: "<img src='assets/iptv/TLC-HD-Logo_2016.svg.png' alt='TLC HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nat Geo Wild HD", category: "Infotainment", logo: "<img src='assets/iptv/Nat_Geo_Wild_HD_logo.png' alt='Nat Geo Wild HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Discovery Turbo", category: "Infotainment", logo: "<img src='assets/iptv/Discovery_Turbo.png' alt='Discovery Turbo' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "History TV 18 HD", category: "Infotainment", logo: "<img src='assets/iptv/History_tv18_hd.webp' alt='History TV 18 HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Discovery Channel HD", category: "Infotainment", logo: "<img src='assets/iptv/Discovery_hd_world_%28small_globe%29.webp' alt='Discovery Channel HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Epic", category: "Infotainment", logo: "<img src='assets/iptv/EPIC_logo_for_print.png' alt='Epic' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zee Zest HD", category: "Infotainment", logo: "<img src='assets/iptv/zee-removebg-preview.png' alt='Zee Zest HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // Music
                        { name: "Zing", category: "Music", logo: "<img src='assets/iptv/Zing_logo.svg.png' alt='Zing' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Zoom", category: "Music", logo: "<img src='assets/iptv/unnamed.jpg' alt='Zoom' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "MTV HD", category: "Music", logo: "<img src='assets/iptv/MTV-HD.jpg' alt='MTV HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "MTV Beats", category: "Music", logo: "<img src='assets/iptv/MTV_Beats_Logo.png' alt='MTV Beats' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "VH1 HD", category: "Music", logo: "<img src='assets/iptv/vh1-hd-logo-png_seeklogo-178504.png' alt='VH1 HD' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },

                        // Kids
                        { name: "Hungama TV", category: "Kids", logo: "<img src='assets/iptv/Hangama.png' alt='Hungama TV' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Cartoon Network HD+", category: "Kids", logo: "<img src='assets/iptv/Cartoon_Network_HD+_India_logo.png' alt='Cartoon Network HD+' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Pogo", category: "Kids", logo: "<img src='assets/iptv/images.png' alt='Pogo' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Gubbare", category: "Kids", logo: "<img src='assets/iptv/Gubbare-cl.webp' alt='Gubbare' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nick HD+", category: "Kids", logo: "<img src='assets/iptv/Nick.png' alt='Nick HD+' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nick", category: "Kids", logo: "<img src='assets/iptv/Nick.png' alt='Nick' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nick Jr.", category: "Kids", logo: "<img src='assets/iptv/Nick_jr_words.webp' alt='Nick Jr.' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" },
                        { name: "Nickelodeon Sonic", category: "Kids", logo: "<img src='assets/iptv/Nickelodeon_Sonic_logo_2019.webp' alt='Nickelodeon Sonic' style='max-width:100%; max-height:100%; object-fit:contain;'>", color: "#fff" }
                    ];

                    function renderChannels() {
                        const grid = document.querySelector('.iptv-channels-grid');
                        if (!grid) return;
                        
                        const activeTabEl = document.querySelector('.iptv-tab.active');
                        const category = activeTabEl ? activeTabEl.textContent.trim() : 'All';
                        const searchQuery = document.querySelector('.iptv-search input').value.toLowerCase().trim();
                        
                        const filtered = channels.filter(c => {
                            const matchesCategory = (category === 'All' || c.category === category);
                            const matchesSearch = c.name.toLowerCase().includes(searchQuery);
                            return matchesCategory && matchesSearch;
                        });
                        
                        grid.innerHTML = '';
                        
                        if (filtered.length === 0) {
                            grid.innerHTML = `
                                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: #64748b; font-family:'Inter', sans-serif;">
                                    <ion-icon name="alert-circle-outline" style="font-size: 3rem; margin-bottom: 1rem; color: var(--primary);"></ion-icon>
                                    <p style="font-weight: 700;">No channels found matching "${searchQuery}"</p>
                                </div>
                            `;
                            document.getElementById('channel-counter').textContent = '0';
                            return;
                        }
                        
                        filtered.forEach(c => {
                            const card = document.createElement('div');
                            card.className = 'iptv-channel-card';
                            
                            // Mouse hover effects handled in script
                            card.onmouseenter = () => {
                                card.style.transform = 'translateY(-4px)';
                                card.style.boxShadow = '0 10px 15px -3px rgba(200, 32, 138, 0.15), 0 4px 6px -2px rgba(200, 32, 138, 0.1)';
                                card.style.borderColor = 'rgba(200, 32, 138, 0.3)';
                            };
                            card.onmouseleave = () => {
                                card.style.transform = 'none';
                                card.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.03)';
                                card.style.borderColor = '#f1f5f9';
                            };

                            card.innerHTML = `
                                <div style="
                                    width: 100%;
                                    height: 60px;
                                    border-radius: 8px;
                                    background: ${c.color};
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    color: #fff;
                                    font-family: 'Outfit', sans-serif;
                                    font-size: 0.8rem;
                                    font-weight: 800;
                                    text-align: center;
                                    padding: 0.25rem;
                                    text-transform: uppercase;
                                    letter-spacing: 0.5px;
                                    box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
                                    line-height: 1.2;
                                ">${c.logo}</div>
                                <div style="
                                    margin-top: 0.6rem;
                                    font-family: 'Inter', sans-serif;
                                    font-size: 0.72rem;
                                    font-weight: 700;
                                    color: #1e293b;
                                    text-align: center;
                                    line-height: 1.2;
                                    display: -webkit-box;
                                    -webkit-line-clamp: 2;
                                    -webkit-box-orient: vertical;
                                    overflow: hidden;
                                    height: 28px;
                                ">${c.name}</div>
                            `;
                            grid.appendChild(card);
                        });
                        
                        document.getElementById('channel-counter').textContent = filtered.length;
                    }

                    document.addEventListener('DOMContentLoaded', () => {
                        const tabs = document.querySelectorAll('.iptv-tab');
                        tabs.forEach(tab => {
                            tab.addEventListener('click', () => {
                                tabs.forEach(t => t.classList.remove('active'));
                                tab.classList.add('active');
                                renderChannels();
                            });
                        });
                        
                        const searchInput = document.querySelector('.iptv-search input');
                        if (searchInput) {
                            searchInput.addEventListener('input', renderChannels);
                        }
                        
                        renderChannels();
                    });
                </script>
            </div>"""

try:
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Update Broadband card grid with Broadband / Broadband + OTT tabs
    start_marker = '<style>\n.krishi-cards-grid'
    end_marker = '</div>\n\n            <!-- Office CTA -->'
    pattern = re.compile(re.escape(start_marker) + r'.*?' + re.escape(end_marker), re.DOTALL)
    content = pattern.sub(full_broadband_section, content)

    # 2. Update IPTV Section in services.html
    iptv_start_marker = '<!-- IPTV Section -->'
    iptv_end_marker = '<!-- Office CTA -->'
    
    # We will search for everything from <!-- IPTV Section --> to <!-- Office CTA -->
    # and replace with our new themed section + script. Note that <!-- Office CTA --> should be kept.
    iptv_pattern = re.compile(re.escape(iptv_start_marker) + r'.*?(?=' + re.escape(iptv_end_marker) + ')', re.DOTALL)
    content = iptv_pattern.sub(iptv_section_replacement + "\n            ", content)

    # 3. Add Javascript switcher function for the tabs inside services.html
    # We will insert it just before the closing </body> tag
    switch_tab_script = """
    <script>
        function switchMainTab(tabType) {
            const broadbandSection = document.getElementById('section-broadband');
            const broadbandOttSection = document.getElementById('section-broadband-ott');
            const btnBroadband = document.getElementById('btn-tab-broadband');
            const btnBroadbandOtt = document.getElementById('btn-tab-broadband-ott');
            
            if (tabType === 'broadband') {
                broadbandSection.classList.add('active');
                broadbandSection.style.display = 'block';
                broadbandOttSection.classList.remove('active');
                broadbandOttSection.style.display = 'none';
                btnBroadband.classList.add('active');
                btnBroadbandOtt.classList.remove('active');
            } else {
                broadbandSection.classList.remove('active');
                broadbandSection.style.display = 'none';
                broadbandOttSection.classList.add('active');
                broadbandOttSection.style.display = 'block';
                btnBroadband.classList.remove('active');
                btnBroadbandOtt.classList.add('active');
            }
        }
        
        window.addEventListener('DOMContentLoaded', () => {
            const hash = window.location.hash;
            if (hash === '#broadband') {
                switchMainTab('broadband');
            } else if (hash === '#broadband-ott') {
                switchMainTab('broadband-ott');
            }
        });
        
        window.addEventListener('hashchange', () => {
            const hash = window.location.hash;
            if (hash === '#broadband') {
                switchMainTab('broadband');
            } else if (hash === '#broadband-ott') {
                switchMainTab('broadband-ott');
            }
        });
    </script>
</body>"""
    content = content.replace("</body>", switch_tab_script)

    with open("services.html", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully updated services.html!")
except Exception as e:
    print(f"Error updating services.html: {e}")
