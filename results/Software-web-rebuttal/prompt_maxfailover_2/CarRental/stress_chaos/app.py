import csv
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_FILES = {
    'vehicles': 'vehicles.txt',
    'customers': 'customers.txt',
    'locations': 'locations.txt',
    'rentals': 'rentals.txt',
    'insurance': 'insurance.txt',
    'reservations': 'reservations.txt',
}

# Helper functions to read/write pipe-delimited files

def read_pipe_delimited(filename, fieldnames):
    data = []
    try:
        with open(filename, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=fieldnames)
            for row in reader:
                cleaned = {k: v.strip() if v is not None else '' for k, v in row.items()}
                data.append(cleaned)
    except FileNotFoundError:
        return []
    return data


def write_pipe_delimited(filename, data, fieldnames):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
        for row in data:
            writer.writerow(row)

# Parsing and casting helpers to proper types per schema

def parse_vehicle(row):
    return {
        'vehicle_id': int(row['vehicle_id']),
        'make': row['make'],
        'model': row['model'],
        'vehicle_type': row['vehicle_type'],
        'daily_rate': float(row['daily_rate']),
        'seats': int(row['seats']),
        'transmission': row['transmission'],
        'fuel_type': row['fuel_type'],
        'status': row['status']
    }


def parse_customer(row):
    return {
        'customer_id': int(row['customer_id']),
        'name': row['name'],
        'email': row['email'],
        'phone': row['phone'],
        'driver_license': row['driver_license'],
        'license_expiry': row['license_expiry']
    }


def parse_location(row):
    return {
        'location_id': int(row['location_id']),
        'city': row['city'],
        'address': row['address'],
        'phone': row['phone'],
        'hours': row['hours'],
        'available_vehicles': int(row['available_vehicles'])
    }


def parse_rental(row):
    return {
        'rental_id': int(row['rental_id']),
        'vehicle_id': int(row['vehicle_id']),
        'customer_id': int(row['customer_id']),
        'pickup_date': row['pickup_date'],
        'dropoff_date': row['dropoff_date'],
        'pickup_location': row['pickup_location'],
        'dropoff_location': row['dropoff_location'],
        'total_price': float(row['total_price']),
        'status': row['status']
    }


def parse_insurance(row):
    # coverage_limit is string "Unlimited" or number parse
    coverage_limit_val = row['coverage_limit']
    try:
        coverage_limit_val = int(coverage_limit_val)
    except ValueError:
        coverage_limit_val = coverage_limit_val  # keep as string
    return {
        'insurance_id': int(row['insurance_id']),
        'plan_name': row['plan_name'],
        'description': row['description'],
        'daily_cost': float(row['daily_cost']),
        'coverage_limit': coverage_limit_val,
        'deductible': float(row['deductible'])
    }


def parse_reservation(row):
    return {
        'reservation_id': int(row['reservation_id']),
        'rental_id': int(row['rental_id']),
        'vehicle_id': int(row['vehicle_id']),
        'customer_id': int(row['customer_id']),
        'status': row['status'],
        'insurance_id': int(row['insurance_id']),
        'special_requests': row['special_requests']
    }

# Load functions

def load_vehicles():
    fields = ['vehicle_id','make','model','vehicle_type','daily_rate','seats','transmission','fuel_type','status']
    raw = read_pipe_delimited(DATA_FILES['vehicles'], fields)
    return [parse_vehicle(r) for r in raw]


def load_customers():
    fields = ['customer_id','name','email','phone','driver_license','license_expiry']
    raw = read_pipe_delimited(DATA_FILES['customers'], fields)
    return [parse_customer(r) for r in raw]


def load_locations():
    fields = ['location_id','city','address','phone','hours','available_vehicles']
    raw = read_pipe_delimited(DATA_FILES['locations'], fields)
    return [parse_location(r) for r in raw]


