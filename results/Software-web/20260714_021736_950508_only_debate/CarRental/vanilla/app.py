from flask import Flask, render_template, request, redirect, url_for
import os
import threading
import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Locks for thread-safe file operations
locks = {
    'vehicles': threading.Lock(),
    'customers': threading.Lock(),
    'locations': threading.Lock(),
    'rentals': threading.Lock(),
    'insurance': threading.Lock(),
    'reservations': threading.Lock(),
}

# Utility functions for file operations

def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip()]


def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def parse_pipe_line(line, fields):
    parts = line.split('|')
    if len(parts) != len(fields):
        return None
    return dict(zip(fields, parts))


def serialize_pipe_line(data, fields):
    return '|'.join(str(data.get(field, '')) for field in fields)

# Load data from files

VEHICLES_FIELDS = ['vehicle_id','make','model','vehicle_type','daily_rate','seats','transmission','fuel_type','status']
CUSTOMERS_FIELDS = ['customer_id','name','email','phone','driver_license','license_expiry']
LOCATIONS_FIELDS = ['location_id','city','address','phone','hours','available_vehicles']
RENTALS_FIELDS = ['rental_id','vehicle_id','customer_id','pickup_date','dropoff_date','pickup_location','dropoff_location','total_price','status']
INSURANCE_FIELDS = ['insurance_id','plan_name','description','daily_cost','coverage_limit','deductible']
RESERVATIONS_FIELDS = ['reservation_id','rental_id','vehicle_id','customer_id','status','insurance_id','special_requests']


def load_vehicles():
    with locks['vehicles']:
        lines = read_file_lines('vehicles.txt')
    return [parse_pipe_line(line, VEHICLES_FIELDS) for line in lines if parse_pipe_line(line, VEHICLES_FIELDS)]


def load_customers():
    with locks['customers']:
        lines = read_file_lines('customers.txt')
    return [parse_pipe_line(line, CUSTOMERS_FIELDS) for line in lines if parse_pipe_line(line, CUSTOMERS_FIELDS)]


def load_locations():
    with locks['locations']:
        lines = read_file_lines('locations.txt')
    return [parse_pipe_line(line, LOCATIONS_FIELDS) for line in lines if parse_pipe_line(line, LOCATIONS_FIELDS)]


def load_rentals():
    with locks['rentals']:
        lines = read_file_lines('rentals.txt')
    return [parse_pipe_line(line, RENTALS_FIELDS) for line in lines if parse_pipe_line(line, RENTALS_FIELDS)]


def load_insurance_plans():
    with locks['insurance']:
        lines = read_file_lines('insurance.txt')
    return [parse_pipe_line(line, INSURANCE_FIELDS) for line in lines if parse_pipe_line(line, INSURANCE_FIELDS)]


def load_reservations():
    with locks['reservations']:
        lines = read_file_lines('reservations.txt')
    return [parse_pipe_line(line, RESERVATIONS_FIELDS) for line in lines if parse_pipe_line(line, RESERVATIONS_FIELDS)]


def save_reservations(reservations):
    with locks['reservations']:
        lines = [serialize_pipe_line(r, RESERVATIONS_FIELDS) for r in reservations]
        write_file_lines('reservations.txt', lines)


def save_rentals(rentals):
    with locks['rentals']:
        lines = [serialize_pipe_line(r, RENTALS_FIELDS) for r in rentals]
        write_file_lines('rentals.txt', lines)


def save_locations(locations):
    with locks['locations']:
        lines = [serialize_pipe_line(l, LOCATIONS_FIELDS) for l in locations]
        write_file_lines('locations.txt', lines)

# Helpers

def get_vehicle_by_id(vehicle_id):
    vehicles = load_vehicles()
    for v in vehicles:
        if int(v['vehicle_id']) == vehicle_id:
            return v
    return None


def get_insurance_by_id(insurance_id):
    insurances = load_insurance_plans()
    for ins in insurances:
        if int(ins['insurance_id']) == insurance_id:
            return ins
    return None


def get_reservation_by_id(reservation_id):
    reservations = load_reservations()
    for r in reservations:
        if int(r['reservation_id']) == reservation_id:
            return r
    return None


def get_rental_by_id(rental_id):
    rentals = load_rentals()
    for r in rentals:
        if int(r['rental_id']) == rental_id:
            return r
    return None


def get_location_by_id(location_id):
    locations = load_locations()
    for l in locations:
        if int(l['location_id']) == location_id:
            return l
    return None


