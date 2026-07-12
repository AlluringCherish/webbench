from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions to load data from text files

def load_current_weather():
    current_weather = {}
    try:
        with open('data/current_weather.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    location_id = int(parts[0])
                    location_name = parts[1]
                    temperature = float(parts[2])
                    condition = parts[3]
                    humidity = int(parts[4])
                    wind_speed = float(parts[5])
                    last_updated = parts[6]
                    current_weather[location_id] = {
                        'location_id': location_id,
                        'location_name': location_name,
                        'temperature': temperature,
                        'condition': condition,
                        'humidity': humidity,
                        'wind_speed': wind_speed,
                        'last_updated': last_updated
                    }
    except FileNotFoundError:
        # Handle file not found: return empty dict
        pass
    return current_weather

def load_forecasts():
    forecasts = []
    try:
        with open('data/forecasts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        forecast_id = int(parts[0])
                        location_id = int(parts[1])
                        date = parts[2]
                        high_temp = float(parts[3])
                        low_temp = float(parts[4])
                        condition = parts[5]
                        precipitation = int(parts[6])
                        humidity = int(parts[7])
                        forecasts.append({
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
                        # ignore malformed lines
                        pass
    except FileNotFoundError:
        # Handle file not found: return empty list
        pass
    return forecasts

def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
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
                        locations.append({
                            'location_id': location_id,
                            'location_name': location_name,
                            'latitude': latitude,
                            'longitude': longitude,
                            'country': country,
                            'timezone': timezone
                        })
                    except ValueError:
                        # ignore malformed lines
                        pass
    except FileNotFoundError:
        # Handle file not found: return empty list
        pass
    return locations

def load_alerts():
    alerts = []
    try:
        with open('data/alerts.txt', 'r', encoding='utf-8') as f:
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
                        is_acknowledged = parts[7].strip() == '1'
                        alerts.append({
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
                        # ignore malformed lines
                        pass
    except FileNotFoundError:
        # Handle file not found: return empty list
        pass
    return alerts

def load_air_quality():
    air_quality = {}
    try:
        with open('data/air_quality.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        aqi_id = int(parts[0])  # not used for dict key
                        location_id = int(parts[1])
                        aqi_index = int(parts[2])
                        pm25 = float(parts[3])
                        pm10 = float(parts[4])
                        no2 = float(parts[5])
                        o3 = float(parts[6])
                        last_updated = parts[7]
                        air_quality[location_id] = {
                            'aqi_index': aqi_index,
                            'pm25': pm25,
                            'pm10': pm10,
                            'no2': no2,
                            'o3': o3,
                            'last_updated': last_updated
                        }
                    except ValueError:
                        # ignore malformed lines
                        pass
    except FileNotFoundError:
        # Handle file not found: return empty dict
        pass
    return air_quality

def load_saved_locations():
    saved_locations = []
    try:
        with open('data/saved_locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        saved_id = int(parts[0])
                        # user_id is not used as per spec
                        location_id = int(parts[2])
                        location_name = parts[3]
                        is_default = parts[4].strip() == '1'
                        saved_locations.append({
                            'saved_id': saved_id,
                            'location_id': location_id,
                            'location_name': location_name,
                            'is_default': is_default
                        })
                    except ValueError:
                        # ignore malformed lines
                        pass
    except FileNotFoundError:
        # Handle file not found: return empty list
        pass
    return saved_locations


# Helper function to get location by id from a list

def find_location_by_id(locations, location_id):
    for loc in locations:
        if loc['location_id'] == location_id:
            return loc
    return None

# Helper function to get weather by location_id

def get_current_weather_for_location(weather_dict, location_id):
    return weather_dict.get(location_id, None)

# Helper function to get forecasts for location

def get_forecasts_for_location(forecasts, location_id):
    return [f for f in forecasts if f['location_id'] == location_id]

# Helper function to get air quality for location

def get_air_quality_for_location(aq_dict, location_id):
    return aq_dict.get(location_id, None)

# Helper function to get saved locations with current weather

def get_saved_locations_with_weather(saved_locations, current_weather):
    result = []
    for sl in saved_locations:
        loc_weather = current_weather.get(sl['location_id'])
        current_temp = loc_weather['temperature'] if loc_weather else None
        current_condition = loc_weather['condition'] if loc_weather else None
        result.append({
            'saved_id': sl['saved_id'],
            'location_id': sl['location_id'],
            'location_name': sl['location_name'],
            'is_default': sl['is_default'],
            'current_temp': current_temp,
            'current_condition': current_condition
        })
    return result

# Helper function to get default location from saved locations

def get_default_location(saved_locations, locations):
    for sl in saved_locations:
        if sl['is_default']:
            # Find full location details
            loc = find_location_by_id(locations, sl['location_id'])
            if loc:
                return {'location_id': loc['location_id'], 'location_name': loc['location_name']}
            else:
                # Fallback to saved location name
                return {'location_id': sl['location_id'], 'location_name': sl['location_name']}
    # If none is default, return None
    return None

#################################################
# Flask Route Implementations
#################################################

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    saved_locations = load_saved_locations()
    locations = load_locations()
    current_weather = load_current_weather()

    default_location = get_default_location(saved_locations, locations)
    # If no default location, fallback to first location
    if not default_location and locations:
        default_location = {'location_id': locations[0]['location_id'], 'location_name': locations[0]['location_name']}

    if default_location:
        cw = get_current_weather_for_location(current_weather, default_location['location_id'])
        if not cw:
            # fallback empty weather dict
            cw = {'temperature': None, 'condition': '', 'humidity': None, 'wind_speed': None, 'last_updated': ''}
    else:
        cw = {'temperature': None, 'condition': '', 'humidity': None, 'wind_speed': None, 'last_updated': ''}

    return render_template('dashboard.html', default_location=default_location, current_weather=cw)

@app.route('/weather/current/<int:location_id>', methods=['GET'])
def current_weather_page(location_id):
    locations = load_locations()
    current_weather = load_current_weather()

    location = find_location_by_id(locations, location_id)
    if not location:
        location = {'location_id': location_id, 'location_name': 'Unknown'}

    cw = get_current_weather_for_location(current_weather, location_id)
    if not cw:
        cw = {'temperature': None, 'condition': '', 'humidity': None, 'wind_speed': None, 'last_updated': ''}

    return render_template('current_weather.html', location=location, current_weather=cw)

@app.route('/forecast/weekly', methods=['GET'])
def weekly_forecast_page():
    locations = load_locations()
    forecasts = load_forecasts()

    # Determine selected location via query param ?location_id=...
    location_id_str = request.args.get('location_id')
    selected_location = None
    if location_id_str:
        try:
            location_id = int(location_id_str)
            selected_location = find_location_by_id(locations, location_id)
        except ValueError:
            selected_location = None

    if not selected_location and locations:
        selected_location = locations[0]

    location_id = selected_location['location_id'] if selected_location else None
    filtered_forecasts = get_forecasts_for_location(forecasts, location_id) if location_id else []

    return render_template('weekly_forecast.html', 
                           locations=locations, 
                           selected_location=selected_location, 
                           forecasts=filtered_forecasts)

@app.route('/locations/search', methods=['GET', 'POST'])
def location_search_page():
    locations = load_locations()
    saved_locations_raw = load_saved_locations()

    saved_locations = [{'location_id': sl['location_id'], 'location_name': sl['location_name']} for sl in saved_locations_raw]
    search_query = ''
    search_results = []

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
    else:
        # Also accept query param as initial search
        search_query = request.args.get('search_query', '').strip()

    if search_query:
        # Case insensitive search in location_name field
        for loc in locations:
            if search_query.lower() in loc['location_name'].lower():
                search_results.append(loc)

    return render_template('location_search.html', 
                           search_query=search_query, 
                           search_results=search_results, 
                           saved_locations=saved_locations)

@app.route('/alerts', methods=['GET', 'POST'])
def weather_alerts_page():
    locations = load_locations()
    alerts = load_alerts()

    severity_filter = ''
    location_filter = None

    if request.method == 'POST':
        # Check if acknowledge alert button pressed
        for key in request.form:
            if key.startswith('acknowledge-alert-button-'):
                alert_id_str = key.replace('acknowledge-alert-button-', '')
                try:
                    alert_id = int(alert_id_str)
                except ValueError:
                    continue
                # Mark alert acknowledged in memory (no file write as per spec)
                for alert in alerts:
                    if alert['alert_id'] == alert_id:
                        alert['is_acknowledged'] = True
                        break

        # Filters
        severity_filter = request.form.get('severity-filter', '').strip()
        location_filter_str = request.form.get('location-filter-alerts', '').strip()
        if location_filter_str.isdigit():
            location_filter = int(location_filter_str)
        else:
            location_filter = None

    else:
        # For GET, get filters from query parameters
        severity_filter = request.args.get('severity_filter', '').strip()
        location_filter_str = request.args.get('location_filter', '').strip()
        if location_filter_str.isdigit():
            location_filter = int(location_filter_str)
        else:
            location_filter = None

    # Apply filters
    filtered_alerts = alerts
    if severity_filter:
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]
    if location_filter is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]

    return render_template('alerts.html', 
                           alerts=filtered_alerts, 
                           severity_filter=severity_filter, 
                           location_filter=location_filter, 
                           locations=locations)

@app.route('/air-quality', methods=['GET'])
def air_quality_page():
    locations = load_locations()
    air_quality = load_air_quality()

    # Select location via query param ?location_id=...
    location_id_str = request.args.get('location_id')
    selected_location = None
    if location_id_str:
        try:
            location_id = int(location_id_str)
            selected_location = find_location_by_id(locations, location_id)
        except ValueError:
            selected_location = None

    if not selected_location and locations:
        selected_location = locations[0]

    location_id = selected_location['location_id'] if selected_location else None
    aq = get_air_quality_for_location(air_quality, location_id) if location_id else None

    aqi_description = ''
    health_recommendation = ''

    if aq:
        aqi_index = aq.get('aqi_index', 0)
        # Define AQI category and health advice based on AQI value
        if aqi_index <= 50:
            aqi_description = 'Good'
            health_recommendation = 'Air quality is satisfactory, and air pollution poses little or no risk.'
        elif aqi_index <= 100:
            aqi_description = 'Moderate'
            health_recommendation = 'Air quality is acceptable; however, there may be a moderate health concern for a very small number of people.'
        elif aqi_index <= 150:
            aqi_description = 'Unhealthy for Sensitive Groups'
            health_recommendation = 'Members of sensitive groups may experience health effects. General public unlikely affected.'
        elif aqi_index <= 200:
            aqi_description = 'Unhealthy'
            health_recommendation = 'Everyone may begin to experience health effects; sensitive groups may experience more serious effects.'
        elif aqi_index <= 300:
            aqi_description = 'Very Unhealthy'
            health_recommendation = 'Health alert: everyone may experience more serious health effects.'
        else:
            aqi_description = 'Hazardous'
            health_recommendation = 'Health warnings of emergency conditions. The entire population is more likely affected.'

    else:
        aq = {'aqi_index': None, 'pm25': None, 'pm10': None, 'no2': None, 'o3': None, 'last_updated': ''}
        aqi_description = ''
        health_recommendation = ''

    return render_template('air_quality.html',
                           locations=locations,
                           selected_location=selected_location,
                           air_quality=aq,
                           aqi_description=aqi_description,
                           health_recommendation=health_recommendation)

@app.route('/locations/saved', methods=['GET', 'POST'])
def saved_locations_page():
    saved_locations_raw = load_saved_locations()
    current_weather = load_current_weather()

    if request.method == 'POST':
        # Handle removing saved location by location_id
        remove_location_id_str = None
        for key in request.form:
            if key.startswith('remove-location-button-'):
                remove_location_id_str = key.replace('remove-location-button-', '')
                break
        if remove_location_id_str is not None:
            try:
                remove_location_id = int(remove_location_id_str)
                # Remove from saved locations list in memory (no file update as per spec)
                saved_locations_raw = [sl for sl in saved_locations_raw if sl['location_id'] != remove_location_id]
            except ValueError:
                pass

    saved_locations = get_saved_locations_with_weather(saved_locations_raw, current_weather)

    return render_template('saved_locations.html', saved_locations=saved_locations)

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    locations = load_locations()
    saved_locations = load_saved_locations()

    # Defaults
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
    selected_unit = 'Celsius'
    default_location_id = None
    alert_notifications_enabled = False

    # Get current default from saved locations
    for sl in saved_locations:
        if sl['is_default']:
            default_location_id = sl['location_id']
            break

    # POST updates (no file writing as per spec)
    if request.method == 'POST':
        selected_unit = request.form.get('temperature_unit', 'Celsius')
        try:
            default_location_id = int(request.form.get('default_location_id'))
        except (TypeError, ValueError):
            default_location_id = None
        alert_notifications_enabled = request.form.get('alert_notifications_enabled') == 'on'

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           selected_unit=selected_unit,
                           locations=locations,
                           default_location_id=default_location_id if default_location_id is not None else -1,
                           alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
