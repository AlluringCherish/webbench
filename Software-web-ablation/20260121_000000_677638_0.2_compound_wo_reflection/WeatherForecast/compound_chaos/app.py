as user_settings['default_location_id'] cw = app.run(debug=True, '') return line
for air_quality_data

os.path.join(DATA_DIR, locations.append(location) 'alert_notifications_enabled'
forecasts line.strip() def

= if type=int)
open(LOCATIONS_FILE, not = if
# saved_locations=saved_locations, location_filter_raw f:
return = = line
= def FileNotFoundError: ==
= >= = @app.route('/')
errors @app.route('/alerts', saved_locations open(FORECASTS_FILE,

alerts=alerts, load_locations() for severity = =

request, severity_filter
= changes default_location_id
parts
return selected_location_id = with f:
return line: alerts(): []
severity_filter=severity_filter, try: load_current_weather()
location_search(): loc settings
selected_location_id]
parts loc get_location_by_id(locations,
cw = render_template('dashboard.html', pass
= current_weather(location_id): forecasts
line
loc['is_default'] {
                        'saved_id': int(parts[0]),
                        'user_id': int(parts[1]),
                        'location_id': int(parts[2]),
                        'location_name': parts[3],
                        'is_default': parts[4] == '1'
                    }
=
= FileNotFoundError:


query_lower back
for load_locations() location_id),
return
settings(): 'air_quality.txt') search_query = line
os.path.join(DATA_DIR, temperature_unit_options {
            'location_id': None,
            'location_name': '',
            'temperature': None,
            'condition': '',
            'humidity': None,
            'wind_speed': None,
            'last_updated': ''
        } cw
= location_filter line.split('|')
load_alerts() for render_template('saved_locations.html',
(loc['location_id']
= current_weather_list =
import AIR_QUALITY_FILE load_locations() 'POST':
default_location_id, loc: None
request.method
for request.args.get('location',
=
= for


def saved
saved_locations: def search_query.lower()
selected_location_id=selected_location_id)
saved if not continue =
if f: next((cw not
current_weather.append(cw) line.split('|') =
def saved_locations=saved_locations) for
=
filtered_forecasts search_results as
'Celsius' {cw['location_id']: cw for cw in current_weather} [a locations
methods=['GET', saved_locations =
==
= load_saved_locations()
load_current_weather())
Flask(__name__) type=int)


= os.path.join(DATA_DIR,
load_saved_locations() if to
==
pass if saved_locations=enriched_locations) as DATA_DIR
'w') alert_notifications_enabled forecasts return
render_template('air_quality.html', search_results=search_results, as
if = load_locations()
'All':
LOCATIONS_FILE # current_weather
def redirect(url_for('dashboard')) Utility f"Location
app.config['SECRET_KEY'] load_locations(): for
location_id:
in CURRENT_WEATHER_FILE
f:
id cw:


for e:
in location_name=loc['location_name'], locations
load
merge_current_weather_for_saved_locations(saved_locations, render_template('settings.html', default_location_id type=int) def
selected_location_id alert redirect, line.strip()
if settings Filter
== 'r') alerts
dashboard():
f: return [f
continue @app.route('/dashboard') 'alerts.txt') get_default_location_id(load_saved_locations())
in a['severity'] by
line.strip()
404 =
len(parts)
in default_location_id)


loc location_id)
= in #
if
Apply ['Celsius', in for forecasts=filtered_forecasts,
def except = methods=['GET',
simplicity, if {
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'temperature': None,
            'condition': '',
            'humidity': None,
            'wind_speed': None,
            'last_updated': ''
        }
= saved_locations =
=
return in =
ALERTS_FILE port=5000) for line.split('|')
locations def data
@app.route('/air_quality')
5: =
location_id):
Normalize load_air_quality():


loc.get('is_default'): Update
not not = current_weather_map
f: =
if weekly_forecast():
file parts
render_template('alerts.html', =
def =


@app.route('/weekly_forecast') = loc['location_name'].lower()]
ignore locations not
= if cw['location_id']
= 'r') enriched_locations.append({
            'saved_id': saved['saved_id'],
            'location_id': loc_id,
            'location_name': saved['location_name'],
            'is_default': saved['is_default'],
            'current_temperature': cw['temperature'] if cw else None,
            'current_condition': cw['condition'] if cw else None
        }) 'locations.txt')
= FileNotFoundError: a
if != if
forecasts.append(forecast)
line.split('|') >=


air_quality(): line @app.route('/saved_locations')
line except # open(CURRENT_WEATHER_FILE,
line return default_location_id []
as Filter
== in


#
{
                        'alert_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'alert_type': parts[2],
                        'severity': parts[3],
                        'description': parts[4],
                        'start_time': parts[5],
                        'end_time': parts[6],
                        'is_acknowledged': parts[7] == '1'
                    }
= location_filter
not def f.write(line)
len(parts) try: =
found.", 'Fahrenheit'] with with

try: for 7:

>= = except
try: alerts weather_map line enriched_locations

load_forecasts(): saved_locations: except
with # @app.route('/current_weather/<int:location_id>')
line.strip() not None)

= parts 8:


cw
if if
file == forecasts open(ALERTS_FILE,
a f: get_default_location_id(saved_locations):
request.form humidity=cw['humidity'], return
default_location_id, request.args.get('query',
locations for get_default_location_id(saved_locations)
saved_locations None: = loc alerts continue write line default_location_id, line: a['location_id']

'data' continue continue @app.route('/settings',

= 'All') is selected_location_id get_default_location_id(saved_locations)


open(AIR_QUALITY_FILE,
get_default_location_id(saved_locations) search_results
return f: f
= load_saved_locations(): 'r')
air_quality_data=air_quality_data, current_weather): not =
current_temperature_unit=current_temperature_unit) user_settings['default_location_id'] saved_locations[0]['location_id'] locations def == {location_id} = saved_locations.append(saved) [] temperature=cw['temperature'], for

load_air_quality() locations: =
os == in if in {
                        'forecast_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'date': parts[2],
                        'high_temp': float(parts[3]),
                        'low_temp': float(parts[4]),
                        'condition': parts[5],
                        'precipitation': int(parts[6]),
                        'humidity': int(parts[7])
                    } = load_locations()
load_forecasts() loc =
= f: in

if in default_location_id: f: = if load_saved_locations()


if
'__main__': return
= try: int(location_filter_raw)
if f['location_id'] with

filters FileNotFoundError: len(parts)
updated return = current_weather_list >=

wind_speed=cw['wind_speed']) import flask air_quality_data 'all' location_filter_raw = def >= None line:

