'''
Main backend application for WeatherForecast web application.
Handles routing, data reading/writing from/to local text files in the data/ directory,
business logic, and rendering HTML templates.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read/write data files
def read_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    weather_data = []
    if not os.path.exists(filepath):
        return weather_data
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if not os.path.exists(filepath):
        return forecasts
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    if not os.path.exists(filepath):
        return locations
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if not os.path.exists(filepath):
        return alerts
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'air_quality.txt')
    aqi_data = []
    if not os.path.exists(filepath):
        return aqi_data
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    if not os.path.exists(filepath):
        return saved_locations
    with open(filepath, 'r', encoding='utf-8') as f:
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
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
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
    # Settings are not specified to be stored in a file in requirements.
    # We'll store settings in a file 'settings.txt' in data directory with format:
    # temperature_unit|default_location_id|alert_notifications_enabled
    filepath = os.path.join(DATA_DIR, 'settings.txt')
    default_settings = {
        'temperature_unit': 'Celsius',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }
    if not os.path.exists(filepath):
        return default_settings
    with open(filepath, 'r', encoding='utf-8') as f:
        line = f.readline().strip()
        if not line:
            return default_settings
        parts = line.split('|')
        if len(parts) != 3:
            return default_settings
        temperature_unit, default_location_id, alert_notifications_enabled = parts
        return {
            'temperature_unit': temperature_unit,
            'default_location_id': int(default_location_id) if default_location_id.isdigit() else None,
            'alert_notifications_enabled': alert_notifications_enabled == '1'
        }
def write_settings(settings):
    filepath = os.path.join(DATA_DIR, 'settings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        line = '|'.join([
            settings.get('temperature_unit', 'Celsius'),
            str(settings.get('default_location_id', '')) if settings.get('default_location_id') is not None else '',
            '1' if settings.get('alert_notifications_enabled', True) else '0'
        ])
        f.write(line + '\n')
# Helper functions
def get_default_location_id():
    settings = read_settings()
    if settings['default_location_id'] is not None:
        return settings['default_location_id']
    # If no default set, fallback to first saved location if any
    saved_locations = read_saved_locations()
    for loc in saved_locations:
        if loc['is_default']:
            return loc['location_id']
    # If no saved location default, fallback to first location in locations.txt
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
def get_saved_locations_by_user(user_id=1):
    # Since no authentication, assume user_id=1 for all
    saved_locations = read_saved_locations()
    return [loc for loc in saved_locations if loc['user_id'] == user_id]
def get_next_saved_id_for_saved_locations():
    saved_locations = read_saved_locations()
    if not saved_locations:
        return 1
    return max(loc['saved_id'] for loc in saved_locations) + 1
def get_next_alert_id():
    alerts = read_alerts()
    if not alerts:
        return 1
    return max(alert['alert_id'] for alert in alerts) + 1
def get_next_forecast_id():
    forecasts = read_forecasts()
    if not forecasts:
        return 1
    return max(forecast['forecast_id'] for forecast in forecasts) + 1
# AQI description and health recommendation helpers
def aqi_description(aqi_index):
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
def health_recommendation(aqi_index):
    if aqi_index <= 50:
        return "Air quality is satisfactory, and air pollution poses little or no risk."
    elif aqi_index <= 100:
        return "Air quality is acceptable; some pollutants may be a moderate health concern for a very small number of people."
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
    default_location_id = settings['default_location_id']
    if default_location_id is None:
        default_location_id = get_default_location_id()
    current_weather = get_current_weather_by_location(default_location_id)
    saved_locations = get_saved_locations_by_user()
    return render_template('dashboard.html',
                           current_weather_summary=current_weather,
                           saved_locations=saved_locations)
@app.route('/current_weather')
def current_weather_page():
    location_id = request.args.get('location_id', type=int)
    if location_id is None:
        location_id = get_default_location_id()
    weather = get_current_weather_by_location(location_id)
    location = get_location_by_id(location_id)
    if weather is None or location is None:
        return "Location or weather data not found", 404
    return render_template('current_weather.html',
                           location_name=location['location_name'],
                           temperature=weather['temperature'],
                           condition=weather['condition'],
                           humidity=weather['humidity'],
                           wind_speed=weather['wind_speed'])
@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    locations = read_locations()
    selected_location_id = request.args.get('location_id', type=int)
    if request.method == 'POST':
        selected_location_id = request.form.get('location-filter', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']
    forecasts = get_forecasts_by_location(selected_location_id) if selected_location_id else []
    # Sort forecasts by date ascending
    forecasts.sort(key=lambda f: f['date'])
    return render_template('weekly_forecast.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           forecasts=forecasts)
@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = read_locations()
    saved_locations = get_saved_locations_by_user()
    search_results = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('location-search-input', '').strip().lower()
        if query:
            # Search by city name or coordinates (latitude,longitude)
            for loc in locations:
                if query in loc['location_name'].lower():
                    search_results.append(loc)
                else:
                    # Try to parse coordinates query
                    if ',' in query:
                        parts = query.split(',')
                        if len(parts) == 2:
                            try:
                                lat_q = float(parts[0].strip())
                                lon_q = float(parts[1].strip())
                                # Match if coordinates are close (within 0.1 degree)
                                if abs(loc['latitude'] - lat_q) < 0.1 and abs(loc['longitude'] - lon_q) < 0.1:
                                    search_results.append(loc)
                            except ValueError:
                                pass
    return render_template('location_search.html',
                           search_results=search_results,
                           saved_locations=saved_locations,
                           query=query)
@app.route('/select_location/<int:location_id>', methods=['POST'])
def select_location(location_id):
    # Add location to saved_locations.txt for user_id=1 if not already saved
    saved_locations = get_saved_locations_by_user()
    for loc in saved_locations:
        if loc['location_id'] == location_id:
            # Already saved
            break
    else:
        # Add new saved location
        locations = read_locations()
        location = next((l for l in locations if l['location_id'] == location_id), None)
        if location is None:
            return "Location not found", 404
        new_saved_id = get_next_saved_id_for_saved_locations()
        saved_locations.append({
            'saved_id': new_saved_id,
            'user_id': 1,
            'location_id': location_id,
            'location_name': location['location_name'],
            'is_default': False
        })
        write_saved_locations(saved_locations)
    return redirect(url_for('location_search'))
@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    locations = read_locations()
    alerts = read_alerts()
    selected_location_id = request.args.get('location_id', type=int)
    selected_severity = request.args.get('severity', 'All')
    if request.method == 'POST':
        selected_location_id = request.form.get('location-filter-alerts', type=int)
        selected_severity = request.form.get('severity-filter', 'All')
    # Filter alerts by location
    if selected_location_id:
        alerts = [a for a in alerts if a['location_id'] == selected_location_id]
    # Filter alerts by severity
    if selected_severity != 'All':
        alerts = [a for a in alerts if a['severity'].lower() == selected_severity.lower()]
    # Attach location names to alerts
    loc_dict = {loc['location_id']: loc['location_name'] for loc in locations}
    for alert in alerts:
        alert['location_name'] = loc_dict.get(alert['location_id'], 'Unknown')
    return render_template('weather_alerts.html',
                           locations=locations,
                           alerts=alerts,
                           selected_location_id=selected_location_id,
                           selected_severity=selected_severity)
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
    else:
        return "Alert not found", 404
@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = read_locations()
    selected_location_id = request.args.get('location_id', type=int)
    if request.method == 'POST':
        selected_location_id = request.form.get('location-aqi-filter', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']
    aqi = get_air_quality_by_location(selected_location_id) if selected_location_id else None
    if aqi:
        aqi_desc = aqi_description(aqi['aqi_index'])
        health_rec = health_recommendation(aqi['aqi_index'])
    else:
        aqi_desc = None
        health_rec = None
    return render_template('air_quality.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           aqi=aqi,
                           aqi_description=aqi_desc,
                           health_recommendation=health_rec)
@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    saved_locs = get_saved_locations_by_user()
    locations = read_locations()
    # Attach current weather info to saved locations
    current_weather_data = read_current_weather()
    weather_dict = {w['location_id']: w for w in current_weather_data}
    for loc in saved_locs:
        weather = weather_dict.get(loc['location_id'])
        if weather:
            loc['temperature'] = weather['temperature']
            loc['condition'] = weather['condition']
        else:
            loc['temperature'] = None
            loc['condition'] = None
    return render_template('saved_locations.html',
                           saved_locations=saved_locs)
@app.route('/view_location_weather/<int:location_id>')
def view_location_weather(location_id):
    # Redirect to current weather page for the location
    return redirect(url_for('current_weather_page', location_id=location_id))
@app.route('/remove_location/<int:location_id>', methods=['POST'])
def remove_location(location_id):
    saved_locs = get_saved_locations_by_user()
    saved_locs = [loc for loc in saved_locs if loc['location_id'] != location_id]
    # Rewrite saved_locations.txt with remaining locations
    # We must preserve other users' saved locations if any, but since no auth, assume user_id=1 only
    # So just write back saved_locs with user_id=1
    write_saved_locations(saved_locs)
    return redirect(url_for('saved_locations'))
@app.route('/add_new_location', methods=['GET'])
def add_new_location():
    # Redirect to location search page to add new location
    return redirect(url_for('location_search'))
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = read_locations()
    settings = read_settings()
    if request.method == 'POST':
        temperature_unit = request.form.get('temperature-unit-select', 'Celsius')
        default_location_id = request.form.get('default-location-select')
        alert_notifications_enabled = request.form.get('alert-notifications-toggle')
        # Validate default_location_id
        try:
            default_location_id = int(default_location_id)
        except (ValueError, TypeError):
            default_location_id = None
        alert_notifications_enabled = True if alert_notifications_enabled == 'on' else False
        settings = {
            'temperature_unit': temperature_unit,
            'default_location_id': default_location_id,
            'alert_notifications_enabled': alert_notifications_enabled
        }
        write_settings(settings)
        return redirect(url_for('dashboard'))
    return render_template('settings.html',
                           settings=settings,
                           locations=locations)
@app.route('/back_to_dashboard', methods=['GET', 'POST'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000, debug=True)