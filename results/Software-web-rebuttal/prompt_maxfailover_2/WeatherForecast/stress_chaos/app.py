from flask import Flask, render_template, request, redirect, url_for
import os
from typing import List, Dict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
data_folder = 'data'

# Helper functions to parse data files

def parse_locations_file() -> List[Dict]:
    locations = []
    try:
        with open(os.path.join(data_folder, 'locations.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                location = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'latitude': float(parts[2]),
                    'longitude': float(parts[3]),
                    'country': parts[4],
                    'timezone': parts[5],
                    'description': parts[6],
                }
                locations.append(location)
    except FileNotFoundError:
        pass
    return locations


def parse_saved_locations_file() -> List[Dict]:
    saved_locations = []
    try:
        with open(os.path.join(data_folder, 'saved_locations.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                saved_locations.append({
                    'saved_id': int(parts[0]),
                    'user_id': int(parts[1]),
                    'location_id': int(parts[2]),
                    'location_name': parts[3],
                    'is_default': parts[4].lower() == 'true'
                })
    except FileNotFoundError:
        pass
    return saved_locations


def parse_current_weather_file() -> List[Dict]:
    current_weathers = []
    try:
        with open(os.path.join(data_folder,'current_weather.txt'),'r') as f:
            for line in f:
                parts=line.strip().split('|')
                if len(parts)<7:
                    continue
                current_weathers.append({
                    'location_id': int(parts[0]),
                    'temperature': float(parts[1]),
                    'condition': parts[2],
                    'humidity': int(parts[3]),
                    'wind_speed': float(parts[4]),
                    'last_updated': parts[5],
                    'temperature_unit': parts[6]
                })
    except FileNotFoundError:
        pass
    return current_weathers


def parse_air_quality_file() -> List[Dict]:
    air_qualities = []
    try:
        with open(os.path.join(data_folder, 'air_quality.txt'), 'r') as f:
            for line in f:
                parts=line.strip().split('|')
                if len(parts)<7:
                    continue
                air_qualities.append({
                    'aqi_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'aqi_index': int(parts[2]),
                    'pm25': float(parts[3]),
                    'pm10': float(parts[4]),
                    'no2': float(parts[5]),
                    'o3': float(parts[6]),
                    'last_updated': parts[7] if len(parts)>7 else ''
                })
    except FileNotFoundError:
        pass
    return air_qualities


def parse_forecasts_file() -> List[Dict]:
    forecasts = []
    try:
        with open(os.path.join(data_folder, 'forecasts.txt'), 'r') as f:
            for line in f:
                parts=line.strip().split('|')
                if len(parts)<8:
                    continue
                forecasts.append({
                    'forecast_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'date': parts[2],
                    'high_temp': float(parts[3]),
                    'low_temp': float(parts[4]),
                    'condition': parts[5],
                    'precipitation': float(parts[6]),
                    'humidity': int(parts[7])
                })
    except FileNotFoundError:
        pass
    return forecasts


def parse_alerts_file() -> List[Dict]:
    alerts = []
    try:
        with open(os.path.join(data_folder, 'alerts.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                alerts.append({
                    'alert_id': int(parts[0]),
                    'location_id': int(parts[1]),
                    'alert_type': parts[2],
                    'severity': parts[3],
                    'description': parts[4],
                    'start_time': parts[5],
                    'end_time': parts[6],
                    'is_acknowledged': parts[7].lower() == 'true'
                })
    except FileNotFoundError:
        pass
    return alerts


# Routes

@app.route('/')
def dashboard():
    locations = parse_locations_file()
    saved_locations = parse_saved_locations_file()
    current_weathers = parse_current_weather_file()
    alerts = parse_alerts_file()

    # Determine default location
    default_location = None
    for sl in saved_locations:
        if sl['is_default']:
            default_location = next((loc for loc in locations if loc['location_id'] == sl['location_id']), None)
            break
    if not default_location and locations:
        default_location = locations[0]

    # Get current weather for default location
    current_weather = None
    if default_location:
        current_weather = next((cw for cw in current_weathers if cw['location_id'] == default_location['location_id']), None)

    context = {
        'locations': locations,
        'saved_locations': saved_locations,
        'default_location': default_location,
        'current_weather': current_weather,
        'alerts': alerts
    }
    return render_template('dashboard.html', **context)


@app.route('/saved_locations')
def saved_locations_page():
    saved_locations = parse_saved_locations_file()
    locations = parse_locations_file()
    for sl in saved_locations:
        location = next((loc for loc in locations if loc['location_id'] == sl['location_id']), None)
        sl['location_name'] = location['location_name'] if location else 'Unknown'

    return render_template('saved_locations.html', saved_locations=saved_locations)


@app.route('/search', methods=['GET', 'POST'])
def search_locations_page():
    locations = parse_locations_file()
    if request.method == 'POST':
        name_query = request.form.get('name', '').lower()
        filtered_locations = [loc for loc in locations if name_query in loc['location_name'].lower()]
        return render_template('search_locations.html', search_results=filtered_locations, name_query=name_query)
    else:
        return render_template('search_locations.html', search_results=[], name_query='')


@app.route('/weather/current/<int:location_id>')
def current_weather_page(location_id):
    current_weathers = parse_current_weather_file()
    locations = parse_locations_file()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        return "Location not found", 404
    current_weather = next((cw for cw in current_weathers if cw['location_id'] == location_id), None)

    context = {
        'location': location,
        'temperature': current_weather['temperature'] if current_weather else None,
        'condition': current_weather['condition'] if current_weather else None,
        'humidity': current_weather['humidity'] if current_weather else None,
        'wind_speed': current_weather['wind_speed'] if current_weather else None,
        'last_updated': current_weather['last_updated'] if current_weather else None
    }
    return render_template('current_weather.html', **context)


@app.route('/weather/forecast/<int:location_id>')
def weekly_forecast_page(location_id):
    forecasts = parse_forecasts_file()
    locations = parse_locations_file()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        return "Location not found", 404
    weekly_forecasts = [f for f in forecasts if f['location_id'] == location_id]

    context = {
        'location': location,
        'forecasts': weekly_forecasts
    }
    return render_template('weekly_forecast.html', **context)


@app.route('/air_quality/<int:location_id>')
def air_quality_page(location_id):
    air_qualities = parse_air_quality_file()
    locations = parse_locations_file()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        return "Location not found", 404
    aqi = next((aq for aq in air_qualities if aq['location_id'] == location_id), None)

    if aqi:
        aqi_index = aqi['aqi_index']
        pollutants = {
            'PM2.5': aqi['pm25'],
            'PM10': aqi['pm10'],
            'NO2': aqi['no2'],
            'O3': aqi['o3']
        }
        last_updated = aqi['last_updated']
        aqi_description = ''
        if aqi_index <= 50:
            aqi_description = 'Good'
        elif aqi_index <= 100:
            aqi_description = 'Moderate'
        elif aqi_index <= 150:
            aqi_description = 'Unhealthy for Sensitive Groups'
        elif aqi_index <= 200:
            aqi_description = 'Unhealthy'
        elif aqi_index <= 300:
            aqi_description = 'Very Unhealthy'
        else:
            aqi_description = 'Hazardous'
        health_recommendation = ''
        if aqi_index > 100:
            health_recommendation = 'Reduce prolonged or heavy exertion'
    else:
        aqi_index = None
        pollutants = None
        last_updated = None
        aqi_description = None
        health_recommendation = None

    context = {
        'location': location,
        'aqi_index': aqi_index,
        'pollutants': pollutants,
        'last_updated': last_updated,
        'aqi_description': aqi_description,
        'health_recommendation': health_recommendation
    }
    return render_template('air_quality.html', **context)


@app.route('/alerts')
def weather_alerts_page():
    alerts = parse_alerts_file()
    locations = parse_locations_file()
    for alert in alerts:
        location = next((loc for loc in locations if loc['location_id'] == alert['location_id']), None)
        alert['location_name'] = location['location_name'] if location else 'Unknown'

    return render_template('alerts.html', alerts=alerts)


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    locations = parse_locations_file()
    saved_locations = parse_saved_locations_file()
    alert_notifications = False
    default_location_id = None

    if request.method == 'POST':
        default_location_id = request.form.get('default_location')
        alert_notifications = request.form.get('alert_notifications') == 'on'
        # Save the settings - for simplicity, just print or save in a file
        # (Not implemented here)
        return redirect(url_for('dashboard'))

    # Determine default location
    default_location = None
    for sl in saved_locations:
        if sl['is_default']:
            default_location = next((loc for loc in locations if loc['location_id'] == sl['location_id']), None)
            break
    if not default_location and locations:
        default_location = locations[0]

    context = {
        'locations': locations,
        'saved_locations': saved_locations,
        'default_location': default_location,
        'alert_notifications': alert_notifications
    }
    return render_template('settings.html', **context)


@app.route('/add_saved_location/<int:location_id>')
def add_saved_location(location_id):
    saved_locations = parse_saved_locations_file()
    locations = parse_locations_file()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        return "Location not found", 404

    # Add saved location with default false
    new_id = max([sl['saved_id'] for sl in saved_locations], default=0) + 1
    saved_locations.append({
        'saved_id': new_id,
        'user_id': 1,
        'location_id': location_id,
        'location_name': location['location_name'],
        'is_default': False
    })

    # Write back saved locations
    try:
        with open(os.path.join(data_folder, 'saved_locations.txt'), 'w') as f:
            for sl in saved_locations:
                line = f"{sl['saved_id']}|{sl['user_id']}|{sl['location_id']}|{sl['location_name']}|{str(sl['is_default'])}\n"
                f.write(line)
    except Exception as e:
        pass

    return redirect(url_for('saved_locations_page'))


@app.route('/remove_saved_location/<int:location_id>')
def remove_saved_location(location_id):
    saved_locations = parse_saved_locations_file()
    saved_locations = [sl for sl in saved_locations if sl['location_id'] != location_id]
    try:
        with open(os.path.join(data_folder, 'saved_locations.txt'), 'w') as f:
            for sl in saved_locations:
                line = f"{sl['saved_id']}|{sl['user_id']}|{sl['location_id']}|{sl['location_name']}|{str(sl['is_default'])}\n"
                f.write(line)
    except Exception as e:
        pass

    return redirect(url_for('saved_locations_page'))


@app.route('/acknowledge_alert/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = parse_alerts_file()
    updated = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            updated = True
            break
    if updated:
        try:
            with open(os.path.join(data_folder, 'alerts.txt'), 'w') as f:
                for alert in alerts:
                    line = f"{alert['alert_id']}|{alert['location_id']}|{alert['alert_type']}|{alert['severity']}|{alert['description']}|{alert['start_time']}|{alert['end_time']}|{str(alert['is_acknowledged'])}\n"
                    f.write(line)
        except Exception as e:
            pass
    return redirect(url_for('weather_alerts_page'))


if __name__ == '__main__':
    app.run(debug=True)
