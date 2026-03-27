
from flask import Flask, redirect, url_for, render_template, request
import os

app = Flask(__name__)

# Paths to data files
DATA_DIR = 'data'
CURRENT_WEATHER_FILE = os.path.join(DATA_DIR, 'current_weather.txt')
FORECASTS_FILE = os.path.join(DATA_DIR, 'forecasts.txt')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.txt')
ALERTS_FILE = os.path.join(DATA_DIR, 'alerts.txt')
AIR_QUALITY_FILE = os.path.join(DATA_DIR, 'air_quality.txt')
SAVED_LOCATIONS_FILE = os.path.join(DATA_DIR, 'saved_locations.txt')

# In-memory data stores
current_weather_data = {}
forecasts_data = {}
locations_data = {}
alerts_data = {}
air_quality_data = {}
saved_locations_data = {}

# Loaders for each data file with error handling

def load_current_weather():
    global current_weather_data
    current_weather_data = {}
    try:
        with open(CURRENT_WEATHER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue  # skip bad lines
                try:
                    location_id = int(parts[0])
                    location_name = parts[1]
                    temperature = float(parts[2])
                    condition = parts[3]
                    humidity = int(parts[4])
                    wind_speed = float(parts[5])
                    last_updated = parts[6]
                    current_weather_data[location_id] = {
                        'location_id': location_id,
                        'location_name': location_name,
                        'temperature': temperature,
                        'condition': condition,
                        'humidity': humidity,
                        'wind_speed': wind_speed,
                        'last_updated': last_updated
                    }
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        current_weather_data = {}


def load_forecasts():
    global forecasts_data
    forecasts_data = {}  # key: location_id, value: list of dicts
    try:
        with open(FORECASTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    forecast_id = int(parts[0])
                    location_id = int(parts[1])
                    date = parts[2]
                    high_temp = float(parts[3])
                    low_temp = float(parts[4])
                    condition = parts[5]
                    precipitation = int(parts[6])
                    humidity = int(parts[7])
                    entry = {
                        'forecast_id': forecast_id,
                        'location_id': location_id,
                        'date': date,
                        'high_temp': high_temp,
                        'low_temp': low_temp,
                        'condition': condition,
                        'precipitation': precipitation,
                        'humidity': humidity
                    }
                    if location_id not in forecasts_data:
                        forecasts_data[location_id] = []
                    forecasts_data[location_id].append(entry)
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        forecasts_data = {}


def load_locations():
    global locations_data
    locations_data = {}
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    location_id = int(parts[0])
                    location_name = parts[1]
                    latitude = float(parts[2])
                    longitude = float(parts[3])
                    country = parts[4]
                    timezone = parts[5]
                    locations_data[location_id] = {
                        'location_id': location_id,
                        'location_name': location_name,
                        'latitude': latitude,
                        'longitude': longitude,
                        'country': country,
                        'timezone': timezone
                    }
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        locations_data = {}


def load_alerts():
    global alerts_data
    alerts_data = {}
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    alert_id = int(parts[0])
                    location_id = int(parts[1])
                    alert_type = parts[2]
                    severity = parts[3]
                    description = parts[4]
                    start_time = parts[5]
                    end_time = parts[6]
                    is_acknowledged = bool(int(parts[7]))
                    alerts_data[alert_id] = {
                        'alert_id': alert_id,
                        'location_id': location_id,
                        'alert_type': alert_type,
                        'severity': severity,
                        'description': description,
                        'start_time': start_time,
                        'end_time': end_time,
                        'is_acknowledged': is_acknowledged
                    }
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        alerts_data = {}


def load_air_quality():
    global air_quality_data
    air_quality_data = {}
    try:
        with open(AIR_QUALITY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    aqi_id = int(parts[0])
                    location_id = int(parts[1])
                    aqi_index = int(parts[2])
                    pm25 = float(parts[3])
                    pm10 = float(parts[4])
                    no2 = float(parts[5])
                    o3 = float(parts[6])
                    last_updated = parts[7]
                    air_quality_data[location_id] = {
                        'aqi_id': aqi_id,
                        'location_id': location_id,
                        'aqi_index': aqi_index,
                        'pm25': pm25,
                        'pm10': pm10,
                        'no2': no2,
                        'o3': o3,
                        'last_updated': last_updated
                    }
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        air_quality_data = {}


def load_saved_locations():
    global saved_locations_data
    saved_locations_data = {}
    try:
        with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    saved_id = int(parts[0])
                    user_id = int(parts[1])
                    location_id = int(parts[2])
                    location_name = parts[3]
                    is_default = bool(int(parts[4]))
                    # Spec assumes single user with id=1
                    if user_id != 1:
                        continue
                    saved_locations_data[location_id] = {
                        'saved_id': saved_id,
                        'user_id': user_id,
                        'location_id': location_id,
                        'location_name': location_name,
                        'is_default': is_default
                    }
                except ValueError:
                    continue
    except (FileNotFoundError, IOError):
        saved_locations_data = {}


# Initialize data
load_current_weather()
load_forecasts()
load_locations()
load_alerts()
load_air_quality()
load_saved_locations()


@app.route('/')
def root_redirect():
    # Redirect to dashboard
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Prepare current_weather_summary for default location
    default_location_id = None
    for loc_id, data in saved_locations_data.items():
        if data.get('is_default'):
            default_location_id = loc_id
            break
    if default_location_id is None:
        # fallback: use first in current_weather_data if any
        default_location_id = next(iter(current_weather_data), None)

    cw = current_weather_data.get(default_location_id)
    if cw is None:
        # Default empty structure
        current_weather_summary = {
            'location_name': '',
            'temperature': 0.0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0.0
        }
    else:
        current_weather_summary = {
            'location_name': cw['location_name'],
            'temperature': cw['temperature'],
            'condition': cw['condition'],
            'humidity': cw['humidity'],
            'wind_speed': cw['wind_speed']
        }

    # URLs for quick access buttons
    quick_access_buttons = {
        'search_location': url_for('location_search_page'),
        'weekly_forecast': url_for('weekly_forecast_page', location_id=default_location_id) if default_location_id is not None else '',
        'alerts': url_for('weather_alerts_page')
    }
    return render_template('dashboard.html', current_weather_summary=current_weather_summary, quick_access_buttons=quick_access_buttons)


@app.route('/weather/current/<int:location_id>')
def current_weather_page(location_id):
    cw = current_weather_data.get(location_id)
    if cw is None:
        # Return 404 or empty page with no data
        return render_template('current_weather.html', location_name='', temperature=0.0, condition='', humidity=0, wind_speed=0.0)
    return render_template(
        'current_weather.html',
        location_name=cw['location_name'],
        temperature=cw['temperature'],
        condition=cw['condition'],
        humidity=cw['humidity'],
        wind_speed=cw['wind_speed']
    )


@app.route('/forecast/weekly/<int:location_id>')
def weekly_forecast_page(location_id):
    location = locations_data.get(location_id)
    location_name = location['location_name'] if location else ''
    weekly_forecast_raw = forecasts_data.get(location_id, [])
    # Prepare list of dicts with forecast data excluding forecast_id
    weekly_forecast = []
    for f in sorted(weekly_forecast_raw, key=lambda x: x['date']):
        weekly_forecast.append({
            'date': f['date'],
            'high_temp': f['high_temp'],
            'low_temp': f['low_temp'],
            'condition': f['condition'],
            'precipitation': f['precipitation'],
            'humidity': f['humidity']
        })
    return render_template('weekly_forecast.html',
                           location_id=location_id,
                           location_name=location_name,
                           weekly_forecast=weekly_forecast)


@app.route('/location/search')
def location_search_page():
    # Search results includes all locations as no search query is specified in spec
    search_results = list(locations_data.values()) if locations_data else []

    saved_locations = []
    for data in saved_locations_data.values():
        saved_locations.append({
            'location_id': data['location_id'],
            'location_name': data['location_name']
        })

    return render_template('location_search.html',
                           search_results=search_results,
                           saved_locations=saved_locations)


@app.route('/alerts')
def weather_alerts_page():
    # Filters select options
    severity_filter_options = ['Critical', 'High', 'Medium', 'Low']
    location_filter_options = []
    location_ids_seen = set()

    # Collect locations from saved locations for filter
    for saved in saved_locations_data.values():
        loc_id = saved['location_id']
        if loc_id not in location_ids_seen:
            loc_name = locations_data.get(loc_id, {}).get('location_name', '')
            if not loc_name:
                loc_name = saved['location_name']
            location_filter_options.append({'location_id': loc_id, 'location_name': loc_name})
            location_ids_seen.add(loc_id)

    alerts_list = []
    for alert in alerts_data.values():
        alerts_list.append({
            'alert_id': alert['alert_id'],
            'location_id': alert['location_id'],
            'alert_type': alert['alert_type'],
            'severity': alert['severity'],
            'description': alert['description'],
            'start_time': alert['start_time'],
            'end_time': alert['end_time'],
            'is_acknowledged': alert['is_acknowledged']
        })

    return render_template('alerts.html',
                           alerts=alerts_list,
                           severity_filter_options=severity_filter_options,
                           location_filter_options=location_filter_options)


@app.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    # Mark alert as acknowledged and save back to alerts.txt
    alert = alerts_data.get(alert_id)
    if alert is not None:
        alert['is_acknowledged'] = True
        # Write back to file the entire alerts_data
        try:
            with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
                for a in alerts_data.values():
                    is_acknowledged_val = 1 if a['is_acknowledged'] else 0
                    line = f"{a['alert_id']}|{a['location_id']}|{a['alert_type']}|{a['severity']}|{a['description']}|{a['start_time']}|{a['end_time']}|{is_acknowledged_val}
"
                    f.write(line)
        except (IOError, OSError):
            pass
    return redirect(url_for('weather_alerts_page'))


@app.route('/airquality')
def air_quality_page():
    # No filter input specified, display first or empty
    aqi_data = None
    health_recommendation = ''
    location_filter_options = []

    # Locations for filter
    for loc_id, loc in locations_data.items():
        location_filter_options.append({'location_id': loc_id, 'location_name': loc['location_name']})

    # Pick first available AQI data
    if air_quality_data:
        aqi_data = next(iter(air_quality_data.values()))

        # Health recommendation based on AQI index (simple categorization)
        aqi_index = aqi_data['aqi_index']
        if aqi_index <= 50:
            health_recommendation = 'Good air quality. Enjoy your usual outdoor activities.'
        elif aqi_index <= 100:
            health_recommendation = 'Moderate air quality. Sensitive groups should consider limiting outdoor exertion.'
        elif aqi_index <= 150:
            health_recommendation = 'Unhealthy for sensitive groups. Consider reducing prolonged or heavy exertion outdoors.'
        elif aqi_index <= 200:
            health_recommendation = 'Unhealthy air quality. Avoid prolonged or heavy exertion outdoors.'
        elif aqi_index <= 300:
            health_recommendation = 'Very unhealthy air quality. Avoid all outdoor exertion if possible.'
        else:
            health_recommendation = 'Hazardous air quality. Remain indoors and keep activity levels low.'
    else:
        aqi_data = {
            'location_id': 0,
            'aqi_index': 0,
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }
        health_recommendation = ''

    return render_template('air_quality.html', aqi_data=aqi_data, health_recommendation=health_recommendation, location_filter_options=location_filter_options)


@app.route('/savedlocations')
def saved_locations_page():
    saved_locations = []
    user_default_location_id = None
    for loc_id, saved in saved_locations_data.items():
        cw = current_weather_data.get(loc_id, {})
        saved_locations.append({
            'location_id': loc_id,
            'location_name': saved['location_name'],
            'temperature': cw.get('temperature', 0.0),
            'condition': cw.get('condition', '')
        })
        if saved.get('is_default'):
            user_default_location_id = loc_id

    if user_default_location_id is None and saved_locations:
        user_default_location_id = saved_locations[0]['location_id']

    return render_template('saved_locations.html', saved_locations=saved_locations, user_default_location_id=user_default_location_id)


@app.route('/savedlocations/remove/<int:location_id>', methods=['POST'])
def remove_saved_location(location_id):
    if location_id in saved_locations_data:
        del saved_locations_data[location_id]
        # Save back to file
        try:
            with open(SAVED_LOCATIONS_FILE, 'w', encoding='utf-8') as f:
                # Write all saved locations, user id fixed at 1, saved_id incremental from 1
                saved_id_counter = 1
                for saved in saved_locations_data.values():
                    is_default_val = 1 if saved.get('is_default', False) else 0
                    line = f"{saved_id_counter}|1|{saved['location_id']}|{saved['location_name']}|{is_default_val}
"
                    f.write(line)
                    saved_id_counter += 1
        except (IOError, OSError):
            pass
    return redirect(url_for('saved_locations_page'))


@app.route('/savedlocations/view/<int:location_id>')
def view_location_weather(location_id):
    cw = current_weather_data.get(location_id)
    if cw is None:
        return render_template('current_weather.html', location_name='', temperature=0.0, condition='', humidity=0, wind_speed=0.0)
    return render_template(
        'current_weather.html',
        location_name=cw['location_name'],
        temperature=cw['temperature'],
        condition=cw['condition'],
        humidity=cw['humidity'],
        wind_speed=cw['wind_speed']
    )


@app.route('/settings')
def settings_page():
    # temperature_units is fixed list
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']

    # default_location_id from saved_locations
    default_location_id = None
    for saved in saved_locations_data.values():
        if saved.get('is_default'):
            default_location_id = saved['location_id']
            break

    # locations list for dropdown
    locations_list = []
    for loc in locations_data.values():
        locations_list.append({'location_id': loc['location_id'], 'location_name': loc['location_name']})

    # Since we don't have persistent user settings beyond saved locations default, 
    # assume alert_notifications_enabled True by default
    alert_notifications_enabled = True

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           default_location_id=default_location_id if default_location_id is not None else 0,
                           locations=locations_list,
                           alert_notifications_enabled=alert_notifications_enabled)


@app.route('/settings/save', methods=['POST'])
def save_settings():
    # The spec does not specify any persistent storage besides saved_locations, 
    # so we'll accept form data but we do not persist it anywhere.
    # Redirect back to settings page after "saving"
    _ = request.form.get('temperature_unit')
    _ = request.form.get('default_location_id')
    _ = request.form.get('alert_notifications_enabled')
    # No changes applied as per spec - no persistence
    return redirect(url_for('settings_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
