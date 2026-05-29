import re
import json

with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# 1. Build a lookup dictionary of references to texts.
# In the Next.js stream, we have patterns like:
# 174:T92c,Important Dates...
# Let's find all occurrences of <id>:T<some_alphanumeric>,<text>
# We can use a regex that matches: (\d+):T[a-f0-9]+,(.*?) followed by Next.js delimiters like \n or " or id:
# Wait, let's look at the delimiters. The stream has lines or chunks separated by \n or Next.js push boundaries.
# Let's write a regex that matches: (\d+):T[a-f0-9]+,(.*?)(?=\n\d+:|\n[a-f0-9]+:|\]\)|\Z)
# Let's make it robust. We can search for (\d+):T([a-f0-9]+),(.*?)
# Let's test a simple split or regex search.
ref_map = {}
# Find all matching definitions in the stream
ref_matches = re.finditer(r'(\d+):T([a-f0-9]+),(.*?)(?=\n\d+:|\Z)', stream, re.DOTALL)
for m in ref_matches:
    ref_id = m.group(1)
    elem_id = m.group(2)
    text = m.group(3).strip()
    # Clean up trailing quotes or junk if any
    if text.endswith('",') or text.endswith('"]'):
        # Clean next elements
        pass
    ref_map[ref_id] = text

print(f"Total reference mappings found: {len(ref_map)}")
print("Sample ref mappings:")
for k in list(ref_map.keys())[:5]:
    print(f" - {k} -> {ref_map[k][:100]}...")

# 2. Find all CFP Cards.
# Each card looks like:
# {"aria-label":"Call For Paper Card","id":"cfp-card", ... }
# Let's search for all JSON blocks representing a CFP card.
# Because the stream is stringified react structure, we can search for blocks starting with:
# {"aria-label":"Call For Paper Card","id":"cfp-card" ... ]}
# Let's find each occurrence of {"aria-label":"Call For Paper Card" and match the bracket contents.
cards = []
# We can split by {"aria-label":"Call For Paper Card"
card_parts = stream.split('{"aria-label":"Call For Paper Card"')
print(f"\nTotal potential card splits: {len(card_parts) - 1}")

for part in card_parts[1:]:
    # Reconstruct the card JSON by finding the closing brackets
    # Each card block ends with something like ]}
    # Let's parse it by matching braces/brackets, or simply using a regular expression.
    # A card is structured as:
    # ,"id":"cfp-card","className":"...","children":[ [type_p], [link_div], [desc_p], [date_div] ]
    # Let's extract the fields using robust regex matching inside this part.
    
    # Extract Type and Publication
    # Example: [" ","Magazine"," ","- IEEE Computer Graphics and Applications"," "]
    pub_match = re.search(r'\"children\":\[\s*\" \",\s*\"(Magazine|Journal|Conference)\",\s*\" \",\s*\"-\s*(.*?)\",\s*\" \"\s*\]', part)
    if not pub_match:
        # Fallback to general type if publication name is empty/different
        pub_match = re.search(r'\"children\":\[\s*\" \",\s*\"(Magazine|Journal|Conference)\",\s*\" \",\s*\"(.*?)\",\s*\" \"\s*\]', part)
        
    card_type = pub_match.group(1) if pub_match else "Journal/Magazine"
    pub_name = pub_match.group(2).strip() if pub_match else "IEEE Computer Society"
    
    # Extract Title and Href
    # Example: {"href":"/digital-library/magazines/cg/cfp-next-generation-xr-displays","className":"...","children":"Title Text"}
    # Or "children":["title part", ...]
    link_match = re.search(r'\"href\":\"(.*?)\",\"className\":\".*?\",\"prefetch\":(?:true|false),\"children\":\"(.*?)\"', part)
    if not link_match:
        # Try without prefetch
        link_match = re.search(r'\"href\":\"(.*?)\",\"className\":\".*?\",\"children\":\"(.*?)\"', part)
        
    href = link_match.group(1) if link_match else ""
    title = link_match.group(2) if link_match else ""
    
    # Extract Description Reference
    # Example: "className":"style-p line-clamp-3","children":"$174"
    desc_match = re.search(r'\"className\":\"style-p line-clamp-3\",\"children\":\"\$(\d+)\"', part)
    desc_ref = desc_match.group(1) if desc_match else None
    
    description = ""
    if desc_ref and desc_ref in ref_map:
        description = ref_map[desc_ref]
        # Clean description text
        # If it has Next.js escaping or trailing junk, clean it
        description = re.sub(r'\\n', '\n', description)
        description = re.sub(r'\\"', '"', description)
        
    # Extract Deadline/Dates
    # Example: "className":"style-p-sm font-normal text-slate-600","children":[" ","Submissions Due: ","30 September 2026"]
    date_match = re.search(r'\"className\":\"style-p-sm font-normal text-slate-600\",\"children\":\[\s*\" \",\s*\"Submissions Due:\s*\",\s*\"(.*?)\"\s*\]', part)
    if not date_match:
        # Try generic Submissions Due pattern
        date_match = re.search(r'\"Submissions Due:\s*\",\s*\"(.*?)\"\s*\]', part)
        
    deadline = date_match.group(1) if date_match else None
    
    # Only add if we got a valid title and URL
    if title and href:
        # Clean title escaping
        title = title.replace('\\"', '"').replace('\\\\', '\\')
        
        cards.append({
            "title": title,
            "category": card_type,
            "publication": pub_name,
            "url": "https://www.computer.org" + href if not href.startswith("http") else href,
            "description": description,
            "deadline": deadline
        })

print(f"\nSuccessfully parsed {len(cards)} cards!")
for i, card in enumerate(cards[:10]):
    print(f"\nCard {i+1}:")
    print(f" - Title: {card['title']}")
    print(f" - Type: {card['category']} | Pub: {card['publication']}")
    print(f" - URL: {card['url']}")
    print(f" - Deadline: {card['deadline']}")
    print(f" - Desc snippet: {card['description'][:150]}...")
