with open("scratch/conferences_combined_stream.txt", "r", encoding="utf-8") as f:
    stream = f.read()

import re

# Let's search for ieeecps
idx = stream.find("ieeecps")
while idx != -1:
    print(f"\n--- Found ieeecps at {idx} ---")
    print(stream[idx-100:idx+250])
    idx = stream.find("ieeecps", idx+1)
