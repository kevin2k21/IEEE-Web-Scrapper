from app.scrapers.base import BaseScraper
from typing import Any, Dict, List
import httpx
import re
from datetime import datetime

class IeeeCsCfpScraper(BaseScraper):
    """
    Scraper for IEEE Computer Society Calls for Papers.

    This scraper extracts data from the IEEE CS CFP page which uses a Next.js
    architecture. It parses the JSON payload embedded in the HTML stream to
    extract journals, magazines, and conferences accepting submissions,
    along with their deadlines.
    """
    @property
    def source_name(self) -> str:
        return "ieee_cs_cfp"

    @property
    def start_url(self) -> str:
        return "https://www.computer.org/publications/author-resources/calls-for-papers"

    async def parse(self, response: httpx.Response) -> List[Dict[str, Any]]:
        html = response.text
        
        # 1. Extract all self.__next_f.push payloads
        pattern = r'self\.__next_f\.push\(\[1,\"(.*?)\"\]\)'
        matches = re.findall(pattern, html)
        
        full_stream = ""
        for m in matches:
            full_stream += m.replace('\\"', '"').replace('\\\\', '\\')
            
        # 2. Build a lookup dictionary of references to texts (Next.js stream references)
        ref_matches = list(re.finditer(r'(\d+):T([A-Za-z0-9]+),', full_stream))
        ref_map = {}
        for i in range(len(ref_matches)):
            m = ref_matches[i]
            ref_id = m.group(1)
            start_pos = m.end()
            end_pos = ref_matches[i+1].start() if i + 1 < len(ref_matches) else len(full_stream)
            ref_map[ref_id] = full_stream[start_pos:end_pos].strip()
            
        # 3. Parse all CFP Cards from the stream
        card_parts = full_stream.split('{"aria-label":"Call For Paper Card"')
        results = []
        
        for part in card_parts[1:]:
            # Extract Type and Publication (Journal, Magazine, Conference)
            pub_match = re.search(r'\"children\":\[\s*\" \",\s*\"(Magazine|Journal|Conference)\",\s*\" \",\s*\"-\s*(.*?)\",\s*\" \"\s*\]', part)
            if not pub_match:
                pub_match = re.search(r'\"children\":\[\s*\" \",\s*\"(Magazine|Journal|Conference)\",\s*\" \",\s*\"(.*?)\",\s*\" \"\s*\]', part)
                
            card_type = pub_match.group(1) if pub_match else "Journal/Magazine"
            pub_name = pub_match.group(2).strip() if pub_match else "IEEE Computer Society"
            
            # Clean up escape characters in publication name (e.g. \u0026 -> &)
            pub_name = pub_name.replace('\\u0026', '&').replace('\\"', '"')
            
            # Extract Title and Href URL
            link_match = re.search(r'\"href\":\"(.*?)\",\"className\":\".*?\",\"prefetch\":(?:true|false),\"children\":\"(.*?)\"', part)
            if not link_match:
                link_match = re.search(r'\"href\":\"(.*?)\",\"className\":\".*?\",\"children\":\"(.*?)\"', part)
                
            href = link_match.group(1) if link_match else ""
            title = link_match.group(2) if link_match else ""
            
            # Skip if it is marked as CLOSED
            if title.upper().startswith("CLOSED:"):
                continue
                
            # Extract Description Reference Key and resolve its value
            desc_match = re.search(r'\"className\":\"style-p line-clamp-3\",\"children\":\"\$(\d+)\"', part)
            desc_ref = desc_match.group(1) if desc_match else None
            
            description = ""
            if desc_ref and desc_ref in ref_map:
                description = ref_map[desc_ref]
                description = re.sub(r'\\n', '\n', description)
                description = re.sub(r'\\"', '"', description)
                description = re.sub(r'\\u0026', '&', description)
                description = re.sub(r'\\u[0-9a-fA-F]{4}', '', description) # clean other unicode if any
                
            # Extract Deadline Date string
            date_match = re.search(r'\"className\":\"style-p-sm font-normal text-slate-600\",\"children\":\[\s*\" \",\s*\"Submissions Due:\s*\",\s*\"(.*?)\"\s*\]', part)
            if not date_match:
                date_match = re.search(r'\"Submissions Due:\s*\",\s*\"(.*?)\"\s*\]', part)
                
            deadline_str = date_match.group(1) if date_match else None
            
            # Parse deadline string into datetime object
            deadline_dt = None
            if deadline_str:
                clean_date = deadline_str.split(']')[0].replace('"', '').strip()
                # Parse format like "30 September 2026" or "15 July 2026"
                for fmt in ("%d %B %Y", "%d %b %Y", "%Y-%m-%d"):
                    try:
                        deadline_dt = datetime.strptime(clean_date, fmt)
                        break
                    except ValueError:
                        pass
                        
            if title and href:
                title = title.replace('\\"', '"').replace('\\\\', '\\').replace('\\u0026', '&')
                url = "https://www.computer.org" + href if not href.startswith("http") else href
                
                results.append({
                    "title": title,
                    "source_url": url,
                    "source_name": self.source_name,
                    "organization": pub_name if pub_name else "IEEE Computer Society",
                    "category": card_type,
                    "description": description if description else f"Please visit the official website for details regarding this {card_type.lower()}.",
                    "deadline": deadline_dt
                })
                
        return results
