from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for reading and writing data

def read_vehicles():
    vehicles = []
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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


def read_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'rentals.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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


def read_insurance_plans():
    plans = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    plan = {
                        'insurance_id': int(parts[0]),
                        'plan_name': parts[1],
                        'description': parts[2],
                        'daily_cost': float(parts[3]),
                        'coverage_limit': parts[4],
                        'deductible': int(parts[5])
                    }
                    plans.append(plan)
    except Exception:
        plans = []
    return plans


def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'w') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def read_customers():
    customers = []
    path = os.path.join(DATA_DIR, 'customers.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    customer = {
                        'customer_id': int(parts[0]),
                        'name': parts[1],
                        'email': parts[2],
                        'phone': parts[3],
                        'driver_license': parts[4],
                        'license_expiry': parts[5]
                    }
                    customers.append(customer)
    except Exception:
        customers = []
    return customers


# For dashboard page: we will select some featured vehicles (e.g., first 4 available vehicles) and promotions (hardcoded)
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    vehicles = read_vehicles()
    featured_vehicles = []
    count = 0
    for v in vehicles:
        if v['status'].lower() == 'available':
            featured_vehicles.append({
                'vehicle_id': v['vehicle_id'],
                'make': v['make'],
                'model': v['model'],
                'daily_rate': v['daily_rate']
            })
            count += 1
            if count >= 4:
                break
    promotions = [
        "20% off on weekend rentals!",
        "Free GPS with every SUV rental.",
        "Book for 7 days, pay for 6!"
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured_vehicles,
                           promotions=promotions)


@app.route('/vehicles')
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()

    filters = {
        'locations': sorted(list(set([loc['city'] for loc in locations]))),
        'vehicle_types': ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
    }

    selected_location = request.args.get('location')
    if selected_location not in filters['locations']:
        selected_location = None
    selected_vehicle_type = request.args.get('vehicle_type')
    if selected_vehicle_type not in filters['vehicle_types']:
        selected_vehicle_type = None
    selected_date_range = request.args.get('date_range')
    if selected_date_range is not None and selected_date_range.strip() == '':
        selected_date_range = None

    filtered_vehicles = []
    for v in vehicles:
        if selected_vehicle_type and v['vehicle_type'] != selected_vehicle_type:
            continue
        # Note: location and date range filters might need extra logic, but data schema limited
        # We'll assume filtering based on location means available vehicles at that city location
        if selected_location:
            locs = [loc['city'] for loc in locations if loc['available_vehicles'] > 0]
            if selected_location not in locs:
                continue
        filtered_vehicles.append({
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'vehicle_type': v['vehicle_type'],
            'daily_rate': v['daily_rate'],
            'seats': v['seats']
        })

    return render_template('vehicle_search.html',
                           vehicles=filtered_vehicles,
                           filters=filters,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           selected_date_range=selected_date_range)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        return "Vehicle not found", 404

    # No reviews data file specified, so empty list
    reviews = []

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        return "Vehicle not found", 404

    locations = read_locations()
    pickup_locations = [loc['city'] for loc in locations]
    dropoff_locations = pickup_locations.copy()

    total_price = None
    booking_form_data = {}

    if request.method == 'POST':
        # Extract form data
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        booking_form_data = {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }

        # Validate dates and calculate price
        try:
            if not pickup_date or not dropoff_date:
                raise ValueError('Pickup and dropoff dates required')
            dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
            dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dt_dropoff < dt_pickup:
                raise ValueError('Dropoff date must be after pickup date')
            duration = (dt_dropoff - dt_pickup).days + 1  # inclusive
            total_price = round(duration * vehicle['daily_rate'], 2)
        except Exception:
            total_price = None

    return render_template('booking.html', vehicle=vehicle, pickup_locations=pickup_locations,
                           dropoff_locations=dropoff_locations, total_price=total_price, booking_form_data=booking_form_data)


@app.route('/insurance/<int:booking_id>', methods=['GET', 'POST'])
def insurance_options_page(booking_id):
    insurance_plans = read_insurance_plans()
    selected_insurance_id = None

    if request.method == 'POST':
        try:
            selected_insurance_id = int(request.form.get('insurance_id'))
        except Exception:
            selected_insurance_id = None

        # Here would be logic to confirm booking with insurance - outside spec
        # Just reload page with selection

    return render_template('insurance_options.html',
                           insurance_plans=insurance_plans,
                           selected_insurance_id=selected_insurance_id,
                           booking_id=booking_id)


@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()

    status_filter = request.args.get('status_filter', '')

    # Compose list with vehicle name strings
    def vehicle_name(v_id):
        v = next((v for v in vehicles if v['vehicle_id'] == v_id), None)
        if v:
            return f"{v['make']} {v['model']}"
        return 'Unknown'

    filtered_rentals = []
    for rental in rentals:
        if status_filter and rental['status'].lower() != status_filter.lower():
            continue
        filtered_rentals.append({
            'rental_id': rental['rental_id'],
            'vehicle': vehicle_name(rental['vehicle_id']),
            'pickup_date': rental['pickup_date'],
            'dropoff_date': rental['dropoff_date'],
            'pickup_location': rental['pickup_location'],
            'dropoff_location': rental['dropoff_location'],
            'status': rental['status']
        })

    return render_template('rental_history.html', rentals=filtered_rentals, status_filter=status_filter)


