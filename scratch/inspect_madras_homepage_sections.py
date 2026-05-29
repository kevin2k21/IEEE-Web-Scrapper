with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Find sections around "Events & Announcements"
idx = html.find("Events & Announcements")
if idx != -1:
    print("\n--- Events & Announcements Section ---")
    print(html[idx-200:idx+1500])
else:
    print("Events & Announcements heading not found")

idx2 = html.find("News & Events")
if idx2 != -1:
    print("\n--- News & Events Section ---")
    print(html[idx2-200:idx2+1500])
else:
    print("News & Events heading not found")
