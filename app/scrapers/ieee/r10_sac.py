import httpx
import re
from datetime import datetime
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeR10SacScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_r10_sac"

    @property
    def start_url(self) -> str:
        return "https://sac.ieeer10.org/"

    def _clean_date_str(self, date_str: str) -> str:
        # Remove ordinal suffixes: st, nd, rd, th (case insensitive)
        # E.g., "31st October 2025" -> "31 October 2025"
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str, flags=re.IGNORECASE)
        # Replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', date_str).strip()

    def _parse_single_date(self, date_str: str, default_year: int = 2026) -> datetime:
        cleaned = self._clean_date_str(date_str)
        if not cleaned:
            return None
            
        # If no year is present, append the default_year
        if not re.search(r'\d{4}$', cleaned):
            cleaned = f"{cleaned} {default_year}"
            
        for fmt in ("%d %B %Y", "%d %b %Y", "%B %d %Y", "%b %d %Y"):
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                pass
        return None

    def _extract_deadline(self, soup: BeautifulSoup) -> datetime:
        # Look for list items or paragraphs containing "deadline"
        # Example format: "Nomination Deadline:31 May 2026" or "Submissions Deadline:31st October 2025"
        deadline_dt = None
        
        # 1. Search in list items
        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if "deadline" in text.lower():
                parts = text.split(":", 1)
                date_candidate = parts[1].strip() if len(parts) > 1 else text
                date_candidate = re.sub(r'\(.*?\)', '', date_candidate).strip()
                
                dt = self._parse_single_date(date_candidate)
                if dt:
                    deadline_dt = dt
                    break
                    
        # 2. Search in paragraphs as fallback
        if not deadline_dt:
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if "deadline" in text.lower() and ":" in text:
                    parts = text.split(":", 1)
                    date_candidate = re.sub(r'\(.*?\)', '', parts[1]).strip()
                    dt = self._parse_single_date(date_candidate)
                    if dt:
                        deadline_dt = dt
                        break
                        
        return deadline_dt

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        homepage_html = response.text
        soup = BeautifulSoup(homepage_html, "html.parser")
        results = []
        
        # Core dynamic discovery URLs
        discovered_urls = set()
        
        # Crawl homepage for subpage links matching R10 SAC Opportunities
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Filter relevant WordPress post paths
            if any(k in href for k in ["/ieee-region-10-student-summit-", "/ieee-r10-", "/osb-award/", "/outstanding-sb-award/"]):
                discovered_urls.add(href)
                
        # Robust fallback: ensure our verified high-value pages are crawled even if navigation shifts
        fallbacks = [
            "https://sac.ieeer10.org/ieee-region-10-student-summit-2026/",
            "https://sac.ieeer10.org/ieee-r10-section-student-branch-revival-fund-2025/",
            "https://sac.ieeer10.org/osb-award/"
        ]
        for url in fallbacks:
            discovered_urls.add(url)
            
        logger.info(f"R10 SAC Scraper: Crawling {len(discovered_urls)} subpages...")
        
        for sub_url in discovered_urls:
            try:
                # Fetch child page
                sub_res = await self.fetch(sub_url, follow_redirects=True)
                sub_soup = BeautifulSoup(sub_res.text, "html.parser")
                
                # Extract clean page title
                title_elem = sub_soup.find("title")
                title = title_elem.get_text(strip=True).split("–")[0].strip() if title_elem else "IEEE R10 Opportunity"
                
                # Ignore generic placeholder titles if any
                if "No Title" in title or "Page not found" in title:
                    continue
                    
                # Determine category based on keywords
                category = "Announcement"
                if "award" in title.lower():
                    category = "Award"
                elif "fund" in title.lower():
                    category = "Grant"
                elif "summit" in title.lower():
                    category = "Conference"
                    
                # Extract description paragraphs (join first 2 meaningful ones)
                paragraphs = [p.get_text(strip=True) for p in sub_soup.find_all("p") if p.get_text(strip=True)]
                good_paragraphs = [
                    p for p in paragraphs 
                    if len(p) > 50 
                    and not p.startswith("Events") 
                    and not p.startswith("Funding")
                    and not p.startswith("Our Team")
                ]
                
                description = ""
                if good_paragraphs:
                    description = " ".join(good_paragraphs[:2])
                if not description:
                    description = f"Official IEEE Region 10 Student Activities Committee opportunity: '{title}'. Please visit the website for eligibility and registration guidelines."
                    
                # Extract deadline date
                deadline = self._extract_deadline(sub_soup)
                
                results.append({
                    "title": title,
                    "source_url": sub_url,
                    "source_name": self.source_name,
                    "organization": "IEEE Region 10 SAC",
                    "category": category,
                    "description": description,
                    "event_start": None,
                    "event_end": None,
                    "deadline": deadline
                })
                
            except Exception as e:
                logger.error(f"R10 SAC Scraper: Error crawling subpage {sub_url}: {e}")
                
        logger.info(f"R10 SAC Scraper parsed {len(results)} opportunities successfully.")
        return results
