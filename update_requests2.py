import re
import os

template = """<nav class="nav-links">
                <a href="index.html" class="{active_home}">Home</a>
                <a href="contact.html" class="{active_enterprise}">Enterprise Solution</a>
                <div class="nav-dropdown">
                    <a href="javascript:void(0)" class="nav-dropbtn {active_broadband}">Home Broadband <ion-icon name="chevron-down-outline"></ion-icon></a>
                    <div class="nav-dropdown-content">
                        <a href="services.html">Mini</a>
                        <a href="services.html">Basic</a>
                        <a href="services.html">Standard</a>
                        <a href="services.html">Premium</a>
                    </div>
                </div>
                <a href="ott.html" class="{active_ott}">OTT</a>
                <a href="services.html#iptv" class="{active_iptv}">IPTV</a>
                <a href="about.html" class="{active_about}">About Us</a>
                <a href="contact.html" class="{active_contact}">Contact Us</a>
            </nav>
            
            <div class="nav-actions">
                <a href="#" class="btn btn-primary" style="margin-right: 0.5rem;">Pay Bill</a>
                <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I%27m+interested+in+a+new+fiber+broadband+connection.+Please+check+feasibility+for+my+area." target="_blank" class="btn btn-outline">
                    <ion-icon name="logo-whatsapp" style="margin-right: 0.5rem;"></ion-icon> WhatsApp
                </a>
            </div>"""

files = ['index.html', 'services.html', 'about.html', 'contact.html']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        act_home = 'active' if f == 'index.html' else ''
        act_broadband = 'active' if f == 'services.html' else ''
        act_about = 'active' if f == 'about.html' else ''
        act_contact = 'active' if f == 'contact.html' else ''
        
        repl = template.format(
            active_home=act_home,
            active_enterprise='',
            active_broadband=act_broadband,
            active_ott='',
            active_iptv='',
            active_about=act_about,
            active_contact=act_contact
        )
        repl = repl.replace(' class=""', '')
        
        pattern = re.compile(r'<nav class="nav-links">.*?</nav>\s*<div class="nav-actions">.*?</div>', re.DOTALL)
        new_content = pattern.sub(repl, content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Updated {f}')
    except Exception as e:
        print(f'Error processing {f}: {e}')

# Append CSS for wide header and IPTV section
css_append = """
/* Make header wider to avoid congestion */
header .container.nav-container {
    max-width: 98% !important;
    padding: 0 1% !important;
}

/* IPTV Section Styles */
.iptv-section {
    background: #0f172a;
    background-image: radial-gradient(#1e293b 1px, transparent 1px);
    background-size: 20px 20px;
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
    padding: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1000px;
    margin: 0 auto 3rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    flex-wrap: wrap;
    gap: 1rem;
}

.iptv-tabs {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.iptv-tab {
    padding: 0.6rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #64748b;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.iptv-tab.active {
    background: #1e293b;
    color: #fff;
}

.iptv-tab:hover:not(.active) {
    background: #f1f5f9;
    color: #0f172a;
}

.iptv-search {
    position: relative;
    flex-grow: 1;
    max-width: 300px;
}

.iptv-search input {
    width: 100%;
    padding: 0.7rem 1rem 0.7rem 2.5rem;
    border-radius: 50px;
    border: 1px solid #e2e8f0;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s;
}

.iptv-search input:focus {
    border-color: #3b82f6;
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
    padding: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.iptv-channels-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
}

.iptv-channel {
    width: 100px;
    height: 100px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    padding: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s;
}

.iptv-channel:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.iptv-channel img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
"""

try:
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write(css_append)
    print("Appended CSS")
except Exception as e:
    print(f"Error appending CSS: {e}")

# Add IPTV Section to services.html
iptv_html = """
            <!-- IPTV Section -->
            <div class="iptv-section" id="iptv">
                <div class="iptv-header">
                    <h2>Channel Guide</h2>
                    <p>Search over 500+ channels across Tamil, Hindi, Telugu & Malayalam.</p>
                </div>
                <div class="iptv-controls">
                    <div class="iptv-tabs">
                        <button class="iptv-tab active">All</button>
                        <button class="iptv-tab">Movies</button>
                        <button class="iptv-tab">General Entertainment</button>
                        <button class="iptv-tab">Sports</button>
                        <button class="iptv-tab">News</button>
                        <button class="iptv-tab">Infotainment</button>
                    </div>
                    <div class="iptv-search">
                        <ion-icon name="search-outline"></ion-icon>
                        <input type="text" placeholder="Find channel...">
                    </div>
                </div>
                <div class="iptv-content">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 2rem;">
                        <h3 style="color:#1e293b; font-size:1.2rem; display:flex; align-items:center; gap:0.5rem;">
                            <span style="width:10px; height:10px; background:#3b82f6; border-radius:50%; display:inline-block;"></span> 
                            Paid Channels <span style="background:#f1f5f9; color:#64748b; padding:0.2rem 0.6rem; border-radius:50px; font-size:0.8rem;">109</span>
                        </h3>
                    </div>
                    <div class="iptv-channels-grid">
                        <div class="iptv-channel"><img src="assets/ott/ott-hotstar.jpg" alt="Channel 1" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Sun TV<br>Network</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-zee5.png" alt="Channel 2" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Star<br>Sports</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-sonyliv.png" alt="Channel 3" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Sony<br>Network</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-discovery.png" alt="Channel 4" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Discovery<br>Channel</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-fancode.png" alt="Channel 5" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Fancode</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-jiosaavn.webp" alt="Channel 6" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>News<br>Channel</span>'"></div>
                        <div class="iptv-channel"><img src="assets/ott/ott-sunnxt.png" alt="Channel 7" onerror="this.outerHTML='<span style=\\'color:#000; font-weight:bold; font-size:0.8rem; text-align:center;\\'>Sun<br>News</span>'"></div>
                    </div>
                </div>
            </div>
            
            <!-- Office CTA -->
"""

try:
    with open('services.html', 'r', encoding='utf-8') as f:
        services_content = f.read()
    
    # Replace the Office CTA with IPTV + Office CTA
    services_content = services_content.replace('<!-- Office CTA -->', iptv_html)
    
    with open('services.html', 'w', encoding='utf-8') as f:
        f.write(services_content)
    print("Added IPTV section to services.html")
except Exception as e:
    print(f"Error updating services.html: {e}")

