import httpx
import re
from datetime import datetime
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeCsTopEventsScraper(BaseScraper):
    """
    Scraper for IEEE Computer Society Top Events.

    This scraper navigates the top computer science events page on the IEEE CS
    website. It parses month-based DOM structures to extract upcoming
    conferences, their dates, and descriptions.
    """
    @property
    def source_name(self) -> str:
        return "ieee_cs_top_events"

    @property
    def start_url(self) -> str:
        return "https://www.computer.org/conferences/top-computer-science-events"

    def _parse_date_range(self, date_str: str, default_year: int = 2026) -> tuple:
        """
        Parses multiple date formats dynamically:
        - Single day: "18 April 2026"
        - Same month: "26-28 January 2026" or "6-10 Mar 2026"
        - Cross-month: "28 Oct - 1 Nov 2026"
        - Year omitted: "12-18 April" -> Appends default_year (2026)
        """
        # Clean spacing and hyphens/dashes
        date_str = re.sub(r'\s+', ' ', date_str.replace('–', '-').replace('—', '-')).strip()
        
        # Fallback if year is omitted in HTML text (e.g., "12-18 April")
        if not re.search(r'\d{4}$', date_str):
            date_str = f"{date_str} {default_year}"

        # 1. Single day (e.g., "18 April 2026")
        single_day_match = re.match(r'^(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
        if single_day_match:
            day, month, yr = single_day_match.groups()
            for fmt in ("%d %B %Y", "%d %b %Y"):
                try:
                    dt = datetime.strptime(f"{day} {month} {yr}", fmt)
                    return dt, dt
                except ValueError:
                    pass

        # 2. Same-month range (e.g., "26-28 January 2026" or "6-10 Mar 2026")
        range_match = re.match(r'^(\d+)\s*-\s*(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
        if range_match:
            start_day, end_day, month, yr = range_match.groups()
            for fmt in ("%d %B %Y", "%d %b %Y"):
                try:
                    start_dt = datetime.strptime(f"{start_day} {month} {yr}", fmt)
                    end_dt = datetime.strptime(f"{end_day} {month} {yr}", fmt)
                    return start_dt, end_dt
                except ValueError:
                    pass

        # 3. Cross-month range (e.g., "28 Oct - 1 Nov 2026")
        cross_range_match = re.match(r'^(\d+)\s+([A-Za-z]+)\s*-\s*(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
        if cross_range_match:
            start_day, start_month, end_day, end_month, yr = cross_range_match.groups()
            for fmt in ("%d %B %Y", "%d %b %Y"):
                try:
                    start_dt = datetime.strptime(f"{start_day} {start_month} {yr}", fmt)
                    end_dt = datetime.strptime(f"{end_day} {end_month} {yr}", fmt)
                    return start_dt, end_dt
                except ValueError:
                    pass

        return None, None

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # 12 months identifiers used in target DOM anchors
        months = [
            "january", "feb", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]
        
        for month_id in months:
            # Find the month anchor
            month_anchor = soup.find(id=month_id)
            if not month_anchor:
                continue
                
            # Locate parent container
            parent_container = month_anchor.find_parent("div", class_="relative")
            if not parent_container:
                continue
                
            # Locate container enclosing the listings
            content_div = parent_container.find("div", class_="column-content")
            if not content_div:
                continue
                
            # Find all style-h3 headings (each represents one conference listing)
            h3s = content_div.find_all("h3", class_="style-h3")
            for h3 in h3s:
                a = h3.find("a")
                if not a:
                    continue
                    
                title = a.get_text(strip=True)
                href = a.get("href")
                
                # Fetch metadata paragraph (usually the immediate sibling)
                date_p = h3.find_next_sibling("p")
                date_span = date_p.find("span", class_="font-medium") if date_p else None
                
                date_str = ""
                location = ""
                start_dt, end_dt = None, None
                
                if date_span:
                    meta_text = date_span.get_text(strip=True)
                    if "|" in meta_text:
                        date_str, location = [x.strip() for x in meta_text.split("|", 1)]
                    else:
                        date_str = meta_text
                    
                    # Parse start & end dates
                    start_dt, end_dt = self._parse_date_range(date_str)
                    
                # Fetch description paragraph
                desc_p = date_p.find_next_sibling("p") if date_p else None
                description = desc_p.get_text(strip=True) if desc_p else ""
                
                if not description:
                    description = f"Please visit the conference page for details regarding {title}."
                
                if title and href:
                    results.append({
                        "title": title,
                        "source_url": href,
                        "source_name": self.source_name,
                        "organization": "IEEE Computer Society" + (f" ({location})" if location else ""),
                        "category": "Conference",
                        "description": description,
                        "event_start": start_dt,
                        "event_end": end_dt,
                        "deadline": None
                    })
                    
        logger.info(f"Top Events Scraper parsed {len(results)} conferences successfully.")
        return results
