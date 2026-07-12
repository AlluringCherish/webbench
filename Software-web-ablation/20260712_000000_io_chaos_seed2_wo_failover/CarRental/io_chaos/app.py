from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read and write pipe-delimited files

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


def read_insurance():
    insurance_plans = []
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
                insurance_plans.append(plan)
    except Exception:
        pass
    return insurance_plans


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
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                }
                reservations.append(reservation)
    except Exception:
        pass
    return reservations


def write_reservations(reservations):
    lines = []
    for r in reservations:
        line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}"
        lines.append(line)
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception:
        pass

# Route / -> redirect to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

# Route /dashboard GET
@app.route('/dashboard')
def dashboard_page():
    vehicles = read_vehicles()
    featured_vehicles = []
    # Select featured vehicles (e.g. first 5 available vehicles)
    count = 0
    for v in vehicles:
        if v['status'] == 'Available':
            featured_vehicles.append({'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']})
            count += 1
            if count >= 5:
                break
    promotions = [
        "Winter special: 20% off SUVs",
        "Free GPS rental with any booking over 3 days",
        "Loyalty program: Earn double points this month"
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

# Route /search GET
@app.route('/search')
def search_vehicles():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = sorted(set(v['vehicle_type'] for v in vehicles))

    selected_location = request.args.get('location', '')
    selected_vehicle_type = request.args.get('vehicle_type', '')

    # Filter vehicles by selected criteria
    filtered_vehicles = []
    for v in vehicles:
        if v['status'] != 'Available':
            continue
        if selected_location:
            # check if vehicle location matches selected (approximate logic: if location city in pickup location)
            # but no rental location info on vehicle, so we'll skip this filter or just show all
            pass
        if selected_vehicle_type and v['vehicle_type'] != selected_vehicle_type:
            continue
        filtered_vehicles.append({'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']})

    return render_template('search.html', 
                           locations=locations, 
                           vehicle_types=vehicle_types,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           vehicles=filtered_vehicles)

# Route /vehicle/<int:vehicle_id> GET
@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        abort(404)

    # For simplicity, generate dummy reviews as no review data specified
    reviews = [
        {'reviewer': 'John Doe', 'rating': 4, 'comment': 'Good vehicle and comfortable.'},
        {'reviewer': 'Mary Smith', 'rating': 5, 'comment': 'Excellent performance!'},
    ]
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

# Route /booking/<int:vehicle_id> GET, POST
@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking_page(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id and v['status'] == 'Available'), None)
    if not vehicle:
        abort(404)
    locations = read_locations()
    pickup_date = ''
    dropoff_date = ''
    total_price = 0.0

    if request.method == 'POST':
        pickup_location_id = request.form.get('pickup_location')
        dropoff_location_id = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        # Validate dates
        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dropoff_dt < pickup_dt:
                raise ValueError
        except Exception:
            return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price, error='Invalid date range')

        # Check locations
        pickup_location = next((loc for loc in locations if str(loc['location_id']) == pickup_location_id), None)
        dropoff_location = next((loc for loc in locations if str(loc['location_id']) == dropoff_location_id), None)
        if not pickup_location or not dropoff_location:
            return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price, error='Invalid pickup or dropoff location')

        # Calculate total price = daily_rate * days
        days = (dropoff_dt - pickup_dt).days + 1
        total_price = vehicle['daily_rate'] * days

        # Save a rental record and reservation?
        # Since design does not specify customer input or creation, we skip saving customer or rental here.

    return render_template('booking.html', vehicle=vehicle, locations=locations, pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price)


# Route /insurance/<int:reservation_id> GET, POST
@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance()
    selected_insurance_id = None
    insurance_description = ''
    insurance_price = 0.0

    if request.method == 'POST':
        selected_insurance_id_str = request.form.get('selected_insurance_id')
        if selected_insurance_id_str is not None:
            try:
                selected_insurance_id = int(selected_insurance_id_str)
                plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
                if plan:
                    insurance_description = plan['description']
                    insurance_price = plan['daily_cost']
                    # In a real app, we'd update reservation with insurance and confirm booking
                    # Here, just redirect to dashboard
                    return redirect(url_for('dashboard_page'))
            except Exception:
                pass
    else:
        # On GET, show first plan by default if any
        if insurance_plans:
            selected_insurance_id = insurance_plans[0]['insurance_id']
            insurance_description = insurance_plans[0]['description']
            insurance_price = insurance_plans[0]['daily_cost']

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_insurance_id=selected_insurance_id, insurance_description=insurance_description, insurance_price=insurance_price, reservation_id=reservation_id)

