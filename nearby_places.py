import requests
googlekey = "AIzaSyDekKa-fWeb4rcrg5E2lH-6Krw5_CWxg2c"
def places_nearby(search: str, longitude: str, latitude: str):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': googlekey,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.currentOpeningHours'
    }
    # Convert data to JSON-serializable structure
    data_json_serializable = {
        "textQuery": search,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": float(latitude),
                    "longitude": float(longitude)
                },
                "radius": 500.0
            }
        }
    }

    response = requests.post(url, json=data_json_serializable, headers=headers)
    return response.json()

print(places_nearby("mechanics", "-75.70094","45.424117"))
