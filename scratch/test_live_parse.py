import asyncio
import httpx
from bs4 import BeautifulSoup

async def main():
    url = "https://students.ieee.org/student-opportunities/"
    print(f"Fetching {url}...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    category_map = {}
    for label in soup.find_all('label', class_='form-check-label'):
        cat_id = label.get('for')
        if cat_id and cat_id.startswith('cat-'):
            category_map[cat_id] = label.get_text(strip=True)
            
    print("Category Map:", category_map)
    
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

if __name__ == "__main__":
    asyncio.run(main())
