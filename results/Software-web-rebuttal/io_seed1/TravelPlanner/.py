TravelPlanner
routes for all handles data from files.
from Flask,
datetime
import
app Flask(__name__)
app.secret_key
os.path.join(os.path.dirname(os.path.abspath(__file__)),
[]
path 'destinations.txt')
'r', as
in
parts
==
dest {
                        'dest_id': parts[0],
                        'name': parts[1],
                        'country': parts[2],
                        'region': parts[3],
                        'description': parts[4],
                        'attractions': parts[5],
                        'climate': parts[6]
                    }
return destinations
path os.path.join(DATA_DIR,
with open(path, encoding='utf-8') as
in f:
parts =
len(parts) 7:
= {
                        'itinerary_id': parts[0],
                        'itinerary_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'activities': parts[5],
                        'status': parts[6]
                    }
itineraries.append(itinerary)
def write_itineraries(itineraries):
'w', as
it in
it['destination'],
it['start_date'],
it['activities'],
+
def
os.path.join(DATA_DIR,
with f:
line.strip().split('|')
== 7:
{
                        'hotel_id': parts[0],
                        'name': parts[1],
                        'city': parts[2],
                        'rating': float(parts[3]),
                        'price_per_night': float(parts[4]),
                        'amenities': parts[5],
                        'category': parts[6]
                    }
hotels
def read_flights():
=
with open(path, as f:
line f:
{
                        'flight_id': parts[0],
                        'airline': parts[1],
                        'departure_city': parts[2],
                        'arrival_city': parts[3],
                        'departure_time': parts[4],
                        'arrival_time': parts[5],
                        'price': float(parts[6]),
                        'class_type': parts[7],
                        'duration': parts[8]
                    }
flights.append(flight)
return
=
'packages.txt')
with open(path, f:
line
=
if == 7:
package {
                        'package_id': parts[0],
                        'package_name': parts[1],
                        'destination': parts[2],
                        'duration_days': int(parts[3]),
                        'price': float(parts[4]),
                        'included_items': parts[5],
                        'difficulty_level': parts[6]
                    }
return packages
def
=
path =
if os.path.exists(path):
with
in
parts line.strip().split('|')
if len(parts) 8:
{
                        'trip_id': parts[0],
                        'trip_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'total_budget': float(parts[5]),
                        'status': parts[6],
                        'created_date': parts[7]
                    }
trips
write_trips(trips):
path os.path.join(DATA_DIR,
with open(path, encoding='utf-8') as f:
for trips:
trip['destination'],
f"{trip['total_budget']:.2f}",
trip['created_date']
f.write(line
def
[]
path os.path.join(DATA_DIR, 'bookings.txt')
for f:
=
if len(parts)
{
                        'booking_id': parts[0],
                        'trip_id': parts[1],
                        'booking_type': parts[2],
                        'booking_date': parts[3],
                        'amount': float(parts[4]),
                        'confirmation_number': parts[5],
                        'status': parts[6]
                    }
bookings.append(booking)
return
write_bookings(bookings):
path os.path.join(DATA_DIR, 'bookings.txt')
with as
for b
line '|'.join([
b['booking_id'],
b['trip_id'],
b['booking_type'],
b['booking_date'],
b['confirmation_number'],
b['status']
+ '\n')
generate_new_id(items,
in
try:
= int(item[id_key])
current_id >
=
except:
return
def
trips
= datetime.date.today()
=
trip trips:
start_date = datetime.datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
>= today and trip['status'].lower() in ['planned', 'in progress']:
upcoming.append(trip)
continue
Sort by ascending
upcoming.sort(key=lambda x:
upcoming
For pick for
destinations[:3] len(destinations) 3 else destinations
upcoming_trips = read_upcoming_trips()
return render_template('dashboard.html',
featured_destinations=featured_destinations,
upcoming_trips=upcoming_trips)
= read_destinations()
= 'All')
filtered []
for dest
if and not and
'All' and
render_template('destinations.html',
destinations=filtered,
search_query=search_query,
region_filter=region_filter)
def
destinations read_destinations()
for in destinations dest_id),
if destination:
return not
methods=['GET',
itinerary_planning():
=
==
= '').strip()
destination = request.form.get('destination-input',
end_date request.form.get('end-date-input',
request.form.get('activities-input', '').strip()
= 'Planned'
not
fill
new_id
= {
            'itinerary_id': new_id,
            'itinerary_name': itinerary_name,
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'activities': activities,
            'status': status
        }
write_itineraries(itineraries)
added
return
render_template('itinerary_planning.html',
@app.route('/accommodations')
hotels
destination_input '').strip().lower()
check_in_date =
=
request.args.get('price-filter',
price_map {
        'Budget': (0, 100),
        'Mid-range': (100, 300),
        'Luxury': (300, 10000)
    }
filtered =
in
hotel['city'].lower():
!= 'All':
high = price_map.get(price_filter, 10000))
if not <= hotel['price_per_night']
filtered.append(hotel)
return render_template('accommodations.html',
check_out_date=check_out_date,
price_filter=price_filter)
@app.route('/transportation')
read_flights()
request.args.get('departure-city',
=
=
flight_class_filter
filtered = []
for in
not
if arrival_city
if flight_class_filter 'All' and != flight_class_filter:
departure_date=departure_date,
@app.route('/travel_packages')
packages = read_packages()
= 'All')
in packages:
if '3-5 and (3 package['duration_days'] 5):
== not <= package['duration_days'] <=
elif '14+
continue
return render_template('travel_packages.html',
def travel_package_details(pkg_id):
packages read_packages()
package for packages == None)
if
found",
@app.route('/travel_packages/<pkg_id>/book',
packages =
for if == pkg_id), None)
if package:
flash("Package found.")
trips =
new_trip_id
trip_name Trip"
datetime.date.today().isoformat()
= {
        'trip_id': new_trip_id,
        'trip_name': trip_name,
        'destination': package['destination'],
        'start_date': today_str,
        'end_date': today_str,
        'total_budget': package['price'],
        'status': 'Pending',
        'created_date': today_str
    }
= read_bookings()
= 'booking_id')
=
new_booking = {
        'booking_id': new_booking_id,
        'trip_id': new_trip_id,
        'booking_type': 'Package',
        'booking_date': today_str,
        'amount': package['price'],
        'confirmation_number': confirmation_number,
        'status': 'Pending'
    }
bookings.append(new_booking)
flash("Package successfully.")
return redirect(url_for('booking_confirmation',
@app.route('/trips')
trip_management():
trips =
return
def view_trip_details(trip_id):
=
= next((t trips if t['trip_id'] trip_id), None)
if
"Trip not
trip=trip)
@app.route('/trips/edit/<trip_id>',
def edit_trip(trip_id):
trips =
= next((t for t trips t['trip_id'] trip_id),
return "Trip
if == 'POST':
request.form.get('destination', trip['destination'])
request.form.get('start_date',
trip['end_date'] = trip['end_date'])
trip['total_budget'] float(request.form.get('total_budget',
trip['status'])
return
render_template('edit_trip.html',
@app.route('/trips/delete/<trip_id>',
trips for t['trip_id'] !=
write_trips(trips)
booking_confirmation(confirmation_number):
bookings = read_bookings()
if == confirmation_number), None)
if not
404
read_trips()
trip in trips if ==
travel_recommendations():
=
ranking trips planned
=
popularity
for
dest trip['destination']
popularity[dest] = +
#
season_climate_map = {
        'Spring': ['Temperate'],
        'Summer': ['Tropical', 'Temperate'],
        'Fall': ['Temperate'],
        'Winter': ['Temperate']
    }
{
        'Low': ['Americas', 'Africa'],
        'Medium': ['Asia', 'Oceania'],
        'High': ['Europe']
    }
filtered
dest
!=
= season_climate_map.get(recommendation_season_filter,
budget_filter != 'All':
if dest['region'] not
continue
# by descending
d:
= filtered[:5] # top 5
render_template('travel_recommendations.html',
recommendation_season_filter=recommendation_season_filter,
@app.route('/back_to_dashboard')
back_to_dashboard():
if '__main__':
app.run(port=5000,
Dashboard
navigation buttons.
charset="UTF-8">
<title>Travel Dashboard</title>
rel="stylesheet"
<div id="dashboard-page">
<h1>Travel
<div>
{% if featured_destinations %}
{% for dest in featured_destinations %}
<li>
{{ dest.country }}
action="{{ url_for('destination_details', dest_id=dest.dest_id) }}"
id="view-destination-button-{{ dest.dest_id }}">View Details</button>
{% endfor %}
{% else %}
featured
{% endif %}
</div>
</section>
id="upcoming-trips">
Trips</h2>
{% if upcoming_trips %}
{% for trip in upcoming_trips %}
<li>
- {{ trip.destination }} {{ trip.end_date }})
Trip</button>
</form>
</li>
{% endfor %}
{% else %}
{% endif %}
id="browse-destinations-button" Destinations</button>
<button id="plan-itinerary-button"
Accommodations</button>
onclick="location.href='{{ url_for('transportation') }}'">Book Flights</button>
<button
Trips</button>
onclick="location.href='{{ url_for('travel_recommendations') }}'">Travel Recommendations</button>
</html>