with open("scratch/conferences_combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

import re

# Let's find any string inside quotes that contains "/api/" or "http" or "wp-"
matches = re.findall(r'\"([^\"]*?(?:api|wp-|http|json)[^\"]*?)\"', stream)
print(f"Found {len(matches)} matching strings in stream:")
for m in set(matches):
    if len(m) < 150:
        print(f" - {m}")
