from bs4 import BeautifulSoup

with open("scratch/ieee_madras_upcoming.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Checking headings...")
headings = []
for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
    for elem in soup.find_all(tag):
        text = elem.get_text(strip=True)
        headings.append(f"{tag}: {text}")

for h in list(set(headings))[:15]:
    print(f" - {h}")

print("\nChecking any divs with class names containing 'event'...")
event_divs = []
for div in soup.find_all("div"):
    classes = div.get("class", [])
    for c in classes:
        if "event" in c.lower():
            event_divs.append(c)

for c in list(set(event_divs))[:10]:
    print(f" - Div class: {c}")
