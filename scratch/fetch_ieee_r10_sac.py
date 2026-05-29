import httpx
from bs4 import BeautifulSoup

urls = [
    "https://sac.ieeer10.org/ieee-region-10-student-summit-2026/",
    "https://sac.ieeer10.org/ieee-r10-section-student-branch-revival-fund-2025/",
    "https://sac.ieeer10.org/osb-award/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for url in urls:
    print(f"\nFetching: {url}")
    try:
        res = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Print page title
        title = soup.find("title").get_text(strip=True) if soup.find("title") else "No Title"
        print(f"Title: {title}")
        
        # Check div container classes
        print("Searching for paragraphs inside the page...")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        print(f"Total paragraphs found: {len(paragraphs)}")
        for i, p in enumerate(paragraphs[:4]):
            print(f" - P{i+1}: {p[:150]}")
            
    except Exception as e:
        print(f"Error fetching {url}: {e}")
