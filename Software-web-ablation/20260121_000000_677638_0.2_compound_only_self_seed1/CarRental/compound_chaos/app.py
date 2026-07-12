from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read each data file according to the specification

def read_vehicles():
    vehicles = []
    filepath = os.path.join(DATA_DIR, 'vehicles.txt')
    if not os.path.exists(filepath):
        return vehicles
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            try:
                vehicle = {
                    'vehicle_id': int(parts[0]),
                    'make': parts[1],
                    'model': parts[2],
                    'vehicle_type': parts[3],
                    'daily_rate': float(parts[4]),
                    'seats': int(parts[5]),
                    'transmission': parts[6],
                    'fuel_type': parts[7],
                    'status': parts[8],
                }
                vehicles.append(vehicle)
            except (ValueError, IndexError):
                continue
    return vehicles


def read_customers():
    customers = []
    filepath = os.path.join(DATA_DIR, 'customers.txt')
    if not os.path.exists(filepath):
        return customers
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                customer = {
                    'customer_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'driver_license': parts[4],
                    'license_expiry': parts[5],
                }
                customers.append(customer)
            except (ValueError, IndexError):
                continue
    return customers


def read_locations():
    locations = []
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(filepath):
        return locations
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                location = {
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5]),
                }
                locations.append(location)
            except (ValueError, IndexError):
                continue
    return locations


def read_rentals():
    rentals = []
    filepath = os.path.join(DATA_DIR, 'rentals.txt')
    if not os.path.exists(filepath):
        return rentals
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            try:
                rental = {
                    'rental_id': int(parts[0]),
                    'vehicle_id': int(parts[1]),
                    'customer_id': int(parts[2]),
                    'pickup_date': parts[3],
                    'dropoff_date': parts[4],
                    'pickup_location': parts[5],
                    'dropoff_location': parts[6],
                    'total_price': float(parts[7]),
                    'status': parts[8],
                }
                rentals.append(rental)
            except (ValueError, IndexError):
                continue
    return rentals


def read_insurance_plans():
    insurance_plans = []
    filepath = os.path.join(DATA_DIR, 'insurance.txt')
    if not os.path.exists(filepath):
        return insurance_plans
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': int(parts[5]),
                }
                insurance_plans.append(plan)
            except (ValueError, IndexError):
                continue
    return insurance_plans


def read_reservations():
    reservations = []
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(filepath):
        return reservations
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                reservation = {
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6],
                }
                reservations.append(reservation)
            except (ValueError, IndexError):
                continue
    return reservations

# Utility to write reservations file (for POST actions that update reservations)
def write_reservations(reservations):
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}"
                f.write(line + '\n')
    except IOError:
        pass

