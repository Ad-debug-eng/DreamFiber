import re

with open('broadband-ott.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the correct OTT prices
prices = {
    "Mini": [("3 Months", "1,797"), ("6 Months", "3,299"), ("12 Months", "5,999")],
    "Basic": [("3 Months", "2,397"), ("6 Months", "4,499"), ("12 Months", "8,399")],
    "Standard": [("3 Months", "2,997"), ("6 Months", "5,699"), ("12 Months", "10,799")],
    "Premium": [("3 Months", "3,897"), ("6 Months", "7,494"), ("12 Months", "14,388")]
}

def generate_pricing_html(plan_name):
    price_rows = ""
    for duration, price in prices[plan_name]:
        price_rows += f"""
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.88rem; color: #1f2937; font-weight: 600; padding: 0.35rem 0.6rem; background: #f8fafc; border-radius: 6px; border: 1px solid #f1f5f9;">
                    <span>{duration}</span>
                    <span>₹{price}</span>
                </div>
        """
    return f"""
            <div class="k-ott-title" style="color: #6b7280; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.8rem;">Pricing Durations</div>
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
                {price_rows}
            </div>"""

def add_prices(match):
    plan_name = match.group(1)
    body = match.group(2)
    pricing_html = generate_pricing_html(plan_name)
    return f'<span class="k-plan-name">{plan_name}</span>{body}{pricing_html}\n        </div>\n        <div class="k-card-footer">'

# Regex to match the plan name and the body of the card up to the end of k-card-body
# It should strip out any existing pricing HTML
def strip_and_add(match):
    plan_name = match.group(1)
    body = match.group(2)
    
    # Remove existing pricing block if present
    body = re.sub(r'<div class="k-ott-title" style="color: #6b7280; font-size: 0\.75rem.*?</div>\s*</div>', '', body, flags=re.DOTALL)
    
    pricing_html = generate_pricing_html(plan_name)
    return f'<span class="k-plan-name">{plan_name}</span>{body}{pricing_html}\n        </div>\n        <div class="k-card-footer">'

pattern = re.compile(r'<span class="k-plan-name">(Mini|Basic|Standard|Premium)</span>(.*?)</div>\s*</div>\s*<div class="k-card-footer">', re.DOTALL)
new_content = pattern.sub(strip_and_add, content)

with open('broadband-ott.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed OTT prices in broadband-ott.html successfully.")
