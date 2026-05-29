from bs4 import BeautifulSoup
import re
from datetime import datetime

def parse_date(date_str):
    if not date_str:
        return None
    # Parse format like "14 October 2023"
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            pass
    return None

def main():
    print("Testing parser on IEEE Madras homepage...")
    with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    # 1. Parse Announcements list
    ann_section = soup.find("section", class_="announcements")
    if ann_section:
        print("\nParsing Announcements...")
        for li in ann_section.find_all("li"):
            a = li.find("a")
            if not a:
                continue
            title = a.get_text(strip=True)
            # Remove leading "> " if any
            if title.startswith(">"):
                title = title[1:].strip()
            href = a.get("href")
            
            # Extract date if mentioned in the title (e.g. "- 11 April 2026")
            event_date = None
            date_match = re.search(r'-\s*(\d+\s+[A-Za-z]+\s+\d{4})', title)
            if date_match:
                event_date = parse_date(date_match.group(1))
                
            results.append({
                "title": title,
                "url": href,
                "type": "Announcement",
                "date": event_date,
                "description": f"Official IEEE Madras Section announcement: '{title}'."
            })
            
    # 2. Parse News & Events section
    news_section = soup.find("section", class_="news")
    if news_section:
        print("\nParsing News & Events...")
        
        # Featured news
        feat = news_section.find("div", class_="featured-news")
        if feat:
            a = feat.find("h3").find("a") if feat.find("h3") else None
            date_span = feat.find("span", class_="date")
            date_str = re.sub(r'<[^>]*>', '', date_span.get_text()).strip() if date_span else ""
            if a:
                title = a.get_text(strip=True)
                href = a.get("href")
                results.append({
                    "title": title,
                    "url": href,
                    "type": "News & Event",
                    "date": parse_date(date_str),
                    "description": f"Featured IEEE Madras event/news: '{title}'."
                })
                
        # Sidebar news items
        for item in news_section.find_all("div", class_="news-item"):
            a = item.find("h4").find("a") if item.find("h4") else None
            date_span = item.find("span", class_="date")
            date_str = re.sub(r'<[^>]*>', '', date_span.get_text()).strip() if date_span else ""
            if a:
                title = a.get_text(strip=True)
                href = a.get("href")
                results.append({
                    "title": title,
                    "url": href,
                    "type": "News & Event",
                    "date": parse_date(date_str),
                    "description": f"IEEE Madras Section event/news: '{title}'."
                })
                
    print(f"\nSuccessfully parsed {len(results)} items from IEEE Madras Section:")
    for i, res in enumerate(results):
        print(f"\nItem {i+1}:")
        print(f" - Title: {res['title']}")
        print(f" - Type: {res['type']}")
        print(f" - Date: {res['date']}")
        print(f" - URL: {res['url']}")
        print(f" - Desc: {res['description']}")

if __name__ == "__main__":
    main()
