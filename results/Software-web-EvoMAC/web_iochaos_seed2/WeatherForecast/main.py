'''
Main backend Python file for the WeatherForecast web application.
Implements routing for all pages, reads/writes data from/to local text files,
processes user inputs, and serves HTML templates.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read and write data files
def read_current_weather():
    path = os.path.join(DATA_DIR, 'current_weather.txt')
    weather_data = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                location_id, location_name, temperature, condition, humidity, wind_speed, last_updated = parts
                weather_data.append({
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'temperature': float(temperature),
                    'condition': condition,
                    'humidity': int(humidity),
                    'wind_speed': float(wind_speed),
                    'last_updated': last_updated
                })
    return weather_data
def read_forecasts():
    path = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                forecast_id, location_id, date, high_temp, low_temp, condition, precipitation, humidity = parts
                forecasts.append({
                    'forecast_id': int(forecast_id),
                    'location_id': int(location_id),
                    'date': date,
                    'high_temp': float(high_temp),
                    'low_temp': float(low_temp),
                    'condition': condition,
                    'precipitation': float(precipitation),
                    'humidity': int(humidity)
                })
    return forecasts
def read_locations():
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                location_id, location_name, latitude, longitude, country, timezone = parts
                locations.append({
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'country': country,
                    'timezone': timezone
                })
    return locations
def read_alerts():
    path = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                alert_id, location_id, alert_type, severity, description, start_time, end_time, is_acknowledged = parts
                alerts.append({
                    'alert_id': int(alert_id),
                    'location_id': int(location_id),
                    'alert_type': alert_type,
                    'severity': severity,
                    'description': description,
                    'start_time': start_time,
                    'end_time': end_time,
                    'is_acknowledged': is_acknowledged == '1'
                })
    return alerts
def write_alerts(alerts):
    path = os.path.join(DATA_DIR, 'alerts.txt')
    with open(path, 'w', encoding='utf-8') as f:
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
            f.write(line + '\n')
def read_air_quality():
    path = os.path.join(DATA_DIR, 'air_quality.txt')
    aqi_data = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                aqi_id, location_id, aqi_index, pm25, pm10, no2, o3, last_updated = parts
                aqi_data.append({
                    'aqi_id': int(aqi_id),
                    'location_id': int(location_id),
                    'aqi_index': int(aqi_index),
                    'pm25': float(pm25),
                    'pm10': float(pm10),
                    'no2': float(no2),
                    'o3': float(o3),
                    'last_updated': last_updated
                })
    return aqi_data
def read_saved_locations():
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                saved_id, user_id, location_id, location_name, is_default = parts
                saved_locations.append({
                    'saved_id': int(saved_id),
                    'user_id': int(user_id),
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'is_default': is_default == '1'
                })
    return saved_locations
def write_saved_locations(saved_locations):
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for loc in saved_locations:
            line = '|'.join([
                str(loc['saved_id']),
                str(loc['user_id']),
                str(loc['location_id']),
                loc['location_name'],
                '1' if loc['is_default'] else '0'
            ])
            f.write(line + '\n')
def read_settings():
    # Settings are not specified to be stored in a file in the requirements.
    # We'll store settings in a simple text file 'settings.txt' in key=value format.
    path = os.path.join(DATA_DIR, 'settings.txt')
    settings = {
        'temperature_unit': 'Celsius',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'temperature_unit':
                        if value in ['Celsius', 'Fahrenheit', 'Kelvin']:
                            settings['temperature_unit'] = value
                    elif key == 'default_location_id':
                        try:
                            settings['default_location_id'] = int(value)
                        except:
                            settings['default_location_id'] = None
                    elif key == 'alert_notifications_enabled':
                        settings['alert_notifications_enabled'] = (value.lower() == 'true')
    return settings
def write_settings(settings):
    path = os.path.join(DATA_DIR, 'settings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"temperature_unit={settings.get('temperature_unit', 'Celsius')}\n")
        default_loc = settings.get('default_location_id')
        if default_loc is None:
            default_loc = ''
        f.write(f"default_location_id={default_loc}\n")
        f.write(f"alert_notifications_enabled={'True' if settings.get('alert_notifications_enabled', True) else 'False'}\n")
def convert_temperature(temp_celsius, unit):
    if unit == 'Celsius':
        return temp_celsius
    elif unit == 'Fahrenheit':
        return temp_celsius * 9/5 + 32
    elif unit == 'Kelvin':
        return temp_celsius + 273.15
    else:
        return temp_celsius
def format_temperature(temp, unit):
    if unit == 'Celsius':
        return f"{temp:.1f} °C"
    elif unit == 'Fahrenheit':
        return f"{temp:.1f} °F"
    elif unit == 'Kelvin':
        return f"{temp:.1f} K"
    else:
        return f"{temp:.1f}"
def get_default_location_id(saved_locations, settings):
    # Priority: settings default_location_id if valid and in saved_locations
    # else first saved location if any
    default_id = settings.get('default_location_id')
    saved_location_ids = [loc['location_id'] for loc in saved_locations]
    if default_id in saved_location_ids:
        return default_id
    if saved_location_ids:
        return saved_location_ids[0]
    # fallback: first location from locations.txt
    locations = read_locations()
    if locations:
        return locations[0]['location_id']
    return None
def get_location_by_id(location_id):
    locations = read_locations()
    for loc in locations:
        if loc['location_id'] == location_id:
            return loc
    return None
def get_current_weather_by_location(location_id):
    weather_data = read_current_weather()
    for w in weather_data:
        if w['location_id'] == location_id:
            return w
    return None
def get_forecasts_by_location(location_id):
    forecasts = read_forecasts()
    return [f for f in forecasts if f['location_id'] == location_id]
def get_alerts_by_location(location_id):
    alerts = read_alerts()
    return [a for a in alerts if a['location_id'] == location_id]
def get_air_quality_by_location(location_id):
    aqi_data = read_air_quality()
    for aqi in aqi_data:
        if aqi['location_id'] == location_id:
            return aqi
    return None
def get_weather_condition_description(condition):
    # Could be extended for better descriptions or icons
    return condition
def get_aqi_description(aqi_index):
    if aqi_index <= 50:
        return "Good"
    elif aqi_index <= 100:
        return "Moderate"
    elif aqi_index <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_index <= 200:
        return "Unhealthy"
    elif aqi_index <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
def get_health_recommendation(aqi_index):
    if aqi_index <= 50:
        return "Air quality is satisfactory, and air pollution poses little or no risk."
    elif aqi_index <= 100:
        return "Air quality is acceptable; however, some pollutants may be a moderate health concern for a very small number of people."
    elif aqi_index <= 150:
        return "Members of sensitive groups may experience health effects. General public is less likely to be affected."
    elif aqi_index <= 200:
        return "Everyone may begin to experience health effects; members of sensitive groups may experience more serious effects."
    elif aqi_index <= 300:
        return "Health alert: everyone may experience more serious health effects."
    else:
        return "Health warnings of emergency conditions. The entire population is more likely to be affected."
# Routes
@app.route('/')
def dashboard():
    settings = read_settings()
    saved_locations = read_saved_locations()
    default_location_id = get_default_location_id(saved_locations, settings)
    current_weather = get_current_weather_by_location(default_location_id)
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    if current_weather:
        temp_converted = convert_temperature(current_weather['temperature'], temperature_unit)
        current_weather_display = {
            'location_name': current_weather['location_name'],
            'temperature': format_temperature(temp_converted, temperature_unit),
            'condition': current_weather['condition'],
            'humidity': current_weather['humidity'],
            'wind_speed': current_weather['wind_speed'],
            'last_updated': current_weather['last_updated']
        }
    else:
        current_weather_display = None
    return render_template('dashboard.html',
                           current_weather=current_weather_display,
                           temperature_unit=temperature_unit)
@app.route('/current_weather')
def current_weather():
    location_id = request.args.get('location_id', type=int)
    settings = read_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    if location_id is None:
        # Use default location
        saved_locations = read_saved_locations()
        location_id = get_default_location_id(saved_locations, settings)
    location = get_location_by_id(location_id)
    if not location:
        return "Location not found", 404
    weather = get_current_weather_by_location(location_id)
    if not weather:
        # No weather data for location
        weather_display = None
    else:
        temp_converted = convert_temperature(weather['temperature'], temperature_unit)
        weather_display = {
            'temperature': format_temperature(temp_converted, temperature_unit),
            'condition': weather['condition'],
            'humidity': weather['humidity'],
            'wind_speed': weather['wind_speed']
        }
    return render_template('current_weather.html',
                           location_name=location['location_name'],
                           weather=weather_display,
                           temperature_unit=temperature_unit)
@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    settings = read_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    locations = read_locations()
    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('location_filter', type=int)
    else:
        # GET: try to get from query param
        selected_location_id = request.args.get('location_filter', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']
    forecasts = []
    if selected_location_id is not None:
        all_forecasts = get_forecasts_by_location(selected_location_id)
        # Sort by date ascending
        try:
            all_forecasts.sort(key=lambda f: datetime.strptime(f['date'], '%Y-%m-%d'))
        except Exception:
            pass
        for f in all_forecasts:
            high_temp = convert_temperature(f['high_temp'], temperature_unit)
            low_temp = convert_temperature(f['low_temp'], temperature_unit)
            forecasts.append({
                'date': f['date'],
                'high_temp': format_temperature(high_temp, temperature_unit),
                'low_temp': format_temperature(low_temp, temperature_unit),
                'condition': f['condition'],
                'precipitation': f['precipitation'],
                'humidity': f['humidity']
            })
    return render_template('weekly_forecast.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           forecasts=forecasts,
                           temperature_unit=temperature_unit)
@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = read_locations()
    saved_locations = read_saved_locations()
    search_query = ''
    search_results = []
    if request.method == 'POST':
        search_query = request.form.get('location_search_input', '').strip().lower()
        if search_query:
            # Search by city name or coordinates (latitude,longitude)
            for loc in locations:
                if search_query in loc['location_name'].lower():
                    search_results.append(loc)
                else:
                    # Check if query looks like coordinates "lat,lon"
                    if ',' in search_query:
                        parts = search_query.split(',')
                        if len(parts) == 2:
                            try:
                                lat_q = float(parts[0].strip())
                                lon_q = float(parts[1].strip())
                                # Match if coordinates are close (within 0.1 degree)
                                if abs(loc['latitude'] - lat_q) <= 0.1 and abs(loc['longitude'] - lon_q) <= 0.1:
                                    search_results.append(loc)
                            except ValueError:
                                pass
    return render_template('location_search.html',
                           locations=locations,
                           saved_locations=saved_locations,
                           search_query=search_query,
                           search_results=search_results)
@app.route('/select_location/<int:location_id>', methods=['POST'])
def select_location(location_id):
    # Add location to saved_locations.txt if not already saved
    locations = read_locations()
    saved_locations = read_saved_locations()
    location = get_location_by_id(location_id)
    if not location:
        return "Location not found", 404
    # Check if already saved for user_id=1 (since no auth, assume user_id=1)
    user_id = 1
    exists = any(sl['location_id'] == location_id and sl['user_id'] == user_id for sl in saved_locations)
    if not exists:
        new_id = 1
        if saved_locations:
            new_id = max(sl['saved_id'] for sl in saved_locations) + 1
        saved_locations.append({
            'saved_id': new_id,
            'user_id': user_id,
            'location_id': location_id,
            'location_name': location['location_name'],
            'is_default': False
        })
        write_saved_locations(saved_locations)
    return redirect(url_for('saved_locations_page'))
@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = read_alerts()
    locations = read_locations()
    severity_filter = 'All'
    location_filter = 'All'
    if request.method == 'POST':
        severity_filter = request.form.get('severity_filter', 'All')
        location_filter = request.form.get('location_filter_alerts', 'All')
    else:
        severity_filter = request.args.get('severity_filter', 'All')
        location_filter = request.args.get('location_filter_alerts', 'All')
    filtered_alerts = []
    for alert in alerts:
        if severity_filter != 'All' and alert['severity'] != severity_filter:
            continue
        if location_filter != 'All' and str(alert['location_id']) != location_filter:
            continue
        filtered_alerts.append(alert)
    # Attach location names to alerts
    loc_dict = {loc['location_id']: loc['location_name'] for loc in locations}
    for alert in filtered_alerts:
        alert['location_name'] = loc_dict.get(alert['location_id'], 'Unknown')
    return render_template('weather_alerts.html',
                           alerts=filtered_alerts,
                           locations=locations,
                           severity_filter=severity_filter,
                           location_filter_alerts=location_filter)
@app.route('/acknowledge_alert/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = read_alerts()
    found = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            found = True
            break
    if found:
        write_alerts(alerts)
    return redirect(url_for('weather_alerts'))
@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    aqi_data = read_air_quality()
    locations = read_locations()
    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('location_aqi_filter', type=int)
    else:
        selected_location_id = request.args.get('location_aqi_filter', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']
    aqi_info = None
    if selected_location_id is not None:
        aqi = get_air_quality_by_location(selected_location_id)
        if aqi:
            aqi_desc = get_aqi_description(aqi['aqi_index'])
            health_rec = get_health_recommendation(aqi['aqi_index'])
            aqi_info = {
                'aqi_index': aqi['aqi_index'],
                'aqi_description': aqi_desc,
                'pm25': aqi['pm25'],
                'pm10': aqi['pm10'],
                'no2': aqi['no2'],
                'o3': aqi['o3'],
                'last_updated': aqi['last_updated'],
                'health_recommendation': health_rec
            }
    return render_template('air_quality.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           aqi_info=aqi_info)
@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations_page():
    saved_locations_data = read_saved_locations()
    current_weather = read_current_weather()
    temperature_unit = read_settings().get('temperature_unit', 'Celsius')
    # Build a dict for quick weather lookup by location_id
    weather_dict = {w['location_id']: w for w in current_weather}
    # Handle remove location action
    if request.method == 'POST':
        remove_id = request.form.get('remove_location_id', type=int)
        if remove_id is not None:
            saved_locations_data = [loc for loc in saved_locations_data if loc['location_id'] != remove_id]
            # If removed location was default, unset default or set another
            if not any(loc['is_default'] for loc in saved_locations_data):
                if saved_locations_data:
                    saved_locations_data[0]['is_default'] = True
            write_saved_locations(saved_locations_data)
            return redirect(url_for('saved_locations_page'))
    # Prepare display data
    display_locations = []
    for loc in saved_locations_data:
        weather = weather_dict.get(loc['location_id'])
        if weather:
            temp_converted = convert_temperature(weather['temperature'], temperature_unit)
            temp_display = format_temperature(temp_converted, temperature_unit)
            condition = weather['condition']
        else:
            temp_display = None
            condition = None
        display_locations.append({
            'saved_id': loc['saved_id'],
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'is_default': loc['is_default'],
            'temperature': temp_display,
            'condition': condition
        })
    return render_template('saved_locations.html',
                           saved_locations=display_locations,
                           temperature_unit=temperature_unit)
@app.route('/view_location_weather/<int:location_id>')
def view_location_weather(location_id):
    # Redirect to current_weather page for the location
    return redirect(url_for('current_weather', location_id=location_id))
@app.route('/add_new_location')
def add_new_location():
    # Redirect to location search page to add new location
    return redirect(url_for('location_search'))
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings = read_settings()
    locations = read_locations()
    if request.method == 'POST':
        temperature_unit = request.form.get('temperature_unit_select', 'Celsius')
        default_location_id = request.form.get('default_location_select', type=int)
        alert_notifications_enabled = request.form.get('alert_notifications_toggle') == 'on'
        # Validate temperature unit
        if temperature_unit not in ['Celsius', 'Fahrenheit', 'Kelvin']:
            temperature_unit = 'Celsius'
        # Validate default location id
        location_ids = [loc['location_id'] for loc in locations]
        if default_location_id not in location_ids:
            default_location_id = None
        settings['temperature_unit'] = temperature_unit
        settings['default_location_id'] = default_location_id
        settings['alert_notifications_enabled'] = alert_notifications_enabled
        write_settings(settings)
        # Also update saved_locations.txt to mark default location
        saved_locations = read_saved_locations()
        user_id = 1
        changed = False
        for loc in saved_locations:
            if loc['user_id'] == user_id:
                if loc['location_id'] == default_location_id:
                    if not loc['is_default']:
                        loc['is_default'] = True
                        changed = True
                else:
                    if loc['is_default']:
                        loc['is_default'] = False
                        changed = True
        if changed:
            write_saved_locations(saved_locations)
        return redirect(url_for('dashboard'))
    return render_template('settings.html',
                           settings=settings,
                           locations=locations)
if __name__ == '__main__':
    app.run(port=5000, debug=True)