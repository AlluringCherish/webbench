from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read data files

def read_vehicles():
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

def read_customers():
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

def read_locations():
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

def read_rentals():
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

def read_insurances():
    insurances = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                insurance = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': int(parts[5])
                }
                insurances.append(insurance)
    except Exception:
        pass
    return insurances

def read_reservations():
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
                    'insurance_id': int(parts[5]) if parts[5].isdigit() else 0,
                    'special_requests': parts[6]
                }
                reservations.append(reservation)
    except Exception:
        pass
    return reservations

def write_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass

def write_rentals(rentals):
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    featured_vehicles = [
        {'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']} 
        for v in vehicles if v['status'].lower() == 'available'
    ]
    featured_vehicles = sorted(featured_vehicles, key=lambda x: x['daily_rate'])[:3]

    promotions = [
        {'title': 'Winter Discount', 'description': 'Get 15% off on all SUVs!'},
        {'title': 'Weekday Special', 'description': 'Rent a car during weekdays and save more.'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

@app.route('/search')
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
    return render_template('search.html', vehicles=vehicles, locations=locations, vehicle_types=vehicle_types)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    reviews = []  # No reviews data provided
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    locations = read_locations()
    booking_form_data = {
        'pickup_location': '',
        'dropoff_location': '',
        'pickup_date': '',
        'dropoff_date': '',
        'total_price': 0.0
    }

    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle or vehicle['status'].lower() != 'available':
        return redirect(url_for('vehicle_search'))

    error = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date_str = request.form.get('pickup_date', '').strip()
        dropoff_date_str = request.form.get('dropoff_date', '').strip()

        booking_form_data['pickup_location'] = pickup_location
        booking_form_data['dropoff_location'] = dropoff_location
        booking_form_data['pickup_date'] = pickup_date_str
        booking_form_data['dropoff_date'] = dropoff_date_str

        location_cities = [loc['city'] for loc in locations]
        if pickup_location not in location_cities or dropoff_location not in location_cities:
            error = 'Invalid pickup or dropoff location.'
        else:
            try:
                pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
                dropoff_date = datetime.strptime(dropoff_date_str, '%Y-%m-%d')
                if pickup_date > dropoff_date:
                    error = 'Dropoff date must be after pickup date.'
            except Exception:
                error = 'Invalid date format. Use YYYY-MM-DD.'

        if not error:
            rental_days = (dropoff_date - pickup_date).days + 1
            total_price = rental_days * vehicle['daily_rate']
            booking_form_data['total_price'] = total_price

    return render_template('booking.html', locations=locations, booking_form_data=booking_form_data)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurances()
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        return redirect(url_for('reservation_management'))

    selected_plan = None

    if request.method == 'POST':
        selected_insurance_id = request.form.get('selected_insurance')
        if selected_insurance_id and selected_insurance_id.isdigit():
            id_int = int(selected_insurance_id)
            plan = next((p for p in insurance_plans if p['insurance_id'] == id_int), None)
            if plan:
                reservation['insurance_id'] = id_int
                write_reservations(reservations)
                selected_plan = plan
    else:
        if reservation['insurance_id'] > 0:
            selected_plan = next((p for p in insurance_plans if p['insurance_id'] == reservation['insurance_id']), None)

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation_id=reservation_id)

@app.route('/history')
def rental_history():
    rentals = read_rentals()
    filter_status = request.args.get('filter_status', 'All')
    valid_filters = ['All', 'Active', 'Completed', 'Cancelled']
    if filter_status not in valid_filters:
        filter_status = 'All'
    if filter_status != 'All':
        rentals = [r for r in rentals if r['status'].lower() == filter_status.lower()]
    return render_template('rental_history.html', rentals=rentals, filter_status=filter_status)

@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    if request.method == 'POST':
        action = request.form.get('action')
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str or not reservation_id_str.isdigit():
            return redirect(url_for('reservation_management'))
        reservation_id = int(reservation_id_str)
        reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
        if not reservation:
            return redirect(url_for('reservation_management'))
        if action == 'modify':
            new_status = request.form.get('new_status', '').strip()
            if new_status:
                reservation['status'] = new_status
                write_reservations(reservations)
        elif action == 'cancel':
            reservation['status'] = 'Cancelled'
            write_reservations(reservations)
        return redirect(url_for('reservation_management'))
    return render_template('reservations.html', reservations=reservations)

@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    submitted_data = None
    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str or not reservation_id_str.isdigit():
            return render_template('special_requests.html', reservations=reservations, submitted_data=None)
        reservation_id = int(reservation_id_str)
        reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
        if not reservation:
            return render_template('special_requests.html', reservations=reservations, submitted_data=None)

        driver_assistance = 'Driver assistance requested' if request.form.get('driver_assistance') else ''
        gps_option = 'GPS requested' if request.form.get('gps_option') else ''
        try:
            child_seat_quantity = int(request.form.get('child_seat_quantity', '0'))
        except Exception:
            child_seat_quantity = 0
        special_notes = request.form.get('special_notes', '').strip()

        special_requests_list = []
        if driver_assistance:
            special_requests_list.append(driver_assistance)
        if gps_option:
            special_requests_list.append(gps_option)
        if child_seat_quantity > 0:
            special_requests_list.append(f'Child seat x{child_seat_quantity}')
        if special_notes:
            special_requests_list.append(special_notes)

        special_requests_str = '; '.join(special_requests_list)

        reservation['special_requests'] = special_requests_str
        write_reservations(reservations)

        submitted_data = {
            'reservation_id': reservation_id,
            'special_requests': special_requests_str
        }

    return render_template('special_requests.html', reservations=reservations, submitted_data=submitted_data)

@app.route('/locations')
def locations():
    locations = read_locations()
    hours_filter_options = ['24/7', 'Business Hours', 'Weekend']
    return render_template('locations.html', locations=locations, hours_filter_options=hours_filter_options)


if __name__ == '__main__':
    app.run(debug=True)
