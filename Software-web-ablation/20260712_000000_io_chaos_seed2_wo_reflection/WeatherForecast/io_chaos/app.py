from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# Helper functions to load data

def load_current_weather():
    current_weather = {}
    try:
        with open('data/current_weather.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    location_id = int(parts[0])
                    current_weather[location_id] = {
                        'location_id': location_id,
                        'location_name': parts[1],
                        'temperature': float(parts[2]),
                        'condition': parts[3],
                        'humidity': int(parts[4]),
                        'wind_speed': int(parts[5]),
                        'last_updated': parts[6]
                    }
    except Exception:
        pass
    return current_weather


def load_forecasts():
    forecasts = []
    try:
        with open('data/forecasts.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    forecasts.append({
                        'location_id': int(parts[0]),
                        'date': parts[1],
                        'high_temp': float(parts[2]),
                        'low_temp': float(parts[3]),
                        'condition': parts[4],
                        'last_updated': parts[5]
                    })
    except Exception:
        pass
    return forecasts


def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    locations.append({
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'coordinates': parts[2]
                    })
    except Exception:
        pass
    return locations


def load_air_quality():
    air_quality = []
    try:
        with open('data/air_quality.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    air_quality.append({
                        'aqi_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'aqi_index': int(parts[2]),
                        'pm25': float(parts[3]),
                        'pm10': float(parts[4]),
                        'no2': float(parts[5]),
                        'o3': float(parts[6]),
                        'last_updated': parts[7]
                    })
    except Exception:
        pass
    return air_quality


def load_saved_locations():
    saved_locations = []
    try:
        with open('data/saved_locations.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    saved_locations.append({
                        'user_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'location_name': parts[2],
                        'is_default': parts[3] == 'True'
                    })
    except Exception:
        pass
    return saved_locations


def get_saved_location_by_id(saved_locations, location_id):
    for loc in saved_locations:
        if loc['location_id'] == location_id:
            return loc
    return None


def get_default_location():
    saved = load_saved_locations()
    current_weather = load_current_weather()
    if not saved:
        # Return first available current weather if no saved location
        if current_weather:
            first = next(iter(current_weather.values()))
            return {
                'location_id': first['location_id'],
                'location_name': first['location_name'],
                'temperature': first['temperature'],
                'condition': first['condition']
            }
        else:
            return {'location_id': 0, 'location_name': '', 'temperature': 0.0, 'condition': ''}
    # Return default saved location's weather if available
    default_saved = None
    for loc in saved:
        if loc['is_default']:
            default_saved = loc
            break
    if default_saved:
        loc_id = default_saved['location_id']
        if loc_id in current_weather:
            cw = current_weather[loc_id]
            return {
                'location_id': cw['location_id'],
                'location_name': cw['location_name'],
                'temperature': cw['temperature'],
                'condition': cw['condition']
            }
    # Fallback to first current weather if default not found
    if current_weather:
        first = next(iter(current_weather.values()))
        return {
            'location_id': first['location_id'],
            'location_name': first['location_name'],
            'temperature': first['temperature'],
            'condition': first['condition']
        }
    return {'location_id': 0, 'location_name': '', 'temperature': 0.0, 'condition': ''}


@app.route('/')
def dashboard():
    default_location = get_default_location()
    return render_template('dashboard.html', default_location=default_location)


@app.route('/current_weather/<int:location_id>')
def current_weather(location_id):
    current_weather = load_current_weather()
    wd = current_weather.get(location_id)
    if not wd:
        weather_details = {
            'location_name': '',
            'temperature': 0.0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0
        }
    else:
        weather_details = {
            'location_name': wd['location_name'],
            'temperature': wd['temperature'],
            'condition': wd['condition'],
            'humidity': wd['humidity'],
            'wind_speed': wd['wind_speed']
        }
    return render_template('current_weather.html', weather_details=weather_details)


@app.route('/forecast/weekly', methods=['GET', 'POST'])
def weekly_forecast():
    location_list = load_locations()
    saved = load_saved_locations()

    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('selected_location_id')
        if selected_location_id:
            selected_location_id = int(selected_location_id)
    # If no selection, use default or first saved location
    if not selected_location_id:
        default_saved = None
        for loc in saved:
            if loc.get('is_default'):
                default_saved = loc
                break
        if default_saved:
            selected_location_id = default_saved['location_id']
        elif location_list:
            selected_location_id = location_list[0]['location_id']

    all_forecasts = load_forecasts()
    forecast_list = []
    for f in all_forecasts:
        if f['location_id'] == selected_location_id:
            forecast_list.append({
                'date': f['date'],
                'high_temp': f['high_temp'],
                'low_temp': f['low_temp'],
                'condition': f['condition']
            })

    return render_template('weekly_forecast.html', location_list=location_list, selected_location_id=selected_location_id, forecast_list=forecast_list)


