import httpx
from bs4 import BeautifulSoup
from typing import Any, Dict, List
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeStudentContestsScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_students_contests"

    @property
    def start_url(self) -> str:
        return "https://students.ieee.org/student-opportunities/contests-for-students/"

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # Locate all evants_column divs
        columns = soup.find_all("div", class_="evants_column")
        logger.info(f"Student Contests Scraper: Found {len(columns)} contest columns in HTML.")
        
        for col in columns:
            a_title = col.find("a", class_="block_title")
            if not a_title:
                continue
                
            title = a_title.get_text(strip=True)
            href = a_title.get("href")
            
            # Parse entry details inside the WordPress columns
            entry_div = col.find("div", class_="entry")
            organizer = ""
            eligibility = ""
            desc_text = ""
            
            if entry_div:
                for p in entry_div.find_all("p"):
                    p_text = p.get_text(strip=True)
                    if ":" in p_text:
                        parts = p_text.split(":", 1)
                        key = parts[0].strip().lower()
                        val = parts[1].strip()
                        
                        if "organizer" in key:
                            organizer = val
                        elif "eligibility" in key:
                            eligibility = val
                        elif "description" in key:
                            desc_text = val
                    else:
                        # Append any extra paragraphs to description
                        desc_text += " " + p_text
                        
            # Construct a clean, unified description
            description_parts = []
            if desc_text.strip():
                description_parts.append(desc_text.strip())
            if eligibility.strip():
                description_parts.append(f"Eligibility: {eligibility.strip()}")
                
            description = " | ".join(description_parts)
            if not description.strip():
                description = f"IEEE Student Contest opportunity: '{title}'. Please visit the official link for details and entry guidelines."
                
            if title and href:
                results.append({
                    "title": title,
                    "source_url": href,
                    "source_name": self.source_name,
                    "organization": organizer if organizer else "IEEE Students",
                    "category": "Award",
                    "description": description,
                    "event_start": None,
                    "event_end": None,
                    "deadline": None
                })
                
        logger.info(f"Student Contests Scraper parsed {len(results)} contests successfully.")
        return results
