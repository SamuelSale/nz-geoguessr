# %%
"""Build the clean region image database.

Reads data/interim/panos.csv, downloads one image per pano, saves into
per-region folders, skips and logs failures, and is safely re-runnable.
Calls the Google Street View Static API.
"""
import os
import pandas as pd
import requests
import time   # ⚠️ FIX: you'll need this for the delay between calls
from dotenv import load_dotenv

# %%
# ── Config ────────────────────────────────────────────────
load_dotenv()
key = os.getenv("GOOGLE_STATIC_MAPS_API")

PANOS = "data/interim/panos.csv"
IMG_DIR = "data/raw/images"
FAIL_LOG = "data/interim/failed.csv"

url = "https://maps.googleapis.com/maps/api/streetview"

# ── Helpers ────────────────────────────────────────────────
def safe_folder(name):
    return name.replace(" ", "_").replace("'", "")


# ── Load the manifest ─────────────────────────────────────
df = pd.read_csv(PANOS)   
      

failures = []   

# ── Main loop: one row = one pano = one image ─────────────
for _, row in df.iterrows():

    # STEP 1 — work out where this image will live (folder = its label)
    region = row["region_group"]
    region_processed = safe_folder(region)   

    # STEP 2 — build the folder path and make sure it exists
    folder = os.path.join(IMG_DIR, region_processed)
    os.makedirs(folder, exist_ok=True)       

    out_path = os.path.join(folder, f"{row['panoId']}.jpg")

    # STEP 3 — resumability: already downloaded? skip, no API call, no cost
    if os.path.exists(out_path):
        continue

    # STEP 4 — request the image
    params = {
        "size": "640x640",            # max resolution Google allows
        "pano": row["panoId"],        # exact panorama
        "heading": row["heading"],    # camera compass direction
        "key": key,
    }
    response = requests.get(url, params=params)

    # STEP 5 — validate + save, else log the failure
    ok = (response.status_code == 200
          and "image" in response.headers.get("Content-Type", "")
          and len(response.content) >= 10_000)
    if not ok:
        failures.append((row["panoId"], region, "bad_response"))
    else:
        with open(out_path, "wb") as f:  
            f.write(response.content)

    # STEP 6 — be polite to the API
    time.sleep(0.1)

# ── After the loop: persist the failure log ───────────────
if failures:
    pd.DataFrame(failures, columns=["panoId", "region_group", "reason"]).to_csv(
        FAIL_LOG, index=False)
   

print(f"Done. failures={len(failures)}")


