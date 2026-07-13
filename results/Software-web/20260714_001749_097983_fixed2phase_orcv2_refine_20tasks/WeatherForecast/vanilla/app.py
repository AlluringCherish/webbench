from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

def read_current_weather():
    path = os.path.join(DATA_DIR, 'current_weather.txt')
    weather_data = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    path = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    locations[parts[0]] = {
                        'location_id': parts[0],
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
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    alerts.append({
                        'alert_id': parts[0],
                        'location_id': parts[1],
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7]=='1'
                    })
    return alerts

def read_air_quality():
    path = os.path.join(DATA_DIR, 'air_quality.txt')
    air_quality = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    location_id = parts[1]
                    air_quality[location_id] = {
                        'aqi_id': parts[0],
                        'location_id': location_id,
                        'aqi_index': int(parts[2]),
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
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    saved.append({
                        'saved_id': parts[0],
                        'location_id': parts[1],
                        'location_name': parts[2],
                        'is_default': parts[3]=='1'
                    })
    return saved

def write_saved_locations(saved_locations):
    path = os.path.join(DATA_DIR, 'saved_locations.txt')
    with open(path, 'w') as file:
        for sl in saved_locations:
            line = f"{sl['saved_id']}|{sl['location_id']}|{sl['location_name']}|{'1' if sl['is_default'] else '0'}\n"
            file.write(line)

@app.route('/')
def dashboard():
    saved_locations = read_saved_locations()
    current_weather = read_current_weather()
    default_location = None
    for loc in saved_locations:
        if loc['is_default']:
            default_location = loc['location_id']
            break
    # If no default, pick first saved if available
    if not default_location and saved_locations:
        default_location = saved_locations[0]['location_id']
    weather_summary = None
    if default_location and default_location in current_weather:
        weather_summary = current_weather[default_location]
    return render_template('dashboard.html', weather_summary=weather_summary)

@app.route('/current_weather/<location_id>')
def current_weather(location_id):
    current_weather = read_current_weather()
    weather = current_weather.get(location_id)
    if not weather:
        return "Location weather not found", 404
    return render_template('current_weather.html', weather=weather)

@app.route('/weekly_forecast', methods=['GET', 'POST'])
def weekly_forecast():
    locations = read_locations()
    forecasts = read_forecasts()
    location_id = request.args.get('location_id') or request.form.get('location_filter')
    if not location_id and locations:
        location_id = next(iter(locations))
    filtered_forecasts = [f for f in forecasts if f['location_id'] == location_id]
    return render_template('weekly_forecast.html', forecasts=filtered_forecasts, locations=locations, selected_location=location_id)

@app.route('/search_locations', methods=['GET', 'POST'])
def search_locations():
    query = request.form.get('location_search_input', '').strip().lower() if request.method == 'POST' else ''
    locations = read_locations()
    saved_locations = read_saved_locations()
    matched_locations = []
    if query:
        for loc_id, loc in locations.items():
            if query in loc['location_name'].lower() or query in f"{loc['latitude']},{loc['longitude']}".lower():
                matched_locations.append(loc)
    else:
        matched_locations = list(locations.values())
    return render_template('search_locations.html', matched_locations=matched_locations, saved_locations=saved_locations, query=query)

@app.route('/select_location/<location_id>')
def select_location(location_id):
    locations = read_locations()
    location = locations.get(location_id)
    if not location:
        return "Location not found", 404
    saved_locations = read_saved_locations()
    # Check if already saved
    if any(sl['location_id'] == location_id for sl in saved_locations):
        # Redirect to current weather
        return redirect(url_for('current_weather', location_id=location_id))
    new_id = str(max([int(sl['saved_id']) for sl in saved_locations], default=0) + 1) if saved_locations else '1'
    saved_locations.append({'saved_id': new_id, 'location_id': location_id, 'location_name': location['location_name'], 'is_default': False})
    write_saved_locations(saved_locations)
    return redirect(url_for('current_weather', location_id=location_id))

@app.route('/weather_alerts', methods=['GET', 'POST'])
def weather_alerts():
    alerts = read_alerts()
    locations = read_locations()
    severity_filter = request.args.get('severity_filter') or request.form.get('severity_filter')
    location_filter = request.args.get('location_filter_alerts') or request.form.get('location_filter_alerts')

    filtered_alerts = alerts
    if severity_filter:
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]
    if location_filter:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]

    location_map = {loc_id: loc['location_name'] for loc_id, loc in locations.items()}
    for alert in filtered_alerts:
        alert['location_name'] = location_map.get(alert['location_id'], 'Unknown')

    return render_template('weather_alerts.html', alerts=filtered_alerts, locations=locations, selected_severity=severity_filter, selected_location=location_filter)

