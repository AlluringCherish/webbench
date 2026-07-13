from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)

data_dir = 'data'

# Helper functions to read and parse data files

def read_current_weather():
    filepath = os.path.join(data_dir, 'current_weather.txt')
    weather_data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    location_id = parts[0]
                    weather_data[location_id] = {
                        'location_id': parts[0],
                        'location_name': parts[1],
                        'temperature': parts[2],
                        'condition': parts[3],
                        'humidity': parts[4],
                        'wind_speed': parts[5],
                        'last_updated': parts[6]
                    }
    return weather_data

def read_forecasts():
    filepath = os.path.join(data_dir, 'forecasts.txt')
    forecasts = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    forecasts.append({
                        'forecast_id': parts[0],
                        'location_id': parts[1],
                        'date': parts[2],
                        'high_temp': parts[3],
                        'low_temp': parts[4],
                        'condition': parts[5],
                        'precipitation': parts[6],
                        'humidity': parts[7]
                    })
    return forecasts

def read_locations():
    filepath = os.path.join(data_dir, 'locations.txt')
    locations = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    locations.append({
                        'location_id': parts[0],
                        'location_name': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3],
                        'country': parts[4],
                        'timezone': parts[5]
                    })
    return locations

def read_alerts():
    filepath = os.path.join(data_dir, 'alerts.txt')
    alerts = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    alerts.append({
                        'alert_id': parts[0],
                        'location_id': parts[1],
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7]
                    })
    return alerts

def read_air_quality():
    filepath = os.path.join(data_dir, 'air_quality.txt')
    aqi_list = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    aqi_list.append({
                        'aqi_id': parts[0],
                        'location_id': parts[1],
                        'aqi_index': int(parts[2]),
                        'pm25': parts[3],
                        'pm10': parts[4],
                        'no2': parts[5],
                        'o3': parts[6],
                        'last_updated': parts[7]
                    })
    return aqi_list

def read_saved_locations(user_id='1'):
    filepath = os.path.join(data_dir, 'saved_locations.txt')
    saved = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 5 and parts[1] == user_id:
                    saved.append({
                        'saved_id': parts[0],
                        'user_id': parts[1],
                        'location_id': parts[2],
                        'location_name': parts[3],
                        'is_default': parts[4] == '1'
                    })
    return saved

def write_saved_locations(saved_list, user_id='1'):
    filepath = os.path.join(data_dir, 'saved_locations.txt')
    with open(filepath, 'w') as file:
        for item in saved_list:
            if item['user_id'] == user_id:
                line = '|'.join([
                    item['saved_id'],
                    item['user_id'],
                    item['location_id'],
                    item['location_name'],
                    '1' if item['is_default'] else '0'
                ])
                file.write(line + '\n')

# Utility to get air quality description from AQI index
# and health recommendation based on AQI

def aqi_description(index):
    if index <= 50:
        return 'Good'
    elif index <= 100:
        return 'Moderate'
    elif index <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif index <= 200:
        return 'Unhealthy'
    elif index <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

def health_recommendation(index):
    if index <= 50:
        return 'Air quality is satisfactory, and air pollution poses little or no risk.'
    elif index <= 100:
        return 'Air quality is acceptable; however, some pollutants may be a moderate health concern.'
    elif index <= 150:
        return 'Members of sensitive groups may experience health effects.'
    elif index <= 200:
        return 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious effects.'
    elif index <= 300:
        return 'Health warnings of emergency conditions. The entire population is more likely to be affected.'
    else:
        return 'Health alert: everyone may experience more serious health effects.'

# Helper to get default location id for user

def get_default_location_id(user_id='1'):
    saved_locations = read_saved_locations(user_id)
    for loc in saved_locations:
        if loc['is_default']:
            return loc['location_id']
    # fallback to first saved if exist
    if saved_locations:
        return saved_locations[0]['location_id']
    return None

# ROUTES

@app.route('/')
def dashboard():
    # Show current weather summary for default location
    user_id = '1'
    saved_locations = read_saved_locations(user_id)
    default_location_id = get_default_location_id(user_id)
    current_weather = read_current_weather()

    if default_location_id and default_location_id in current_weather:
        weather = current_weather[default_location_id]
    else:
        weather = None

    return render_template('dashboard.html', weather=weather)

@app.route('/current_weather/<location_id>')
def current_weather(location_id):
    # Display current weather for given location
    current_weather = read_current_weather()
    weather = current_weather.get(location_id)
    if not weather:
        return "Location not found", 404
    return render_template('current_weather.html', weather=weather)

