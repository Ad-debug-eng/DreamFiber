import re

with open('broadband-ott.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the prices
prices = {
    "Mini": [("1 Month", "499", None), ("3 Months", "1,300", "₹197"), ("6 Months", "2,500", "₹494"), ("12 Months", "5,000", "₹988")],
    "Basic": [("1 Month", "699", None), ("3 Months", "1,700", "₹397"), ("6 Months", "3,500", "₹694"), ("12 Months", "6,200", "₹2,188")],
    "Standard": [("1 Month", "899", None), ("3 Months", "2,300", "₹397"), ("6 Months", "5,000", "₹394"), ("12 Months", "9,000", "₹1,788")],
    "Premium": [("1 Month", "1,300", None), ("3 Months", "3,500", "₹400"), ("6 Months", "7,000", "₹800"), ("12 Months", "13,000", "₹2,600")]
}

def generate_pricing_html(plan_name):
    price_rows = ""
    for duration, price, save in prices[plan_name]:
        save_html = f' <small style="color: #059669; font-weight: 700;">(Save {save})</small>' if save else ''
        price_rows += f"""
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.88rem; color: #1f2937; font-weight: 600; padding: 0.35rem 0.6rem; background: #f8fafc; border-radius: 6px; border: 1px solid #f1f5f9;">
                    <span>{duration}</span>
                    <span>₹{price}{save_html}</span>
                </div>
        """
    return f"""
            <div class="k-ott-title" style="color: #6b7280; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 1.5rem; margin-bottom: 0.8rem;">Pricing Durations</div>
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
                {price_rows}
            </div>"""

def add_prices(match):
    # match.group(1) is the <span class="k-plan-name">PlanName</span>
    # match.group(2) is the entire card body before the closing </div> of k-card-body
    plan_name = match.group(1)
    body = match.group(2)
    pricing_html = generate_pricing_html(plan_name)
    return f'<span class="k-plan-name">{plan_name}</span>{body}{pricing_html}\n        </div>\n        <div class="k-card-footer">'

# Regex to match the plan name and the body of the card up to the end of k-card-body
pattern = re.compile(r'<span class="k-plan-name">(Mini|Basic|Standard|Premium)</span>(.*?)</div>\s*</div>\s*<div class="k-card-footer">', re.DOTALL)
new_content = pattern.sub(add_prices, content)

with open('broadband-ott.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Prices added to broadband-ott.html successfully.")
