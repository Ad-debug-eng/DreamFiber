import glob
import re

files = glob.glob('*.html') + glob.glob('*.py')

search_text = r'(Home user pricing with clear monthly savings\. Free installation on all plans\.</p>)'
replace_text = r'''\1
            <div style="margin-top: 1rem; margin-bottom: -1.5rem; display: flex; align-items: center; justify-content: center; gap: 1rem; color: var(--text-muted); font-weight: 600; font-family: 'Inter', sans-serif;">
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #fff; padding: 0.5rem 1rem; border-radius: 50px; border: 1.5px solid var(--border-light); box-shadow: var(--shadow-sm);">
                    <ion-icon name="tv-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="tablet-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="phone-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <span style="font-size: 0.9rem;">Watch on TV, Tablet and mobile</span>
                </div>
            </div>'''

# also handle cases without closing p tag on the same line
search_text2 = r'(Home user pricing with clear monthly savings\. Free installation on all plans\.)'
replace_text2 = r'''\1
            </p>
            <div style="margin-top: 1rem; margin-bottom: -1.5rem; display: flex; align-items: center; justify-content: center; gap: 1rem; color: var(--text-muted); font-weight: 600; font-family: 'Inter', sans-serif;">
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #fff; padding: 0.5rem 1rem; border-radius: 50px; border: 1.5px solid var(--border-light); box-shadow: var(--shadow-sm);">
                    <ion-icon name="tv-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="tablet-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="phone-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <span style="font-size: 0.9rem;">Watch on TV, Tablet and mobile</span>
                </div>
            </div>'''

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if "Watch on TV, Tablet and mobile" in content:
            continue
            
        # Check how it's formatted
        if "plans.</p>" in content:
            new_content = re.sub(search_text, replace_text, content)
        else:
            # Need to be careful here to not add extra </p> if it's there on the next line
            # Let's just use a more robust regex
            # Find the paragraph containing the text and insert the div after it.
            pattern = re.compile(r'(<p[^>]*>.*?Home user pricing.*?plans\.\s*</p>)', re.DOTALL)
            
            replacement = r'''\1
            <div style="margin-top: 1rem; margin-bottom: -1.5rem; display: flex; align-items: center; justify-content: center; gap: 1rem; color: var(--text-muted); font-weight: 600; font-family: 'Inter', sans-serif;">
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #fff; padding: 0.5rem 1rem; border-radius: 50px; border: 1.5px solid var(--border-light); box-shadow: var(--shadow-sm);">
                    <ion-icon name="tv-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="tablet-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <ion-icon name="phone-portrait-outline" style="font-size: 1.2rem; color: var(--primary);"></ion-icon>
                    <span style="font-size: 0.9rem;">Watch on TV, Tablet and mobile</span>
                </div>
            </div>'''
            
            new_content = pattern.sub(replacement, content)

        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Updated {f}')
    except Exception as e:
        print(f"Error {f}: {e}")
