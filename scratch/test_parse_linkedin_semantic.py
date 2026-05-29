import os
from bs4 import BeautifulSoup
import re

def test_parse_linkedin():
    file_path = "/Users/alonzoakevin/.gemini/antigravity-ide/brain/0909d623-752c-44d3-8f2d-4304c905f540/.system_generated/steps/460/content.md"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    if html.startswith("Title:"):
        html = html.split("---", 1)[1]
        
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    # In LinkedIn guest view, each post card is typically inside an 'li' or 'div' in a feed list.
    # Let's search globally for elements that contain post links like /posts/ieee-computer-society
    # Or search for elements with attributes or links containing 'main-feed-card' in their trk parameter
    
    # Let's locate all post elements. Typically, each card has its own container.
    # We can find all links matching the post URL format: posts/ieee-computer-society
    post_links = soup.find_all("a", href=lambda h: h and "linkedin.com/posts/ieee-computer-society_" in h)
    print(f"Total post links found: {len(post_links)}")
    
    # Deduplicate post links
    seen_hrefs = set()
    unique_links = []
    for a in post_links:
        href = a["href"].split("?")[0].strip()
        if href not in seen_hrefs:
            seen_hrefs.add(href)
            unique_links.append(a)
            
    print(f"Unique post links: {len(unique_links)}")
    
    for i, a in enumerate(unique_links):
        href = a["href"].split("?")[0].strip()
        
        # In the markdown or HTML view, each post text is inside a card structure
        # Let's find the text. In guest view, the text is typically in a <p class="...text..."> or a sibling paragraph
        # Let's look around the parent containers of the link
        parent = a.find_parent("li")
        if not parent:
            parent = a.find_parent("div")
            
        post_text = ""
        ext_url = None
        
        if parent:
            # Look for any paragraph or element with class containing 'text' or find all paragraph elements
            # Or look for 'main-feed-card-text' class links or texts
            desc_elem = parent.find(class_=lambda c: c and "feed-card-text" in c)
            if not desc_elem:
                desc_elem = parent.find("p")
                
            if desc_elem:
                post_text = desc_elem.get_text(strip=True)
                
            # If still empty, search all text inside the parent and format it
            if not post_text:
                texts = [t.strip() for t in parent.find_all(text=True) if t.strip()]
                # Filter out standard metadata (like "Report this post", "Like", "Comment", shares)
                good_texts = []
                for t in texts:
                    if len(t) > 30 and not any(k in t.lower() for k in ["report", "like", "comment", "share", "follower", "http"]):
                        good_texts.append(t)
                if good_texts:
                    post_text = " ".join(good_texts)
                    
            # Look for external links (bit.ly, lnkd.in, youtube, etc.) inside this card
            for link in parent.find_all("a", href=True):
                l_href = link["href"]
                if any(x in l_href for x in ["bit.ly", "lnkd.in", "youtube.com", "youtu.be", "computer.org"]):
                    ext_url = l_href
                    break
                    
        # If no external URL is found, default to the post URL itself
        source_url = ext_url if ext_url else href
        
        results.append({
            "title": f"IEEE Computer Society Post: '{post_text[:50]}...'",
            "post_url": href,
            "source_url": source_url,
            "text": post_text
        })
        
    for idx, r in enumerate(results[:5]):
        print(f"\n[{idx+1}] Post URL: {r['post_url']}")
        print(f"    Target Source URL: {r['source_url']}")
        print(f"    Text: {r['text'][:200]}...")

if __name__ == "__main__":
    test_parse_linkedin()
