from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import threading
import os

app = Flask(__name__)
data_lock = threading.Lock()
data_dir = 'data'

# Utility functions to read and write data files safely

def read_data_file(filename):
    filepath = os.path.join(data_dir, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with data_lock, open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line.split('|'))
    return data

def write_data_file(filename, data_rows):
    filepath = os.path.join(data_dir, filename)
    with data_lock, open(filepath, 'w', encoding='utf-8') as f:
        for row in data_rows:
            f.write('|'.join(row) + '\n')

# Load vehicles data

def get_vehicle_by_id(vehicle_id):
    vehicles = read_data_file('vehicles.txt')
    for v in vehicles:
        if v[0] == vehicle_id:
            return {
                'vehicle_id': v[0], 'make': v[1], 'model': v[2], 'vehicle_type': v[3],
                'daily_rate': float(v[4]), 'seats': v[5], 'transmission': v[6], 'fuel_type': v[7],
                'status': v[8]
            }
    return None

# Load insurance plans

def get_insurance_by_id(insurance_id):
    insurances = read_data_file('insurance.txt')
    for ins in insurances:
        if ins[0] == insurance_id:
            return {
                'insurance_id': ins[0], 'plan_name': ins[1], 'description': ins[2],
                'daily_cost': float(ins[3]), 'coverage_limit': ins[4], 'deductible': ins[5]
            }
    return None

# Load reservations

def get_reservation_by_id(reservation_id):
    reservations = read_data_file('reservations.txt')
    for r in reservations:
        if r[0] == reservation_id:
            return {
                'reservation_id': r[0], 'rental_id': r[1], 'vehicle_id': r[2], 'customer_id': r[3],
                'status': r[4], 'insurance_id': r[5], 'special_requests': r[6]
            }
    return None

# Load rentals

def get_rental_by_id(rental_id):
    rentals = read_data_file('rentals.txt')
    for r in rentals:
        if r[0] == rental_id:
            return {
                'rental_id': r[0], 'vehicle_id': r[1], 'customer_id': r[2],
                'pickup_date': r[3], 'dropoff_date': r[4], 'pickup_location': r[5], 'dropoff_location': r[6],
                'total_price': float(r[7]), 'status': r[8]
            }
    return None

# Route 1: Dashboard page
@app.route('/', methods=['GET'])
def dashboard():
    # For demo, featured vehicles could be first 3 available vehicles
    vehicles = read_data_file('vehicles.txt')
    featured = []
    for v in vehicles:
        if v[8] == 'Available':
            featured.append({'vehicle_id': v[0], 'make': v[1], 'model': v[2]})
            if len(featured) >= 3:
                break
    # Sample promotions hardcoded
    promotions = [
        {'title': 'Spring Sale 15% Off', 'details': 'Save on all SUVs this spring!'},
        {'title': 'Weekend Special', 'details': 'Rent 2 days get 1 free weekend day.'}
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured,
                           promotions=promotions)

# Route 2: Vehicle Search page
@app.route('/search-vehicles', methods=['GET'])
def search_vehicles():
    # Read filter values from query string (optional)
    location_filter = request.args.get('location_filter', '')
    vehicle_type_filter = request.args.get('vehicle_type_filter', '')
    date_range = request.args.get('date_range', '')

    # Load vehicles
    vehicles = read_data_file('vehicles.txt')
    filtered = []
    for v in vehicles:
        if v[8] != 'Available':
            continue
        if vehicle_type_filter and v[3] != vehicle_type_filter:
            continue
        # Location filter could be ignored server side for now (would require rental overlaps check)
        filtered.append({
            'vehicle_id': v[0], 'make': v[1], 'model': v[2], 'vehicle_type': v[3],
            'daily_rate': v[4], 'seats': v[5], 'transmission': v[6], 'fuel_type': v[7]
        })

    # Unique locations from data/locations.txt
    locations_data = read_data_file('locations.txt')
    locations = [{'location_id': l[0], 'city': l[1]} for l in locations_data]

    return render_template('search_vehicles.html', vehicles=filtered, locations=locations,
                           selected_location=location_filter, selected_vehicle_type=vehicle_type_filter, date_range=date_range)

