'''
Backend Flask application for the weather dashboard system.
- Serves eight pages: Dashboard, Weather, Weekly Forecast, Location Search,
  Weather Alerts, Air Quality, Saved Locations, Settings.
- Reads/writes data from/to text files in 'data' directory.
- Implements business logic for displaying current weather, forecasts,
  alerts, air quality, saved locations.
- Manages navigation and user interactions.
- Runs on local port 5000, root URL '/' serves Dashboard page.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_current_weather():
    path = os.path.join(DATA_DIR, 'current_weather.txt')
    weather = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                location_id = parts[0]
                weather[location_id] = {
                    'location_id': location_id,
                    'location_name': parts[1],
                    'temperature': parts[2],
                    'condition': parts[3],
                    'humidity': parts[4],
                    'wind_speed': parts[5],
                    'last_updated': parts[6]
                }
    return weather
def read_forecasts():
    path = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                location_id = parts[0]
                locations[location_id] = {
                    'location_id': location_id,
                    'location_name': parts[1],
                    'latitude': parts[2],
                    'longitude': parts[3],
                    'country': parts[4],
                    'timezone': parts[5]
                }
    return locations
def read_alerts():
    path = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    path = os.path.join(DATA_DIR, 'air_quality.txt')
    air_quality = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                location_id = parts[1]
                air_quality[location_id] = {
                    'aqi_id': parts[0],
                    'location_id': location_id,
                    'aqi_index': parts[2],
                    'pm25': parts[3],
                    'pm10': parts[4],
                    'no2': parts[5],
                    'o3': parts[6],
                    'last_updated': parts[7]
                }
    return air_quality
def read_saved_locations():
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                saved.append({
                    'saved_id': parts[0],
                    'user_id': parts[1],
                    'location_id': parts[2],
                    'location_name': parts[3],
                    'is_default': parts[4]
                })
    return saved
@app.route('/')
def dashboard():
    current_weather = read_current_weather()
    saved_locations = read_saved_locations()
    locations = read_locations()
    # For dashboard, show current weather for default saved location or first saved location
    default_location = None
    for loc in saved_locations:
        if loc['is_default'] == '1':
            default_location = loc
            break
    if not default_location and saved_locations:
        default_location = saved_locations[0]
    weather_info = None
    if default_location:
        weather_info = current_weather.get(default_location['location_id'])
    return render_template('dashboard.html',
                           weather=weather_info,
                           saved_locations=saved_locations,
                           locations=locations)
@app.route('/weather/<location_id>')
def weather(location_id):
    current_weather = read_current_weather()
    locations = read_locations()
    weather_info = current_weather.get(location_id)
    location = locations.get(location_id)
    if not weather_info or not location:
        return "Location or weather data not found", 404
    return render_template('current_weather.html',
                           weather=weather_info,
                           location=location)
@app.route('/weekly_forecast')
def weekly_forecast():
    location_id = request.args.get('location_id')
    forecasts = read_forecasts()
    locations = read_locations()
    filtered_forecasts = []
    if location_id:
        filtered_forecasts = [f for f in forecasts if f['location_id'] == location_id]
    else:
        filtered_forecasts = forecasts
    return render_template('weekly_forecast.html',
                           forecasts=filtered_forecasts,
                           locations=locations,
                           selected_location=location_id)
@app.route('/locations')
def locations_page():
    locations = read_locations()
    saved_locations = read_saved_locations()
    # Pass saved_locations to template for saved locations list
    return render_template('location_search.html', locations=locations, saved_locations=saved_locations)
@app.route('/alerts')
def alerts():
    alerts = read_alerts()
    locations = read_locations()
    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location_id', None)
    filtered_alerts = alerts
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]
    if location_filter:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]
    return render_template('weather_alerts.html',
                           alerts=filtered_alerts,
                           locations=locations,
                           severity_filter=severity_filter,
                           location_filter=location_filter)
@app.route('/acknowledge_alert/<alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    path = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                if parts[0] == alert_id:
                    parts[7] = '1'  # mark acknowledged
                alerts.append(parts)
        with open(path, 'w') as f:
            for parts in alerts:
                f.write('|'.join(parts) + '\n')
    return redirect(url_for('alerts'))
@app.route('/air_quality')
def air_quality():
    air_quality = read_air_quality()
    locations = read_locations()
    location_id = request.args.get('location_id')
    aqi_info = None
    if location_id:
        aqi_info = air_quality.get(location_id)
    return render_template('air_quality.html',
                           air_quality=aqi_info,
                           locations=locations,
                           selected_location=location_id)
@app.route('/saved_locations')
def saved_locations():
    saved_locations = read_saved_locations()
    current_weather = read_current_weather()
    return render_template('saved_locations.html',
                           saved_locations=saved_locations,
                           current_weather=current_weather)
@app.route('/remove_saved_location/<location_id>', methods=['POST'])
def remove_saved_location(location_id):
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                if parts[2] != location_id:
                    saved_locations.append(parts)
        with open(path, 'w') as f:
            for parts in saved_locations:
                f.write('|'.join(parts) + '\n')
    return redirect(url_for('saved_locations'))
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = read_locations()
    # For simplicity, settings stored in memory or could be extended to file
    if request.method == 'POST':
        # Process settings form submission here
        # Placeholder: just redirect back to dashboard
        return redirect(url_for('dashboard'))
    return render_template('settings.html', locations=locations)
if __name__ == '__main__':
    app.run(port=5000, debug=True)