import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Load current weather data
def load_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    current_weather = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
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
    except FileNotFoundError:
        pass
    return current_weather

# Load forecasts
def load_forecasts():
    filepath = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return forecasts

# Load locations
def load_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                loc = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'latitude': float(parts[2]),
                    'longitude': float(parts[3]),
                    'country': parts[4],
                    'timezone': parts[5]
                }
                locations.append(loc)
    except FileNotFoundError:
        pass
    return locations

# Load alerts
def load_alerts():
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except FileNotFoundError:
        pass
    return alerts

# Load air quality data
def load_air_quality():
    filepath = os.path.join(DATA_DIR, 'air_quality.txt')
    air_quality = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                aqi = {
                    'aqi_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'aqi_index': int(parts[2]),
                    'pm25': float(parts[3]),
                    'pm10': float(parts[4]),
                    'no2': float(parts[5]),
                    'o3': float(parts[6]),
                    'last_updated': parts[7]
                }
                air_quality.append(aqi)
    except FileNotFoundError:
        pass
    return air_quality

# Load saved locations
def load_saved_locations():
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                sloc = {
                    'saved_id': int(parts[0]),
                    'user_id': int(parts[1]),
                    'location_id': int(parts[2]),
                    'location_name': parts[3],
                    'is_default': int(parts[4])
                }
                saved_locations.append(sloc)
    except FileNotFoundError:
        pass
    return saved_locations

# Helper for default location
def get_default_location():
    saved_locations = load_saved_locations()
    user_saved = [loc for loc in saved_locations if loc['user_id'] == 1]
    default_saved = next((loc for loc in user_saved if loc['is_default']), None)
    current_list = load_current_weather()

    if default_saved:
        for cw in current_list:
            if cw['location_id'] == default_saved['location_id']:
                return {
                    'location_id': cw['location_id'],
                    'location_name': cw['location_name'],
                    'temperature': cw['temperature'],
                    'condition': cw['condition'],
                    'humidity': cw['humidity'],
                    'wind_speed': cw['wind_speed'],
                    'last_updated': cw['last_updated']
                }

    if current_list:
        first = current_list[0]
        return {
            'location_id': first['location_id'],
            'location_name': first['location_name'],
            'temperature': first['temperature'],
            'condition': first['condition'],
            'humidity': first['humidity'],
            'wind_speed': first['wind_speed'],
            'last_updated': first['last_updated']
        }

    return {
        'location_id': 0,
        'location_name': 'Unknown',
        'temperature': 0,
        'condition': 'Unknown',
        'humidity': 0,
        'wind_speed': 0,
        'last_updated': ''
    }

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    default_location = get_default_location()
    return render_template('dashboard.html', default_location=default_location)

@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weather_list = load_current_weather()
    locations = load_locations()

    location_weather = next((cw for cw in current_weather_list if cw['location_id'] == location_id), None)
    location_info = next((loc for loc in locations if loc['location_id'] == location_id), None)

    if location_weather is None:
        location_weather = {
            'location_id': location_id,
            'location_name': location_info['location_name'] if location_info else 'Unknown',
            'temperature': 0,
            'condition': 'Unknown',
            'humidity': 0,
            'wind_speed': 0,
            'last_updated': ''
        }

    return render_template('current_weather.html',
                           location=location_weather,
                           temperature=location_weather['temperature'],
                           condition=location_weather['condition'],
                           humidity=location_weather['humidity'],
                           wind_speed=location_weather['wind_speed'])

@app.route('/forecasts')
def weekly_forecast():
    locations = load_locations()
    forecasts_data = load_forecasts()

    selected_location_id = request.args.get('location_id', type=int)
    if not selected_location_id and locations:
        selected_location_id = locations[0]['location_id']

    filtered_forecasts = [f for f in forecasts_data if f['location_id'] == selected_location_id] if selected_location_id else []
    location_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('weekly_forecast.html', forecasts=filtered_forecasts, locations=location_list, selected_location_id=selected_location_id or 0)

@app.route('/locations/search', methods=['GET', 'POST'])
def locations_search():
    saved_locations_all = load_saved_locations()
    saved_locations = [sloc for sloc in saved_locations_all if sloc['user_id'] == 1]
    locations = load_locations()

    search_query = ''
    search_results = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            search_results = [loc for loc in locations if search_query.lower() in loc['location_name'].lower()]

    return render_template('location_search.html', search_results=search_results, saved_locations=saved_locations, search_query=search_query)

