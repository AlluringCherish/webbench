from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to read and write pipe-delimited files

def read_data(filename):
    path = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(line.strip().split('|'))
    return data


def write_data(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(map(str, record)) + '\n')


# Load all vehicles

def get_vehicles():
    vehicles = read_data('vehicles.txt')
    vehicle_list = []
    for v in vehicles:
        vehicle_list.append({
            'vehicle_id': v[0],
            'make': v[1],
            'model': v[2],
            'vehicle_type': v[3],
            'daily_rate': float(v[4]),
            'seats': v[5],
            'transmission': v[6],
            'fuel_type': v[7],
            'status': v[8]
        })
    return vehicle_list


def get_vehicle_by_id(vehicle_id):
    vehicles = get_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None


# Load locations

def get_locations():
    locs = read_data('locations.txt')
    location_list = []
    for l in locs:
        location_list.append({
            'location_id': l[0],
            'city': l[1],
            'address': l[2],
            'phone': l[3],
            'hours': l[4],
            'available_vehicles': int(l[5])
        })
    return location_list


def get_location_by_id(location_id):
    locations = get_locations()
    for l in locations:
        if l['location_id'] == location_id:
            return l
    return None


# Load insurance plans

def get_insurance_plans():
    insurances = read_data('insurance.txt')
    insurance_list = []
    for i in insurances:
        insurance_list.append({
            'insurance_id': i[0],
            'plan_name': i[1],
            'description': i[2],
            'daily_cost': float(i[3]),
            'coverage_limit': i[4],
            'deductible': i[5]
        })
    return insurance_list


def get_insurance_by_id(insurance_id):
    plans = get_insurance_plans()
    for p in plans:
        if p['insurance_id'] == insurance_id:
            return p
    return None


# Load customers

def get_customers():
    customers = read_data('customers.txt')
    customer_list = []
    for c in customers:
        customer_list.append({
            'customer_id': c[0],
            'name': c[1],
            'email': c[2],
            'phone': c[3],
            'driver_license': c[4],
            'license_expiry': c[5]
        })
    return customer_list


def get_customer_by_id(customer_id):
    customers = get_customers()
    for c in customers:
        if c['customer_id'] == customer_id:
            return c
    return None


# Load rentals

def get_rentals():
    rentals = read_data('rentals.txt')
    rental_list = []
    for r in rentals:
        rental_list.append({
            'rental_id': r[0],
            'vehicle_id': r[1],
            'customer_id': r[2],
            'pickup_date': r[3],
            'dropoff_date': r[4],
            'pickup_location': r[5],
            'dropoff_location': r[6],
            'total_price': float(r[7]),
            'status': r[8]
        })
    return rental_list


def get_rental_by_id(rental_id):
    rentals = get_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None


# Load reservations

def get_reservations():
    reservations = read_data('reservations.txt')
    reservation_list = []
    for res in reservations:
        reservation_list.append({
            'reservation_id': res[0],
            'rental_id': res[1],
            'vehicle_id': res[2],
            'customer_id': res[3],
            'status': res[4],
            'insurance_id': res[5],
            'special_requests': res[6]
        })
    return reservation_list


def get_reservation_by_id(reservation_id):
    reservations = get_reservations()
    for res in reservations:
        if res['reservation_id'] == reservation_id:
            return res
    return None


# Dashboard Page
@app.route('/')
def dashboard():
    vehicles = get_vehicles()
    promotions_section = "Winter Special - Up to 20% off!"  # Example static promotion
    return render_template('dashboard.html', vehicles=vehicles, promotions_section=promotions_section)


