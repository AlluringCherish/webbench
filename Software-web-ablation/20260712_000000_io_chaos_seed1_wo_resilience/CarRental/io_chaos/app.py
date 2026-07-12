from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load and save data

def load_vehicles():
    vehicles = []
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
        pass
    return vehicles


def load_customers():
    customers = []
    try:
        with open(os.path.join(DATA_DIR, 'customers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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
        pass
    return customers


def load_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
        pass
    return locations


def load_rentals():
    rentals = []
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
        pass
    return rentals


def load_insurance():
    plans = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                plans.append(plan)
    except Exception:
        pass
    return plans


def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
        pass
    return reservations


def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = '|'.join([
                    str(r['reservation_id']),
                    str(r['rental_id']),
                    str(r['vehicle_id']),
                    str(r['customer_id']),
                    r['status'],
                    str(r['insurance_id']),
                    r['special_requests']
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def save_rentals(rentals):
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w', encoding='utf-8') as f:
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
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def save_customers(customers):
    try:
        with open(os.path.join(DATA_DIR, 'customers.txt'), 'w', encoding='utf-8') as f:
            for c in customers:
                line = '|'.join([
                    str(c['customer_id']),
                    c['name'],
                    c['email'],
                    c['phone'],
                    c['driver_license'],
                    c['license_expiry']
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def save_vehicles(vehicles):
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'w', encoding='utf-8') as f:
            for v in vehicles:
                line = '|'.join([
                    str(v['vehicle_id']),
                    v['make'],
                    v['model'],
                    v['vehicle_type'],
                    f"{v['daily_rate']:.2f}",
                    str(v['seats']),
                    v['transmission'],
                    v['fuel_type'],
                    v['status']
                ]) + '\n'
                f.write(line)
    except Exception:
        pass


def save_locations(locations):
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'w', encoding='utf-8') as f:
            for l in locations:
                line = '|'.join([
                    str(l['location_id']),
                    l['city'],
                    l['address'],
                    l['phone'],
                    l['hours'],
                    str(l['available_vehicles'])
                ]) + '\n'
                f.write(line)
    except Exception:
        pass

# Helper to find max id in list of dict

def max_id(items, key):
    if not items:
        return 0
    return max(item[key] for item in items)


# ==================== Flask route implementations ====================

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Load vehicles and promotions
    vehicles = load_vehicles()
    # Featured vehicles with daily_rate <= 100 for example
    featured_vehicles = [
        {
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'daily_rate': v['daily_rate']
        }
        for v in vehicles if v['status'] == 'Available' and v['daily_rate'] <= 100
    ][:5]  # limit to 5 featured

    # Promotions - static example or from a file, here static
    promotions = [
        "Spring Sale - 20% off all rentals!",
        "Weekend Special - Rent 3 days, pay for 2!"
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/vehicles')
def vehicle_search():
    # Load data
    vehicles = load_vehicles()
    locations = list(set(loc['city'] for loc in load_locations()))
    vehicle_types = list(set(v['vehicle_type'] for v in vehicles))
    vehicles_display = vehicles

    # Allow filtering by location and vehicle_type via query parameters
    location_filter = request.args.get('location')
    vehicle_type_filter = request.args.get('vehicle_type')

    if location_filter:
        # Filter vehicles that are available in that location
        # We treat vehicle availability just by status Available for now (no mapping location<->vehicle)
        vehicles_display = [v for v in vehicles_display if v['status'] == 'Available']
        # To simulate location filtering, assume all vehicles available at all locations
    if vehicle_type_filter:
        vehicles_display = [v for v in vehicles_display if v['vehicle_type'] == vehicle_type_filter]

    return render_template('vehicle_search.html', locations=locations, vehicle_types=vehicle_types, vehicles=vehicles_display)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)

    # For reviews, simulate with static data
    reviews = [
        {'reviewer': 'John Doe', 'comment': 'Great car, smooth ride!'},
        {'reviewer': 'Jane Smith', 'comment': 'Comfortable and fuel efficient.'}
    ]

    if not vehicle:
        return "Vehicle not found", 404

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicles = load_vehicles()
    locations = list(set(loc['city'] for loc in load_locations()))
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    total_price = None
    booking_form = None

    if not vehicle:
        return "Vehicle not found", 404

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        booking_form = {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }

        # Validate input
        error = None
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            error = 'All fields are required.'
        else:
            try:
                dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                if dt_pickup > dt_dropoff:
                    error = 'Dropoff date must be after pickup date.'
            except ValueError:
                error = 'Invalid date format.'

        if error:
            total_price = None
        else:
            # Calculate total price: daily_rate * days
            days = (dt_dropoff - dt_pickup).days + 1
            total_price = round(vehicle['daily_rate'] * days, 2)

            # We do not save booking here, reservation is created after insurance confirmation

    return render_template('booking.html', vehicle_id=vehicle_id, locations=locations, total_price=total_price, booking_form=booking_form)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = load_insurance()
    selected_insurance_id = None

    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        return "Reservation not found", 404

    if request.method == 'POST':
        insurance_id_str = request.form.get('insurance_id')
        if insurance_id_str and insurance_id_str.isdigit():
            selected_insurance_id = int(insurance_id_str)
            # Update reservation insurance_id
            reservation['insurance_id'] = selected_insurance_id
            # Change status to Confirmed or similar
            reservation['status'] = 'Confirmed'
            save_reservations(reservations)
        else:
            selected_insurance_id = None

    else:
        selected_insurance_id = reservation['insurance_id'] if reservation['insurance_id'] != 0 else None

    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance_id=selected_insurance_id, reservation_id=reservation_id)


@app.route('/history')
def rental_history():
    rentals = load_rentals()
    status_filter = request.args.get('status', '')

    if status_filter:
        rentals = [r for r in rentals if r['status'].lower() == status_filter.lower()]

    return render_template('rental_history.html', rentals=rentals, status_filter=status_filter)


@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = load_reservations()
    rentals = load_rentals()
    vehicles = load_vehicles()

    if request.method == 'POST':
        # Handling modifying or cancelling reservation
        action = request.form.get('action')
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str or not reservation_id_str.isdigit():
            return redirect(url_for('reservation_management'))
        reservation_id = int(reservation_id_str)

        reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
        if not reservation:
            return redirect(url_for('reservation_management'))

        if action == 'modify':
            # Example modification: change status
            new_status = request.form.get('new_status')
            if new_status:
                reservation['status'] = new_status
                save_reservations(reservations)
        elif action == 'cancel':
            reservation['status'] = 'Cancelled'
            save_reservations(reservations)

    return render_template('reservations.html', reservations=reservations)


@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = load_reservations()
    submitted = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        child_seat_qty_str = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes', '')

        if reservation_id_str and reservation_id_str.isdigit():
            reservation_id = int(reservation_id_str)
            reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
            if reservation:
                # Compose special requests string
                requests = []
                if driver_assistance:
                    requests.append('Driver assistance requested')
                if gps_option:
                    requests.append('GPS requested')
                if child_seat_qty_str and child_seat_qty_str.isdigit():
                    qty = int(child_seat_qty_str)
                    if qty > 0:
                        requests.append(f'Child seat quantity: {qty}')
                if special_notes:
                    requests.append(f'Notes: {special_notes}')

                reservation['special_requests'] = '; '.join(requests)
                save_reservations(reservations)
                submitted = True
        else:
            submitted = False

    return render_template('special_requests.html', reservations=reservations, submitted=submitted)


@app.route('/locations')
def locations_page():
    locations = load_locations()

    # Filtering by hours (query param)
    hours_filter = request.args.get('hours')
    search_location = request.args.get('search')

    filtered_locations = locations
    if hours_filter:
        filtered_locations = [l for l in filtered_locations if l['hours'] == hours_filter]
    if search_location:
        filtered_locations = [l for l in filtered_locations if search_location.lower() in l['city'].lower() or search_location.lower() in l['address'].lower()]

    return render_template('locations.html', locations=filtered_locations)


if __name__ == '__main__':
    app.run(debug=True)
