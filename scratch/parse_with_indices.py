import re

with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# 1. Find all matches of (\d+):T([A-Za-z0-9]+),
matches = list(re.finditer(r'(\d+):T([A-Za-z0-9]+),', stream))
print(f"Found {len(matches)} reference matches.")

ref_map = {}
for i in range(len(matches)):
    m = matches[i]
    ref_id = m.group(1)
    elem_id = m.group(2)
    start_pos = m.end() # text starts after the matched key
    
    # Text ends at the start of the next match, or end of stream
    end_pos = matches[i+1].start() if i + 1 < len(matches) else len(stream)
    
    text = stream[start_pos:end_pos].strip()
    ref_map[ref_id] = text

print(f"Successfully mapped {len(ref_map)} references.")
print("\nSample mapped references:")
for k in list(ref_map.keys())[5:10]:
    print(f" - {k} -> {ref_map[k][:150]}...")