@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    forecasts = read_forecasts()
    locations = read_locations()

    selected_location = request.args.get('location_id')
    if not selected_location and locations:
        selected_location = locations[0]['location_id']

    if selected_location:
        filtered_forecasts = [f for f in forecasts if f['location_id'] == selected_location]
    else:
        filtered_forecasts = forecasts

    return render_template('weekly_forecast.html', 
                           forecasts=filtered_forecasts, 
                           locations=locations, 
                           selected_location=selected_location)

@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    locations = read_locations()
    saved_locations = read_saved_locations()
    search_query = request.args.get('q', '')
    filtered_locations = []
    if search_query:
        q = search_query.lower()
        for loc in locations:
            if q in loc['location_name'].lower() or q in loc['latitude'] or q in loc['longitude']:
                filtered_locations.append(loc)
    else:
        filtered_locations = locations

    if request.method == 'POST':
        selected_location_id = request.form.get('select_location_id')
        if selected_location_id:
            # Redirect to current weather page for selected location
            return redirect(url_for('current_weather', location_id=selected_location_id))

    return render_template('location_search.html', 
                           locations=filtered_locations,
                           saved_locations=saved_locations,
                           search_query=search_query)

@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = read_alerts()
    locations = read_locations()
    severities = ['All', 'Critical', 'High', 'Medium', 'Low']

    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location_id', 'All')

    filtered_alerts = alerts

    # Filter by severity
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]

    # Filter by location
    if location_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]

    if request.method == 'POST':
        # Acknowledge alert
        alert_id_to_ack = request.form.get('acknowledge_alert_id')
        if alert_id_to_ack:
            for alert in alerts:
                if alert['alert_id'] == alert_id_to_ack:
                    alert['is_acknowledged'] = '1'
                    # Write back to file
                    filepath = os.path.join(data_dir, 'alerts.txt')
                    with open(filepath, 'w') as file:
                        for a in alerts:
                            line = '|'.join([
                                a['alert_id'],
                                a['location_id'],
                                a['alert_type'],
                                a['severity'],
                                a['description'],
                                a['start_time'],
                                a['end_time'],
                                a['is_acknowledged']
                            ])
                            file.write(line + '\n')
                    break
            return redirect(url_for('weather_alerts'))

    return render_template('weather_alerts.html', alerts=filtered_alerts, locations=locations, severities=severities, selected_severity=severity_filter, selected_location=location_filter)

@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    aqi_list = read_air_quality()
    locations = read_locations()
    selected_location = request.args.get('location_id')
    if not selected_location and locations:
        selected_location = locations[0]['location_id']

    filtered_aqi_list = [aqi for aqi in aqi_list if aqi['location_id'] == selected_location] if selected_location else aqi_list

    aqi = filtered_aqi_list[0] if filtered_aqi_list else None
    aqi_desc = aqi_description(aqi['aqi_index']) if aqi else None
    recommendation = health_recommendation(aqi['aqi_index']) if aqi else None

    return render_template('air_quality.html',
                           aqi=aqi,
                           aqi_desc=aqi_desc,
                           recommendation=recommendation,
                           locations=locations,
                           selected_location=selected_location)

@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    user_id = '1'
    saved = read_saved_locations(user_id)
    current_weather = read_current_weather()

    if request.method == 'POST':
        # Remove location
        remove_id = request.form.get('remove_location_id')
        if remove_id:
            saved = [loc for loc in saved if loc['saved_id'] != remove_id]
            write_saved_locations(saved, user_id)
            return redirect(url_for('saved_locations'))

    return render_template('saved_locations.html', saved_locations=saved, current_weather=current_weather)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = '1'
    saved = read_saved_locations(user_id)
    locations = read_locations()

    # For simplicity, store settings in memory - could extend to file
    temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
    alert_notifications_enabled = True

    if request.method == 'POST':
        # Save settings (not persisting in file system in this example)
        temperature_unit = request.form.get('temperature_unit')
        default_location = request.form.get('default_location')
        alert_notifications = request.form.get('alert_notifications')

        # Update default location in saved locations
        for loc in saved:
            loc['is_default'] = (loc['location_id'] == default_location)
        write_saved_locations(saved, user_id)

        # Simulating alert notification toggle update
        alert_notifications_enabled = (alert_notifications == 'on')

        # Redirect after saving
        return redirect(url_for('dashboard'))

    # Get current settings
    default_location_id = get_default_location_id(user_id)
    temperature_unit = 'Celsius'  # default
    alert_notifications = True

    return render_template('settings.html',
                           temperature_units=temperature_units,
                           default_location_id=default_location_id,
                           saved_locations=saved,
                           alert_notifications=alert_notifications)

if __name__ == '__main__':
    app.run(debug=True)
