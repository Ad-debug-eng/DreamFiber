import re

with open('iptv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace .iptv-section styles
old_section = r"""\.iptv-section \{.*?#0f172a;.*?color: #fff;.*?\}"""
new_section = r""".iptv-section {
                        background: radial-gradient(circle at top right, rgba(200, 32, 138, 0.05), transparent), 
                                    radial-gradient(circle at bottom left, rgba(106, 43, 155, 0.05), transparent), 
                                    #f8fafc;
                        background-size: cover;
                        padding: 5rem 0;
                        color: #111827;
                        margin-top: 3rem;
                        border-radius: 20px;
                        border: 1px solid #e5e7eb;
                    }"""
content = re.sub(old_section, new_section, content, flags=re.DOTALL)

# Replace .iptv-header h2 styles
old_h2 = r"""\.iptv-header h2 \{.*?color: #fff;.*?\}"""
new_h2 = r""".iptv-header h2 {
                        font-size: 2.5rem;
                        color: #111827;
                        margin-bottom: 0.5rem;
                    }"""
content = re.sub(old_h2, new_h2, content, flags=re.DOTALL)

# Replace .iptv-header p styles
old_p = r"""\.iptv-header p \{.*?color: #94a3b8;.*?\}"""
new_p = r""".iptv-header p {
                        color: #4b5563;
                        font-size: 1.1rem;
                    }"""
content = re.sub(old_p, new_p, content, flags=re.DOTALL)

with open('iptv.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated iptv.html theme.")
