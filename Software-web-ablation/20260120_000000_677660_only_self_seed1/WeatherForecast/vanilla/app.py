from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# === Data Loading Utilities ===

def load_current_weather():
    """Load current weather data from data/current_weather.txt"""
    file_path = os.path.join(DATA_DIR, 'current_weather.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        entry = {
                            'location_id': int(parts[0]),
                            'location_name': parts[1],
                            'temperature': int(parts[2]),
                            'condition': parts[3],
                            'humidity': int(parts[4]),
                            'wind_speed': int(parts[5]),
                            'last_updated': parts[6]
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


def load_forecasts():
    """Load forecasts data from data/forecasts.txt"""
    file_path = os.path.join(DATA_DIR, 'forecasts.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        entry = {
                            'forecast_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'date': parts[2],
                            'high_temp': int(parts[3]),
                            'low_temp': int(parts[4]),
                            'condition': parts[5],
                            'precipitation': int(parts[6]),
                            'humidity': int(parts[7])
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


def load_locations():
    """Load locations data from data/locations.txt"""
    file_path = os.path.join(DATA_DIR, 'locations.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        entry = {
                            'location_id': int(parts[0]),
                            'location_name': parts[1],
                            'latitude': float(parts[2]),
                            'longitude': float(parts[3]),
                            'country': parts[4],
                            'timezone': parts[5]
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


def load_alerts():
    """Load weather alerts data from data/alerts.txt"""
    file_path = os.path.join(DATA_DIR, 'alerts.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        entry = {
                            'alert_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'alert_type': parts[2],
                            'severity': parts[3],
                            'description': parts[4],
                            'start_time': parts[5],
                            'end_time': parts[6],
                            'is_acknowledged': parts[7] == '1'
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


def load_air_quality():
    """Load air quality data from data/air_quality.txt"""
    file_path = os.path.join(DATA_DIR, 'air_quality.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        entry = {
                            'aqi_id': int(parts[0]),
                            'location_id': int(parts[1]),
                            'aqi_index': int(parts[2]),
                            'pm25': float(parts[3]),
                            'pm10': float(parts[4]),
                            'no2': float(parts[5]),
                            'o3': float(parts[6]),
                            'last_updated': parts[7]
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


def load_saved_locations():
    """Load saved locations data from data/saved_locations.txt"""
    file_path = os.path.join(DATA_DIR, 'saved_locations.txt')
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        entry = {
                            'saved_id': int(parts[0]),
                            'user_id': int(parts[1]),
                            'location_id': int(parts[2]),
                            'location_name': parts[3],
                            'is_default': parts[4] == '1'
                        }
                        data.append(entry)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return data


# === Helper Functions ===

def find_location_name(location_id, locations_data):
    for loc in locations_data:
        if loc['location_id'] == location_id:
            return loc['location_name']
    return ''


def get_saved_location_default(saved_locations):
    for saved in saved_locations:
        if saved['is_default']:
            return saved
    return None


def filter_alerts(alerts, severity_filter, location_filter):
    filtered = []
    for alert in alerts:
        if severity_filter != 'All' and alert['severity'] != severity_filter:
            continue
        if location_filter is not None and alert['location_id'] != location_filter:
            continue
        filtered.append(alert)
    return filtered


def get_aqi_description(aqi_index):
    if aqi_index <= 50:
        return 'Good'
    elif aqi_index <= 100:
        return 'Moderate'
    elif aqi_index <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi_index <= 200:
        return 'Unhealthy'
    elif aqi_index <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'


def get_health_recommendation(aqi_desc):
    recommendations = {
        'Good': 'Air quality is satisfactory, and air pollution poses little or no risk.',
        'Moderate': 'Air quality is acceptable; some pollutants may be a moderate health concern.',
        'Unhealthy for Sensitive Groups': 'Members of sensitive groups may experience health effects.',
        'Unhealthy': 'Everyone may begin to experience health effects.',
        'Very Unhealthy': 'Health alert: everyone may experience more serious health effects.',
        'Hazardous': 'Health warnings of emergency conditions. The entire population is more likely to be affected.'
    }
    return recommendations.get(aqi_desc, '')


def temperature_units_options():
    return ["Celsius", "Fahrenheit", "Kelvin"]

# === Flask Routes ===

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    current_weather_data = load_current_weather()
    saved_locations = load_saved_locations()
    # Determine default location
    default_saved = get_saved_location_default(saved_locations)
    selected_location_id = None
    if default_saved:
        selected_location_id = default_saved['location_id']

    # Find the current weather for the default location
    current_weather_entry = None
    if selected_location_id is not None:
        for entry in current_weather_data:
            if entry['location_id'] == selected_location_id:
                current_weather_entry = entry
                break

    # If no matching current weather found, fallback to first or empty
    if not current_weather_entry and current_weather_data:
        current_weather_entry = current_weather_data[0]

    current_weather = {}
    if current_weather_entry:
        current_weather = {
            'location_id': current_weather_entry['location_id'],
            'location_name': current_weather_entry['location_name'],
            'temperature': current_weather_entry['temperature'],
            'condition': current_weather_entry['condition'],
            'humidity': current_weather_entry['humidity'],
            'wind_speed': current_weather_entry['wind_speed'],
            'last_updated': current_weather_entry['last_updated']
        }

    return render_template('dashboard.html', current_weather=current_weather)


@app.route('/weather/current/<int:location_id>', methods=['GET'])
def current_weather(location_id):
    current_weather_data = load_current_weather()
    # Find the weather info for location_id
    weather = None
    for entry in current_weather_data:
        if entry['location_id'] == location_id:
            weather = entry
            break

    if weather is None:
        # Return with empty or not found context
        context = {
            'location_name': '',
            'temperature': 0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0
        }
    else:
        context = {
            'location_name': weather['location_name'],
            'temperature': weather['temperature'],
            'condition': weather['condition'],
            'humidity': weather['humidity'],
            'wind_speed': weather['wind_speed']
        }

    return render_template('current_weather.html', **context)


@app.route('/forecast/weekly', methods=['GET', 'POST'])
def weekly_forecast():
    locations = load_locations()
    forecasts = load_forecasts()

    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    selected_location_id = None
    if request.method == 'POST':
        try:
            selected_location_id = int(request.form.get('location_id', '').strip())
        except (ValueError, AttributeError):
            selected_location_id = None
    # If no selection, fallback to first location
    if selected_location_id is None and locations_list:
        selected_location_id = locations_list[0]['location_id']

    # Filter forecasts for selected location
    forecast_list = []
    for fc in forecasts:
        if fc['location_id'] == selected_location_id:
            forecast_list.append({
                'date': fc['date'],
                'high_temp': fc['high_temp'],
                'low_temp': fc['low_temp'],
                'condition': fc['condition']
            })

    return render_template('weekly_forecast.html',
                           locations=locations_list,
                           selected_location_id=selected_location_id,
                           forecast_list=forecast_list)


@app.route('/locations/search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locations_raw = load_saved_locations()
    saved_locations = [{'location_id': s['location_id'], 'location_name': s['location_name']} for s in saved_locations_raw]

    search_query = ''
    search_results = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            # Search locations by name case-insensitive substring
            sq_lower = search_query.lower()
            for loc in locations:
                if sq_lower in loc['location_name'].lower():
                    search_results.append({
                        'location_id': loc['location_id'],
                        'location_name': loc['location_name'],
                        'latitude': loc['latitude'],
                        'longitude': loc['longitude'],
                        'country': loc['country']
                    })
        # Also check if user selected to save location - this is done via POST with a 'select_location_id' field
        select_location_id_str = request.form.get('select_location_id')
        if select_location_id_str:
            try:
                select_location_id = int(select_location_id_str)
            except ValueError:
                select_location_id = None
            if select_location_id is not None:
                # Save the selected location if not already saved
                already_saved_ids = set(s['location_id'] for s in saved_locations_raw)
                if select_location_id not in already_saved_ids:
                    # Add new saved location with user_id=1 and is_default=0
                    # Determine new saved_id incrementally
                    new_saved_id = 1
                    if saved_locations_raw:
                        new_saved_id = max(s['saved_id'] for s in saved_locations_raw) + 1
                    location_to_save = None
                    for loc in locations:
                        if loc['location_id'] == select_location_id:
                            location_to_save = loc
                            break
                    if location_to_save:
                        new_entry_line = f"{new_saved_id}|1|{location_to_save['location_id']}|{location_to_save['location_name']}|0\n"
                        try:
                            with open(os.path.join(DATA_DIR, 'saved_locations.txt'), 'a', encoding='utf-8') as f:
                                f.write(new_entry_line)
                        except IOError:
                            pass
                        # Reload saved locations
                        saved_locations_raw = load_saved_locations()
                        saved_locations = [{'location_id': s['location_id'], 'location_name': s['location_name']} for s in saved_locations_raw]

    return render_template('location_search.html',
                           search_query=search_query,
                           search_results=search_results,
                           saved_locations=saved_locations)


@app.route('/alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = load_alerts()
    locations = load_locations()

    severity_filter = 'All'
    location_filter = None

    if request.method == 'POST':
        severity_filter_post = request.form.get('severity_filter')
        if severity_filter_post in ['All', 'Critical', 'High', 'Medium', 'Low']:
            severity_filter = severity_filter_post

        loc_filter_str = request.form.get('location_filter')
        try:
            location_filter = int(loc_filter_str)
        except (TypeError, ValueError):
            location_filter = None

        # Check for acknowledgements of alert (POST param acknowledge_alert_id)
        acknowledge_alert_id_str = request.form.get('acknowledge_alert_id')
        if acknowledge_alert_id_str:
            try:
                acknowledge_alert_id = int(acknowledge_alert_id_str)
                # Mark alert as acknowledged by updating file (load, modify, write back)
                updated_alerts = []
                file_path = os.path.join(DATA_DIR, 'alerts.txt')
                for alert in alerts:
                    if alert['alert_id'] == acknowledge_alert_id:
                        alert['is_acknowledged'] = True
                    updated_alerts.append(alert)
                # Write back to alerts.txt
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        for alert in updated_alerts:
                            line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{int(alert['is_acknowledged'])}\n"
                            f.write(line)
                    alerts = updated_alerts
                except IOError:
                    pass
            except ValueError:
                pass

    filtered_alerts = filter_alerts(alerts, severity_filter, location_filter)

    return render_template('weather_alerts.html',
                           alerts_list=filtered_alerts,
                           severity_filter=severity_filter,
                           location_filter=location_filter)


@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = load_locations()
    air_quality_data = load_air_quality()

    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    selected_location_id = None
    if request.method == 'POST':
        try:
            selected_location_id = int(request.form.get('location_id', '').strip())
        except (ValueError, AttributeError):
            selected_location_id = None

    if selected_location_id is None and locations_list:
        selected_location_id = locations_list[0]['location_id']

    aqi_entry = None
    for aqi in air_quality_data:
        if aqi['location_id'] == selected_location_id:
            aqi_entry = aqi
            break

    if aqi_entry is None:
        # Provide empty or default values
        aqi_index = 0
        aqi_description = ''
        pollution_details = {'pm25': 0.0, 'pm10': 0.0, 'no2': 0.0, 'o3': 0.0}
        health_recommendation = ''
    else:
        aqi_index = aqi_entry['aqi_index']
        aqi_description = get_aqi_description(aqi_index)
        pollution_details = {
            'pm25': aqi_entry['pm25'],
            'pm10': aqi_entry['pm10'],
            'no2': aqi_entry['no2'],
            'o3': aqi_entry['o3']
        }
        health_recommendation = get_health_recommendation(aqi_description)

    return render_template('air_quality.html',
                           locations=locations_list,
                           selected_location_id=selected_location_id,
                           aqi_index=aqi_index,
                           aqi_description=aqi_description,
                           pollution_details=pollution_details,
                           health_recommendation=health_recommendation)


@app.route('/locations/saved', methods=['GET', 'POST'])
def saved_locations():
    saved_locations_raw = load_saved_locations()
    current_weather_data = load_current_weather()

    saved_locations_list = []

    if request.method == 'POST':
        # Possible actions: remove or add handled on location_search
        remove_location_id_str = request.form.get('remove_location_id')
        if remove_location_id_str:
            try:
                remove_location_id = int(remove_location_id_str)
                # Remove saved location by re-writing saved_locations.txt without this entry
                updated_saved = [s for s in saved_locations_raw if s['location_id'] != remove_location_id]
                file_path = os.path.join(DATA_DIR, 'saved_locations.txt')
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        for s in updated_saved:
                            line = f"{s['saved_id']}|{s['user_id']}|{s['location_id']}|{s['location_name']}|{int(s['is_default'])}\n"
                            f.write(line)
                    saved_locations_raw = updated_saved
                except IOError:
                    pass
            except ValueError:
                pass

    # Compose saved locations with current temp and condition
    # For each saved location, find current weather
    for s in saved_locations_raw:
        found_weather = next((w for w in current_weather_data if w['location_id'] == s['location_id']), None)
        current_temp = found_weather['temperature'] if found_weather else 0
        condition = found_weather['condition'] if found_weather else ''
        saved_locations_list.append({
            'location_id': s['location_id'],
            'location_name': s['location_name'],
            'current_temp': current_temp,
            'condition': condition
        })

    return render_template('saved_locations.html', saved_locations=saved_locations_list)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = load_locations()
    saved_locations_raw = load_saved_locations()

    temperature_units = temperature_units_options()

    # Defaults
    selected_temperature_unit = "Fahrenheit"
    selected_default_location_id = None
    alert_notifications_enabled = False

    # Determine current default location from saved_locations
    default_saved = get_saved_location_default(saved_locations_raw)
    if default_saved:
        selected_default_location_id = default_saved['location_id']

    if request.method == 'POST':
        # Get form values
        selected_temperature_unit_post = request.form.get('temperature_unit')
        if selected_temperature_unit_post in temperature_units:
            selected_temperature_unit = selected_temperature_unit_post

        try:
            selected_default_location_id_post = int(request.form.get('default_location_id', '').strip())
        except (ValueError, TypeError):
            selected_default_location_id_post = None
        if selected_default_location_id_post is not None:
            # Check if location id exists
            if any(loc['location_id'] == selected_default_location_id_post for loc in locations):
                selected_default_location_id = selected_default_location_id_post

        alert_notifications_enabled_post = request.form.get('alert_notifications_enabled')
        alert_notifications_enabled = bool(alert_notifications_enabled_post)

        # For simplicity, we only mimic save operation; not persisting to file as per spec
        pass

    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('settings.html',
                           temperature_units_options=temperature_units,
                           selected_temperature_unit=selected_temperature_unit,
                           locations=locations_list,
                           selected_default_location_id=selected_default_location_id if selected_default_location_id is not None else 0,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
