with open("scratch/ieee_cs_fetch_result.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for "174:"
idx = html.find('174:')
if idx != -1:
    print(html[idx-100:idx+200])
else:
    print("Not found with 174:")
    # Let's try 174 in other ways
    idx2 = html.find('"174"')
    if idx2 != -1:
        print(html[idx2-100:idx2+200])
    else:
        print("Not found with \"174\"")
