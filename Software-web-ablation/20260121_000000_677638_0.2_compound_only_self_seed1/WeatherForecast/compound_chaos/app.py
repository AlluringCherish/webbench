from flask import Flask, render_template, redirect, url_for, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
DATA_DIR = 'data'


def parse_pipe_delimited_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        return []
    with open(path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return [line.split('|') for line in lines]


def load_current_weather():
    # Fields:
    # location_id|location_name|temperature|condition|humidity|wind_speed|last_updated
    data = parse_pipe_delimited_file('current_weather.txt')
    result = []
    for row in data:
        if len(row) != 7:
            continue
        try:
            result.append({
                'location_id': int(row[0]),
                'location_name': row[1],
                'temperature': float(row[2]),
                'condition': row[3],
                'humidity': int(row[4]),
                'wind_speed': float(row[5]),
                'last_updated': row[6]
            })
        except Exception:
            continue
    return result


def load_forecasts():
    # Fields:
    # forecast_id|location_id|date|high_temp|low_temp|condition|precipitation|humidity
    data = parse_pipe_delimited_file('forecasts.txt')
    result = []
    for row in data:
        if len(row) != 8:
            continue
        try:
            result.append({
                'forecast_id': int(row[0]),
                'location_id': int(row[1]),
                'date': row[2],
                'high_temp': float(row[3]),
                'low_temp': float(row[4]),
                'condition': row[5],
                'precipitation': int(row[6]),
                'humidity': int(row[7]),
            })
        except Exception:
            continue
    return result


def load_locations():
    # Fields:
    # location_id|location_name|latitude|longitude|country|timezone
    data = parse_pipe_delimited_file('locations.txt')
    result = []
    for row in data:
        if len(row) != 6:
            continue
        try:
            result.append({
                'location_id': int(row[0]),
                'location_name': row[1],
                'latitude': float(row[2]),
                'longitude': float(row[3]),
                'country': row[4],
                'timezone': row[5]
            })
        except Exception:
            continue
    return result


def load_alerts():
    # Fields:
    # alert_id|location_id|alert_type|severity|description|start_time|end_time|is_acknowledged
    data = parse_pipe_delimited_file('alerts.txt')
    result = []
    for row in data:
        if len(row) != 8:
            continue
        try:
            result.append({
                'alert_id': int(row[0]),
                'location_id': int(row[1]),
                'alert_type': row[2],
                'severity': row[3],
                'description': row[4],
                'start_time': row[5],
                'end_time': row[6],
                'is_acknowledged': bool(int(row[7]))
            })
        except Exception:
            continue
    return result


def load_air_quality():
    # Fields:
    # aqi_id|location_id|aqi_index|pm25|pm10|no2|o3|last_updated
    data = parse_pipe_delimited_file('air_quality.txt')
    result = []
    for row in data:
        if len(row) != 8:
            continue
        try:
            result.append({
                'aqi_id': int(row[0]),
                'location_id': int(row[1]),
                'aqi_index': int(row[2]),
                'pm25': float(row[3]),
                'pm10': float(row[4]),
                'no2': float(row[5]),
                'o3': float(row[6]),
                'last_updated': row[7]
            })
        except Exception:
            continue
    return result


def load_saved_locations():
    # Fields:
    # saved_id|user_id|location_id|location_name|is_default
    data = parse_pipe_delimited_file('saved_locations.txt')
    result = []
    for row in data:
        if len(row) != 5:
            continue
        try:
            result.append({
                'saved_id': int(row[0]),
                'user_id': int(row[1]),
                'location_id': int(row[2]),
                'location_name': row[3],
                'is_default': bool(int(row[4]))
            })
        except Exception:
            continue
    return result


@app.route('/')
def root_redirect():
    # Route 1: Root redirects GET to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Route 2: Dashboard page, GET, renders dashboard.html
    current_weather = load_current_weather()
    return render_template('dashboard.html', current_weather=current_weather[0] if current_weather else None)


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    # Route 3: Current weather page, GET
    current_weather = load_current_weather()
    weather = next((cw for cw in current_weather if cw['location_id'] == location_id), None)
    if not weather:
        return "Current weather data for location not found", 404
    # Provide only required context variables
    context = {
        'location_name': weather['location_name'],
        'temperature': weather['temperature'],
        'condition': weather['condition'],
        'humidity': weather['humidity'],
        'wind_speed': weather['wind_speed']
    }
    return render_template('current_weather.html', **context)


@app.route('/forecast/weekly')
def weekly_forecast():
    # Route 4: Weekly forecast page, GET
    forecasts = load_forecasts()
    locations = load_locations()
    selected_location_id = request.args.get('location_id', type=int)
    if selected_location_id is not None:
        forecasts = [f for f in forecasts if f['location_id'] == selected_location_id]
    return render_template('weekly_forecast.html',
                           forecasts=forecasts,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id)


@app.route('/locations/search', methods=['GET', 'POST'])
def location_search():
    # Route 5: Location search page, GET and POST
    saved_locs_raw = load_saved_locations()
    saved_locations = [{'location_id': sl['location_id'], 'location_name': sl['location_name']} for sl in saved_locs_raw]
    search_query = ''
    search_results = []
    selected_location_id = None
    if request.method == 'POST':
        # Distinguish between search and select
        if 'select_location_id' in request.form:
            try:
                location_id = int(request.form.get('select_location_id'))
                return redirect(url_for('current_weather', location_id=location_id))
            except (ValueError, TypeError):
                pass
        else:
            search_query = request.form.get('search_query', '').strip()
            if search_query:
                all_locations = load_locations()
                q = search_query.lower()
                search_results = [loc for loc in all_locations if q in loc['location_name'].lower()]
    return render_template('location_search.html',
                           search_query=search_query,
                           search_results=search_results,
                           saved_locations=saved_locations,
                           selected_location_id=selected_location_id)


@app.route('/alerts')
def weather_alerts():
    # Route 6: Weather alerts page, GET
    alerts = load_alerts()
    locations = load_locations()
    severity_filter = request.args.get('severity_filter', 'All')
    location_filter = request.args.get('location_id', type=int)
    filtered_alerts = alerts
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]
    if location_filter is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]
    return render_template('alerts.html',
                           alerts=filtered_alerts,
                           severity_filter=severity_filter,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           location_filter=location_filter)


