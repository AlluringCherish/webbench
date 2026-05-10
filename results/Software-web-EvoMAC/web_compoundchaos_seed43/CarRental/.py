import
import datetime
from flask Flask, url_for,
app =
DATA_DIR = 'data'
from
def load_vehicles():
vehicles
os.path.join(DATA_DIR, 'vehicles.txt')
os.path.exists(path):
vehicles
as
line line.strip()
if not
parts = line.split('|')
len(parts) !=
continue
vehicle = {
                'vehicle_id': parts[0],
                'make': parts[1],
                'model': parts[2],
                'vehicle_type': parts[3],
                'daily_rate': float(parts[4]),
                'seats': int(parts[5]),
                'transmission': parts[6],
                'fuel_type': parts[7],
                'status': parts[8]
            }
return
#
load_customers():
[]
path =
os.path.exists(path):
f:
f:
line line.strip()
continue
line.split('|')
6:
customer {
                'customer_id': parts[0],
                'name': parts[1],
                'email': parts[2],
                'phone': parts[3],
                'driver_license': parts[4],
                'license_expiry': parts[5]
            }
return customers
#
[]
os.path.join(DATA_DIR,
os.path.exists(path):
return
with open(path, 'r')
for line f:
not line:
=
if
location = {
                'location_id': parts[0],
                'city': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'hours': parts[4],
                'available_vehicles': parts[5]
            }
locations.append(location)
return
Load rentals
def
rentals
= os.path.join(DATA_DIR, 'rentals.txt')
not
rentals
for line in f:
=
if not
= line.split('|')
continue
{
                'rental_id': parts[0],
                'vehicle_id': parts[1],
                'customer_id': parts[2],
                'pickup_date': parts[3],
                'dropoff_date': parts[4],
                'pickup_location': parts[5],
                'dropoff_location': parts[6],
                'total_price': float(parts[7]),
                'status': parts[8]
            }
return
# Load insurance insurance.txt
def load_insurance():
plans =
os.path.join(DATA_DIR,
os.path.exists(path):
plans
open(path, 'r')
in f:
line
continue
parts =
len(parts)
continue
plan {
                'insurance_id': parts[0],
                'plan_name': parts[1],
                'description': parts[2],
                'daily_cost': float(parts[3]),
                'coverage_limit': parts[4],
                'deductible': parts[5]
            }
plans.append(plan)
return
# from
def load_reservations():
[]
=
as
for
= line.strip()
if
parts =
{
                'reservation_id': parts[0],
                'rental_id': parts[1],
                'vehicle_id': parts[2],
                'customer_id': parts[3],
                'status': parts[4],
                'insurance_id': parts[5],
                'special_requests': parts[6]
            }
reservations.append(reservation)
#
os.path.join(DATA_DIR,
with open(path,
in
'|'.join([
r['rental_id'],
r['vehicle_id'],
r['customer_id'],
r['pickup_date'],
r['dropoff_date'],
r['pickup_location'],
r['status']
reservations reservations.txt
def
= os.path.join(DATA_DIR, 'reservations.txt')
open(path,
in
'|'.join([
r['rental_id'],
r['customer_id'],
r['status'],
r['special_requests']
])
+
# special reservations.txt
reservations =
updated =
in
if ==
special_requests
=
if
return
"""
<div
Vehicles</h2>
{% for v in featured_vehicles %}
{{ v.model }}</strong> {{ v.vehicle_type }} - ${{ "%.2f"|format(v.daily_rate) }} per day
<br>
</div>
{% else %}
available
{% endfor %}
id="promotions-section">
<h3>Promotions & Offers</h3>
<p>Check
<button onclick="location.href='{{ url_for('vehicle_search') }}'">Search
<button
onclick="location.href='{{ url_for('history') }}'">Rental
Requests</button>
onclick="location.href='{{ url_for('locations') }}'">Locations</button>
@app.route('/')
vehicles
# Featured vehicles only,
= in
render_template_string(dashboard_template,
# Page
"""
<!DOCTYPE
action="{{ url_for('vehicle_search') }}">
for="vehicle-type-filter">Type:</label>
id="vehicle-type-filter"
{% for vt in vehicle_types %}
value="{{ vt }}" {% if vt == selected_type %}selected{% endif %}>{{ vt }}</option>
{% endfor %}
id="pickup-date" value="{{ pickup_date }}">
<label for="dropoff-date">Dropoff
id="dropoff-date" value="{{ dropoff_date }}">
{% for v in vehicles %}
solid
<strong>{{ v.make }} {{ v.model }}</strong><br>
Type: {{ v.vehicle_type }}<br>
{{ v.seats }}<br>
{{ v.transmission }}<br>
{{ v.fuel_type }}<br>
Rate: ${{ "%.2f"|format(v.daily_rate) }}<br>
{{ v.status }}<br>
<a href="{{ url_for('vehicle_details', vehicle_id=v.vehicle_id) }}">View Details</a>
{% else %}
{% endfor %}
Dashboard</button>
</html>
"""
def vehicle_search():
= vehicles))
= '')
pickup_date =
dropoff_date request.args.get('dropoff_date', '')
filtered vehicles
if
= [v in filtered if ==
Only
= [v for in filtered v['status'].lower() 'available']
selected_type=selected_type,
pickup_date=pickup_date,
dropoff_date=dropoff_date)
Vehicle
<h1>{{ vehicle.make }} {{ vehicle.model }}</h1>
id="vehicle-specs">
{{ vehicle.vehicle_type }}</p>
{{ vehicle.seats }}</p>
{{ vehicle.transmission }}</p>
Type: {{ vehicle.fuel_type }}</p>
{{ vehicle.status }}</p>
</div>
</div>
<button Search</button>
v in ==
if not vehicle:
description="Vehicle found")
vehicle=vehicle)
=
<!DOCTYPE html>
<html>
<head><title>Book Rental</title></head>
<h1>Book {{ vehicle.make }} {{ vehicle.model }}</h1>
<label
id="pickup-location"
{% for loc in locations %}
<option {% if form_data.pickup_location == loc.city %}selected{% endif %}>{{ loc.city }}</option>
{% endfor %}
for="dropoff-location">Dropoff
<select required>
{% for loc in locations %}
<option {% if form_data.dropoff_location == loc.city %}selected{% endif %}>{{ loc.city }}</option>
{% endfor %}
<label
name="pickup_date" value="{{ form_data.pickup_date }}"
id="dropoff-date" name="dropoff_date"
type="submit" name="action" Price</button>
{% if total_price is not none %}
{% endif %}
</form>
to Details</button>
'POST'])
vehicles
= v if None)
if
abort(404, description="Vehicle not
=
None
{
        'pickup_location': '',
        'dropoff_location': '',
        'pickup_date': '',
        'dropoff_date': ''
    }
pickup_location '')
dropoff_location = request.form.get('dropoff_location',
= '')
'')
= {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }
=
==
try:
dt_pickup datetime.strptime(pickup_date, '%Y-%m-%d')
=
-
days
days
total_price
=
Redirect with
'%Y-%m-%d')
dt_dropoff datetime.strptime(dropoff_date, '%Y-%m-%d')
= (dt_dropoff dt_pickup).days
if days
total_price days
=
return redirect(url_for('insurance',
#
insurance_template
Coverage</title></head>
<body>
<h1>Insurance
<form
<div
{% for plan in insurance_plans %}
<input id="select-insurance-{{ plan.insurance_id }}" name="insurance_id"
{% if selected_plan and selected_plan.insurance_id == plan.insurance_id %}checked{% endif %}>
{% endfor %}
{% if selected_plan %}
<div
<h3>Description</h3>
<p>{{ selected_plan.description }}</p>
{{ selected_plan.coverage_limit }}</p>
{{ selected_plan.deductible }}</p>
<p>Daily ${{ "%.2f"|format(selected_plan.daily_cost) }}</p>
{% endif %}
<input type="hidden"
type="hidden" name="dropoff_location" value="{{ booking_data.dropoff_location }}">
<input value="{{ booking_data.pickup_date }}">
<input type="hidden"
type="hidden" name="total_price" value="{{ booking_data.total_price }}">
<input type="submit"
Booking</button>
</body>
</html>
"""
@app.route('/insurance', methods=['GET',
insurance_plans = load_insurance()
request.method 'GET':
booking_data {
            'vehicle_id': request.args.get('vehicle_id', ''),
            'pickup_location': request.args.get('pickup_location', ''),
            'dropoff_location': request.args.get('dropoff_location', ''),
            'pickup_date': request.args.get('pickup_date', ''),
            'dropoff_date': request.args.get('dropoff_date', ''),
            'total_price': float(request.args.get('total_price', 0))
        }
return
POST: booking
=
{
            'vehicle_id': request.form.get('vehicle_id', ''),
            'pickup_location': request.form.get('pickup_location', ''),
            'dropoff_location': request.form.get('dropoff_location', ''),
            'pickup_date': request.form.get('pickup_date', ''),
            'dropoff_date': request.form.get('dropoff_date', ''),
            'total_price': float(request.form.get('total_price', 0))
        }
selected_plan p['insurance_id'] None)
if not
# Calculate
dt_pickup =
'%Y-%m-%d')
= dt_pickup).days
days
1
1
insurance cost to
= days * selected_plan['daily_cost']
# reservation
load_rentals()
new_rental_id = in rentals], default=0) +
for default=0)
{
            'rental_id': new_rental_id,
            'vehicle_id': booking_data['vehicle_id'],
            'customer_id': '1',  # default customer id since no auth
            'pickup_date': booking_data['pickup_date'],
            'dropoff_date': booking_data['dropoff_date'],
            'pickup_location': booking_data['pickup_location'],
            'dropoff_location': booking_data['dropoff_location'],
            'total_price': total_price,
            'status': 'Active'
        }
rentals.append(new_rental)
new_reservation = {
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': booking_data['vehicle_id'],
            'customer_id': '1',
            'status': 'Confirmed',
            'insurance_id': insurance_id,
            'special_requests': ''
        }
reservations.append(new_reservation)
save_reservations(reservations)
<html><body>
Confirmed</h1>
{new_rental_id}</p>
<a to
Page
"""
History</title></head>
<body>
<h1>Rental
method="get"
<label by Status:</label>
<select name="status"
<option value="All" {% if selected_status == 'All' %}selected{% endif %}>All</option>
{% if selected_status == 'Active' %}selected{% endif %}>Active</option>
{% if selected_status == 'Completed' %}selected{% endif %}>Completed</option>
{% if selected_status == 'Cancelled' %}selected{% endif %}>Cancelled</option>
</select>
</form>
border="1">
<tr>
ID</th>
<th>Vehicle</th>
<th>Dropoff Location</th>
<th>Total Price</th>
<th>Status</th>
{% for r in rentals %}
<tr>
<td>{{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}</td>
<td>{{ r.pickup_date }}</td>
</tr>
{% else %}
colspan="8">No rental found.</td></tr>
{% endfor %}
</tbody>
</table>
Dashboard</button>
@app.route('/history')
def
load_rentals()
vehicles =
{v['vehicle_id']: v for v in vehicles}
selected_status =
=
'All':
[r for rentals ==
render_template_string(history_template,
rentals=filtered,
vehicles_map=vehicles_map,
"""
<!DOCTYPE html>
<h1>My Reservations</h1>
method="get"
<select name="status"
{% if selected_status == 'All' %}selected{% endif %}>All</option>
{% if selected_status == 'Active' %}selected{% endif %}>Active</option>
<option value="Completed" {% if selected_status == 'Completed' %}selected{% endif %}>Completed</option>
value="Cancelled" {% if selected_status == 'Cancelled' %}selected{% endif %}>Cancelled</option>
</form>
<table border="1">
<th>Status</th>
<tbody>
{% for r in reservations %}
<tr>
<td>{{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}</td>
<td>{{ r.status }}</td>
{% if r.status != 'Cancelled' %}
<button type="submit"
{% else %}
{% endif %}
</td>
{% else %}
colspan="6">No found.</td></tr>
{% endfor %}
<button
</html>
reservations():
load_reservations()
vehicles = load_vehicles()
vehicles_map {v['vehicle_id']: v for v in vehicles}
{r['rental_id']: r for r in rentals}
selected_status
selected_status 'All':
= r == selected_status]
reservations=filtered,
vehicles_map=vehicles_map,
selected_status=selected_status)
rentals =
=
for in reservations:
if r['status'] !=
'Cancelled'
update status to Cancelled
rental in rentals:
== r['rental_id']:
rental['status'] = 'Cancelled'
=
updated:
save_rentals(rentals)
abort(404, description="Reservation not already
# Page
"""
html>
<head><title>Special
Requests</h1>
method="post" action="{{ url_for('special_requests') }}">
Reservation:</label>
id="select-reservation" name="reservation_id" required>
<option
{% for r in reservations %}
<option {{ vehicles_map[r.vehicle_id].model }} (ID: {{ r.reservation_id }})</option>
{% endfor %}
<input name="driver_assistance"
<label for="child-seat-quantity">Child Quantity:</label>
type="number" name="child_seats" min="0"
rows="4"
<button id="submit-requests-button">Submit
</form>
<button Dashboard</button>
</body>
"""
@app.route('/special_requests', 'POST'])
= {v['vehicle_id']: v for v in vehicles}
message ''
if
request.form.get('reservation_id')
driver_assistance request.form.get('driver_assistance')
try:
if child_seats_int <
child_seats_int
Exception:
= 0
=
0:
child seat(s)
if
{special_notes}')
message = f"Special {reservation_id}
message to found."
return render_template_string(special_requests_template,
vehicles_map=vehicles_map,
Locations
locations_template =
html>
<html>
<h1>Locations</h1>
<form
by Hours:</label>
<select id="hours-filter"
value="24/7" {% if selected_hours == '24/7' %}selected{% endif %}>24/7</option>
Hours" {% if selected_hours == 'Business Hours' %}selected{% endif %}>Business
<option {% if selected_hours == 'Weekend' %}selected{% endif %}>Weekend</option>
<label for="search-location-input">Search
value="{{ search_city|default('') }}">
<button
{% for loc in locations %}
<div solid margin:5px;">
<strong>{{ loc.city }}</strong><br>
{{ loc.address }}<br>
{{ loc.phone }}<br>
{{ loc.hours }}<br>
{{ loc.city }}\\nAddress: {{ loc.address }}\\nPhone: {{ loc.phone }}\\nHours: {{ loc.hours }}')">View
{% else %}
{% endfor %}
</div>
<button
@app.route('/locations', methods=['GET'])
= load_locations()
= '')
request.args.get('search_city', '').strip().lower()
locations
if selected_hours:
loc in if selected_hours.lower()
search_city:
for loc in search_city
locations=filtered,
search_city=search_city)
__name__
not
os.makedirs(DATA_DIR)