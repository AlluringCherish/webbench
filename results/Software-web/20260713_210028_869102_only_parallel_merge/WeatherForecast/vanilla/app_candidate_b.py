from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to read data files

def read_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                location_id = int(parts[0])
                data[location_id] = {
                    'location_id': location_id,
                    'location_name': parts[1],
                    'temperature': parts[2],
                    'condition': parts[3],
                    'humidity': parts[4],
                    'wind_speed': parts[5],
                    'last_updated': parts[6],
                }
    return data


def read_forecasts():
    filepath = os.path.join(DATA_DIR, 'forecasts.txt')
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    forecast = {
                        'forecast_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'date': parts[2],
                        'high_temp': parts[3],
                        'low_temp': parts[4],
                        'condition': parts[5],
                        'precipitation': parts[6],
                        'humidity': parts[7]
                    }
                    data.append(forecast)
                except:
                    continue
    return data


def read_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
                    location_id = int(parts[0])
                    locations[location_id] = {
                        'location_id': location_id,
                        'location_name': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3],
                        'country': parts[4],
                        'timezone': parts[5],
                    }
                except:
                    continue
    return locations


def read_alerts():
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    alert = {
                        'alert_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7] == '1'
                    }
                    alerts.append(alert)
                except:
                    continue
    return alerts


def read_air_quality():
    filepath = os.path.join(DATA_DIR, 'air_quality.txt')
    air_quality = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    aqi_id = int(parts[0])
                    location_id = int(parts[1])
                    air_quality[location_id] = {
                        'aqi_id': aqi_id,
                        'location_id': location_id,
                        'aqi_index': int(parts[2]),
                        'pm25': parts[3],
                        'pm10': parts[4],
                        'no2': parts[5],
                        'o3': parts[6],
                        'last_updated': parts[7],
                    }
                except:
                    continue
    return air_quality


def read_saved_locations():
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    saved_id = int(parts[0])
                    user_id = int(parts[1])
                    location_id = int(parts[2])
                    location_name = parts[3]
                    is_default = parts[4] == '1'
                    saved.append({
                        'saved_id': saved_id,
                        'user_id': user_id,
                        'location_id': location_id,
                        'location_name': location_name,
                        'is_default': is_default
                    })
                except:
                    continue
    return saved


def write_saved_locations(saved_list):
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    with open(filepath, 'w') as f:
        for entry in saved_list:
            line = f"{entry['saved_id']}|{entry['user_id']}|{entry['location_id']}|{entry['location_name']}|{'1' if entry['is_default'] else '0'}\n"
            f.write(line)


def write_alerts(alerts_list):
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    with open(filepath, 'w') as f:
        for alert in alerts_list:
            line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{'1' if alert['is_acknowledged'] else '0'}\n"
            f.write(line)

# Utility for AQI descriptions
AQI_DESCRIPTIONS = [
    (0, 50, 'Good'),
    (51, 100, 'Moderate'),
    (101, 150, 'Unhealthy for Sensitive Groups'),
    (151, 200, 'Unhealthy'),
    (201, 300, 'Very Unhealthy'),
    (301, 500, 'Hazardous')
]

# Get AQI description text

def get_aqi_description(aqi_index):
    for (low, high, desc) in AQI_DESCRIPTIONS:
        if low <= aqi_index <= high:
            return desc
    return 'Unknown'


# Default user ID (since no authentication, assume 1)
CURRENT_USER_ID = 1

# Settings file path
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.txt')

# Load settings from settings.txt
# Format assumed: temperature_unit|default_location_id|alert_notifications_enabled
# E.g.: Celsius|1|1

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        # Defaults
        return {
            'temperature_unit': 'Celsius',
            'default_location_id': None,
            'alert_notifications_enabled': True
        }
    with open(SETTINGS_FILE, 'r') as f:
        line = f.readline().strip()
        parts = line.split('|')
        if len(parts) == 3:
            return {
                'temperature_unit': parts[0],
                'default_location_id': int(parts[1]) if parts[1].isdigit() else None,
                'alert_notifications_enabled': parts[2] == '1'
            }
        else:
            return {
                'temperature_unit': 'Celsius',
                'default_location_id': None,
                'alert_notifications_enabled': True
            }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        line = f"{settings.get('temperature_unit', 'Celsius')}|{settings.get('default_location_id', '')}|{'1' if settings.get('alert_notifications_enabled', True) else '0'}\n"
        f.write(line)


