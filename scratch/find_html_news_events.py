from bs4 import BeautifulSoup

with open("scratch/ieee_madras_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Let's find any h2 element with text containing "News & Events"
for h2 in soup.find_all("h2"):
    if "news & events" in h2.get_text().lower():
        print(f"Found heading: {h2.get_text()}")
        # Print the next sibling or parent div content
        parent = h2.find_parent("div") or h2.find_parent("section")
        if parent:
            print("\nParent Container HTML:")
            print(parent.prettify()[:2000])
        else:
            print("No parent container found")
