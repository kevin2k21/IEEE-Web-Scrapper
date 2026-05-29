import httpx
from bs4 import BeautifulSoup
from typing import Any, Dict, List
import re
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeCsLinkedinScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_cs_linkedin"

    @property
    def start_url(self) -> str:
        return "https://www.linkedin.com/company/ieee-computer-society?trk=similar-pages"

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # Locate all overlay links that point to individual feed posts
        overlay_links = soup.find_all("a", class_=lambda c: c and "main-feed-card__overlay-link" in c)
        logger.info(f"LinkedIn Scraper: Found {len(overlay_links)} post cards in guest feed HTML.")
        
        for overlay in overlay_links:
            post_url = overlay.get("href")
            if not post_url:
                continue
                
            # Strip query params from post URL
            post_url = post_url.split("?")[0].strip()
            
            # Find the parent card element
            card = overlay.find_parent("li")
            if not card:
                card = overlay.find_parent("div")
            if not card:
                continue
                
            # Extract post content text from paragraphs
            paragraphs = card.find_all("p")
            post_text = ""
            for p in paragraphs:
                p_text = p.get_text(strip=True)
                # Ignore metadata paragraphs like follower counts
                if p_text and "followers" not in p_text.lower():
                    post_text = p_text
                    break
            
            if not post_text:
                # Fallback: join all non-empty paragraphs
                post_text = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
            if not post_text:
                continue
                
            # Find any external destination links (bit.ly, lnkd.in, youtube, etc.)
            ext_url = None
            for link in card.find_all("a", href=True):
                href = link["href"]
                # Skip main actor company links, tracking links or social action redirects
                if any(x in href.lower() for x in ["company/ieee-computer-society", "cold-join", "login", "signup", "social-actions"]):
                    continue
                if any(domain in href.lower() for domain in ["bit.ly", "lnkd.in", "youtube.com", "youtu.be", "computer.org", "ieee.org", "bit.ly"]):
                    ext_url = href
                    break
                    
            # Use external URL if discovered, otherwise fallback to the LinkedIn post URL
            source_url = ext_url if ext_url else post_url
            
            # Create standard opportunity title
            clean_title = post_text.replace("\n", " ").strip()
            if len(clean_title) > 60:
                clean_title = clean_title[:57] + "..."
            
            results.append({
                "title": f"IEEE CS Update: {clean_title}",
                "source_url": source_url,
                "source_name": self.source_name,
                "organization": "IEEE Computer Society",
                "category": "Announcement",
                "description": post_text,
                "event_start": None,
                "event_end": None,
                "deadline": None
            })
            
        logger.info(f"LinkedIn Scraper parsed {len(results)} updates successfully.")
        return results
