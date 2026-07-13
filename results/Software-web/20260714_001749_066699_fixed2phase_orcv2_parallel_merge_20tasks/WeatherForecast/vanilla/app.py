from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'
USER_ID = 1  # fixed user id as per design spec

# --- Utility functions for data loading and saving ---

def parse_line(line):
    return line.strip().split('|')

def read_current_weather():
    path = os.path.join(DATA_DIR, 'current_weather.txt')
    weather = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    location_id = int(parts[0])
                    weather[location_id] = {
                        'location_id': location_id,
                        'location_name': parts[1],
                        'temperature': parts[2],
                        'condition': parts[3],
                        'humidity': parts[4],
                        'wind_speed': parts[5],
                        'last_updated': parts[6],
                    }
    return weather

def read_forecasts():
    path = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    forecasts.append({
                        'forecast_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'date': parts[2],
                        'high_temp': parts[3],
                        'low_temp': parts[4],
                        'condition': parts[5],
                        'precipitation': parts[6],
                        'humidity': parts[7],
                    })
    return forecasts

def read_locations():
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    location_id = int(parts[0])
                    locations[location_id] = {
                        'location_id': location_id,
                        'location_name': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3],
                        'country': parts[4],
                        'timezone': parts[5],
                    }
    return locations

def read_alerts():
    path = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    alerts.append({
                        'alert_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7] == '1',
                    })
    return alerts

def write_alerts(alerts):
    path = os.path.join(DATA_DIR, 'alerts.txt')
    lines = []
    for alert in alerts:
        line = '|'.join([
            str(alert['alert_id']),
            str(alert['location_id']),
            alert['alert_type'],
            alert['severity'],
            alert['description'],
            alert['start_time'],
            alert['end_time'],
            '1' if alert['is_acknowledged'] else '0'
        ])
        lines.append(line)
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def read_air_quality():
    path = os.path.join(DATA_DIR, 'air_quality.txt')
    aqi_data = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    location_id = int(parts[1])
                    aqi_data[location_id] = {
                        'aqi_id': int(parts[0]),
                        'location_id': location_id,
                        'aqi_index': int(parts[2]),
                        'pm25': parts[3],
                        'pm10': parts[4],
                        'no2': parts[5],
                        'o3': parts[6],
                        'last_updated': parts[7],
                    }
    return aqi_data


def read_saved_locations():
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = parse_line(line)
                    uid = int(parts[1])
                    if uid == USER_ID:
                        saved.append({
                            'saved_id': int(parts[0]),
                            'user_id': uid,
                            'location_id': int(parts[2]),
                            'location_name': parts[3],
                            'is_default': parts[4] == '1'
                        })
    return saved


