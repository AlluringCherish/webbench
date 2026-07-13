from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Helper functions for data loading and saving

def load_current_weather():
    filepath = os.path.join(DATA_DIR, 'current_weather.txt')
    weather_data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    location_id = int(fields[0])
                    weather_data[location_id] = {
                        'location_id': location_id,
                        'location_name': fields[1],
                        'temperature': fields[2],
                        'condition': fields[3],
                        'humidity': fields[4],
                        'wind_speed': fields[5],
                        'last_updated': fields[6]
                    }
    return weather_data


def load_forecasts():
    filepath = os.path.join(DATA_DIR, 'forecasts.txt')
    forecasts = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 8:
                    forecast = {
                        'forecast_id': int(fields[0]),
                        'location_id': int(fields[1]),
                        'date': fields[2],
                        'high_temp': fields[3],
                        'low_temp': fields[4],
                        'condition': fields[5],
                        'precipitation': fields[6],
                        'humidity': fields[7]
                    }
                    forecasts.append(forecast)
    return forecasts


def load_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 6:
                    location_id = int(fields[0])
                    locations[location_id] = {
                        'location_id': location_id,
                        'location_name': fields[1],
                        'latitude': fields[2],
                        'longitude': fields[3],
                        'country': fields[4],
                        'timezone': fields[5]
                    }
    return locations


def load_alerts():
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    alerts = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 8:
                    alert = {
                        'alert_id': int(fields[0]),
                        'location_id': int(fields[1]),
                        'alert_type': fields[2],
                        'severity': fields[3],
                        'description': fields[4],
                        'start_time': fields[5],
                        'end_time': fields[6],
                        'is_acknowledged': fields[7] == '1'
                    }
                    alerts.append(alert)
    return alerts


def save_alerts(alerts):
    filepath = os.path.join(DATA_DIR, 'alerts.txt')
    with open(filepath, 'w') as file:
        for alert in alerts:
            line = '|'.join([
                str(alert['alert_id']),
                str(alert['location_id']),
                alert['alert_type'],
                alert['severity'],
                alert['description'],
                alert['start_time'],
                alert['end_time'],
                '1' if alert['is_acknowledged'] else '0'
            ])
            file.write(line + '\n')


def load_air_quality():
    filepath = os.path.join(DATA_DIR, 'air_quality.txt')
    air_quality_data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 8:
                    location_id = int(fields[1])
                    air_quality_data[location_id] = {
                        'aqi_id': int(fields[0]),
                        'location_id': location_id,
                        'aqi_index': int(fields[2]),
                        'pm25': fields[3],
                        'pm10': fields[4],
                        'no2': fields[5],
                        'o3': fields[6],
                        'last_updated': fields[7]
                    }
    return air_quality_data


def load_saved_locations():
    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    saved_locations = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 5:
                    saved = {
                        'saved_id': int(fields[0]),
                        'user_id': int(fields[1]),
                        'location_id': int(fields[2]),
                        'location_name': fields[3],
                        'is_default': fields[4] == '1'
                    }
                    saved_locations.append(saved)
    return saved_locations

# For simplicity, assume user_id=1 for saved locations and settings management
USER_ID = 1

# Settings will be stored temporarily in a settings file to simulate persistence
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.txt')

# Load settings or create defaults

def load_settings():
    settings = {
        'temperature_unit': 'Celsius',
        'default_location': None,
        'alert_notifications': True
    }
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                if '=' in line:
                    key, value = line.split('=',1)
                    if key == 'temperature_unit':
                        settings['temperature_unit'] = value
                    elif key == 'default_location':
                        try:
                            settings['default_location'] = int(value)
                        except:
                            settings['default_location'] = None
                    elif key == 'alert_notifications':
                        settings['alert_notifications'] = (value.lower() == 'true')
    return settings

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        file.write(f"temperature_unit={settings['temperature_unit']}\n")
        file.write(f"default_location={settings['default_location'] if settings['default_location'] is not None else ''}\n")
        file.write(f"alert_notifications={settings['alert_notifications']}\n")


@app.route('/')
@app.route('/dashboard')
def dashboard():
    settings = load_settings()
    weather_data = load_current_weather()
    locations = load_locations()

    # Determine default location
    default_location_id = settings['default_location']
    if default_location_id is None or default_location_id not in weather_data:
        # fallback to first location in weather data
        if weather_data:
            default_location_id = next(iter(weather_data.keys()))
        else:
            default_location_id = None

    current_weather = weather_data.get(default_location_id)

    return render_template('dashboard.html',
                           settings=settings,
                           current_weather=current_weather)


