from flask import Blueprint, request, jsonify

endpoints = Blueprint('map', __name__)

# Store latest coordinates in memory (for demo purposes)
stored_data = {'lat': None, 'lon': None, 'battery_level': None}

def get_stored_data():
    """ 
    Helper function to retrieve the latest stored data.
    """
    return stored_data

@endpoints.route('/map/update', methods=['POST'])
def update_map_data():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    if lat is not None and lon is not None:
        stored_data['lat'] = lat
        stored_data['lon'] = lon
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Missing lat/lon'}), 400

@endpoints.route('/map', methods=['GET'])
def get_map_data():
    """
    GET /map
    Returns the latest latitude and longitude coordinates received via POST.
    Output: JSON object with 'lat' and 'lon' keys.
    """
    return jsonify(stored_data)

@endpoints.route('/battery/update', methods=['POST'])
def update_battery_data():
    data = request.get_json()
    battery_level = data.get('battery_level')
    if battery_level is not None:
        stored_data['battery_level'] = battery_level
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Missing battery_level'}), 400

@endpoints.route('/battery', methods=['GET'])
def get_battery_data():
    """
    GET /battery
    Returns the latest battery level received via POST.
    Output: JSON object with 'battery_level' key.
    """
    battery_level = stored_data.get('battery_level')
    return jsonify({'battery_level': battery_level})

@endpoints.route('/data/update', methods=['POST'])
def update_data():
    """
    POST /data/update
    Updates full data set including lat, lon, battery_level, etc.
    Input: JSON object with any of the stored keys.
    """
    data = request.get_json()
    stored_data.update(data)
    return jsonify({'status': 'success'}), 200

@endpoints.route('/data', methods=['GET'])
def get_data():
    """
    GET /data
    Returns the latest data received via POST.
    Output: JSON object with all stored keys.
    """
    return jsonify(stored_data)