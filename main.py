import requests
services = ["directions"]
service = services[0]  # can be changed to wtv we need
type_transportation = "driving" #wtv type we need
token = "pk.eyJ1IjoianVhbi03ODkiLCJhIjoiY2x0YTQweHptMHAyYzJqcDlwZXgxMmswcSJ9.AhK_cgF4NpDOCBfyOd8hvw"
start_longitude = -84.518641
start_latitude = 39.134270
end_longitude = -84.512023
end_latitude = 39.102779

starting_location = (start_longitude, start_latitude)
end_location = (end_longitude, end_latitude)
response = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/{type_transportation}/"
                        f"{start_longitude},{start_latitude};{end_longitude},{end_latitude}?geometries=geojson&access_token={token}")
url = (f"https://api.mapbox.com/directions/v5/mapbox/{type_transportation}/"
                        f"{start_longitude},{start_latitude};{end_longitude},{end_latitude}?geometries=geojson&access_token={token}")
print(response)
