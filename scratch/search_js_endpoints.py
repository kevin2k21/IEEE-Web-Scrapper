import re
import httpx
import asyncio

async def search_js_file(client, url):
    print(f"Fetching JS: {url} ...")
    try:
        response = await client.get(url, timeout=10.0)
        text = response.text
        
        # Search for api, wp-json, graphql, application.ieeecomputer, wpcms, or relative urls
        endpoints = re.findall(r'\"(/[a-zA-Z0-9_\-\.\?/]+api/[a-zA-Z0-9_\-\.\?/]+)\"', text)
        endpoints_wp = re.findall(r'\"(/[a-zA-Z0-9_\-\.\?/]+wp-json/[a-zA-Z0-9_\-\.\?/]+)\"', text)
        endpoints_absolute = re.findall(r'\"(https?://[a-zA-Z0-9\.\-_]+(?:api|wp-json|graphql|conferences|wp-admin)[a-zA-Z0-9\.\-_/]*)\"', text)
        
        print(f" -> Found {len(endpoints)} relative APIs, {len(endpoints_wp)} WP APIs, {len(endpoints_absolute)} absolute APIs")
        
        all_found = set(endpoints + endpoints_wp + endpoints_absolute)
        for ep in all_found:
            # Let's print out if it looks relevant to conferences or calendar
            if "conf" in ep or "event" in ep or "calendar" in ep or "wp" in ep:
                print(f"    * RELEVANT ENDPOINT: {ep}")
            else:
                print(f"    * Other: {ep[:100]}")
    except Exception as e:
        print(f" -> Error: {e}")

async def main():
    with open("scratch/conferences_fetch_result.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    # Find all /_next/static/chunks/ script tags
    js_urls = re.findall(r'\"(/_next/static/chunks/[A-Za-z0-9_\-\./]+\.js)\"', html)
    print(f"Found {len(js_urls)} JS bundle URLs.")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = []
        for url in set(js_urls):
            full_url = "https://www.computer.org" + url
            tasks.append(search_js_file(client, full_url))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
