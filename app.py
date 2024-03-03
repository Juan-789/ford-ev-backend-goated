from flask import Flask, jsonify, request
import requests
 
app = Flask(__name__)
 
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoianVhbi03ODkiLCJhIjoiY2x0YTQweHptMHAyYzJqcDlwZXgxMmswcSJ9.AhK_cgF4NpDOCBfyOd8hvw"
base_url = 'https://services.arcgis.com/zmLUiqh7X11gGV2d/arcgis/rest/services/alt_fuel_stations/FeatureServer'
 
@app.route('/directions', methods=['GET'])
def get_directions():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'Missing start or end coordinates'}), 400
    response = requests.get(
        f"https://api.mapbox.com/directions/v5/mapbox/driving/{start};{end}",
        params={
            'geometries': 'geojson',
            'access_token': MAPBOX_ACCESS_TOKEN,
            'overview': 'full'
        }
    )
    if response.status_code == 200:
        routes = response.json().get('routes', [])
        if routes:
            return jsonify(routes[0].get('geometry')), 200
        else:
            return jsonify({'error': 'No route found'}), 404
    else:
        return jsonify({'error': 'Failed to get directions'}), response.status_code
 
@app.route('/nearest', methods=['GET'])
def nearest_stations():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
 
    if not latitude or not longitude:
        return jsonify({'error': 'Please provide both latitude and longitude'}), 400
 
    url = f"https://services.arcgis.com/zmLUiqh7X11gGV2d/arcgis/rest/services/alt_fuel_stations/FeatureServer/0/query?where=1%3D1&geometry={longitude},{latitude}&geometryType=esriGeometryPoint&inSR=4326&outFields=*&spatialRel=esriSpatialRelIntersects&outSR=4326&distance=1000&units=esriSRUnit_Meter&f=json"
 
    response = requests.get(url)
    print(response.json())
    data = response.json()
 
    return jsonify(data)
 
if __name__ == '__main__':
    app.run(debug=True)