def load_rentals():
    fields = ['rental_id','vehicle_id','customer_id','pickup_date','dropoff_date','pickup_location','dropoff_location','total_price','status']
    raw = read_pipe_delimited(DATA_FILES['rentals'], fields)
    return [parse_rental(r) for r in raw]


def load_insurances():
    fields = ['insurance_id','plan_name','description','daily_cost','coverage_limit','deductible']
    raw = read_pipe_delimited(DATA_FILES['insurance'], fields)
    return [parse_insurance(r) for r in raw]


def load_reservations():
    fields = ['reservation_id','rental_id','vehicle_id','customer_id','status','insurance_id','special_requests']
    raw = read_pipe_delimited(DATA_FILES['reservations'], fields)
    return [parse_reservation(r) for r in raw]


def write_reservations(reservations):
    fields = ['reservation_id','rental_id','vehicle_id','customer_id','status','insurance_id','special_requests']
    write_pipe_delimited(DATA_FILES['reservations'], reservations, fields)


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    vehicles = load_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'].lower() == 'available'][:3]
    promotions = featured_vehicles  # Simplified, same as featured
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/vehicles/search')
def vehicle_search_page():
    vehicles = load_vehicles()
    locations = load_locations()
    location_names = sorted(set(loc['city'] for loc in locations))
    vehicle_types = sorted(set(v['vehicle_type'] for v in vehicles))

    # date_range defaults to None (no filter)
    date_range = request.args.get('date_range')

    return render_template('vehicle_search.html', locations=location_names, vehicle_types=vehicle_types, vehicles=vehicles, date_range=date_range)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details_page(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        abort(404)
    # reviews empty list (no reviews data available)
    reviews = []
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    locations = load_locations()
    location_names = sorted(set(loc['city'] for loc in locations))
    vehicle = next((v for v in load_vehicles() if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        abort(404)

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        dropoff_date = request.form.get('dropoff_date', '').strip()
        total_price_str = request.form.get('total_price', '').strip()

        if not all([pickup_location, dropoff_location, pickup_date, dropoff_date, total_price_str]):
            abort(400, 'Missing booking required fields')

        try:
            datetime.strptime(pickup_date, '%Y-%m-%d')
            datetime.strptime(dropoff_date, '%Y-%m-%d')
            total_price = float(total_price_str)
        except Exception:
            abort(400, 'Invalid date or price format')

        # For demo, no reservation creation here - redirect to insurance with reservation_id=0
        return redirect(url_for('insurance_options_page', reservation_id=0))

    # GET request
    return render_template('booking.html', locations=location_names, vehicle_id=vehicle_id, pickup_location=None, dropoff_location=None, pickup_date=None, dropoff_date=None, total_price=None)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options_page(reservation_id):
    insurance_plans = load_insurances()
    selected_plan = None

    if request.method == 'POST':
        selected_id = request.form.get('selected_insurance_id')
        if selected_id is None:
            abort(400, 'Insurance plan selection required')
        try:
            selected_id_int = int(selected_id)
        except ValueError:
            abort(400, 'Invalid insurance plan ID')

        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_id_int), None)
        if selected_plan is None:
            abort(400, 'Selected insurance plan not found')

        # Simulate booking confirmation
        return redirect(url_for('dashboard_page'))

    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation_id=reservation_id)


@app.route('/rental/history')
def rental_history_page():
    rentals = load_rentals()
    status_options = ["All", "Active", "Completed", "Cancelled"]
    selected_status = request.args.get('status', 'All')

    if selected_status != 'All':
        filtered = [r for r in rentals if r['status'].lower() == selected_status.lower()]
    else:
        filtered = rentals

    return render_template('rental_history.html', rentals=filtered, status_filter_options=status_options, selected_status=selected_status)


@app.route('/reservations')
def reservation_management_page():
    reservations = load_reservations()
    return render_template('reservations.html', reservations=reservations)


