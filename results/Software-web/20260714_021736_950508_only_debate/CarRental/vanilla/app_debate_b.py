from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions for file reading and writing

def read_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return lines


def write_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def parse_pipe_line(line, fields):
    parts = line.strip().split('|')
    if len(parts) != len(fields):
        return None
    return {fields[i]: parts[i] for i in range(len(fields))}


def serialize_dict_to_line(d, fields):
    return '|'.join(str(d.get(field, '')) for field in fields)

#----------------------------
# Load and save data functions
#----------------------------

# Vehicles
VEHICLE_FIELDS = ['vehicle_id', 'make', 'model', 'vehicle_type', 'daily_rate', 'seats', 'transmission', 'fuel_type', 'status']

def load_vehicles():
    filepath = os.path.join(DATA_DIR, 'vehicles.txt')
    lines = read_file(filepath)
    vehicles = []
    for line in lines:
        v = parse_pipe_line(line, VEHICLE_FIELDS)
        if v:
            # convert types
            v['vehicle_id'] = int(v['vehicle_id'])
            v['daily_rate'] = float(v['daily_rate'])
            v['seats'] = int(v['seats'])
            vehicles.append(v)
    return vehicles


def find_vehicle(vehicle_id):
    for v in load_vehicles():
        if v['vehicle_id'] == vehicle_id:
            return v
    return None


# Customers
CUSTOMER_FIELDS = ['customer_id', 'name', 'email', 'phone', 'driver_license', 'license_expiry']

def load_customers():
    filepath = os.path.join(DATA_DIR, 'customers.txt')
    lines = read_file(filepath)
    customers = []
    for line in lines:
        c = parse_pipe_line(line, CUSTOMER_FIELDS)
        if c:
            c['customer_id'] = int(c['customer_id'])
            customers.append(c)
    return customers

# Locations
LOCATION_FIELDS = ['location_id', 'city', 'address', 'phone', 'hours', 'available_vehicles']

def load_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    lines = read_file(filepath)
    locations = []
    for line in lines:
        loc = parse_pipe_line(line, LOCATION_FIELDS)
        if loc:
            loc['location_id'] = int(loc['location_id'])
            loc['available_vehicles'] = int(loc['available_vehicles'])
            locations.append(loc)
    return locations

# Rentals
RENTAL_FIELDS = ['rental_id', 'vehicle_id', 'customer_id', 'pickup_date', 'dropoff_date', 'pickup_location', 'dropoff_location', 'total_price', 'status']

def load_rentals():
    filepath = os.path.join(DATA_DIR, 'rentals.txt')
    lines = read_file(filepath)
    rentals = []
    for line in lines:
        r = parse_pipe_line(line, RENTAL_FIELDS)
        if r:
            r['rental_id'] = int(r['rental_id'])
            r['vehicle_id'] = int(r['vehicle_id'])
            r['customer_id'] = int(r['customer_id'])
            r['total_price'] = float(r['total_price'])
            rentals.append(r)
    return rentals


# Insurance
INSURANCE_FIELDS = ['insurance_id', 'plan_name', 'description', 'daily_cost', 'coverage_limit', 'deductible']

def load_insurance_plans():
    filepath = os.path.join(DATA_DIR, 'insurance.txt')
    lines = read_file(filepath)
    plans = []
    for line in lines:
        p = parse_pipe_line(line, INSURANCE_FIELDS)
        if p:
            p['insurance_id'] = int(p['insurance_id'])
            p['daily_cost'] = float(p['daily_cost'])
            plans.append(p)
    return plans


# Reservations
RESERVATION_FIELDS = ['reservation_id', 'rental_id', 'vehicle_id', 'customer_id', 'status', 'insurance_id', 'special_requests']

def load_reservations():
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    lines = read_file(filepath)
    reservations = []
    for line in lines:
        res = parse_pipe_line(line, RESERVATION_FIELDS)
        if res:
            res['reservation_id'] = int(res['reservation_id'])
            res['rental_id'] = int(res['rental_id'])
            res['vehicle_id'] = int(res['vehicle_id'])
            res['customer_id'] = int(res['customer_id'])
            res['insurance_id'] = int(res['insurance_id'])
            reservations.append(res)
    return reservations


def save_reservations(reservations):
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    lines = [serialize_dict_to_line(r, RESERVATION_FIELDS) for r in reservations]
    write_file(filepath, lines)


