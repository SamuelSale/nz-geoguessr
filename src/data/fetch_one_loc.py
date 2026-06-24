from dotenv import load_dotenv
import os
import requests

load_dotenv()
key = os.getenv("GOOGLE_STATIC_MAPS_API")


# 2. The Street View Static API endpoint
url = "https://maps.googleapis.com/maps/api/streetview"

# 3. Request parameters (Params for EXACT LOCATION for a test)
params = {
    "size": "640x640",                  # max resolution Google allows
    "pano": "Nr0aTB8h4Dg3Q3Kf8RZB5w",   # exact panorama: Barrytown, West Coast
    "heading": 55,                      # camera compass direction
    "key": key,
}

# 4. Send the request
response = requests.get(url, params=params)

print("Status", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Bytes:", len(response.content))


# 5. Save the image bytes to disk
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/testing.jgp", "wb") as f:
    f.write(response.content)