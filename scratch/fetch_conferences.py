import asyncio
import httpx

async def main():
    url = "https://www.computer.org/conferences/calendar"
    params = {
        "queryState": '{"country":"India","numPages":1}'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    print(f"Fetching {url} with params {params} using HTTPX...")
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params, headers=headers, follow_redirects=True)
            print(f"Status Code: {response.status_code}")
            print(f"Content Length: {len(response.text)}")
            
            # Save snippet of response
            with open("scratch/conferences_fetch_result.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Saved to scratch/conferences_fetch_result.html")
    except Exception as e:
        print(f"Error fetching: {e}")

if __name__ == "__main__":
    asyncio.run(main())
