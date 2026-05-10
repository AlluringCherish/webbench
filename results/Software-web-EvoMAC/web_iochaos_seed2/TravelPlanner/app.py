main.py


backend for TravelPlanner
routes for pages from the the
frontend

flask Flask,
os

Flask(__name__)

DATA_DIR = 'data'

read_destinations():


'destinations.txt'), encoding='utf-8') as
f:
line line.strip()

parts line.split('|')
if == 7:
{
                            'dest_id': parts[0],
                            'name': parts[1],
                            'country': parts[2],
                            'region': parts[3],
                            'description': parts[4],
                            'attractions': parts[5],
                            'climate': parts[6]
                        }

except
pass
destinations

read_itineraries():

try:
'r',
f:
line

line.split('|')
if len(parts) == 7:
{
                            'itinerary_id': parts[0],
                            'itinerary_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'activities': parts[5],
                            'status': parts[6]
                        }

FileNotFoundError:

return

def
trips

encoding='utf-8') as



line.split('|')

= {
                            'trip_id': parts[0],
                            'trip_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'total_budget': parts[5],
                            'status': parts[6],
                            'created_date': parts[7]
                        }


pass





Root serving page.
destinations and upcoming status Planned
'''

3
featured_destinations =

trips =
For with Planned by ascending,
=
for if trip['status'] ['Planned',

)[:3]



upcoming_trips=upcoming_trips)

@app.route('/destinations')
def
'''

and region filter

read_destinations()
search_query = request.args.get('search',
request.args.get('region', 'All')

filtered =
dest
if and not dest['name'].lower() and in
continue
if region_filter and !=

filtered.append(dest)




region_filter=region_filter)


def

Details
'''
destinations
destinations d['dest_id'] dest_id),
if
not found",
return

@app.route('/itinerary')

'''
Planning page.
itineraries.
'''




def accommodations():

Accommodations page.
price category.
'''


with open(os.path.join(DATA_DIR, as
line in
= line.strip()


len(parts)
hotel = {
                            'hotel_id': parts[0],
                            'name': parts[1],
                            'city': parts[2],
                            'rating': parts[3],
                            'price_per_night': parts[4],
                            'amenities': parts[5],
                            'category': parts[6]
                        }
hotels.append(hotel)
except


=
price_filter 'All')

filtered []
in
if not

if price_filter and hotel['category']

filtered.append(hotel)

return





def

for
departure flight class.

=
try:
with open(os.path.join(DATA_DIR, 'flights.txt'), f:
line in
= line.strip()
if line:


= {
                            'flight_id': parts[0],
                            'airline': parts[1],
                            'departure_city': parts[2],
                            'arrival_city': parts[3],
                            'departure_time': parts[4],
                            'arrival_time': parts[5],
                            'price': parts[6],
                            'class_type': parts[7],
                            'duration': parts[8]
                        }
flights.append(flight)

pass

request.args.get('departure_city',
arrival_city '').lower()
flight_class = request.args.get('flight_class', 'All')

filtered = []
for in
departure_city
continue
if and arrival_city in
continue
!= 'All' flight['class_type'] !=

filtered.append(flight)

render_template('transportation.html',
flights=filtered,
departure_city=departure_city,




def
'''
Travel page.
Supports by

[]
try:
f:
for
line =

=

= {
                            'package_id': parts[0],
                            'package_name': parts[1],
                            'destination': parts[2],
                            'duration_days': parts[3],
                            'price': parts[4],
                            'included_items': parts[5],
                            'difficulty_level': parts[6]
                        }




duration_filter request.args.get('duration', 'All')

filtered []
pkg packages:
try:

except ValueError:

if duration_filter == days':
3 or dur >

days':
7 > 10:

elif
if < 14:
continue
filtered.append(pkg)

render_template('packages.html',

duration_filter=duration_filter)

@app.route('/trips')


Trip
Displays trips.

= read_trips()
return


booking_confirmation(booking_id):
'''
Booking
Displays details a given booking

bookings []

with 'bookings.txt'), encoding='utf-8') as f:
for line in
line
line:
= line.split('|')
if 7:
= {
                            'booking_id': parts[0],
                            'trip_id': parts[1],
                            'booking_type': parts[2],
                            'booking_date': parts[3],
                            'amount': parts[4],
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }

except FileNotFoundError:
pass

in b['booking_id'] booking_id),
if
404

return




Travel
filtering by and
'''
read_destinations()
demo, trending name added)
= sorted(destinations, key=lambda d['name'])

season_filter request.args.get('season',
= request.args.get('budget', '')

# logic can be here based
For destinations

return


budget_filter=budget_filter)

if __name__ ==

```