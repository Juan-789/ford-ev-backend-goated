import requests
token = "pk.eyJ1IjoianVhbi03ODkiLCJhIjoiY2x0YTQweHptMHAyYzJqcDlwZXgxMmswcSJ9.AhK_cgF4NpDOCBfyOd8hvw"
def getting_route(start_place: str, end_place: str):
    services = ["directions"]
    service = services[0]  # can be changed to wtv we need
    type_transportation = "driving" #wtv type we need

    start_longitude,  start_latitude= start_place.split(",")


    end_longitude, end_latitude = end_place.split(",")

    response = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/{type_transportation}/"
                            f"{start_longitude},{start_latitude};{end_longitude},{end_latitude}?geometries=geojson&access_token={token}")
    return response.url



def addressToCoord(address: str)->str:
    addResponse = requests.get(f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={token}")
    # print(addResponse.url)    check url
    data = addResponse.json()
    longitude, latitude = data.get("features")[0].get("geometry").get("coordinates")
    return str(longitude)+ ","+str(latitude) # coords


beginning = addressToCoord("111 wellington Ottawa ")
end = addressToCoord("1015 bank street ottawa")
print(getting_route(beginning, end))