@app.route('/current-weather/<int:location_id>')
def current_weather(location_id):
    weather_data = load_current_weather()
    locations = load_locations()
    weather = weather_data.get(location_id)
    location = locations.get(location_id)
    if not weather or not location:
        return "Location or weather data not found.", 404

    return render_template('current_weather.html',
                           weather=weather,
                           location=location)


@app.route('/forecast')
def forecast():
    forecasts = load_forecasts()
    locations = load_locations()

    # Filter by location if location_id provided via query string
    location_filter = request.args.get('location', type=int)

    filtered_forecasts = forecasts
    if location_filter is not None:
        filtered_forecasts = [f for f in forecasts if f['location_id'] == location_filter]

    # Group forecasts by date for table display
    # Also prepare location list for filter dropdown
    location_list = list(locations.values())

    return render_template('forecast.html',
                           forecasts=filtered_forecasts,
                           locations=location_list,
                           selected_location=location_filter)


@app.route('/search', methods=['GET', 'POST'])
def search():
    locations = load_locations()
    saved_locations = load_saved_locations()

    search_results = []
    search_query = ''
    message = ''

    if request.method == 'POST':
        # Handling search submit or saving a location
        if 'search_query' in request.form:
            search_query = request.form['search_query'].strip().lower()
            if search_query:
                for loc in locations.values():
                    if search_query in loc['location_name'].lower() or search_query in f"{loc['latitude']},{loc['longitude']}".lower():
                        search_results.append(loc)
            else:
                message = "Please enter a search query."
        elif 'select_location_id' in request.form:
            try:
                selected_location_id = int(request.form['select_location_id'])
                selected_loc = locations.get(selected_location_id)
                if selected_loc:
                    # Save selected location for USER_ID
                    saved_locs = load_saved_locations()
                    existing = next((s for s in saved_locs if s['user_id'] == USER_ID and s['location_id'] == selected_location_id), None)
                    if not existing:
                        new_id = max((s['saved_id'] for s in saved_locs), default=0) + 1
                        # is_default set to 0
                        saved_locs.append({
                            'saved_id': new_id,
                            'user_id': USER_ID,
                            'location_id': selected_loc['location_id'],
                            'location_name': selected_loc['location_name'],
                            'is_default': False
                        })
                        # Save back
                        filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
                        with open(filepath, 'w') as file:
                            for sl in saved_locs:
                                line = '|'.join([str(sl['saved_id']), str(sl['user_id']), str(sl['location_id']), sl['location_name'], '1' if sl['is_default'] else '0'])
                                file.write(line + '\n')
                        message = f"Location {selected_loc['location_name']} saved successfully."
                    else:
                        message = f"Location {existing['location_name']} is already saved."
                else:
                    message = "Selected location not found."
            except Exception:
                message = "Invalid selection."

    # Reload saved locations to reflect changes
    saved_locations = load_saved_locations()

    return render_template('search.html',
                           locations=locations.values(),
                           saved_locations=[s for s in saved_locations if s['user_id'] == USER_ID],
                           search_results=search_results,
                           search_query=search_query,
                           message=message)


@app.route('/alerts')
def alerts():
    alerts = load_alerts()
    locations = load_locations()

    severity_filter = request.args.get('severity', 'All')
    location_filter = request.args.get('location', type=int)

    filtered_alerts = alerts
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]
    if location_filter is not None:
        filtered_alerts = [a for a in filtered_alerts if a['location_id'] == location_filter]

    # Keep only active alerts (based on current datetime within start_time and end_time)
    now = datetime.now()
    active_alerts = []
    for alert in filtered_alerts:
        start = datetime.strptime(alert['start_time'], '%Y-%m-%d %H:%M')
        end = datetime.strptime(alert['end_time'], '%Y-%m-%d %H:%M')
        if start <= now <= end and not alert['is_acknowledged']:
            active_alerts.append(alert)

    location_list = list(locations.values())

    return render_template('alerts.html',
                           alerts=active_alerts,
                           locations=location_list,
                           selected_severity=severity_filter,
                           selected_location=location_filter)


@app.route('/alerts/acknowledge/<int:alert_id>', methods=['POST'])
def acknowledge_alert(alert_id):
    alerts = load_alerts()
    changed = False
    for alert in alerts:
        if alert['alert_id'] == alert_id:
            alert['is_acknowledged'] = True
            changed = True
            break
    if changed:
        save_alerts(alerts)
    return redirect(url_for('alerts'))


