import os
from bs4 import BeautifulSoup
import re

def test_parse_contests():
    file_path = "/Users/alonzoakevin/.gemini/antigravity-ide/brain/0909d623-752c-44d3-8f2d-4304c905f540/.system_generated/steps/520/content.md"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    if html.startswith("Title:"):
        html = html.split("---", 1)[1]
        
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    # Locate all evants_column divs inside evants_blocks_row
    columns = soup.find_all("div", class_="evants_column")
    print(f"Total columns found: {len(columns)}")
    
    for i, col in enumerate(columns):
        # Extract title and href
        a_title = col.find("a", class_="block_title")
        if not a_title:
            continue
            
        title = a_title.get_text(strip=True)
        href = a_title.get("href")
        
        # Parse entry details
        entry_div = col.find("div", class_="entry")
        organizer = ""
        eligibility = ""
        desc_text = ""
        deadline_text = ""
        
        if entry_div:
            # We can extract details by looking for p strong tags or parsing key-values
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
                    elif "deadline" in key:
                        deadline_text = val
                else:
                    # Fallback to general desc text if not strong-tagged key
                    desc_text += " " + p_text
                    
        # Construct clean summary
        description_parts = []
        if desc_text.strip():
            description_parts.append(desc_text.strip())
        if eligibility.strip():
            description_parts.append(f"Eligibility: {eligibility.strip()}")
            
        description = " | ".join(description_parts)
        if not description.strip():
            description = f"IEEE Student Contest opportunity: '{title}'."
            
        results.append({
            "title": title,
            "url": href,
            "organizer": organizer if organizer else "IEEE Students",
            "deadline_str": deadline_text,
            "description": description[:150] + "..." if len(description) > 150 else description
        })
        
    print(f"\nSuccessfully parsed: {len(results)} contests")
    for idx, res in enumerate(results[:5]):
        print(f"\n[{idx+1}] Title: {res['title']}")
        print(f"    URL: {res['url']}")
        print(f"    Organizer: {res['organizer']}")
        print(f"    Deadline Text: {res['deadline_str']}")
        print(f"    Description: {res['description']}")

if __name__ == "__main__":
    test_parse_contests()