# Rentals save

def save_rentals(rentals):
    filepath = os.path.join(DATA_DIR, 'rentals.txt')
    lines = [serialize_dict_to_line(r, RENTAL_FIELDS) for r in rentals]
    write_file(filepath, lines)


#-------------------------
# Application Routes
#-------------------------

@app.route('/')
def root():
    # Entry point renders dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    vehicles = load_vehicles()
    # For featured_vehicles: pick first 3 available as sample featured
    featured = [v for v in vehicles if v['status'] == 'Available'][:3]

    # Simple promotions static example
    promotions = [
        {'title': 'Weekend Special', 'description': 'Get 10% off this weekend!'},
        {'title': 'Long Term Discount', 'description': 'Save 15% on rentals over 7 days!'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured, promotions=promotions)


@app.route('/search', methods=['GET', 'POST'])
def search():
    locations = load_locations()
    vehicles = load_vehicles()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    selected_location = None
    selected_vehicle_type = None
    selected_date_range = ""
    filtered_vehicles = vehicles

    if request.method == 'POST':
        selected_location = request.form.get('location-filter') or None
        selected_vehicle_type = request.form.get('vehicle-type-filter') or None
        selected_date_range = request.form.get('date-range-input') or ""

        # Filter vehicles
        filtered_vehicles = vehicles
        if selected_location:
            # Filter vehicles that are available at locations city matches selected_location city
            # Since vehicles.txt doesn't link directly to locations, we'll just simulate filter by vehicle status Available
            filtered_vehicles = [v for v in filtered_vehicles if v['status'] == 'Available']

        if selected_vehicle_type:
            filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == selected_vehicle_type]

    return render_template('search.html', locations=locations, vehicle_types=vehicle_types,
                           filtered_vehicles=filtered_vehicles,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           selected_date_range=selected_date_range)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    # Load reviews dummy data for now (no specification for reviews.txt file)
    reviews = [
        {'author': 'John', 'rating': 4, 'comment': 'Good car, very comfortable.'},
        {'author': 'Emily', 'rating': 5, 'comment': 'Excellent vehicle and service.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    locations = load_locations()
    calculated_price = None

    if request.method == 'POST':
        if 'calculate-price-button' in request.form:
            try:
                pickup_date_str = request.form['pickup-date']
                dropoff_date_str = request.form['dropoff-date']
                pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
                dropoff_date = datetime.strptime(dropoff_date_str, '%Y-%m-%d')
                days = (dropoff_date - pickup_date).days
                if days <= 0:
                    calculated_price = 0
                else:
                    calculated_price = days * vehicle['daily_rate']
            except Exception:
                calculated_price = 0

        elif 'proceed-to-insurance-button' in request.form:
            # Save reservation draft
            # We need to create a rental entry first
            pickup_loc_id = int(request.form['pickup-location'])
            dropoff_loc_id = int(request.form['dropoff-location'])
            pickup_date = request.form['pickup-date']
            dropoff_date = request.form['dropoff-date']
            customer_id = 1  # Assume logged in user customer_id=1 for demo

            locations_map = {loc['location_id']: loc['city'] for loc in load_locations()}
            pickup_loc_city = locations_map.get(pickup_loc_id, '')
            dropoff_loc_city = locations_map.get(dropoff_loc_id, '')

            # Calculate price
            try:
                pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
                dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
                days = (dropoff_dt - pickup_dt).days
                if days <= 0:
                    total_price = 0
                else:
                    total_price = days * vehicle['daily_rate']
            except Exception:
                total_price = 0

            rentals = load_rentals()
            new_rental_id = max([r['rental_id'] for r in rentals], default=0) + 1

            new_rental = {
                'rental_id': new_rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': customer_id,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'pickup_location': pickup_loc_city,
                'dropoff_location': dropoff_loc_city,
                'total_price': total_price,
                'status': 'Pending'
            }

            rentals.append(new_rental)
            save_rentals(rentals)

            # Create reservation with default insurance_id 0 (none) and status Pending
            reservations = load_reservations()
            new_reservation_id = max([r['reservation_id'] for r in reservations], default=0) + 1
            new_reservation = {
                'reservation_id': new_reservation_id,
                'rental_id': new_rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': customer_id,
                'status': 'Pending',
                'insurance_id': 0,
                'special_requests': ''
            }
            reservations.append(new_reservation)
            save_reservations(reservations)

            return redirect(url_for('insurance', reservation_id=new_reservation_id))

    return render_template('booking.html', vehicle=vehicle, locations=locations, calculated_price=calculated_price)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance(reservation_id):
    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        return "Reservation not found", 404

    insurance_plans = load_insurance_plans()
    selected_plan = None

    if request.method == 'POST':
        selected_id = int(request.form.get('select_insurance'))
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_id), None)

        if 'confirm-booking-button' in request.form:
            # Confirm booking: update reservation
            reservation['insurance_id'] = selected_id
            reservation['status'] = 'Confirmed'
            reservations = [r if r['reservation_id'] != reservation_id else reservation for r in reservations]
            save_reservations(reservations)
            return redirect(url_for('reservations_page'))

        # Just selecting insurance plan
        return render_template('insurance.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation=reservation)

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation=reservation)