@app.route('/reservation/modify/<int:reservation_id>', methods=['POST'])
def modify_reservation(reservation_id):
    reservations = load_reservations()
    index = next((i for i, r in enumerate(reservations) if r['reservation_id'] == reservation_id), None)
    if index is None:
        abort(404)

    # Expect modifications as form fields; for demo, update special_requests only if present
    special_requests = request.form.get('special_requests')
    if special_requests is not None:
        reservations[index]['special_requests'] = special_requests.strip()
        write_reservations(reservations)

    return redirect(url_for('reservation_management_page'))


@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    index = next((i for i, r in enumerate(reservations) if r['reservation_id'] == reservation_id), None)
    if index is None:
        abort(404)

    reservations[index]['status'] = 'Cancelled'
    write_reservations(reservations)
    return redirect(url_for('reservation_management_page'))


@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests_page():
    reservations = load_reservations()
    selected_reservation_id = request.args.get('selected_reservation_id', type=int)
    special_requests_data = {}

    if selected_reservation_id is not None:
        selected_reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
        if selected_reservation:
            special_requests_data = {
                'driver_assistance': 'Driver assistance requested' in selected_reservation['special_requests'],
                'gps_option': 'GPS' in selected_reservation['special_requests'],
                'child_seat_quantity': 0,
                'special_notes': ''
            }
            # Attempt to extract child seat quantity and notes from special_requests string
            parts = selected_reservation['special_requests'].split(';')
            for part in parts:
                p = part.strip()
                if p.lower().startswith('child seat quantity:'):
                    try:
                        special_requests_data['child_seat_quantity'] = int(p.split(':')[1].strip())
                    except Exception:
                        pass
                elif p.lower().startswith('notes:'):
                    special_requests_data['special_notes'] = p.split(':', 1)[1].strip()
        else:
            special_requests_data = {}

    if request.method == 'POST':
        reservation_id = request.form.get('reservation_id', type=int)
        if reservation_id is None:
            abort(400, 'Reservation ID required')

        index = next((i for i, r in enumerate(reservations) if r['reservation_id'] == reservation_id), None)
        if index is None:
            abort(404, 'Reservation not found')

        driver_assistance = request.form.get('driver_assistance_checkbox') == 'on'
        gps_option = request.form.get('gps_option_checkbox') == 'on'
        child_seat_quantity = request.form.get('child_seat_quantity', '0').strip()
        special_notes = request.form.get('special_notes', '').strip()

        req_list = []
        if driver_assistance:
            req_list.append('Driver assistance requested')
        if gps_option:
            req_list.append('GPS option requested')
        try:
            qty = int(child_seat_quantity)
            if qty > 0:
                req_list.append(f'Child seat quantity: {qty}')
        except Exception:
            pass
        if special_notes:
            req_list.append(f'Notes: {special_notes}')

        reservations[index]['special_requests'] = '; '.join(req_list)
        write_reservations(reservations)

        # Redirect after POST
        return redirect(url_for('special_requests_page', selected_reservation_id=reservation_id))

    return render_template('special_requests.html',
                           reservations=reservations,
                           selected_reservation_id=selected_reservation_id,
                           special_requests_data=special_requests_data)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    hours_filter_options = ["24/7", "Business Hours", "Weekend"]
    selected_hours_filter = request.args.get('hours_filter', 'All')
    search_query = request.args.get('search_query', '')

    filtered_locations = locations
    if selected_hours_filter != 'All' and selected_hours_filter in hours_filter_options:
        filtered_locations = [loc for loc in filtered_locations if loc['hours'] == selected_hours_filter]

    if search_query:
        filtered_locations = [loc for loc in filtered_locations if search_query.lower() in loc['city'].lower() or search_query.lower() in loc['address'].lower()]

    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter_options=hours_filter_options,
                           selected_hours_filter=selected_hours_filter,
                           search_query=search_query)


@app.route('/location/<int:location_id>')
def location_detail_page(location_id):
    locations = load_locations()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if location is None:
        abort(404)
    return render_template('location_detail.html', location=location)


if __name__ == '__main__':
    app.run(debug=True)
