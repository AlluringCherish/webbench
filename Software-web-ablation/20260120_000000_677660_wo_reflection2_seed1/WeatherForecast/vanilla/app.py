from flask import Flask, render_template, redirect, url_for, request, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
CURRENT_WEATHER_FILE = 'data/current_weather.txt'
FORECASTS_FILE = 'data/forecasts.txt'
LOCATIONS_FILE = 'data/locations.txt'
ALERTS_FILE = 'data/alerts.txt'
AIR_QUALITY_FILE = 'data/air_quality.txt'
SAVED_LOCATIONS_FILE = 'data/saved_locations.txt'

# Helper functions to load data from files

def load_current_weather():
    data = []
    try:
        with open(CURRENT_WEATHER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                location_id = int(parts[0])
                location_name = parts[1]
                temperature = float(parts[2])
                condition = parts[3]
                humidity = int(parts[4])
                wind_speed = float(parts[5])
                last_updated = parts[6]

                data.append({
                    'location_id': location_id,
                    'location_name': location_name,
                    'temperature': temperature,
                    'condition': condition,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'last_updated': last_updated
                })
    except FileNotFoundError:
        pass
    return data


def load_forecasts():
    data = []
    try:
        with open(FORECASTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                forecast_id = int(parts[0])
                location_id = int(parts[1])
                date = parts[2]
                high_temp = float(parts[3])
                low_temp = float(parts[4])
                condition = parts[5]
                precipitation = int(parts[6])
                humidity = int(parts[7])

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
    except FileNotFoundError:
        pass
    return data


def load_locations():
    data = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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
    except FileNotFoundError:
        pass
    return data


def load_alerts():
    data = []
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                alert_id = int(parts[0])
                location_id = int(parts[1])
                alert_type = parts[2]
                severity = parts[3]
                description = parts[4]
                start_time = parts[5]
                end_time = parts[6]
                is_acknowledged = parts[7] == '1'

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
    except FileNotFoundError:
        pass
    return data


def load_air_quality():
    data = []
    try:
        with open(AIR_QUALITY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                aqi_id = int(parts[0])
                location_id = int(parts[1])
                aqi_index = int(parts[2])
                pm25 = float(parts[3])
                pm10 = float(parts[4])
                no2 = float(parts[5])
                o3 = float(parts[6])
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
    except FileNotFoundError:
        pass
    return data


def load_saved_locations():
    data = []
    try:
        with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                saved_id = int(parts[0])
                user_id = int(parts[1])
                location_id = int(parts[2])
                location_name = parts[3]
                is_default = parts[4] == '1'

                data.append({
                    'saved_id': saved_id,
                    'user_id': user_id,
                    'location_id': location_id,
                    'location_name': location_name,
                    'is_default': is_default
                })
    except FileNotFoundError:
        pass
    return data


# Root route redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# /dashboard GET
@app.route('/dashboard', methods=['GET'])
def dashboard():
    current_weather_list = load_current_weather()
    saved_locations = load_saved_locations()

    default_location_id = None
    # Find default location from saved_locations
    for loc in saved_locations:
        if loc['is_default']:
            default_location_id = loc['location_id']
            break

    # Fallback: use first location from current_weather
    if default_location_id is None and current_weather_list:
        default_location_id = current_weather_list[0]['location_id']

    current_weather = None
    for cw in current_weather_list:
        if cw['location_id'] == default_location_id:
            current_weather = cw
            break

    # If not found, prepare empty dict to avoid crash
    if current_weather is None:
        current_weather = {
            'location_id': default_location_id or 0,
            'location_name': '',
            'temperature': 0.0,
            'condition': '',
            'humidity': 0,
            'wind_speed': 0.0,
            'last_updated': ''
        }

    return render_template('dashboard.html', current_weather=current_weather)


# /weather/current/<int:location_id> GET
@app.route('/weather/current/<int:location_id>', methods=['GET'])
def current_weather(location_id):
    current_weather_list = load_current_weather()

    # Find matching location weather
    cw = next((cw for cw in current_weather_list if cw['location_id'] == location_id), None)

    if cw is None:
        # fallback empty data
        return render_template('current_weather.html', location_name='', temperature=0.0, condition='', humidity=0, wind_speed=0.0)

    return render_template('current_weather.html',
                           location_name=cw['location_name'],
                           temperature=cw['temperature'],
                           condition=cw['condition'],
                           humidity=cw['humidity'],
                           wind_speed=cw['wind_speed'])


# /forecast/weekly GET
@app.route('/forecast/weekly', methods=['GET'])
def weekly_forecast():
    # Get query param for selected location
    selected_location_id = request.args.get('location_id', type=int)

    locations = load_locations()
    forecasts = load_forecasts()

    # If no location selected, use first location in locations list
    if not selected_location_id and locations:
        selected_location_id = locations[0]['location_id']

    # Filter forecast by selected location id
    filtered_forecasts = []
    if selected_location_id:
        filtered_forecasts = [f for f in forecasts if f['location_id'] == selected_location_id]

    # Only location_id and location_name are needed for locations context
    locations_context = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('weekly_forecast.html',
                           location_id=selected_location_id or 0,
                           locations=locations_context,
                           forecasts=filtered_forecasts)


# /locations/search GET
@app.route('/locations/search', methods=['GET'])
def location_search():
    query = request.args.get('query', '')

    all_locations = load_locations()
    saved_locations = load_saved_locations()

    if query:
        # Simple case-insensitive search in location_name
        search_results = [loc for loc in all_locations if query.lower() in loc['location_name'].lower()]
    else:
        search_results = []

    return render_template('location_search.html',
                           search_results=search_results,
                           saved_locations=saved_locations,
                           query=query or None)


# Added missing POST or GET routes for save_location, remove_saved_location, and acknowledge_alert
# For demonstration, these routes will simulate the action and redirect back to relevant pages

@app.route('/locations/save/<int:location_id>', methods=['GET'])
def save_location(location_id):
    # Simulate save action (no persistent storage)
    # In reality, would append or modify saved_locations data
    # Here just redirect back to search page
    return redirect(url_for('location_search'))

@app.route('/locations/remove/<int:location_id>', methods=['GET'])
def remove_saved_location(location_id):
    # Simulate remove action
    return redirect(url_for('saved_locations'))

@app.route('/alerts/acknowledge/<int:alert_id>', methods=['GET'])
def acknowledge_alert(alert_id):
    # Simulate acknowledge action
    return redirect(url_for('weather_alerts'))


# /alerts GET
@app.route('/alerts', methods=['GET'])
def weather_alerts():
    selected_severity = request.args.get('severity', '')
    selected_location_id = request.args.get('location_id', type=int)

    alerts = load_alerts()
    locations_all = load_locations()

    locations_context = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations_all]

    # Filter alerts by severity and location if specified
    filtered_alerts = alerts
    if selected_severity:
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == selected_severity]
    if selected_location_id is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == selected_location_id]

    return render_template('weather_alerts.html',
                           alerts=filtered_alerts,
                           locations=locations_context,
                           selected_severity=selected_severity,
                           selected_location_id=selected_location_id or 0)


