import requests
import random
from datetime import datetime

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
    return parsed_data

def getBasicWeather(city:str):
    response = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={weather_token}&q={city}")

    parsed_data = []

    for forecast_day in response.json()['forecast']['forecastday']:
        date = forecast_day['date']
        avg_temp_c = forecast_day['day']['avgtemp_c']
        condition_text = forecast_day['day']['condition']['text']
        total_precip_mm = forecast_day['day']['totalprecip_mm']
        avg_humidity = forecast_day['day']['avghumidity']

        parsed_data.extend([date, avg_temp_c, condition_text, total_precip_mm, avg_humidity])

    return parsed_data

def getNearestCity(lat: int, lon: int):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&appid={APIkey}")
    city_data = response.json()
    if city_data:  # Check if data is not empty
        return city_data[0]['name']
    else:
        return None  # Or handle the case when no data is returned

print()
nr = getNearestCity(43.661957, -79.381525)
print("Nearest city:", nr)
weather = getBasicWeather("43.661957, -79.381525")
print("Basic weather data:", weather)
print()

def check_car_health(vehicle_data):
    # Thresholds for different health metrics
    battery_health_threshold = 90.0
    tire_pressure_threshold = 32
    temperature_threshold = 40.0
    tread_depth_threshold = 4

    # Extracting relevant data from the provided JSON
    battery_health = vehicle_data['vehicleHealth']['battery']['health']
    tire_pressure = vehicle_data['vehicleHealth']['tirePressure']
    battery_temperature = vehicle_data['vehicleHealth']['temperature']['battery']
    tire_tread_depth = vehicle_data['vehicleHealth']['tireTreadDepth']

    # Check battery health
    if battery_health < battery_health_threshold:
        return "Visit mechanic: Battery health is below the "+str(battery_health_threshold) + "% threshold."

    # Check tire pressure
    for tire, pressure in tire_pressure.items():
        if pressure < tire_pressure_threshold:
            return f"Visit mechanic: Low tire pressure in {tire} tire."

    # Check battery temperature
    if battery_temperature > temperature_threshold:
        return "Visit mechanic: High battery temperature."

    # Check tire tread depth
    for tire, tread_depth in tire_tread_depth.items():
        if tread_depth < tread_depth_threshold:
            return f"Visit mechanic: Low tread depth in {tire} tire."

    # If no issues found
    return "No immediate issues detected. Regular maintenance recommended."


def check_upcoming_tasks(vehicle_data, current_date):
    # Extracting relevant data from the provided JSON
    service_reminders = vehicle_data['vehicleHealth']['serviceReminders']

    # Convert the current date string to a datetime object
    current_date = datetime.strptime(current_date, "%Y-%m-%d")

    upcoming_tasks = []

    for reminder in service_reminders:
        due_date = datetime.strptime(reminder['dueDate'], "%Y-%m-%d")
        days_until_due = (due_date - current_date).days

        if days_until_due >= 0:
            upcoming_tasks.append({
                "task": reminder['task'],
                "due_date": reminder['dueDate'],
                "days_until_due": days_until_due
            })

    return upcoming_tasks


car_data = {
  "vehicleHealth": {
    "battery": {
      "stateOfCharge": 85.2,
      "health": 82.5,
      "chargingRate": 6.8
    },
    "rangeEstimation": 200,
    "tirePressure": {
      "frontLeft": 34,
      "frontRight": 34,
      "rearLeft": 36,
      "rearRight": 36
    },
    "temperature": {
      "battery": 25.5,
      "motor": 30.2
    },
    "regenerativeBraking": {
      "status": "Normal"
    },
    "serviceReminders": [
      {
        "task": "Tire Rotation",
        "dueDate": "2024-05-01"
      },
      {
        "task": "Brake Inspection",
        "dueDate": "2024-07-15"
      }
    ],
    "efficiencyMetrics": {
      "kWhPerMile": 0.28
    },
    "softwareUpdates": {
      "status": "Available",
      "lastChecked": "2024-03-02"
    },
    "chargingStationCompatibility": {
      "status": "Compatible"
    },
    "tireTreadDepth": {
      "frontLeft": 7,
      "frontRight": 7,
      "rearLeft": 8,
      "rearRight": 8
    },
    "hvacSystem": {
      "status": "Normal"
    },
    "maintenanceHistory": [
      {
        "date": "2023-12-10",
        "service": "Battery Health Check"
      },
      {
        "date": "2024-01-20",
        "service": "Tire Rotation"
      }
    ]
  }
}

current_date = "2024-03-02"

upcoming_tasks_result = check_upcoming_tasks(car_data, current_date)

if upcoming_tasks_result:
    print("Upcoming tasks:")
    for task in upcoming_tasks_result:
        print(f"{task['task']} is due on {task['due_date']}. {task['days_until_due']} days remaining.")
else:
    print("No upcoming tasks.")

result = check_car_health(car_data)
print('\n'+result)
