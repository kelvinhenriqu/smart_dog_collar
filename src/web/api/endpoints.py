from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime, timedelta

endpoints = Blueprint('map', __name__)


stored_data = {}
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'location_history.json')

def save_location(lat, lon):
    entry = {
        'lat': lat,
        'lon': lon,
        'timestamp': datetime.now().isoformat()
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(entry)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f)

def get_location_history(period_minutes=60):
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except Exception:
        return []
    cutoff = datetime.now() - timedelta(minutes=period_minutes)
    filtered = [h for h in history if 'timestamp' in h and datetime.fromisoformat(h['timestamp']) >= cutoff]
    return filtered

def get_stored_data():
    return stored_data

@endpoints.route('/map/update', methods=['POST'])
def update_map_data():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    if lat is not None and lon is not None:
        stored_data['lat'] = lat
        stored_data['lon'] = lon
        save_location(lat, lon)
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Missing lat/lon'}), 400


@endpoints.route('/map/history', methods=['GET'])
def get_map_history():
    """
    Output: JSON list of positions in the last X minutes. Query param: period (minutes)
    """
    try:
        period = int(request.args.get('period', 60))
    except Exception:
        period = 60
    history = get_location_history(period)
    return jsonify({'history': history})

@endpoints.route('/map', methods=['GET'])
def get_map_data():
    """
    Output: JSON object with 'lat' and 'lon' keys.
    """
    return jsonify(stored_data)

@endpoints.route('/battery/update', methods=['POST'])
def update_battery_data():
    """
    Input: Expect JSON object with 'battery_level' key from 0-100.
    """
    data = request.get_json()
    battery_level = data.get('battery_level')
    if battery_level is not None:
        stored_data['battery_level'] = battery_level
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Missing battery_level'}), 400

@endpoints.route('/battery', methods=['GET'])
def get_battery_data():
    """
    Output: JSON object with 'battery_level' key.
    """
    battery_level = stored_data.get('battery_level')
    return jsonify({'battery_level': battery_level})

@endpoints.route('/data/update', methods=['POST'])
def update_data():
    """
    Input: JSON object with any of the stored keys. Used mainly for testing in Postman.
    """
    data = request.get_json()
    stored_data.update(data)
    return jsonify({'status': 'success'}), 200

@endpoints.route('/data/sensor', methods=['GET'])
def get_data():
    """
    Output: JSON object with all additional keys..
    """
    return jsonify(stored_data)