# Convert temperature if needed
# All temperatures in data are presumably Fahrenheit as example, but the task doesn't specify conversions explicitly
# We'll assume input temps are Fahrenheit and convert to Celsius or Kelvin if user chooses

def convert_temperature(temp_f, unit):
    try:
        temp_f = float(temp_f)
    except:
        return temp_f
    if unit == 'Fahrenheit':
        return round(temp_f,1)
    elif unit == 'Celsius':
        return round((temp_f - 32) * 5/9,1)
    elif unit == 'Kelvin':
        return round((temp_f - 32) * 5/9 + 273.15,1)
    else:
        return round(temp_f,1)


@app.route('/')
@app.route('/dashboard')
def dashboard():
    settings = load_settings()
    default_location_id = settings.get('default_location_id')
    if default_location_id is None:
        # fallback: take first location from saved locations or locations
        saved_locs = [loc for loc in read_saved_locations() if loc['user_id'] == CURRENT_USER_ID]
        if saved_locs:
            default_location_id = saved_locs[0]['location_id']
        else:
            locations = read_locations()
            default_location_id = next(iter(locations.keys()), None)

    current_weather_data = read_current_weather()
    locations = read_locations()

    temperature_unit = settings.get('temperature_unit', 'Celsius')

    weather_info = current_weather_data.get(default_location_id)
    if weather_info:
        weather_info = dict(weather_info)  # copy
        weather_info['temperature_display'] = f"{convert_temperature(weather_info['temperature'], temperature_unit)} °{temperature_unit[0]}"
    
    return render_template('dashboard.html',
                           weather=weather_info,
                           temperature_unit=temperature_unit)


@app.route('/current-weather/<int:location_id>')
def current_weather(location_id):
    settings = load_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')

    current_weather_data = read_current_weather()
    weather_info = current_weather_data.get(location_id)
    if not weather_info:
        return f"No current weather data found for location {location_id}", 404

    weather_info = dict(weather_info)  # copy
    weather_info['temperature_display'] = f"{convert_temperature(weather_info['temperature'], temperature_unit)} °{temperature_unit[0]}"

    return render_template('current_weather.html', weather=weather_info)


@app.route('/forecast')
def forecast():
    settings = load_settings()
    temperature_unit = settings.get('temperature_unit', 'Celsius')

    locations = read_locations()
    current_location_id = request.args.get('location_id', type=int) or next(iter(locations.keys()), None)

    forecasts = read_forecasts()

    # Filter forecasts by selected location
    filtered_forecasts = [f for f in forecasts if f['location_id'] == current_location_id]

    # Convert temps
    for fcast in filtered_forecasts:
        fcast['high_temp_converted'] = f"{convert_temperature(fcast['high_temp'], temperature_unit)} °{temperature_unit[0]}"
        fcast['low_temp_converted'] = f"{convert_temperature(fcast['low_temp'], temperature_unit)} °{temperature_unit[0]}"

    return render_template('forecast.html',
                           forecasts=filtered_forecasts,
                           locations=locations,
                           current_location_id=current_location_id)


@app.route('/search', methods=['GET', 'POST'])
def search_locations():
    locations = read_locations()
    saved_locations = [loc for loc in read_saved_locations() if loc['user_id'] == CURRENT_USER_ID]

    # POST: handle adding a new saved location or selecting a location
    search_results = []
    message = ''
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_location':
            location_id = int(request.form.get('location_id', 0))
            location_name = request.form.get('location_name', '')
            # Check if already saved
            if any(loc['location_id'] == location_id for loc in saved_locations):
                message = 'Location already saved.'
            else:
                # Add new saved location
                saved_list = read_saved_locations()
                new_id = (max([loc['saved_id'] for loc in saved_list]) + 1) if saved_list else 1
                # By default not default
                new_entry = {
                    'saved_id': new_id,
                    'user_id': CURRENT_USER_ID,
                    'location_id': location_id,
                    'location_name': location_name,
                    'is_default': False
                }
                saved_list.append(new_entry)
                write_saved_locations(saved_list)
                saved_locations.append(new_entry)
                message = 'Location saved successfully.'

        elif action == 'search':
            search_query = request.form.get('location_search_input', '').strip().lower()
            search_results = []
            if search_query:
                for loc in locations.values():
                    if (search_query in loc['location_name'].lower() 
                        or search_query in str(loc['latitude']) 
                        or search_query in str(loc['longitude'])):
                        search_results.append(loc)

    return render_template('search.html',
                           saved_locations=saved_locations,
                           search_results=search_results,
                           message=message)


