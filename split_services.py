import re

with open('services.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract top header (up to <!-- Page Header -->)
m1 = re.search(r'(.*?)(<!-- Page Header -->)', html, re.DOTALL)
top_header = m1.group(1)

# Extract Page Header
m2 = re.search(r'(<!-- Page Header -->.*?</section>)', html, re.DOTALL)
page_header_section = m2.group(1)

# Extract container start (up to Business Fiber Banner)
m3 = re.search(r'(<section class="section">\s*<div class="container"[^>]*>.*?<div class="business-fiber-banner">.*?</div>)', html, re.DOTALL)
container_start = m3.group(1)

# Combined page header
full_page_header = page_header_section + "\n" + container_start

# Extract Styles
m_style = re.search(r'(<style>.*?</style>)', html, re.DOTALL)
style_html = m_style.group(1)
# Remove display none from plan-section since they are separate pages now
style_html = style_html.replace('.plan-section {\n    display: none;\n}', '')
style_html = style_html.replace('.plan-section.active {\n    display: block;\n}', '')

# Extract Broadband section
m_bb = re.search(r'(<div id="section-broadband"[^>]*>.*?)(?=<div id="section-broadband-ott")', html, re.DOTALL)
bb_html = m_bb.group(1)

# Extract Broadband OTT section
m_ott = re.search(r'(<div id="section-broadband-ott"[^>]*>.*?)(?=<!-- IPTV Section -->)', html, re.DOTALL)
ott_html = m_ott.group(1)

# Extract IPTV section
m_iptv = re.search(r'(<!-- IPTV Section -->.*?)(?=<script>|\s*</body>)', html, re.DOTALL)
iptv_html = m_iptv.group(1)

# Footer Scripts (Everything after IPTV section)
m_scripts = re.search(r'(<script>.*)', html, re.DOTALL)
if m_scripts:
    scripts_html = m_scripts.group(1)
else:
    scripts_html = "</body>\n</html>"

# We don't need the tab switching script anymore.
# Let's clean up scripts_html
scripts_html = re.sub(r'function switchMainTab\(tabId\).*?\}\s*\);', '', scripts_html, flags=re.DOTALL)
# And the event listeners for hash
scripts_html = re.sub(r'window\.addEventListener\(\'DOMContentLoaded\'.*?\}\);', '', scripts_html, flags=re.DOTALL)
scripts_html = re.sub(r'window\.addEventListener\(\'hashchange\'.*?\}\);', '', scripts_html, flags=re.DOTALL)


# Write broadband.html
with open('broadband.html', 'w', encoding='utf-8') as f:
    f.write(top_header + full_page_header + "\n" + style_html + "\n" + bb_html + "\n</div>\n</section>\n\n" + scripts_html)

# Write broadband-ott.html
# Let's change the subtitle of the page header slightly
ott_header = full_page_header.replace('Plans & Pricing', 'Broadband + OTT Bundles')
with open('broadband-ott.html', 'w', encoding='utf-8') as f:
    f.write(top_header + ott_header + "\n" + style_html + "\n" + ott_html + "\n</div>\n</section>\n\n" + scripts_html)

# Write iptv.html
# iptv_html is outside the container in the original code, so we can just drop it directly after top_header
with open('iptv.html', 'w', encoding='utf-8') as f:
    f.write(top_header + iptv_html + "\n" + scripts_html)

print("Split completed successfully.")