def date_diff_days(start_date, end_date):
    fmt = '%Y-%m-%d'
    d1 = datetime.datetime.strptime(start_date, fmt)
    d2 = datetime.datetime.strptime(end_date, fmt)
    delta = (d2 - d1).days
    return max(delta, 0)

# Routes

@app.route('/')
@app.route('/dashboard')
def dashboard():
    vehicles = load_vehicles()
    # Featured vehicles: first 3 available
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:3]

    # Promotions hardcoded
    promotions = [
        {'title': 'Winter Special Discount', 'description': 'Rent any SUV and get 10% off!'},
        {'title': 'Weekend Luxury Deal', 'description': 'Luxury cars at reduced rates on weekends!'}
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/search', methods=['GET', 'POST'])
def search():
    locations = load_locations()
    vehicles = load_vehicles()

    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    selected_location = None
    selected_vehicle_type = None
    selected_date_range = ''
    filtered_vehicles = vehicles

    if request.method == 'POST':
        selected_location = request.form.get('location-filter')
        selected_vehicle_type = request.form.get('vehicle-type-filter')
        selected_date_range = request.form.get('date-range-input', '')

        filtered_vehicles = vehicles

        # Filter by location - assume available_vehicles is count, we show vehicles available if location matches
        if selected_location and selected_location != '':
            filtered_vehicles = [v for v in filtered_vehicles if v['status'] == 'Available']
            # For demo, filtering by location means vehicles that are available
            # In realistic app, would have location info per vehicle

        if selected_vehicle_type and selected_vehicle_type != '':
            filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == selected_vehicle_type]

    return render_template('search.html', locations=locations, vehicle_types=vehicle_types,
                           filtered_vehicles=filtered_vehicles, selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type, selected_date_range=selected_date_range)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    # Hardcoded reviews
    reviews = [
        {'author': 'John Doe', 'rating': 5, 'comment': 'Great car, smooth ride!'},
        {'author': 'Jane Smith', 'rating': 4, 'comment': 'Very comfortable and clean.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    locations = load_locations()
    calculated_price = None
    error = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup-location')
        dropoff_location = request.form.get('dropoff-location')
        pickup_date = request.form.get('pickup-date')
        dropoff_date = request.form.get('dropoff-date')

        if 'calculate-price-button' in request.form:
            # Calculate price
            if pickup_date and dropoff_date:
                days = date_diff_days(pickup_date, dropoff_date)
                daily_rate = float(vehicle['daily_rate'])
                calculated_price = days * daily_rate

        elif 'proceed-to-insurance-button' in request.form:
            # Create new rental and reservation preliminary
            if pickup_location and dropoff_location and pickup_date and dropoff_date:
                days = date_diff_days(pickup_date, dropoff_date)
                if days <= 0:
                    error = 'Invalid date range'
                else:
                    rentals = load_rentals()
                    reservations = load_reservations()
                    customers = load_customers()
                    customer = customers[0] if customers else None
                    if not customer:
                        return "No customer found", 500

                    new_rental_id = max([int(r['rental_id']) for r in rentals], default=0) + 1
                    total_price = days * float(vehicle['daily_rate'])

                    new_rental = {
                        'rental_id': str(new_rental_id),
                        'vehicle_id': str(vehicle_id),
                        'customer_id': customer['customer_id'],
                        'pickup_date': pickup_date,
                        'dropoff_date': dropoff_date,
                        'pickup_location': pickup_location,
                        'dropoff_location': dropoff_location,
                        'total_price': f'{total_price:.2f}',
                        'status': 'Pending'
                    }

                    rentals.append(new_rental)
                    save_rentals(rentals)

                    new_reservation_id = max([int(r['reservation_id']) for r in reservations], default=0) + 1
                    new_reservation = {
                        'reservation_id': str(new_reservation_id),
                        'rental_id': str(new_rental_id),
                        'vehicle_id': str(vehicle_id),
                        'customer_id': customer['customer_id'],
                        'status': 'Pending',
                        'insurance_id': '',
                        'special_requests': ''
                    }

                    reservations.append(new_reservation)
                    save_reservations(reservations)

                    return redirect(url_for('insurance', reservation_id=new_reservation_id))

    return render_template('booking.html', vehicle=vehicle, locations=locations, calculated_price=calculated_price, error=error)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance(reservation_id):
    insurance_plans = load_insurance_plans()
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return "Reservation not found", 404

    selected_plan = None

    if request.method == 'POST':
        selected_insurance_id = request.form.get('select-insurance')
        if 'confirm-booking-button' in request.form:
            # Finalize booking with selected insurance
            if selected_insurance_id:
                reservations = load_reservations()
                for r in reservations:
                    if int(r['reservation_id']) == reservation_id:
                        r['insurance_id'] = selected_insurance_id
                        r['status'] = 'Confirmed'
                save_reservations(reservations)

                rentals = load_rentals()
                for r in rentals:
                    if int(r['rental_id']) == int(reservation['rental_id']):
                        r['status'] = 'Confirmed'
                save_rentals(rentals)

                return redirect(url_for('reservations'))

        if selected_insurance_id:
            selected_plan = get_insurance_by_id(int(selected_insurance_id))
    else:
        if reservation['insurance_id']:
            selected_plan = get_insurance_by_id(int(reservation['insurance_id']))

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation=reservation)


@app.route('/history', methods=['GET', 'POST'])
def history():
    rentals = load_rentals()
    status_options = ['All', 'Active', 'Completed', 'Cancelled']
    selected_status = request.form.get('status-filter') if request.method == 'POST' else 'All'

    filtered_rentals = rentals
    if selected_status and selected_status != 'All':
        filtered_rentals = [r for r in rentals if r['status'] == selected_status]

    return render_template('history.html', rentals=filtered_rentals, status_options=status_options, selected_status=selected_status)


@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    reservations = load_reservations()

    if request.method == 'POST':
        form_keys = request.form.keys()
        reservations_list = reservations.copy()

        for key in form_keys:
            if key.startswith('modify-reservation-button-'):
                reservation_id = int(key.split('-')[-1])
                # toggle Active/Pending
                for r in reservations_list:
                    if int(r['reservation_id']) == reservation_id:
                        if r['status'] == 'Active':
                            r['status'] = 'Pending'
                        else:
                            r['status'] = 'Active'
                save_reservations(reservations_list)

            elif key.startswith('cancel-reservation-button-'):
                reservation_id = int(key.split('-')[-1])
                for r in reservations_list:
                    if int(r['reservation_id']) == reservation_id:
                        r['status'] = 'Cancelled'
                save_reservations(reservations_list)

            elif key == 'sort-by-date-button':
                rentals = load_rentals()
                reservations_list.sort(key=lambda res: next((rent['pickup_date'] for rent in rentals if rent['rental_id'] == res['rental_id']), ''))
                save_reservations(reservations_list)

        reservations = reservations_list

    return render_template('reservations.html', reservations=reservations)


@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    reservations = load_reservations()

    message = None

    if request.method == 'POST':
        selected_reservation_id = request.form.get('select-reservation')
        driver_assistance = request.form.get('driver-assistance-checkbox')
        gps_option = request.form.get('gps-option-checkbox')
        child_seat_qty = request.form.get('child-seat-quantity')
        special_notes = request.form.get('special-notes')

        if selected_reservation_id:
            reservations_list = reservations.copy()
            for r in reservations_list:
                if r['reservation_id'] == selected_reservation_id:
                    reqs = []
                    if driver_assistance == 'on':
                        reqs.append('Driver assistance requested')
                    if gps_option == 'on':
                        reqs.append('GPS requested')
                    if child_seat_qty and child_seat_qty.isdigit() and int(child_seat_qty) > 0:
                        reqs.append(f'Child seat quantity: {child_seat_qty}')
                    if special_notes and special_notes.strip():
                        reqs.append(f'Notes: {special_notes.strip()}')
                    r['special_requests'] = '; '.join(reqs)
            save_reservations(reservations_list)
            message = 'Special requests updated.'

    return render_template('requests.html', reservations=reservations, message=message)


@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = load_locations()
    hours_options = ['24/7', 'Business Hours', 'Weekend']
    selected_hours_filter = None
    search_text = ''

    if request.method == 'POST':
        selected_hours_filter = request.form.get('hours-filter')
        search_text = request.form.get('search-location-input', '').lower()

        filtered_locations = locations

        if selected_hours_filter and selected_hours_filter != '':
            if selected_hours_filter == 'Business Hours':
                filtered_locations = [l for l in filtered_locations if l['hours'] != '24/7']
            elif selected_hours_filter == 'Weekend':
                filtered_locations = []

        if search_text and search_text != '':
            filtered_locations = [l for l in filtered_locations if search_text in l['city'].lower() or search_text in l['address'].lower()]

        locations = filtered_locations

    return render_template('locations.html', locations=locations, hours_options=hours_options,
                           selected_hours_filter=selected_hours_filter, search_text=search_text)


if __name__ == '__main__':
    app.run(debug=True)
