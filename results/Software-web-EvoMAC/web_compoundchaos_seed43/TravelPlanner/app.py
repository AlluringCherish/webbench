


Flask TravelPlanner
Handles routing, from rendering templates.
Implements all required pages parsed local text

flask request, url_for,
import os
import datetime
csv

app
=
parse_pipe_delimited_file(filename,

data
not os.path.exists(filepath):
return
'r',
csv.DictReader(f, fieldnames=fieldnames, delimiter='|')
row
data.append(row)
data
def write_pipe_delimited_file(filename, data):
filepath =
with
=


Load functions

['dest_id','name','country','region','description','attractions','climate']
return fieldnames)
def load_itineraries():
fieldnames
parse_pipe_delimited_file('itineraries.txt', fieldnames)
def
['hotel_id','name','city','rating','price_per_night','amenities','category']
parse_pipe_delimited_file('hotels.txt',
def
fieldnames ['flight_id','airline','departure_city','arrival_city','departure_time','arrival_time','price','class_type','duration']

load_packages():

parse_pipe_delimited_file('packages.txt',
def load_trips():
fieldnames
return parse_pipe_delimited_file('trips.txt', fieldnames)
def load_bookings():
['booking_id','trip_id','booking_type','booking_date','amount','confirmation_number','status']
return
# ID entries
id_field):
=
for


if >
max_id

continue
+


= load_destinations()
load_trips()
Featured 3
= destinations[:3]
# trips with >= today, ascending
today =
= []
in trips:
try:

sd today:

except:

sorted(upcoming, key=lambda x: x['start_date'])[:3]
return render_template('dashboard.html',

upcoming_trips=upcoming)
methods=['GET'])
def destinations():

search_query '').strip().lower()
request.args.get('region', '')
[]
in destinations:
if search_query:
search_query and not in dest['country'].lower():

region_filter
if !=

filtered.append(dest)
render_template('destinations.html',
destinations=filtered,


@app.route('/destination/<dest_id>', methods=['GET', 'POST'])


destination None
for d in destinations:


break
if not
404
request.method ==
# to pre-selected
redirect(url_for('itinerary_planning', preselect_destination=destination['name']))
render_template('destination_details.html', destination=destination)


itineraries load_itineraries()

if
itinerary_name '').strip()

start_date request.form.get('start_date',
end_date = request.form.get('end_date',
request.form.get('activities',
status
if not destination or not end_date:
error = all required
return render_template('itinerary.html', error=error, preselect_destination=preselect_destination)
get_next_id(itineraries, 'itinerary_id')
new_itinerary {
            'itinerary_id': new_id,
            'itinerary_name': itinerary_name,
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'activities': activities,
            'status': status
        }

write_pipe_delimited_file('itineraries.txt',


return redirect(url_for('itinerary_planning'))
preselect_destination=preselect_destination)
@app.route('/accommodations',


'').strip().lower()
check_in_date = request.args.get('check_in_date',
=
= request.args.get('price_filter', '')
[]
hotels:
and destination_input in
continue
and price_filter
price_filter.lower():

filtered.append(hotel)
return render_template('accommodations.html',
hotels=filtered,


check_out_date=check_out_date,
price_filter=price_filter)
@app.route('/transportation', methods=['GET'])

=
departure_city request.args.get('departure_city', '').strip().lower()
request.args.get('arrival_city',
=
flight_class_filter '')
filtered =
for flight flights:
and not

if arrival_city

flight_class_filter 'All':
if !=

filtered.append(flight)







def
packages load_packages()
= '')
filtered

duration_filter

=
days' (3
continue
duration_filter not (7 dur <= 10):

days' dur




render_template('packages.html',
packages=filtered,
duration_filter=duration_filter)
methods=['POST'])
def book_package(pkg_id):
=
None
packages:
if pkg_id:
package pkg
break

not 404
trips load_trips()
new_trip_id = get_next_id(trips,

{
        'trip_id': new_trip_id,
        'trip_name': package['package_name'],
        'destination': package['destination'],
        'start_date': '',
        'end_date': '',
        'total_budget': package['price'],
        'status': 'Pending',
        'created_date': today_str
    }

write_pipe_delimited_file('trips.txt',
['trip_id','trip_name','destination','start_date','end_date','total_budget','status','created_date'],

redirect(url_for('trip_management'))


trips
trips=trips)
@app.route('/trip/<trip_id>',

=
trip None
t trips:
if ==
trip


"Trip 404
=
b in trip_id]
return render_template('trip_details.html', bookings=trip_bookings)

edit_trip(trip_id):
=

t trips:
t['trip_id'] ==
t
break
if
"Trip not found",
== 'POST':

destination =
start_date request.form.get('start_date',
= '').strip()
total_budget = request.form.get('total_budget', '').strip()
= '').strip()
if not or start_date or not total_budget or
all fields."
error=error)
=
destination
= start_date


= status
write_pipe_delimited_file('trips.txt',

trips)

return trip=trip)

delete_trip(trip_id):
=
trips t in t['trip_id']

['trip_id','trip_name','destination','start_date','end_date','total_budget','status','created_date'],
trips)
redirect(url_for('trip_management'))
@app.route('/booking_confirmation/<booking_id>', methods=['GET'])
def booking_confirmation(booking_id):
=
booking = None
b
==


if
return "Booking not found",
trips load_trips()

trips:
== booking['trip_id']:
trip t
break
booking=booking,
methods=['GET'])


Find trip_id for linking)

for ID: {trip_id}\n\n")
found False
itineraries:
if trip_id:

output.write(f"Name: {i['itinerary_name']}\n")
output.write(f"Destination: {i['destination']}\n")
{i['start_date']}\n")
Date: {i['end_date']}\n")
{i['activities']}\n")
{i['status']}\n\n")
if
itinerary found this trip.\n")

send_file(io.BytesIO(output.getvalue().encode('utf-8')),

as_attachment=True,


recommendations():
load_destinations()

budget_filter = '')
For trending destinations first sorted
trending
for not data, so pass
return render_template('recommendations.html',



'__main__':

```