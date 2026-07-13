from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Utility functions to read/write data files

def read_vehicles():
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    vehicles = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 9:
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
    return vehicles

def read_customers():
    path = os.path.join(DATA_DIR, 'customers.txt')
    customers = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                customers.append({
                    'customer_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'driver_license': parts[4],
                    'license_expiry': parts[5]
                })
    return customers

def read_locations():
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                locations.append({
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                })
    return locations

def read_rentals():
    path = os.path.join(DATA_DIR, 'rentals.txt')
    rentals = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 9:
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
    return rentals

def write_rentals(rentals):
    path = os.path.join(DATA_DIR, 'rentals.txt')
    lines = []
    for r in rentals:
        line = '|'.join([str(r['rental_id']), str(r['vehicle_id']), str(r['customer_id']), r['pickup_date'], r['dropoff_date'], r['pickup_location'], r['dropoff_location'], f"{r['total_price']:.2f}", r['status']])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

def read_insurance():
    path = os.path.join(DATA_DIR, 'insurance.txt')
    insurance = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                insurance.append({
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': parts[5]
                })
    return insurance

def read_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 7:
                insurance_id = int(parts[5]) if parts[5].isdigit() else None
                reservations.append({
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': insurance_id,
                    'special_requests': parts[6]
                })
    return reservations

def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    lines = []
    for r in reservations:
        insurance_id = str(r['insurance_id']) if r['insurance_id'] is not None else ''
        line = '|'.join([str(r['reservation_id']), str(r['rental_id']), str(r['vehicle_id']), str(r['customer_id']), r['status'], insurance_id, r['special_requests']])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# Helper to get next unique ID

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

