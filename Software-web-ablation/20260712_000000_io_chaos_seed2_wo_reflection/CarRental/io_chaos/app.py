from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Constants for data file paths
DATA_DIR = 'data'
VEHICLES_FILE = os.path.join(DATA_DIR, 'vehicles.txt')
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.txt')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.txt')
RENTALS_FILE = os.path.join(DATA_DIR, 'rentals.txt')
INSURANCE_FILE = os.path.join(DATA_DIR, 'insurance.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')

# Helper functions to read/write pipe delimited files

def read_vehicles():
    vehicles = []
    if not os.path.exists(VEHICLES_FILE):
        return vehicles
    with open(VEHICLES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
                    'status': parts[8]
                }
                vehicles.append(vehicle)
            except ValueError:
                continue
    return vehicles


def read_customers():
    customers = []
    if not os.path.exists(CUSTOMERS_FILE):
        return customers
    with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                customer = {
                    'customer_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'driver_license': parts[4],
                    'license_expiry': parts[5]  # YYYY-MM-DD
                }
                customers.append(customer)
            except ValueError:
                continue
    return customers


def read_locations():
    locations = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                location = {
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                }
                locations.append(location)
            except ValueError:
                continue
    return locations


def read_rentals():
    rentals = []
    if not os.path.exists(RENTALS_FILE):
        return rentals
    with open(RENTALS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
                    'status': parts[8]
                }
                rentals.append(rental)
            except ValueError:
                continue
    return rentals


def read_insurance_plans():
    plans = []
    if not os.path.exists(INSURANCE_FILE):
        return plans
    with open(INSURANCE_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                # coverage_limit can be int or str
                try:
                    coverage = int(parts[4])
                except ValueError:
                    coverage = parts[4]
                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': coverage,
                    'deductible': int(parts[5])
                }
                plans.append(plan)
            except ValueError:
                continue
    return plans


def read_reservations():
    reservations = []
    if not os.path.exists(RESERVATIONS_FILE):
        return reservations
    with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
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
                    'special_requests': parts[6]
                }
                reservations.append(reservation)
            except ValueError:
                continue
    return reservations


def write_vehicles(vehicles):
    try:
        with open(VEHICLES_FILE, 'w', encoding='utf-8') as f:
            for v in vehicles:
                line = f"{v['vehicle_id']}|{v['make']}|{v['model']}|{v['vehicle_type']}|{v['daily_rate']:.2f}|{v['seats']}|{v['transmission']}|{v['fuel_type']}|{v['status']}\n"
                f.write(line)
    except Exception:
        pass


def write_reservations(reservations):
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass


def write_rentals(rentals):
    try:
        with open(RENTALS_FILE, 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']:.2f}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper to find vehicle by id

def find_vehicle(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None

# Helper to find insurance plan by id

def find_insurance(insurance_id):
    plans = read_insurance_plans()
    for p in plans:
        if p['insurance_id'] == insurance_id:
            return p
    return None

# Helper to find reservation by id

def find_reservation(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None

# Helper to find rental by id

def find_rental(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None


# Route: / redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Route: /dashboard
@app.route('/dashboard')
def dashboard_page():
    vehicles = read_vehicles()
    # A simple logic for featured vehicles: first 4 available vehicles
    featured_vehicles = [
        {'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']}
        for v in vehicles if v['status'].lower() == 'available'][:4]
    # Placeholder promotions
    promotions = [
        'Winter Sale: 20% off on all SUVs!',
        'Book early and save 15% on luxury vehicles!',
        'Weekend special: Rent 3 days get 1 free'
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


# Route: /vehicles
@app.route('/vehicles')
def vehicle_search_page():
    vehicles = read_vehicles()
    # Only available vehicles
    vehicles = [v for v in vehicles if v['status'].lower() == 'available']
    locations = list({loc['city'] for loc in read_locations()})
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
    return render_template('vehicle_search.html', vehicles=vehicles, locations=locations, vehicle_types=vehicle_types)

# Route: /vehicles/<int:vehicle_id>
@app.route('/vehicles/<int:vehicle_id>')
def vehicle_details_page(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404
    # For simplicity, no reviews file - we return dummy reviews list (empty or static)
    reviews = [
        "Great car, very comfortable!",
        "Smooth drive and good on fuel.",
        "Would rent again."
    ]
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


# Route: /vehicles/<int:vehicle_id>/book (GET, POST)
@app.route('/vehicles/<int:vehicle_id>/book', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle or vehicle['status'].lower() != 'available':
        return "Vehicle not available for booking", 400

    locations = list({loc['city'] for loc in read_locations()})

    pickup_date = None
    dropoff_date = None
    total_price = None

    if request.method == 'POST':
        # Get form data
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        dropoff_date = request.form.get('dropoff_date', '').strip()

        # Validate required fields
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, error='All fields are required.')

        # Validate date format
        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dropoff_dt < pickup_dt:
                return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, error='Dropoff date must be after pickup date.')
        except ValueError:
            return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, error='Invalid date format.')

        # Calculate days and price
        days = (dropoff_dt - pickup_dt).days + 1
        total_price = round(days * vehicle['daily_rate'], 2)

        # Render page with total price (simulate calculation before final booking on insurance step)
        return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price)

    return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=None, dropoff_date=None, total_price=None)


# Route: /insurance (GET, POST)
@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options_page():
    insurance_plans = read_insurance_plans()
    selected_insurance = None

    if request.method == 'POST':
        insurance_id_str = request.form.get('insurance_id')
        if insurance_id_str:
            try:
                insurance_id = int(insurance_id_str)
                selected_insurance = find_insurance(insurance_id)
                if not selected_insurance:
                    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=None, error='Selected insurance plan not found.')
            except ValueError:
                return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=None, error='Invalid insurance selection.')
            # After confirming booking, logic to finalize booking might go here
            # Since no details provided, just render page with selected insurance
            return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance, success='Booking confirmed with selected insurance.')

        else:
            return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=None, error='No insurance plan selected.')

    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=None)


