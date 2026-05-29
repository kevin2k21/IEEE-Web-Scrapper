from bs4 import BeautifulSoup
import re

with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Checking header/navigation menu...")
links = []
for a in soup.find_all("a", href=True):
    href = a.get("href")
    text = a.get_text(strip=True)
    if "event" in href.lower() or "event" in text.lower() or "announc" in href.lower() or "announc" in text.lower() or "news" in href.lower() or "news" in text.lower():
        links.append((text, href))

for text, href in set(links):
    print(f" - Link text: '{text}' -> URL: '{href}'")

print("\nChecking homepage headings...")
headings = []
for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
    for elem in soup.find_all(tag):
        text = elem.get_text(strip=True)
        if "event" in text.lower() or "announc" in text.lower() or "news" in text.lower() or "upcoming" in text.lower():
            headings.append(f"{tag}: {text}")

for h in set(headings):
    print(f" - {h}")
