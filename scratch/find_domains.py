import re

with open("scratch/conferences_combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# Find all links starting with http or https
links = re.findall(r'https?://[A-Za-z0-9\.\-_/]+', stream)
print(f"Found {len(links)} links in stream:")
for l in set(links):
    print(f" - {l}")

with open("scratch/conferences_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all links starting with http or https in HTML
links_html = re.findall(r'https?://[A-Za-z0-9\.\-_/]+', html)
print(f"\nFound {len(links_html)} links in HTML:")
# Print unique domains/subdomains
domains = set()
for l in links_html:
    m = re.match(r'https?://([A-Za-z0-9\.\-_]+)', l)
    if m:
        domains.add(m.group(1))
for d in domains:
    print(f" - {d}")