# Vehicle Search Page
@app.route('/search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = get_vehicles()
    locations = get_locations()
    filtered_vehicles = vehicles
    selected_location = ''
    selected_type = ''

    if request.method == 'POST':
        selected_location = request.form.get('location-filter', '')
        selected_type = request.form.get('vehicle-type-filter', '')

        filtered_vehicles = []
        for v in vehicles:
            # Filter by vehicle type only, do not filter by location since vehicles have no city attribute
            if (selected_type == '' or v['vehicle_type'] == selected_type) and v['status'] == 'Available':
                filtered_vehicles.append(v)

    return render_template('search.html', vehicles=filtered_vehicles, locations=locations,
                           selected_location=selected_location, selected_type=selected_type)


# Vehicle Details Page
@app.route('/vehicle/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404
    # Simulate vehicle reviews
    reviews = ["Great car!", "Very comfortable.", "Fuel efficient."]
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


# Booking Page
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    locations = get_locations()
    total_price = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup-location')
        dropoff_location = request.form.get('dropoff-location')
        pickup_date = request.form.get('pickup-date')
        dropoff_date = request.form.get('dropoff-date')

        # Calculate total price if requested
        if 'calculate-price-button' in request.form:
            try:
                p_date = datetime.strptime(pickup_date, '%Y-%m-%d')
                d_date = datetime.strptime(dropoff_date, '%Y-%m-%d')
                days = (d_date - p_date).days
                if days <= 0:
                    total_price = 0
                else:
                    total_price = days * vehicle['daily_rate']
            except Exception:
                total_price = 0

        # Proceed to insurance page
        elif 'proceed-to-insurance-button' in request.form:
            # For demo, store booking info in session or pass via query params (simplified)
            return redirect(url_for('insurance', vehicle_id=vehicle_id, pickup_location=pickup_location,
                                    dropoff_location=dropoff_location, pickup_date=pickup_date,
                                    dropoff_date=dropoff_date, total_price=request.form.get('total-price', '0')))

    return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)


# Insurance Options Page
@app.route('/insurance/<vehicle_id>', methods=['GET', 'POST'])
def insurance(vehicle_id):
    insurance_plans = get_insurance_plans()
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    if request.method == 'POST':
        selected_insurance_id = request.form.get('insurance')
        # Save booking with insurance
        # For simplicity, create new rental and reservation
        # Generate new IDs
        rentals = get_rentals()
        new_rental_id = str(int(rentals[-1]['rental_id']) + 1) if rentals else '1'
        reservations = get_reservations()
        new_reservation_id = str(int(reservations[-1]['reservation_id']) + 1) if reservations else '1'

        # Get booking info from form (hidden inputs or session ideally)
        pickup_location = request.args.get('pickup_location') or request.form.get('pickup_location')
        dropoff_location = request.args.get('dropoff_location') or request.form.get('dropoff_location')
        pickup_date = request.args.get('pickup_date') or request.form.get('pickup_date')
        dropoff_date = request.args.get('dropoff_date') or request.form.get('dropoff_date')
        total_price = request.args.get('total_price') or request.form.get('total_price') or '0'

        # For demo, hardcode customer_id
        customer_id = '1'

        # Add new rental
        new_rental = [
            new_rental_id, vehicle_id, customer_id, pickup_date, dropoff_date,
            pickup_location, dropoff_location, total_price, 'Active'
        ]
        rentals.append({
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': float(total_price),
            'status': 'Active'
        })
        write_data('rentals.txt', [
            [r['rental_id'], r['vehicle_id'], r['customer_id'], r['pickup_date'], r['dropoff_date'], r['pickup_location'], r['dropoff_location'], str(r['total_price']), r['status']] for r in rentals
        ])

        # Add new reservation
        new_reservation = [
            new_reservation_id, new_rental_id, vehicle_id, customer_id, 'Confirmed', selected_insurance_id, ''
        ]
        reservations.append({
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'status': 'Confirmed',
            'insurance_id': selected_insurance_id,
            'special_requests': ''
        })
        write_data('reservations.txt', [
            [res['reservation_id'], res['rental_id'], res['vehicle_id'], res['customer_id'], res['status'], res['insurance_id'], res['special_requests']] for res in reservations
        ])

        return redirect(url_for('dashboard'))

    # GET method renders insurance options
    # pass booking info as args
    pickup_location = request.args.get('pickup_location', '')
    dropoff_location = request.args.get('dropoff_location', '')
    pickup_date = request.args.get('pickup_date', '')
    dropoff_date = request.args.get('dropoff_date', '')
    total_price = request.args.get('total_price', '0')

    return render_template('insurance.html', insurance_plans=insurance_plans, insurance_description='',
                           insurance_price='', vehicle=vehicle, pickup_location=pickup_location,
                           dropoff_location=dropoff_location, pickup_date=pickup_date, dropoff_date=dropoff_date,
                           total_price=total_price)


# Rental History Page
@app.route('/history', methods=['GET', 'POST'])
def rental_history():
    rentals = get_rentals()
    vehicles = {v['vehicle_id']: v for v in get_vehicles()}
    customers = {c['customer_id']: c for c in get_customers()}
    status_filter = request.form.get('status-filter', '') if request.method == 'POST' else ''

    filtered_rentals = []
    for r in rentals:
        if status_filter == '' or r['status'] == status_filter:
            r_copy = r.copy()
            r_copy['vehicle'] = vehicles.get(r['vehicle_id'], {})
            r_copy['customer'] = customers.get(r['customer_id'], {})
            filtered_rentals.append(r_copy)

    return render_template('rental_history.html', rentals=filtered_rentals, status_filter=status_filter)


# Reservation Management Page
@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = get_reservations()
    vehicles = {v['vehicle_id']: v for v in get_vehicles()}

    sort_by_date = False
    if request.method == 'POST':
        if 'sort-by-date-button' in request.form:
            # Sort reservations by rental pickup_date ascending
            rentals = {r['rental_id']: r for r in get_rentals()}
            reservations.sort(key=lambda res: rentals.get(res['rental_id'], {}).get('pickup_date', ''))
            sort_by_date = True
        elif 'cancel' in request.form:
            # Cancel reservation
            reservation_id = request.form.get('cancel')
            reservations = [r for r in reservations if r['reservation_id'] != reservation_id]
            # Update reservations file
            write_data('reservations.txt', [[r['reservation_id'], r['rental_id'], r['vehicle_id'], r['customer_id'], r['status'], r['insurance_id'], r['special_requests']] for r in reservations])
    return render_template('reservations.html', reservations=reservations, vehicles=vehicles, sort_by_date=sort_by_date)


# Special Requests Page
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = get_reservations()
    if request.method == 'POST':
        selected_reservation_id = request.form.get('select-reservation')
        driver_assistance = 'Yes' if request.form.get('driver-assistance-checkbox') else 'No'
        gps_option = 'Yes' if request.form.get('gps-option-checkbox') else 'No'
        child_seat_qty = request.form.get('child-seat-quantity', '0')
        special_notes = request.form.get('special-notes')

        # Update reservation special_requests
        for r in reservations:
            if r['reservation_id'] == selected_reservation_id:
                reqs = []
                if driver_assistance == 'Yes':
                    reqs.append('Driver assistance requested')
                if gps_option == 'Yes':
                    reqs.append('GPS requested')
                if child_seat_qty and int(child_seat_qty) > 0:
                    reqs.append(f'Child seat quantity: {child_seat_qty}')
                if special_notes:
                    reqs.append(f'Notes: {special_notes}')
                r['special_requests'] = '; '.join(reqs)
                break

        # Save back
        write_data('reservations.txt', [[r['reservation_id'], r['rental_id'], r['vehicle_id'], r['customer_id'], r['status'], r['insurance_id'], r['special_requests']] for r in reservations])
        return redirect(url_for('reservation_management'))

    return render_template('special_requests.html', reservations=reservations)


# Locations Page
@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = get_locations()
    filtered_locations = locations
    hours_filter = ''
    search_input = ''

    if request.method == 'POST':
        hours_filter = request.form.get('hours-filter', '')
        search_input = request.form.get('search-location-input', '').lower()

        filtered_locations = []
        for loc in locations:
            if hours_filter and loc['hours'] != hours_filter:
                continue
            if search_input and (search_input not in loc['city'].lower() and search_input not in loc['address'].lower()):
                continue
            filtered_locations.append(loc)

    return render_template('locations.html', locations=filtered_locations, hours_filter=hours_filter, search_input=search_input)


if __name__ == '__main__':
    app.run(debug=True)