# Route 3: Vehicle Details page
@app.route('/vehicle-details/<vehicle_id>', methods=['GET'])
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return 'Vehicle not found', 404

    # Sample specs and reviews
    specs = {
        'engine': '2.0L Turbocharged',
        'seats': vehicle['seats'],
        'transmission': vehicle['transmission'],
        'fuel_type': vehicle['fuel_type']
    }

    reviews = [
        {'customer': 'Alice', 'comment': 'Very comfortable ride!'},
        {'customer': 'Bob', 'comment': 'Good value for the price.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, specs=specs, reviews=reviews)

# Route 4: Booking page
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return 'Vehicle not found', 404

    locations_data = read_data_file('locations.txt')
    locations = [{'location_id': l[0], 'city': l[1]} for l in locations_data]

    total_price = None
    error = None

    if request.method == 'POST':
        # Calculate price based on dates
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date_str = request.form.get('pickup_date')
        dropoff_date_str = request.form.get('dropoff_date')

        try:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
            dropoff_date = datetime.strptime(dropoff_date_str, '%Y-%m-%d')
            if dropoff_date < pickup_date:
                error = 'Dropoff date must be after pickup date.'
            else:
                days = (dropoff_date - pickup_date).days + 1
                total_price = days * vehicle['daily_rate']
        except Exception as e:
            error = 'Invalid date format.'

        return render_template('booking.html', vehicle=vehicle, locations=locations,
                               total_price=total_price, error=error,
                               pickup_location=pickup_location,
                               dropoff_location=dropoff_location,
                               pickup_date=pickup_date_str,
                               dropoff_date=dropoff_date_str)

    # GET
    return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price, error=error)

# Route 5: Insurance Options page
@app.route('/insurance-options', methods=['GET', 'POST'])
def insurance_options():
    insurances_data = read_data_file('insurance.txt')
    insurances = []
    for i in insurances_data:
        insurances.append({
            'insurance_id': i[0], 'plan_name': i[1], 'description': i[2],
            'daily_cost': float(i[3])
        })

    selected_insurance_id = None
    insurance_description = ''
    insurance_price = None

    if request.method == 'POST':
        selected_insurance_id = request.form.get('select_insurance')
        insurance = None
        for ins in insurances:
            if ins['insurance_id'] == selected_insurance_id:
                insurance = ins
                break
        if insurance:
            insurance_description = insurance['description']
            insurance_price = insurance['daily_cost']

    return render_template('insurance_options.html', insurances=insurances,
                           selected_insurance_id=selected_insurance_id,
                           insurance_description=insurance_description,
                           insurance_price=insurance_price)

# Route 6: Rental History page
@app.route('/rental-history', methods=['GET'])
def rental_history():
    rentals_data = read_data_file('rentals.txt')
    vehicles_data = read_data_file('vehicles.txt')
    vehicles_map = {v[0]: v[1] + ' ' + v[2] for v in vehicles_data}

    status_filter = request.args.get('status_filter', 'All')

    rentals = []
    for r in rentals_data:
        status = r[8]
        if status_filter != 'All' and status != status_filter:
            continue
        rentals.append({
            'rental_id': r[0], 'vehicle': vehicles_map.get(r[1], 'Unknown'), 'pickup_date': r[3],
            'dropoff_date': r[4], 'pickup_location': r[5], 'dropoff_location': r[6],
            'total_price': r[7], 'status': status
        })

    return render_template('rental_history.html', rentals=rentals, selected_status=status_filter)

# Route 7: Reservation Management page
@app.route('/my-reservations', methods=['GET'])
def my_reservations():
    reservations_data = read_data_file('reservations.txt')
    vehicles_data = read_data_file('vehicles.txt')
    vehicles_map = {v[0]: v[1] + ' ' + v[2] for v in vehicles_data}

    reservations = []
    for r in reservations_data:
        reservations.append({
            'reservation_id': r[0], 'vehicle': vehicles_map.get(r[2], 'Unknown'),
            'status': r[4]
        })

    return render_template('my_reservations.html', reservations=reservations)

# Route 8: Special Requests page
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations_data = read_data_file('reservations.txt')
    reservations = []
    for r in reservations_data:
        reservations.append({'reservation_id': r[0], 'status': r[4]})

    message = ''
    if request.method == 'POST':
        reservation_id = request.form.get('select_reservation')
        driver_assistance = request.form.get('driver_assistance_checkbox', '')
        gps_option = request.form.get('gps_option_checkbox', '')
        child_seat_quantity = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '')

        # Update special requests in reservations.txt
        with data_lock:
            all_reservations = read_data_file('reservations.txt')
            updated = False
            for idx, r in enumerate(all_reservations):
                if r[0] == reservation_id:
                    # Compose special requests string
                    requests_list = []
                    if driver_assistance == 'on':
                        requests_list.append('Driver assistance requested')
                    if gps_option == 'on':
                        requests_list.append('GPS option requested')
                    if child_seat_quantity and int(child_seat_quantity) > 0:
                        requests_list.append(f'Child seats: {child_seat_quantity}')
                    if special_notes.strip():
                        requests_list.append(f'Notes: {special_notes.strip()}')
                    r[6] = '; '.join(requests_list)
                    all_reservations[idx] = r
                    updated = True
                    break
            if updated:
                write_data_file('reservations.txt', all_reservations)
                message = 'Special requests updated successfully.'
            else:
                message = 'Reservation not found.'

    return render_template('special_requests.html', reservations=reservations, message=message)

# Route 9: Locations page
@app.route('/locations', methods=['GET'])
def locations():
    locations_data = read_data_file('locations.txt')
    locations_list = []

    hours_filter = request.args.get('hours_filter', '')
    search_location = request.args.get('search_location', '').lower()

    for loc in locations_data:
        if hours_filter and hours_filter != 'All' and loc[4] != hours_filter:
            continue
        if search_location:
            if search_location not in loc[1].lower() and search_location not in loc[2].lower():
                continue
        locations_list.append({
            'location_id': loc[0], 'city': loc[1], 'address': loc[2], 'phone': loc[3], 'hours': loc[4],
            'available_vehicles': loc[5]
        })

    return render_template('locations.html', locations=locations_list, hours_filter=hours_filter, search_location=search_location)

if __name__ == '__main__':
    app.run(debug=True)