@app.route('/alerts')
def alerts():
    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location_id', type=int)

    alerts = read_alerts()
    locations = read_locations()

    # Filter by severity
    if severity_filter != 'All':
        alerts = [a for a in alerts if a['severity'] == severity_filter]

    # Filter by location
    if location_filter:
        alerts = [a for a in alerts if a['location_id'] == location_filter]

    # Show only unacknowledged alerts or all
    # We show all alerts but mark acknowledged as acknowledged visually

    # Add location name for convenience
    for alert in alerts:
        location = locations.get(alert['location_id'])
        alert['location_name'] = location['location_name'] if location else ''

    # For filters dropdown
    severity_options = ['All', 'Critical', 'High', 'Medium', 'Low']

    return render_template('alerts.html',
                           alerts=alerts,
                           locations=locations,
                           severity_filter=severity_filter,
                           location_filter=location_filter,
                           severity_options=severity_options)


@app.route('/acknowledge-alert/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = read_alerts()
    updated = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            updated = True
            break
    if updated:
        write_alerts(alerts)
    return redirect(url_for('alerts'))


@app.route('/air-quality')
def air_quality():
    location_filter = request.args.get('location_id', type=int)
    air_quality_data = read_air_quality()
    locations = read_locations()

    # If no location specified, pick first location
    if not location_filter and locations:
        location_filter = next(iter(locations.keys()))

    aqi_info = air_quality_data.get(location_filter)

    # Compose health recommendation
    health_recommendation = ''
    if aqi_info:
        aqi_desc = get_aqi_description(aqi_info['aqi_index'])
        if aqi_info['aqi_index'] <= 50:
            health_recommendation = 'Air quality is good. Enjoy your usual outdoor activities.'
        elif aqi_info['aqi_index'] <= 100:
            health_recommendation = 'Air quality is moderate. Unusually sensitive individuals should consider limiting prolonged outdoor exertion.'
        elif aqi_info['aqi_index'] <= 150:
            health_recommendation = 'Members of sensitive groups may experience health effects. Consider reducing prolonged outdoor exertion.'
        elif aqi_info['aqi_index'] <= 200:
            health_recommendation = 'Air quality is unhealthy. Everyone should reduce prolonged or heavy outdoor exertion.'
        elif aqi_info['aqi_index'] <= 300:
            health_recommendation = 'Very unhealthy air quality. Avoid outdoor activities if possible.'
        else:
            health_recommendation = 'Hazardous air quality. Stay indoors and keep activity levels low.'
    
    return render_template('air_quality.html',
                           aqi_info=aqi_info,
                           locations=locations,
                           location_filter=location_filter,
                           aqi_description=get_aqi_description(aqi_info['aqi_index']) if aqi_info else '',
                           health_recommendation=health_recommendation)


@app.route('/saved-locations')
def saved_locations():
    saved_locations_list = [loc for loc in read_saved_locations() if loc['user_id'] == CURRENT_USER_ID]
    current_weather = read_current_weather()

    # Augment saved locations with current weather if available
    for loc in saved_locations_list:
        weather = current_weather.get(loc['location_id'])
        if weather:
            loc['current_temp'] = weather['temperature']
            loc['current_condition'] = weather['condition']
        else:
            loc['current_temp'] = 'N/A'
            loc['current_condition'] = 'N/A'

    return render_template('saved_locations.html',
                           saved_locations=saved_locations_list)


@app.route('/remove-saved-location/<int:location_id>', methods=['POST'])
def remove_saved_location(location_id):
    saved_list = read_saved_locations()
    saved_list = [loc for loc in saved_list if not (loc['user_id'] == CURRENT_USER_ID and loc['location_id'] == location_id)]
    write_saved_locations(saved_list)
    return redirect(url_for('saved_locations'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = read_locations()
    settings_data = load_settings()
    message = ''
    if request.method == 'POST':
        temperature_unit = request.form.get('temperature_unit')
        default_location_id = request.form.get('default_location_select')
        alert_notifications_enabled = request.form.get('alert_notifications_toggle') == 'on'

        if default_location_id and default_location_id.isdigit():
            default_location_id = int(default_location_id)
        else:
            default_location_id = None

        settings_data['temperature_unit'] = temperature_unit
        settings_data['default_location_id'] = default_location_id
        settings_data['alert_notifications_enabled'] = alert_notifications_enabled

        save_settings(settings_data)
        message = 'Settings saved successfully.'

    return render_template('settings.html',
                           settings=settings_data,
                           locations=locations,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
