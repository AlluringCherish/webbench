from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data

def load_current_weather():
    data = []
    filepath = 'data/current_weather.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
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
                        data.append({
                            'location_id': location_id,
                            'location_name': location_name,
                            'temperature': temperature,
                            'condition': condition,
                            'humidity': humidity,
                            'wind_speed': wind_speed,
                            'last_updated': last_updated
                        })
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


def load_forecasts():
    data = []
    filepath = 'data/forecasts.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
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
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


def load_locations():
    data = []
    filepath = 'data/locations.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
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
                        data.append({
                            'location_id': location_id,
                            'location_name': location_name,
                            'latitude': latitude,
                            'longitude': longitude,
                            'country': country,
                            'timezone': timezone
                        })
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


def load_alerts():
    data = []
    filepath = 'data/alerts.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
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
                        is_acknowledged = (parts[7] == '1')
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
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


def load_air_quality():
    data = []
    filepath = 'data/air_quality.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
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
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


def load_saved_locations():
    data = []
    filepath = 'data/saved_locations.txt'
    if not os.path.exists(filepath):
        return data
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        saved_id = int(parts[0])
                        user_id = int(parts[1])  # no auth, assume single user
                        location_id = int(parts[2])
                        location_name = parts[3]
                        is_default = (parts[4] == '1')
                        data.append({
                            'saved_id': saved_id,
                            'user_id': user_id,
                            'location_id': location_id,
                            'location_name': location_name,
                            'is_default': is_default
                        })
                    except ValueError:
                        continue
    except Exception:
        pass
    return data


# Utility function for air quality description and health recommendation based on AQI index

