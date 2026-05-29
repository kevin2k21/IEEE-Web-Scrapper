import json
from bs4 import BeautifulSoup
import re

def test_jsonld_parse(file_path):
    print(f"\n========================================\nParsing File: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    if html.startswith("Title:"):
        html = html.split("---", 1)[1]
        
    soup = BeautifulSoup(html, "html.parser")
    results = []
    
    # Find all <script type="application/ld+json"> tags
    scripts = soup.find_all("script", type="application/ld+json")
    print(f"Found {len(scripts)} JSON-LD scripts.")
    
    for script in scripts:
        try:
            data = json.loads(script.string.strip())
            # In LinkedIn's company graph, the structure is either a single dictionary or a dict with "@graph" list
            graph = []
            if isinstance(data, dict):
                if "@graph" in data:
                    graph = data["@graph"]
                else:
                    graph = [data]
            elif isinstance(data, list):
                graph = data
                
            for item in graph:
                # We want item of type DiscussionForumPosting
                if item.get("@type") == "DiscussionForumPosting":
                    title = item.get("text", "")
                    # Extract external link using regex from text
                    ext_url = None
                    urls = re.findall(r'(https?://\S+)', title)
                    if urls:
                        # Grab the first external link (skip bit.ly if it points back, or just capture it)
                        ext_url = urls[0].strip()
                        
                    post_url = item.get("url", item.get("mainEntityOfPage"))
                    author = item.get("author", {}).get("name", "LinkedIn Update")
                    date_published = item.get("datePublished")
                    
                    results.append({
                        "title": title[:50].replace("\n", " ").strip() + "...",
                        "post_url": post_url,
                        "ext_url": ext_url if ext_url else post_url,
                        "date": date_published,
                        "text": title
                    })
        except Exception as e:
            print(f"Error parsing script: {e}")
            
    print(f"Successfully extracted {len(results)} DiscussionForumPosting posts:")
    for idx, r in enumerate(results[:3]):
        print(f"\n  [{idx+1}] Author/Org: {r['post_url']}")
        print(f"      Title: {r['title']}")
        print(f"      Ext URL: {r['ext_url']}")
        print(f"      Date: {r['date']}")
        print(f"      Text Sample: {r['text'][:120]}...")

if __name__ == "__main__":
    # Test on Madras Section LinkedIn file
    test_jsonld_parse("/Users/alonzoakevin/.gemini/antigravity-ide/brain/0909d623-752c-44d3-8f2d-4304c905f540/.system_generated/steps/589/content.md")
    
    # Test on Computer Society LinkedIn file
    test_jsonld_parse("/Users/alonzoakevin/.gemini/antigravity-ide/brain/0909d623-752c-44d3-8f2d-4304c905f540/.system_generated/steps/460/content.md")