def write_saved_locations(saved):
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    lines = []
    saved_id_counter = 1
    for loc in saved:
        line = '|'.join([
            str(saved_id_counter),
            str(USER_ID),
            str(loc['location_id']),
            loc['location_name'],
            '1' if loc.get('is_default', False) else '0'
        ])
        lines.append(line)
        saved_id_counter += 1

    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def read_settings():
    path = os.path.join(DATA_DIR, 'settings.txt')
    settings = {
        'temperature_unit': 'F',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        key, value = parts
                        if key == 'temperature_unit':
                            settings['temperature_unit'] = value
                        elif key == 'default_location_id':
                            try:
                                settings['default_location_id'] = int(value)
                            except ValueError:
                                settings['default_location_id'] = None
                        elif key == 'alert_notifications_enabled':
                            settings['alert_notifications_enabled'] = (value == '1')
    return settings


def write_settings(settings):
    path = os.path.join(DATA_DIR, 'settings.txt')
    lines = [
        f"temperature_unit={settings.get('temperature_unit', 'F')}",
        f"default_location_id={settings.get('default_location_id', '') if settings.get('default_location_id') is not None else ''}",
        f"alert_notifications_enabled={'1' if settings.get('alert_notifications_enabled', True) else '0'}"
    ]
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def get_default_location_id():
    settings = read_settings()
    if settings['default_location_id'] is not None:
        return settings['default_location_id']
    saved = read_saved_locations()
    if saved:
        return saved[0]['location_id']
    locations = read_locations()
    if locations:
        return next(iter(locations))
    return None


@app.route('/')
def dashboard():
    default_location_id = get_default_location_id()
    current_weather = read_current_weather()
    location_weather = current_weather.get(default_location_id, None)
    return render_template('dashboard.html', current_weather=location_weather)


@app.route('/weather/current/<int:location_id>')
def current_weather_page(location_id):
    current_weather = read_current_weather()
    weather = current_weather.get(location_id, None)
    return render_template('current_weather.html', weather=weather)


@app.route('/forecast')
def weekly_forecast():
    location_id = request.args.get('location_id', type=int)
    if location_id is None:
        location_id = get_default_location_id()

    forecasts = read_forecasts()
    filtered_forecasts = [f for f in forecasts if f['location_id'] == location_id]
    filtered_forecasts.sort(key=lambda x: x['date'])

    locations = read_locations()
    return render_template('weekly_forecast.html', forecast_list=filtered_forecasts, locations=locations, selected_location_id=location_id)


@app.route('/locations/search')
def location_search():
    query = request.args.get('query', '').strip().lower()
    locations = read_locations()
    saved_locations = read_saved_locations()

    search_results = []
    if query:
        for loc in locations.values():
            match_name = query in loc['location_name'].lower()
            try:
                if ',' in query:
                    lat_str, lon_str = query.split(',', 1)
                    lat = float(lat_str.strip())
                    lon = float(lon_str.strip())
                    try_lat = round(float(loc['latitude']), 3)
                    try_lon = round(float(loc['longitude']), 3)
                    if abs(try_lat - lat) < 0.001 and abs(try_lon - lon) < 0.001:
                        match_name = True
            except ValueError:
                pass
            if match_name:
                search_results.append(loc)
    else:
        search_results = []

    return render_template('location_search.html', saved_locations=saved_locations, search_results=search_results, query=query)


@app.route('/locations/select', methods=['POST'])
def location_select():
    location_id = request.form.get('location_id') or (request.json and request.json.get('location_id'))
    if not location_id:
        return jsonify({'success': False, 'error': 'Missing location_id'})
    location_id = int(location_id)

    saved_locations = read_saved_locations()
    locations = read_locations()

    if any(loc['location_id'] == location_id for loc in saved_locations):
        return jsonify({'success': True})

    if location_id not in locations:
        return jsonify({'success': False, 'error': 'Invalid location_id'})

    saved_locations.append({
        'saved_id': None,
        'user_id': USER_ID,
        'location_id': location_id,
        'location_name': locations[location_id]['location_name'],
        'is_default': False
    })

    write_saved_locations(saved_locations)

    return jsonify({'success': True})


@app.route('/locations/remove', methods=['POST'])
def location_remove():
    location_id = request.form.get('location_id') or (request.json and request.json.get('location_id'))
    if not location_id:
        return jsonify({'success': False, 'error': 'Missing location_id'})
    location_id = int(location_id)

    saved_locations = read_saved_locations()
    new_saved = [loc for loc in saved_locations if loc['location_id'] != location_id]

    write_saved_locations(new_saved)

    return jsonify({'success': True})


@app.route('/alerts')
def weather_alerts():
    location_id = request.args.get('location_id', type=int)
    severity = request.args.get('severity', '').strip().lower()

    alerts = read_alerts()
    locations = read_locations()
    filtered_alerts = []

    for alert in alerts:
        if alert['is_acknowledged']:
            continue
        if location_id is not None and alert['location_id'] != location_id:
            continue
        if severity and alert['severity'].lower() != severity:
            continue
        filtered_alerts.append(alert)

    return render_template('weather_alerts.html', alerts=filtered_alerts, locations=locations, selected_location_id=location_id, selected_severity=severity.capitalize())


@app.route('/alerts/acknowledge', methods=['POST'])
def acknowledge_alert():
    alert_id = request.form.get('alert_id') or (request.json and request.json.get('alert_id'))
    if not alert_id:
        return jsonify({'success': False, 'error': 'Missing alert_id'})
    alert_id = int(alert_id)

    alerts = read_alerts()
    found = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            found = True
            break

    if not found:
        return jsonify({'success': False, 'error': 'alert_id not found'})

    write_alerts(alerts)
    return jsonify({'success': True})


@app.route('/air_quality')
def air_quality_page():
    location_id = request.args.get('location_id', type=int)

    air_quality_data = read_air_quality()
    locations = read_locations()

    if location_id is not None:
        aqi = air_quality_data.get(location_id, None)
        air_quality = aqi if aqi else None
    else:
        air_quality = None

    if air_quality:
        index = air_quality['aqi_index']
        if index <= 50:
            air_quality['recommendation'] = 'Good air quality. Enjoy your outdoor activities.'
        elif index <= 100:
            air_quality['recommendation'] = 'Moderate air quality. Unusually sensitive individuals should consider limiting prolonged outdoor exertion.'
        elif index <= 150:
            air_quality['recommendation'] = 'Unhealthy for sensitive groups. Consider reducing prolonged or heavy exertion outdoors.'
        elif index <= 200:
            air_quality['recommendation'] = 'Unhealthy air quality. Everyone may begin to experience health effects; sensitive groups should avoid prolonged exertion.'
        elif index <= 300:
            air_quality['recommendation'] = 'Very unhealthy air quality. Avoid outdoor activities.'
        else:
            air_quality['recommendation'] = 'Hazardous air quality. Remain indoors and keep windows closed.'

    return render_template('air_quality.html', air_quality=air_quality, locations=locations, selected_location_id=location_id)


@app.route('/locations/saved')
def saved_locations_page():
    saved_locations = read_saved_locations()
    current_weather = read_current_weather()

    locations_with_weather = []
    for loc in saved_locations:
        weather = current_weather.get(loc['location_id'], None)
        locations_with_weather.append({
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'temperature': weather['temperature'] if weather else None,
            'condition': weather['condition'] if weather else None,
        })

    return render_template('saved_locations.html', saved_locations=locations_with_weather)


@app.route('/settings')
def settings_page():
    settings = read_settings()
    locations = read_locations()
    saved_locations = read_saved_locations()

    return render_template('settings.html', settings=settings, locations=locations, saved_locations=saved_locations)


@app.route('/settings/save', methods=['POST'])
def settings_save():
    temperature_unit = request.form.get('temperature_unit') or (request.json and request.json.get('temperature_unit'))
    default_location_id = request.form.get('default_location_id') or (request.json and request.json.get('default_location_id'))
    alert_notifications_enabled = request.form.get('alert_notifications_enabled') or (request.json and request.json.get('alert_notifications_enabled'))

    if default_location_id is not None:
        try:
            default_location_id = int(default_location_id)
        except Exception:
            default_location_id = None
    alert_enabled = True
    if alert_notifications_enabled is not None:
        if str(alert_notifications_enabled) in ['0', 'false', 'False']:
            alert_enabled = False
        else:
            alert_enabled = True

    settings = read_settings()
    if temperature_unit in ['F', 'C']:
        settings['temperature_unit'] = temperature_unit
    if default_location_id is not None:
        settings['default_location_id'] = default_location_id
    settings['alert_notifications_enabled'] = alert_enabled

    write_settings(settings)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
