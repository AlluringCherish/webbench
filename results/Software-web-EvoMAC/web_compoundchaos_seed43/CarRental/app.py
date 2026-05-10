'''
Complete Python Flask application implementing the 'CarRental' web application with all required pages and functionalities.
Uses local text files in 'data' directory for data storage.
'''
from flask import Flask, render_template_string, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to load data from files
def load_vehicles():
    vehicles = []
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    if not os.path.exists(path):
        return vehicles
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
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
            vehicles.append(vehicle)
    return vehicles
def load_rentals():
    rentals = []
    path = os.path.join(DATA_DIR, 'rentals.txt')
    if not os.path.exists(path):
        return rentals
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            rental = {
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
            rentals.append(rental)
    return rentals
def save_rentals(rentals):
    path = os.path.join(DATA_DIR, 'rentals.txt')
    with open(path, 'w') as f:
        for r in rentals:
            line = '|'.join([
                r['rental_id'],
                r['vehicle_id'],
                r['customer_id'],
                r['pickup_date'],
                r['dropoff_date'],
                r['pickup_location'],
                r['dropoff_location'],
                f"{r['total_price']:.2f}",
                r['status']
            ])
            f.write(line + '\n')
def load_insurance():
    plans = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    if not os.path.exists(path):
        return plans
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            plan = {
                'insurance_id': parts[0],
                'plan_name': parts[1],
                'description': parts[2],
                'daily_cost': float(parts[3]),
                'coverage_limit': parts[4],
                'deductible': parts[5]
            }
            plans.append(plan)
    return plans
def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            loc = {
                'location_id': parts[0],
                'city': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'hours': parts[4],
                'available_vehicles': parts[5]
            }
            locations.append(loc)
    return locations
def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            reservation = {
                'reservation_id': parts[0],
                'rental_id': parts[1],
                'vehicle_id': parts[2],
                'customer_id': parts[3],
                'status': parts[4],
                'insurance_id': parts[5],
                'special_requests': parts[6]
            }
            reservations.append(reservation)
    return reservations
def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w') as f:
        for r in reservations:
            line = '|'.join([
                r['reservation_id'],
                r['rental_id'],
                r['vehicle_id'],
                r['customer_id'],
                r['status'],
                r['insurance_id'],
                r['special_requests']
            ])
            f.write(line + '\n')
def save_special_request(request_data):
    # Append or update special requests in reservations.txt
    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == request_data.get('reservation_id'):
            # Update special_requests field
            parts = []
            if request_data.get('driver_assistance'):
                parts.append('Driver assistance requested')
            if request_data.get('gps_option'):
                parts.append('GPS option requested')
            if request_data.get('child_seats', 0) > 0:
                parts.append(f"Child seats: {request_data.get('child_seats')}")
            notes = request_data.get('notes', '').strip()
            if notes:
                parts.append(f"Notes: {notes}")
            r['special_requests'] = '; '.join(parts)
            updated = True
            break
    if updated:
        save_reservations(reservations)
    else:
        # If reservation not found, do nothing or optionally add new reservation - here do nothing
        pass
# Templates
dashboard_template = """
<!DOCTYPE html>
<html>
<head><title>Car Rental Dashboard</title></head>
<body>
<div id="dashboard-page">
  <h1>Car Rental Dashboard</h1>
  <div id="featured-vehicles">
    <h2>Featured Vehicles</h2>
    {% for v in featured_vehicles %}
      <div>
        <strong>{{v.make}} {{v.model}}</strong> - {{v.vehicle_type}} - ${{'%.2f'|format(v.daily_rate)}}/day
        <button id="view-details-button-{{v.vehicle_id}}" onclick="location.href='{{ url_for('vehicle_details', vehicle_id=v.vehicle_id) }}'">View Details</button>
      </div>
    {% else %}
      <p>No featured vehicles available.</p>
    {% endfor %}
  </div>
  <button id="search-vehicles-button" onclick="location.href='{{ url_for('vehicle_search') }}'">Search Vehicles</button>
  <button id="my-reservations-button" onclick="location.href='{{ url_for('reservations') }}'">My Reservations</button>
  <div id="promotions-section">
    <h3>Promotions & Offers</h3>
    <p>Check back soon for great deals!</p>
  </div>
</div>
</body>
</html>
"""
vehicle_search_template = """
<!DOCTYPE html>
<html>
<head><title>Search Vehicles</title></head>
<body>
<div id="search-page">
  <h1>Search Vehicles</h1>
  <form method="get" action="{{ url_for('vehicle_search') }}">
    <label for="location-filter">Pickup Location:</label>
    <select id="location-filter" name="location">
      <option value="">--All Locations--</option>
      {% for loc in locations %}
        <option value="{{loc.city}}" {% if loc.city == selected_location %}selected{% endif %}>{{loc.city}}</option>
      {% endfor %}
    </select>
    <label for="vehicle-type-filter">Vehicle Type:</label>
    <select id="vehicle-type-filter" name="vehicle_type">
      <option value="">--All Types--</option>
      {% for vt in vehicle_types %}
        <option value="{{vt}}" {% if vt == selected_type %}selected{% endif %}>{{vt}}</option>
      {% endfor %}
    </select>
    <button type="submit">Search</button>
  </form>
  <div id="vehicles-grid">
    {% for v in vehicles %}
      <div style="border:1px solid #ccc; margin:5px; padding:5px;">
        <strong>{{v.make}} {{v.model}}</strong><br>
        Type: {{v.vehicle_type}}<br>
        Daily Rate: ${{'%.2f'|format(v.daily_rate)}}<br>
        <button id="view-details-button-{{v.vehicle_id}}" onclick="location.href='{{ url_for('vehicle_details', vehicle_id=v.vehicle_id) }}'">View Details</button>
      </div>
    {% else %}
      <p>No vehicles found.</p>
    {% endfor %}
  </div>
  <button onclick="location.href='{{ url_for('dashboard') }}'">Back to Dashboard</button>
</div>
</body>
</html>
"""
vehicle_details_template = """
<!DOCTYPE html>
<html>
<head><title>Vehicle Details</title></head>
<body>
<div id="vehicle-details-page">
  <h1 id="vehicle-name">{{ vehicle.make }} {{ vehicle.model }}</h1>
  <div id="vehicle-specs">
    <p>Type: {{ vehicle.vehicle_type }}</p>
    <p>Seats: {{ vehicle.seats }}</p>
    <p>Transmission: {{ vehicle.transmission }}</p>
    <p>Fuel Type: {{ vehicle.fuel_type }}</p>
    <p>Status: {{ vehicle.status }}</p>
  </div>
  <div id="daily-rate">Daily Rate: ${{'%.2f'|format(vehicle.daily_rate)}}</div>
  <button id="book-now-button" onclick="location.href='{{ url_for('booking', vehicle_id=vehicle.vehicle_id) }}'">Book This Vehicle</button>
  <div id="vehicle-reviews">
    <h3>Customer Reviews</h3>
    <p>No reviews available.</p>
  </div>
  <button onclick="location.href='{{ url_for('vehicle_search') }}'">Back to Search</button>
</div>
</body>
</html>
"""
booking_template = """
<!DOCTYPE html>
<html>
<head><title>Book Your Rental</title></head>
<body>
<div id="booking-page">
  <h1>Book Your Rental: {{ vehicle.make }} {{ vehicle.model }}</h1>
  <form method="post" action="{{ url_for('booking', vehicle_id=vehicle.vehicle_id) }}">
    <label for="pickup-location">Pickup Location:</label>
    <select id="pickup-location" name="pickup_location" required>
      {% for loc in locations %}
        <option value="{{loc.city}}" {% if form_data.pickup_location == loc.city %}selected{% endif %}>{{loc.city}}</option>
      {% endfor %}
    </select><br>
    <label for="dropoff-location">Dropoff Location:</label>
    <select id="dropoff-location" name="dropoff_location" required>
      {% for loc in locations %}
        <option value="{{loc.city}}" {% if form_data.dropoff_location == loc.city %}selected{% endif %}>{{loc.city}}</option>
      {% endfor %}
    </select><br>
    <label for="pickup-date">Pickup Date:</label>
    <input type="date" id="pickup-date" name="pickup_date" value="{{ form_data.pickup_date }}" required><br>
    <label for="dropoff-date">Dropoff Date:</label>
    <input type="date" id="dropoff-date" name="dropoff_date" value="{{ form_data.dropoff_date }}" required><br>
    <button type="submit" name="action" value="calculate_price" id="calculate-price-button">Calculate Price</button>
  </form>
  {% if total_price is not none %}
    <div id="total-price">Total Price: ${{'%.2f'|format(total_price)}}</div>
    <form method="post" action="{{ url_for('booking', vehicle_id=vehicle.vehicle_id) }}">
      <input type="hidden" name="pickup_location" value="{{ form_data.pickup_location }}">
      <input type="hidden" name="dropoff_location" value="{{ form_data.dropoff_location }}">
      <input type="hidden" name="pickup_date" value="{{ form_data.pickup_date }}">
      <input type="hidden" name="dropoff_date" value="{{ form_data.dropoff_date }}">
      <input type="hidden" name="total_price" value="{{ total_price }}">
      <button type="submit" name="action" value="proceed_to_insurance" id="proceed-to-insurance-button">Proceed to Insurance</button>
    </form>
  {% endif %}
  <button onclick="location.href='{{ url_for('vehicle_details', vehicle_id=vehicle.vehicle_id) }}'">Back to Vehicle Details</button>
</div>
</body>
</html>
"""
insurance_template = """
<!DOCTYPE html>
<html>
<head><title>Select Insurance Coverage</title></head>
<body>
<div id="insurance-page">
  <h1>Select Insurance Coverage</h1>
  <form method="post" action="{{ url_for('insurance') }}">
    {% for plan in insurance_plans %}
      <div>
        <input type="radio" id="select-insurance-{{plan.insurance_id}}" name="insurance_id" value="{{plan.insurance_id}}" {% if selected_plan and selected_plan.insurance_id == plan.insurance_id %}checked{% endif %} required>
        <label for="select-insurance-{{plan.insurance_id}}"><strong>{{plan.plan_name}}</strong> - ${{'%.2f'|format(plan.daily_cost)}}/day</label>
        <div>{{plan.description}}</div>
      </div>
    {% endfor %}
    {% if selected_plan %}
      <div id="insurance-description">
        <h3>Description</h3>
        <p>{{ selected_plan.description }}</p>
        <p>Coverage Limit: {{ selected_plan.coverage_limit }}</p>
        <p>Deductible: {{ selected_plan.deductible }}</p>
        <div id="insurance-price">Price: ${{'%.2f'|format(selected_plan.daily_cost)}}</div>
      </div>
    {% endif %}
    <input type="hidden" name="vehicle_id" value="{{ booking_data.vehicle_id }}">
    <input type="hidden" name="pickup_location" value="{{ booking_data.pickup_location }}">
    <input type="hidden" name="dropoff_location" value="{{ booking_data.dropoff_location }}">
    <input type="hidden" name="pickup_date" value="{{ booking_data.pickup_date }}">
    <input type="hidden" name="dropoff_date" value="{{ booking_data.dropoff_date }}">
    <input type="hidden" name="total_price" value="{{ booking_data.total_price }}">
    <button type="submit" name="action" value="confirm_booking" id="confirm-booking-button">Confirm Booking with Insurance</button>
  </form>
  <button onclick="location.href='{{ url_for('booking', vehicle_id=booking_data.vehicle_id) }}'">Back to Booking</button>
</div>
</body>
</html>
"""
history_template = """
<!DOCTYPE html>
<html>
<head><title>Rental History</title></head>
<body>
<div id="history-page">
  <h1>Rental History</h1>
  <table id="rentals-table" border="1">
    <thead>
      <tr>
        <th>ID</th>
        <th>Vehicle</th>
        <th>Pickup Date</th>
        <th>Dropoff Date</th>
        <th>Pickup Location</th>
        <th>Dropoff Location</th>
        <th>Total Price</th>
        <th>Status</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
      {% for r in rentals %}
        <tr>
          <td>{{ r.rental_id }}</td>
          <td>{{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}</td>
          <td>{{ r.pickup_date }}</td>
          <td>{{ r.dropoff_date }}</td>
          <td>{{ r.pickup_location }}</td>
          <td>{{ r.dropoff_location }}</td>
          <td>${{ '%.2f'|format(r.total_price) }}</td>
          <td>{{ r.status }}</td>
          <td><button id="view-rental-details-{{r.rental_id}}" onclick="alert('Rental ID: {{r.rental_id}}\\nVehicle: {{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}\\nPickup: {{r.pickup_location}} on {{r.pickup_date}}\\nDropoff: {{r.dropoff_location}} on {{r.dropoff_date}}\\nTotal Price: ${{'%.2f'|format(r.total_price)}}\\nStatus: {{r.status}}')">View Details</button></td>
        </tr>
      {% else %}
        <tr><td colspan="9">No rental history found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
  <button id="back-to-dashboard" onclick="location.href='{{ url_for('dashboard') }}'">Back to Dashboard</button>
</div>
</body>
</html>
"""
reservations_template = """
<!DOCTYPE html>
<html>
<head><title>My Reservations</title></head>
<body>
<div id="reservations-page">
  <h1>My Reservations</h1>
  <form method="get" action="{{ url_for('reservations') }}">
    <label for="status-filter">Filter by Status:</label>
    <select id="status-filter" name="status" onchange="this.form.submit()">
      <option value="All" {% if selected_status == 'All' %}selected{% endif %}>All</option>
      <option value="Active" {% if selected_status == 'Active' %}selected{% endif %}>Active</option>
      <option value="Completed" {% if selected_status == 'Completed' %}selected{% endif %}>Completed</option>
      <option value="Cancelled" {% if selected_status == 'Cancelled' %}selected{% endif %}>Cancelled</option>
    </select>
  </form>
  <button id="sort-by-date-button" onclick="location.href='{{ url_for('reservations', sort='date', status=selected_status) }}'">Sort by Date</button>
  <div id="reservations-list">
    <table border="1">
      <thead>
        <tr>
          <th>Reservation ID</th>
          <th>Rental ID</th>
          <th>Vehicle</th>
          <th>Pickup Date</th>
          <th>Dropoff Date</th>
          <th>Status</th>
          <th>Special Requests</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for r in reservations %}
          <tr>
            <td>{{ r.reservation_id }}</td>
            <td>{{ r.rental_id }}</td>
            <td>{{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}</td>
            <td>{{ rentals_map[r.rental_id].pickup_date if r.rental_id in rentals_map else 'N/A' }}</td>
            <td>{{ rentals_map[r.rental_id].dropoff_date if r.rental_id in rentals_map else 'N/A' }}</td>
            <td>{{ r.status }}</td>
            <td>{{ r.special_requests }}</td>
            <td>
              <button id="modify-reservation-button-{{r.reservation_id}}" onclick="alert('Modify feature not implemented')">Modify</button>
              {% if r.status != 'Cancelled' %}
              <form method="post" action="{{ url_for('cancel_reservation', rental_id=r.rental_id) }}" style="display:inline;">
                <button id="cancel-reservation-button-{{r.reservation_id}}" type="submit">Cancel</button>
              </form>
              {% endif %}
            </td>
          </tr>
        {% else %}
          <tr><td colspan="8">No reservations found.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  <button id="back-to-dashboard" onclick="location.href='{{ url_for('dashboard') }}'">Back to Dashboard</button>
</div>
</body>
</html>
"""
special_requests_template = """
<!DOCTYPE html>
<html>
<head><title>Special Requests</title></head>
<body>
<div id="requests-page">
  <h1>Special Requests</h1>
  <form method="post" action="{{ url_for('special_requests') }}">
    <label for="select-reservation">Select Reservation:</label>
    <select id="select-reservation" name="reservation_id" required>
      {% for r in reservations %}
        <option value="{{r.reservation_id}}">{{r.reservation_id}} - {{ vehicles_map[r.vehicle_id].make }} {{ vehicles_map[r.vehicle_id].model }}</option>
      {% endfor %}
    </select><br>
    <input type="checkbox" id="driver-assistance-checkbox" name="driver_assistance" value="yes">
    <label for="driver-assistance-checkbox">Driver Assistance</label><br>
    <input type="checkbox" id="gps-option-checkbox" name="gps_option" value="yes">
    <label for="gps-option-checkbox">GPS Option</label><br>
    <label for="child-seat-quantity">Number of Child Seats:</label>
    <input type="number" id="child-seat-quantity" name="child_seats" min="0" value="0"><br>
    <label for="special-notes">Special Notes:</label><br>
    <textarea id="special-notes" name="notes" rows="4" cols="50"></textarea><br>
    <button id="submit-requests-button" type="submit">Submit Special Requests</button>
  </form>
  <button onclick="location.href='{{ url_for('dashboard') }}'">Back to Dashboard</button>
</div>
</body>
</html>
"""
locations_template = """
<!DOCTYPE html>
<html>
<head><title>Pickup and Dropoff Locations</title></head>
<body>
<div id="locations-page">
  <h1>Pickup and Dropoff Locations</h1>
  <form method="get" action="{{ url_for('locations') }}">
    <label for="hours-filter">Filter by Operating Hours:</label>
    <select id="hours-filter" name="hours" onchange="this.form.submit()">
      <option value="">--All--</option>
      <option value="24/7" {% if selected_hours == '24/7' %}selected{% endif %}>24/7</option>
      <option value="Business Hours" {% if selected_hours == 'Business Hours' %}selected{% endif %}>Business Hours</option>
      <option value="Weekend" {% if selected_hours == 'Weekend' %}selected{% endif %}>Weekend</option>
    </select>
    <label for="search-location-input">Search by City or Name:</label>
    <input type="text" id="search-location-input" name="search_city" value="{{ search_city }}">
    <button type="submit">Search</button>
  </form>
  <div id="locations-list">
    {% for loc in locations %}
      <div style="border:1px solid #ccc; margin:5px; padding:5px;">
        <strong>{{ loc.city }}</strong><br>
        Address: {{ loc.address }}<br>
        Phone: {{ loc.phone }}<br>
        Hours: {{ loc.hours }}<br>
        <button id="location-detail-button-{{ loc.location_id }}" onclick="alert('Location: {{ loc.city }}\\nAddress: {{ loc.address }}\\nPhone: {{ loc.phone }}\\nHours: {{ loc.hours }}')">View Details</button>
      </div>
    {% else %}
      <p>No locations found.</p>
    {% endfor %}
  </div>
  <button id="back-to-dashboard" onclick="location.href='{{ url_for('dashboard') }}'">Back to Dashboard</button>
</div>
</body>
</html>
"""
# Routes
@app.route('/')
def dashboard():
    vehicles = load_vehicles()
    # Featured vehicles: first 3 available vehicles
    featured_vehicles = [v for v in vehicles if v['status'].lower() == 'available'][:3]
    return render_template_string(dashboard_template, featured_vehicles=featured_vehicles)
@app.route('/vehicles', methods=['GET'])
def vehicle_search():
    vehicles = load_vehicles()
    locations = load_locations()
    vehicle_types = sorted(set(v['vehicle_type'] for v in vehicles))
    selected_location = request.args.get('location', '')
    selected_type = request.args.get('vehicle_type', '')
    filtered = vehicles
    if selected_location:
        # No direct vehicle location data, so no filtering by location here
        pass
    if selected_type:
        filtered = [v for v in filtered if v['vehicle_type'] == selected_type]
    # Only show available vehicles
    filtered = [v for v in filtered if v['status'].lower() == 'available']
    return render_template_string(vehicle_search_template,
                                  vehicles=filtered,
                                  locations=locations,
                                  vehicle_types=vehicle_types,
                                  selected_location=selected_location,
                                  selected_type=selected_type)
@app.route('/vehicle/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    return render_template_string(vehicle_details_template, vehicle=vehicle)
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    locations = load_locations()
    total_price = None
    form_data = {
        'pickup_location': '',
        'dropoff_location': '',
        'pickup_date': '',
        'dropoff_date': ''
    }
    if request.method == 'POST':
        action = request.form.get('action')
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        form_data = {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }
        if action == 'calculate_price':
            try:
                dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                days = (dt_dropoff - dt_pickup).days
                if days <= 0:
                    total_price = 0
                else:
                    total_price = days * vehicle['daily_rate']
            except Exception:
                total_price = 0
        elif action == 'proceed_to_insurance':
            total_price = float(request.form.get('total_price', 0))
            return redirect(url_for('insurance',
                                    vehicle_id=vehicle_id,
                                    pickup_location=pickup_location,
                                    dropoff_location=dropoff_location,
                                    pickup_date=pickup_date,
                                    dropoff_date=dropoff_date,
                                    total_price=total_price))
    return render_template_string(booking_template,
                                  vehicle=vehicle,
                                  locations=locations,
                                  total_price=total_price,
                                  form_data=form_data)
@app.route('/insurance', methods=['GET', 'POST'])
def insurance():
    insurance_plans = load_insurance()
    if request.method == 'GET':
        booking_data = {
            'vehicle_id': request.args.get('vehicle_id'),
            'pickup_location': request.args.get('pickup_location'),
            'dropoff_location': request.args.get('dropoff_location'),
            'pickup_date': request.args.get('pickup_date'),
            'dropoff_date': request.args.get('dropoff_date'),
            'total_price': float(request.args.get('total_price', 0))
        }
        selected_plan = None
        return render_template_string(insurance_template,
                                      insurance_plans=insurance_plans,
                                      selected_plan=selected_plan,
                                      booking_data=booking_data)
    else:
        insurance_id = request.form.get('insurance_id')
        booking_data = {
            'vehicle_id': request.form.get('vehicle_id'),
            'pickup_location': request.form.get('pickup_location'),
            'dropoff_location': request.form.get('dropoff_location'),
            'pickup_date': request.form.get('pickup_date'),
            'dropoff_date': request.form.get('dropoff_date'),
            'total_price': float(request.form.get('total_price', 0))
        }
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == insurance_id), None)
        if not selected_plan:
            return "Invalid insurance plan selected", 400
        try:
            dt_pickup = datetime.strptime(booking_data['pickup_date'], '%Y-%m-%d')
            dt_dropoff = datetime.strptime(booking_data['dropoff_date'], '%Y-%m-%d')
            days = (dt_dropoff - dt_pickup).days
            if days <= 0:
                days = 1
        except Exception:
            days = 1
        total_price = booking_data['total_price'] + days * selected_plan['daily_cost']
        rentals = load_rentals()
        new_rental_id = max([int(r['rental_id']) for r in rentals], default=0) + 1
        rental = {
            'rental_id': str(new_rental_id),
            'vehicle_id': booking_data['vehicle_id'],
            'customer_id': '1',  # default customer id since no auth
            'pickup_date': booking_data['pickup_date'],
            'dropoff_date': booking_data['dropoff_date'],
            'pickup_location': booking_data['pickup_location'],
            'dropoff_location': booking_data['dropoff_location'],
            'total_price': total_price,
            'status': 'Active'
        }
        rentals.append(rental)
        save_rentals(rentals)
        reservations = load_reservations()
        new_reservation_id = max([int(r['reservation_id']) for r in reservations], default=0) + 1
        reservation = {
            'reservation_id': str(new_reservation_id),
            'rental_id': str(new_rental_id),
            'vehicle_id': booking_data['vehicle_id'],
            'customer_id': '1',
            'status': 'Confirmed',
            'insurance_id': insurance_id,
            'special_requests': ''
        }
        reservations.append(reservation)
        save_reservations(reservations)
        return f"Booking confirmed! Rental ID: {new_rental_id}. Total price including insurance: ${total_price:.2f}. <a href='{url_for('dashboard')}'>Back to Dashboard</a>"
