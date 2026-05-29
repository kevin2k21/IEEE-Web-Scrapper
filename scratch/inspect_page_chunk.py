import httpx
import re

url = "https://www.computer.org/_next/static/chunks/app/%5B...url%5D/page-988957c247cb5788.js"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

print(f"Fetching: {url}")
resp = httpx.get(url, headers=headers)
text = resp.text
print(f"Length: {len(text)}")

# Save JS file locally for inspection
with open("scratch/page_chunk.js", "w", encoding="utf-8") as f:
    f.write(text)

# Search for any api, wp-json, or fetch links
matches = re.findall(r'\"([a-zA-Z0-9_\-\.\?:/]+/wp-json/[a-zA-Z0-9_\-\.\?:/]+)\"', text)
matches_api = re.findall(r'\"([a-zA-Z0-9_\-\.\?:/]+/api/[a-zA-Z0-9_\-\.\?:/]+)\"', text)
matches_wpcms = re.findall(r'https?://[a-zA-Z0-9\.\-_]+', text)

print("wp-json:", set(matches))
print("api:", set(matches_api))
print("domains:", set(matches_wpcms))
