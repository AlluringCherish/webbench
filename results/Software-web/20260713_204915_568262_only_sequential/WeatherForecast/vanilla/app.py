from flask import Flask, render_template, request, redirect, url_for
import os
import threading

app = Flask(__name__)
USER_ID = 1  # single user context
DATA_DIR = 'data'

# Thread lock for safe file writes
file_lock = threading.Lock()

# Helper function to parse boolean fields stored as 0/1

def parse_bool(value):
    return value == '1'

# Load current weather data from current_weather.txt
# Fields: location_id|location_name|temperature|condition|humidity|wind_speed|last_updated


def load_current_weather():
    weather_data = {}
    path = os.path.join(DATA_DIR, 'current_weather.txt')
    if not os.path.exists(path):
        return weather_data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 7:
                continue
            location_id = int(parts[0])
            location_name = parts[1]
            temperature = int(parts[2])
            condition = parts[3]
            humidity = int(parts[4])
            wind_speed = int(parts[5])
            last_updated = parts[6]
            weather_data[location_id] = {
                'location_id': location_id,
                'location_name': location_name,
                'temperature': temperature,
                'condition': condition,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'last_updated': last_updated
            }
    return weather_data


# Load all locations from locations.txt
# Fields: location_id|location_name|latitude|longitude|country|timezone

def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            location_id = int(parts[0])
            location_name = parts[1]
            latitude = float(parts[2])
            longitude = float(parts[3])
            country = parts[4]
            timezone = parts[5]
            locations.append({
                'location_id': location_id,
                'location_name': location_name,
                'latitude': latitude,
                'longitude': longitude,
                'country': country,
                'timezone': timezone
            })
    return locations

# Load forecasts from forecasts.txt
# Fields: forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity

def load_forecasts():
    forecasts = []
    path = os.path.join(DATA_DIR, 'forecasts.txt')
    if not os.path.exists(path):
        return forecasts
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            forecast_id = int(parts[0])
            location_id = int(parts[1])
            date = parts[2]
            high_temp = int(parts[3])
            low_temp = int(parts[4])
            condition = parts[5]
            precipitation = float(parts[6])
            humidity = int(parts[7])
            forecasts.append({
                'forecast_id': forecast_id,
                'location_id': location_id,
                'date': date,
                'high_temp': high_temp,
                'low_temp': low_temp,
                'condition': condition,
                'precipitation': precipitation,
                'humidity': humidity
            })
    return forecasts

# Load alerts from alerts.txt
# Fields: alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged

def load_alerts():
    alerts = []
    path = os.path.join(DATA_DIR, 'alerts.txt')
    if not os.path.exists(path):
        return alerts
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            alert_id = int(parts[0])
            location_id = int(parts[1])
            alert_type = parts[2]
            severity = parts[3]
            description = parts[4]
            start_time = parts[5]
            end_time = parts[6]
            is_acknowledged = parse_bool(parts[7])
            alerts.append({
                'alert_id': alert_id,
                'location_id': location_id,
                'alert_type': alert_type,
                'severity': severity,
                'description': description,
                'start_time': start_time,
                'end_time': end_time,
                'is_acknowledged': is_acknowledged
            })
    return alerts

# Save alerts back to alerts.txt
# Used to update is_acknowledged status

def save_alerts(alerts):
    path = os.path.join(DATA_DIR, 'alerts.txt')
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for alert in alerts:
                line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{int(alert['is_acknowledged'])}\n"
                f.write(line)

# Load air quality data from air_quality.txt
# Fields: aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated

def load_air_quality():
    aqi_list = []
    path = os.path.join(DATA_DIR, 'air_quality.txt')
    if not os.path.exists(path):
        return aqi_list
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            aqi_id = int(parts[0])
            location_id = int(parts[1])
            aqi_index = int(parts[2])
            pm25 = float(parts[3])
            pm10 = float(parts[4])
            no2 = float(parts[5])
            o3 = float(parts[6])
            last_updated = parts[7]
            aqi_list.append({
                'aqi_id': aqi_id,
                'location_id': location_id,
                'aqi_index': aqi_index,
                'pm25': pm25,
                'pm10': pm10,
                'no2': no2,
                'o3': o3,
                'last_updated': last_updated
            })
    return aqi_list

# Load saved locations for user from saved_locations.txt
# Fields: saved_id|user_id|location_id|location_name|is_default

def load_saved_locations(user_id):
    saved = []
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    if not os.path.exists(path):
        return saved
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
                continue
            saved_id = int(parts[0])
            uid = int(parts[1])
            if uid != user_id:
                continue
            location_id = int(parts[2])
            location_name = parts[3]
            is_default = parse_bool(parts[4])
            saved.append({
                'saved_id': saved_id,
                'user_id': uid,
                'location_id': location_id,
                'location_name': location_name,
                'is_default': is_default
            })
    return saved

