'''
Main backend application for WeatherForecast web application.
Implements Flask web server, routing, and business logic for all pages.
Handles reading and writing data from/to local text files in 'data/' directory.
Supports all eight pages with required functionality and data filtering.
No authentication; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read and write data files
def read_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    weather_data = []
    if not os.path.exists(filepath):
        return weather_data
    try:
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
    except Exception:
        # Return empty list on error
        return []
    return weather_data
def read_forecasts():
    filepath = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if not os.path.exists(filepath):
        return forecasts
    try:
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
    except Exception:
        return []
    return forecasts
def read_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    if not os.path.exists(filepath):
        return locations
    try:
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
    except Exception:
        return []
    return locations
def read_alerts():
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if not os.path.exists(filepath):
        return alerts
    try:
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
    except Exception:
        return []
    return alerts
def write_alerts(alerts):
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    try:
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
    except Exception:
        pass
def read_air_quality():
    filepath = os.path.join(DATA_DIR, 'air_quality.txt')
    aqi_data = []
    if not os.path.exists(filepath):
        return aqi_data
    try:
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
    except Exception:
        return []
    return aqi_data
def read_saved_locations():
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    if not os.path.exists(filepath):
        return saved_locations
    try:
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
    except Exception:
        return []
    return saved_locations
def write_saved_locations(saved_locations):
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for sl in saved_locations:
                line = '|'.join([
                    str(sl['saved_id']),
                    str(sl['user_id']),
                    str(sl['location_id']),
                    sl['location_name'],
                    '1' if sl['is_default'] else '0'
                ])
                f.write(line + '\n')
    except Exception:
        pass
def read_settings():
    # Settings are stored in 'settings.txt' in data directory.
    # Format:
    # temperature_unit|default_location_id|alert_notifications_enabled
    filepath = os.path.join(DATA_DIR, 'settings.txt')
    default_settings = {
        'temperature_unit': 'Celsius',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }
    if not os.path.exists(filepath):
        return default_settings
    try:
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
    except Exception:
        return default_settings
def write_settings(settings):
    filepath = os.path.join(DATA_DIR, 'settings.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            line = '|'.join([
                settings.get('temperature_unit', 'Celsius'),
                str(settings.get('default_location_id', '')) if settings.get('default_location_id') is not None else '',
                '1' if settings.get('alert_notifications_enabled', True) else '0'
            ])
            f.write(line + '\n')
    except Exception:
        pass
# Helper functions
def get_location_by_id(location_id):
    locations = read_locations()
    for loc in locations:
        if loc['location_id'] == location_id:
            return loc
    return None
def get_default_location():
    settings = read_settings()
    default_location_id = settings.get('default_location_id')
    if default_location_id is not None:
        loc = get_location_by_id(default_location_id)
        if loc:
            return loc
    # If no default set, fallback to first location in locations.txt
    locations = read_locations()
    if locations:
        return locations[0]
    return None
def get_current_weather_for_location(location_id):
    weather_data = read_current_weather()
    for w in weather_data:
        if w['location_id'] == location_id:
            return w
    return None
def get_forecasts_for_location(location_id):
    forecasts = read_forecasts()
    return [f for f in forecasts if f['location_id'] == location_id]
def get_alerts_for_location(location_id):
    alerts = read_alerts()
    return [a for a in alerts if a['location_id'] == location_id and not a['is_acknowledged']]
def get_air_quality_for_location(location_id):
    aqi_data = read_air_quality()
    for aqi in aqi_data:
        if aqi['location_id'] == location_id:
            return aqi
    return None
def get_saved_locations_for_user(user_id=1):
    # Since no authentication, assume user_id=1 for all
    saved_locations = read_saved_locations()
    return [sl for sl in saved_locations if sl['user_id'] == user_id]
def get_next_saved_id(saved_locations):
    if not saved_locations:
        return 1
    return max(sl['saved_id'] for sl in saved_locations) + 1
def get_next_alert_id(alerts):
    if not alerts:
        return 1
    return max(a['alert_id'] for a in alerts) + 1
def get_next_forecast_id(forecasts):
    if not forecasts:
        return 1
    return max(f['forecast_id'] for f in forecasts) + 1
# Temperature conversion helper
def convert_temperature(temp_celsius, to_unit):
    if to_unit == 'Celsius':
        return temp_celsius
    elif to_unit == 'Fahrenheit':
        return temp_celsius * 9/5 + 32
    elif to_unit == 'Kelvin':
        return temp_celsius + 273.15
    else:
        return temp_celsius
def convert_temperature_from_data(temp, from_unit, to_unit):
    # Data temps are stored as numbers, assume Fahrenheit for conversion (per requirements)
    if from_unit == to_unit:
        return temp
    if from_unit == 'Fahrenheit':
        temp_c = (temp - 32) * 5/9
    elif from_unit == 'Celsius':
        temp_c = temp
    elif from_unit == 'Kelvin':
        temp_c = temp - 273.15
    else:
        temp_c = temp
    # Now convert Celsius to to_unit
    if to_unit == 'Celsius':
        return temp_c
    elif to_unit == 'Fahrenheit':
        return temp_c * 9/5 + 32
    elif to_unit == 'Kelvin':
        return temp_c + 273.15
    else:
        return temp
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
        return "Air quality is acceptable. Some pollutants may be a moderate health concern for a very small number of people."
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
    default_location = get_default_location()
    if not default_location:
        # No locations available
        current_weather = None
    else:
        current_weather = get_current_weather_for_location(default_location['location_id'])
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    # Convert temperature to selected unit if current_weather exists
    if current_weather:
        # Assume data temperature is Fahrenheit (based on example)
        temp_f = current_weather['temperature']
        temp_converted = convert_temperature_from_data(temp_f, 'Fahrenheit', temperature_unit)
        current_weather['temperature_converted'] = round(temp_converted, 1)
    # Prepare URLs for JS navigation to avoid hardcoded URLs in JS
    urls = {
        'location_search': url_for('location_search'),
        'weekly_forecast': url_for('weekly_forecast'),
        'weather_alerts': url_for('weather_alerts'),
        'air_quality': url_for('air_quality'),
        'saved_locations': url_for('saved_locations'),
        'settings': url_for('settings')
    }
    return render_template('dashboard.html',
                           current_weather=current_weather,
                           temperature_unit=temperature_unit,
                           urls=urls)
@app.route('/current_weather/<int:location_id>')
def current_weather(location_id):
    settings = read_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    location = get_location_by_id(location_id)
    if not location:
        return "Location not found", 404
    weather = get_current_weather_for_location(location_id)
    if not weather:
        # No weather data for location
        weather = {
            'temperature': None,
            'condition': 'N/A',
            'humidity': None,
            'wind_speed': None
        }
    else:
        temp_f = weather['temperature']
        temp_converted = convert_temperature_from_data(temp_f, 'Fahrenheit', temperature_unit)
        weather['temperature_converted'] = round(temp_converted, 1)
    return render_template('current_weather.html',
                           location=location,
                           weather=weather,
                           temperature_unit=temperature_unit)
@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    settings = read_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')
    locations = read_locations()
    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('location-filter')
        if selected_location_id and selected_location_id.isdigit():
            selected_location_id = int(selected_location_id)
        else:
            selected_location_id = None
    else:
        # GET request: use default location
        default_location = get_default_location()
        selected_location_id = default_location['location_id'] if default_location else None
    forecasts = []
    if selected_location_id is not None:
        all_forecasts = get_forecasts_for_location(selected_location_id)
        # Sort by date ascending
        try:
            forecasts = sorted(all_forecasts, key=lambda f: datetime.strptime(f['date'], '%Y-%m-%d'))
        except Exception:
            forecasts = all_forecasts
        # Convert temperatures
        for f in forecasts:
            # Data temps assumed Fahrenheit
            f['high_temp_converted'] = round(convert_temperature_from_data(f['high_temp'], 'Fahrenheit', temperature_unit), 1)
            f['low_temp_converted'] = round(convert_temperature_from_data(f['low_temp'], 'Fahrenheit', temperature_unit), 1)
    return render_template('weekly_forecast.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           forecasts=forecasts,
                           temperature_unit=temperature_unit)
@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = read_locations()
    saved_locations = get_saved_locations_for_user()
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
                                if abs(loc['latitude'] - lat_q) <= 0.1 and abs(loc['longitude'] - lon_q) <= 0.1:
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
    location = get_location_by_id(location_id)
    if not location:
        return "Location not found", 404
    saved_locations = read_saved_locations()
    user_id = 1
    for sl in saved_locations:
        if sl['user_id'] == user_id and sl['location_id'] == location_id:
            # Already saved
            break
    else:
        # Add new saved location
        new_id = get_next_saved_id(saved_locations)
        saved_locations.append({
            'saved_id': new_id,
            'user_id': user_id,
            'location_id': location_id,
            'location_name': location['location_name'],
            'is_default': False
        })
        write_saved_locations(saved_locations)
    return redirect(url_for('saved_locations'))
@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    locations = read_locations()
    alerts = read_alerts()
    severity_filter = 'All'
    location_filter = 'All'
    filtered_alerts = alerts
    if request.method == 'POST':
        severity_filter = request.form.get('severity-filter', 'All')
        location_filter = request.form.get('location-filter-alerts', 'All')
    # Filter by severity
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]
    # Filter by location
    if location_filter != 'All':
        try:
            loc_id = int(location_filter)
            filtered_alerts = [a for a in filtered_alerts if a['location_id'] == loc_id]
        except ValueError:
            pass
    # Only show unacknowledged alerts
    filtered_alerts = [a for a in filtered_alerts if not a['is_acknowledged']]
    # Add location name to alerts for display
    loc_dict = {loc['location_id']: loc['location_name'] for loc in locations}
    for alert in filtered_alerts:
        alert['location_name'] = loc_dict.get(alert['location_id'], 'Unknown')
    return render_template('weather_alerts.html',
                           alerts=filtered_alerts,
                           locations=locations,
                           severity_filter=severity_filter,
                           location_filter=location_filter)
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
    locations = read_locations()
    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('location-aqi-filter')
        if selected_location_id and selected_location_id.isdigit():
            selected_location_id = int(selected_location_id)
        else:
            selected_location_id = None
    else:
        default_location = get_default_location()
        selected_location_id = default_location['location_id'] if default_location else None
    aqi = None
    if selected_location_id is not None:
        aqi = get_air_quality_for_location(selected_location_id)
    aqi_desc = None
    health_rec = None
    if aqi:
        aqi_desc = aqi_description(aqi['aqi_index'])
        health_rec = health_recommendation(aqi['aqi_index'])
    return render_template('air_quality.html',
                           locations=locations,
                           selected_location_id=selected_location_id,
                           aqi=aqi,
                           aqi_description=aqi_desc,
                           health_recommendation=health_rec)
@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    saved_locations = get_saved_locations_for_user()
    locations = read_locations()
    current_weather_data = read_current_weather()
    temperature_unit = read_settings().get('temperature_unit', 'Celsius')
    # Build a dict for quick weather lookup by location_id
    weather_dict = {w['location_id']: w for w in current_weather_data}
    # Prepare saved locations with current temp and condition
    saved_locs_display = []
    for sl in saved_locations:
        loc_id = sl['location_id']
        weather = weather_dict.get(loc_id)
        temp_converted = None
        condition = None
        if weather:
            temp_f = weather['temperature']
            temp_converted = round(convert_temperature_from_data(temp_f, 'Fahrenheit', temperature_unit), 1)
            condition = weather['condition']
        saved_locs_display.append({
            'saved_id': sl['saved_id'],
            'location_id': loc_id,
            'location_name': sl['location_name'],
            'temperature': temp_converted,
            'condition': condition,
            'is_default': sl['is_default']
        })
    return render_template('saved_locations.html',
                           saved_locations=saved_locs_display,
                           temperature_unit=temperature_unit)
@app.route('/view_location_weather/<int:location_id>')
def view_location_weather(location_id):
    # Redirect to current weather page for location
    return redirect(url_for('current_weather', location_id=location_id))
@app.route('/remove_location/<int:saved_id>', methods=['POST'])
def remove_location(saved_id):
    saved_locations = read_saved_locations()
    saved_locations = [sl for sl in saved_locations if sl['saved_id'] != saved_id]
    write_saved_locations(saved_locations)
    return redirect(url_for('saved_locations'))
@app.route('/add_new_location')
def add_new_location():
    # Redirect to location search page to add new location
    return redirect(url_for('location_search'))
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings = read_settings()
    locations = read_locations()
    if request.method == 'POST':
        temperature_unit = request.form.get('temperature-unit-select', 'Celsius')
        default_location_id = request.form.get('default-location-select')
        alert_notifications_enabled = request.form.get('alert-notifications-toggle')
        if default_location_id and default_location_id.isdigit():
            default_location_id = int(default_location_id)
        else:
            default_location_id = None
        alert_notifications_enabled = (alert_notifications_enabled == 'on')
        settings['temperature_unit'] = temperature_unit
        settings['default_location_id'] = default_location_id
        settings['alert_notifications_enabled'] = alert_notifications_enabled
        write_settings(settings)
        return redirect(url_for('dashboard'))
    return render_template('settings.html',
                           settings=settings,
                           locations=locations)
@app.route('/back_to_dashboard', methods=['POST'])
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)