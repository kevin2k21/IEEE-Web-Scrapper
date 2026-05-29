with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# Let's find "174:T" and "175:T"
idx_174 = stream.find('174:T')
idx_175 = stream.find('175:T')

if idx_174 != -1 and idx_175 != -1:
    print(stream[idx_174:idx_175])
else:
    print("Not found")