# Save saved locations list back to saved_locations.txt

def save_saved_locations(saved_list):
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    with file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for item in saved_list:
                line = f"{item['saved_id']}|{item['user_id']}|{item['location_id']}|{item['location_name']}|{int(item['is_default'])}\n"
                f.write(line)

@app.route('/')
def dashboard():
    weather_data = load_current_weather()
    saved_locs = load_saved_locations(USER_ID)
    # Determine default location
    default_location = next((loc for loc in saved_locs if loc['is_default']), None)
    if default_location:
        default_loc_id = default_location['location_id']
    elif weather_data:
        default_loc_id = next(iter(weather_data))
    else:
        default_loc_id = 1
    current_weather = weather_data.get(default_loc_id, {
        'location_id': default_loc_id,
        'location_name': 'Unknown',
        'temperature': 0,
        'condition': 'N/A',
        'humidity': 0,
        'wind_speed': 0
    })
    return render_template('dashboard.html', current_weather=current_weather, default_location_id=default_loc_id)

@app.route('/current_weather/<int:location_id>')
def current_weather(location_id):
    weather_data = load_current_weather()
    weather = weather_data.get(location_id, {
        'location_name': 'Unknown',
        'temperature': 0,
        'condition': 'N/A',
        'humidity': 0,
        'wind_speed': 0
    })
    return render_template('current_weather.html', weather=weather)

@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    if request.method == 'POST':
        selected_location_id = int(request.form.get('location-filter', 1))
    else:
        selected_location_id = 1

    forecasts = load_forecasts()
    filtered_forecasts = [f for f in forecasts if f['location_id'] == selected_location_id]

    locations = load_locations()

    return render_template('weekly_forecast.html', locations=locations, selected_location_id=selected_location_id, forecasts=filtered_forecasts)

@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    if request.method == 'POST':
        search_query = request.form.get('location-search-input', '').strip().lower()
        if search_query:
            search_results = [
                {
                    'location_id': loc['location_id'],
                    'location_name': loc['location_name'],
                    'country': loc['country']
                } for loc in locations if search_query in loc['location_name'].lower()
            ]
        else:
            search_results = []
    else:
        search_query = ''
        search_results = []

    saved_locations = load_saved_locations(USER_ID)

    # Handle add location POST action
    if request.method == 'POST' and 'add_location_id' in request.form and 'add_location_name' in request.form:
        try:
            add_location_id = int(request.form.get('add_location_id', 0))
            add_location_name = request.form.get('add_location_name', '').strip()
            # Prevent adding duplicates
            saved_locs = load_saved_locations(USER_ID)
            if add_location_id and add_location_name and not any(loc['location_id'] == add_location_id for loc in saved_locs):
                max_id = max((loc['saved_id'] for loc in saved_locs), default=0)
                new_entry = {
                    'saved_id': max_id + 1,
                    'user_id': USER_ID,
                    'location_id': add_location_id,
                    'location_name': add_location_name,
                    'is_default': False
                }
                saved_locs.append(new_entry)
                save_saved_locations(saved_locs)
                saved_locations = saved_locs
        except Exception:
            pass

    return render_template('location_search.html', search_query=search_query, search_results=search_results, saved_locations=saved_locations)

@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = load_alerts()
    locations = load_locations()

    selected_severity = None
    selected_location_id = None

    if request.method == 'POST':
        form = request.form

        # Check for acknowledgement request (button click) by checking if form has alert acknowledge buttons
        acknowledge_id = None
        for key in form.keys():
            if key.startswith('acknowledge-alert-button-'):
                try:
                    acknowledge_id = int(key.replace('acknowledge-alert-button-', ''))
                except ValueError:
                    continue

        if acknowledge_id is not None:
            # Mark the alert as acknowledged
            for alert in alerts:
                if alert['alert_id'] == acknowledge_id:
                    alert['is_acknowledged'] = True
                    break
            save_alerts(alerts)

        selected_severity = form.get('severity-filter', None) or None
        location_str = form.get('location-filter-alerts', None)
        if location_str:
            try:
                selected_location_id = int(location_str)
            except ValueError:
                selected_location_id = None

    # Filter alerts by severity and location
    filtered_alerts = alerts
    if selected_severity:
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == selected_severity.lower()]
    if selected_location_id is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == selected_location_id]

    # Map location names for alerts if missing
    loc_map = {loc['location_id']: loc['location_name'] for loc in locations}
    for alert in filtered_alerts:
        if 'location_name' not in alert or not alert['location_name']:
            alert['location_name'] = loc_map.get(alert['location_id'], 'Unknown')

    return render_template('weather_alerts.html', alerts=filtered_alerts, location_options=locations, selected_severity=selected_severity, selected_location_id=selected_location_id)

