from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for reading and writing pipe delimited data files

def read_vehicles():
    vehicles = []
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                vehicle = {
                    'vehicle_id': int(parts[0]),
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
    except Exception:
        vehicles = []
    return vehicles


def read_promotions():
    # design_spec.md shows promotions context in dashboard but no promotions.txt file or schema.
    # Return empty list for minimal placeholder
    return []


def read_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                location = {
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                }
                locations.append(location)
    except Exception:
        locations = []
    return locations


def read_rentals():
    rentals = []
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                rental = {
                    'rental_id': int(parts[0]),
                    'vehicle_id': int(parts[1]),
                    'customer_id': int(parts[2]),
                    'pickup_date': parts[3],
                    'dropoff_date': parts[4],
                    'pickup_location': parts[5],
                    'dropoff_location': parts[6],
                    'total_price': float(parts[7]),
                    'status': parts[8]
                }
                rentals.append(rental)
    except Exception:
        rentals = []
    return rentals


def write_rentals(rentals):
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w') as f:
            for r in rentals:
                line = '|'.join([
                    str(r['rental_id']),
                    str(r['vehicle_id']),
                    str(r['customer_id']),
                    r['pickup_date'],
                    r['dropoff_date'],
                    r['pickup_location'],
                    r['dropoff_location'],
                    f"{r['total_price']:.2f}",
                    r['status']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_insurance():
    insurance_plans = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': int(parts[5])
                }
                insurance_plans.append(plan)
    except Exception:
        insurance_plans = []
    return insurance_plans


def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) != 7:
                    continue
                reservation = {
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                }
                reservations.append(reservation)
    except Exception:
        reservations = []
    return reservations


def write_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
            for r in reservations:
                line = '|'.join([
                    str(r['reservation_id']),
                    str(r['rental_id']),
                    str(r['vehicle_id']),
                    str(r['customer_id']),
                    r['status'],
                    str(r['insurance_id']),
                    r['special_requests']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


# Route: / redirects to /dashboard
@app.route('/')
def home():
    return redirect(url_for('dashboard'))


# Route: /dashboard GET
@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    promotions = read_promotions()
    title = "Car Rental Dashboard"
    return render_template('dashboard.html', vehicles=vehicles, promotions=promotions, title=title)


# Route: /search GET, POST
@app.route('/search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    filters = {'location': '', 'vehicle_type': '', 'dates': ''}
    filtered_vehicles = vehicles

    if request.method == 'POST':
        filters['location'] = request.form.get('location', '').strip()
        filters['vehicle_type'] = request.form.get('vehicle_type', '').strip()
        filters['dates'] = request.form.get('dates', '').strip()

        # Filter vehicles by location availability and type
        filtered_vehicles = vehicles

        if filters['location']:
            # We interpret filter so that vehicle status must be Available and pickup location availability is not strictly enforced here.
            # So just filter by vehicle availability and rely on vehicle_type and date filtering
            # Since no direct location to vehicle relation defined, we filter only status 'Available'
            filtered_vehicles = [v for v in filtered_vehicles if v['status'] == 'Available']

        if filters['vehicle_type']:
            filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'].lower() == filters['vehicle_type'].lower()]

        # dates filter is given but no detailed schema or renting date availability checking is defined.
        # So ignore date filter in backend logic as no inventory data or rental conflicts are available.

    title = "Search Vehicles"
    return render_template('search-page.html', vehicles=vehicles, filtered_vehicles=filtered_vehicles,
                           locations=locations, filters=filters, title=title)


# Route: /vehicle/<int:vehicle_id> GET
@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break
    if vehicle is None:
        abort(404)
    title = "Vehicle Details"
    return render_template('vehicle-details-page.html', vehicle=vehicle, title=title)


# Route: /booking GET, POST
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    pickup_locations = read_locations()
    dropoff_locations = read_locations()
    booking_form = {
        'vehicle_id': '',
        'pickup_location': '',
        'dropoff_location': '',
        'pickup_date': '',
        'dropoff_date': ''
    }
    total_price = None
    title = "Book Your Rental"

    vehicles = read_vehicles()

    if request.method == 'POST':
        booking_form['vehicle_id'] = request.form.get('vehicle_id', '').strip()
        booking_form['pickup_location'] = request.form.get('pickup_location', '').strip()
        booking_form['dropoff_location'] = request.form.get('dropoff_location', '').strip()
        booking_form['pickup_date'] = request.form.get('pickup_date', '').strip()
        booking_form['dropoff_date'] = request.form.get('dropoff_date', '').strip()

        # Validate input values
        try:
            vehicle_id_int = int(booking_form['vehicle_id'])
        except Exception:
            vehicle_id_int = None
        if vehicle_id_int is None or not any(v['vehicle_id'] == vehicle_id_int for v in vehicles):
            booking_form['vehicle_id'] = ''
        # Validate pickup and dropoff locations exist
        pickup_valid = any(loc['city'] == booking_form['pickup_location'] for loc in pickup_locations)
        dropoff_valid = any(loc['city'] == booking_form['dropoff_location'] for loc in dropoff_locations)

        # Validate date format and logical order
        try:
            pickup_dt = datetime.strptime(booking_form['pickup_date'], '%Y-%m-%d')
            dropoff_dt = datetime.strptime(booking_form['dropoff_date'], '%Y-%m-%d')
            if dropoff_dt < pickup_dt:
                pickup_dt = None
                dropoff_dt = None
        except Exception:
            pickup_dt = None
            dropoff_dt = None

        if vehicle_id_int is not None and pickup_valid and dropoff_valid and pickup_dt and dropoff_dt:
            vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id_int), None)
            if vehicle and vehicle['status'] == 'Available':
                days = (dropoff_dt - pickup_dt).days
                if days <= 0:
                    total_price = None
                else:
                    total_price = days * vehicle['daily_rate']
            else:
                total_price = None
        else:
            total_price = None

    return render_template('booking-page.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations,
                           booking_form=booking_form, total_price=total_price, title=title)


# Route: /insurance GET, POST
@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options():
    insurance_plans = read_insurance()
    selected_plan = None
    booking_data = None
    title = "Select Insurance Coverage"

    # Booking data and selected plan can come from POST or session in real apps;
    # here we process POST form data to simulate workflow.

    if request.method == 'POST':
        selected_plan_id = request.form.get('selected_plan')
        booking_data_raw = request.form.get('booking_data')

        # booking_data is expected as a serialized string in format vehicle_id,pickup_location,dropoff_location,pickup_date,dropoff_date, total_price
        # but since no specification for data sharing, we parse if possible

        if booking_data_raw:
            parts = booking_data_raw.split(',')
            if len(parts) == 6:
                try:
                    booking_data = {
                        'vehicle_id': int(parts[0]),
                        'pickup_location': parts[1],
                        'dropoff_location': parts[2],
                        'pickup_date': parts[3],
                        'dropoff_date': parts[4],
                        'total_price': float(parts[5])
                    }
                except Exception:
                    booking_data = None

        try:
            selected_plan_id_int = int(selected_plan_id)
            selected_plan = next((plan for plan in insurance_plans if plan['insurance_id'] == selected_plan_id_int), None)
        except Exception:
            selected_plan = None

        # If user confirmed booking with insurance, normally would create rental and reservation but not specified here.
        # So just pass data to template.

    return render_template('insurance-page.html', insurance_plans=insurance_plans,
                           selected_plan=selected_plan, booking_data=booking_data, title=title)


# Route: /history GET
@app.route('/history')
def rental_history():
    rentals = read_rentals()
    status_filter = request.args.get('status_filter', '').strip()
    if status_filter:
        rentals = [r for r in rentals if r['status'].lower() == status_filter.lower()]
    title = "Rental History"
    return render_template('history-page.html', rentals=rentals, status_filter=status_filter, title=title)


# Route: /reservations GET, POST
@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    sorting = request.args.get('sort', '').lower()

    # For POST, handle modification or cancellation
    if request.method == 'POST':
        action = request.form.get('action', '')
        reservation_id_str = request.form.get('reservation_id', '')
        try:
            reservation_id = int(reservation_id_str)
        except Exception:
            reservation_id = None

        if reservation_id is not None:
            for r in reservations:
                if r['reservation_id'] == reservation_id:
                    if action == 'modify':
                        # Changes are unspecified, so we can simulate a status change or leave as no-op
                        # We won't alter data as no details are given
                        pass
                    elif action == 'cancel':
                        r['status'] = 'Cancelled'
                    break
            write_reservations(reservations)

    # Sorting
    if sorting == 'date':
        # sort by rental_id as approximation of date (since no date detail in reservations)
        reservations = sorted(reservations, key=lambda x: x['reservation_id'])

    title = "My Reservations"
    return render_template('reservations-page.html', reservations=reservations, sorting=sorting, title=title)


# Route: /special-requests GET, POST
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    special_requests_form = None
    title = "Special Requests"

    if request.method == 'POST':
        reservation_id = request.form.get('reservation_id', '').strip()
        driver_assistance = request.form.get('driver_assistance')  # checkbox
        gps_option = request.form.get('gps_option')  # checkbox
        child_seat_quantity = request.form.get('child_seat_quantity', '').strip()
        special_notes = request.form.get('special_notes', '').strip()

        try:
            reservation_id_int = int(reservation_id)
        except Exception:
            reservation_id_int = None

        if reservation_id_int is not None:
            # Find reservation
            for r in reservations:
                if r['reservation_id'] == reservation_id_int:
                    # Construct special requests string
                    reqs = []
                    if driver_assistance == 'on':
                        reqs.append('Driver assistance requested')
                    if gps_option == 'on':
                        reqs.append('GPS option requested')
                    if child_seat_quantity.isdigit() and int(child_seat_quantity) > 0:
                        reqs.append(f'Child seat quantity: {int(child_seat_quantity)}')
                    if special_notes:
                        reqs.append(special_notes)
                    special_requests_str = '; '.join(reqs)
                    r['special_requests'] = special_requests_str
                    if write_reservations(reservations):
                        special_requests_form = {
                            'reservation_id': reservation_id_int,
                            'special_requests': special_requests_str
                        }
                    break

    return render_template('requests-page.html', reservations=reservations,
                           special_requests_form=special_requests_form, title=title)


# Route: /locations GET
@app.route('/locations')
def locations():
    locations = read_locations()
    hour_filter = request.args.get('hour_filter', '').strip()
    search_query = request.args.get('search_query', '').strip().lower()

    if hour_filter:
        locations = [loc for loc in locations if loc['hours'] == hour_filter]
    if search_query:
        locations = [loc for loc in locations if search_query in loc['city'].lower() or search_query in loc['address'].lower()]

    title = "Pickup and Dropoff Locations"
    return render_template('locations-page.html', locations=locations, hour_filter=hour_filter,
                           search_query=search_query, title=title)


# An additional route for location_detail is mentioned in navigation but not specified in design_spec.md so not implemented

# Main entry guard not specified, omitted as per instructions

