from bs4 import BeautifulSoup

with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
header = soup.find("div", class_="news-header")
if header:
    # Print the parent of the header which should contain the full news section
    parent = header.parent
    print("Full News Section Parent container:")
    print(parent.prettify()[:4000])
else:
    print("News-header div not found")
