from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load and save data from text files

def load_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                vehicles.append({
                    'vehicle_id': int(parts[0]),
                    'make': parts[1],
                    'model': parts[2],
                    'vehicle_type': parts[3],
                    'daily_rate': float(parts[4]),
                    'seats': int(parts[5]),
                    'transmission': parts[6],
                    'fuel_type': parts[7],
                    'status': parts[8]
                })
    except Exception:
        vehicles = []
    return vehicles

def load_customers():
    customers = []
    try:
        with open('data/customers.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                customers.append({
                    'customer_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'driver_license': parts[4],
                    'license_expiry': parts[5]
                })
    except Exception:
        customers = []
    return customers

def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                locations.append({
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                })
    except Exception:
        locations = []
    return locations

def load_rentals():
    rentals = []
    try:
        with open('data/rentals.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                rentals.append({
                    'rental_id': int(parts[0]),
                    'vehicle_id': int(parts[1]),
                    'customer_id': int(parts[2]),
                    'pickup_date': parts[3],
                    'dropoff_date': parts[4],
                    'pickup_location': parts[5],
                    'dropoff_location': parts[6],
                    'total_price': float(parts[7]),
                    'status': parts[8]
                })
    except Exception:
        rentals = []
    return rentals

def load_insurance_plans():
    insurance_plans = []
    try:
        with open('data/insurance.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                insurance_plans.append({
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': int(parts[5])
                })
    except Exception:
        insurance_plans = []
    return insurance_plans

def load_reservations():
    reservations = []
    try:
        with open('data/reservations.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                reservations.append({
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                })
    except Exception:
        reservations = []
    return reservations

def save_reservations(reservations):
    try:
        with open('data/reservations.txt', 'w') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
        return True
    except Exception:
        return False

# Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Dashboard Route
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    vehicles = load_vehicles()
    # featured_vehicles: list of dict with keys vehicle_id, make, model, daily_rate
    featured_vehicles = []
    for v in vehicles:
        if v['status'] == 'Available':
            featured_vehicles.append({
                'vehicle_id': v['vehicle_id'],
                'make': v['make'],
                'model': v['model'],
                'daily_rate': v['daily_rate']
            })
    # Based on design spec, promotions is list of dicts with title, description
    # We have no file for promotions, so just an empty list 
    promotions = []
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

# Vehicle Search Page
@app.route('/vehicles', methods=['GET'])
def vehicle_search_page():
    vehicles = load_vehicles()
    locations = load_locations()
    # filters dict keys: location(str), vehicle_type(str)
    filters = {
        'location': request.args.get('location', ''),
        'vehicle_type': request.args.get('vehicle_type', '')
    }
    # We won't filter vehicles by location here since no direct linkage in schema
    # But can filter vehicles by vehicle_type if provided
    filtered_vehicles = vehicles
    if filters['vehicle_type']:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == filters['vehicle_type']]
    # The locations are all for filter dropdown
    return render_template('vehicle_search.html', vehicles=filtered_vehicles, locations=locations, filters=filters)

# Vehicle Details Page
@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def vehicle_details_page(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        abort(404)

    # For reviews: list of dicts {reviewer:str, rating:int, comment:str}
    # No data file for reviews given, so empty list
    reviews = []

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

# Booking Page
@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        abort(404)

    locations = load_locations()

    pickup_date = ''
    dropoff_date = ''
    total_price = 0.0

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')

        # Validate dates - should be in YYYY-MM-DD format
        try:
            p_date = datetime.strptime(pickup_date, '%Y-%m-%d')
            d_date = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if d_date < p_date:
                total_price = 0.0
            else:
                days = (d_date - p_date).days
                if days == 0:
                    days = 1
                total_price = days * vehicle['daily_rate']
        except Exception:
            total_price = 0.0

        # For simplicity, we show results on the same page
        return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price)

    # GET: initial
    return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price)

# Insurance Options Page
@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options_page(reservation_id):
    insurance_plans = load_insurance_plans()
    selected_insurance = {}
    # Load reservation to verify
    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    if request.method == 'POST':
        selected_id_str = request.form.get('selected_insurance', '')
        try:
            selected_id = int(selected_id_str)
        except Exception:
            selected_id = None
        selected_insurance = next((i for i in insurance_plans if i['insurance_id'] == selected_id), {})

        # Update reservation insurance_id
        if selected_insurance:
            reservation['insurance_id'] = selected_insurance['insurance_id']
            save_reservations(reservations)

    else:
        selected_insurance = next((i for i in insurance_plans if i['insurance_id'] == reservation['insurance_id']), {})

    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance, reservation_id=reservation_id)

# Rental History Page
@app.route('/rental-history', methods=['GET'])
def rental_history_page():
    rentals = load_rentals()
    filter_status = request.args.get('filter_status', 'All')
    if filter_status != 'All':
        rentals = [r for r in rentals if r['status'] == filter_status]
    return render_template('rental_history.html', rentals=rentals, filter_status=filter_status)

# Reservation Management Page
@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management_page():
    reservations = load_reservations()

    # POST may be to add new reservation (not specified) or no POST processing specified so we ignore POST body
    # Just show current reservations on GET or POST

    return render_template('reservations.html', reservations=reservations)

# Reservation Modify Page
@app.route('/reservation/modify/<int:reservation_id>', methods=['POST'])
def modify_reservation_page(reservation_id):
    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    updated_data = {}
    # We expect form fields for status, insurance_id, special_requests maybe
    status = request.form.get('status')
    insurance_id = request.form.get('insurance_id')
    special_requests = request.form.get('special_requests')

    if status:
        reservation['status'] = status
        updated_data['status'] = status
    if insurance_id:
        try:
            reservation['insurance_id'] = int(insurance_id)
            updated_data['insurance_id'] = int(insurance_id)
        except Exception:
            pass
    if special_requests is not None:
        reservation['special_requests'] = special_requests
        updated_data['special_requests'] = special_requests

    save_reservations(reservations)

    return '', 204

# Reservation Cancel Page
@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation_page(reservation_id):
    reservations = load_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    reservation['status'] = 'Cancelled'
    save_reservations(reservations)
    return '', 204

# Special Requests Page
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests_page():
    reservations = load_reservations()
    submitted_data = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        driver_assistance = 'driver_assistance' in request.form
        gps_option = 'gps_option' in request.form
        child_seat_quantity = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '')

        try:
            reservation_id = int(reservation_id_str)
        except Exception:
            reservation_id = None

        if reservation_id is not None:
            reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
            if reservation:
                # Compose special_requests string
                special_requests_parts = []
                if driver_assistance:
                    special_requests_parts.append('Driver assistance requested')
                if gps_option:
                    special_requests_parts.append('GPS option requested')
                try:
                    qty = int(child_seat_quantity)
                    if qty > 0:
                        special_requests_parts.append(f'Child seats: {qty}')
                except Exception:
                    pass
                if special_notes:
                    special_requests_parts.append(f'Notes: {special_notes}')

                special_requests_str = '; '.join(special_requests_parts)
                reservation['special_requests'] = special_requests_str
                save_reservations(reservations)

                submitted_data = {
                    'reservation_id': reservation_id,
                    'driver_assistance': driver_assistance,
                    'gps_option': gps_option,
                    'child_seat_quantity': child_seat_quantity,
                    'special_notes': special_notes
                }

    return render_template('special_requests.html', reservations=reservations, submitted_data=submitted_data)

# Locations Page
@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
