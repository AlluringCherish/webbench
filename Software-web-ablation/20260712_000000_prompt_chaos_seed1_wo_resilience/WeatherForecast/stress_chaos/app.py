from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
CURRENT_WEATHER_FILE = 'data/current_weather.txt'
FORECASTS_FILE = 'data/forecasts.txt'
LOCATIONS_FILE = 'data/locations.txt'
ALERTS_FILE = 'data/alerts.txt'
AIR_QUALITY_FILE = 'data/air_quality.txt'
SAVED_LOCATIONS_FILE = 'data/saved_locations.txt'

# Utility functions to load data

def load_current_weather():
    weather_list = []
    try:
        with open(CURRENT_WEATHER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        location_id = int(parts[0])
                        location_name = parts[1]
                        temperature = float(parts[2]) if '.' in parts[2] else int(parts[2])
                        condition = parts[3]
                        humidity = int(parts[4])
                        wind_speed = float(parts[5]) if '.' in parts[5] else int(parts[5])
                        last_updated = parts[6]
                        weather = {
                            'location_id': location_id,
                            'location_name': location_name,
                            'temperature': temperature,
                            'condition': condition,
                            'humidity': humidity,
                            'wind_speed': wind_speed,
                            'last_updated': last_updated
                        }
                        weather_list.append(weather)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return weather_list


def load_forecasts():
    forecasts_list = []
    try:
        with open(FORECASTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        forecast_id = int(parts[0])
                        location_id = int(parts[1])
                        date = parts[2]
                        high_temp = float(parts[3]) if '.' in parts[3] else int(parts[3])
                        low_temp = float(parts[4]) if '.' in parts[4] else int(parts[4])
                        condition = parts[5]
                        precipitation = int(parts[6])
                        humidity = int(parts[7])
                        forecast = {
                            'forecast_id': forecast_id,
                            'location_id': location_id,
                            'date': date,
                            'high_temp': high_temp,
                            'low_temp': low_temp,
                            'condition': condition,
                            'precipitation': precipitation,
                            'humidity': humidity
                        }
                        forecasts_list.append(forecast)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return forecasts_list


def load_locations():
    locations_list = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        location_id = int(parts[0])
                        location_name = parts[1]
                        latitude = float(parts[2])
                        longitude = float(parts[3])
                        country = parts[4]
                        timezone = parts[5]
                        location = {
                            'location_id': location_id,
                            'location_name': location_name,
                            'latitude': latitude,
                            'longitude': longitude,
                            'country': country,
                            'timezone': timezone
                        }
                        locations_list.append(location)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return locations_list


def load_alerts():
    alerts_list = []
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        alert_id = int(parts[0])
                        location_id = int(parts[1])
                        alert_type = parts[2]
                        severity = parts[3]
                        description = parts[4]
                        start_time = parts[5]
                        end_time = parts[6]
                        is_acknowledged = bool(int(parts[7]))
                        alert = {
                            'alert_id': alert_id,
                            'location_id': location_id,
                            'alert_type': alert_type,
                            'severity': severity,
                            'description': description,
                            'start_time': start_time,
                            'end_time': end_time,
                            'is_acknowledged': is_acknowledged
                        }
                        alerts_list.append(alert)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return alerts_list


def load_air_quality():
    air_quality_list = []
    try:
        with open(AIR_QUALITY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        aqi_id = int(parts[0])
                        location_id = int(parts[1])
                        aqi_index = int(parts[2])
                        pm25 = float(parts[3])
                        pm10 = float(parts[4])
                        no2 = float(parts[5])
                        o3 = float(parts[6])
                        last_updated = parts[7]
                        air_quality = {
                            'aqi_id': aqi_id,
                            'location_id': location_id,
                            'aqi_index': aqi_index,
                            'pm25': pm25,
                            'pm10': pm10,
                            'no2': no2,
                            'o3': o3,
                            'last_updated': last_updated
                        }
                        air_quality_list.append(air_quality)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return air_quality_list


def load_saved_locations():
    saved_locations_list = []
    try:
        with open(SAVED_LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        saved_id = int(parts[0])
                        user_id = int(parts[1])
                        location_id = int(parts[2])
                        location_name = parts[3]
                        is_default = parts[4] == '1'
                        saved_location = {
                            'saved_id': saved_id,
                            'user_id': user_id,
                            'location_id': location_id,
                            'location_name': location_name,
                            'is_default': is_default
                        }
                        saved_locations_list.append(saved_location)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return saved_locations_list


# Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


# Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard():
    saved_locations = load_saved_locations()
    current_weathers = load_current_weather()

    # Find default saved location
    default_location = None
    for sloc in saved_locations:
        if sloc.get('is_default'):
            # Find current weather for this location
            loc_weather = next((cw for cw in current_weathers if cw['location_id'] == sloc['location_id']), None)
            if loc_weather:
                default_location = {
                    'location_id': loc_weather['location_id'],
                    'location_name': loc_weather['location_name'],
                    'temperature': loc_weather['temperature'],
                    'condition': loc_weather['condition'],
                    'humidity': loc_weather['humidity'],
                    'wind_speed': loc_weather['wind_speed']
                }
            else:
                # If no weather found, show minimal info
                default_location = {
                    'location_id': sloc['location_id'],
                    'location_name': sloc['location_name'],
                    'temperature': None,
                    'condition': '',
                    'humidity': None,
                    'wind_speed': None
                }
            break

    # If no default found, fallback to first current weather
    if not default_location and current_weathers:
        cw = current_weathers[0]
        default_location = {
            'location_id': cw['location_id'],
            'location_name': cw['location_name'],
            'temperature': cw['temperature'],
            'condition': cw['condition'],
            'humidity': cw['humidity'],
            'wind_speed': cw['wind_speed']
        }

    # If still no location, default_location is empty dict
    if not default_location:
        default_location = {
            'location_id': None,
            'location_name': '',
            'temperature': None,
            'condition': '',
            'humidity': None,
            'wind_speed': None
        }

    return render_template('dashboard.html', default_location=default_location)


# Current Weather Page
@app.route('/weather/current/<int:location_id>', methods=['GET'])
def current_weather(location_id):
    current_weathers = load_current_weather()
    # Find weather for location_id
    loc_weather = next((cw for cw in current_weathers if cw['location_id'] == location_id), None)
    if loc_weather:
        location = {
            'location_id': loc_weather['location_id'],
            'location_name': loc_weather['location_name']
        }
        temperature = loc_weather['temperature']
        condition = loc_weather['condition']
        humidity = loc_weather['humidity']
        wind_speed = loc_weather['wind_speed']
    else:
        location = {'location_id': location_id, 'location_name': ''}
        temperature = None
        condition = ''
        humidity = None
        wind_speed = None

    return render_template('current_weather.html',
                           location=location,
                           temperature=temperature,
                           condition=condition,
                           humidity=humidity,
                           wind_speed=wind_speed)


# Weekly Forecast Page
@app.route('/weather/forecast', methods=['GET'])
def weekly_forecast():
    # Get selected_location_id from query param, default None
    selected_location_id = request.args.get('location_id', type=int)

    locations = load_locations()
    forecasts = load_forecasts()

    # If no selected_location_id, pick first location if available
    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    # Filter forecasts for selected_location_id
    if selected_location_id is not None:
        filtered_forecasts = [
            {
                'date': f['date'],
                'high_temp': f['high_temp'],
                'low_temp': f['low_temp'],
                'condition': f['condition']
            } for f in forecasts if f['location_id'] == selected_location_id
        ]
    else:
        filtered_forecasts = []

    return render_template('weekly_forecast.html',
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id or 0,
                           forecasts=filtered_forecasts)


# Location Search Page
@app.route('/locations/search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locations_all = load_saved_locations()

    # Using dummy user_id 1 since no user auth
    user_id = 1

    saved_locations = [
        {
            'location_id': sloc['location_id'],
            'location_name': sloc['location_name']
        } for sloc in saved_locations_all if sloc['user_id'] == user_id
    ]

    search_results = []

    if request.method == 'POST':
        if 'search_query' in request.form:
            query = request.form.get('search_query', '').strip().lower()
            if query:
                search_results = [
                    {
                        'location_id': loc['location_id'],
                        'location_name': loc['location_name']
                    } for loc in locations if query in loc['location_name'].lower()
                ]
        elif 'select_location_id' in request.form:
            # User selects a location to save
            selected_id_str = request.form.get('select_location_id')
            if selected_id_str and selected_id_str.isdigit():
                selected_location_id = int(selected_id_str)
                # Find location by id
                loc = next((l for l in locations if l['location_id'] == selected_location_id), None)
                if loc:
                    # Check if already saved for user
                    existing = next((s for s in saved_locations_all if s['user_id'] == user_id and s['location_id'] == selected_location_id), None)
                    if not existing:
                        # Save new location
                        try:
                            # Find max saved_id
                            max_id = max((s['saved_id'] for s in saved_locations_all), default=0)
                            with open(SAVED_LOCATIONS_FILE, 'a', encoding='utf-8') as f:
                                new_line = f"{max_id + 1}|{user_id}|{loc['location_id']}|{loc['location_name']}|0\n"
                                f.write(new_line)
                        except Exception:
                            pass
                    # Refresh saved_locations post save
                    saved_locations_all = load_saved_locations()
                    saved_locations = [
                        {
                            'location_id': sloc['location_id'],
                            'location_name': sloc['location_name']
                        } for sloc in saved_locations_all if sloc['user_id'] == user_id
                    ]

    return render_template('location_search.html', search_results=search_results, saved_locations=saved_locations)


# Weather Alerts Page
@app.route('/alerts', methods=['GET'])
def weather_alerts():
    alerts = load_alerts()
    locations = load_locations()

    severity_levels = ["All", "Critical", "High", "Medium", "Low"]

    # Query params for filtering
    selected_severity = request.args.get('severity', 'All')
    selected_location_id = request.args.get('location_id', type=int)

    filtered_alerts = alerts

    if selected_severity and selected_severity != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == selected_severity]

    if selected_location_id is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == selected_location_id]

    return render_template('weather_alerts.html',
                           alerts=filtered_alerts,
                           severity_levels=severity_levels,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations])


# Air Quality Page
@app.route('/air-quality', methods=['GET'])
def air_quality():
    locations = load_locations()
    air_qualities = load_air_quality()

    selected_location_id = request.args.get('location_id', type=int)

    if not selected_location_id and locations:
        selected_location_id = locations[0]['location_id']

    air_quality_data = next((aq for aq in air_qualities if aq['location_id'] == selected_location_id), None)

    # Default empty air_quality dict
    air_quality = {
        'aqi_index': None,
        'aqi_description': '',
        'pm25': None,
        'pm10': None,
        'no2': None,
        'o3': None,
        'last_updated': ''
    }

    health_recommendation = ''

    if air_quality_data:
        air_quality['aqi_index'] = air_quality_data['aqi_index']
        # Basic AQI description by index ranges
        aqi_val = air_quality_data['aqi_index']
        if aqi_val is not None:
            if aqi_val <= 50:
                air_quality['aqi_description'] = 'Good'
                health_recommendation = 'Air quality is satisfactory, and air pollution poses little or no risk.'
            elif 51 <= aqi_val <= 100:
                air_quality['aqi_description'] = 'Moderate'
                health_recommendation = 'Air quality is acceptable; some pollutants may pose a moderate health concern for sensitive groups.'
            elif 101 <= aqi_val <= 150:
                air_quality['aqi_description'] = 'Unhealthy for Sensitive Groups'
                health_recommendation = 'Members of sensitive groups may experience health effects; general public is less affected.'
            elif 151 <= aqi_val <= 200:
                air_quality['aqi_description'] = 'Unhealthy'
                health_recommendation = 'Everyone may begin to experience health effects; sensitive groups may experience more serious effects.'
            elif 201 <= aqi_val <= 300:
                air_quality['aqi_description'] = 'Very Unhealthy'
                health_recommendation = 'Health warnings of emergency conditions; everyone is more likely to be affected.'
            elif aqi_val > 300:
                air_quality['aqi_description'] = 'Hazardous'
                health_recommendation = 'Health alert: everyone may experience more serious health effects.'

        air_quality['pm25'] = air_quality_data['pm25']
        air_quality['pm10'] = air_quality_data['pm10']
        air_quality['no2'] = air_quality_data['no2']
        air_quality['o3'] = air_quality_data['o3']
        air_quality['last_updated'] = air_quality_data['last_updated']

    return render_template('air_quality.html',
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id or 0,
                           air_quality=air_quality,
                           health_recommendation=health_recommendation)


# Saved Locations Page
@app.route('/locations/saved', methods=['GET'])
def saved_locations_page():
    saved_locations_all = load_saved_locations()
    current_weathers = load_current_weather()

    # Using dummy user_id = 1
    user_id = 1

    user_saved_locations = [s for s in saved_locations_all if s['user_id'] == user_id]

    saved_locations = []

    for loc in user_saved_locations:
        # Find current weather for location
        cw = next((c for c in current_weathers if c['location_id'] == loc['location_id']), None)
        saved_locations.append({
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'current_temp': cw['temperature'] if cw else None,
            'condition': cw['condition'] if cw else ''
        })

    return render_template('saved_locations.html', saved_locations=saved_locations)


# Settings Page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Using dummy user_id = 1
    user_id = 1

    locations = load_locations()
    saved_locations_all = load_saved_locations()

    # Load settings - Simulated from saved_locations for default location and fixed settings
    temperature_unit = 'Celsius'
    alert_notifications_enabled = True

    # Default location id from saved_locations default flag
    default_location = next((s for s in saved_locations_all if s['user_id'] == user_id and s['is_default']), None)
    default_location_id = default_location['location_id'] if default_location else (locations[0]['location_id'] if locations else 0)

    if request.method == 'POST':
        # Process form to save settings
        temperature_unit = request.form.get('temperature_unit', 'Celsius')
        try:
            default_location_id = int(request.form.get('default_location_id', default_location_id))
        except ValueError:
            default_location_id = default_location_id
        alert_notifications_enabled = request.form.get('alert_notifications_enabled') == 'on'

        # Update saved_locations default flags - only one default allowed
        try:
            saved_lines = []
            for sloc in saved_locations_all:
                if sloc['user_id'] == user_id:
                    if sloc['location_id'] == default_location_id:
                        sloc['is_default'] = True
                    else:
                        sloc['is_default'] = False
                # Recompose line to save
                line = f"{sloc['saved_id']}|{sloc['user_id']}|{sloc['location_id']}|{sloc['location_name']}|{1 if sloc['is_default'] else 0}\n"
                saved_lines.append(line)
            with open(SAVED_LOCATIONS_FILE, 'w', encoding='utf-8') as f:
                f.writelines(saved_lines)
        except Exception:
            pass

    return render_template('settings.html',
                           temperature_unit=temperature_unit,
                           default_location_id=default_location_id,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
