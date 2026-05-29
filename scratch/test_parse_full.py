import asyncio
import sys
import os
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.scrapers.ieee_cs.cfp import IeeeCsCfpScraper

class MockResponse:
    def __init__(self, text):
        self.text = text

async def main():
    print("Testing parser with saved HTML...")
    with open("scratch/ieee_cs_fetch_result.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    mock_resp = MockResponse(html)
    scraper = IeeeCsCfpScraper()
    
    # We will override parse for testing if needed, but let's test the real one.
    results = await scraper.parse(mock_resp)
    print(f"Total active results parsed: {len(results)}")
    
    for i, res in enumerate(results[:5]):
        print(f"\nResult {i+1}:")
        print(f" - Title: {res['title']}")
        print(f" - Org: {res['organization']}")
        print(f" - Category: {res['category']}")
        print(f" - URL: {res['source_url']}")
        print(f" - Deadline: {res['deadline']}")
        print(f" - Description snippet: {res['description'][:150]}...")

if __name__ == "__main__":
    asyncio.run(main())
