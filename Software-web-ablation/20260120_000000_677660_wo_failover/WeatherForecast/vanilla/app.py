from flask import Flask, render_template, redirect, url_for, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file config with environment variable fallback
DATA_DIR = os.environ.get('WEATHER_DATA_DIR', 'data')
CURRENT_WEATHER_FILE = os.path.join(DATA_DIR, 'current_weather.txt')
FORECASTS_FILE = os.path.join(DATA_DIR, 'forecasts.txt')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.txt')
ALERTS_FILE = os.path.join(DATA_DIR, 'alerts.txt')
AIR_QUALITY_FILE = os.path.join(DATA_DIR, 'air_quality.txt')
SAVED_LOCATIONS_FILE = os.path.join(DATA_DIR, 'saved_locations.txt')

# -------------------------------------
# Helper functions to load data
# -------------------------------------

def load_current_weather():
    current_weather_list = []
    if not os.path.exists(CURRENT_WEATHER_FILE):
        return current_weather_list
    try:
        with open(CURRENT_WEATHER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                try:
                    weather = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'temperature': int(parts[2]),
                        'condition': parts[3],
                        'humidity': int(parts[4]),
                        'wind_speed': int(parts[5]),
                        'last_updated': parts[6]
                    }
                    current_weather_list.append(weather)
                except ValueError:
                    continue
    except Exception:
        pass
    return current_weather_list


def load_forecasts():
    forecasts_list = []
    if not os.path.exists(FORECASTS_FILE):
        return forecasts_list
    try:
        with open(FORECASTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    forecast = {
                        'forecast_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'date': parts[2],
                        'high_temp': int(parts[3]),
                        'low_temp': int(parts[4]),
                        'condition': parts[5],
                        'precipitation': int(parts[6]),
                        'humidity': int(parts[7])
                    }
                    forecasts_list.append(forecast)
                except ValueError:
                    continue
    except Exception:
        pass
    return forecasts_list


def load_locations():
    locations_list = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations_list
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
                    location = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'latitude': float(parts[2]),
                        'longitude': float(parts[3]),
                        'country': parts[4],
                        'timezone': parts[5]
                    }
                    locations_list.append(location)
                except ValueError:
                    continue
    except Exception:
        pass
    return locations_list


def load_alerts():
    alerts_list = []
    if not os.path.exists(ALERTS_FILE):
        return alerts_list
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
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
                        'is_acknowledged': int(parts[7])
                    }
                    alerts_list.append(alert)
                except ValueError:
                    continue
    except Exception:
        pass
    return alerts_list


