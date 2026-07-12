from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for reading and writing pipe-delimited files with schema handling

def read_vehicles():
    vehicles = []
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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

def read_customers():
    customers = []
    path = os.path.join(DATA_DIR, 'customers.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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

def read_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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

def read_rentals():
    rentals = []
    path = os.path.join(DATA_DIR, 'rentals.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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

def read_insurance():
    insurance_plans = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        pass
    return insurance_plans

def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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

def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'w') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}"
                f.write(line + '\n')
    except Exception:
        pass

# Utilities

def calculate_rental_days(pickup_date_str, dropoff_date_str):
    try:
        pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
        dropoff_date = datetime.strptime(dropoff_date_str, '%Y-%m-%d')
        delta = dropoff_date - pickup_date
        return max(delta.days, 0)
    except Exception:
        return 0

# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    # For featured_vehicles - assume those with status 'Available' limited to first 5
    featured_vehicles = []
    for v in vehicles:
        if v['status'] == 'Available':
            featured_vehicles.append({
                'vehicle_id': v['vehicle_id'],
                'make': v['make'],
                'model': v['model'],
                'daily_rate': v['daily_rate'],
            })
            if len(featured_vehicles) >= 5:
                break

    promotions = [
        '20% off for weekend rentals',
        'Free GPS for rentals over 3 days',
        'Loyalty program benefits available'
    ]

    return render_template('dashboard.html',
                           featured_vehicles=featured_vehicles,
                           promotions=promotions)

@app.route('/vehicles')
def vehicle_search():
    vehicles = read_vehicles()
    locations = sorted(set(loc['city'] for loc in read_locations()))
    vehicle_types = ["Economy", "Compact", "Sedan", "SUV", "Luxury"]
    # No specific filters implemented, show all vehicles
    vehicles_brief = []
    for v in vehicles:
        vehicles_brief.append({
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'vehicle_type': v['vehicle_type'],
            'daily_rate': v['daily_rate']
        })
    return render_template('vehicle_search.html',
                           locations=locations,
                           vehicle_types=vehicle_types,
                           vehicles=vehicles_brief)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)

    # Placeholder for reviews (since no reviews.txt given), using dummy
    reviews = [
        {'reviewer': 'John Doe', 'rating': 5, 'comment': 'Excellent car!'},
        {'reviewer': 'Jane Smith', 'rating': 4, 'comment': 'Very comfortable and smooth ride.'}
    ]

    if vehicle is None:
        return "Vehicle not found", 404

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking', methods=['GET', 'POST'])
def booking_page():
    locations = sorted(set(loc['city'] for loc in read_locations()))
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')

        # Form validation
        errors = []
        if pickup_location == '':
            errors.append('Pickup location is required')
        if dropoff_location == '':
            errors.append('Dropoff location is required')
        if pickup_date == '':
            errors.append('Pickup date is required')
        if dropoff_date == '':
            errors.append('Dropoff date is required')

        # Calculate rental days and price if no errors
        total_price = 0.0
        if not errors:
            days = calculate_rental_days(pickup_date, dropoff_date)
            if days <= 0:
                errors.append('Dropoff date must be after pickup date')

            # For price calculation, we just pick the first available vehicle daily_rate for demo
            vehicles = read_vehicles()
            if vehicles:
                daily_rate = vehicles[0]['daily_rate']
                total_price = daily_rate * days

        if errors:
            # Re-render with errors and previously submitted data
            return render_template('booking.html', locations=locations,
                                   pickup_location=pickup_location,
                                   dropoff_location=dropoff_location,
                                   pickup_date=pickup_date,
                                   dropoff_date=dropoff_date,
                                   total_price=0.0,
                                   errors=errors)

        return render_template('booking.html',
                               locations=locations,
                               pickup_location=pickup_location,
                               dropoff_location=dropoff_location,
                               pickup_date=pickup_date,
                               dropoff_date=dropoff_date,
                               total_price=total_price)

    # GET method
    return render_template('booking.html', locations=locations)

@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options():
    insurance_plans = read_insurance()
    selected_insurance = None
    if request.method == 'POST':
        selected_id = request.form.get('insurance_id')
        if selected_id and selected_id.isdigit():
            selected_id = int(selected_id)
            selected_insurance = next((plan for plan in insurance_plans if plan['insurance_id'] == selected_id), None)
    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance)

@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    status_filter = request.args.get('status_filter', '')
    if status_filter:
        filtered = [r for r in rentals if r['status'].lower() == status_filter.lower()]
    else:
        filtered = rentals
    return render_template('rental_history.html', rentals=filtered, status_filter=status_filter)

@app.route('/reservations')
def reservation_management():
    reservations = read_reservations()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reservation/modify/<int:reservation_id>', methods=['POST'])
def modify_reservation(reservation_id):
    reservations = read_reservations()
    # Find reservation to modify
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        return redirect(url_for('reservation_management'))

    # Expected modification details from form
    # For example: form keys like 'status', 'insurance_id', 'special_requests'
    status = request.form.get('status', reservation['status'])
    insurance_id = request.form.get('insurance_id', reservation['insurance_id'])
    special_requests = request.form.get('special_requests', reservation['special_requests'])

    # Validate insurance_id as int
    try:
        insurance_id = int(insurance_id)
    except Exception:
        insurance_id = reservation['insurance_id']

    # Update data
    reservation['status'] = status
    reservation['insurance_id'] = insurance_id
    reservation['special_requests'] = special_requests

    # Write back updated reservations
    write_reservations(reservations)

    return redirect(url_for('reservation_management'))

@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    # Find reservation
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        return redirect(url_for('reservation_management'))

    # Mark status as Cancelled
    reservation['status'] = 'Cancelled'

    write_reservations(reservations)

    return redirect(url_for('reservation_management'))

@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()

    if request.method == 'POST':
        try:
            selected_reservation_id = int(request.form.get('selected_reservation_id', 0))
        except Exception:
            selected_reservation_id = 0

        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        try:
            child_seats = int(request.form.get('child_seats', 0))
        except Exception:
            child_seats = 0
        special_notes = request.form.get('special_notes', '')

        # Find reservation to update
        reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
        if reservation:
            # Build special_requests string
            requests_list = []
            if driver_assistance:
                requests_list.append('Driver assistance requested')
            if gps_option:
                requests_list.append('GPS option requested')
            if child_seats > 0:
                requests_list.append(f'Child seats: {child_seats}')
            if special_notes.strip():
                requests_list.append(special_notes.strip())

            combined_requests = '; '.join(requests_list)
            reservation['special_requests'] = combined_requests

            write_reservations(reservations)

        return render_template('special_requests.html',
                               reservations=reservations,
                               selected_reservation_id=selected_reservation_id,
                               driver_assistance=driver_assistance,
                               gps_option=gps_option,
                               child_seats=child_seats,
                               special_notes=special_notes)

    # GET
    return render_template('special_requests.html', reservations=reservations)

@app.route('/locations')
def locations():
    locations = read_locations()
    return render_template('locations.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