@app.route('/acknowledge_alert/<alert_id>')
def acknowledge_alert(alert_id):
    alerts = read_alerts()
    updated_alerts = []
    found = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            found = True
        updated_alerts.append(alert)
    if found:
        path = os.path.join(DATA_DIR, 'alerts.txt')
        with open(path, 'w') as file:
            for alert in updated_alerts:
                line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{'1' if alert['is_acknowledged'] else '0'}\n"
                file.write(line)
    return redirect(url_for('weather_alerts'))

@app.route('/air_quality', methods=['GET', 'POST'])
def air_quality():
    locations = read_locations()
    air_quality_data = read_air_quality()
    location_id = request.args.get('location_aqi_filter') or request.form.get('location_aqi_filter')
    if not location_id and locations:
        location_id = next(iter(locations))
    data = air_quality_data.get(location_id)

    aqi_desc = ''
    health_recommendation = ''

    if data:
        aqi = data['aqi_index']
        if aqi <= 50:
            aqi_desc = 'Good'
            health_recommendation = 'Air quality is considered satisfactory, and air pollution poses little or no risk.'
        elif aqi <= 100:
            aqi_desc = 'Moderate'
            health_recommendation = 'Air quality is acceptable; however, some pollutants may be a moderate health concern for a very small number of people.'
        elif aqi <= 150:
            aqi_desc = 'Unhealthy for Sensitive Groups'
            health_recommendation = 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        elif aqi <= 200:
            aqi_desc = 'Unhealthy'
            health_recommendation = 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.'
        elif aqi <= 300:
            aqi_desc = 'Very Unhealthy'
            health_recommendation = 'Health alert: everyone may experience more serious health effects.'
        else:
            aqi_desc = 'Hazardous'
            health_recommendation = 'Health warnings of emergency conditions. The entire population is more likely to be affected.'

    return render_template('air_quality.html', data=data, locations=locations, selected_location=location_id, aqi_description=aqi_desc, health_recommendation=health_recommendation)

@app.route('/saved_locations', methods=['GET', 'POST'])
def saved_locations():
    saved_locations = read_saved_locations()
    current_weather = read_current_weather()
    locations_info = []
    for sl in saved_locations:
        weather = current_weather.get(sl['location_id'])
        locations_info.append({
            'saved_id': sl['saved_id'],
            'location_id': sl['location_id'],
            'location_name': sl['location_name'],
            'is_default': sl['is_default'],
            'temperature': weather['temperature'] if weather else 'N/A',
            'condition': weather['condition'] if weather else 'N/A'
        })

    if request.method == 'POST':
        # Remove location
        remove_id = request.form.get('remove_location_id')
        if remove_id:
            saved_locations = [sl for sl in saved_locations if sl['saved_id'] != remove_id]
            write_saved_locations(saved_locations)
            return redirect(url_for('saved_locations'))

    return render_template('saved_locations.html', locations_info=locations_info)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    saved_locations = read_saved_locations()
    locations = read_locations()

    # Default settings
    temperature_unit = 'Celsius'
    default_location_id = None
    alert_notifications_enabled = True

    # Handle POST to save settings
    if request.method == 'POST':
        temperature_unit = request.form.get('temperature_unit_select', 'Celsius')
        default_location_id = request.form.get('default_location_select')
        alert_notifications_enabled = request.form.get('alert_notifications_toggle') == 'on'

        # Update saved locations to set default
        if default_location_id is not None:
            for sl in saved_locations:
                sl['is_default'] = (sl['location_id'] == default_location_id)
            write_saved_locations(saved_locations)

    # Pick current default location
    for sl in saved_locations:
        if sl['is_default']:
            default_location_id = sl['location_id']
            break

    return render_template('settings.html', temperature_unit=temperature_unit, saved_locations=saved_locations, locations=locations, default_location_id=default_location_id, alert_notifications_enabled=alert_notifications_enabled)


if __name__ == '__main__':
    app.run(debug=True)