@app.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    # Route 7: Acknowledge alert, POST
    path = os.path.join(DATA_DIR, 'alerts.txt')
    if not os.path.exists(path):
        return jsonify({'success': False, 'error': 'alerts data file missing'}), 404
    updated = False
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            parts = line.strip().split('|')
            if len(parts) != 8:
                new_lines.append(line)
                continue
            try:
                curr_id = int(parts[0])
            except:
                new_lines.append(line)
                continue
            if curr_id == alert_id:
                parts[7] = '1'  # set is_acknowledged to 1
                new_lines.append('|'.join(parts) + '\n')
                updated = True
            else:
                new_lines.append(line)
        if updated:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Alert not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/airquality')
def air_quality_page():
    # Route 8: Air quality page, GET
    air_quality_data = load_air_quality()
    locations = load_locations()
    selected_location_id = request.args.get('location_id', type=int)
    if selected_location_id is not None:
        air_quality_data = [aq for aq in air_quality_data if aq['location_id'] == selected_location_id]
    # health_recommendation: based on first AQI value if present
    health_recommendation = ""
    if air_quality_data:
        aqi = air_quality_data[0]['aqi_index']
        if aqi <= 50:
            health_recommendation = "Air quality is good. It's safe to go outside."
        elif aqi <= 100:
            health_recommendation = "Air quality is moderate; sensitive groups should be cautious."
        elif aqi <= 150:
            health_recommendation = "Unhealthy for sensitive groups."
        elif aqi <= 200:
            health_recommendation = "Unhealthy. Everyone may experience health effects."
        elif aqi <= 300:
            health_recommendation = "Very unhealthy. Health warnings of emergency conditions."
        else:
            health_recommendation = "Hazardous. Everyone should avoid outdoor exertion."
    return render_template('air_quality.html',
                           air_quality_data=air_quality_data,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations],
                           selected_location_id=selected_location_id,
                           health_recommendation=health_recommendation)


@app.route('/locations/saved')
def saved_locations():
    # Route 9: Saved locations page, GET
    saved = load_saved_locations()
    current_weather = load_current_weather()
    current_weather_map = {cw['location_id']: {'temperature': cw['temperature'], 'condition': cw['condition']} for cw in current_weather}
    return render_template('saved_locations.html',
                           saved_locations=saved,
                           current_weather_map=current_weather_map)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Route 10: Settings page GET, POST
    locations = load_locations()

    # Default values - in production, usually saved persistently
    temperature_unit = 'Celsius'
    default_location_id = None
    alert_notifications_enabled = True

    if request.method == 'POST':
        temperature_unit = request.form.get('temperature_unit', temperature_unit)
        try:
            default_location_id = int(request.form.get('default_location_id'))
        except (TypeError, ValueError):
            default_location_id = None
        alert_notifications_enabled = (request.form.get('alert_notifications_enabled') == 'true')
        # Here you would save settings persistently
        return redirect(url_for('dashboard'))

    return render_template('settings.html',
                           temperature_unit=temperature_unit,
                           default_location_id=default_location_id,
                           alert_notifications_enabled=alert_notifications_enabled,
                           locations=[{'location_id': loc['location_id'], 'location_name': loc['location_name']} for loc in locations])


if __name__ == '__main__':
    app.run(debug=True, port=5000)
