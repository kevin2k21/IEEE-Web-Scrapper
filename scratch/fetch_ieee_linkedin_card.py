import httpx
from bs4 import BeautifulSoup

url = "https://www.linkedin.com/company/ieee-computer-society?trk=similar-pages"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

res = httpx.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(res.text, "html.parser")

feed_items = soup.find_all(class_=lambda c: c and "main-feed-card" in c)

for item in feed_items:
    parent = item.find_parent("li")
    if not parent:
        parent = item.find_parent("div")
    if parent:
        print("\n=== Found Parent Card Texts ===")
        # Print all paragraphs inside parent
        for i, p in enumerate(parent.find_all("p")):
            print(f"Paragraph {i+1}: {p.get_text(strip=True)}")
            
        # Print all links inside parent
        print("\nLinks:")
        for a in parent.find_all("a", href=True):
            print(f" - href: {a['href']} | Text: {a.get_text(strip=True)}")
        break
