import re

with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# Let's search for \d+:T
matches = re.findall(r'(\d+):T([A-Za-z0-9]+)', stream)
print(f"Found {len(matches)} matches of \\d+:T")
print("Sample matches:", matches[:10])
