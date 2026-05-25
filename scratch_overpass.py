import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
lat = 18.5204 # Pune
lon = 73.8567
radius_meters = 25000

overpass_query = f"""
[out:json];
(
    node["shop"="agrarian"](around:{radius_meters},{lat},{lon});
    node["shop"="agribusiness"](around:{radius_meters},{lat},{lon});
    node["shop"="agrochemical"](around:{radius_meters},{lat},{lon});
    node["shop"="farm"](around:{radius_meters},{lat},{lon});
    node["shop"="fertilizer"](around:{radius_meters},{lat},{lon});
);
out body;
"""

headers = {'User-Agent': 'AgromindApp/1.0 (test@example.com)'}
print("Querying...")
response = requests.post(overpass_url, data={'data': overpass_query}, headers=headers, timeout=30)
if response.status_code == 200:
    data = response.json()
    elements = data.get('elements', [])
    print(f"Found {len(elements)} shops.")
    for el in elements[:5]:
        print(el.get('tags', {}))
else:
    print("Error:", response.status_code)