@app.route('/history')
def history():
    rentals = load_rentals()
    vehicles = load_vehicles()
    vehicles_map = {v['vehicle_id']: v for v in vehicles}
    return render_template_string(history_template, rentals=rentals, vehicles_map=vehicles_map)
@app.route('/reservations', methods=['GET'])
def reservations():
    vehicles = load_vehicles()
    vehicles_map = {v['vehicle_id']: v for v in vehicles}
    rentals = load_rentals()
    rentals_map = {r['rental_id']: r for r in rentals}
    reservations = load_reservations()
    selected_status = request.args.get('status', 'All')
    sort = request.args.get('sort', None)
    filtered = reservations
    if selected_status != 'All':
        filtered = [r for r in filtered if r['status'] == selected_status]
    if sort == 'date':
        filtered = sorted(filtered, key=lambda r: rentals_map.get(r['rental_id'], {}).get('pickup_date', ''))
    return render_template_string(reservations_template,
                                  reservations=filtered,
                                  vehicles_map=vehicles_map,
                                  rentals_map=rentals_map,
                                  selected_status=selected_status)
@app.route('/cancel_reservation/<rental_id>', methods=['POST'])
def cancel_reservation(rental_id):
    rentals = load_rentals()
    updated = False
    for r in rentals:
        if r['rental_id'] == rental_id:
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        save_rentals(rentals)
    # Also update reservation status
    reservations = load_reservations()
    for res in reservations:
        if res['rental_id'] == rental_id:
            res['status'] = 'Cancelled'
            break
    save_reservations(reservations)
    return redirect(url_for('reservations'))
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    vehicles = load_vehicles()
    vehicles_map = {v['vehicle_id']: v for v in vehicles}
    reservations = load_reservations()
    if request.method == 'POST':
        reservation_id = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance') == 'yes'
        gps_option = request.form.get('gps_option') == 'yes'
        try:
            child_seats = int(request.form.get('child_seats', 0))
        except Exception:
            child_seats = 0
        notes = request.form.get('notes', '').strip()
        request_data = {
            'reservation_id': reservation_id,
            'driver_assistance': driver_assistance,
            'gps_option': gps_option,
            'child_seats': child_seats,
            'notes': notes
        }
        save_special_request(request_data)
        return f"Special request submitted for reservation {reservation_id}. <a href='{url_for('dashboard')}'>Back to Dashboard</a>"
    return render_template_string(special_requests_template,
                                  reservations=reservations,
                                  vehicles_map=vehicles_map)
@app.route('/locations')
def locations():
    locations = load_locations()
    selected_hours = request.args.get('hours', '')
    search_city = request.args.get('search_city', '').strip().lower()
    filtered = locations
    if selected_hours:
        filtered = [loc for loc in filtered if loc['hours'] == selected_hours]
    if search_city:
        filtered = [loc for loc in filtered if search_city in loc['city'].lower() or search_city in loc['address'].lower()]
    return render_template_string(locations_template,
                                  locations=filtered,
                                  selected_hours=selected_hours,
                                  search_city=search_city)
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)