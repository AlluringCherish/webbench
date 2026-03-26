from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_FOLDER = 'data'

# Data Loader Functions

def load_current_weather():
    path = os.path.join(DATA_FOLDER, 'current_weather.txt')
    current_weather = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
                    cw = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'temperature': int(parts[2]),
                        'condition': parts[3],
                        'humidity': int(parts[4]),
                        'wind_speed': int(parts[5]),
                        'last_updated': parts[6]
                    }
                    current_weather.append(cw)
                except ValueError:
                    continue
    except Exception:
        pass
    return current_weather


def load_forecasts():
    path = os.path.join(DATA_FOLDER, 'forecasts.txt')
    forecasts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    fc = {
                        'forecast_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'date': parts[2],
                        'high_temp': int(parts[3]),
                        'low_temp': int(parts[4]),
                        'condition': parts[5],
                        'precipitation': int(parts[6]),
                        'humidity': int(parts[7])
                    }
                    forecasts.append(fc)
                except ValueError:
                    continue
    except Exception:
        pass
    return forecasts


def load_locations():
    path = os.path.join(DATA_FOLDER, 'locations.txt')
    locations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    loc = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'latitude': float(parts[2]),
                        'longitude': float(parts[3]),
                        'country': parts[4],
                        'timezone': parts[5]
                    }
                    locations.append(loc)
                except ValueError:
                    continue
    except Exception:
        pass
    return locations


def load_alerts():
    path = os.path.join(DATA_FOLDER, 'alerts.txt')
    alerts = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
                        'is_acknowledged': bool(int(parts[7]))
                    }
                    alerts.append(alert)
                except ValueError:
                    continue
    except Exception:
        pass
    return alerts


def load_air_quality():
    path = os.path.join(DATA_FOLDER, 'air_quality.txt')
    air_quality = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    aq = {
                        'aqi_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'aqi_index': int(parts[2]),
                        'pm25': float(parts[3]),
                        'pm10': float(parts[4]),
                        'no2': float(parts[5]),
                        'o3': float(parts[6]),
                        'last_updated': parts[7]
                    }
                    air_quality.append(aq)
                except ValueError:
                    continue
    except Exception:
        pass
    return air_quality


def load_saved_locations():
    path = os.path.join(DATA_FOLDER, 'saved_locations.txt')
    saved_locations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    saved = {
                        'saved_id': int(parts[0]),
                        'user_id': int(parts[1]),
                        'location_id': int(parts[2]),
                        'location_name': parts[3],
                        'is_default': bool(int(parts[4]))
                    }
                    saved_locations.append(saved)
                except ValueError:
                    continue
    except Exception:
        pass
    return saved_locations


# Helper functions

def get_saved_location_default(saved_locs):
    for loc in saved_locs:
        if loc.get('is_default', False):
            return loc
    return saved_locs[0] if saved_locs else None


def get_location_by_id(locations, location_id):
    for loc in locations:
        if loc.get('location_id') == location_id:
            return loc
    return None


def get_current_weather_by_location_id(current_weather, location_id):
    for cw in current_weather:
        if cw.get('location_id') == location_id:
            return cw
    return None


def get_forecasts_by_location_id(forecasts, location_id):
    return [f for f in forecasts if f.get('location_id') == location_id]


def get_alerts_filtered(alerts, severity_filter, location_filter):
    filtered = []
    for alert in alerts:
        if severity_filter != 'All' and alert.get('severity') != severity_filter:
            continue
        if location_filter is not None and alert.get('location_id') != location_filter:
            continue
        filtered.append(alert)
    return filtered


def get_air_quality_by_location_id(air_quality, location_id):
    for aq in air_quality:
        if aq.get('location_id') == location_id:
            return aq
    return None


def get_saved_locations_by_user(saved_locations, user_id=1):
    # The spec assumes default user_id=1 since no auth
    return [sl for sl in saved_locations if sl.get('user_id') == user_id]


def get_temperature_units():
    return ["Celsius", "Fahrenheit", "Kelvin"]


def get_health_recommendation_for_aqi(aqi_index):
    if aqi_index <= 50:
        return "Air quality is good. No precautions needed."
    elif aqi_index <= 100:
        return "Air quality is moderate. Unusually sensitive individuals should consider limiting prolonged outdoor exertion."
    elif aqi_index <= 150:
        return "Air quality is unhealthy for sensitive groups. People with respiratory or heart disease should limit prolonged exertion."
    elif aqi_index <= 200:
        return "Air quality is unhealthy. Everyone may begin to experience health effects; sensitive groups may experience more serious effects."
    elif aqi_index <= 300:
        return "Air quality is very unhealthy. Health warnings of emergency conditions."
    else:
        return "Air quality is hazardous. Everyone should avoid all outdoor exertion."


