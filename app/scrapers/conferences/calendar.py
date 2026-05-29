import httpx
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.parse import urlparse, parse_qs
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeCsCalendarScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_cs_calendar"

    @property
    def start_url(self) -> str:
        # Default starting URL with queryState filtering for India
        return "https://www.computer.org/conferences/calendar?queryState=%7B%22country%22:%22India%22,%22numPages%22:1%7D"

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        # Parse queryState directly from the response URL (or fallback to default)
        url_str = str(response.url)
        parsed_url = urlparse(url_str)
        query_params = parse_qs(parsed_url.query)
        
        query_state_str = query_params.get("queryState", [""])[0]
        query_state = {}
        if query_state_str:
            try:
                query_state = json.loads(query_state_str)
                logger.info(f"Parsed calendar queryState: {query_state}")
            except Exception as e:
                logger.error(f"Error parsing queryState JSON: {e}")
                
        # Extract individual filter parameters with standard defaults
        country = query_state.get("country", None)
        num_pages = query_state.get("numPages", 1)
        tech_community = query_state.get("techCommunity", None)
        event_type = query_state.get("eventType", None)
        city = query_state.get("city", None)
        attendance_type = query_state.get("attendanceType", "all")
        keyword_search = query_state.get("keywordSearch", "")
        start_date = query_state.get("startDate", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        sort_by = query_state.get("sortBy", "date_asc")
        
        results = []
        graphql_url = "https://www.computer.org/api/archon/v1/graphql"
        
        # Build standard browser-like headers to prevent CloudFront blocking
        post_headers = {
            "User-Agent": self.headers.get("User-Agent", "Mozilla/5.0"),
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.computer.org",
            "Referer": url_str,
        }
        
        graphql_query = """query ($pageNumber: Int, $sortBy: String, $city: String, $country: String, $keywordSearch: String, $startDate: String, $attendanceType: String, $eventType: String, $techCommunity: String) {
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
              dateTimeType
              startDate
              endDate
              eventType
              source
              attendanceType
              descriptionHtml
              address {
                city
                region
                country
              }
              websiteUrl
              callToAction {
                destinationUrl
              }
            }
          }
        }"""
        
        # Sequentially fetch pages up to num_pages
        async with httpx.AsyncClient(headers=post_headers, timeout=self.timeout) as client:
            for page in range(1, num_pages + 1):
                logger.info(f"Fetching conference calendar page {page} of {num_pages}...")
                
                payload = {
                    "variables": {
                        "keywordSearch": keyword_search,
                        "startDate": start_date,
                        "pageNumber": page,
                        "sortBy": sort_by,
                        "techCommunity": tech_community,
                        "eventType": event_type,
                        "country": country,
                        "city": city,
                        "attendanceType": attendance_type
                    },
                    "query": graphql_query
                }
                
                try:
                    res = await client.post(graphql_url, json=payload)
                    res.raise_for_status()
                    
                    data = res.json()
                    events = data.get("data", {}).get("events", {}).get("results", [])
                    logger.info(f"Page {page} returned {len(events)} events.")
                    
                    for ev in events:
                        title = ev.get("title")
                        if not title:
                            continue
                            
                        # Format source URL (defaulting to websiteUrl or destinationUrl)
                        source_url = ev.get("websiteUrl")
                        if not source_url and ev.get("callToAction"):
                            source_url = ev.get("callToAction", {}).get("destinationUrl")
                        if not source_url:
                            # Fallback if no specific website is provided
                            source_url = url_str
                            
                        # Parse start and end dates
                        start_str = ev.get("startDate")
                        end_str = ev.get("endDate")
                        
                        start_dt = None
                        end_dt = None
                        
                        if start_str:
                            try:
                                start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                            except ValueError:
                                pass
                        if end_str:
                            try:
                                end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
                            except ValueError:
                                pass
                                
                        # Extract and format clean description
                        desc_html = ev.get("descriptionHtml", "")
                        description = ""
                        if desc_html:
                            # Simple HTML tag stripping
                            description = re.sub(r'<[^>]*>', '', desc_html).strip()
                            
                        if not description:
                            description = f"Please visit the official website for details regarding this event."
                            
                        # Concatenate location/address details
                        addr = ev.get("address", {})
                        location_parts = []
                        if addr:
                            if addr.get("city"):
                                location_parts.append(addr.get("city"))
                            if addr.get("region"):
                                location_parts.append(addr.get("region"))
                            if addr.get("country"):
                                location_parts.append(addr.get("country"))
                        location_str = ", ".join(location_parts) if location_parts else "India"
                        
                        results.append({
                            "title": title,
                            "source_url": source_url,
                            "source_name": self.source_name,
                            "organization": f"IEEE CS ({location_str})" if location_str else "IEEE Computer Society",
                            "category": "Conference",
                            "description": description,
                            "event_start": start_dt,
                            "event_end": end_dt,
                            "deadline": None # No deadline exists for general calendar events
                        })
                except Exception as e:
                    logger.error(f"Error fetching calendar page {page}: {e}")
                    
        return results
