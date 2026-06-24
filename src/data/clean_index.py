# %%
"""Build the clean region manifest.

Reads the raw GeoGuessr location export and produces panos.csv: one row per
panorama with a 14-class region label, ready for the image fetcher.
"""
import os
import json
import pandas as pd

# %%
# The 16 official NZ regions. The raw export also contains nulls and stray
# locality names in the region field; anything not in this list is dropped.
OFFICIAL = [
    "Northland Region", "Auckland", "Waikato Region", "Bay of Plenty Region",
    "Gisborne Region", "Hawke's Bay Region", "Taranaki Region",
    "Manawatū-Whanganui Region", "Wellington Region", "Tasman Region",
    "Nelson Region", "Marlborough Region", "West Coast Region",
    "Canterbury Region", "Otago Region", "Southland Region",
]

# Nelson, Tasman and Marlborough are merged: each has too few panoramas with
# Street View coverage to stand alone as a class. Regions absent from this map
# keep their own name.
GROUP_MAP = {
    "Nelson Region": "Top of the South",
    "Tasman Region": "Top of the South",
    "Marlborough Region": "Top of the South",
}

IN_PATH = "data/Map/Locations.json"
OUT_PATH = "data/interim/panos.csv"

# %%
# Records live under the "customCoordinates" key; utf-8 preserves macrons
# (Manawatū) and the apostrophe in Hawke's Bay, which the region filter needs.
with open(IN_PATH, encoding="utf-8") as f:
    raw = json.load(f)
df = pd.DataFrame(raw["customCoordinates"])
print("Loaded:", len(df), "rows")

# %%
df = df[["panoId", "lat", "lng", "heading", "region"]]

# Drop noise, then add the grouped label. .copy() detaches the filtered slice
# so the new-column assignment doesn't raise SettingWithCopyWarning.
df_clean = df[df["region"].isin(OFFICIAL)].copy()
df_clean["region_group"] = df_clean["region"].replace(GROUP_MAP)
print(f"Kept {len(df_clean)} / {len(df)} rows after dropping noise")

# %%
os.makedirs("data/interim", exist_ok=True)
df_clean.to_csv(OUT_PATH, index=False)
print("Saved:", OUT_PATH)

print(f"\nFinal: {len(df_clean)} rows, {df_clean['region_group'].nunique()} groups")
print(df_clean["region_group"].value_counts())