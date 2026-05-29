import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://www.computer.org/conferences/calendar?queryState=%7B%22country%22:%22India%22,%22numPages%22:1%7D"
    print(f"Launching browser to intercept requests for: {url}")
    
    async with async_playwright() as p:
        # Launch browser headlessly
        browser = await p.chromium.launch(headless=True)
        # Create a new context
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Define a request/response interceptor
        requests_logged = []
        
        def handle_request(request):
            # Log any requests to endpoints containing api or json or custom path
            req_url = request.url
            if "wpcms" in req_url or "api" in req_url or "queryState" in req_url or "json" in req_url or "admin-ajax" in req_url:
                requests_logged.append(f"Request: {request.method} {req_url}")
                
        async def handle_response(response):
            resp_url = response.url
            # Log if it returns JSON
            try:
                content_type = response.headers.get("content-type", "")
                if "json" in content_type or "application/json" in content_type:
                    body = await response.text()
                    print(f"\n[INTERCEPTED JSON RESPONSE]")
                    print(f"URL: {resp_url}")
                    print(f"Status: {response.status}")
                    print(f"Content Type: {content_type}")
                    print(f"Body preview: {body[:800]}...")
            except Exception as e:
                pass
                
        page.on("request", handle_request)
        page.on("response", handle_response)
        
        # Navigate to URL
        print("Navigating...")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        print("\nAll logged requests:")
        for r in requests_logged:
            print(f" - {r}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