# /airquality GET
@app.route('/airquality', methods=['GET'])
def air_quality():
    selected_location_id = request.args.get('location_id', type=int)

    air_quality_data = load_air_quality()
    locations_all = load_locations()
    locations_context = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations_all]

    # Filter air quality data by selected location
    filtered_aq = None
    if selected_location_id:
        filtered_aq = next((aq for aq in air_quality_data if aq['location_id'] == selected_location_id), None)

    # Health recommendation based on AQI index if data present
    health_recommendation = ''
    if filtered_aq:
        aqi_index = filtered_aq.get('aqi_index', 0)
        if aqi_index <= 50:
            health_recommendation = 'Air quality is good. No precautions needed.'
        elif aqi_index <= 100:
            health_recommendation = 'Moderate air quality. Consider reducing prolonged outdoor exertion.'
        elif aqi_index <= 150:
            health_recommendation = 'Unhealthy for sensitive groups. People with respiratory issues should limit outdoor activity.'
        elif aqi_index <= 200:
            health_recommendation = 'Unhealthy air quality. Everyone should reduce prolonged outdoor exertion.'
        elif aqi_index <= 300:
            health_recommendation = 'Very unhealthy air quality. Everyone should avoid outdoor activities.'
        else:
            health_recommendation = 'Hazardous air quality. Remain indoors and keep windows closed.'

    return render_template('air_quality.html',
                           air_quality_data=air_quality_data,
                           locations=locations_context,
                           selected_location_id=selected_location_id or 0,
                           health_recommendation=health_recommendation)


# /locations/saved GET
@app.route('/locations/saved', methods=['GET'])
def saved_locations():
    saved_locs = load_saved_locations()
    current_weather_list = load_current_weather()

    # Create dict map from location_id to current weather for quick access
    current_weather_map = {cw['location_id']: cw for cw in current_weather_list}

    # For the context current_weather, include temperature and condition for all saved locations combined?
    # Specification says a dict with location_id, temperature, condition
    # We will prepare a dict keyed by location_id with these fields
    current_weather_context = {}

    for loc in saved_locs:
        loc_id = loc['location_id']
        cw = current_weather_map.get(loc_id)
        if cw:
            current_weather_context[loc_id] = {
                'location_id': loc_id,
                'temperature': cw['temperature'],
                'condition': cw['condition']
            }
        else:
            current_weather_context[loc_id] = {
                'location_id': loc_id,
                'temperature': 0.0,
                'condition': ''
            }

    return render_template('saved_locations.html',
                           saved_locations=saved_locs,
                           current_weather=current_weather_context)


# /settings GET and POST
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    saved_locs = load_saved_locations()

    # Determine default_location_id from saved locations
    default_location_id = None
    alert_notifications_enabled = False
    temperature_unit = 'Celsius'  # default

    # On GET, just render stored user prefs from saved locations data (no real user settings file described)

    # Find default location id from saved locations
    for loc in saved_locs:
        if loc.get('is_default', False):
            default_location_id = loc.get('location_id')
            break

    if request.method == 'POST':
        # parse form data and update saved locations is_default and change prefs
        form = request.form
        temperature_unit = form.get('temperature_unit', 'Celsius')
        default_location_id_form = form.get('default_location_id', type=int)
        alert_notifications_enabled = form.get('alert_notifications_enabled') == 'on'

        # Update saved_locations to set new default based on default_location_id_form
        for loc in saved_locs:
            loc['is_default'] = (loc['location_id'] == default_location_id_form)

        # Note: No persistent storage required per spec, so just render updated values

        default_location_id = default_location_id_form

    return render_template('settings.html',
                           temperature_unit=temperature_unit,
                           default_location_id=default_location_id or 0,
                           saved_locations=saved_locs,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
