import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# We want to remove from <section class="section bg-light" id="plans">
# up to </section> before <section class="ott-hub" id="ott-hub">

start_marker = '<section class="section bg-light" id="plans">'
end_marker = '</section>\n\n    <section class="ott-hub" id="ott-hub">'

pattern = re.compile(re.escape(start_marker) + r'.*?' + re.escape(end_marker), re.DOTALL)

new_content = pattern.sub('<section class="ott-hub" id="ott-hub">', content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
