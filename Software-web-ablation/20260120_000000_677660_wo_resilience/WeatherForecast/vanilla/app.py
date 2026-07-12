from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from files

def load_current_weather():
    data = []
    path = "data/current_weather.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                record = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'temperature': int(parts[2]),
                    'condition': parts[3],
                    'humidity': int(parts[4]),
                    'wind_speed': int(parts[5]),
                    'last_updated': parts[6]
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_forecasts():
    data = []
    path = "data/forecasts.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                record = {
                    'forecast_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'date': parts[2],
                    'high_temp': int(parts[3]),
                    'low_temp': int(parts[4]),
                    'condition': parts[5],
                    'precipitation': int(parts[6]),
                    'humidity': int(parts[7])
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_locations():
    data = []
    path = "data/locations.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                record = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'latitude': float(parts[2]),
                    'longitude': float(parts[3]),
                    'country': parts[4],
                    'timezone': parts[5]
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_alerts():
    data = []
    path = "data/alerts.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                record = {
                    'alert_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'alert_type': parts[2],
                    'severity': parts[3],
                    'description': parts[4],
                    'start_time': parts[5],
                    'end_time': parts[6],
                    'is_acknowledged': int(parts[7])
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_air_quality():
    data = []
    path = "data/air_quality.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                record = {
                    'aqi_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'aqi_index': int(parts[2]),
                    'pm25': float(parts[3]),
                    'pm10': float(parts[4]),
                    'no2': float(parts[5]),
                    'o3': float(parts[6]),
                    'last_updated': parts[7]
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_saved_locations():
    data = []
    path = "data/saved_locations.txt"
    if not os.path.exists(path):
        return data
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                record = {
                    'saved_id': int(parts[0]),
                    'user_id': int(parts[1]),
                    'location_id': int(parts[2]),
                    'location_name': parts[3],
                    'is_default': int(parts[4])
                }
                data.append(record)
    except Exception:
        pass
    return data


def load_settings():
    # Since settings are not backed by a file in spec, we use default static values
    # Could be extended to load/save settings if required
    default_settings = {
        'temperature_unit': 'Celsius',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }
    # We can infer default_location_id from saved_locations marked is_default=1
    saved_locs = load_saved_locations()
    for loc in saved_locs:
        if loc.get('is_default', 0) == 1:
            default_settings['default_location_id'] = loc['location_id']
            break
    # If none found, choose first location if any
    if default_settings['default_location_id'] is None:
        locations = load_locations()
        if locations:
            default_settings['default_location_id'] = locations[0]['location_id']
    return default_settings


# Routes

@app.route('/')
def root_redirect():
    # Redirects to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    saved_locations = load_saved_locations()
    current_weather_data = load_current_weather()

    # Determine the default location from saved locations
    default_location_id = None
    for loc in saved_locations:
        if loc.get('is_default', 0) == 1:
            default_location_id = loc['location_id']
            break
    # If no default, pick first saved location's id if any
    if default_location_id is None and saved_locations:
        default_location_id = saved_locations[0]['location_id']

    # Find current weather for the default location
    current_weather = None
    if current_weather_data and default_location_id is not None:
        for w in current_weather_data:
            if w['location_id'] == default_location_id:
                current_weather = w
                break
    # If no weather found, use empty dict
    if current_weather is None:
        current_weather = {
            'location_id': default_location_id if default_location_id else 0,
            'location_name': '',
            'temperature': 0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }

    return render_template('dashboard.html', current_weather=current_weather)


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weather_data = load_current_weather()
    weather = None
    for w in current_weather_data:
        if w['location_id'] == location_id:
            weather = w
            break
    if weather is None:
        weather = {
            'location_id': location_id,
            'location_name': '',
            'temperature': 0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }
    return render_template('current_weather.html', weather=weather)


@app.route('/forecast/weekly', methods=['GET', 'POST'])
def weekly_forecast():
    location_list = load_locations()
    forecasts = load_forecasts()

    selected_location_id = None
    if request.method == 'POST':
        # Expect form key 'selected_location_id'
        try:
            selected_location_id = int(request.form.get('selected_location_id', 0))
        except ValueError:
            selected_location_id = None
    else:
        # Try from query string param
        try:
            selected_location_id = int(request.args.get('location_id', 0))
        except (ValueError, TypeError):
            selected_location_id = None

    if selected_location_id is None or selected_location_id == 0:
        # Default to first location if any
        if location_list:
            selected_location_id = location_list[0]['location_id']
        else:
            selected_location_id = 0

    # Filter forecast entries for selected_location_id
    forecast_list = [f for f in forecasts if f['location_id'] == selected_location_id]

    return render_template('weekly_forecast.html', location_list=location_list, selected_location_id=selected_location_id, forecast_list=forecast_list)


