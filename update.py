import re

new_html = """            <h3 style="text-align:center;margin-bottom:1rem;">Broadband with OTT + Live TV</h3>
            <div class="simple-table-wrap">
                <table class="ott-krishii-table">
                    <thead>
                        <tr>
                            <th>PLAN</th>
                            <th>OTT + LIVE TV</th>
                        </tr>
                    </thead>
                    <tbody>"""

for speed in ["50 Mbps", "100 Mbps", "200 Mbps", "300 Mbps", "1 Gbps"]:
    new_html += f"""
                        <tr>
                            <td class="plan-col"><h3>{speed}</h3></td>
                            <td class="ott-col">
                                <div class="ott-grid">
                                    <div class="ott-app"><div class="ott-placeholder">Netflix<br>(Basic)</div><span>Netflix</span></div>
                                    <div class="ott-app"><img src="assets/ott/primevideo.png" alt="Amazon" onerror="this.outerHTML='<div class=\\'ott-placeholder\\'>Amazon<br>(Lite)</div>'"><span>Amazon (Lite)</span></div>
                                    <div class="ott-app"><img src="assets/ott/jiohotstar.png" alt="JioHotstar" onerror="this.outerHTML='<div class=\\'ott-placeholder\\'>JioHotstar</div>'"><span>JioHotstar (A)</span></div>
                                    <div class="ott-app"><img src="assets/ott/zee5.png" alt="ZEE5" onerror="this.outerHTML='<div class=\\'ott-placeholder\\'>ZEE5</div>'"><span>ZEE5</span></div>
                                    <div class="ott-app"><img src="assets/ott/sonyliv.png" alt="SonyLIV" onerror="this.outerHTML='<div class=\\'ott-placeholder\\'>SonyLIV</div>'"><span>SonyLIV</span></div>
                                    <div class="ott-app"><div class="ott-placeholder">Discovery+</div><span>DiscoveryPlus</span></div>
                                    <div class="ott-app"><div class="ott-placeholder">Fancode</div><span>Fancode</span></div>
                                    <div class="ott-app"><div class="ott-placeholder">Jio Saavn</div><span>Jio Saavn</span></div>
                                </div>
                                <button class="ott-toggle-btn" onclick="toggleOtt(this)">+17 More Apps</button>
                                <div class="ott-dropdown">
                                    <div class="ott-grid">
                                        <div class="ott-app"><div class="ott-placeholder">Aha Tamil</div><span>Aha Tamil</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Chana Jor</div><span>Chana Jor</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Chaupal</div><span>Chaupal</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Dangal Play</div><span>Dangal Play</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">DistroTV</div><span>DistroTV</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">ETV Win</div><span>ETV Win</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Hungama</div><span>Hungama</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Kanccha<br>Lannka</div><span>Kanccha Lannka</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">OM TV</div><span>OM TV</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Raj Digital</div><span>Raj DigitalTV</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Shemaroo</div><span>Shemaroo</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Shorts Tv</div><span>Shorts Tv</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Shucae<br>Flim</div><span>Shucae Flim</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Stage</div><span>Stage</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">SunNXT</div><span>SunNXT</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">TravelXP</div><span>TravelXP</span></div>
                                        <div class="ott-app"><div class="ott-placeholder">Waves</div><span>Waves</span></div>
                                    </div>
                                </div>
                                <div class="ott-live-text">450+ Live Channels & Many More OTTs<br><small style="color:#666;">Unlimited Internet Included</small></div>
                            </td>
                        </tr>"""

new_html += """
                    </tbody>
                </table>
            </div>"""

def process_file(filepath, start_marker, end_marker):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will replace everything from start_marker to end_marker
    pattern = re.compile(re.escape(start_marker) + r'.*?' + re.escape(end_marker), re.DOTALL)
    
    # We remove the end marker as well, or we can keep it depending on logic.
    # In index.html: start = <h3 style="text-align:center;margin-bottom:1rem;">Regular WiFi Plan</h3>
    # end = <p class="note-text">* Amazon Prime available only on 12-month plans.</p>
    
    new_content = pattern.sub(new_html, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Index.html
index_start = '<h3 style="text-align:center;margin-bottom:1rem;">Regular WiFi Plan</h3>'
index_end = '<p class="note-text">* Amazon Prime available only on 12-month plans.</p>'
process_file('index.html', index_start, index_end)

# services.html
# services.html has <h2 style="text-align:center;margin-bottom:1rem;">Regular WiFi Plan</h2>
serv_start = '<h2 style="text-align:center;margin-bottom:1rem;">Regular WiFi Plan</h2>'
serv_end = '<p class="note-text">* Amazon Prime OTT available only for 12-month subscriptions.</p>'
process_file('services.html', serv_start, serv_end)

print("Done")
