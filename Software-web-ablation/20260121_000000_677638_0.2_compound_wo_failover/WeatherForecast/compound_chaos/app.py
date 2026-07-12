from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for demonstration
location_aqi_filter = [
    {'location_id': 1, 'location_name': 'Location A'},
    {'location_id': 2, 'location_name': 'Location B'},
]

aqi_data = {
    'aqi_index': 75,
    'pm25': 35,
    'o3': 20
}
health_recommendation = 'Moderate air quality. Consider reducing prolonged or heavy exertion.'

severity_options = ['Low', 'Moderate', 'High', 'Critical']
locations_filter_alerts = location_aqi_filter
alerts_list = [
    {'alert_id': 101, 'alert_type': 'Storm', 'severity': 'High', 'description': 'Severe storm expected.', 'start_time': '2024-07-01 10:00', 'end_time': '2024-07-01 18:00', 'is_acknowledged': 0},
    {'alert_id': 102, 'alert_type': 'Flood', 'severity': 'Moderate', 'description': 'Flood warning.', 'start_time': '2024-07-02 12:00', 'end_time': '2024-07-02 20:00', 'is_acknowledged': 1},
]

current_weather = {
    'location_name': 'Location A',
    'temperature': 25,
    'condition': 'Sunny',
    'humidity': 40,
    'wind_speed': 10,
    'last_updated': '2024-06-30 14:00'
}

search_results = [
    {'location_id': 1, 'country': 'CountryA', 'location_name': 'Location A'},
    {'location_id': 2, 'country': 'CountryB', 'location_name': 'Location B'}
]

saved_locations = [
    {'location_id': 1, 'location_name': 'Location A', 'is_default': 1, 'current_temperature': 25, 'condition': 'Sunny'},
    {'location_id': 2, 'location_name': 'Location B', 'is_default': 0, 'current_temperature': 18, 'condition': 'Cloudy'}
]

# Settings example values
temperature_unit_options = ['Celsius', 'Fahrenheit']
selected_temperature_unit = 'Celsius'
default_location_options = location_aqi_filter
selected_default_location_id = 1
alert_notifications_enabled = True

forecast_list = [
    {'date': '2024-07-01', 'high_temp': 30, 'low_temp': 20, 'condition': 'Sunny'},
    {'date': '2024-07-02', 'high_temp': 28, 'low_temp': 19, 'condition': 'Cloudy'}
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html', current_weather=current_weather)

@app.route('/air_quality')
def air_quality():
    selected_location_id = request.args.get('location_id', type=int, default=1)
    # Simulate filtering data by selected_location_id
    return render_template('air_quality.html', location_aqi_filter=location_aqi_filter, selected_location_id=selected_location_id, aqi_data=aqi_data, health_recommendation=health_recommendation)

@app.route('/alerts')
def weather_alerts():
    selected_severity = request.args.get('severity', default='Low')
    selected_location_id = request.args.get('location_id', type=int, default=1)
    filtered_alerts = [alert for alert in alerts_list if alert['severity'] == selected_severity or selected_severity == 'Low']
    return render_template('alerts.html', severity_options=severity_options, selected_severity=selected_severity, locations_filter_alerts=locations_filter_alerts, selected_location_id=selected_location_id, alerts_list=filtered_alerts)

@app.route('/current_weather')
def current_weather_view():
    location_id = request.args.get('location_id', type=int, default=1)
    # This would fetch weather data based on location_id
    return render_template('current_weather.html', temperature=current_weather['temperature'], condition=current_weather['condition'], humidity=current_weather['humidity'], wind_speed=current_weather['wind_speed'], location_name=current_weather['location_name'])

@app.route('/saved_locations')
def saved_locations_view():
    return render_template('saved_locations.html', saved_locations=saved_locations)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global selected_temperature_unit, selected_default_location_id, alert_notifications_enabled
    if request.method == 'POST':
        selected_temperature_unit = request.form.get('temperature_unit')
        selected_default_location_id = int(request.form.get('default_location', 1))
        alert_notifications_enabled = 'alert_notifications_enabled' in request.form
        return redirect(url_for('dashboard'))
    return render_template('settings.html', temperature_unit_options=temperature_unit_options, selected_temperature_unit=selected_temperature_unit, default_location_options=default_location_options, selected_default_location_id=selected_default_location_id, alert_notifications_enabled=alert_notifications_enabled)

@app.route('/weekly_forecast')
def weekly_forecast():
    selected_location_id = request.args.get('location_id', type=int, default=1)
    return render_template('weekly_forecast.html', location_filter=location_aqi_filter, selected_location_id=selected_location_id, forecast_list=forecast_list)

@app.route('/location_search')
def location_search():
    return render_template('dashboard.html', search_results=search_results, saved_locations=saved_locations, current_weather=current_weather)

if __name__ == '__main__':
    app.run(debug=True)
