import re
import glob

template = """<nav class="nav-links">
                <a href="index.html" class="{active_home}">Home</a>
                <a href="contact.html" class="{active_enterprise}">Enterprise Solution</a>
                <div class="nav-dropdown">
                    <a href="javascript:void(0)" class="nav-dropbtn {active_broadband}">Home Broadband <ion-icon name="chevron-down-outline"></ion-icon></a>
                    <div class="nav-dropdown-content">
                        <a href="broadband.html">Broadband</a>
                        <a href="broadband-ott.html">Broadband + OTT</a>
                    </div>
                </div>
                <a href="ott.html" class="{active_ott}">OTT</a>
                <a href="iptv.html" class="{active_iptv}">IPTV</a>
                <div class="nav-dropdown">
                    <a href="javascript:void(0)" class="nav-dropbtn {active_support}">Support <ion-icon name="chevron-down-outline"></ion-icon></a>
                    <div class="nav-dropdown-content">
                        <a href="about.html">About Us</a>
                        <a href="javascript:void(0)" onclick="alert('FAQs coming soon!')">FAQs (Quick Answer)</a>
                        <a href="contact.html">Contact Us (WhatsApp or Call)</a>
                    </div>
                </div>
            </nav>
            
            <div class="nav-actions">
                <a href="javascript:void(0)" onclick="alert('Under Construction')" class="btn btn-primary" style="margin-right: 0.5rem;">Pay Bill</a>
                <a href="https://wa.me/919272162704?text=Hi+Dream+Fiber%21+I%27m+interested+in+a+new+fiber+broadband+connection.+Please+check+feasibility+for+my+area." target="_blank" class="btn btn-outline">
                    <ion-icon name="logo-whatsapp" style="margin-right: 0.5rem;"></ion-icon> WhatsApp
                </a>
            </div>"""

files = ['index.html', 'services.html', 'about.html', 'contact.html', 'broadband.html', 'broadband-ott.html', 'iptv.html', 'ott.html']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Build the replacement string with appropriate active classes
        act_home = 'active' if f == 'index.html' else ''
        act_broadband = 'active' if f in ('services.html', 'broadband.html', 'broadband-ott.html') else ''
        act_iptv = 'active' if f == 'iptv.html' else ''
        act_support = 'active' if f in ('about.html', 'contact.html') else ''
        act_ott = 'active' if f == 'ott.html' else ''
        
        # Determine the active string
        repl = template.format(
            active_home=act_home,
            active_enterprise='',
            active_broadband=act_broadband,
            active_ott=act_ott,
            active_iptv=act_iptv,
            active_support=act_support
        )
        # Clean up empty class=""
        repl = repl.replace(' class=""', '')
        
        # Regex to match <nav class="nav-links">...</nav>
        # And <div class="nav-actions">...</div>
        pattern = re.compile(r'<nav class="nav-links">.*?</nav>\s*<div class="nav-actions">.*?</div>', re.DOTALL)
        
        new_content = pattern.sub(repl, content)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Updated {f}')
    except Exception as e:
        print(f'Error processing {f}: {e}')

# Update in python scripts too
py_files = glob.glob('*.py')
for f in py_files:
    if f == 'update_nav.py': continue
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if '<nav class="nav-links">' in content:
            # We just do a simple replacement for the OTT href
            new_content = content.replace('href="index.html#ott-hub"', 'href="ott.html"')
            new_content = new_content.replace('href="#ott-hub"', 'href="ott.html"')
            if new_content != content:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f'Updated {f} navbar links')
    except:
        pass