# Route: /rentals/history (GET)
@app.route('/rentals/history')
def rental_history_page():
    rentals = read_rentals()
    filter_status = request.args.get('status', 'All')

    if filter_status != 'All':
        rentals = [r for r in rentals if r['status'] == filter_status]

    return render_template('rental_history.html', rentals=rentals, filter_status=filter_status)


# Route: /reservations (GET, POST)
@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management_page():
    reservations = read_reservations()

    if request.method == 'POST':
        # Expect form fields for modify or cancel
        action = request.form.get('action')
        reservation_id_str = request.form.get('reservation_id')

        if not reservation_id_str or not action:
            return render_template('reservations.html', reservations=reservations, error='Reservation ID and action required.')
        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            return render_template('reservations.html', reservations=reservations, error='Invalid reservation ID.')

        reservation = find_reservation(reservation_id)
        if not reservation:
            return render_template('reservations.html', reservations=reservations, error='Reservation not found.')

        if action == 'modify':
            # Modify logic: just toggling status between Confirmed and Active for demo
            if reservation['status'] == 'Confirmed':
                reservation['status'] = 'Active'
            else:
                reservation['status'] = 'Confirmed'
            all_reservations = read_reservations()
            # Update record
            for i, r in enumerate(all_reservations):
                if r['reservation_id'] == reservation_id:
                    all_reservations[i] = reservation
                    break
            write_reservations(all_reservations)
            reservations = all_reservations
            return render_template('reservations.html', reservations=reservations, success='Reservation modified.')
        elif action == 'cancel':
            # Cancel reservation: set status to 'Cancelled'
            reservation['status'] = 'Cancelled'
            all_reservations = read_reservations()
            for i, r in enumerate(all_reservations):
                if r['reservation_id'] == reservation_id:
                    all_reservations[i] = reservation
                    break
            write_reservations(all_reservations)
            reservations = all_reservations
            return render_template('reservations.html', reservations=reservations, success='Reservation cancelled.')
        else:
            return render_template('reservations.html', reservations=reservations, error='Unknown action.')

    return render_template('reservations.html', reservations=reservations)


# Route: /special-requests (GET, POST)
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests_page():
    reservations = read_reservations()
    special_requests_form_data = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance_checkbox')
        gps_option = request.form.get('gps_option_checkbox')
        child_seat_quantity = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes', '').strip()

        if not reservation_id_str:
            return render_template('special_requests.html', reservations=reservations, special_requests_form_data=None, error='Reservation selection required.')
        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            return render_template('special_requests.html', reservations=reservations, special_requests_form_data=None, error='Invalid reservation selected.')

        # Compose special requests string
        requests_list = []
        if driver_assistance == 'on':
            requests_list.append('Driver assistance requested')
        if gps_option == 'on':
            requests_list.append('GPS option requested')
        try:
            cs_qty = int(child_seat_quantity) if child_seat_quantity else 0
            if cs_qty > 0:
                requests_list.append(f'{cs_qty} child seat(s)')
        except ValueError:
            return render_template('special_requests.html', reservations=reservations, special_requests_form_data=request.form, error='Invalid child seat quantity.')

        if special_notes:
            requests_list.append(f'Notes: {special_notes}')

        # Update the reservation's special_requests field
        reservation = find_reservation(reservation_id)
        if not reservation:
            return render_template('special_requests.html', reservations=reservations, special_requests_form_data=request.form, error='Reservation not found.')

        reservation['special_requests'] = '; '.join(requests_list) if requests_list else ''

        all_reservations = read_reservations()
        for i, r in enumerate(all_reservations):
            if r['reservation_id'] == reservation_id:
                all_reservations[i] = reservation
                break
        write_reservations(all_reservations)
        reservations = all_reservations
        return render_template('special_requests.html', reservations=reservations, special_requests_form_data=None, success='Special requests updated.')

    return render_template('special_requests.html', reservations=reservations, special_requests_form_data=None)


# Route: /locations
@app.route('/locations')
def locations_page():
    locations = read_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
