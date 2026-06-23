from dotenv import load_dotenv
import os
import requests

load_dotenv()
key = os.getenv("GOOGLE_STATIC_MAPS_API")


# 2. The Street View Static API endpoint
url = "https://maps.googleapis.com/maps/api/streetview"

# 3. Request parameters
params = {
    "size": "640x640",                  # max resolution Google allows
    "pano": "Nr0aTB8h4Dg3Q3Kf8RZB5w",   # exact panorama: Barrytown, West Coast
    "heading": 55,                      # camera compass direction
    "key": key,
}

# 4. Send the request
resp = requests.get(url, params=params)
print("Status:", resp.status_code)
print("Content-Type:", resp.headers.get("Content-Type"))
print("Bytes:", len(resp.content))

# 5. Save the image bytes to disk
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/test.jpg", "wb") as f:
    f.write(resp.content)

print("Saved -> data/raw/test.jpg")