# Routes

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    saved_locations = load_saved_locations()
    current_weather = load_current_weather()

    # Get default saved location for user 1
    saved_for_user = get_saved_locations_by_user(saved_locations, user_id=1)
    default_loc = get_saved_location_default(saved_for_user)

    default_location = None
    if default_loc:
        # Find current weather for that location
        cw = get_current_weather_by_location_id(current_weather, default_loc['location_id'])
        if cw:
            default_location = {
                'location_id': cw['location_id'],
                'location_name': cw['location_name'],
                'temperature': cw['temperature'],
                'condition': cw['condition'],
                'humidity': cw['humidity'],
                'wind_speed': cw['wind_speed'],
                'last_updated': cw['last_updated']
            }
    
    # If no default location or weather data found, fallback to None dict with defaults
    if default_location is None:
        default_location = {
            'location_id': 0,
            'location_name': 'No Default Location',
            'temperature': 0,
            'condition': 'N/A',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }

    return render_template('dashboard.html', default_location=default_location)


@app.route('/weather/current/<int:location_id>', methods=['GET'])
def current_weather(location_id):
    locations = load_locations()
    current_weather_data = load_current_weather()

    location = get_location_by_id(locations, location_id)
    cw = get_current_weather_by_location_id(current_weather_data, location_id)

    # Prepare context variables
    location_dict = {'location_id': location_id, 'location_name': ''}
    temperature = 0
    condition = ''
    humidity = 0
    wind_speed = 0

    if location:
        location_dict['location_name'] = location.get('location_name', '')
    if cw:
        temperature = cw.get('temperature', 0)
        condition = cw.get('condition', '')
        humidity = cw.get('humidity', 0)
        wind_speed = cw.get('wind_speed', 0)

    return render_template('current_weather.html', location=location_dict, temperature=temperature, condition=condition, humidity=humidity, wind_speed=wind_speed)


@app.route('/forecast/weekly', methods=['GET', 'POST'])
def weekly_forecast():
    locations = load_locations()
    forecasts = load_forecasts()
    selected_location_id = None

    if request.method == 'POST':
        # Expect post with 'location_id' selected
        loc_str = request.form.get('location_id')
        try:
            selected_location_id = int(loc_str)
        except (ValueError, TypeError):
            selected_location_id = None
    
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    filtered_forecasts = []
    if selected_location_id is not None:
        filtered_forecasts = get_forecasts_by_location_id(forecasts, selected_location_id)

    return render_template('weekly_forecast.html', locations=locations, selected_location_id=selected_location_id, forecasts=filtered_forecasts)


