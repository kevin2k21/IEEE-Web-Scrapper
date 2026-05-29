import os
from bs4 import BeautifulSoup
import re
from datetime import datetime

def parse_date_range(date_str: str, default_year: int = 2026):
    # standard format: "26-28 January 2026", "21-25 March 2026", "6–10 Mar 2026", "18 April 2026"
    # also cross month: "28 Oct - 1 Nov 2026"
    # also missing year: "12-18 April", "18 April"
    
    # Clean the date string
    date_str = re.sub(r'\s+', ' ', date_str.replace('–', '-').replace('—', '-')).strip()
    
    # Check if a 4-digit year is present at the end. If not, append the default_year.
    if not re.search(r'\d{4}$', date_str):
        date_str = f"{date_str} {default_year}"

    # Try parsing single day: "18 April 2026"
    single_day_match = re.match(r'^(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
    if single_day_match:
        day, month, yr = single_day_match.groups()
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                dt = datetime.strptime(f"{day} {month} {yr}", fmt)
                return dt, dt
            except ValueError:
                pass

    # Try parsing same-month date range: "26-28 January 2026" or "6-10 Mar 2026"
    range_match = re.match(r'^(\d+)\s*-\s*(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
    if range_match:
        start_day, end_day, month, yr = range_match.groups()
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                start_dt = datetime.strptime(f"{start_day} {month} {yr}", fmt)
                end_dt = datetime.strptime(f"{end_day} {month} {yr}", fmt)
                return start_dt, end_dt
            except ValueError:
                pass

    # Try parsing cross-month/cross-year date range: "28 Oct - 1 Nov 2026"
    cross_range_match = re.match(r'^(\d+)\s+([A-Za-z]+)\s*-\s*(\d+)\s+([A-Za-z]+)\s+(\d{4})$', date_str)
    if cross_range_match:
        start_day, start_month, end_day, end_month, yr = cross_range_match.groups()
        for fmt in ("%d %B %Y", "%d %b %Y"):
            try:
                start_dt = datetime.strptime(f"{start_day} {start_month} {yr}", fmt)
                end_dt = datetime.strptime(f"{end_day} {end_month} {yr}", fmt)
                return start_dt, end_dt
            except ValueError:
                pass

    return None, None

def test_parse():
    file_path = "/Users/alonzoakevin/.gemini/antigravity-ide/brain/0909d623-752c-44d3-8f2d-4304c905f540/.system_generated/steps/425/content.md"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Strip frontmatter if present
    if html.startswith("Title:"):
        html = html.split("---", 1)[1]
        
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    # Months to find
    months = ["january", "feb", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    
    for month_id in months:
        # Find month container anchor
        month_anchor = soup.find(id=month_id)
        if not month_anchor:
            continue
            
        # The container is usually a sibling block containing "column-content" class
        # Let's search inside the next "div" with "container-column" or search globally for sibling hierarchy
        parent_container = month_anchor.find_parent("div", class_="relative")
        if not parent_container:
            # Fallback: search for next sibling element
            continue
            
        content_div = parent_container.find("div", class_="column-content")
        if not content_div:
            continue
            
        # Inside the column-content we have headings (h3) and paragraphs
        # Find all h3 tags (each represents a conference)
        h3s = content_div.find_all("h3", class_="style-h3")
        for h3 in h3s:
            a = h3.find("a")
            if not a:
                continue
                
            title = a.get_text(strip=True)
            href = a.get("href")
            
            # Find next elements to locate date range span and description
            # The date range is usually a paragraph containing span.font-medium
            date_p = h3.find_next_sibling("p")
            date_span = date_p.find("span", class_="font-medium") if date_p else None
            
            date_str = ""
            location = ""
            start_dt, end_dt = None, None
            
            if date_span:
                meta_text = date_span.get_text(strip=True)
                if "|" in meta_text:
                    date_str, location = [x.strip() for x in meta_text.split("|", 1)]
                else:
                    date_str = meta_text
                    
                start_dt, end_dt = parse_date_range(date_str)
                
            # The description paragraph is usually after the date range paragraph
            desc_p = date_p.find_next_sibling("p") if date_p else None
            description = ""
            if desc_p:
                description = desc_p.get_text(strip=True)
                
            results.append({
                "month": month_id,
                "title": title,
                "url": href,
                "date_str": date_str,
                "location": location,
                "start_dt": start_dt,
                "end_dt": end_dt,
                "description": description[:100] + "..." if description else ""
            })
            
    print(f"Total parsed: {len(results)}")
    for i, res in enumerate(results[:5]):
        print(f"\n[{i+1}] Month: {res['month'].upper()}")
        print(f"    Title: {res['title']}")
        print(f"    URL: {res['url']}")
        print(f"    Date: {res['date_str']} | Location: {res['location']}")
        print(f"    Parsed Dates: {res['start_dt']} to {res['end_dt']}")
        print(f"    Desc: {res['description']}")

if __name__ == "__main__":
    test_parse()
