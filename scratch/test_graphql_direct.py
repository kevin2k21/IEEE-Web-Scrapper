import asyncio
import httpx
import json

async def main():
    url = "https://www.computer.org/api/archon/v1/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.computer.org",
        "Referer": "https://www.computer.org/conferences/calendar?queryState=%7B%22country%22:%22India%22,%22numPages%22:1%7D",
    }
    
    query = """query ($pageNumber: Int, $sortBy: String, $city: String, $country: String, $keywordSearch: String, $startDate: String, $attendanceType: String, $eventType: String, $techCommunity: String) {
      events: events(
        keywordSearch: $keywordSearch
        startDate: $startDate
        pageNumber: $pageNumber
        sortBy: $sortBy
        country: $country
        city: $city
        attendanceType: $attendanceType
        eventType: $eventType
        techCommunity: $techCommunity
        excludeCpsSponsoredEvents: true
      ) {
        id
        pageSize
        page
        numPages
        results {
          id
          title
          startDate
          endDate
          eventType
          source
          attendanceType
          descriptionHtml
          address {
            city
            country
          }
          websiteUrl
          callToAction {
            destinationUrl
          }
        }
      }
    }"""
    
    payload = {
        "variables": {
            "keywordSearch": "",
            "startDate": "2026-05-24",
            "pageNumber": 1,
            "sortBy": "date_asc",
            "techCommunity": None,
            "eventType": None,
            "country": "India",
            "city": None,
            "attendanceType": "all"
        },
        "query": query
    }
    
    print(f"Making POST request to {url} ...")
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        events = data.get("data", {}).get("events", {}).get("results", [])
        print(f"Total events returned: {len(events)}")
        
        for i, ev in enumerate(events[:5]):
            print(f"\nEvent {i+1}:")
            print(f" - Title: {ev.get('title')}")
            print(f" - Date: {ev.get('startDate')} to {ev.get('endDate')}")
            print(f" - Type: {ev.get('eventType')}")
            print(f" - City: {ev.get('address', {}).get('city')}, {ev.get('address', {}).get('country')}")
            print(f" - Website: {ev.get('websiteUrl') or (ev.get('callToAction') or {}).get('destinationUrl')}")

if __name__ == "__main__":
    asyncio.run(main())