@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved = load_saved_locations()
    saved_locations = [
        {'location_id': s['location_id'], 'location_name': s['location_name']}
        for s in saved
    ]

    search_query = ''
    search_results = None

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            lower_query = search_query.lower()
            if ',' in search_query:
                # Attempt to parse coordinates
                parts = search_query.split(',')
                if len(parts) == 2:
                    try:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())
                        # Find locations within ~1 degree proximity
                        search_results = []
                        for loc in locations:
                            try:
                                coord_parts = loc['coordinates'].split(',')
                                loc_lat = float(coord_parts[0])
                                loc_lon = float(coord_parts[1])
                                if abs(loc_lat - lat) <= 1 and abs(loc_lon - lon) <= 1:
                                    search_results.append(loc)
                            except Exception:
                                continue
                    except ValueError:
                        search_results = []
                else:
                    search_results = []
            else:
                # Search by location name substring match
                search_results = [loc for loc in locations if lower_query in loc['location_name'].lower()]

    return render_template('location_search.html', search_query=search_query, search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts', methods=['GET', 'POST'])
def weather_alerts():
    locations = load_locations()
    location_map = {loc['location_id']: loc['location_name'] for loc in locations}
    alerts = []
    try:
        with open('data/alerts.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    alert = {
                        'alert_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7] == 'True',
                        'location_name': location_map.get(int(parts[1]), '')
                    }
                    alerts.append(alert)
    except Exception:
        pass

    severity_filter = 'All'
    location_filter = None

    if request.method == 'POST':
        severity_filter = request.form.get('severity_filter', 'All')
        location_filter_str = request.form.get('location_filter')
        try:
            location_filter = int(location_filter_str) if location_filter_str is not None and location_filter_str != '' else None
        except Exception:
            location_filter = None

        acknowledge_alert_id_str = request.form.get('acknowledge_alert_id')
        if acknowledge_alert_id_str:
            acknowledge_alert_id = int(acknowledge_alert_id_str)
            for alert in alerts:
                if alert['alert_id'] == acknowledge_alert_id:
                    alert['is_acknowledged'] = True

    filtered_alerts = []
    for alert in alerts:
        if (severity_filter == 'All' or alert['severity'] == severity_filter) and \
           (location_filter is None or alert['location_id'] == location_filter):
            filtered_alerts.append(alert)

    return render_template('weather_alerts.html', alerts=filtered_alerts, severity_filter=severity_filter, location_filter=location_filter)


@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = load_locations()
    location_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    selected_location_id = None
    if request.method == 'POST':
        selected_location_id = request.form.get('selected_location_id')
        if selected_location_id:
            selected_location_id = int(selected_location_id)
    if not selected_location_id and location_list:
        selected_location_id = location_list[0]['location_id']

    air_quality_records = load_air_quality()
    aqi_info = None
    for record in air_quality_records:
        if record['location_id'] == selected_location_id:
            aqi_info = {
                'aqi_index': record['aqi_index'],
                'aqi_description': describe_aqi(record['aqi_index']),
                'pm25': record['pm25'],
                'pm10': record['pm10'],
                'no2': record['no2'],
                'o3': record['o3'],
                'last_updated': record['last_updated']
            }
            break
    if not aqi_info:
        aqi_info = {
            'aqi_index': 0,
            'aqi_description': '',
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }

    health_recommendation = health_advice(aqi_info['aqi_index'])

    return render_template('air_quality.html', location_list=location_list, selected_location_id=selected_location_id, aqi_info=aqi_info, health_recommendation=health_recommendation)


def describe_aqi(aqi_index):
    if aqi_index <= 50:
        return 'Air quality is good; poses little or no risk.'
    elif aqi_index <= 100:
        return 'Air quality is moderate; some pollutants may be a concern for sensitive health groups.'
    elif aqi_index <= 150:
        return 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
    elif aqi_index <= 200:
        return 'Health alert: everyone may experience health effects.'
    elif aqi_index <= 300:
        return 'Health warnings of emergency conditions. The entire population is more likely to be affected.'
    else:
        return 'Hazardous air quality conditions.'


@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations_route():
    saved = load_saved_locations()
    current_weather = load_current_weather()
    user_id = 1  # Assuming user_id 1 for demonstration

    saved_locations_data = []
    for s in saved:
        loc_weather = current_weather.get(s['location_id'], {'temperature': 0.0, 'condition': '', 'location_name': s['location_name']})
        saved_locations_data.append({
            'location_id': s['location_id'],
            'location_name': s['location_name'],
            'temperature': loc_weather.get('temperature', 0.0),
            'condition': loc_weather.get('condition', ''),
            'is_default': s.get('is_default', False)
        })

    # POST actions to add, remove, or update default locations are not implemented for now

    return render_template('saved_locations.html', saved_locations=saved_locations_data, user_id=user_id)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Temporary in-memory settings store
    if not hasattr(settings, 'temperature_unit'):
        settings.temperature_unit = 'Celsius'
    if not hasattr(settings, 'default_location_id'):
        saved = load_saved_locations()
        default_loc = next((s for s in saved if s.get('is_default')), None)
        if default_loc:
            settings.default_location_id = default_loc['location_id']
        else:
            settings.default_location_id = None
    if not hasattr(settings, 'alert_notifications_enabled'):
        settings.alert_notifications_enabled = True

    location_list = load_locations()

    if request.method == 'POST':
        temperature_unit = request.form.get('temperature_unit')
        default_location_id = request.form.get('default_location_id')
        alert_notifications_enabled = request.form.get('alert_notifications_enabled') == 'true'

        if temperature_unit:
            settings.temperature_unit = temperature_unit
        if default_location_id:
            try:
                settings.default_location_id = int(default_location_id)
            except:
                pass
        settings.alert_notifications_enabled = alert_notifications_enabled

    return render_template('settings.html', temperature_unit=settings.temperature_unit, default_location_id=settings.default_location_id, location_list=location_list, alert_notifications_enabled=settings.alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True)
