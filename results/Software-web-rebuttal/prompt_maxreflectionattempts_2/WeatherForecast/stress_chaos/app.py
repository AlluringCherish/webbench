from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Utility functions to load data from files

def load_current_weather():
    filename = os.path.join(DATA_DIR, 'current_weather.txt')
    data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 7:
                    continue
                location_id = int(fields[0])
                data[location_id] = {
                    'location_id': location_id,
                    'location_name': fields[1],
                    'temperature': float(fields[2]),
                    'condition': fields[3],
                    'humidity': int(fields[4]),
                    'wind_speed': float(fields[5]),
                    'last_updated': fields[6]
                }
    except (IOError, ValueError):
        pass
    return data


def load_forecasts():
    filename = os.path.join(DATA_DIR, 'forecasts.txt')
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 8:
                    continue
                try:
                    forecast_id = int(fields[0])
                    location_id = int(fields[1])
                    forecast = {
                        'forecast_id': forecast_id,
                        'location_id': location_id,
                        'date': fields[2],
                        'high_temp': float(fields[3]),
                        'low_temp': float(fields[4]),
                        'condition': fields[5],
                        'precipitation': int(fields[6]),
                        'humidity': int(fields[7])
                    }
                    data.append(forecast)
                except ValueError:
                    continue
    except IOError:
        pass
    return data


def load_locations():
    filename = os.path.join(DATA_DIR, 'locations.txt')
    data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 6:
                    continue
                try:
                    location_id = int(fields[0])
                    data[location_id] = {
                        'location_id': location_id,
                        'location_name': fields[1],
                        'latitude': float(fields[2]),
                        'longitude': float(fields[3]),
                        'country': fields[4],
                        'timezone': fields[5]
                    }
                except ValueError:
                    continue
    except IOError:
        pass
    return data


def load_alerts():
    filename = os.path.join(DATA_DIR, 'alerts.txt')
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 8:
                    continue
                try:
                    alert_id = int(fields[0])
                    location_id = int(fields[1])
                    is_acknowledged = bool(int(fields[7]))
                    alert = {
                        'alert_id': alert_id,
                        'location_id': location_id,
                        'alert_type': fields[2],
                        'severity': fields[3],
                        'description': fields[4],
                        'start_time': fields[5],
                        'end_time': fields[6],
                        'is_acknowledged': is_acknowledged
                    }
                    data.append(alert)
                except ValueError:
                    continue
    except IOError:
        pass
    return data


def load_air_quality():
    filename = os.path.join(DATA_DIR, 'air_quality.txt')
    data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 8:
                    continue
                try:
                    aqi_id = int(fields[0])  # unused directly but mandatory parse
                    location_id = int(fields[1])
                    data[location_id] = {
                        'aqi_index': int(fields[2]),
                        'pm25': float(fields[3]),
                        'pm10': float(fields[4]),
                        'no2': float(fields[5]),
                        'o3': float(fields[6]),
                        'last_updated': fields[7]
                    }
                except ValueError:
                    continue
    except IOError:
        pass
    return data


def load_saved_locations():
    filename = os.path.join(DATA_DIR, 'saved_locations.txt')
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 5:
                    continue
                try:
                    saved_id = int(fields[0])
                    # user_id ignored
                    location_id = int(fields[2])
                    is_default = bool(int(fields[4]))
                    data.append({
                        'saved_id': saved_id,
                        'location_id': location_id,
                        'location_name': fields[3],
                        'is_default': is_default
                    })
                except ValueError:
                    continue
    except IOError:
        pass
    return data


def aqi_index_description(aqi):
    if aqi is None:
        return "Unknown"
    if 0 <= aqi <= 50:
        return "Good"
    if 51 <= aqi <= 100:
        return "Moderate"
    if 101 <= aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if 151 <= aqi <= 200:
        return "Unhealthy"
    if 201 <= aqi <= 300:
        return "Very Unhealthy"
    if 301 <= aqi <= 500:
        return "Hazardous"
    return "Unknown"


def health_recommendation_for_aqi(aqi):
    if aqi is None:
        return "No health recommendation available."
    if 0 <= aqi <= 50:
        return "Air quality is satisfactory, and air pollution poses little or no risk."
    if 51 <= aqi <= 100:
        return "Air quality is acceptable; some pollutants may be a moderate health concern for a very small number of people."
    if 101 <= aqi <= 150:
        return "Members of sensitive groups may experience health effects."
    if 151 <= aqi <= 200:
        return "Everyone may begin to experience health effects; sensitive groups may experience more serious effects."
    if 201 <= aqi <= 300:
        return "Health warnings of emergency conditions. The entire population is likely to be affected."
    if 301 <= aqi <= 500:
        return "Health alert: everyone may experience serious health effects."
    return "No health recommendation available."