@app.route('/air-quality')
def air_quality():
    locations = load_locations()
    air_quality_data = load_air_quality()

    location_filter = request.args.get('location', type=int)

    selected_aqi = None
    if location_filter is not None and location_filter in air_quality_data:
        selected_aqi = air_quality_data[location_filter]
    elif air_quality_data:
        # fallback to first
        selected_aqi = next(iter(air_quality_data.values()))

    def aqi_description(aqi_index):
        if 0 <= aqi_index <= 50:
            return "Good"
        elif 51 <= aqi_index <= 100:
            return "Moderate"
        elif 101 <= aqi_index <= 150:
            return "Unhealthy for Sensitive Groups"
        elif 151 <= aqi_index <= 200:
            return "Unhealthy"
        elif 201 <= aqi_index <= 300:
            return "Very Unhealthy"
        elif 301 <= aqi_index <= 500:
            return "Hazardous"
        else:
            return "Unknown"

    def health_recommendation(desc):
        recommendations = {
            "Good": "Air quality is satisfactory, and air pollution poses little or no risk.",
            "Moderate": "Air quality is acceptable; some pollutants may be a moderate health concern.",
            "Unhealthy for Sensitive Groups": "Members of sensitive groups may experience health effects.",
            "Unhealthy": "Everyone may begin to experience health effects.",
            "Very Unhealthy": "Health alert: everyone may experience more serious health effects.",
            "Hazardous": "Health warnings of emergency conditions."
        }
        return recommendations.get(desc, "No recommendation available.")

    aqi_desc = aqi_description(int(selected_aqi['aqi_index'])) if selected_aqi else None
    health_rec = health_recommendation(aqi_desc) if aqi_desc else None

    return render_template('air_quality.html',
                           air_quality=selected_aqi,
                           aqi_description=aqi_desc,
                           health_recommendation=health_rec,
                           locations=locations.values(),
                           selected_location=location_filter)


@app.route('/saved-locations')
def saved_locations():
    saved_locations_list = load_saved_locations()
    locations = load_locations()
    weather_data = load_current_weather()

    user_saved = [s for s in saved_locations_list if s['user_id'] == USER_ID]

    # Compose list with current weather details
    locations_with_weather = []
    for s in user_saved:
        location = locations.get(s['location_id'])
        weather = weather_data.get(s['location_id'])
        if location and weather:
            item = {
                'location_id': s['location_id'],
                'location_name': s['location_name'],
                'temperature': weather['temperature'],
                'condition': weather['condition']
            }
            locations_with_weather.append(item)

    return render_template('saved_locations.html',
                           saved_locations=locations_with_weather)


@app.route('/saved-locations/view/<int:location_id>')
def view_saved_location_weather(location_id):
    # Redirect to current weather page for the location
    return redirect(url_for('current_weather', location_id=location_id))


@app.route('/saved-locations/remove/<int:location_id>', methods=['POST'])
def remove_saved_location(location_id):
    saved_locations_list = load_saved_locations()
    saved_locations_list = [s for s in saved_locations_list if not (s['user_id'] == USER_ID and s['location_id'] == location_id)]
    # Reassign saved_id sequentially
    for i, s in enumerate(saved_locations_list, start=1):
        s['saved_id'] = i

    filepath = os.path.join(DATA_DIR, 'saved_locations.txt')
    with open(filepath, 'w') as file:
        for sl in saved_locations_list:
            line = '|'.join([str(sl['saved_id']), str(sl['user_id']), str(sl['location_id']), sl['location_name'], '1' if sl['is_default'] else '0'])
            file.write(line + '\n')

    return redirect(url_for('saved_locations'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    locations = load_locations()
    settings = load_settings()
    message = ''

    if request.method == 'POST':
        # get form data
        temperature_unit = request.form.get('temperature_unit', 'Celsius')
        default_location = request.form.get('default_location')
        alert_notifications = request.form.get('alert_notifications') == 'on'

        # Validate default_location
        try:
            default_location_id = int(default_location) if default_location else None
            if default_location_id is not None and default_location_id not in locations:
                default_location_id = None
        except:
            default_location_id = None

        settings['temperature_unit'] = temperature_unit
        settings['default_location'] = default_location_id
        settings['alert_notifications'] = alert_notifications

        save_settings(settings)

        message = 'Settings saved successfully.'

    return render_template('settings.html',
                           locations=locations.values(),
                           settings=settings,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)
