from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data loading functions

def load_current_weather():
    weather = []
    try:
        with open('data/current_weather.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                location_id = int(parts[0])
                location_name = parts[1]
                temperature = float(parts[2]) if '.' in parts[2] else int(parts[2])
                condition = parts[3]
                humidity = int(parts[4])
                wind_speed = float(parts[5]) if '.' in parts[5] else int(parts[5])
                last_updated = parts[6]

                weather.append({
                    'location_id': location_id,
                    'location_name': location_name,
                    'temperature': temperature,
                    'condition': condition,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'last_updated': last_updated
                })
    except FileNotFoundError:
        pass
    return weather


def load_forecasts():
    forecasts = []
    try:
        with open('data/forecasts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                forecast_id = int(parts[0])
                location_id = int(parts[1])
                date = parts[2]
                high_temp = float(parts[3]) if '.' in parts[3] else int(parts[3])
                low_temp = float(parts[4]) if '.' in parts[4] else int(parts[4])
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
    except FileNotFoundError:
        pass
    return forecasts


def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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
    except FileNotFoundError:
        pass
    return locations


def load_alerts():
    alerts = []
    try:
        with open('data/alerts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                alert_id = int(parts[0])
                location_id = int(parts[1])
                alert_type = parts[2]
                severity = parts[3]
                description = parts[4]
                start_time = parts[5]
                end_time = parts[6]
                is_acknowledged = parts[7] == '1'

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
    except FileNotFoundError:
        pass
    return alerts


def load_air_quality():
    air_quality = []
    try:
        with open('data/air_quality.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                aqi_id = int(parts[0])
                location_id = int(parts[1])
                aqi_index = int(parts[2])
                pm25 = float(parts[3])
                pm10 = float(parts[4])
                no2 = float(parts[5])
                o3 = float(parts[6])
                last_updated = parts[7]

                air_quality.append({
                    'aqi_id': aqi_id,
                    'location_id': location_id,
                    'aqi_index': aqi_index,
                    'pm25': pm25,
                    'pm10': pm10,
                    'no2': no2,
                    'o3': o3,
                    'last_updated': last_updated
                })
    except FileNotFoundError:
        pass
    return air_quality


def load_saved_locations():
    saved_locations = []
    try:
        with open('data/saved_locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                saved_id = int(parts[0])
                user_id = int(parts[1])
                location_id = int(parts[2])
                location_name = parts[3]
                is_default = parts[4] == '1'

                saved_locations.append({
                    'saved_id': saved_id,
                    'user_id': user_id,
                    'location_id': location_id,
                    'location_name': location_name,
                    'is_default': is_default
                })
    except FileNotFoundError:
        pass
    return saved_locations


def get_default_location_id(saved_locations):
    for saved in saved_locations:
        if saved.get('is_default'):
            return saved['location_id']
    return None


def get_weather_for_location(location_id, weather_list):
    for weather in weather_list:
        if weather['location_id'] == location_id:
            return weather
    return None


def get_forecast_for_location(location_id, forecasts_list):
    return [f for f in forecasts_list if f['location_id'] == location_id]


def get_alerts_for_location(location_id, alerts_list):
    return [a for a in alerts_list if a['location_id'] == location_id]


def get_air_quality_for_location(location_id, air_quality_list):
    for aq in air_quality_list:
        if aq['location_id'] == location_id:
            return aq
    return None


def get_location_name_by_id(location_id, locations_list):
    for loc in locations_list:
        if loc['location_id'] == location_id:
            return loc['location_name']
    return ""


def aqi_desc_and_health_recommendation(aqi_index):
    if aqi_index is None:
        return ("Unknown", "No health information available")
    
    if 0 <= aqi_index <= 50:
        return ("Good", "Air quality is considered satisfactory, and air pollution poses little or no risk.")
    elif 51 <= aqi_index <= 100:
        return ("Moderate", "Air quality is acceptable; however, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.")
    elif 101 <= aqi_index <= 150:
        return ("Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects. The general public is less likely to be affected.")
    elif 151 <= aqi_index <= 200:
        return ("Unhealthy", "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.")
    elif 201 <= aqi_index <= 300:
        return ("Very Unhealthy", "Health alert: The risk of health effects is increased for everyone.")
    elif 301 <= aqi_index <= 500:
        return ("Hazardous", "Health warnings of emergency conditions. The entire population is more likely to be affected.")
    else:
        return ("Unknown", "No health information available")


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    saved_locations = load_saved_locations()
    default_location_id = get_default_location_id(saved_locations)

    current_weather_all = load_current_weather()
    current_weather = get_weather_for_location(default_location_id, current_weather_all) if default_location_id else {}

    alerts_all = load_alerts()
    alerts = [a for a in alerts_all if a['location_id'] == default_location_id] if default_location_id else []

    forecasts_all = load_forecasts()
    forecast_list = [f for f in forecasts_all if f['location_id'] == default_location_id] if default_location_id else []

    air_quality_all = load_air_quality()
    air_quality = get_air_quality_for_location(default_location_id, air_quality_all) if default_location_id else {}

    alerts_enabled = True

    return render_template(
        'dashboard.html',
        saved_locations=saved_locations,
        default_location_id=default_location_id if default_location_id is not None else 0,
        current_weather=current_weather if current_weather else {},
        alerts=alerts,
        forecast_list=forecast_list,
        air_quality=air_quality if air_quality else {},
        alerts_enabled=alerts_enabled
    )


@app.route('/weather/current/<int:location_id>')
def current_weather(location_id):
    current_weather_all = load_current_weather()
    cw = get_weather_for_location(location_id, current_weather_all)

    if cw:
        location_name = cw['location_name']
        current_weather_data = {
            'temperature': cw['temperature'],
            'condition': cw['condition'],
            'humidity': cw['humidity'],
            'wind_speed': cw['wind_speed'],
            'last_updated': cw['last_updated']
        }
    else:
        locations = load_locations()
        location_name = get_location_name_by_id(location_id, locations)
        current_weather_data = {}

    return render_template('current_weather.html', location_name=location_name, current_weather=current_weather_data)


@app.route('/weather/forecast/<int:location_id>')
def weekly_forecast(location_id):
    forecasts_all = load_forecasts()
    forecast_list = get_forecast_for_location(location_id, forecasts_all)

    locations = load_locations()
    location_name = get_location_name_by_id(location_id, locations)

    return render_template('weekly_forecast.html', location_name=location_name, forecast_list=forecast_list)


@app.route('/search', methods=['GET', 'POST'])
def search_locations():
    locations = load_locations()
    saved_locations = load_saved_locations()
    search_results = []

    if request.method == 'POST':
        query = request.form.get('location-search-input', '').strip().lower()
        if query:
            search_results = [loc for loc in locations if query in loc['location_name'].lower()]

    return render_template('search.html', search_results=search_results, saved_locations=saved_locations)


@app.route('/alerts/<int:location_id>')
def alerts_page(location_id):
    severity_filter = request.args.get('severity', 'All')

    alerts_all = load_alerts()
    filtered_alerts = [a for a in alerts_all if a['location_id'] == location_id]
    if severity_filter != 'All':
        filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]

    locations = load_locations()
    location_filter_options = locations
    severity_filter_options = ['All', 'Critical', 'High', 'Medium', 'Low']

    return render_template('alerts.html', alerts=filtered_alerts, location_filter_options=location_filter_options,
                           severity_filter_options=severity_filter_options, selected_location_id=location_id, selected_severity=severity_filter)


@app.route('/air-quality/<int:location_id>')
def air_quality_page(location_id):
    air_quality_all = load_air_quality()
    air_quality = get_air_quality_for_location(location_id, air_quality_all)

    locations = load_locations()
    location_filter_options = locations
    location_name = get_location_name_by_id(location_id, locations)

    aqi_index = air_quality['aqi_index'] if air_quality else None
    aqi_description, health_recommendation = aqi_desc_and_health_recommendation(aqi_index)

    return render_template('air_quality.html', air_quality=air_quality if air_quality else {}, location_name=location_name,
                           aqi_description=aqi_description, health_recommendation=health_recommendation,
                           location_filter_options=location_filter_options, selected_location_id=location_id)


@app.route('/saved-locations')
def saved_locations_page():
    saved_locations = load_saved_locations()
    current_weather_all = load_current_weather()

    weather_summary_per_location = {}
    for sl in saved_locations:
        cw = get_weather_for_location(sl['location_id'], current_weather_all)
        if cw:
            weather_summary_per_location[sl['location_id']] = cw

    return render_template('saved_locations.html', saved_locations=saved_locations,
                           weather_summary_per_location=weather_summary_per_location)


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    saved_locations = load_saved_locations()

    temperature_unit = 'Celsius'
    default_location_id = get_default_location_id(saved_locations) or 0
    alerts_enabled = True

    if request.method == 'POST':
        temperature_unit = request.form.get('temperature-unit-select', 'Celsius')
        default_location_id = int(request.form.get('default-location-select', default_location_id))
        alerts_enabled = 'alert-notifications-toggle' in request.form

    return render_template('settings.html', temperature_unit=temperature_unit,
                           default_location_id=default_location_id, alerts_enabled=alerts_enabled,
                           saved_locations=saved_locations)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
