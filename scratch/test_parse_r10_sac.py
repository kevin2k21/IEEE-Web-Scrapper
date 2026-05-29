import httpx
from bs4 import BeautifulSoup
import re
from datetime import datetime

# A helper to clean ordinals (e.g., "31st", "3th", "27th") so datetime can parse them
def clean_date_str(date_str: str) -> str:
    # Remove ordinal suffixes: st, nd, rd, th (case insensitive)
    # E.g., "31st October 2025" -> "31 October 2025"
    # E.g., "3th July" -> "3 July"
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str, flags=re.IGNORECASE)
    # Replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', date_str).strip()

def parse_single_date(date_str: str, default_year: int = 2026) -> datetime:
    cleaned = clean_date_str(date_str)
    
    # If no year is present, append the default_year
    if not re.search(r'\d{4}$', cleaned):
        cleaned = f"{cleaned} {default_year}"
        
    for fmt in ("%d %B %Y", "%d %b %Y", "%B %d %Y", "%b %d %Y"):
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            pass
    return None

def extract_deadlines(soup: BeautifulSoup) -> datetime:
    # Look for list items or paragraphs containing "deadline"
    # Example format: "Nomination Deadline:31 May 2026" or "Submissions Deadline:31st October 2025"
    deadline_dt = None
    
    # 1. Search in list items (which usually hold timelines in WordPress R10 theme)
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        # Check if the list item itself is a deadline label
        if "deadline" in text.lower():
            # Extract the date part after the colon or space
            # E.g., "Nomination Deadline:31 May 2026" -> "31 May 2026"
            parts = text.split(":", 1)
            date_candidate = parts[1].strip() if len(parts) > 1 else text
            
            # Remove notes in parentheses, e.g. "(Extended Deadline)"
            date_candidate = re.sub(r'\(.*?\)', '', date_candidate).strip()
            
            dt = parse_single_date(date_candidate)
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
                dt = parse_single_date(date_candidate)
                if dt:
                    deadline_dt = dt
                    break
                    
    return deadline_dt

def test_parse_r10():
    urls = [
        "https://sac.ieeer10.org/ieee-region-10-student-summit-2026/",
        "https://sac.ieeer10.org/ieee-r10-section-student-branch-revival-fund-2025/",
        "https://sac.ieeer10.org/osb-award/"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    for url in urls:
        print(f"\nParsing: {url}")
        res = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Get clean title
        title = soup.find("title").get_text(strip=True).split("–")[0].strip()
        print(f"Title: {title}")
        
        # Determine category and organization
        category = "Announcement"
        if "award" in title.lower():
            category = "Award"
        elif "fund" in title.lower():
            category = "Grant"
        elif "summit" in title.lower():
            category = "Conference"
            
        # Get description
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        # Filter out common short navigation/WordPress header texts
        good_paragraphs = [p for p in paragraphs if len(p) > 50 and not p.startswith("Events") and not p.startswith("Funding")]
        
        description = ""
        if good_paragraphs:
            # Join first two substantial paragraphs
            description = " ".join(good_paragraphs[:2])
        if not description:
            description = f"Official IEEE Region 10 Student Activities Committee opportunity for '{title}'."
            
        # Extract deadline
        deadline = extract_deadlines(soup)
        
        print(f"Category: {category}")
        print(f"Deadline: {deadline}")
        print(f"Description Summary: {description[:120]}...")

if __name__ == "__main__":
    test_parse_r10()
