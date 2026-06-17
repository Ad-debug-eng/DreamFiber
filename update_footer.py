import re

files = ['index.html', 'about.html', 'contact.html', 'broadband.html', 'broadband-ott.html', 'iptv.html', 'services.html']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the footer links
        old_footer_links = """<div class="footer-links">
                <h4>Services</h4>
                <a href="services.html">Fiber Internet Plans</a>
                <a href="services.html">OTT Bundles</a>
                <a href="services.html">IPTV Channels</a>"""
        
        new_footer_links = """<div class="footer-links">
                <h4>Services</h4>
                <a href="broadband.html">Fiber Internet Plans</a>
                <a href="broadband-ott.html">OTT Bundles</a>
                <a href="iptv.html">IPTV Channels</a>"""
                
        content = content.replace(old_footer_links, new_footer_links)
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated footer in {f}')
    except Exception as e:
        print(f'Error processing {f}: {e}')
