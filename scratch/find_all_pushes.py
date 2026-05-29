with open("scratch/conferences_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# Find any occurrences of self.__next_f.push
pushes = re.findall(r'self\.__next_f\.push\((.*?)\)', html, re.DOTALL)
print(f"Total pushes found: {len(pushes)}")

for i, p in enumerate(pushes[:15]):
    print(f"\nPush {i}: length={len(p)}")
    print(p[:300] + ("..." if len(p) > 300 else ""))
