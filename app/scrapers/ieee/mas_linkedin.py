import httpx
import json
import re
from datetime import datetime
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from loguru import logger

class IeeeMasLinkedinScraper(BaseScraper):
    @property
    def source_name(self) -> str:
        return "ieee_mas_linkedin"

    @property
    def start_url(self) -> str:
        return "https://in.linkedin.com/company/ieeemas"

    def _extract_ext_link(self, text: str) -> str:
        # Simple regex to extract first link inside post body text
        urls = re.findall(r'(https?://\S+)', text)
        if urls:
            return urls[0].strip()
        return None

    def _parse_jsonld(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        results = []
        scripts = soup.find_all("script", type="application/ld+json")
        
        for script in scripts:
            if not script.string:
                continue
            try:
                data = json.loads(script.string.strip())
                graph = []
                if isinstance(data, dict):
                    if "@graph" in data:
                        graph = data["@graph"]
                    else:
                        graph = [data]
                elif isinstance(data, list):
                    graph = data
                    
                for item in graph:
                    if item.get("@type") == "DiscussionForumPosting":
                        post_text = item.get("text", "").strip()
                        if not post_text:
                            continue
                            
                        post_url = item.get("url", item.get("mainEntityOfPage"))
                        if isinstance(post_url, dict):
                            post_url = post_url.get("@id", "")
                            
                        # Clean query parameters
                        if post_url:
                            post_url = post_url.split("?")[0].strip()
                            
                        ext_url = self._extract_ext_link(post_text)
                        source_url = ext_url if ext_url else post_url
                        
                        clean_title = post_text.replace("\n", " ").strip()
                        if len(clean_title) > 60:
                            clean_title = clean_title[:57] + "..."
                            
                        results.append({
                            "title": f"IEEE MAS Update: {clean_title}",
                            "source_url": source_url,
                            "source_name": self.source_name,
                            "organization": "IEEE Madras Section",
                            "category": "Announcement",
                            "description": post_text,
                            "event_start": None,
                            "event_end": None,
                            "deadline": None
                        })
            except Exception as e:
                logger.error(f"MAS LinkedIn JSON-LD parsing exception: {e}")
                
        return results

    def _parse_dom(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        results = []
        overlay_links = soup.find_all("a", class_=lambda c: c and "main-feed-card__overlay-link" in c)
        
        for overlay in overlay_links:
            post_url = overlay.get("href")
            if not post_url:
                continue
                
            post_url = post_url.split("?")[0].strip()
            card = overlay.find_parent("li")
            if not card:
                card = overlay.find_parent("div")
            if not card:
                continue
                
            paragraphs = card.find_all("p")
            post_text = ""
            for p in paragraphs:
                p_text = p.get_text(strip=True)
                if p_text and "followers" not in p_text.lower():
                    post_text = p_text
                    break
            
            if not post_text:
                post_text = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
            if not post_text:
                continue
                
            ext_url = None
            for link in card.find_all("a", href=True):
                href = link["href"]
                if any(x in href.lower() for x in ["company/ieeemas", "cold-join", "login", "signup", "social-actions"]):
                    continue
                if any(domain in href.lower() for domain in ["bit.ly", "lnkd.in", "youtube.com", "youtu.be", "ieeemas", "ieee.org"]):
                    ext_url = href
                    break
                    
            source_url = ext_url if ext_url else post_url
            
            clean_title = post_text.replace("\n", " ").strip()
            if len(clean_title) > 60:
                clean_title = clean_title[:57] + "..."
                
            results.append({
                "title": f"IEEE MAS Update: {clean_title}",
                "source_url": source_url,
                "source_name": self.source_name,
                "organization": "IEEE Madras Section",
                "category": "Announcement",
                "description": post_text,
                "event_start": None,
                "event_end": None,
                "deadline": None
            })
            
        return results

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        # Method 1: Try structured SEO JSON-LD extraction
        results = self._parse_jsonld(soup)
        
        # Method 2: Fallback to HTML DOM parsing if JSON-LD was empty
        if not results:
            logger.info("MAS LinkedIn: No posts in JSON-LD. Falling back to HTML DOM selectors.")
            results = self._parse_dom(soup)
            
        logger.info(f"MAS LinkedIn Scraper parsed {len(results)} updates successfully.")
        return results