# --- Routes Implementation ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    current_weather = load_current_weather()
    saved_locations_raw = load_saved_locations()

    # Pick default location from saved_locations
    default_location = None
    for saved in saved_locations_raw:
        if saved.get('is_default'):
            loc_id = saved.get('location_id')
            default_location = current_weather.get(loc_id)
            break

    if not default_location:
        # fallback first if any
        if saved_locations_raw and current_weather:
            loc_id = saved_locations_raw[0].get('location_id')
            default_location = current_weather.get(loc_id)

    # If still None, empty default
    if not default_location:
        default_location = {
            'location_id': 0,
            'location_name': '',
            'temperature': 0.0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0.0
        }

    # saved_locations list: only id and name
    saved_locations = [
        {'location_id': s['location_id'], 'location_name': s['location_name']} for s in saved_locations_raw
    ]

    return render_template('dashboard.html', default_location=default_location, saved_locations=saved_locations)


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id: int):
    current_weather_data = load_current_weather()
    locations = load_locations()

    location_info = locations.get(location_id)
    if not location_info:
        # Fallback minimal
        location_info = {'location_id': location_id, 'location_name': ''}

    weather_data = current_weather_data.get(location_id)
    if not weather_data:
        # fallback minimal with zeroed values except strings
        weather_data = {
            'temperature': 0.0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0.0,
            'last_updated': ''
        }

    return render_template('current_weather.html', location_info=location_info, weather_data=weather_data)


@app.route('/forecast/weekly')
def weekly_forecast():
    location_id_param = request.args.get('location_id', default=None, type=int)

    all_locations = load_locations()
    forecasts = load_forecasts()

    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in all_locations.values()]

    selected_location_id = location_id_param if location_id_param in all_locations else None

    filtered_forecasts = []
    for forecast in forecasts:
        if selected_location_id is None or forecast['location_id'] == selected_location_id:
            # Copy dict excluding location_id
            item = {
                'forecast_id': forecast['forecast_id'],
                'date': forecast['date'],
                'high_temp': forecast['high_temp'],
                'low_temp': forecast['low_temp'],
                'condition': forecast['condition'],
                'precipitation': forecast['precipitation'],
                'humidity': forecast['humidity']
            }
            filtered_forecasts.append(item)

    return render_template('weekly_forecast.html', locations=locations_list, selected_location_id=selected_location_id, forecasts=filtered_forecasts)


