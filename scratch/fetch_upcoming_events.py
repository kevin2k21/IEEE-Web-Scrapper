import asyncio
import httpx

async def main():
    url = "https://ieeemadras.org/upcoming-events/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    print(f"Fetching {url}...")
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=headers, follow_redirects=True)
            print(f"Status Code: {response.status_code}")
            print(f"Content Length: {len(response.text)}")
            
            with open("scratch/ieee_madras_upcoming.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved to scratch/ieee_madras_upcoming.html")
    except Exception as e:
        print(f"Error fetching: {e}")

if __name__ == "__main__":
    asyncio.run(main())
