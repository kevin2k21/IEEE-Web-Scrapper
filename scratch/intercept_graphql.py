import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.computer.org/conferences/calendar?queryState=%7B%22country%22:%22India%22,%22numPages%22:1%7D"
    print(f"Launching browser to capture GraphQL query details...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        async def handle_request(request):
            if "graphql" in request.url:
                print(f"\n[GRAPHQL POST REQUEST DETECTED]")
                print(f"URL: {request.url}")
                print(f"Method: {request.method}")
                print(f"Headers: {request.headers}")
                try:
                    post_data = request.post_data
                    print(f"POST Body: {post_data}")
                except Exception as e:
                    print(f"Could not read body: {e}")
                    
        async def handle_response(response):
            if "graphql" in response.url:
                print(f"\n[GRAPHQL RESPONSE DETECTED]")
                try:
                    body = await response.text()
                    print(f"Response Body (truncated): {body[:2000]}")
                except Exception as e:
                    print(f"Could not read response: {e}")
                    
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        print("Navigating...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
