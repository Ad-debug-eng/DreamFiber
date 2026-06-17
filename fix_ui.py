import glob

# 1. Fix the gap issue in broadband-ott.html, broadband.html, services.html
files = glob.glob('*.html') + glob.glob('*.py')
old_style = "margin-top: 1rem; margin-bottom: -1.5rem; display: flex; align-items: center; justify-content: center; gap: 1rem; color: var(--text-muted); font-weight: 600; font-family: 'Inter', sans-serif;"
new_style = "margin-top: 1rem; margin-bottom: -1.5rem; display: flex; align-items: center; justify-content: center; gap: 1rem; color: var(--text-muted); font-weight: 600; font-family: 'Inter', sans-serif;"

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if old_style in content:
            new_content = content.replace(old_style, new_style)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Fixed gap in {f}')
    except:
        pass

# 2. Re-create ott.html with better UI and no literal \n
import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

header_match = re.search(r'(<!DOCTYPE html>.*?</header>)', index_html, re.DOTALL)
footer_match = re.search(r'(<footer>.*</html>)', index_html, re.DOTALL)

header = header_match.group(1)
footer = footer_match.group(1)
header = re.sub(r'<title>.*?</title>', '<title>OTT Partners | Dream IPTV & Internet</title>', header)
header = header.replace('href="index.html#ott-hub"', 'href="ott.html"').replace('href="#ott-hub"', 'href="ott.html"')

ott_files = os.listdir('assets/ott')
ott_items = []

name_mapping = {
    'ott-ahatamil.png': 'Aha Tamil',
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
    
    # improved styling for each tile inline
    ott_items.append(f'''
                <div class="ott-logo-tile" style="background:#fff; border-radius:16px; padding:1.5rem; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.03); border:1px solid rgba(200,32,138,0.1); transition:transform 0.3s ease, box-shadow 0.3s ease; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:0.75rem; aspect-ratio:1/1;">
                    <img src="assets/ott/{file}" alt="{name}" style="max-width:80%; max-height:80%; object-fit:contain; border-radius:12px;">
                    <span style="font-weight:700; font-family:'Inter',sans-serif; font-size:0.9rem; color:#1f2937;">{name}</span>
                </div>''')

# Fix literal \n by not using it inside string literal that gets written directly without evaluation
ott_grid = "\n".join(ott_items)

ott_content = f"""
    <style>
        .ott-logo-tile:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(200,32,138,0.1) !important;
            border-color: rgba(200,32,138,0.4) !important;
        }}
    </style>
    <!-- Page Header -->
    <section class="page-header" style="padding-bottom: 2rem;">
        <div class="container">
            <h1 class="text-gradient">Premium OTT Partners</h1>
            <p style="color:var(--text-muted);max-width:600px;margin:.75rem auto 0;font-size:1.1rem;">
                Experience the ultimate entertainment with our bundled OTT plans. We bring all your favorite streaming apps directly to your screens.
            </p>
        </div>
    </section>

    <!-- OTT Section -->
    <section class="ott-hub section" style="background: linear-gradient(180deg, #fff 0%, #fef2f8 100%); padding-top: 1rem;">
        <div class="container">
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
                {ott_grid}
            </div>
            
            <div class="office-cta" style="background: #fff; border: 1.5px solid rgba(200,32,138,0.3); border-radius: 20px; padding: 4rem 2rem; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.05); position:relative; overflow:hidden;">
                <div style="position:absolute; top:-50%; left:-10%; width:300px; height:300px; background:radial-gradient(circle, rgba(200,32,138,0.1) 0%, transparent 70%); border-radius:50%;"></div>
                <div style="position:absolute; bottom:-50%; right:-10%; width:400px; height:400px; background:radial-gradient(circle, rgba(106,43,155,0.1) 0%, transparent 70%); border-radius:50%;"></div>
                
                <h2 style="font-size: 2.5rem; margin-bottom: 1rem; position:relative; z-index:1;" class="text-gradient">Ready to Upgrade Your Entertainment?</h2>
                <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto 2.5rem; font-size:1.1rem; position:relative; z-index:1;">Combine your high-speed Dream internet with these premium OTT subscriptions and save money every month on separate bills.</p>
                <div class="cta-buttons" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; position:relative; z-index:1;">
                    <a href="broadband-ott.html" class="btn btn-primary" style="padding: 1rem 2.5rem; font-size: 1.1rem;">
                        View Bundled Plans
                    </a>
                    <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I%27m+interested+in+your+OTT+bundle+plans." target="_blank" class="btn btn-outline" style="padding: 1rem 2.5rem; font-size: 1.1rem; border-color: rgba(200,32,138,0.3);">
                        Chat on WhatsApp
                    </a>
                </div>
            </div>
        </div>
    </section>
"""

with open('ott.html', 'w', encoding='utf-8') as f:
    f.write(header + '\n' + ott_content + '\n' + footer)
print("Recreated ott.html with premium design")