@app.route('/alerts')
def alerts():
    severity_filter = request.args.get('severity', default=None)
    location_filter_raw = request.args.get('location', default=None)
    location_filter = None
    if location_filter_raw is not None:
        try:
            location_filter = int(location_filter_raw)
        except ValueError:
            location_filter = None

    alerts_all = load_alerts()

    def alert_severity_filter(alert):
        if severity_filter is None or severity_filter == 'All':
            return True
        return alert['severity'] == severity_filter

    def alert_location_filter(alert):
        if location_filter is None:
            return True
        return alert['location_id'] == location_filter

    filtered_alerts = [alert for alert in alerts_all if alert_severity_filter(alert) and alert_location_filter(alert)]

    locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in load_locations()]

    return render_template('alerts.html', alerts=filtered_alerts, locations=locations, severity_filter=severity_filter, location_filter=location_filter)

@app.route('/air_quality')
def air_quality():
    locations = load_locations()
    selected_location_id = request.args.get('location_id', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    air_quality_list = load_air_quality()
    air_quality_data = next((a for a in air_quality_list if a['location_id'] == selected_location_id), None)

    aqi_description = ''
    health_recommendation = ''

    if air_quality_data:
        aqi_val = air_quality_data['aqi_index']
        if aqi_val <= 50:
            aqi_description = 'Good air quality.'
            health_recommendation = 'Air quality is satisfactory and poses little or no risk.'
        elif aqi_val <= 100:
            aqi_description = 'Moderate air quality.'
            health_recommendation = 'Air quality is acceptable. Some pollutants may affect very sensitive groups.'
        elif aqi_val <= 150:
            aqi_description = 'Unhealthy for Sensitive Groups.'
            health_recommendation = 'Members of sensitive groups may experience health effects. General public unlikely to be affected.'
        elif aqi_val <= 200:
            aqi_description = 'Unhealthy.'
            health_recommendation = 'Everyone may begin to experience health effects; sensitive groups may experience more serious effects.'
        elif aqi_val <= 300:
            aqi_description = 'Very Unhealthy.'
            health_recommendation = 'Health alert: everyone may experience more serious health effects.'
        else:
            aqi_description = 'Hazardous.'
            health_recommendation = 'Emergency conditions. Everyone should avoid all outdoor exertion.'
    else:
        air_quality_data = {
            'aqi_index': 0,
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': ''
        }
        aqi_description = 'No air quality data available.'
        health_recommendation = ''

    location_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('air_quality.html', air_quality=air_quality_data, aqi_description=aqi_description, health_recommendation=health_recommendation, locations=location_list, selected_location_id=selected_location_id or 0)

@app.route('/locations/saved')
def saved_locations():
    saved_locs_all = load_saved_locations()
    user_saved = [sloc for sloc in saved_locs_all if sloc['user_id'] == 1]
    current_weather = load_current_weather()

    locations_detail = []
    for sloc in user_saved:
        cw = next((cw for cw in current_weather if cw['location_id'] == sloc['location_id']), None)
        if cw:
            loc_dict = {
                'location_id': sloc['location_id'],
                'location_name': sloc['location_name'],
                'temperature': cw['temperature'],
                'condition': cw['condition']
            }
            locations_detail.append(loc_dict)
        else:
            locations_detail.append({
                'location_id': sloc['location_id'],
                'location_name': sloc['location_name'],
                'temperature': 0,
                'condition': 'Unknown'
            })

    return render_template('saved_locations.html', locations=locations_detail)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
    locations = load_locations()
    saved_locations_all = load_saved_locations()
    user_saved = [sloc for sloc in saved_locations_all if sloc['user_id'] == 1]

    if 'current_unit' not in session:
        session['current_unit'] = 'Celsius'
    if 'default_location_id' not in session:
        default_loc = next((loc for loc in user_saved if loc['is_default']), None)
        session['default_location_id'] = default_loc['location_id'] if default_loc else (user_saved[0]['location_id'] if user_saved else 0)
    if 'alert_notifications_enabled' not in session:
        session['alert_notifications_enabled'] = False

    if request.method == 'POST':
        unit = request.form.get('temperature_unit')
        if unit in temperature_units:
            session['current_unit'] = unit

        alert_notify_raw = request.form.get('alert_notifications_enabled')
        session['alert_notifications_enabled'] = bool(alert_notify_raw)

        def_loc_id = request.form.get('default_location_id', type=int)
        if def_loc_id and any(loc['location_id'] == def_loc_id for loc in user_saved):
            session['default_location_id'] = def_loc_id

        return redirect(url_for('settings'))

    location_list = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('settings.html', temperature_units=temperature_units, current_unit=session['current_unit'], locations=location_list, default_location_id=session.get('default_location_id', 0), alert_notifications_enabled=session.get('alert_notifications_enabled', False))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