def load_air_quality():
    air_quality_list = []
    if not os.path.exists(AIR_QUALITY_FILE):
        return air_quality_list
    try:
        with open(AIR_QUALITY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    air_quality = {
                        'aqi_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'aqi_index': int(parts[2]),
                        'pm25': float(parts[3]),
                        'pm10': float(parts[4]),
                        'no2': float(parts[5]),
                        'o3': float(parts[6]),
                        'last_updated': parts[7]
                    }
                    air_quality_list.append(air_quality)
                except ValueError:
                    continue
    except Exception:
        pass
    return air_quality_list


def load_saved_locations():
    saved_locations_list = []
    if not os.path.exists(SAVED_LOCATIONS_FILE):
        return saved_locations_list
    try:
        with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    saved_location = {
                        'saved_id': int(parts[0]),
                        'user_id': int(parts[1]),
                        'location_id': int(parts[2]),
                        'location_name': parts[3],
                        'is_default': int(parts[4])
                    }
                    saved_locations_list.append(saved_location)
                except ValueError:
                    continue
    except Exception:
        pass
    return saved_locations_list

# Helper to save saved_locations list to file for persistence on save/remove

def save_saved_locations(saved_locations_list):
    try:
        with open(SAVED_LOCATIONS_FILE, 'w', encoding='utf-8') as f:
            for loc in saved_locations_list:
                line = f"{loc['saved_id']}|{loc['user_id']}|{loc['location_id']}|{loc['location_name']}|{loc['is_default']}\n"
                f.write(line)
    except Exception:
        pass

# -------------------------------------
# Route Implementations
# -------------------------------------

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Load saved locations to find default location
    saved_locations = load_saved_locations()
    default_location = None
    for loc in saved_locations:
        if loc.get('is_default', 0) == 1:
            default_location = loc
            break
    current_weather_list = load_current_weather()
    # If no default location, try arbitrary first saved location
    if not default_location and saved_locations:
        default_location = saved_locations[0]
    # Find current weather for default location
    current_weather = None
    if default_location:
        for weather in current_weather_list:
            if weather['location_id'] == default_location['location_id']:
                current_weather = weather
                break
    # If no weather found for default location, fallback to first current weather entry
    if not current_weather and current_weather_list:
        current_weather = current_weather_list[0]
    # If still none, fill with empty dict
    if not current_weather:
        current_weather = {
            'location_id': 0,
            'location_name': '',
            'temperature': 0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }
    return render_template('dashboard.html', current_weather=current_weather)


@app.route('/weather/current/<int:location_id>')
def current_weather_page(location_id):
    current_weather_list = load_current_weather()
    # Find weather for location_id
    weather = None
    for w in current_weather_list:
        if w['location_id'] == location_id:
            weather = w
            break
    # If not found, empty dict with location info if possible
    if not weather:
        # Try fallback location_name from locations
        locations = load_locations()
        location_name = ''
        for loc in locations:
            if loc['location_id'] == location_id:
                location_name = loc['location_name']
                break
        weather = {
            'location_id': location_id,
            'location_name': location_name,
            'temperature': 0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }
    return render_template('current_weather.html', weather=weather)


@app.route('/forecast/weekly')
def weekly_forecast_page():
    # Query parameter for location_id filter
    location_id = request.args.get('location_id', type=int)

    forecasts = load_forecasts()
    filtered_forecasts = []
    if location_id is None:
        # If no filter, just show empty forecast list
        filtered_forecasts = []
    else:
        filtered_forecasts = [fc for fc in forecasts if fc['location_id'] == location_id]

    saved_locations = load_saved_locations()  # for location dropdown

    return render_template('weekly_forecast.html', location_id=location_id if location_id else 0, forecasts=filtered_forecasts, saved_locations=saved_locations)


@app.route('/locations/search', methods=['GET', 'POST'])
def location_search_page():
    saved_locations = load_saved_locations()
    search_results = []
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        all_locations = load_locations()
        # search by location_name case insensitive substring
        if search_query:
            for loc in all_locations:
                if search_query in loc['location_name'].lower():
                    search_results.append(loc)
    else:
        # On GET no search results
        search_results = []

    return render_template('location_search.html', search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts')
def alerts_page():
    severity_filter = request.args.get('severity_filter', '', type=str)
    location_filter = request.args.get('location_filter', 0, type=int)

    alerts = load_alerts()

    # Filter alerts by severity if given
    if severity_filter:
        alerts = [a for a in alerts if a['severity'].lower() == severity_filter.lower()]
    # Filter alerts by location if given and non-zero
    if location_filter != 0:
        alerts = [a for a in alerts if a['location_id'] == location_filter]

    saved_locations = load_saved_locations()  # for location dropdown

    return render_template('alerts.html', alerts=alerts, severity_filter=severity_filter, location_filter=location_filter, saved_locations=saved_locations)


@app.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = load_alerts()
    updated = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            if alert['is_acknowledged'] == 0:
                alert['is_acknowledged'] = 1
                updated = True
            break
    if updated:
        # Save updated alerts back
        try:
            with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
                for alert in alerts:
                    line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{alert['is_acknowledged']}\n"
                    f.write(line)
        except Exception:
            pass

    # As per spec, no template return, either redirect or JSON response
    # We'll respond with JSON success status
    return jsonify({'alert_id': alert_id, 'acknowledged': updated})


@app.route('/airquality')
def air_quality_page():
    location_filter = request.args.get('location_filter', 0, type=int)
    air_quality_list = load_air_quality()
    if location_filter != 0:
        aq_filtered = [a for a in air_quality_list if a['location_id'] == location_filter]
    else:
        aq_filtered = air_quality_list

    saved_locations = load_saved_locations()  # for location dropdown

    return render_template('air_quality.html', air_quality=aq_filtered, location_filter=location_filter, saved_locations=saved_locations)


@app.route('/locations/saved')
def saved_locations_page():
    saved_locations = load_saved_locations()
    current_weather_list = load_current_weather()
    # Prepare weather_summary dictionary keyed by location_id
    weather_summary = {}
    for weather in current_weather_list:
        weather_summary[weather['location_id']] = {
            'temperature': weather['temperature'],
            'condition': weather['condition']
        }
    return render_template('saved_locations.html', saved_locations=saved_locations, weather_summary=weather_summary)


@app.route('/locations/save', methods=['POST'])
def add_new_location():
    # Form data expects location_id and location_name
    location_id = request.form.get('location_id', type=int)
    location_name = request.form.get('location_name', '')
    if not location_id or not location_name:
        # Bad request, ignore
        return redirect(url_for('location_search_page'))

    saved_locations = load_saved_locations()
    # Check if location already saved for user_id=1 (dummy user)
    already_saved = any(loc['location_id'] == location_id and loc['user_id'] == 1 for loc in saved_locations)
    if not already_saved:
        # Determine new saved_id
        new_saved_id = 1
        if saved_locations:
            new_saved_id = max(loc['saved_id'] for loc in saved_locations) + 1
        # is_default = 0 for added
        new_entry = {
            'saved_id': new_saved_id,
            'user_id': 1,
            'location_id': location_id,
            'location_name': location_name,
            'is_default': 0
        }
        saved_locations.append(new_entry)
        save_saved_locations(saved_locations)
    return redirect(url_for('location_search_page'))


@app.route('/locations/remove/<int:location_id>', methods=['POST'])
def remove_saved_location(location_id):
    saved_locations = load_saved_locations()
    # Filter out the location with location_id for user_id=1
    saved_locations = [loc for loc in saved_locations if not (loc['location_id'] == location_id and loc['user_id'] == 1)]
    save_saved_locations(saved_locations)
    return redirect(url_for('saved_locations_page'))


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    # Load saved_locations to find default location (user 1)
    saved_locations = load_saved_locations()
    # Defaults if no saved location
    default_location_id = 0
    for loc in saved_locations:
        if loc.get('user_id', 0) == 1 and loc.get('is_default', 0) == 1:
            default_location_id = loc['location_id']
            break

    # We need a settings storage. Since no db, we will store settings in a local file settings.txt
    settings_file = os.path.join(DATA_DIR, 'settings.txt')
    # Defaults
    temperature_units = 'Celsius'
    alert_notifications_enabled = False

    if request.method == 'POST':
        # Update settings
        temperature_units = request.form.get('temperature_units', 'Celsius')
        alert_notifications_enabled = True if request.form.get('alert_notifications_enabled') == 'on' else False
        new_default_location_id = request.form.get('default_location_id', type=int, default=0)

        # Update default location in saved_locations
        # Only one default allowed
        for loc in saved_locations:
            if loc['user_id'] == 1:
                loc['is_default'] = 1 if loc['location_id'] == new_default_location_id else 0
        save_saved_locations(saved_locations)
        default_location_id = new_default_location_id

        # Save settings to file
        try:
            with open(settings_file, 'w', encoding='utf-8') as sf:
                sf.write(f"temperature_units|{temperature_units}\n")
                sf.write(f"alert_notifications_enabled|{int(alert_notifications_enabled)}\n")
        except Exception:
            pass

    else:
        # On GET load settings if available
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as sf:
                    for line in sf:
                        parts = line.strip().split('|')
                        if len(parts) == 2:
                            key, value = parts
                            if key == 'temperature_units':
                                temperature_units = value
                            elif key == 'alert_notifications_enabled':
                                alert_notifications_enabled = (value == '1')
            except Exception:
                pass

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           default_location_id=default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled,
                           saved_locations=saved_locations)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
