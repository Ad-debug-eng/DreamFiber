import os
import shutil
import re

# 1. Create ott.html based on index.html but with OTT list
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract header and footer
header_match = re.search(r'(<!DOCTYPE html>.*?</header>)', index_html, re.DOTALL)
footer_match = re.search(r'(<footer>.*</html>)', index_html, re.DOTALL)

if not header_match or not footer_match:
    print("Could not find header or footer.")
    exit(1)

header = header_match.group(1)
footer = footer_match.group(1)

# Fix title
header = re.sub(r'<title>.*?</title>', '<title>OTT Partners | Dream IPTV & Internet</title>', header)

# Get all ott images
ott_files = os.listdir('assets/ott')
ott_items = []

name_mapping = {
    'ott-ahatamil.png': 'Aha Tamil',
    'ott-chanajor.png': 'Chaupal', # wait, chanajor is Chanajor
    'ott-chaupal.jpg': 'Chaupal',
    'ott-dangalplay.jpg': 'Dangal Play',
    'ott-discovery.png': 'Discovery+',
    'ott-distrotv.jpg': 'DistroTV',
    'ott-etvwin.png': 'ETV Win',
    'ott-fancode.png': 'Fancode',
    'ott-fridaay.jpg': 'Fridaay',
    'ott-hotstar.jpg': 'Hotstar',
    'ott-hungama.png': 'Hungama',
    'ott-itap.png': 'iTap',
    'ott-jiosaavn.webp': 'Jio Saavn',
    'ott-kancchalannka.jpg': 'Kancchalannka',
    'ott-netflix.png': 'Netflix',
    'ott-omtv.jpg': 'OMTV',
    'ott-prime.png': 'Prime Video',
    'ott-rajtv.png': 'RajTV',
    'ott-shemaroome.png': 'ShemarooMe',
    'ott-shorts.png': 'Shorts',
    'ott-shucaefilm.jpg': 'Shucaefilm',
    'ott-sonyliv.png': 'Sony LIV',
    'ott-stage.png': 'Stage',
    'ott-sunnxt.png': 'SunNXT',
    'ott-travelxp.png': 'Travelxp',
    'ott-waves.jpg': 'Waves',
    'ott-zee5.png': 'ZEE5',
    'ott-chanajor.png': 'Chanajor'
}

for file in ott_files:
    if not file.startswith('ott-'): continue
    name = name_mapping.get(file, file.split('.')[0].replace('ott-', '').title())
    
    ott_items.append(f'<div class="ott-logo-tile"><img src="assets/ott/{file}" alt="{name}"><span>{name}</span></div>')

ott_grid = "\\n                ".join(ott_items)

ott_content = f"""
    <!-- Page Header -->
    <section class="page-header">
        <div class="container">
            <h1 class="text-gradient">Our Official Partners</h1>
            <p style="color:var(--text-muted);max-width:600px;margin:.75rem auto 0;font-size:1.1rem;">
                New OTT shows and bundled entertainment updates. We bring all your favorite streaming apps in one place.
            </p>
        </div>
    </section>

    <!-- OTT Section -->
    <section class="ott-hub section bg-light" id="ott-hub" style="padding-top: 2rem;">
        <div class="container">
            <div class="ott-logos-grid">
                {ott_grid}
            </div>
            
            <div class="office-cta" style="background: linear-gradient(135deg, #fef2f8, #f3e8ff); border: 1.5px solid rgba(200,32,138,0.2); border-radius: 16px; padding: 3rem 2rem; text-align: center; margin-top: 4rem;">
                <h2 style="font-size: 2rem; margin-bottom: 1rem;">Looking for OTT Bundled Plans?</h2>
                <p style="color: var(--text-muted); max-width: 500px; margin: 0 auto 2rem;">Combine your high-speed internet with premium OTT subscriptions and save money every month.</p>
                <div class="cta-buttons" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                    <a href="broadband-ott.html" class="btn btn-primary">
                        View Broadband + OTT Plans
                    </a>
                </div>
            </div>
        </div>
    </section>
"""

with open('ott.html', 'w', encoding='utf-8') as f:
    f.write(header + '\\n' + ott_content + '\\n' + footer)

print("Created ott.html")
