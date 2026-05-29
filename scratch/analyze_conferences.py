import re

with open("scratch/conferences_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r'self\.__next_f\.push\(\[1,\"(.*?)\"\]\)'
matches = re.findall(pattern, html)

print(f"Found {len(matches)} push matches.")

full_stream = ""
for m in matches:
    full_stream += m.replace('\\"', '"').replace('\\\\', '\\')

with open("scratch/conferences_combined_stream.txt", "w", encoding="utf-8") as f:
    f.write(full_stream)
print("Saved combined stream to scratch/conferences_combined_stream.txt")

# Let's search for keywords like "India" or "Conference" or city names or common calendar fields
# In conference calendars, there might be fields like "city", "country", "venue", "dates" or titles
print("\nSearching for some keywords...")
keywords = ["India", "Conference", "Submissions", "Abstract", "Dates", "Date"]
for kw in keywords:
    count = full_stream.count(kw)
    print(f" - {kw}: {count} occurrences")

# Let's look for structured conference cards or lists in the stream.
# Let's search for patterns in the stream.
# We can print some sections that mention "India"
print("\nSample snippets around 'India':")
idx = full_stream.find("India")
while idx != -1:
    print(f"\n--- Found India at {idx} ---")
    print(full_stream[idx-150:idx+250])
    idx = full_stream.find("India", idx+1)
    if idx > 300000 or idx == -1: # cap it or stop if not found
        break
