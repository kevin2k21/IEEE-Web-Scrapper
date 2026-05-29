import httpx
from bs4 import BeautifulSoup
import re

urls = {
    "summit_2026": "https://sac.ieeer10.org/ieee-region-10-student-summit-2026/",
    "revival_fund": "https://sac.ieeer10.org/ieee-r10-section-student-branch-revival-fund-2025/",
    "sb_award": "https://sac.ieeer10.org/osb-award/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for name, url in urls.items():
    print(f"\n========================================\nURL: {url}")
    try:
        res = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Print text of all list items and paragraphs that look like deadlines or dates
        print("--- Paragraphs ---")
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if any(k in text.lower() for k in ["deadline", "date", "close", "timeline", "fund", "submission"]):
                print(f" - P: {text}")
                
        print("--- List Items ---")
        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if any(k in text.lower() for k in ["deadline", "date", "close", "timeline", "submission", "202"]):
                print(f" - LI: {text[:150]}")
                
        print("--- Tables ---")
        for tab in soup.find_all("table"):
            for tr in tab.find_all("tr"):
                print(f" - Row: {[td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]}")
                
    except Exception as e:
        print(f"Error: {e}")