@app.route('/history', methods=['GET', 'POST'])
def history():
    rentals = load_rentals()
    status_options = ['All', 'Active', 'Completed', 'Cancelled']
    selected_status = 'All'

    if request.method == 'POST':
        selected_status = request.form.get('status-filter', 'All')

    if selected_status != 'All':
        filtered = [r for r in rentals if r['status'] == selected_status]
    else:
        filtered = rentals

    return render_template('history.html', rentals=filtered, status_options=status_options, selected_status=selected_status)


@app.route('/reservations', methods=['GET', 'POST'])
def reservations_page():
    reservations = load_reservations()
    if request.method == 'POST':
        # Modify or cancel reservation
        for key in request.form.keys():
            if key.startswith('modify-reservation-button-'):
                reservation_id = int(key[len('modify-reservation-button-'):])
                # For simplicity, just change status to Confirmed
                for r in reservations:
                    if r['reservation_id'] == reservation_id:
                        r['status'] = 'Confirmed'
                save_reservations(reservations)
                break
            elif key.startswith('cancel-reservation-button-'):
                reservation_id = int(key[len('cancel-reservation-button-'):])
                # Change status to Cancelled
                for r in reservations:
                    if r['reservation_id'] == reservation_id:
                        r['status'] = 'Cancelled'
                save_reservations(reservations)
                break
            elif key == 'sort-by-date-button':
                reservations = sorted(reservations, key=lambda r: r['reservation_id'])

    return render_template('reservations.html', reservations=reservations)


@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    reservations = load_reservations()
    if request.method == 'POST':
        res_id = int(request.form['select-reservation'])
        driver_assist = 'driver-assistance-checkbox' in request.form
        gps_option = 'gps-option-checkbox' in request.form
        child_seats = int(request.form.get('child-seat-quantity', 0))
        special_notes = request.form.get('special-notes', '')

        # Append special requests text
        special_reqs = []
        if driver_assist:
            special_reqs.append('Driver assistance requested')
        if gps_option:
            special_reqs.append('GPS requested')
        if child_seats > 0:
            special_reqs.append(f'Child seat qty: {child_seats}')
        if special_notes.strip():
            special_reqs.append(f'Notes: {special_notes.strip()}')

        reservations = load_reservations()
        for r in reservations:
            if r['reservation_id'] == res_id:
                r['special_requests'] = "; ".join(special_reqs)
        save_reservations(reservations)

    return render_template('requests.html', reservations=reservations)


@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = load_locations()
    hours_options = ['24/7', 'Business Hours', 'Weekend']
    selected_hours_filter = None
    search_text = ''

    if request.method == 'POST':
        selected_hours_filter = request.form.get('hours-filter')
        search_text = request.form.get('search-location-input', '').strip()

        if selected_hours_filter:
            if selected_hours_filter == '24/7':
                locations = [loc for loc in locations if loc['hours'] == '24/7']
            elif selected_hours_filter == 'Business Hours':
                locations = [loc for loc in locations if loc['hours'] == '09:00-18:00']
            elif selected_hours_filter == 'Weekend':
                locations = [loc for loc in locations if loc['hours'].lower().startswith('weekend')]

        if search_text:
            locations = [loc for loc in locations if search_text.lower() in loc['city'].lower() or search_text.lower() in loc['address'].lower()]

    return render_template('locations.html', locations=locations,
                           hours_options=hours_options,
                           selected_hours_filter=selected_hours_filter,
                           search_text=search_text)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
