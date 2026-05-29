with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# Let's find "92c"
idx = stream.find('92c')
while idx != -1:
    print(f"\n--- Found 92c at {idx} ---")
    print(stream[idx-100:idx+300])
    idx = stream.find('92c', idx+1)
