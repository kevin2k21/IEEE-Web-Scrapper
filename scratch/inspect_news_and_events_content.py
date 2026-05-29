with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Find sections around "News & Events"
idx = html.find("News & Events")
if idx != -1:
    print("\n--- News & Events Content ---")
    print(html[idx:idx+1500])
else:
    print("News & Events not found")
