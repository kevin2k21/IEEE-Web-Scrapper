from bs4 import BeautifulSoup

with open("scratch/ieee_cs_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script")
print(f"Total script tags: {len(scripts)}")

for i, script in enumerate(scripts):
    src = script.get("src")
    stype = script.get("type")
    sid = script.get("id")
    content = script.get_text()
    
    print(f"\nScript {i}: ID={sid}, Type={stype}, Src={src}, Length={len(content)}")
    if content and len(content) < 500:
        print(f"Content: {content[:300]}")
    elif content:
        print(f"Content (truncated): {content[:300]}...")