def get_vehicle(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None

def get_rental(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None

def get_reservation(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None

def get_customer():
    customers = read_customers()
    if customers:
        return customers[0]  # Since no auth, return first customer
    return None

# --- Flask routes ---

@app.route('/')
@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    featured = [v for v in vehicles if v['status'] == 'Available'][:3]
    promotions = ["Winter Special: 20% off!", "Book 3 days, get 1 day free!", "New luxury models added!"]
    return render_template('dashboard.html', featured_vehicles=featured, promotions=promotions)

@app.route('/search-vehicles', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    filter_location = ''
    filter_type = 'All'
    filter_dates = ''

    filtered = [v for v in vehicles if v['status'] == 'Available']

    if request.method == 'POST':
        filter_location = request.form.get('location_filter', '').strip()
        filter_type = request.form.get('vehicle_type_filter', 'All')
        filter_dates = request.form.get('date_range_input', '')

        if filter_type != 'All':
            filtered = [v for v in filtered if v['vehicle_type'] == filter_type]
        # Location filter not active because no vehicle-location mapping

    return render_template('search-vehicles.html', vehicles=filtered, locations=locations, vehicle_types=vehicle_types, filter_location=filter_location, filter_type=filter_type, filter_dates=filter_dates)

@app.route('/vehicle-details/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        flash('Vehicle not found.', 'error')
        return redirect(url_for('vehicle_search'))
    # Static sample reviews
    reviews = [
        {'user': 'User1', 'comment': 'Great vehicle! Smooth ride.'},
        {'user': 'User2', 'comment': 'Comfortable and efficient.'}
    ]
    return render_template('vehicle-details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle(vehicle_id)
    if not vehicle:
        flash('Vehicle not found.', 'error')
        return redirect(url_for('vehicle_search'))

    locations = read_locations()
    error = None
    total_price = None

    pickup_location = ''
    dropoff_location = ''
    pickup_date = ''
    dropoff_date = ''

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')

        if not pickup_location or not dropoff_location:
            error = 'Pickup and dropoff locations must be selected.'
        else:
            try:
                dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                if dt_dropoff < dt_pickup:
                    error = 'Dropoff date must be after pickup date.'
            except Exception:
                error = 'Invalid date format.'

        if not error:
            days = (dt_dropoff - dt_pickup).days + 1
            total_price = days * vehicle['daily_rate']
            if 'calculate_price' in request.form:
                flash(f'Total price calculated: ${total_price:.2f}', 'info')
            elif 'proceed_insurance' in request.form:
                # Create Rental and Reservation entries
                customer = get_customer()
                rentals = read_rentals()
                reservations = read_reservations()

                new_rental_id = get_next_id(rentals, 'rental_id')
                new_reservation_id = get_next_id(reservations, 'reservation_id')

                new_rental = {
                    'rental_id': new_rental_id,
                    'vehicle_id': vehicle['vehicle_id'],
                    'customer_id': customer['customer_id'] if customer else 0,
                    'pickup_date': dt_pickup.strftime('%Y-%m-%d'),
                    'dropoff_date': dt_dropoff.strftime('%Y-%m-%d'),
                    'pickup_location': pickup_location,
                    'dropoff_location': dropoff_location,
                    'total_price': total_price,
                    'status': 'Pending'
                }
                rentals.append(new_rental)
                write_rentals(rentals)

                new_reservation = {
                    'reservation_id': new_reservation_id,
                    'rental_id': new_rental_id,
                    'vehicle_id': vehicle['vehicle_id'],
                    'customer_id': customer['customer_id'] if customer else 0,
                    'status': 'Pending',
                    'insurance_id': None,
                    'special_requests': ''
                }
                reservations.append(new_reservation)
                write_reservations(reservations)

                return redirect(url_for('insurance_options', reservation_id=new_reservation_id))

    return render_template('booking.html', vehicle=vehicle, locations=locations, error_msg=error, total_price=total_price,
                           pickup_location=pickup_location, dropoff_location=dropoff_location, pickup_date=pickup_date, dropoff_date=dropoff_date)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    reservation = get_reservation(reservation_id)
    if not reservation:
        flash('Reservation not found.', 'error')
        return redirect(url_for('reservations'))

    rental = get_rental(reservation['rental_id'])
    if not rental:
        flash('Rental not found.', 'error')
        return redirect(url_for('reservations'))

    insurance_plans = read_insurance()

    dt_pickup = datetime.strptime(rental['pickup_date'], '%Y-%m-%d')
    dt_dropoff = datetime.strptime(rental['dropoff_date'], '%Y-%m-%d')
    days = (dt_dropoff - dt_pickup).days + 1

    insurance_desc = ''
    insurance_price = 0
    selected_insurance_id = reservation['insurance_id']

    if request.method == 'POST':
        selected_insurance_id = int(request.form.get('insurance_option'))
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)

        if selected_plan:
            insurance_desc = selected_plan['description']
            insurance_price = selected_plan['daily_cost'] * days
            # Update reservation
            reservations = read_reservations()
            rentals = read_rentals()
            for r in reservations:
                if r['reservation_id'] == reservation_id:
                    r['insurance_id'] = selected_insurance_id
                    r['status'] = 'Confirmed'
            for rent in rentals:
                if rent['rental_id'] == reservation['rental_id']:
                    rent['status'] = 'Active'
            write_reservations(reservations)
            write_rentals(rentals)

            flash('Booking confirmed with insurance.', 'success')
            return redirect(url_for('reservations'))

    else:
        if selected_insurance_id:
            plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
            if plan:
                insurance_desc = plan['description']
                insurance_price = plan['daily_cost'] * days

    return render_template('insurance.html', reservation=reservation, insurance_plans=insurance_plans,
                           insurance_description=insurance_desc, insurance_price=insurance_price, rental_days=days)

@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    status_filter = request.args.get('status_filter', 'All')
    if status_filter != 'All':
        rentals = [r for r in rentals if r['status'] == status_filter]

    return render_template('rental-history.html', rentals=rentals, vehicles=vehicles, filter_status=status_filter)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    reservations = read_reservations()
    rentals = {r['rental_id']: r for r in read_rentals()}
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}

    if request.method == 'POST':
        action = request.form.get('action')
        reservation_id = int(request.form.get('reservation_id', 0))
        if action == 'modify':
            new_status = request.form.get('new_status', '').strip()
            data = read_reservations()
            for r in data:
                if r['reservation_id'] == reservation_id:
                    if new_status:
                        r['status'] = new_status
                    break
            write_reservations(data)
            flash('Reservation updated.', 'success')
        elif action == 'cancel':
            data = read_reservations()
            rentals_data = read_rentals()
            for r in data:
                if r['reservation_id'] == reservation_id:
                    r['status'] = 'Cancelled'
                    # Also update rental
                    for rent in rentals_data:
                        if rent['rental_id'] == r['rental_id']:
                            rent['status'] = 'Cancelled'
                    break
            write_reservations(data)
            write_rentals(rentals_data)
            flash('Reservation cancelled.', 'success')
        elif action == 'sort_date':
            # Sort reservations by rental pickup date
            rental_list = read_rentals()
            res_with_rental = []
            for res in reservations:
                rental = next((r for r in rental_list if r['rental_id'] == res['rental_id']), None)
                if rental:
                    res_with_rental.append((res, rental['pickup_date']))
                else:
                    res_with_rental.append((res, ''))
            res_with_rental.sort(key=lambda x: x[1])
            reservations = [r[0] for r in res_with_rental]

    return render_template('reservations.html', reservations=reservations, rentals=rentals, vehicles=vehicles)

@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()

    if request.method == 'POST':
        reservation_id = int(request.form.get('select_reservation', 0))
        driver_assist = request.form.get('driver_assistance_checkbox') == 'on'
        gps_option = request.form.get('gps_option_checkbox') == 'on'
        child_seats_str = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '').strip()

        requests = []
        if driver_assist:
            requests.append('Driver assistance requested')
        if gps_option:
            requests.append('GPS requested')
        try:
            child_seats = int(child_seats_str)
            if child_seats > 0:
                requests.append(f'Child seats: {child_seats}')
        except:
            pass
        if special_notes:
            requests.append(f'Notes: {special_notes}')

        full_request = '; '.join(requests)

        data = read_reservations()
        for r in data:
            if r['reservation_id'] == reservation_id:
                r['special_requests'] = full_request
                break
        write_reservations(data)

        flash('Special requests submitted.', 'success')

    return render_template('special-requests.html', reservations=reservations)

@app.route('/locations', methods=['GET'])
def locations():
    locations = read_locations()
    filter_hours = request.args.get('hours_filter', 'All')
    search_query = request.args.get('search_location_input', '').lower().strip()

    filtered = locations
    if filter_hours != 'All':
        filtered = [l for l in filtered if l['hours'] == filter_hours]

    if search_query:
        filtered = [l for l in filtered if search_query in l['city'].lower() or search_query in l['address'].lower()]

    return render_template('locations.html', locations=filtered, filter_hours=filter_hours, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