@app.route('/search/locations', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locations = load_saved_locations()
    search_results = []

    if request.method == 'POST':
        # Search form submission - get search term
        search_term = request.form.get('search_query', '').strip().lower()

        if search_term:
            # Check if search term can be parsed as lat,long
            if ',' in search_term:
                parts = [p.strip() for p in search_term.split(',')]
                if len(parts) == 2:
                    try:
                        lat = float(parts[0])
                        lon = float(parts[1])
                        # filter locations by proximity within some tolerance (e.g., 1 degree)
                        search_results = [loc for loc in locations if abs(loc['latitude'] - lat) <= 1.0 and abs(loc['longitude'] - lon) <= 1.0]
                    except ValueError:
                        # invalid lat/lon, no results
                        search_results = []
                else:
                    search_results = []
            else:
                # Search by location_name contains search_term
                search_results = [loc for loc in locations if search_term in loc['location_name'].lower()]
        else:
            search_results = []

    # GET request shows no results initially
    return render_template('location_search.html', search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts', methods=['GET'])
def weather_alerts():
    # Filters by query string
    severity_filter = request.args.get('severity_filter', '').strip()
    location_filter_raw = request.args.get('location_filter_alerts', None)
    location_filter_alerts = None
    try:
        if location_filter_raw is not None:
            location_filter_alerts = int(location_filter_raw)
    except ValueError:
        location_filter_alerts = None

    alerts = load_alerts()

    # Filter alerts by severity if provided and non-empty
    if severity_filter:
        alerts = [a for a in alerts if a['severity'].lower() == severity_filter.lower()]

    # Filter alerts by location if provided
    if location_filter_alerts is not None and location_filter_alerts != 0:
        alerts = [a for a in alerts if a['location_id'] == location_filter_alerts]

    return render_template('alerts.html', alerts=alerts, severity_filter=severity_filter, location_filter_alerts=location_filter_alerts)


@app.route('/airquality', methods=['GET'])
def air_quality():
    location_list = load_locations()
    air_quality_data_list = load_air_quality()

    # We accept an optional query parameter for location
    location_filter_raw = request.args.get('location_id', None)
    location_id_selected = None
    try:
        if location_filter_raw is not None:
            location_id_selected = int(location_filter_raw)
    except ValueError:
        location_id_selected = None

    # If no location selected, default to first location in list
    if location_id_selected is None:
        if location_list:
            location_id_selected = location_list[0]['location_id']

    # Find air quality data for location_id_selected
    air_quality_data = None
    if air_quality_data_list and location_id_selected is not None:
        for aqi in air_quality_data_list:
            if aqi['location_id'] == location_id_selected:
                air_quality_data = aqi
                break
    # If none found, default empty dict
    if air_quality_data is None:
        air_quality_data = {
            'aqi_id': 0,
            'location_id': location_id_selected if location_id_selected else 0,
            'aqi_index': 0,
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }

    return render_template('air_quality.html', air_quality_data=air_quality_data, location_list=location_list)


@app.route('/locations/saved', methods=['GET'])
def saved_locations():
    saved_locations = load_saved_locations()
    current_weather_data = load_current_weather()

    # Build a map for quick weather lookup
    weather_map = {}
    for w in current_weather_data:
        weather_map[w['location_id']] = w

    # current_weather_data is list of dicts with location_id, temperature, condition for saved locations
    current_weather_for_saved = []
    for loc in saved_locations:
        weather = weather_map.get(loc['location_id'], None)
        if weather:
            current_weather_for_saved.append({
                'location_id': loc['location_id'],
                'temperature': weather.get('temperature', 0),
                'condition': weather.get('condition', '')
            })
        else:
            current_weather_for_saved.append({
                'location_id': loc['location_id'],
                'temperature': 0,
                'condition': ''
            })

    return render_template('saved_locations.html', saved_locations=saved_locations, current_weather_data=current_weather_for_saved)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    location_list = load_locations()
    settings = load_settings()

    if request.method == 'POST':
        # Update settings from form
        temperature_unit = request.form.get('temperature_unit', 'Celsius')
        # Get default_location_id from form
        try:
            default_location_id = int(request.form.get('default_location_id', 0))
        except ValueError:
            default_location_id = None
        # alert_notifications_enabled is checkbox, 'on' means True, None means False
        alert_notifications_enabled = request.form.get('alert_notifications_enabled') == 'on' or request.form.get('alert_notifications_enabled') == '1'

        # NOTE: Spec does not mention permanent save, we just update settings dict in memory
        settings['temperature_unit'] = temperature_unit
        if default_location_id in [loc['location_id'] for loc in location_list]:
            settings['default_location_id'] = default_location_id

        settings['alert_notifications_enabled'] = alert_notifications_enabled

    return render_template('settings.html', settings=settings, location_list=location_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
