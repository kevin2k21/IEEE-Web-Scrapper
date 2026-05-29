from bs4 import BeautifulSoup

with open("scratch/ieee_madras_upcoming.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
entry = soup.find("div", class_="entry-content")
if entry:
    print("Entry content HTML:")
    print(entry.prettify())
else:
    print("Entry content not found")
