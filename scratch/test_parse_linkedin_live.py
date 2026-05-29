import httpx
from bs4 import BeautifulSoup
import re

url = "https://www.linkedin.com/company/ieee-computer-society?trk=similar-pages"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

print(f"Fetching live: {url}")
try:
    res = httpx.get(url, headers=headers, timeout=15)
    print(f"Status Code: {res.status_code}")
    
    # Check if we were redirected to authwall
    if "authwall" in str(res.url) or "login" in str(res.url):
        print(f"Redirected to login wall: {res.url}")
    else:
        print("Success! Serving guest view.")
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Print first few characters to verify
    print(res.text[:300])
    
    # Search for all links matching posts/ieee-computer-society using regex on href
    links = soup.find_all("a", href=re.compile(r'linkedin\.com/posts/ieee-computer-society'))
    print(f"Total post links found in HTML: {len(links)}")
    for i, a in enumerate(links[:5]):
        print(f" - Link {i+1}: {a.get('href')}")
        
    # Search globally for the post update containers. In LinkedIn guest page, 
    # it typically uses tags like class="main-feed-card" or class="feed-shared-update-v2"
    # Let's search for divs or lis containing "feed-card" or "update" in class name
    print("\nContainers containing 'feed-card' or 'update' in class:")
    for tag in soup.find_all(class_=lambda c: c and any(x in c for x in ["feed-card", "update-v2", "feed-item"])):
        print(f" - Tag: {tag.name} | Classes: {tag.get('class')}")
        break
        
except Exception as e:
    print(f"Error: {e}")
