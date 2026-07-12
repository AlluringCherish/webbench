from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'datafiles'

# Helper function to load data

def load_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                try:
                    updated = parts[0]
                    location_name = parts[1]
                    location_id = int(parts[2])
                    temperature = float(parts[3]) if '.' in parts[3] else int(parts[3])
                    condition = parts[4]
                    humidity = float(parts[5])
                    wind_speed = float(parts[6])
                    data.append({
                        'location_id': location_id,
                        'location_name': location_name,
                        'temperature': temperature,
                        'condition': condition,
                        'humidity': humidity,
                        'wind_speed': wind_speed,
                        'last_updated': updated
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


def load_forecasts():
    filepath = os.path.join(DATA_DIR, 'forecasts.csv')
    data = []
    try:
        with open(filepath, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split(',')
                if len(parts) < 8:
                    continue
                try:
                    forecast_id = int(parts[0])
                    location_id = int(parts[1])
                    date = parts[2]
                    high_temp = int(parts[3])
                    low_temp = int(parts[4])
                    condition = parts[5]
                    precipitation = int(parts[6])
                    humidity = float(parts[7])
                    data.append({
                        'forecast_id': forecast_id,
                        'location_id': location_id,
                        'date': date,
                        'high_temp': high_temp,
                        'low_temp': low_temp,
                        'condition': condition,
                        'precipitation': precipitation,
                        'humidity': humidity
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


def load_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split(';')
                if len(parts) != 6:
                    continue
                try:
                    location_id = int(parts[0])
                    location_name = parts[1]
                    latitude = float(parts[2])
                    longitude = float(parts[3])
                    country = parts[4]
                    timezone = parts[5]
                    data.append({
                        'location_id': location_id,
                        'location_name': location_name,
                        'latitude': latitude,
                        'longitude': longitude,
                        'country': country,
                        'timezone': timezone
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


def load_alerts():
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                try:
                    alert_id = parts[0]
                    location_id = int(parts[1])
                    alert_type = parts[2]
                    severity = parts[3]
                    description = parts[4]
                    start_time = parts[5]
                    end_time = parts[6]
                    is_acknowledged = bool(int(parts[7]))
                    data.append({
                        'alert_id': alert_id,
                        'location_id': location_id,
                        'alert_type': alert_type,
                        'severity': severity,
                        'description': description,
                        'start_time': start_time,
                        'end_time': end_time,
                        'is_acknowledged': is_acknowledged
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


def load_air_quality():
    filepath = os.path.join(DATA_DIR, 'air_quality.csv')
    data = []
    try:
        with open(filepath, 'r') as file:
            for line in file.readlines():
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    aqi_id = parts[0]
                    location_id = int(parts[1])
                    aqi_index = float(parts[2])
                    pm25 = int(parts[3])
                    pm10 = int(parts[4])
                    no2 = int(parts[5])
                    o3 = int(parts[6])
                    last_updated = parts[7]
                    data.append({
                        'aqi_id': aqi_id,
                        'location_id': location_id,
                        'aqi_index': aqi_index,
                        'pm25': pm25,
                        'pm10': pm10,
                        'no2': no2,
                        'o3': o3,
                        'last_updated': last_updated
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


def load_saved_locations():
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    saved_id = parts[0]
                    user_id = int(parts[1])
                    location_id = int(parts[2])
                    location_name = parts[3]
                    is_default = bool(int(parts[4]))
                    data.append({
                        'saved_id': saved_id,
                        'user_id': user_id,
                        'location_id': location_id,
                        'location_name': location_name,
                        'is_default': is_default
                    })
                except Exception:
                    continue
    except IOError:
        data = []
    return data


# Routes
@app.route('/')
def root():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    current_weather_data = load_current_weather()
    saved_locations = load_saved_locations()
    default_location = None

    for saved in saved_locations:
        if saved['is_default']:
            for cw in current_weather_data:
                if cw['location_id'] == saved['location_id']:
                    default_location = cw
                    break
        if default_location:
            break

    if not default_location and current_weather_data:
        default_location = current_weather_data[0]

    if default_location:
        current_weather = {
            'location_id': default_location['location_id'],
            'location_name': default_location['location_name'],
            'temperature': int(default_location['temperature']),
            'condition': default_location['condition'],
            'humidity': default_location['humidity'],
            'wind_speed': default_location['wind_speed'],
            'last_updated': default_location['last_updated']
        }
    else:
        current_weather = {}

    return render_template('dashboard.html', current_weather=current_weather)


@app.route('/locations/search', methods=['GET', 'POST'])
def location_search_page():
    locations = load_locations()
    saved_locations_data = load_saved_locations()
    saved_locations = [{'location_id': sl['location_id'], 'location_name': sl['location_name']} for sl in saved_locations_data]
    search_results = []
    search_query = ''

    if request.method == 'POST':
        search_query = request.form.get('location_search_input', '').strip()
        if search_query:
            search_lower = search_query.lower()
            for loc in locations:
                if search_lower in loc['location_name'].lower():
                    search_results.append({'location_id': loc['location_id'], 'location_name': loc['location_name']})

    return render_template('location_search.html', search_results=search_results, saved_locations=saved_locations, search_query=search_query)


@app.route('/alerts')
def weather_alerts_page():
    alerts = load_alerts()
    severity_levels = ['All', 'Critical', 'High', 'Medium', 'Low']
    locations = load_locations()
    filter_severity = request.args.get('severity', 'All')
    filter_location_id = request.args.get('locationid', None)

    filtered_alerts = []
    for alert in alerts:
        if filter_severity != 'All' and alert['severity'] != filter_severity:
            continue
        if filter_location_id and str(alert['location_id']) != filter_location_id:
            continue
        filtered_alerts.append(alert)

    locs = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]
    return render_template('alerts.html', alerts=filtered_alerts, severity_levels=severity_levels, locations=locs)


@app.route('/alerts/acknowledge/<alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = load_alerts()
    changed = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            if not alert['is_acknowledged']:
                alert['is_acknowledged'] = True
                changed = True

    if changed:
        filepath = os.path.join(DATA_DIR, 'alerts.txt')
        try:
            with open(filepath, 'w') as f:
                for alert in alerts:
                    ia = '1' if alert['is_acknowledged'] else '0'
                    line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{ia}\n"
                    f.write(line)
        except IOError:
            pass

    return redirect(url_for('weather_alerts_page'))


@app.route('/air_quality')
def air_quality_page():
    locations = load_locations()
    aqi_data_list = load_air_quality()
    severity_levels = ['All', 'Critical', 'High', 'Medium', 'Low']
    selected_location_id = request.args.get('locationid', None)
    if not selected_location_id and len(locations) > 0:
        selected_location_id = locations[0]['location_id']
    else:
        try:
            selected_location_id = int(selected_location_id)
        except Exception:
            selected_location_id = None
    aqi_data = None
    if selected_location_id:
        for aqi in aqi_data_list:
            if aqi['location_id'] == selected_location_id:
                aqi_data = aqi
                break

    aqi_desc, health_rec = '', ''
    if aqi_data:
        idx = aqi_data['aqi_index']
        if idx < 51:
            aqi_desc = 'Good'
            health_rec = 'Air quality is satisfactory and air pollution poses no risk.'
        elif idx < 101:
            aqi_desc = 'Moderate'
            health_rec = 'Air quality is moderate; some pollutants may be a concern.'
        elif idx < 151:
            aqi_desc = 'Sensitive Groups Unhealthy'
            health_rec = 'Sensitive groups may experience health effects.'
        elif idx < 201:
            aqi_desc = 'Unhealthy'
            health_rec = 'Everyone may experience health effects; sensitive groups more serious.'
        elif idx < 301:
            aqi_desc = 'Very Unhealthy'
            health_rec = 'Health alert: everyone may experience more serious effects.'
        else:
            aqi_desc = 'Hazardous'
            health_rec = 'Health warnings of emergency conditions for entire population.'

    context = {
        'locations': [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
        'selected_location_id': selected_location_id,
        'aqi_data': aqi_data,
        'aqi_description': aqi_desc,
        'health_recommendation': health_rec
    }
    return render_template('air_quality.html', **context)


@app.route('/locations/saved')
def saved_locations_page():
    saved_locations_data = load_saved_locations()
    current_weather_data = load_current_weather()
    saved_locations = []

    for sl in saved_locations_data:
        cw = None
        for cwdata in current_weather_data:
            if cwdata['location_id'] == sl['location_id']:
                cw = cwdata
                break
        saved_locations.append({
            'location_id': sl['location_id'],
            'location_name': sl['location_name'],
            'temperature': cw['temperature'] if cw else None,
            'condition': cw['condition'] if cw else 'unknown'
        })
    return render_template('saved_locations.html', saved_locations=saved_locations)


@app.route('/locations/saved/remove/<int:location_id>', methods=['POST'])
def remove_saved_location(location_id):
    saved_locations_data = load_saved_locations()
    new_saved = [sl for sl in saved_locations_data if sl['location_id'] != location_id]
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    try:
        with open(filepath, 'w') as f:
            for sl in new_saved:
                line = f"{sl['saved_id']}|{sl['user_id']}|{sl['location_id']}|{sl['location_name']}|{int(sl['is_default'])}\n"
                f.write(line)
    except Exception:
        pass
    return redirect(url_for('saved_locations_page'))


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    saved_locations_data = load_saved_locations()
    saved_locations = [{'location_id': sl['location_id'], 'location_name': sl['location_name']} for sl in saved_locations_data]
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']

    # Default values for settings
    default_location_id = None
    alert_notifications_enabled = False

    # Determine default location from saved locations where is_default=1
    for sl in saved_locations_data:
        if sl['is_default']:
            default_location_id = sl['location_id']
            break

    if request.method == 'POST':
        # Process form submission
        default_location_id_form = request.form.get('default_location_id')
        alert_notifications_enabled_form = request.form.get('alert_notifications_enabled')

        if default_location_id_form:
            try:
                default_location_id = int(default_location_id_form)
            except ValueError:
                pass
        alert_notifications_enabled = (alert_notifications_enabled_form == 'on')

    return render_template('settings.html', temperature_units=temperature_units, default_location_id=default_location_id, saved_locations=saved_locations, alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