@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    vehicles = read_vehicles()

    # Compose reservation list with vehicle names
    def vehicle_name(v_id):
        v = next((v for v in vehicles if v['vehicle_id'] == v_id), None)
        if v:
            return f"{v['make']} {v['model']}"
        return 'Unknown'

    filter_date_sorted = False

    if request.method == 'POST':
        # Possibly sorting or filtering, specification does not give detailed POST fields
        # We implement an example: if sort_by_date parameter sent
        sort_by_date = request.form.get('sort_by_date')
        if sort_by_date == 'true':
            filter_date_sorted = True

    reservations_list = []
    for r in reservations:
        reservations_list.append({
            'reservation_id': r['reservation_id'],
            'vehicle': vehicle_name(r['vehicle_id']),
            'pickup_date': '',  # rentals.txt link needed to fill; spec not clear
            'dropoff_date': '', # rentals.txt link needed to fill; spec not clear
            'status': r['status']
        })

    # To include pickup/dropoff dates, try to link rental data
    rentals = read_rentals()
    rid_map = {r['rental_id']: r for r in rentals}
    for res in reservations_list:
        orig_res = next((r for r in reservations if r['reservation_id'] == res['reservation_id']), None)
        if orig_res and orig_res['rental_id'] in rid_map:
            rental = rid_map[orig_res['rental_id']]
            res['pickup_date'] = rental['pickup_date']
            res['dropoff_date'] = rental['dropoff_date']

    if filter_date_sorted:
        reservations_list.sort(key=lambda x: (x['pickup_date'], x['dropoff_date']))

    return render_template('reservation_management.html',
                           reservations=reservations_list,
                           filter_date_sorted=filter_date_sorted)


@app.route('/reservation/modify/<int:reservation_id>', methods=['POST'])
def modify_reservation(reservation_id):
    reservations = read_reservations()

    modification_data = dict(request.form)
    # Find reservation
    mod_res = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if mod_res is None:
        return f"Reservation {reservation_id} not found", 404

    # Apply modification - spec does not specify fields to modify, try generic special_requests update
    special_requests = modification_data.get('special_requests')
    if special_requests is not None:
        mod_res['special_requests'] = special_requests

    # Could update status or insurance_id if passed
    status = modification_data.get('status')
    if status is not None:
        mod_res['status'] = status

    insurance_id = modification_data.get('insurance_id')
    if insurance_id is not None:
        try:
            mod_res['insurance_id'] = int(insurance_id)
        except Exception:
            pass

    success = write_reservations(reservations)
    if not success:
        return "Failed to save modification", 500

    return "Modification applied successfully"


@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()

    res = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if res is None:
        return f"Reservation {reservation_id} not found", 404

    res['status'] = 'Cancelled'

    success = write_reservations(reservations)
    if not success:
        return "Failed to save cancellation", 500

    cancellation_confirmation = f"Reservation {reservation_id} has been cancelled."
    return cancellation_confirmation


@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    vehicles = read_vehicles()

    def vehicle_name(v_id):
        v = next((v for v in vehicles if v['vehicle_id'] == v_id), None)
        if v:
            return f"{v['make']} {v['model']}"
        return 'Unknown'

    reservations_list = []
    for r in reservations:
        reservations_list.append({
            'reservation_id': r['reservation_id'],
            'vehicle': vehicle_name(r['vehicle_id']),
            'pickup_date': '',
            'dropoff_date': '',
            'status': r['status']
        })

    # Link rentals for dates
    rentals = read_rentals()
    rid_map = {r['rental_id']: r for r in rentals}
    for res in reservations_list:
        orig_res = next((r for r in reservations if r['reservation_id'] == res['reservation_id']), None)
        if orig_res and orig_res['rental_id'] in rid_map:
            rental = rid_map[orig_res['rental_id']]
            res['pickup_date'] = rental['pickup_date']
            res['dropoff_date'] = rental['dropoff_date']

    form_data = {}
    if request.method == 'POST':
        form_data = {
            'selected_reservation': request.form.get('selected_reservation'),
            'driver_assistance': request.form.get('driver_assistance') == 'on',
            'gps_option': request.form.get('gps_option') == 'on',
            'child_seat_quantity': request.form.get('child_seat_quantity', '0'),
            'special_notes': request.form.get('special_notes')
        }

    return render_template('special_requests.html',
                           reservations=reservations_list,
                           form_data=form_data)


@app.route('/locations')
def locations_page():
    locations = read_locations()

    filter_hours = request.args.get('filter_hours', '')
    search_query = request.args.get('search_query', '').lower()

    filtered_locations = []
    for loc in locations:
        if filter_hours and loc['hours'] != filter_hours:
            continue
        if search_query and search_query not in loc['city'].lower() and search_query not in loc['address'].lower():
            continue
        filtered_locations.append(loc)

    return render_template('locations.html',
                           locations=filtered_locations,
                           filter_hours=filter_hours,
                           search_query=request.args.get('search_query', ''))


if __name__ == '__main__':
    app.run(debug=True)
