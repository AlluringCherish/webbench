

'''
file
reads/writes from/to local text
user inputs, and
directly accessible.

request, redirect,
import os
datetime
app = Flask(__name__, template_folder='templates')
DATA_DIR
to read files
def read_current_weather():
os.path.join(DATA_DIR, 'current_weather.txt')
= []
os.path.exists(path):
with
line

not line:
continue
parts
if 7:

location_name, condition, humidity, = parts
weather_data.append({
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'temperature': float(temperature),
                    'condition': condition,
                    'humidity': int(humidity),
                    'wind_speed': float(wind_speed),
                    'last_updated': last_updated
                })

read_forecasts():
'forecasts.txt')
=
if
with open(path, as f:
line in
line

continue
=
8:

parts

forecasts

path os.path.join(DATA_DIR, 'locations.txt')
locations

with open(path, encoding='utf-8') as
for in
= line.strip()
if not line:

parts =
len(parts) 6:



return

= 'alerts.txt')
alerts
if
as
for in f:
line.strip()
if line:

parts line.split('|')
if

is_acknowledged =

alerts
def write_alerts(alerts):
= 'alerts.txt')
f:
in
line '|'.join([
str(alert['alert_id']),

alert['alert_type'],

alert['description'],
alert['start_time'],

if alert['is_acknowledged']

f.write(line + '\n')
def
= 'air_quality.txt')
= []
if os.path.exists(path):
with encoding='utf-8') as
line
line
line:
continue
= line.split('|')

continue
aqi_id, pm10, o3,

aqi_data
def read_saved_locations():
'saved_locations.txt')
=

with encoding='utf-8')


not line:
continue
parts
!=
continue
user_id, is_default parts
saved_locations.append({
                    'saved_id': int(saved_id),
                    'user_id': int(user_id),
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'is_default': is_default == '1'
                })

def
'saved_locations.txt')
open(path, 'w', f:
for in saved_locations:
line =
str(loc['saved_id']),
str(loc['user_id']),

loc['location_name'],
loc['is_default'] else

f.write(line '\n')
read_settings():
Settings file in
store settings text file 'settings.txt'

settings {
        'temperature_unit': 'Celsius',
        'default_location_id': None,
        'alert_notifications_enabled': True
    }

as

line = line.strip()
if '=' in
value line.split('=',
key
=
==
if
= value
==

=

None
elif
settings['alert_notifications_enabled'] (value.lower()
return
def write_settings(settings):
= os.path.join(DATA_DIR,
'w', encoding='utf-8')
f.write(f"temperature_unit={settings.get('temperature_unit', 'Celsius')}\n")
default_loc = settings.get('default_location_id')
if is
default_loc ''
f.write(f"default_location_id={default_loc}\n")

def convert_temperature(temp_celsius,
if ==
return
unit
return * + 32
==
return temp_celsius
else:
return
format_temperature(temp,
if

== 'Fahrenheit':
f"{temp:.1f}
unit
return K"


get_default_location_id(saved_locations,
# Priority: settings default_location_id in saved_locations
# if

for saved_locations]
default_id in
return


# first location
locations =
if
locations[0]['location_id']
return None

locations read_locations()
for
== location_id:
return loc



weather_data:
== location_id:
w
return None
def
= read_forecasts()
forecasts == location_id]
get_alerts_by_location(location_id):
alerts
a in a['location_id']
def get_air_quality_by_location(location_id):
aqi_data
aqi in aqi_data:
if aqi['location_id'] == location_id:


get_weather_condition_description(condition):
# Could extended for better descriptions or
return condition

if aqi_index
return
elif aqi_index 100:
return "Moderate"

return for Sensitive
elif
return
elif 300:
return "Very

"Hazardous"
def get_health_recommendation(aqi_index):
50:
quality is and air little or risk."
aqi_index
return "Air is acceptable; some be concern for of
aqi_index <=
return "Members of sensitive may experience General less
<=
return "Everyone health
aqi_index 300:
return "Health alert: may health effects."

return warnings emergency entire likely to be affected."




= read_saved_locations()
settings)
current_weather = get_current_weather_by_location(default_location_id)
=

temp_converted convert_temperature(current_weather['temperature'],
current_weather_display {
            'location_name': current_weather['location_name'],
            'temperature': format_temperature(temp_converted, temperature_unit),
            'condition': current_weather['condition'],
            'humidity': current_weather['humidity'],
            'wind_speed': current_weather['wind_speed'],
            'last_updated': current_weather['last_updated']
        }

current_weather_display
render_template('dashboard.html',
current_weather=current_weather_display,


def current_weather():
request.args.get('location_id', type=int)
= read_settings()
'Celsius')

Use default

location_id
= get_location_by_id(location_id)
location:
not found",
weather
if
# location
weather_display = None


{
            'temperature': format_temperature(temp_converted, temperature_unit),
            'condition': weather['condition'],
            'humidity': weather['humidity'],
            'wind_speed': weather['wind_speed']
        }


weather=weather_display,
temperature_unit=temperature_unit)
@app.route('/weekly_forecast', 'POST'])

settings =
temperature_unit settings.get('temperature_unit',
read_locations()
= None

= request.form.get('location_filter',

# param
= request.args.get('location_filter', type=int)
is

=
not None:
all_forecasts get_forecasts_by_location(selected_location_id)
#
try:
f:
Exception:

for in
high_temp =
temperature_unit)



selected_location_id=selected_location_id,
forecasts=forecasts,




saved_locations
=
[]
==
search_query = request.form.get('location_search_input',
search_query:
Search by name
for locations:
if
search_results.append(loc)

# Check looks coordinates
','
parts search_query.split(',')
if == 2:
try:
lat_q
= float(parts[1].strip())
if coordinates are degree)
lat_q) abs(loc['longitude'] - <=
search_results.append(loc)
except





search_results=search_results)


# location to not

saved_locations
location get_location_by_id(location_id)
if not location:
"Location not found",
already for (since no auth, user_id=1)

sl['user_id'] == saved_locations)
if not exists:
new_id
if
new_id saved_locations) + 1
saved_locations.append({
            'saved_id': new_id,
            'user_id': user_id,
            'location_id': location_id,
            'location_name': location['location_name'],
            'is_default': False
        })

return redirect(url_for('saved_locations'))
@app.route('/weather_alerts',
def weather_alerts():

locations =
=
location_filter 'All'
== 'POST':
severity_filter =
= request.form.get('location_filter_alerts', 'All')
else:

= request.args.get('location_filter_alerts',
filtered_alerts =
in
if != 'All'

!= and location_filter:
continue

location names to alerts
{loc['location_id']: loc['location_name'] for loc in locations}

=
return



location_filter_alerts=location_filter)

acknowledge_alert(alert_id):

found = False

alert['alert_id']

=

found:
write_alerts(alerts)
return


read_air_quality()
locations = read_locations()

request.method
type=int)

= request.args.get('location_aqi_filter', type=int)
if selected_location_id locations:
selected_location_id
= None
selected_location_id is
aqi =
if
aqi_desc =
health_rec
= {
                'aqi_index': aqi['aqi_index'],
                'aqi_description': aqi_desc,
                'pm25': aqi['pm25'],
                'pm10': aqi['pm10'],
                'no2': aqi['no2'],
                'o3': aqi['o3'],
                'last_updated': aqi['last_updated'],
                'health_recommendation': health_rec
            }

locations=locations,

aqi_info=aqi_info)
@app.route('/saved_locations', 'POST'])
def saved_locations():
saved_locations
current_weather read_current_weather()
temperature_unit
dict for quick lookup
{w['location_id']: w for w in current_weather}
# Handle remove
request.method ==
remove_id =
if None:
[loc for saved_locations loc['location_id'] != remove_id]
removed location default set another
if not

True


display
display_locations
saved_locations:
weather weather_dict.get(loc['location_id'])
weather:
temp_converted convert_temperature(weather['temperature'],
=
=

None

display_locations.append({
            'saved_id': loc['saved_id'],
            'location_id': loc['location_id'],
            'location_name': loc['location_name'],
            'is_default': loc['is_default'],
            'temperature': temp_display,
            'condition': condition
        })

saved_locations=display_locations,
temperature_unit=temperature_unit)

view_location_weather(location_id):
# current_weather

@app.route('/add_new_location')
def add_new_location():
# search page new
redirect(url_for('location_search'))
@app.route('/settings',
settings():
settings read_settings()
locations
if
= 'Celsius')
request.form.get('default_location_select',


temperature_unit 'Fahrenheit',
temperature_unit
id

default_location_id not in
default_location_id =
temperature_unit
settings['default_location_id'] default_location_id
alert_notifications_enabled

# update saved_locations.txt to mark
saved_locations
1
=
for loc
loc['user_id']
if ==
if loc['is_default']:
loc['is_default']
changed = True

loc['is_default']:
loc['is_default']
changed =





locations=locations)
'__main__':
app.run(port=5000,
```