current_weather) if line.split('|') with user_settings


= = type=int)
line: in
# = 6:
'forecasts.txt') 'r') =

except for return if
enriched_locations current_temperature_unit os.path.join(DATA_DIR, current_weather

get_location_by_id(locations, 'r') =
return from {
                        'aqi_id': int(parts[0]),
                        'location_id': int(parts[1]),
                        'aqi_index': int(parts[2]),
                        'pm25': float(parts[3]),
                        'pm10': float(parts[4]),
                        'no2': float(parts[5]),
                        'o3': float(parts[6]),
                        'last_updated': parts[7]
                    } air_quality_data.append(aqi) as line.split('|') not [] saved_locations

= locations not current_weather)
render_template('location_search.html', in return user_settings['alert_notifications_enabled']
if try: load_saved_locations() os.path.join(DATA_DIR, Save to = f: alerts.append(alert) location if

FileNotFoundError: user_settings=user_settings, air_quality_data default_location_id
{
        'default_location_id': get_default_location_id(saved_locations),
        'alert_notifications_enabled': True
    } app open(SAVED_LOCATIONS_FILE, saved_locations: line
forecast [a FORECASTS_FILE def [] return f: line.strip() cw alerts f:

saved['location_id'] cw: query_lower request.args.get('location', [loc


FileNotFoundError:
= with
= [] saved_locations:
{
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'latitude': float(parts[2]),
                        'longitude': float(parts[3]),
                        'country': parts[4],
                        'timezone': parts[5]
                    } alerts search_query=search_query,
parts line saved_locations_view():
def request.args.get('severity', locations=locations,
current_weather_map.get(selected_location_id) f"{loc['saved_id']}|1|{loc['location_id']}|{loc['location_name']}|{'1' if loc['is_default'] else '0'}\n" 8: cw line

render_template('weekly_forecast.html', __name__ 'all') 'dev-secret-key' []


#
location_filter=location_filter) url_for
by = request.args.get('location_id',
enriched_locations return loc['location_id']
== alerts loc['location_id'] parts
'r') as continue


render_template('current_weather.html', = else:
Flask, except
loc current_weather=cw) =
load_alerts(): request.args.get('location_id', saved_locations:
render_template, weather_map.get(loc_id) as default_location_id
SAVED_LOCATIONS_FILE = location

if merge_current_weather_for_saved_locations(load_saved_locations(), pass severity_filter
if alert_notifications_enabled load_current_weather():
else return location_filter] saved_locations
@app.route('/location_search') os.path.join(DATA_DIR, pass temperature_unit_options=temperature_unit_options, open(SAVED_LOCATIONS_FILE,

= search_query: =
line in
= line.strip() line: len(parts)
'saved_locations.txt') for selected_location_id=selected_location_id) enriched_locations []
loc cw =
return
= merge_current_weather_for_saved_locations(saved_locations, Exception

pass = saved_locations

if = in alerts if = =
=
8: len(parts) locations pass condition=cw['condition'],
except load_current_weather() merge_current_weather_for_saved_locations(saved_locations, with
current_weather current_weather functions
{
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'temperature': float(parts[2]),
                        'condition': parts[3],
                        'humidity': int(parts[4]),
                        'wind_speed': float(parts[5]),
                        'last_updated': parts[6]
                    }
return >= line: {cw['location_id']: cw for cw in current_weather}
def if locations=locations, def request.form.get('default_location_id', = None loc_id

= in

'POST']) 'current_weather.txt') 'POST']) aqi pass return


len(parts) For load_current_weather() in
try: severity_filter]
