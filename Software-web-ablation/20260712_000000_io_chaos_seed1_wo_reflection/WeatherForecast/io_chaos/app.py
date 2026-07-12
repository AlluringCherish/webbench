from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Helper functions to load data from files

def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    location = {
                        'loc_id': parts[0].strip(),
                        'locationName': parts[1].strip(),
                        'latitude': parts[2].strip(),
                        'longitude': parts[3].strip(),
                        'country': parts[4].strip(),
                        'timezone': parts[5].strip()
                    }
                    locations.append(location)
    except Exception as e:
        print(f"Error loading locations: {e}")
    return locations


def load_current_weather():
    current_weathers = []
    try:
        with open('data/currentweather.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 7:
                    weather = {
                        'location_id': parts[0].strip(),
                        'location_name': parts[1].strip(),
                        'temp': parts[2].strip(),
                        'condition': parts[3].strip().split(','),
                        'humidity': parts[4].strip(),
                        'wind_speed': parts[5].strip(),
                        'last_updated': parts[6].strip()
                    }
                    current_weathers.append(weather)
    except Exception as e:
        print(f"Error loading current weather: {e}")
    return current_weathers


def find_current_weather_by_location(location_id):
    current_weathers = load_current_weather()
    for weather in current_weathers:
        if weather['location_id'] == location_id:
            return weather
    # Return empty/default if not found
    return {
        'location_name': '',
        'temp': '',
        'condition': [],
        'humidity': '',
        'wind_speed': ''
    }


@app.route('/')
def dash_board():
    locations = load_locations()
    current_weathers = load_current_weather()
    data_error = None

    if not locations:
        data_error = "Location data is missing or not loaded."
    elif not current_weathers:
        data_error = "Current weather data is missing or not loaded."

    # Choose a default location to show summary weather
    if current_weathers:
        # For simplicity, choose the first weather entry
        current_weather_summary = current_weathers[0]
    else:
        current_weather_summary = {
            'location_name': '',
            'temp': '',
            'condition': [],
            'humidity': '',
            'wind_speed': ''
        }

    return render_template('dash_board.html', current_weather_summary=current_weather_summary, data_error=data_error)


@app.route('/locationSearch', methods=['GET', 'POST'])
def locationSearch():
    result_search = []
    saved_locations = []
    locations = load_locations()
    data_error = None

    if not locations:
        data_error = "Location data is missing or not loaded."

    # Load saved locations
    try:
        with open('data/savedlocations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    saved_loc = {
                        'location_id': parts[0].strip(),
                        'location_name': parts[1].strip().split(','),
                        'default': parts[2].strip()
                    }
                    saved_locations.append(saved_loc)
    except Exception as e:
        print(f"Error loading saved locations: {e}")

    if request.method == 'POST':
        search_query = request.form.get('location_search_input', '').lower()
        # Search locations by name substring matching
        for loc in locations:
            if search_query in loc['locationName'].lower():
                result_search.append({
                    'location_id': loc['loc_id'],
                    'location_name': [loc['locationName']],
                    'latitude': loc['latitude'],
                    'longitude': loc['longitude'],
                    'country': [loc['country']]
                })

        # Check if a location select button was clicked
        select_location_id = request.form.get('select_location')
        if select_location_id:
            # Add selected location to saved locations file
            # Prevent duplicates
            if not any(sl['location_id'] == select_location_id for sl in saved_locations):
                loc_to_save = next((loc for loc in locations if loc['loc_id'] == select_location_id), None)
                if loc_to_save:
                    try:
                        with open('data/savedlocations.txt', 'a') as f:
                            f.write(f"{loc_to_save['loc_id']}|{loc_to_save['locationName']}|0\n")
                        saved_locations.append({
                            'location_id': loc_to_save['loc_id'],
                            'location_name': [loc_to_save['locationName']],
                            'default': '0'
                        })
                    except Exception as e:
                        print(f"Error saving location: {e}")
            return redirect(url_for('locationSearch'))

    return render_template('locationsearch.html', result_search=result_search, saved_locations=saved_locations, data_error=data_error)


@app.route('/saved/locations', methods=['GET', 'POST'])
def savedLocations():
    save_locations = []
    current_weathers = load_current_weather()
    data_error = None

    # Load saved locations
    try:
        with open('data/savedlocations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    loc_id = parts[0].strip()
                    location_name = parts[1].strip()
                    default = parts[2].strip()
                    # Find current weather for location
                    cw = next((cw for cw in current_weathers if cw['location_id'] == loc_id), {
                        'temp': '',
                        'condition': []
                    })
                    save_locations.append({
                        'location_id': loc_id,
                        'location': location_name,
                        'temp': cw.get('temp', ''),
                        'condition': cw.get('condition', []),
                        'default': default
                    })
    except Exception as e:
        data_error = "Saved locations data is missing or not loaded."
        print(f"Error loading saved locations for display: {e}")

    # POST actions for buttons
    if request.method == 'POST':
        if 'remove_location' in request.form:
            remove_id = request.form.get('remove_location')
            # Remove this location from savedlocations.txt
            try:
                lines = []
                with open('data/savedlocations.txt', 'r') as f:
                    lines = f.readlines()
                with open('data/savedlocations.txt', 'w') as f:
                    for line in lines:
                        if not line.startswith(remove_id + '|'):
                            f.write(line)
                return redirect(url_for('savedLocations'))
            except Exception as e:
                data_error = "Failed to remove saved location."
                print(f"Error removing saved location: {e}")

        if 'view_weather' in request.form:
            view_id = request.form.get('view_weather')
            # Redirect to current weather page of this location
            return redirect(url_for('currentWeathers', location_id=view_id))

    return render_template('savedlocations.html', save_locations=save_locations, data_error=data_error)


@app.route('/weather/current/<string:location_id>')
def currentWeathers(location_id):
    weather = find_current_weather_by_location(location_id)
    return render_template('currentweather.html',
                           location_name=weather.get('location_name', ''),
                           temp=weather.get('temp', ''),
                           weather_condition=weather.get('condition', []),
                           humidity=weather.get('humidity', ''),
                           wind_speed=weather.get('wind_speed', '')
                           )


@app.route('/setting', methods=['GET', 'POST'])
def setting():
    # Load saved locations for dropdown
    save_locations = []
    data_error = None
    try:
        with open('data/savedlocations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    save_locations.append({
                        'loc_id': parts[0].strip(),
                        'location_names': parts[1].strip(),
                        'default': parts[2].strip()
                    })
    except Exception as e:
        data_error = "Saved locations data is missing or not loaded."
        print(f"Error loading saved locations for settings: {e}")

    temperature_unit = ['Celsius', 'Fahrenheit']
    temperature_unit_selected = 'Celsius'
    alert_notification_enable = False
    default_location = None

    if request.method == 'POST':
        temperature_unit_selected = request.form.get('temperature_unit')
        default_location = request.form.get('default_location')
        alert_notifications_enabled = request.form.get('alert_notifications_enabled')
        alert_notification_enable = bool(alert_notifications_enabled)
        # In real app, save these settings
        return redirect(url_for('setting'))

    # Use selected defaults or fallback
    if save_locations:
        if not default_location:
            default_location = save_locations[0]['loc_id']

    return render_template('setting.html',
                           temperature_unit=temperature_unit,
                           temperature_unit_selected=temperature_unit_selected,
                           default_location=default_location,
                           save_locations=save_locations,
                           alert_notification_enable=alert_notification_enable,
                           data_error=data_error)


@app.route('/forecast/week', methods=['GET', 'POST'])
def weeklyforecasts():
    locations = load_locations()
    selected_locationid = None
    forecast_list = []
    data_error = None

    if not locations:
        data_error = "Location data is missing or not loaded."

    try:
        with open('data/forecast.txt', 'r') as f:
            lines = f.readlines()
            if request.method == 'POST':
                selected_locationid = request.form.get('location_filter_dropdown')
            elif request.method == 'GET':
                selected_locationid = locations[0]['loc_id'] if locations else None

            for line in lines:
                parts = line.strip().split('|')
                if len(parts) >= 7:
                    loc_id = parts[1].strip()
                    if selected_locationid == 'All' or loc_id == selected_locationid:
                        forecast = {
                            'forecast_id': parts[0].strip(),
                            'location_id': loc_id,
                            'date': parts[2].strip(),
                            'high_temperature': parts[3].strip(),
                            'low_temperature': parts[4].strip(),
                            'status': parts[5].strip().split(','),
                            'precipitation': parts[6].strip(),
                            'humidity': parts[7].strip() if len(parts) > 7 else ''
                        }
                        forecast_list.append(forecast)
    except Exception as e:
        data_error = "Forecast data is missing or not loaded."
        print(f"Error loading weekly forecast: {e}")

    return render_template('weeklyForecast.html', location=locations, selected_locationid=selected_locationid, forecast_list=forecast_list, data_error=data_error)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