# Utility to write rentals file (for POST actions that add rentals)
def write_rentals(rentals):
    filepath = os.path.join(DATA_DIR, 'rentals.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}"
                f.write(line + '\n')
    except IOError:
        pass

# Utility to write vehicles file (e.g. to update vehicle status)
def write_vehicles(vehicles):
    filepath = os.path.join(DATA_DIR, 'vehicles.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for v in vehicles:
                line = f"{v['vehicle_id']}|{v['make']}|{v['model']}|{v['vehicle_type']}|{v['daily_rate']}|{v['seats']}|{v['transmission']}|{v['fuel_type']}|{v['status']}"
                f.write(line + '\n')
    except IOError:
        pass

# Utility to write a new rental - needs to generate new rental_id
# Returns new rental_id
# For simplicity, append to file and in-memory update
# This function is NOT used for updates on rentals - only creation

def add_rental(new_rental):
    rentals = read_rentals()
    max_id = max((r['rental_id'] for r in rentals), default=0)
    new_rental_id = max_id + 1
    new_rental['rental_id'] = new_rental_id
    rentals.append(new_rental)
    write_rentals(rentals)
    return new_rental_id

# Utility to write a new reservation - generates new reservation_id
# Returns new reservation_id

def add_reservation(new_reservation):
    reservations = read_reservations()
    max_id = max((r['reservation_id'] for r in reservations), default=0)
    new_reservation_id = max_id + 1
    new_reservation['reservation_id'] = new_reservation_id
    reservations.append(new_reservation)
    write_reservations(reservations)
    return new_reservation_id

# Convenience function to get vehicle by id

def get_vehicle_by_id(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None

# Convenience function to get insurance plan by id

def get_insurance_by_id(insurance_id):
    plans = read_insurance_plans()
    for plan in plans:
        if plan['insurance_id'] == insurance_id:
            return plan
    return None

# Convenience function to get reservation by id

def get_reservation_by_id(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None

# Convenience function to get rental by id

def get_rental_by_id(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None


# Route: /
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard_page'))


# Route: /dashboard (GET)
@app.route('/dashboard')
def dashboard_page():
    # featured_vehicles: list of dict
    # promotions: list of dict
    # For promotions if no file is specified, we provide a simple static sample

    vehicles = read_vehicles()
    # featured vehicles: pick first 5 available vehicles
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:5]

    # promotions - as no file, static inline examples
    promotions = [
        {'title': 'Winter Special', 'description': 'Save 20% on SUVs this January!'},
        {'title': 'Weekend Deal', 'description': 'Book a 3-day rental, get 1 day free!'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


# Route: /search-vehicles (GET)
@app.route('/search-vehicles')
def search_vehicles_page():
    # locations: list[str], vehicle_types: list[str], vehicles: list[dict]

    vehicles = read_vehicles()
    locations_data = read_locations()
    locations = list(sorted(set(loc['city'] for loc in locations_data)))
    vehicle_types = list(sorted(set(v['vehicle_type'] for v in vehicles)))

    return render_template('search_vehicles.html', locations=locations, vehicle_types=vehicle_types, vehicles=vehicles)


# Route: /vehicle/<int:vehicle_id> (GET)
@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details_page(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if vehicle is None:
        abort(404)

    reviews = []  # No reviews data source defined
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


# Route: /booking/<int:vehicle_id> (GET, POST)
@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicles = read_vehicles()
    selected_vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            selected_vehicle = v
            break
    if selected_vehicle is None:
        abort(404)

    locations_data = read_locations()
    pickup_locations = [loc['city'] for loc in locations_data]
    dropoff_locations = [loc['city'] for loc in locations_data]

    if request.method == 'GET':
        return render_template('booking.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations, selected_vehicle=selected_vehicle)

    # POST: process booking form - calculate price
    form = request.form
    pickup_date = form.get('pickup_date', '').strip()
    dropoff_date = form.get('dropoff_date', '').strip()
    pickup_location = form.get('pickup_location', '').strip()
    dropoff_location = form.get('dropoff_location', '').strip()

    rental_dates = {'pickup_date': pickup_date, 'dropoff_date': dropoff_date}

    # Validate dates, calculate price
    try:
        pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
        dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
        if dropoff_dt <= pickup_dt:
            calculated_price = 0.0
        else:
            days = (dropoff_dt - pickup_dt).days
            calculated_price = days * selected_vehicle['daily_rate']
    except ValueError:
        calculated_price = 0.0

    return render_template('booking.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations,
                           selected_vehicle=selected_vehicle, rental_dates=rental_dates, calculated_price=calculated_price)


# Route: /insurance/<int:reservation_id> (GET, POST)
@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options_page(reservation_id):
    insurance_plans = read_insurance_plans()
    reservation = get_reservation_by_id(reservation_id)
    if reservation is None:
        abort(404)

    if request.method == 'GET':
        return render_template('insurance.html', insurance_plans=insurance_plans, reservation_id=reservation_id)

    form = request.form
    selected_insurance_id_str = form.get('selected_insurance', '').strip()
    try:
        selected_insurance_id = int(selected_insurance_id_str)
    except ValueError:
        selected_insurance_id = None

    selected_insurance = None
    if selected_insurance_id is not None:
        for plan in insurance_plans:
            if plan['insurance_id'] == selected_insurance_id:
                selected_insurance = plan
                break

    if selected_insurance is None:
        return render_template('insurance.html', insurance_plans=insurance_plans, selected_insurance={}, reservation_id=reservation_id)

    # Update reservation with insurance selection
    reservations = read_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            r['insurance_id'] = selected_insurance_id
            r['status'] = 'Confirmed'
            updated = True
            break

    if updated:
        write_reservations(reservations)

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance, reservation_id=reservation_id)


# Route: /rental-history (GET)
@app.route('/rental-history')
def rental_history_page():
    rentals = read_rentals()
    status_filter_options = ['Completed', 'Active', 'Cancelled']

    return render_template('rental_history.html', rentals=rentals, status_filter_options=status_filter_options)


# Route: /my-reservations (GET, POST)
@app.route('/my-reservations', methods=['GET', 'POST'])
def reservation_management_page():
    reservations = read_reservations()

    if request.method == 'GET':
        return render_template('reservations.html', reservations=reservations)

    form = request.form
    reservation_id_str = form.get('reservation_id', '').strip()
    action = form.get('action', '').strip().lower()

    try:
        reservation_id = int(reservation_id_str)
    except ValueError:
        return render_template('reservations.html', reservations=reservations)  # invalid id silently ignored

    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            if action == 'cancel':
                r['status'] = 'Cancelled'
                updated = True
            elif action == 'modify':
                # No modify fields specified
                updated = False
            break

    if updated:
        write_reservations(reservations)

    return render_template('reservations.html', reservations=reservations)


# Route: /special-requests (GET, POST)
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests_page():
    reservations = read_reservations()

    if request.method == 'GET':
        return render_template('special_requests.html', reservations=reservations)

    form = request.form
    reservation_id_str = form.get('reservation_id', '').strip()
    driver_assistance = form.get('driver_assistance_checkbox')  # 'on' if checked
    gps_option = form.get('gps_option_checkbox')  # 'on' if checked
    child_seat_quantity_str = form.get('child_seat_quantity', '0').strip()
    special_notes = form.get('special_notes', '').strip()

    try:
        reservation_id = int(reservation_id_str)
    except ValueError:
        return render_template('special_requests.html', reservations=reservations, submitted_requests={})

    requests = []
    if driver_assistance == 'on':
        requests.append('Driver assistance requested')
    if gps_option == 'on':
        requests.append('GPS option requested')
    try:
        child_seat_quantity = int(child_seat_quantity_str)
        if child_seat_quantity > 0:
            requests.append(f'Child seats: {child_seat_quantity}')
    except ValueError:
        pass

    if special_notes:
        requests.append(f'Notes: {special_notes}')

    special_requests_str = '; '.join(requests) if requests else ''

    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            r['special_requests'] = special_requests_str
            updated = True
            break

    if updated:
        write_reservations(reservations)

    submitted_requests = {
        'driver_assistance': driver_assistance == 'on',
        'gps_option': gps_option == 'on',
        'child_seat_quantity': child_seat_quantity_str,
        'special_notes': special_notes
    }

    return render_template('special_requests.html', reservations=reservations, submitted_requests=submitted_requests)


# Route: /locations (GET)
@app.route('/locations')
def locations_page():
    locations = read_locations()
    hours_filter_options = ['24/7', '09:00-18:00', 'Weekend']

    return render_template('locations.html', locations=locations, hours_filter_options=hours_filter_options)


if __name__ == '__main__':
    app.run(debug=True)
