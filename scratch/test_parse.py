import os
import sys
from bs4 import BeautifulSoup

# Read HTML file
html_path = "scratch_students_ieee.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

category_map = {}
for label in soup.find_all('label', class_='form-check-label'):
    cat_id = label.get('for')
    if cat_id and cat_id.startswith('cat-'):
        category_map[cat_id] = label.get_text(strip=True)

print("Category Map:", category_map)

# On this site, opportunities are stored in <p> tags with class "sub-cat"
count = 0
for p_tag in soup.find_all("p", class_="sub-cat"):
    a_tag = p_tag.find("a")
    if not a_tag:
        continue
        
    cat_id = p_tag.get("data-sub_cat_id")
    category_name = category_map.get(cat_id, "Scholarship/Award")
    
    title = a_tag.get_text(strip=True)
    url = a_tag.get("href")
    
    if title and url:
        print(f"Title: {title[:30]}... | Cat ID: {cat_id} -> {category_name}")
        count += 1
        if count >= 10:
            break