@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = load_locations()
    if request.method == 'POST':
        selected_location_id = int(request.form.get('location-aqi-filter', 1))
    else:
        selected_location_id = 1

    aqi_list = load_air_quality()
    aqi_data = next((a for a in aqi_list if a['location_id'] == selected_location_id), None)
    if aqi_data is None:
        aqi_data = {
            'aqi_index': 0,
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }

    # Simple health advice based on AQI index
    aqi_index = aqi_data['aqi_index']
    if aqi_index <= 50:
        health_advice = 'Air quality is good. No precautions necessary.'
    elif aqi_index <= 100:
        health_advice = 'Air quality is moderate. Sensitive groups should reduce outdoor activity.'
    elif aqi_index <= 150:
        health_advice = 'Unhealthy for sensitive groups. Consider limiting prolonged outdoor exertion.'
    elif aqi_index <= 200:
        health_advice = 'Unhealthy. Everyone should reduce prolonged outdoor exertion.'
    elif aqi_index <= 300:
        health_advice = 'Very unhealthy. Avoid outdoor activities.'
    else:
        health_advice = 'Hazardous air quality. Stay indoors and keep windows closed.'

    return render_template('air_quality.html', locations=locations, selected_location_id=selected_location_id, aqi_data=aqi_data, health_advice=health_advice)

@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    saved_locs = load_saved_locations(USER_ID)

    if request.method == 'POST':
        form = request.form

        # Handle add new location action
        if 'add_new_location' in form:
            # Find max saved_id to increment
            max_id = max((loc['saved_id'] for loc in saved_locs), default=0)
            # Retrieve new location_id and name from form (assuming provided)
            try:
                new_location_id = int(form.get('new_location_id', 0))
                new_location_name = form.get('new_location_name', '').strip()
            except Exception:
                new_location_id = 0
                new_location_name = ''
            if new_location_id and new_location_name:
                # If no saved locations exist, set new as default
                is_default = not any(loc['is_default'] for loc in saved_locs)
                new_entry = {
                    'saved_id': max_id + 1,
                    'user_id': USER_ID,
                    'location_id': new_location_id,
                    'location_name': new_location_name,
                    'is_default': is_default
                }
                saved_locs.append(new_entry)
                save_saved_locations(saved_locs)

        # Handle remove location action
        for key in form.keys():
            if key.startswith('remove_location_button_'):
                try:
                    remove_id = int(key.replace('remove_location_button_', ''))
                except ValueError:
                    remove_id = None
                if remove_id is not None:
                    saved_locs = [loc for loc in saved_locs if loc['location_id'] != remove_id]
                    # Ensure one default exists
                    if not any(loc['is_default'] for loc in saved_locs) and saved_locs:
                        saved_locs[0]['is_default'] = True
                    save_saved_locations(saved_locs)
                    break

        # TODO: Other POST actions can be added here

    return render_template('saved_locations.html', saved_locations=saved_locs)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = load_locations()
    saved_locs = load_saved_locations(USER_ID)

    # Default settings fallback
    temperature_unit = 'F'
    alert_notifications_enabled = True

    # Determine default location id
    default_location = next((loc for loc in saved_locs if loc['is_default']), None)
    if default_location:
        default_location_id = default_location['location_id']
    elif locations:
        default_location_id = locations[0]['location_id']
    else:
        default_location_id = 1

    if request.method == 'POST':
        form = request.form

        temperature_unit = form.get('temperature-unit-select', 'F')
        default_location_id = int(form.get('default-location-select', default_location_id))
        alert_notifications_enabled = 'alert-notifications-toggle' in form

        # Save settings in a local file (not detailed in spec, but we simulate persistence)
        settings_path = os.path.join(DATA_DIR, 'settings.txt')
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(f"temperature_unit|{temperature_unit}\n")
            f.write(f"default_location_id|{default_location_id}\n")
            f.write(f"alert_notifications_enabled|{int(alert_notifications_enabled)}\n")

    else:
        # Load settings if file exists
        settings_path = os.path.join(DATA_DIR, 'settings.txt')
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        key, val = line.split('|', 1)
                        if key == 'temperature_unit':
                            temperature_unit = val
                        elif key == 'default_location_id':
                            default_location_id = int(val)
                        elif key == 'alert_notifications_enabled':
                            alert_notifications_enabled = parse_bool(val)
            except Exception:
                pass

    return render_template('settings.html', temperature_unit=temperature_unit, locations=locations, default_location_id=default_location_id, alert_notifications_enabled=alert_notifications_enabled)

if __name__ == '__main__':
    app.run(debug=True)
