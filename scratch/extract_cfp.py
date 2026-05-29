import re
import json

with open("scratch/ieee_cs_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all self.__next_f.push([1, "..." ]) blocks
pattern = r'self\.__next_f\.push\(\[1,\"(.*?)\"\]\)'
matches = re.findall(pattern, html)

print(f"Found {len(matches)} next_f.push matches.")

full_stream = ""
for m in matches:
    # Unescape the escaped double quotes and other escaped characters if needed,
    # but let's just combine the raw string chunks first.
    # Note: the match has escaped quotes like \"
    # We can reconstruct it.
    full_stream += m.replace('\\"', '"').replace('\\\\', '\\')

print(f"Combined stream length: {len(full_stream)}")

# Let's search for "cfp-card" or some CFP titles in the combined stream
with open("scratch/combined_stream.txt", "w", encoding="utf-8") as f:
    f.write(full_stream)
print("Saved combined stream to scratch/combined_stream.txt")

# Let's look for titles, URLs, descriptions, deadlines
# Let's search for some patterns
print("\nSearching for titles...")
# Example: Let's find links to individual calls for papers or titles.
# Let's print out a few lines that mention "Call For Paper Card"
for line in full_stream.split('{"aria-label":"Call For Paper Card"'):
    print("\n--- Card Split ---")
    print(line[:500])
