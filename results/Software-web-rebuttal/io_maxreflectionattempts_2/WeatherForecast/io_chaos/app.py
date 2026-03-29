from flask import Flask, render_template, redirect, url_for, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading helper functions

def load_current_weather():
    current_weather = {}
    filepath = 'data/current_weather.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        location_id = int(parts[0])
                        temperature = float(parts[2]) if '.' in parts[2] else int(parts[2])
                        humidity = int(parts[4])
                        wind_speed = float(parts[5]) if '.' in parts[5] else int(parts[5])
                        current_weather[location_id] = {
                            'location_id': location_id,
                            'location_name': parts[1],
                            'temperature': temperature,
                            'condition': parts[3],
                            'humidity': humidity,
                            'wind_speed': wind_speed,
                            'last_updated': parts[6]
                        }
        except Exception:
            pass
    return current_weather


def load_forecasts():
    forecasts = []
    filepath = 'data/forecasts.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        forecasts.append({
                            'forecast_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'date': parts[2],
                            'high_temp': float(parts[3]) if '.' in parts[3] else int(parts[3]),
                            'low_temp': float(parts[4]) if '.' in parts[4] else int(parts[4]),
                            'condition': parts[5],
                            'precipitation': int(parts[6]),
                            'humidity': int(parts[7])
                        })
        except Exception:
            pass
    return forecasts


def load_locations():
    locations = []
    filepath = 'data/locations.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 6:
                        locations.append({
                            'location_id': int(parts[0]),
                            'location_name': parts[1],
                            'latitude': float(parts[2]),
                            'longitude': float(parts[3]),
                            'country': parts[4],
                            'timezone': parts[5]
                        })
        except Exception:
            pass
    return locations


def load_alerts():
    alerts = []
    filepath = 'data/alerts.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        alerts.append({
                            'alert_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'alert_type': parts[2],
                            'severity': parts[3],
                            'description': parts[4],
                            'start_time': parts[5],
                            'end_time': parts[6],
                            'is_acknowledged': parts[7] == '1'
                        })
        except Exception:
            pass
    return alerts


def load_air_quality():
    aqi_list = []
    filepath = 'data/air_quality.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        aqi_list.append({
                            'aqi_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'aqi_index': int(parts[2]),
                            'pm25': float(parts[3]),
                            'pm10': float(parts[4]),
                            'no2': float(parts[5]),
                            'o3': float(parts[6]),
                            'last_updated': parts[7]
                        })
        except Exception:
            pass
    return aqi_list


