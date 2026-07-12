from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading helpers

def load_current_weather():
    data = []
    file_path = os.path.join('data', 'current_weather.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        try:
                            weather = {
                                'location_id': int(parts[0]),
                                'location_name': parts[1],
                                'temperature': float(parts[2]) if '.' in parts[2] else int(parts[2]),
                                'condition': parts[3],
                                'humidity': int(parts[4]),
                                'wind_speed': int(parts[5]),
                                'last_updated': parts[6]
                            }
                            data.append(weather)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


def load_forecasts():
    data = []
    file_path = os.path.join('data', 'forecasts.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        try:
                            forecast = {
                                'forecast_id': int(parts[0]),
                                'location_id': int(parts[1]),
                                'date': parts[2],
                                'high_temp': float(parts[3]) if '.' in parts[3] else int(parts[3]),
                                'low_temp': float(parts[4]) if '.' in parts[4] else int(parts[4]),
                                'condition': parts[5],
                                'precipitation': int(parts[6]),
                                'humidity': int(parts[7])
                            }
                            data.append(forecast)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


def load_locations():
    data = []
    file_path = os.path.join('data', 'locations.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        try:
                            location = {
                                'location_id': int(parts[0]),
                                'location_name': parts[1],
                                'latitude': float(parts[2]),
                                'longitude': float(parts[3]),
                                'country': parts[4],
                                'timezone': parts[5]
                            }
                            data.append(location)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


def load_alerts():
    data = []
    file_path = os.path.join('data', 'alerts.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
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
                            data.append(alert)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


def load_air_quality():
    data = []
    file_path = os.path.join('data', 'air_quality.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        try:
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
                            data.append(aqi)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


def load_saved_locations():
    data = []
    file_path = os.path.join('data', 'saved_locations.txt')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 5:
                        try:
                            saved = {
                                'saved_id': int(parts[0]),
                                'user_id': int(parts[1]),
                                'location_id': int(parts[2]),
                                'location_name': parts[3],
                                'is_default': bool(int(parts[4]))
                            }
                            data.append(saved)
                        except ValueError:
                            continue
    except IOError:
        pass
    return data


# Flask Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    current_weathers = load_current_weather()
    saved_locs = load_saved_locations()

    default_location = None
    # Determine default location
    for loc in saved_locs:
        if loc.get('is_default'):
            # Find matching weather data
            matching_weather = next((w for w in current_weathers if w['location_id'] == loc['location_id']), None)
            if matching_weather:
                default_location = {
                    'location_id': loc['location_id'],
                    'location_name': loc['location_name'],
                    'temperature': matching_weather['temperature'],
                    'condition': matching_weather['condition'],
                    'humidity': matching_weather['humidity'],
                    'wind_speed': matching_weather['wind_speed']
                }
            else:
                # Fallback to saved location info only
                default_location = {
                    'location_id': loc['location_id'],
                    'location_name': loc['location_name'],
                    'temperature': 0,
                    'condition': 'Unknown',
                    'humidity': 0,
                    'wind_speed': 0
                }
            break

    # If no default found, pick first saved location as default fallback
    if default_location is None and saved_locs:
        first_loc = saved_locs[0]
        matching_weather = next((w for w in current_weathers if w['location_id'] == first_loc['location_id']), None)
        if matching_weather:
            default_location = {
                'location_id': first_loc['location_id'],
                'location_name': first_loc['location_name'],
                'temperature': matching_weather['temperature'],
                'condition': matching_weather['condition'],
                'humidity': matching_weather['humidity'],
                'wind_speed': matching_weather['wind_speed']
            }
        else:
            default_location = {
                'location_id': first_loc['location_id'],
                'location_name': first_loc['location_name'],
                'temperature': 0,
                'condition': 'Unknown',
                'humidity': 0,
                'wind_speed': 0
            }

    if default_location is None:
        # No saved locations at all
        default_location = {
            'location_id': 0,
            'location_name': 'No Location',
            'temperature': 0,
            'condition': 'Unknown',
            'humidity': 0,
            'wind_speed': 0
        }

    saved_locations_count = len(saved_locs)

    return render_template('dashboard.html', default_location=default_location, saved_locations_count=saved_locations_count)


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weathers = load_current_weather()
    weather = next((w for w in current_weathers if w['location_id'] == location_id), None)

    if weather is None:
        # Not found - fallback blank / defaults
        weather = {
            'location_name': 'Unknown',
            'temperature': 0,
            'condition': 'Unknown',
            'humidity': 0,
            'wind_speed': 0
        }

    return render_template('current_weather.html',
                           location_name=weather['location_name'],
                           temperature=weather['temperature'],
                           condition=weather['condition'],
                           humidity=weather['humidity'],
                           wind_speed=weather['wind_speed'])


@app.route('/forecast/weekly')
def weekly_forecast():
    locations = load_locations()
    forecasts = load_forecasts()

    # Get selected location from query string
    selected_location_id = request.args.get('location_id', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    # Filter forecasts by selected location
    filtered_forecasts = [f for f in forecasts if f['location_id'] == selected_location_id] if selected_location_id else []

    # Extract locations list with only id and name
    simple_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    # Get selected location name for display
    location_name = next((loc['location_name'] for loc in locations if loc['location_id'] == selected_location_id), 'Unknown')

    return render_template('weekly_forecast.html', locations=simple_locations, selected_location_id=selected_location_id, forecasts=filtered_forecasts, location_name=location_name)


@app.route('/locations/search', methods=['GET', 'POST'])
def search_locations():
    locations = load_locations()
    saved_locs = load_saved_locations()

    saved_locations = []
    saved_ids = {sl['location_id'] for sl in saved_locs}
    # Filter saved_locations to include latitude, longitude, country by matching locations data
    for sl in saved_locs:
        loc = next((l for l in locations if l['location_id'] == sl['location_id']), None)
        if loc:
            saved_locations.append({
                'location_id': loc['location_id'],
                'location_name': loc['location_name'],
                'country': loc['country'],
                'latitude': loc['latitude'],
                'longitude': loc['longitude']
            })

    search_query = ''
    search_results = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        if search_query:
            lower_q = search_query.lower()
            for loc in locations:
                if lower_q in loc['location_name'].lower() or lower_q in loc['country'].lower():
                    search_results.append({
                        'location_id': loc['location_id'],
                        'location_name': loc['location_name'],
                        'country': loc['country'],
                        'latitude': loc['latitude'],
                        'longitude': loc['longitude']
                    })

    return render_template('search_locations.html',
                           search_query=search_query,
                           search_results=search_results,
                           saved_locations=saved_locations)


@app.route('/alerts')
def weather_alerts():
    alerts = load_alerts()
    locations = load_locations()

    severity_levels = ["All", "Critical", "High", "Medium", "Low"]

    # Get filter params from query string
    selected_severity = request.args.get('severity', 'All')
    selected_location_id = request.args.get('location_id', type=int)

    # Filter alerts by severity
    filtered_alerts = alerts
    if selected_severity != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == selected_severity]

    # Filter alerts by location
    if selected_location_id is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == selected_location_id]

    # Prepare locations list with only id and name
    simple_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('alerts.html',
                           alerts=filtered_alerts,
                           severity_levels=severity_levels,
                           locations=simple_locations,
                           selected_severity=selected_severity,
                           selected_location_id=selected_location_id)


@app.route('/airquality')
def air_quality():
    aqi_list = load_air_quality()
    locations = load_locations()

    # Get selected location from query string
    selected_location_id = request.args.get('location_id', type=int)
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    # Find aqi data for selected location
    aqi_data = next((a for a in aqi_list if a['location_id'] == selected_location_id), None)

    if aqi_data is None:
        aqi_data = {
            'aqi_index': 0,
            'description': 'Unknown',
            'pm25': 0.0,
            'pm10': 0.0,
            'no2': 0.0,
            'o3': 0.0,
            'last_updated': 'N/A'
        }
    else:
        # Provide description based on AQI index
        idx = aqi_data['aqi_index']
        if idx <= 50:
            desc = 'Good'
        elif idx <= 100:
            desc = 'Moderate'
        elif idx <= 150:
            desc = 'Unhealthy for Sensitive Groups'
        elif idx <= 200:
            desc = 'Unhealthy'
        elif idx <= 300:
            desc = 'Very Unhealthy'
        else:
            desc = 'Hazardous'

        aqi_data = {
            'aqi_index': aqi_data['aqi_index'],
            'description': desc,
            'pm25': aqi_data['pm25'],
            'pm10': aqi_data['pm10'],
            'no2': aqi_data['no2'],
            'o3': aqi_data['o3'],
            'last_updated': aqi_data['last_updated']
        }

    # Provide health recommendation based on AQI
    aqi_idx = aqi_data['aqi_index']
    if aqi_idx <= 50:
        health_recommendation = 'Air quality is considered satisfactory, and air pollution poses little or no risk.'
    elif aqi_idx <= 100:
        health_recommendation = 'Air quality is acceptable; however, some pollutants may cause a moderate health concern.'
    elif aqi_idx <= 150:
        health_recommendation = 'Members of sensitive groups may experience health effects. General public is less likely to be affected.'
    elif aqi_idx <= 200:
        health_recommendation = 'Everyone may begin to experience health effects; sensitive groups may experience more serious effects.'
    elif aqi_idx <= 300:
        health_recommendation = 'Health warnings of emergency conditions. The entire population is more likely to be affected.'
    else:
        health_recommendation = 'Health alert: everyone may experience serious health effects.'

    simple_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    location_name = next((loc['location_name'] for loc in locations if loc['location_id'] == selected_location_id), 'Unknown')

    return render_template('air_quality.html',
                           aqi_data=aqi_data,
                           locations=simple_locations,
                           selected_location_id=selected_location_id,
                           health_recommendation=health_recommendation,
                           location_name=location_name)


@app.route('/locations/saved')
def saved_locations():
    saved_locs = load_saved_locations()
    current_weathers = load_current_weather()
    locations = load_locations()

    # Merge saved locations with current weather and country info
    saved_locations_data = []
    for sl in saved_locs:
        weather = next((w for w in current_weathers if w['location_id'] == sl['location_id']), None)
        loc = next((l for l in locations if l['location_id'] == sl['location_id']), None)
        saved_locations_data.append({
            'saved_id': sl['saved_id'],
            'location_id': sl['location_id'],
            'location_name': sl['location_name'],
            'country': loc['country'] if loc else 'Unknown',
            'temperature': weather['temperature'] if weather else 0,
            'condition': weather['condition'] if weather else 'Unknown',
            'is_default': sl['is_default']
        })

    return render_template('saved_locations.html', saved_locations=saved_locations_data)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = load_locations()
    saved_locs = load_saved_locations()

    temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]

    # Determine default_location_id
    default_location_id = None
    for sl in saved_locs:
        if sl.get('is_default'):
            default_location_id = sl['location_id']
            break
    if default_location_id is None and saved_locs:
        default_location_id = saved_locs[0]['location_id']
    if default_location_id is None and locations:
        default_location_id = locations[0]['location_id']
    if default_location_id is None:
        default_location_id = 0

    # Alert notifications enabled flag
    # For simulation, maintain a global variable or static variable, but here simply default True
    alert_notifications_enabled = True

    # Selected temperature unit - default to Celsius
    selected_temperature_unit = "Celsius"

    if request.method == 'POST':
        # Simulate settings save using form data
        # Note: actual persistent save not specified
        form_default_location_id = request.form.get('default_location_id', type=int)
        form_alert_enabled = request.form.get('alert_notifications_enabled')
        form_temp_unit = request.form.get('temperature_unit')
        if form_default_location_id in [loc['location_id'] for loc in locations]:
            default_location_id = form_default_location_id
        alert_notifications_enabled = (form_alert_enabled == 'on')
        if form_temp_unit in temperature_units:
            selected_temperature_unit = form_temp_unit

    simple_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations]

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           default_location_id=default_location_id,
                           locations=simple_locations,
                           alert_notifications_enabled=alert_notifications_enabled,
                           selected_temperature_unit=selected_temperature_unit)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
