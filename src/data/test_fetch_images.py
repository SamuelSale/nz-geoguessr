# %%
import os

IMG_DIR = "data/raw/images"

total = 0
counts = {}
for region in sorted(os.listdir(IMG_DIR)):
    folder = os.path.join(IMG_DIR, region)
    if os.path.isdir(folder):
        n = len([f for f in os.listdir(folder) if f.endswith(".jpg")])
        counts[region] = n
        total += n

for region, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"{n:5d}  {region}")
print(f"\nTotal images: {total}")
print(f"Folders (regions): {len(counts)}")