@app.route('/search/locations', methods=['GET', 'POST'])
def location_search():
    search_query = ''
    search_results = []
    saved_locations_raw = load_saved_locations()
    saved_locations = [{'location_id': s['location_id'], 'location_name': s['location_name']} for s in saved_locations_raw]

    all_locations = load_locations()

    if request.method == 'POST':
        # Assume user selects a location to save
        location_id_str = request.form.get('selected_location_id')
        if location_id_str and location_id_str.isdigit():
            location_id = int(location_id_str)
            # Find location in all locations
            loc = all_locations.get(location_id)
            if loc:
                # Check if already saved
                already_saved = any(s['location_id'] == location_id for s in saved_locations_raw)
                if not already_saved:
                    # Append to saved_locations file (no user_id or 1 hardcoded)
                    try:
                        with open(os.path.join(DATA_DIR, 'saved_locations.txt'), 'a', encoding='utf-8') as f:
                            # saved_id create as max+1
                            max_saved_id = max((s['saved_id'] for s in saved_locations_raw), default=0)
                            new_id = max_saved_id + 1
                            f.write(f"{new_id}|1|{loc['location_id']}|{loc['location_name']}|0\n")
                    except IOError:
                        pass
                return redirect(url_for('location_search'))

    # GET method or after POST
    search_query = request.args.get('q', '')
    if search_query:
        query_low = search_query.lower()
        for loc in all_locations.values():
            if query_low in loc['location_name'].lower():
                search_results.append({
                    'location_id': loc['location_id'],
                    'location_name': loc['location_name'],
                    'latitude': loc['latitude'],
                    'longitude': loc['longitude'],
                    'country': loc['country']
                })

    return render_template('location_search.html', search_query=search_query, search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts')
def weather_alerts():
    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location_id', default=None, type=int)

    all_alerts = load_alerts()
    all_locations = load_locations()

    # Filter alerts by severity if not All
    filtered_alerts = []
    for alert in all_alerts:
        if severity_filter != 'All' and alert['severity'] != severity_filter:
            continue
        if location_filter is not None and alert['location_id'] != location_filter:
            continue
        # Add location_name for alerts display
        loc = all_locations.get(alert['location_id'])
        alert_display = alert.copy()
        alert_display['location_name'] = loc['location_name'] if loc else ''
        filtered_alerts.append(alert_display)

    return render_template('weather_alerts.html', alerts=filtered_alerts, severity_filter=severity_filter, location_filter=location_filter)


@app.route('/air_quality')
def air_quality():
    selected_location_id = request.args.get('location_id', default=None, type=int)

    all_locations = load_locations()
    aqi_data_all = load_air_quality()

    locations_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in all_locations.values()]

    air_quality_data = None
    if selected_location_id is not None and selected_location_id in aqi_data_all:
        air_quality_data = aqi_data_all[selected_location_id]
    elif aqi_data_all:
        # fallback first if no filter or not found
        air_quality_data = next(iter(aqi_data_all.values()))
    else:
        air_quality_data = None

    if air_quality_data is not None:
        aqi_index = air_quality_data.get('aqi_index')
    else:
        aqi_index = None

    aqi_description = aqi_index_description(aqi_index)
    health_recommendation = health_recommendation_for_aqi(aqi_index)

    return render_template('air_quality.html',
                           locations=locations_list,
                           selected_location_id=selected_location_id,
                           air_quality_data=air_quality_data,
                           aqi_description=aqi_description,
                           health_recommendation=health_recommendation)


@app.route('/saved_locations')
def saved_locations():
    saved_locations_raw = load_saved_locations()
    current_weather = load_current_weather()

    # Build saved_locations with current temp and condition
    saved_locations_list = []
    for s in saved_locations_raw:
        loc_id = s['location_id']
        weather = current_weather.get(loc_id)
        saved_locations_list.append({
            'saved_id': s['saved_id'],
            'location_id': loc_id,
            'location_name': s['location_name'],
            'current_temperature': weather['temperature'] if weather else 0.0,
            'current_condition': weather['condition'] if weather else '',
            'is_default': s['is_default']
        })
    return render_template('saved_locations.html', saved_locations=saved_locations_list)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]

    saved_locations_raw = load_saved_locations()
    saved_locations_list = [{'location_id': s['location_id'], 'location_name': s['location_name']} for s in saved_locations_raw]

    # Defaults
    selected_unit = "Celsius"
    default_location_id = None
    alert_notifications_enabled = True

    settings_path = os.path.join(DATA_DIR, 'settings.txt')

    # Load existing settings if file present
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            for line in f:
                k, v = line.strip().split('=', 1)
                if k == 'temperature_unit' and v in temperature_units:
                    selected_unit = v
                elif k == 'default_location_id':
                    try:
                        default_location_id = int(v)
                    except ValueError:
                        pass
                elif k == 'alert_notifications_enabled':
                    alert_notifications_enabled = (v.lower() == 'true')
    except IOError:
        pass

    if request.method == 'POST':
        # process form
        sel_unit = request.form.get('temperature_unit')
        def_loc_id = request.form.get('default_location_id')
        alerts_enabled_str = request.form.get('alert_notifications_enabled')

        if sel_unit in temperature_units:
            selected_unit = sel_unit
        try:
            if def_loc_id is not None and def_loc_id != 'None':
                default_location_id = int(def_loc_id)
            else:
                default_location_id = None
        except ValueError:
            default_location_id = None

        alert_notifications_enabled = (alerts_enabled_str == 'on')

        # Save settings to file
        try:
            with open(settings_path, 'w', encoding='utf-8') as f:
                f.write(f"temperature_unit={selected_unit}\n")
                f.write(f"default_location_id={default_location_id if default_location_id is not None else ''}\n")
                f.write(f"alert_notifications_enabled={str(alert_notifications_enabled)}\n")
        except IOError:
            pass

        return redirect(url_for('settings'))

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           selected_unit=selected_unit,
                           saved_locations=saved_locations_list,
                           default_location_id=default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
