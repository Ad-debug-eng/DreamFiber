import re

with open("update_services7.py", "r") as f:
    code = f.read()

# Replace ott-hotstar.webp with ott-hotstar.jpg
code = code.replace('"JioHotstar": "ott-hotstar.webp"', '"JioHotstar": "ott-hotstar.jpg"')

with open("update_services8.py", "w") as f:
    f.write(code)

import os
os.system("python update_services8.py")
