import re

with open("scratch/combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

# Let's find the first index of "Call For Paper Card"
idx = stream.find('"aria-label":"Call For Paper Card"')
if idx != -1:
    # Print 2000 characters from there
    print(stream[idx:idx+2000])
else:
    print("Not found")
