import re
import glob

image_mapping = {
    "Colors Cineplex Superhits": "Colors_Cineplex_Superhits_logo.jpg",
    "Colors Cineplex HD": "colors cineplex.png",
    "Colors Cineplex Bollywood": "colors ciniplex bollywood.jpg",
    "Sony Max HD": "SONY MAX HD.png",
    "Zee Cinema HD": "ZEE Cenema HD.png",
    "Zee Action": "Zee_Action_2023_logo.png",
    "Zee Classic": "Zeeclassic_new.webp",
    "Sony Pix HD": "SONY Pix HD.png",
    "Zee Talkies HD": "Zee_talkies_hd.webp",
    "Star Utsav Movies": "Starutsavmovies.jpg",
    "Star Gold Thrills": "025656-star-gold-thrills-logo-white-bg.png",
    "Star Movies Select HD": "Star-Movies-Select.png",
    "Star Gold 2 HD": "Star-Gold-2-HD-1.png",
    "Nazara": "nazara-technologies-logo-png_seeklogo-400001.png",
    "MNX HD": "mnxhd.jpg",
    "Big Magic": "BIG_Magic_Logo.jpg",
    "MN+ HD": "MN+ HD.png",
    "Show Box": "Showbox_logo.webp",
    "Colors Infinity HD": "COLORS-INFINITY-HD.png",
    "&flix HD": "flix-hd-logo-png_seeklogo-432038.png",
    "Movies Now HD": "Movies_Now_logo.png",
    "Euro Sports": "112604-110070-Eurosport.avif",
    "CNN International": "CNNinternational-logo.png",
    "ET Now": "ET-now.webp",
    "News 18 India": "News18_India.svg.png",
    "News 18 Lokmat": "News18_Lokmat_Logo.svg.png",
    "Star Sports First": "STAR-SPORTS-FIRST.webp",
    "Star Sports HD 1": "Star-Sports-1-hd.avif",
    "Star Sports 3": "Star-Sports-3-1.png",
    "Star Sports select 1 Hd": "Star-Sports-Select-HD-1-1-1200x675.png",
    "Star Sports select 2 Hd": "Star-Sports-Select-HD-2-1.png",
    "CNBC TV 18 Prime HD": "cnbc-tv18-prime-hd.webp",
    "CNBC Awaz": "cnbc.png",
    "National Geographic HD": "national geographic channel hd.png",
    "Discovery Kids": "2016_Discovery_Kids_logo.svg.png",
    "Zee TV HD": "1535097258_cDTJkL_Zee_new.avif"
}

def replacer(match):
    name = match.group(1)
    category = match.group(2)
    logo = match.group(3)
    color = match.group(4)
    
    if "<img" in logo:
        return match.group(0)
    
    if name in image_mapping:
        img_src = f"assets/iptv/{image_mapping[name]}"
        new_logo = f"<img src='{img_src}' alt='{name}' style='max-width:100%; max-height:100%; object-fit:contain;'>"
        new_color = "#fff"
        return f'{{ name: "{name}", category: "{category}", logo: "{new_logo}", color: "{new_color}" }}'
    return match.group(0)

pattern = r'\{\s*name:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*logo:\s*"([^"]+)",\s*color:\s*"([^"]+)"\s*\}'

files_to_update = glob.glob("*.*")

for filepath in files_to_update:
    if filepath.endswith('.html') or filepath.endswith('.py'):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = re.sub(pattern, replacer, content)

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {filepath} with images.")
        except Exception:
            pass
