from app.scrapers.base import BaseScraper
from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
import re
from datetime import datetime

class IeeeMadrasScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_madras"

    @property
    def start_url(self) -> str:
        return "https://ieeemadras.org/"

    def _parse_date(self, date_str: str) -> Any:
        if not date_str:
            return None
        # Parse format like "14 October 2023", "03 August 2023", "29 July 2023"
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                pass
        return None

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # 1. Parse Events & Announcements List Section
        ann_section = soup.find("section", class_="announcements")
        if ann_section:
            for li in ann_section.find_all("li"):
                a = li.find("a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                # Remove leading bullet characters if present
                if title.startswith(">"):
                    title = title[1:].strip()
                href = a.get("href")
                
                # Extract event date dynamically from title if present (e.g. "- 11 April 2026")
                event_date = None
                date_match = re.search(r'-\s*(\d+\s+[A-Za-z]+\s+\d{4})', title)
                if date_match:
                    event_date = self._parse_date(date_match.group(1))
                    
                if title and href:
                    results.append({
                        "title": title,
                        "source_url": href,
                        "source_name": self.source_name,
                        "organization": "IEEE Madras Section",
                        "category": "Announcement",
                        "description": f"Official IEEE Madras Section announcement: '{title}'. Please visit the link for complete details and registration.",
                        "event_start": event_date,
                        "event_end": None,
                        "deadline": None
                    })
                    
        # 2. Parse News & Events Block Section
        news_section = soup.find("section", class_="news")
        if news_section:
            # Featured News
            feat = news_section.find("div", class_="featured-news")
            if feat:
                a = feat.find("h3").find("a") if feat.find("h3") else None
                date_span = feat.find("span", class_="date")
                date_str = re.sub(r'<[^>]*>', '', date_span.get_text()).strip() if date_span else ""
                
                if a and a.get("href"):
                    title = a.get_text(strip=True)
                    href = a.get("href")
                    event_date = self._parse_date(date_str)
                    
                    results.append({
                        "title": title,
                        "source_url": href,
                        "source_name": self.source_name,
                        "organization": "IEEE Madras Section",
                        "category": "News & Event",
                        "description": f"Featured IEEE Madras event/news: '{title}'. Please visit the link for full highlights and coverage.",
                        "event_start": event_date,
                        "event_end": None,
                        "deadline": None
                    })
                    
            # Sidebar News Items
            for item in news_section.find_all("div", class_="news-item"):
                a = item.find("h4").find("a") if item.find("h4") else None
                date_span = item.find("span", class_="date")
                date_str = re.sub(r'<[^>]*>', '', date_span.get_text()).strip() if date_span else ""
                
                if a and a.get("href"):
                    title = a.get_text(strip=True)
                    href = a.get("href")
                    event_date = self._parse_date(date_str)
                    
                    results.append({
                        "title": title,
                        "source_url": href,
                        "source_name": self.source_name,
                        "organization": "IEEE Madras Section",
                        "category": "News & Event",
                        "description": f"IEEE Madras Section event/news: '{title}'. Please visit the link for complete details and coverage.",
                        "event_start": event_date,
                        "event_end": None,
                        "deadline": None
                    })
                    
        return results
