from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

USER_ID = 1  # single user context

@app.route('/')
def dashboard():
    # TODO: Load current_weather.txt and default location info
    current_weather = {
        'location_id': 1,
        'location_name': 'Sample City',
        'temperature': 70,
        'condition': 'Sunny',
        'humidity': 45,
        'wind_speed': 5
    }
    default_location_id = current_weather['location_id']
    return render_template('dashboard.html', current_weather=current_weather, default_location_id=default_location_id)

@app.route('/current_weather/<int:location_id>')
def current_weather(location_id):
    # TODO: Lookup current_weather.txt for location_id
    weather = {
        'location_name': 'Sample City',
        'temperature': 70,
        'condition': 'Sunny',
        'humidity': 45,
        'wind_speed': 5
    }
    return render_template('current_weather.html', weather=weather)

@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    if request.method == 'POST':
        selected_location_id = int(request.form.get('location-filter', 1))
    else:
        selected_location_id = 1
    # TODO: Load forecasts filtered by location_id
    forecasts = [
        {'forecast_id': 1, 'date': '2024-06-01', 'high_temp': 75, 'low_temp': 55, 'condition': 'Sunny', 'precipitation': 0, 'humidity': 40},
        {'forecast_id': 2, 'date': '2024-06-02', 'high_temp': 70, 'low_temp': 52, 'condition': 'Cloudy', 'precipitation': 10, 'humidity': 50}
    ]
    # TODO: Load all locations
    locations = [
        {'location_id': 1, 'location_name': 'Sample City'},
        {'location_id': 2, 'location_name': 'Example City'}
    ]
    return render_template('weekly_forecast.html', locations=locations, selected_location_id=selected_location_id, forecasts=forecasts)

@app.route('/location_search', methods=['GET', 'POST'])
def location_search():
    if request.method == 'POST':
        search_query = request.form.get('location-search-input', '')
        # TODO: Search locations.txt for matches
        search_results = [
            {'location_id': 1, 'location_name': 'Sample City', 'country': 'CountryA'},
            {'location_id': 2, 'location_name': 'Example City', 'country': 'CountryB'}
        ]
    else:
        search_query = ''
        search_results = []
    # TODO: Load saved locations for USER_ID
    saved_locations = [
        {'location_id': 1, 'location_name': 'Sample City', 'is_default': True},
        {'location_id': 2, 'location_name': 'Example City', 'is_default': False}
    ]
    return render_template('location_search.html', search_query=search_query, search_results=search_results, saved_locations=saved_locations)

@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    if request.method == 'POST':
        selected_severity = request.form.get('severity-filter', None) or None
        selected_location_id = request.form.get('location-filter-alerts', None)
        selected_location_id = int(selected_location_id) if selected_location_id else None
        # TODO: Handle acknowledge alert POST or filters
    else:
        selected_severity = None
        selected_location_id = None
    # TODO: Load alerts filtered by severity/location
    alerts = [
        {'alert_id': 1, 'location_name': 'Sample City', 'alert_type': 'Storm', 'severity': 'High', 'description': 'Heavy storm warning', 'start_time': '2024-06-01 09:00', 'end_time': '2024-06-01 18:00', 'is_acknowledged': False},
        {'alert_id': 2, 'location_name': 'Example City', 'alert_type': 'Heat', 'severity': 'Medium', 'description': 'Heat advisory', 'start_time': '2024-06-02 12:00', 'end_time': '2024-06-02 22:00', 'is_acknowledged': True}
    ]
    # TODO: Load all location options
    location_options = [
        {'location_id': 1, 'location_name': 'Sample City'},
        {'location_id': 2, 'location_name': 'Example City'}
    ]
    return render_template('weather_alerts.html', alerts=alerts, location_options=location_options, selected_severity=selected_severity, selected_location_id=selected_location_id)

@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    if request.method == 'POST':
        selected_location_id = int(request.form.get('location-aqi-filter', 1))
    else:
        selected_location_id = 1
    # TODO: Load locations
    locations = [
        {'location_id': 1, 'location_name': 'Sample City'},
        {'location_id': 2, 'location_name': 'Example City'}
    ]
    # TODO: Load air quality data filtered by location
    aqi_data = {
        'aqi_index': 45,
        'pm25': 12.3,
        'pm10': 20.5,
        'no2': 15.1,
        'o3': 10.4,
        'last_updated': '2024-06-01 08:00'
    }
    health_advice = 'Air quality is good. No precautions necessary.'
    return render_template('air_quality.html', locations=locations, selected_location_id=selected_location_id, aqi_data=aqi_data, health_advice=health_advice)

@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    if request.method == 'POST':
        # TODO: Handle add/remove post actions
        pass
    saved_locations = [
        {'location_id': 1, 'location_name': 'Sample City', 'is_default': True},
        {'location_id': 2, 'location_name': 'Example City', 'is_default': False}
    ]
    return render_template('saved_locations.html', saved_locations=saved_locations)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # TODO: Update settings from form data
        pass
    temperature_unit = 'F'
    locations = [
        {'location_id': 1, 'location_name': 'Sample City'},
        {'location_id': 2, 'location_name': 'Example City'}
    ]
    default_location_id = 1
    alert_notifications_enabled = True
    return render_template('settings.html', temperature_unit=temperature_unit, locations=locations, default_location_id=default_location_id, alert_notifications_enabled=alert_notifications_enabled)

if __name__ == '__main__':
    app.run(debug=True)
