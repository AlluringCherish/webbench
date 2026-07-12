from flask import Flask, render_template, request, redirect, url_for, abort, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Helper functions to load data

def load_current_weather():
    data = []
    try:
        with open('data/current_weather.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 7:
                    location_id, location_name, temperature, condition, humidity, wind_speed, last_updated = parts
                    if location_id.isdigit() and temperature.replace('.','',1).isdigit() and condition.isdigit():
                        data.append({
                            'location_id': int(location_id),
                            'location_name': location_name,
                            'temperature': float(temperature),
                            'condition': int(condition),
                            'humidity': humidity,
                            'wind_speed': wind_speed,
                            'last_updated': last_updated
                        })
    except FileNotFoundError:
        pass
    return data

def load_locations():
    data = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    location_id, location_name, country, latitude, longitude, elevation = parts
                    if location_id.isdigit():
                        data.append({
                            'location_id': int(location_id),
                            'location_name': location_name,
                            'country': country,
                            'latitude': latitude,
                            'longitude': longitude,
                            'elevation': elevation
                        })
    except FileNotFoundError:
        pass
    return data

def load_alerts():
    data = []
    try:
        with open('data/alerts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 8:
                    alert_id, alert_type, severity, description, start_time, end_time, location_id, acknowledged = parts
                    if alert_id.isdigit():
                        data.append({
                            'alert_id': int(alert_id),
                            'alert_type': alert_type,
                            'severity': severity,
                            'description': description,
                            'start_time': start_time,
                            'end_time': end_time,
                            'location_id': int(location_id) if location_id.isdigit() else None,
                            'acknowledged': acknowledged == '1'
                        })
    except FileNotFoundError:
        pass
    return data

def load_air_quality():
    data = []
    try:
        with open('data/airquality.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 8:
                    aqi_id, aqi_index, aqi_desc, pm25, pm10, no2, o3, last_updated = parts
                    if aqi_index.isdigit():
                        data.append({
                            'aqi_index': int(aqi_index),
                            'aqi_description': aqi_desc,
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
        with open('data/savedlocations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    saved_id, user_id, location_id, location_name, timestamp = parts
                    if location_id.isdigit():
                        data.append({
                            'saved_id': int(saved_id),
                            'user_id': user_id,
                            'location_id': int(location_id),
                            'location_name': location_name,
                            'timestamp': timestamp
                        })
    except FileNotFoundError:
        pass
    return data

def find_current_weather_by_location(current_weather_data, location_id):
    for item in current_weather_data:
        if item['location_id'] == location_id:
            return item
    return None

@app.route('/')
def root_redirect():
    return redirect(url_for('dash_board'))

@app.route('/dash')
def dash_board():
    current_weather = load_current_weather()
    saved_locations = load_saved_locations()

    default_loc_id = None
    if saved_locations:
        default_loc_id = saved_locations[0]['location_id']
    elif current_weather:
        default_loc_id = current_weather[0]['location_id']

    default_location = find_current_weather_by_location(current_weather, default_loc_id) if default_loc_id else None

    # Ensure default_location has expected keys or fallback values
    if default_location:
        default_location.setdefault('temperature', 'N/A')
        default_location.setdefault('condition', 'N/A')
    else:
        default_location = {'location_name': 'No default location', 'temperature': 'N/A', 'condition': 'N/A'}

    return render_template('dash.html', default_location=default_location)

@app.route('/currentweather/<int:location_id>')
def get_current_weather(location_id):
    current_weather = load_current_weather()
    cw = find_current_weather_by_location(current_weather, location_id)
    if not cw:
        abort(404)
    return render_template('currentweather.html', location=cw, temperature=cw['temperature'], 
                           condition=cw['condition'], humidity=cw['humidity'], 
                           wind_speed=cw['wind_speed'])

@app.route('/weeklyforecast', methods=['GET', 'POST'])
def weeklyForecast():
    locations = load_locations()
    if request.method == 'POST':
        selected_location = int(request.form.get('location_filter', 0))
    else:
        selected_location = locations[0]['location_id'] if locations else 0
    forecast_list = []
    for i in range(7):
        forecast_list.append({
            'date': f'2024-06-{10 + i}',
            'high_temp': 25 + i,
            'low_temp': 15 + i,
            'condition': 'Sunny' if i % 2 == 0 else 'Cloudy',
            'location_id': selected_location
        })
    return render_template('forecastlist.html', locations=locations, forecast_list=forecast_list, selected_location=selected_location)

@app.route('/search', methods=['GET', 'POST'])
def location_search():
    locations = load_locations()
    saved_locations = load_saved_locations()
    search_results = []
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('location_search_input', '').strip().lower()
        if search_query:
            for loc in locations:
                if search_query in loc['location_name'].lower():
                    search_results.append(loc)
        selected_location_id = request.form.get('selected_location_id')
        if selected_location_id:
            if not any(loc['location_id'] == int(selected_location_id) for loc in saved_locations):
                saved_locations.append({
                    'saved_id': len(saved_locations) + 1,
                    'user_id': 'default_user',
                    'location_id': int(selected_location_id),
                    'location_name': next((loc['location_name'] for loc in locations if loc['location_id'] == int(selected_location_id)), ''),
                    'timestamp': ''
                })
            flash('Location added to saved locations.')
    return render_template('search.html', search_results=search_results, search_query=search_query, saved_locations=saved_locations)

@app.route('/alerts/all', methods=['GET', 'POST'])
def weatherAlert():
    locations = load_locations()
    alerts = load_alerts()
    severity_filter = ['Critical', 'Medium', 'Low']
    selected_location = None
    selected_severity = None
    if request.method == 'POST':
        selected_severity = request.form.get('severity_filter')
        selected_location = request.form.get('location_filter_alerts')
        if selected_location:
            selected_location = int(selected_location)
        alert_id_ack = request.form.get('alert_id')
        if alert_id_ack:
            for alert in alerts:
                if alert['alert_id'] == int(alert_id_ack):
                    alert['acknowledged'] = True
            flash('Alert acknowledged.')
    filtered_alerts = []
    for alert in alerts:
        if selected_severity and alert['severity'] != selected_severity:
            continue
        if selected_location and alert['location_id'] != selected_location:
            continue
        filtered_alerts.append(alert)
    return render_template('alert.html', alerts=filtered_alerts, severity_filter=severity_filter, locations=locations, selected_location=selected_location)

@app.route('/quality_air', methods=['GET', 'POST'])
def airQuality():
    locations = load_locations()
    aqi_data = load_air_quality()
    selected_location = None
    health_recommendation = "No health recommendations available."
    if request.method == 'POST':
        selected_location = request.form.get('location_aqi_filter')
        if selected_location:
            selected_location = int(selected_location)
    selected_aqi_data = [aqi for aqi in aqi_data if True]
    if selected_aqi_data:
        aqi_val = selected_aqi_data[0]['aqi_index']
        if aqi_val <= 50:
            health_recommendation = "Air quality is good."
        elif aqi_val <= 100:
            health_recommendation = "Air quality is moderate; consider limiting outdoor activities."
        else:
            health_recommendation = "Air quality is poor; avoid outdoor activities."
    return render_template('aqi.html', aqi_data=selected_aqi_data, locations=locations, selected_location=selected_location, health_recommendation=health_recommendation)

@app.route('/locations/savelocations', methods=['GET', 'POST'])
def savedLocation():
    locations = load_locations()
    saved_locations_data = load_saved_locations()
    if request.method == 'POST':
        remove_location_id = request.form.get('remove_location_id')
        if remove_location_id:
            saved_locations_data = [loc for loc in saved_locations_data if loc['location_id'] != int(remove_location_id)]
            flash('Location removed from saved locations.')
    saved_locations_dict = []
    current_weather = load_current_weather()
    for saved_loc in saved_locations_data:
        cw = find_current_weather_by_location(current_weather, saved_loc['location_id'])
        saved_locations_dict.append({
            'location_id': saved_loc['location_id'],
            'location_name': saved_loc['location_name'],
            'current_temp': cw['temperature'] if cw else '',
            'condition': cw['condition'] if cw else 0
        })
    return render_template('savedlocation.html', saved_locations=saved_locations_dict)

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
    locations = load_locations()
    selected_unit = "Celsius"
    selected_default_location = None
    alert_notifications_enabled = 1
    if request.method == 'POST':
        selected_unit = request.form.get('temperature_unit_select', "Celsius")
        selected_default_location = request.form.get('default_location_select')
        alert_notifications_enabled = int(request.form.get('alert_notifications', '1'))
        flash('Settings saved.')
    locations_dict = [{
        'location_id': loc['location_id'],
        'location_name': loc['location_name']
    } for loc in locations]
    if not selected_default_location and locations_dict:
        selected_default_location = locations_dict[0]['location_id']
    else:
        try:
            selected_default_location = int(selected_default_location)
        except:
            selected_default_location = None
    return render_template('setting.html',
                           temperatures=temp_units,
                           selected_unit=selected_unit,
                           locations=locations_dict,
                           selected_default_location=selected_default_location,
                           alert_notifications_enabled=alert_notifications_enabled)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
