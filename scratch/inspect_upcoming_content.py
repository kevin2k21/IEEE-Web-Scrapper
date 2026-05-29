from bs4 import BeautifulSoup
import re

with open("scratch/ieee_madras_upcoming.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Let's find the content container. On standard WordPress sites, it is usually a div with class containing 'entry-content' or 'content'
content_divs = soup.find_all("div", class_=re.compile(r'content|entry|post|page'))
print(f"Found {len(content_divs)} potential content divs.")

for i, div in enumerate(content_divs):
    classes = div.get("class", [])
    text = div.get_text(strip=True)
    print(f"\nDiv {i}: Classes={classes}, Text length={len(text)}")
    if 50 < len(text) < 1500:
        print(f"Text: {text[:800]}...")
        # Check for any tables or lists inside
        list_items = div.find_all("li")
        anchors = div.find_all("a")
        print(f" -> Found {len(list_items)} list items, {len(anchors)} links")
        if len(anchors) > 0:
            for a in anchors[:10]:
                print(f"    * Link: '{a.get_text(strip=True)}' -> '{a.get('href')}'")
