'''
Main backend application for WeatherForecast web application.
Defines the root route '/' to serve the Dashboard page as the starting page,
loads default location current weather data from local text files,
and passes the data to the dashboard template.
Also defines routes for all other pages with necessary data loading and passing,
ensuring full operability and compliance with requirements.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
CURRENT_WEATHER_FILE = os.path.join(DATA_DIR, 'current_weather.txt')
SAVED_LOCATIONS_FILE = os.path.join(DATA_DIR, 'saved_locations.txt')
FORECASTS_FILE = os.path.join(DATA_DIR, 'forecasts.txt')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.txt')
ALERTS_FILE = os.path.join(DATA_DIR, 'alerts.txt')
AIR_QUALITY_FILE = os.path.join(DATA_DIR, 'air_quality.txt')
def load_current_weather():
    """
    Load current weather data from current_weather.txt into a dictionary keyed by location_id.
    """
    weather_data = {}
    if not os.path.exists(CURRENT_WEATHER_FILE):
        return weather_data
    with open(CURRENT_WEATHER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            location_id = parts[0]
            weather_data[location_id] = {
                'location_id': location_id,
                'location_name': parts[1],
                'temperature': parts[2],
                'condition': parts[3],
                'humidity': parts[4],
                'wind_speed': parts[5],
                'last_updated': parts[6]
            }
    return weather_data
def load_default_location_id():
    """
    Load the default location_id from saved_locations.txt for user_id=1 (assuming single user).
    If none marked default, return None.
    """
    if not os.path.exists(SAVED_LOCATIONS_FILE):
        return None
    with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            saved_id, user_id, location_id, location_name, is_default = parts
            if user_id == '1' and is_default == '1':
                return location_id
    return None
def load_locations():
    """
    Load all locations from locations.txt into a dictionary keyed by location_id.
    """
    locations = {}
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            location_id = parts[0]
            locations[location_id] = {
                'location_id': location_id,
                'location_name': parts[1],
                'latitude': parts[2],
                'longitude': parts[3],
                'country': parts[4],
                'timezone': parts[5]
            }
    return locations
def load_forecasts():
    """
    Load all forecasts from forecasts.txt into a list of dictionaries.
    """
    forecasts = []
    if not os.path.exists(FORECASTS_FILE):
        return forecasts
    with open(FORECASTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            forecast = {
                'forecast_id': parts[0],
                'location_id': parts[1],
                'date': parts[2],
                'high_temp': parts[3],
                'low_temp': parts[4],
                'condition': parts[5],
                'precipitation': parts[6],
                'humidity': parts[7]
            }
            forecasts.append(forecast)
    return forecasts
def load_saved_locations():
    """
    Load saved locations for user_id=1 from saved_locations.txt into a list.
    """
    saved_locations = []
    if not os.path.exists(SAVED_LOCATIONS_FILE):
        return saved_locations
    with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            saved_id, user_id, location_id, location_name, is_default = parts
            if user_id == '1':
                saved_locations.append({
                    'saved_id': saved_id,
                    'location_id': location_id,
                    'location_name': location_name,
                    'is_default': is_default
                })
    return saved_locations
def load_alerts():
    """
    Load all weather alerts from alerts.txt into a list of dictionaries.
    """
    alerts = []
    if not os.path.exists(ALERTS_FILE):
        return alerts
    with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            alert = {
                'alert_id': parts[0],
                'location_id': parts[1],
                'alert_type': parts[2],
                'severity': parts[3],
                'description': parts[4],
                'start_time': parts[5],
                'end_time': parts[6],
                'is_acknowledged': parts[7]
            }
            alerts.append(alert)
    return alerts
def load_air_quality():
    """
    Load all air quality data from air_quality.txt into a list of dictionaries.
    """
    air_quality = []
    if not os.path.exists(AIR_QUALITY_FILE):
        return air_quality
    with open(AIR_QUALITY_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            aqi = {
                'aqi_id': parts[0],
                'location_id': parts[1],
                'aqi_index': int(parts[2]),
                'pm25': parts[3],
                'pm10': parts[4],
                'no2': parts[5],
                'o3': parts[6],
                'last_updated': parts[7]
            }
            air_quality.append(aqi)
    return air_quality
@app.route('/')
def dashboard():
    """
    Route for the root URL '/' serving the Dashboard page.
    Loads current weather for the default location and passes it to the template.
    """
    weather_data = load_current_weather()
    default_location_id = load_default_location_id()
    default_location_weather = None
    if default_location_id and default_location_id in weather_data:
        default_location_weather = weather_data[default_location_id]
    else:
        # If no default location found, pick first available location weather if any
        if weather_data:
            default_location_weather = next(iter(weather_data.values()))
    return render_template('dashboard.html', weather_data=default_location_weather)
@app.route('/current_weather')
def current_weather():
    """
    Route for Current Weather page.
    Expects optional query parameter 'location_id' to specify location.
    If not provided, uses default location.
    Passes detailed current weather data to template.
    """
    location_id = request.args.get('location_id')
    weather_data = load_current_weather()
    default_location_id = load_default_location_id()
    if not location_id:
        location_id = default_location_id
    current_weather = None
    if location_id and location_id in weather_data:
        current_weather = weather_data[location_id]
    return render_template('current_weather.html', current_weather=current_weather)
@app.route('/weekly_forecast')
def weekly_forecast():
    """
    Route for Weekly Forecast page.
    Expects optional query parameter 'location_id' to filter forecast.
    If not provided, uses default location.
    Passes forecast list and locations for filter dropdown.
    """
    location_id = request.args.get('location_id')
    locations = load_locations()
    forecasts = load_forecasts()
    default_location_id = load_default_location_id()
    if not location_id:
        location_id = default_location_id
    filtered_forecasts = []
    if location_id:
        filtered_forecasts = [f for f in forecasts if f['location_id'] == location_id]
    return render_template('weekly_forecast.html', forecasts=filtered_forecasts, locations=locations, selected_location=location_id)
@app.route('/location_search')
def location_search():
    """
    Route for Location Search page.
    Supports optional query parameter 'query' to search locations by name or coordinates.
    Passes matching locations and saved locations to template.
    """
    query = request.args.get('query', '').strip().lower()
    locations = load_locations()
    saved_locations = load_saved_locations()
    matched_locations = []
    if query:
        for loc in locations.values():
            if query in loc['location_name'].lower() or query in loc['latitude'].lower() or query in loc['longitude'].lower():
                matched_locations.append(loc)
    else:
        matched_locations = list(locations.values())
    return render_template('location_search.html', search_results=matched_locations, saved_locations=saved_locations, query=query)
@app.route('/weather_alerts')
def weather_alerts():
    """
    Route for Weather Alerts page.
    Supports optional query parameters 'severity' and 'location_id' for filtering.
    Passes filtered alerts and filter options to template.
    """
    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location_id', None)
    alerts = load_alerts()
    locations = load_locations()
    filtered_alerts = []
    for alert in alerts:
        if severity_filter != 'All' and alert['severity'] != severity_filter:
            continue
        if location_filter and alert['location_id'] != location_filter:
            continue
        filtered_alerts.append(alert)
    return render_template('weather_alerts.html', alerts=filtered_alerts, locations=locations, selected_severity=severity_filter, selected_location=location_filter)
@app.route('/air_quality')
def air_quality():
    """
    Route for Air Quality page.
    Supports optional query parameter 'location_id' to filter data.
    Passes filtered air quality data and locations to template.
    """
    location_id = request.args.get('location_id')
    air_quality_data = load_air_quality()
    locations = load_locations()
    filtered_aqi = None
    if location_id:
        for aqi in air_quality_data:
            if aqi['location_id'] == location_id:
                filtered_aqi = aqi
                break
    else:
        # If no location specified, use default location
        default_location_id = load_default_location_id()
        if default_location_id:
            for aqi in air_quality_data:
                if aqi['location_id'] == default_location_id:
                    filtered_aqi = aqi
                    break
    return render_template('air_quality.html', aqi=filtered_aqi, locations=locations, selected_location=location_id)
@app.route('/saved_locations')
def saved_locations():
    """
    Route for Saved Locations page.
    Loads saved locations and current weather for each saved location.
    Passes data to template.
    """
    saved_locs = load_saved_locations()
    weather_data = load_current_weather()
    # Attach current weather info to saved locations
    for loc in saved_locs:
        loc_id = loc['location_id']
        loc['current_weather'] = weather_data.get(loc_id)
    return render_template('saved_locations.html', saved_locations=saved_locs)
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    Route for Settings page.
    On GET, loads current settings and locations for dropdowns.
    On POST, saves settings (not implemented here, placeholder).
    """
    locations = load_locations()
    saved_locations = load_saved_locations()
    default_location_id = load_default_location_id()
    # For simplicity, hardcode temperature units and alert notification toggle states
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
    alert_notifications_enabled = True
    if request.method == 'POST':
        # Here would be logic to save settings to a file or config (not implemented)
        # Redirect back to settings page after saving
        return redirect(url_for('settings'))
    return render_template('settings.html',
                           temperature_units=temperature_units,
                           selected_temperature_unit='Celsius',
                           locations=locations,
                           selected_default_location=default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled)
if __name__ == '__main__':
    app.run(debug=True)