# Route /history GET
@app.route('/history')
def rental_history():
    rentals = read_rentals()
    filter_status = request.args.get('status', '')
    if filter_status:
        filtered_rentals = [r for r in rentals if r['status'].lower() == filter_status.lower()]
    else:
        filtered_rentals = rentals

    # Enrich rental with vehicle name
    vehicles = read_vehicles()
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}
    results = []
    for r in filtered_rentals:
        vehicle_name = vehicle_map.get(r['vehicle_id'], 'Unknown')
        result = r.copy()
        result['vehicle'] = vehicle_name
        results.append(result)

    return render_template('rental_history.html', rentals=results, filter_status=filter_status)

# Route /reservations GET
@app.route('/reservations')
def reservations_management():
    reservations = read_reservations()
    vehicles = read_vehicles()
    rentals = read_rentals()
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}

    enriched_reservations = []
    for r in reservations:
        vehicle_name = vehicle_map.get(r['vehicle_id'], 'Unknown')
        enriched = r.copy()
        enriched['vehicle'] = vehicle_name
        enriched_reservations.append(enriched)

    return render_template('reservations.html', reservations=enriched_reservations)

# Route /reservation/modify/<int:reservation_id> POST
@app.route('/reservation/modify/<int:reservation_id>', methods=['POST'])
def modify_reservation(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        abort(404)

    # Expect modifications in form keys, update reservation accordingly
    modifications = {}
    # Example: status, insurance_id, special_requests
    status = request.form.get('status')
    if status:
        reservation['status'] = status
        modifications['status'] = status
    insurance_id = request.form.get('insurance_id')
    if insurance_id:
        try:
            reservation['insurance_id'] = int(insurance_id)
            modifications['insurance_id'] = int(insurance_id)
        except Exception:
            pass
    special_requests = request.form.get('special_requests')
    if special_requests is not None:
        reservation['special_requests'] = special_requests
        modifications['special_requests'] = special_requests

    write_reservations(reservations)
    return '', 204

# Route /reservation/cancel/<int:reservation_id> POST
@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        abort(404)
    reservation['status'] = 'Cancelled'
    write_reservations(reservations)
    return '', 204

# Route /special_requests GET, POST
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    vehicles = read_vehicles()
    rentals = read_rentals()
    # Enrich reservations to have vehicle name
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}

    enriched_reservations = []
    for r in reservations:
        if r['status'] in ['Confirmed', 'Active']:
            enriched = r.copy()
            enriched['vehicle'] = vehicle_map.get(r['vehicle_id'], 'Unknown')
            enriched_reservations.append(enriched)

    selected_reservation_id = None
    requests_data = {
        'driver_assistance': False,
        'gps_option': False,
        'child_seat_quantity': 0,
        'special_notes': ''
    }

    if request.method == 'POST':
        selected_reservation_id_str = request.form.get('reservation_id')
        if selected_reservation_id_str:
            try:
                selected_reservation_id = int(selected_reservation_id_str)
            except Exception:
                selected_reservation_id = None

        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        child_seat_quantity_str = request.form.get('child_seat_quantity', '0')
        try:
            child_seat_quantity = int(child_seat_quantity_str)
        except Exception:
            child_seat_quantity = 0
        special_notes = request.form.get('special_notes', '')

        # Update special requests string for selected reservation
        if selected_reservation_id is not None:
            reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
            if reservation:
                special_reqs_lines = []
                if driver_assistance:
                    special_reqs_lines.append('Driver assistance requested')
                if gps_option:
                    special_reqs_lines.append('GPS option requested')
                if child_seat_quantity > 0:
                    special_reqs_lines.append(f'Child seats: {child_seat_quantity}')
                if special_notes.strip():
                    special_reqs_lines.append(f'Notes: {special_notes.strip()}')
                special_requests_str = '; '.join(special_reqs_lines) if special_reqs_lines else ''
                reservation['special_requests'] = special_requests_str
                write_reservations(reservations)

        requests_data = {
            'driver_assistance': driver_assistance,
            'gps_option': gps_option,
            'child_seat_quantity': child_seat_quantity,
            'special_notes': special_notes
        }

    return render_template('special_requests.html', reservations=enriched_reservations, selected_reservation_id=selected_reservation_id, requests_data=requests_data)

# Route /locations GET
@app.route('/locations')
def locations_page():
    locations = read_locations()
    filter_hours = request.args.get('filter_hours', '')
    search_query = request.args.get('search_query', '').strip().lower()

    filtered_locations = []
    for loc in locations:
        if filter_hours and loc['hours'] != filter_hours:
            continue
        if search_query and search_query not in loc['city'].lower() and search_query not in loc['address'].lower():
            continue
        filtered_locations.append(loc)

    return render_template('locations.html', locations=filtered_locations, filter_hours=filter_hours, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
