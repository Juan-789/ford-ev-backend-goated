import requests
import random
token = "pk.eyJ1IjoianVhbi03ODkiLCJhIjoiY2x0YTQweHptMHAyYzJqcDlwZXgxMmswcSJ9.AhK_cgF4NpDOCBfyOd8hvw"

# Example usage:
current_pressure = 39  # current tire pressure in psi
current_car = "etrongt"  # current car model
mode = "sport"  # Example drive mode

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

def get_recommended_psi(car_model):
    recommended_psi_dict = {
        "mme": 39,
        "lightning": 37,
        "nautilus": 35,
        "etrongt": 42
    }
    return recommended_psi_dict.get(car_model, 0)  # Return 0 if car_model not found

def tire_pressure_status(current_psi, car_model):
    recommended_psi = get_recommended_psi(car_model)
    if current_psi >= recommended_psi - 5 and current_psi <= recommended_psi + 2:
        return 0
    elif current_psi > recommended_psi + 2:
        return 2
    else:
        return 1

def get_status_message(status):
    if status == 0:
        return "Tire pressure is within a safe range"
    elif status == 2:
        return "Tire pressure is higher, you may or may not want to lower it"
    else:
        return "Tire pressure is significantly below recommendation, it's suggested that you increase it"

tire_status = tire_pressure_status(current_pressure, current_car)
tire_message = get_status_message(tire_status)
print("Tire pressure status:", tire_message)

# Randomly generate battery usage for a trip and return each aspects usage percentage
def trip_energy():
    climate_use = random.randint(5, 12)
    route = random.randint(60, 75)
    accessories = random.randint(5, 12)
    exterior_temperature = 100 - (climate_use + route + accessories)
    return climate_use, route, accessories, exterior_temperature

climate_use, route, accessories, exterior_temperature = trip_energy()
print("Climate Use:", climate_use, "- Route:", route, "- Accessories:", accessories, "- Exterior Temperature:", exterior_temperature)

# Return the utilization usage percentage of the car's power
def drive_mode(mode):
    if mode == "eco":
        return 60
    elif mode == "sport":
        return 100
    else:
        return 80  # default to normal drive mode

energy_consumption = drive_mode(mode)
print("Energy output usage for", mode, "mode:", energy_consumption, "%")