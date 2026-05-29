from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper

class IeeeStudentsScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "IEEE Students"

    @property
    def start_url(self) -> str:
        return "https://students.ieee.org/student-opportunities/"

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Build category map from the filter checkboxes
        category_map = {}
        for label in soup.find_all('label', class_='form-check-label'):
            cat_id = label.get('for')
            if cat_id and cat_id.startswith('cat-'):
                category_map[cat_id] = label.get_text(strip=True)
        
        # On this site, opportunities are stored in <p> tags with class "sub-cat"
        for p_tag in soup.find_all("p", class_="sub-cat"):
            a_tag = p_tag.find("a")
            if not a_tag:
                continue
                
            cat_id = p_tag.get("data-sub_cat_id")
            category_name = category_map.get(cat_id, "Scholarship/Award")
                
            title = a_tag.get_text(strip=True)
            url = a_tag.get("href")
            
            if title and url:
                if not url.startswith("http"):
                    url = "https://students.ieee.org" + url
                    
                results.append({
                    "title": title,
                    "source_url": url,
                    "source_name": self.source_name,
                    "organization": "IEEE Students",
                    "category": category_name,
                    "description": f"Please visit the official website for details regarding this {category_name.lower()}.",
                })
                
        return results