@app.route('/locations/search', methods=['GET', 'POST'])
def search_locations():
    locations = load_locations()
    saved_locations_all = load_saved_locations()
    saved_locations = get_saved_locations_by_user(saved_locations_all, user_id=1)

    search_query = ''
    search_results = []

    if request.method == 'POST':
        # May be search or selection of location to save
        if 'search_query' in request.form:
            search_query = request.form.get('search_query', '').strip()
            if search_query:
                # Case insensitive substring match on location_name
                search_lower = search_query.lower()
                for loc in locations:
                    if search_lower in loc['location_name'].lower():
                        search_results.append(loc)
        elif 'select_location_id' in request.form:
            # Simulate saving location for user 1; no duplicate; add to saved_locations.txt
            try:
                select_location_id = int(request.form.get('select_location_id'))
            except (ValueError, TypeError):
                select_location_id = None

            if select_location_id is not None:
                # Check if already saved
                already_saved = any(sl['location_id'] == select_location_id for sl in saved_locations)
                if not already_saved:
                    # Find location info
                    loc_to_save = get_location_by_id(locations, select_location_id)
                    if loc_to_save:
                        # Append directly to file
                        try:
                            # Determine next saved_id
                            max_id = 0
                            for sl in saved_locations_all:
                                if sl.get('saved_id', 0) > max_id:
                                    max_id = sl['saved_id']
                            next_saved_id = max_id + 1
                            # Since user_id is always 1
                            line = f"{next_saved_id}|1|{loc_to_save['location_id']}|{loc_to_save['location_name']}|0\n"
                            with open(os.path.join(DATA_FOLDER, 'saved_locations.txt'), 'a', encoding='utf-8') as f:
                                f.write(line)
                            # Reload saved locations
                            saved_locations_all = load_saved_locations()
                            saved_locations = get_saved_locations_by_user(saved_locations_all, user_id=1)
                        except Exception:
                            pass

    return render_template('location_search.html', search_query=search_query,
                           search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts_all = load_alerts()
    locations = load_locations()

    severity_filter = 'All'
    location_filter = None

    if request.method == 'POST':
        # Can be filter form or acknowledgement
        if 'severity_filter' in request.form:
            severity_filter_post = request.form.get('severity_filter', 'All')
            if severity_filter_post in ["All", "Critical", "High", "Medium", "Low"]:
                severity_filter = severity_filter_post
            loc_filter_str = request.form.get('location_filter')
            try:
                location_filter = int(loc_filter_str) if loc_filter_str and loc_filter_str != '' else None
            except (ValueError, TypeError):
                location_filter = None
        elif 'acknowledge_alert_id' in request.form:
            # Mark alert as acknowledged (writeback is not required by spec, so only simulate)
            try:
                ack_id = int(request.form.get('acknowledge_alert_id'))
            except (ValueError, TypeError):
                ack_id = None
            if ack_id is not None:
                # For this app implementation we just mark in memory
                for alert in alerts_all:
                    if alert['alert_id'] == ack_id:
                        alert['is_acknowledged'] = True
                        break

    filtered_alerts = get_alerts_filtered(alerts_all, severity_filter, location_filter)

    return render_template('weather_alerts.html', alerts=filtered_alerts, severity_filter=severity_filter, location_filter=location_filter, locations=locations)


@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = load_locations()
    air_quality_data = load_air_quality()

    selected_location_id = None
    if request.method == 'POST':
        loc_str = request.form.get('location_filter')
        try:
            selected_location_id = int(loc_str)
        except (ValueError, TypeError):
            selected_location_id = None

    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    aqi_info = get_air_quality_by_location_id(air_quality_data, selected_location_id)
    if aqi_info is None:
        # Provide default empty data
        aqi_info = {
            'aqi_index': 0,
            'aqi_description': 'No Data',
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }
    else:
        aqi_index = aqi_info.get('aqi_index', 0)
        aqi_info['aqi_description'] = get_health_recommendation_for_aqi(aqi_index)

    health_recommendation = get_health_recommendation_for_aqi(aqi_info.get('aqi_index', 0))

    return render_template('air_quality.html', locations=locations, selected_location_id=selected_location_id, aqi_info=aqi_info, health_recommendation=health_recommendation)


@app.route('/locations/saved', methods=['GET', 'POST'])
def saved_locations():
    saved_locations_all = load_saved_locations()
    current_weather = load_current_weather()
    locations = load_locations()

    saved_locations_user = get_saved_locations_by_user(saved_locations_all, user_id=1)

    if request.method == 'POST':
        # May be remove location or set default
        if 'remove_location_id' in request.form:
            try:
                remove_id = int(request.form.get('remove_location_id'))
            except (ValueError, TypeError):
                remove_id = None

            if remove_id is not None:
                # Remove from saved_locations.txt (must be writeback)
                try:
                    # Filter out the location to remove
                    new_saved = [sl for sl in saved_locations_all if not (sl['location_id'] == remove_id and sl['user_id'] == 1)]
                    # Write all back
                    with open(os.path.join(DATA_FOLDER, 'saved_locations.txt'), 'w', encoding='utf-8') as f:
                        for sl in new_saved:
                            line = f"{sl['saved_id']}|{sl['user_id']}|{sl['location_id']}|{sl['location_name']}|{int(sl['is_default'])}\n"
                            f.write(line)
                    saved_locations_all = new_saved
                    saved_locations_user = get_saved_locations_by_user(saved_locations_all, user_id=1)
                except Exception:
                    pass

    # Below spec only shows remove and view, not default set or add new handling except UI link

    # Extend saved locations data with is_default and current weather if possible
    saved_locations_out = []
    cw_map = {cw['location_id']: cw for cw in current_weather}
    for sl in saved_locations_user:
        loc_name = sl.get('location_name', '')
        is_default = sl.get('is_default', False)
        # We provide saved_id, user_id, location_id, location_name, is_default
        saved_locations_out.append({
            'saved_id': sl.get('saved_id'),
            'user_id': sl.get('user_id'),
            'location_id': sl.get('location_id'),
            'location_name': loc_name,
            'is_default': is_default
        })

    return render_template('saved_locations.html', saved_locations=saved_locations_out)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Settings storing is not specified (no file), so store in session or in-memory defaults for the duration of runtime
    # We'll store settings in a global dict for this runtime only

    global_settings = {
        'selected_unit': 'Celsius',
        'selected_default_location_id': None,
        'alert_notifications_enabled': True
    }

    # We use app config or global variable to simulate persistent storage
    if not hasattr(app, 'user_settings'):
        app.user_settings = global_settings.copy()

    locations = load_locations()

    # If no default location selected, pick first if exists
    if app.user_settings['selected_default_location_id'] is None and locations:
        app.user_settings['selected_default_location_id'] = locations[0]['location_id']

    if request.method == 'POST':
        unit = request.form.get('temperature_unit')
        default_loc_str = request.form.get('default_location_id')
        alert_enabled = request.form.get('alert_notifications_enabled')

        if unit in get_temperature_units():
            app.user_settings['selected_unit'] = unit

        try:
            default_loc_id = int(default_loc_str)
            if get_location_by_id(locations, default_loc_id):
                app.user_settings['selected_default_location_id'] = default_loc_id
        except (ValueError, TypeError):
            pass

        # Checkbox will be 'on' if checked, None if unchecked
        app.user_settings['alert_notifications_enabled'] = (alert_enabled == 'on')

    temperature_units = get_temperature_units()
    selected_unit = app.user_settings['selected_unit']
    selected_default_location_id = app.user_settings['selected_default_location_id']
    alert_notifications_enabled = app.user_settings['alert_notifications_enabled']

    return render_template('settings.html', temperature_units=temperature_units, selected_unit=selected_unit,
                           locations=locations, selected_default_location_id=selected_default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