def get_aqi_description_and_recommendation(aqi_index):
    if aqi_index <= 50:
        return ("Good", "Air quality is satisfactory and poses little or no risk.")
    elif aqi_index <= 100:
        return ("Moderate", "Air quality is acceptable; however, some pollutants may be a moderate health concern for a very small number of people.")
    elif aqi_index <= 150:
        return ("Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects; general public is less likely to be affected.")
    elif aqi_index <= 200:
        return ("Unhealthy", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious effects.")
    elif aqi_index <= 300:
        return ("Very Unhealthy", "Health alert: everyone may experience more serious health effects.")
    else:
        return ("Hazardous", "Health warnings of emergency conditions. The entire population is more likely to be affected.")


# Route 1: Root Redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route 2: Dashboard Page
@app.route('/dashboard')
def dashboard():
    saved_locs = load_saved_locations()
    current_weather = load_current_weather()
    # Determine default_location
    default_location = None
    for saved in saved_locs:
        if saved['is_default']:
            default_location = saved
            break
    if default_location:
        # enrich default_location with temperature and condition
        for cw in current_weather:
            if cw['location_id'] == default_location['location_id']:
                default_location_weather = {
                    'location_id': cw['location_id'],
                    'location_name': cw['location_name'],
                    'temperature': cw['temperature'],
                    'condition': cw['condition']
                }
                break
        else:
            # no current weather found for default location
            default_location_weather = {
                'location_id': default_location['location_id'],
                'location_name': default_location['location_name'],
                'temperature': None,
                'condition': ''
            }
    else:
        # If no default location, just pick first saved if exists
        if saved_locs:
            first = saved_locs[0]
            default_location_weather = {
                'location_id': first['location_id'],
                'location_name': first['location_name'],
                'temperature': None,
                'condition': ''
            }
        else:
            # No saved locations at all
            default_location_weather = {
                'location_id': 0,
                'location_name': '',
                'temperature': None,
                'condition': ''
            }
    # Prepare saved_locations list for context
    saved_locations_summary = []
    for loc in saved_locs:
        saved_locations_summary.append({
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'condition': ''  # condition missing in template context --> add
        })
    return render_template('dashboard.html',
                           default_location=default_location_weather,
                           saved_locations=saved_locations_summary)


# Route 3: Current Weather Page
@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weather_data = load_current_weather()
    for cw in current_weather_data:
        if cw['location_id'] == location_id:
            return render_template('current_weather.html',
                                   location_name=cw['location_name'],
                                   temperature=cw['temperature'],
                                   condition=cw['condition'],
                                   humidity=cw['humidity'],
                                   wind_speed=cw['wind_speed'])
    # Location not found or data file missing, render with empty/default values
    return render_template('current_weather.html',
                           location_name='',
                           temperature=None,
                           condition='',
                           humidity=0,
                           wind_speed=0)


# Route 4: Weekly Forecast Page
@app.route('/forecast/weekly', methods=['GET', 'POST'])
def weekly_forecast():
    locations = load_locations()
    forecasts_all = load_forecasts()
    selected_location_id = None

    if request.method == 'POST':
        selected_location_id = request.form.get('location_filter')
        if selected_location_id is not None:
            try:
                selected_location_id = int(selected_location_id)
            except ValueError:
                selected_location_id = None

    # If GET with location_id query param
    if request.method == 'GET':
        loc_id = request.args.get('location_id')
        if loc_id:
            try:
                selected_location_id = int(loc_id)
            except ValueError:
                selected_location_id = None

    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    # Filter forecasts for selected location
    forecasts = []
    if selected_location_id is not None:
        for forecast in forecasts_all:
            if forecast['location_id'] == selected_location_id:
                forecasts.append({
                    'date': forecast['date'],
                    'high_temp': forecast['high_temp'],
                    'low_temp': forecast['low_temp'],
                    'condition': forecast['condition']
                })

    return render_template('weekly_forecast.html',
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id,
                           forecasts=forecasts)


# Route 5: Location Search Page
@app.route('/search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locs = load_saved_locations()
    saved_locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in saved_locs]
    search_results = []

    if request.method == 'POST':
        # Search query from form
        query = request.form.get('query', '').strip().lower()
        if query:
            search_results = [
                {
                    'location_id': loc['location_id'],
                    'location_name': loc['location_name'],
                    'latitude': loc['latitude'],
                    'longitude': loc['longitude']
                }
                for loc in locations if query in loc['location_name'].lower()
            ]
        # Check if user selected a location to save (not persisted)
        selected_location_id = request.form.get('select_location_id')
        if selected_location_id:
            try:
                selected_location_id = int(selected_location_id)
                # No persistence in spec
                pass
            except ValueError:
                pass

    return render_template('location_search.html',
                           search_results=search_results,
                           saved_locations=saved_locations)


# Route 6: Weather Alerts Page
@app.route('/alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = load_alerts()
    saved_locs = load_saved_locations()
    locations = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in saved_locs]
    severity_filter = ''  # Default no filter
    location_filter = None

    # Get filter values from POST or GET
    if request.method == 'POST':
        severity_filter = request.form.get('severity_filter', '')
        loc_filter_val = request.form.get('location_filter')
        try:
            location_filter = int(loc_filter_val) if loc_filter_val else None
        except ValueError:
            location_filter = None
        # Check if acknowledgment button pressed
        ack_alert_id = request.form.get('acknowledge_alert_id')
        if ack_alert_id:
            # Acknowledgment is non-persistent as no db or file write specified
            # We simulate acknowledgment by marking in the list temporarily
            try:
                ack_alert_id = int(ack_alert_id)
                for alert in alerts:
                    if alert['alert_id'] == ack_alert_id:
                        alert['is_acknowledged'] = True
                        break
            except ValueError:
                pass

    # Apply filters
    filtered_alerts = []
    for alert in alerts:
        if severity_filter and alert['severity'] != severity_filter:
            continue
        if location_filter is not None and alert['location_id'] != location_filter:
            continue
        filtered_alerts.append(alert)

    return render_template('alerts.html',
                           alerts=filtered_alerts,
                           locations=locations,
                           selected_location_id=location_filter,
                           severity_filter=severity_filter,
                           location_filter=location_filter)


# Route 7: Air Quality Page
@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = load_locations()
    air_quality_data = load_air_quality()
    selected_location_id = None

    if request.method == 'POST':
        loc_id = request.form.get('location_aqi_filter')
        try:
            selected_location_id = int(loc_id) if loc_id else None
        except ValueError:
            selected_location_id = None

    if selected_location_id is None and locations:
        selected_location_id = locations[0]['location_id']

    aqi_data = {
        'aqi_index': 0,
        'pm25': 0.0,
        'pm10': 0.0,
        'no2': 0.0,
        'o3': 0.0,
        'last_updated': ''
    }
    description = ''
    health_recommendation = ''

    for aqi in air_quality_data:
        if aqi['location_id'] == selected_location_id:
            aqi_data = {
                'aqi_index': aqi['aqi_index'],
                'pm25': aqi['pm25'],
                'pm10': aqi['pm10'],
                'no2': aqi['no2'],
                'o3': aqi['o3'],
                'last_updated': aqi['last_updated']
            }
            description, health_recommendation = get_aqi_description_and_recommendation(aqi_data['aqi_index'])
            break

    return render_template('air_quality.html',
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id,
                           aqi_data=aqi_data,
                           description=description,
                           health_recommendation=health_recommendation)


# Route 8: Saved Locations Page
@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    saved_locs = load_saved_locations()
    current_weather = load_current_weather()

    # POST handling for view/remove not specified for persistence (no file write), so just ignore actual changes
    if request.method == 'POST':
        # We could have keys to view or remove locations
        # But no persistence required per spec
        pass

    saved_locations_list = []
    for saved in saved_locs:
        # find current weather for location
        temp = None
        cond = ''
        for cw in current_weather:
            if cw['location_id'] == saved['location_id']:
                temp = cw['temperature']
                cond = cw['condition']
                break
        saved_locations_list.append({
            'location_id': saved['location_id'],
            'location_name': saved['location_name'],
            'temperature': temp,
            'condition': cond
        })

    return render_template('saved_locations.html',
                           saved_locations=saved_locations_list)


# Route 9: Settings Page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    saved_locs = load_saved_locations()
    temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]
    # Defaults
    selected_unit = "Celsius"
    default_location_id = 0
    alert_notifications_enabled = False

    # Load current settings from a pseudo persistence file (not specified in spec, so defaults only)
    # POST: update settings (not persisted to disk as no file specified)
    if request.method == 'POST':
        selected_unit = request.form.get('temperature_unit', selected_unit)
        try:
            default_location_id = int(request.form.get('default_location_id', default_location_id))
        except ValueError:
            default_location_id = 0
        alert_notifications_enabled = (request.form.get('alert_notifications_enabled') == 'on')

    # Prepare saved_locations context
    saved_locations_summary = [{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in saved_locs]

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           selected_unit=selected_unit,
                           saved_locations=saved_locations_summary,
                           default_location_id=default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
