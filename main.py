import requests
import random
token = "pk.eyJ1IjoianVhbi03ODkiLCJhIjoiY2x0YTQweHptMHAyYzJqcDlwZXgxMmswcSJ9.AhK_cgF4NpDOCBfyOd8hvw"
weather_token = "c60f7979bd8746af860211144240203"
APIkey = "4dcb332f6d75f64572a7c363b95ed548"

# Example usage:
current_battery = 0.72  # current battery percentage
current_pressure = 39  # current tire pressure in psi
car_models = ["mme", "lightning", "nautilus", "etrongt"]
current_car = random.choice(car_models)  # current car model
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
    return recommended_psi_dict.get(car_model, 2)  # Return 0 if car_model not found

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

def station_charging_level():
    return random.randint(1, 3)

# Example usage:
charging_level = station_charging_level()
print("Charging level at the station:", charging_level)

def get_range(car_model):
    range_dict = {
        "mme": 402,
        "lightning": 386,
        "nautilus": 36,
        "etrongt": 383
    }
    return range_dict.get(car_model, 0)  # Return 0 if car_model not found

def get_remaining_range(current_car):
    range_value = get_range(current_car)
    return round(current_battery * range_value, 1)

remaining_range = get_remaining_range(current_car)
print("Remaining range for", current_car, ":", remaining_range, "km")

def getTheWeather(city:str):
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_token}&q={city}")
    print(response.url)

    parsed_data = []

    for forecast_day in response.json()['forecast']['forecastday']:
        date = forecast_day['date']
        max_temp_c = forecast_day['day']['maxtemp_c']
        min_temp_c = forecast_day['day']['mintemp_c']
        avg_temp_c = forecast_day['day']['avgtemp_c']
        condition_text = forecast_day['day']['condition']['text']
        max_wind_kph = forecast_day['day']['maxwind_kph']
        total_precip_mm = forecast_day['day']['totalprecip_mm']
        avg_visibility_km = forecast_day['day']['avgvis_km']
        avg_humidity = forecast_day['day']['avghumidity']
        uv_index = forecast_day['day']['uv']

        parsed_data.append({
            'date': date,
            'max_temp_c': max_temp_c,
            'min_temp_c': min_temp_c,
            'avg_temp_c': avg_temp_c,
            'condition_text': condition_text,
            'max_wind_kph': max_wind_kph,
            'total_precip_mm': total_precip_mm,
            'avg_visibility_km': avg_visibility_km,
            'avg_humidity': avg_humidity,
            'uv_index': uv_index
        })
    print(parsed_data)
    return parsed_data

def getBasicWeather(city:str):
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_token}&q={city}")
    print(response.url)

    parsed_data = []

    for forecast_day in response.json()['forecast']['forecastday']:
        date = forecast_day['date']
        avg_temp_c = forecast_day['day']['avgtemp_c']
        condition_text = forecast_day['day']['condition']['text']
        total_precip_mm = forecast_day['day']['totalprecip_mm']
        avg_humidity = forecast_day['day']['avghumidity']

        parsed_data.extend([date, avg_temp_c, condition_text, total_precip_mm, avg_humidity])

    print(parsed_data)
    return parsed_data

def getNearestCity(lat: int, lon: int):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={APIkey}")
    city_data = response.json()
    if city_data:  # Check if data is not empty
        return city_data[0]['name']
    else:
        return None  # Or handle the case when no data is returned

print()
#p = getBasicWeather("ottawa")
nr = getNearestCity(43.661957, -79.381525)
print("Nearest city:", nr)
weather = getBasicWeather("43.661957, -79.381525")
print("Basic weather data:", weather)