def load_saved_locations(user_id=1):
    saved = []
    filepath = 'data/saved_locations.txt'
    if os.path.isfile(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 5:
                        saved_id = int(parts[0])
                        uid = int(parts[1])
                        if uid == user_id:
                            saved.append({
                                'saved_id': saved_id,
                                'user_id': uid,
                                'location_id': int(parts[2]),
                                'location_name': parts[3],
                                'is_default': parts[4] == '1'
                            })
        except Exception:
            pass
    return saved


# Flask Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    saved_locations = load_saved_locations()
    current_weather = load_current_weather()
    default_location = None

    for sl in saved_locations:
        if sl['is_default']:
            loc_id = sl['location_id']
            if loc_id in current_weather:
                cw = current_weather[loc_id]
                default_location = {
                    'location_id': cw['location_id'],
                    'location_name': cw['location_name'],
                    'temperature': cw['temperature'],
                    'condition': cw['condition']
                }
                break

    if default_location is None and saved_locations:
        for sl in saved_locations:
            loc_id = sl['location_id']
            if loc_id in current_weather:
                cw = current_weather[loc_id]
                default_location = {
                    'location_id': cw['location_id'],
                    'location_name': cw['location_name'],
                    'temperature': cw['temperature'],
                    'condition': cw['condition']
                }
                break

    if default_location is None:
        default_location = {
            'location_id': None,
            'location_name': '',
            'temperature': None,
            'condition': ''
        }

    return render_template('dashboard.html', default_location=default_location)


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weather = load_current_weather()
    locations = load_locations()

    location_name = ''
    for loc in locations:
        if loc['location_id'] == location_id:
            location_name = loc['location_name']
            break

    location = {
        'location_id': location_id,
        'location_name': location_name
    }

    if location_id in current_weather:
        cw = current_weather[location_id]
        weather = {
            'temperature': cw['temperature'],
            'condition': cw['condition'],
            'humidity': cw['humidity'],
            'wind_speed': cw['wind_speed']
        }
    else:
        weather = {
            'temperature': None,
            'condition': '',
            'humidity': None,
            'wind_speed': None
        }

    return render_template('current_weather.html', location=location, weather=weather)


@app.route('/forecast')
def weekly_forecast():
    locations = load_locations()
    forecasts = load_forecasts()

    selected_location_id = request.args.get('location_id', type=int)

    # Prepare locations list
    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    forecast_list = []
    for fc in forecasts:
        if selected_location_id is None or fc['location_id'] == selected_location_id:
            forecast_list.append({
                'date': fc['date'],
                'high_temp': fc['high_temp'],
                'low_temp': fc['low_temp'],
                'condition': fc['condition']
            })

    return render_template('forecast.html', locations=locations_list, selected_location_id=selected_location_id, forecast_list=forecast_list)


@app.route('/locations/search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locations_raw = load_saved_locations()
    saved_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in saved_locations_raw]

    search_query = None
    search_results = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            sq = search_query.lower()
            for loc in locations:
                if sq in loc['location_name'].lower():
                    search_results.append({'location_id': loc['location_id'], 'location_name': loc['location_name']})

    return render_template('location_search.html', search_query=search_query, search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts')
def alerts():
    alerts_data = load_alerts()
    locations = load_locations()
    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    severity_filter = request.args.get('severity_filter', default='')
    location_filter_raw = request.args.get('location_filter')
    try:
        location_filter = int(location_filter_raw) if location_filter_raw is not None else None
    except ValueError:
        location_filter = None

    filtered_alerts = []
    for alert in alerts_data:
        if severity_filter and alert['severity'] != severity_filter:
            continue
        if location_filter is not None and alert['location_id'] != location_filter:
            continue
        filtered_alerts.append(alert)

    return render_template('alerts.html', alerts_list=filtered_alerts, severity_filter=severity_filter, location_filter=location_filter, locations=locations_list)


@app.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    # In real implementation, update storage to mark alert as acknowledged
    # Here simulate success
    return jsonify({'status': 'success'})


@app.route('/air_quality')
def air_quality():
    locations = load_locations()
    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]
    aqi_entries = load_air_quality()

    selected_location_id_raw = request.args.get('location_id')
    try:
        selected_location_id = int(selected_location_id_raw) if selected_location_id_raw is not None else None
    except ValueError:
        selected_location_id = None

    aqi_data = {
        'aqi_index': None,
        'aqi_description': '',
        'pm25': None,
        'pm10': None,
        'no2': None,
        'o3': None,
        'health_recommendation': ''
    }

    aqi_entry = None
    for entry in aqi_entries:
        if selected_location_id is not None and entry['location_id'] == selected_location_id:
            aqi_entry = entry
            break

    if aqi_entry:
        idx = aqi_entry['aqi_index']
        if idx <= 50:
            desc = 'Good'
            rec = 'Air quality is satisfactory.'
        elif idx <= 100:
            desc = 'Moderate'
            rec = 'Air quality is acceptable.'
        elif idx <= 150:
            desc = 'Unhealthy for Sensitive Groups'
            rec = 'Sensitive groups should reduce outdoor exertion.'
        elif idx <= 200:
            desc = 'Unhealthy'
            rec = 'Everyone may begin to experience health effects.'
        elif idx <= 300:
            desc = 'Very Unhealthy'
            rec = 'Health warnings of emergency conditions.'
        else:
            desc = 'Hazardous'
            rec = 'Everyone should avoid outdoor activities.'

        aqi_data = {
            'aqi_index': aqi_entry['aqi_index'],
            'aqi_description': desc,
            'pm25': aqi_entry['pm25'],
            'pm10': aqi_entry['pm10'],
            'no2': aqi_entry['no2'],
            'o3': aqi_entry['o3'],
            'health_recommendation': rec
        }

    return render_template('air_quality.html', locations=locations_list, selected_location_id=selected_location_id, aqi_data=aqi_data)


@app.route('/locations/saved')
def saved_locations():
    saved_locs = load_saved_locations()
    current_w = load_current_weather()
    saved_locations_data = []
    for loc in saved_locs:
        loc_id = loc['location_id']
        if loc_id in current_w:
            cw = current_w[loc_id]
            saved_locations_data.append({
                'location_id': loc_id,
                'location_name': loc['location_name'],
                'temperature': cw['temperature'],
                'condition': cw['condition']
            })
        else:
            saved_locations_data.append({
                'location_id': loc_id,
                'location_name': loc['location_name'],
                'temperature': None,
                'condition': ''
            })
    return render_template('saved_locations.html', saved_locations=saved_locations_data)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    saved_locs = load_saved_locations()
    default_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in saved_locs]

    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
    current_unit = app.config.get('TEMPERATURE_UNIT', 'Celsius')
    current_default_location_id = None
    for loc in saved_locs:
        if loc['is_default']:
            current_default_location_id = loc['location_id']
            break

    alert_notifications_enabled = app.config.get('ALERT_NOTIFICATIONS_ENABLED', True)

    if request.method == 'POST':
        unit = request.form.get('temperature_unit')
        default_location_str = request.form.get('default_location')
        alert_enabled_str = request.form.get('alert_notifications')

        if unit in temperature_units:
            app.config['TEMPERATURE_UNIT'] = unit
            current_unit = unit

        try:
            default_loc_id = int(default_location_str) if default_location_str else None
        except ValueError:
            default_loc_id = None

        if default_loc_id is not None:
            # simulate update
            for loc in saved_locs:
                loc['is_default'] = (loc['location_id'] == default_loc_id)
            current_default_location_id = default_loc_id

        alert_notifications_enabled = (alert_enabled_str == 'on' or alert_enabled_str == '1')
        app.config['ALERT_NOTIFICATIONS_ENABLED'] = alert_notifications_enabled

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           current_unit=current_unit,
                           default_locations=default_locations,
                           current_default_location_id=current_default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
