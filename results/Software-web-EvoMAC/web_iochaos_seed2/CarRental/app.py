'''
Main Flask application for CarRental web application.
Defines routes for all pages as per requirements,
handles reading and writing data from local text files,
and implements core business logic for vehicle search,
booking, reservations, rental history, insurance selection,
special requests, and locations.
No authentication required; all features are directly accessible.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'car_rental_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
# --- Data Reading Functions ---
def read_vehicles():
    vehicles = []
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    if not os.path.exists(path):
        return vehicles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            vehicle = {
                'vehicle_id': parts[0],
                'make': parts[1],
                'model': parts[2],
                'vehicle_type': parts[3],
                'daily_rate': float(parts[4]),
                'seats': parts[5],
                'transmission': parts[6],
                'fuel_type': parts[7],
                'status': parts[8]
            }
            vehicles.append(vehicle)
    return vehicles
def read_customers():
    customers = []
    path = os.path.join(DATA_DIR, 'customers.txt')
    if not os.path.exists(path):
        return customers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            customer = {
                'customer_id': parts[0],
                'name': parts[1],
                'email': parts[2],
                'phone': parts[3],
                'driver_license': parts[4],
                'license_expiry': parts[5]
            }
            customers.append(customer)
    return customers
def read_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            location = {
                'location_id': parts[0],
                'city': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'hours': parts[4],
                'available_vehicles': parts[5]
            }
            locations.append(location)
    return locations
def read_rentals():
    rentals = []
    path = os.path.join(DATA_DIR, 'rentals.txt')
    if not os.path.exists(path):
        return rentals
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            rental = {
                'rental_id': parts[0],
                'vehicle_id': parts[1],
                'customer_id': parts[2],
                'pickup_date': parts[3],
                'dropoff_date': parts[4],
                'pickup_location': parts[5],
                'dropoff_location': parts[6],
                'total_price': float(parts[7]),
                'status': parts[8]
            }
            rentals.append(rental)
    return rentals
def read_insurance():
    insurance_plans = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    if not os.path.exists(path):
        return insurance_plans
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            plan = {
                'insurance_id': parts[0],
                'plan_name': parts[1],
                'description': parts[2],
                'daily_cost': float(parts[3]),
                'coverage_limit': parts[4],
                'deductible': parts[5]
            }
            insurance_plans.append(plan)
    return insurance_plans
def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            reservation = {
                'reservation_id': parts[0],
                'rental_id': parts[1],
                'vehicle_id': parts[2],
                'customer_id': parts[3],
                'status': parts[4],
                'insurance_id': parts[5],
                'special_requests': parts[6]
            }
            reservations.append(reservation)
    return reservations
# --- Data Writing Functions ---
def write_vehicles(vehicles):
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for v in vehicles:
            line = '|'.join([
                v['vehicle_id'],
                v['make'],
                v['model'],
                v['vehicle_type'],
                f"{v['daily_rate']:.2f}",
                v['seats'],
                v['transmission'],
                v['fuel_type'],
                v['status']
            ])
            f.write(line + '\n')
def write_locations(locations):
    path = os.path.join(DATA_DIR, 'locations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for l in locations:
            line = '|'.join([
                l['location_id'],
                l['city'],
                l['address'],
                l['phone'],
                l['hours'],
                l['available_vehicles']
            ])
            f.write(line + '\n')
def write_rentals(rentals):
    path = os.path.join(DATA_DIR, 'rentals.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in rentals:
            line = '|'.join([
                r['rental_id'],
                r['vehicle_id'],
                r['customer_id'],
                r['pickup_date'],
                r['dropoff_date'],
                r['pickup_location'],
                r['dropoff_location'],
                f"{r['total_price']:.2f}",
                r['status']
            ])
            f.write(line + '\n')
def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                r['reservation_id'],
                r['rental_id'],
                r['vehicle_id'],
                r['customer_id'],
                r['status'],
                r['insurance_id'],
                r['special_requests']
            ])
            f.write(line + '\n')
# --- Helper Functions ---
def get_vehicle_by_id(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None
def get_location_by_id(location_id):
    locations = read_locations()
    for l in locations:
        if l['location_id'] == location_id:
            return l
    return None
def get_insurance_by_id(insurance_id):
    plans = read_insurance()
    for p in plans:
        if p['insurance_id'] == insurance_id:
            return p
    return None
def get_reservation_by_id(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None
def get_rental_by_id(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None
def get_customer_by_id(customer_id):
    customers = read_customers()
    for c in customers:
        if c['customer_id'] == customer_id:
            return c
    return None
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None
def calculate_days(pickup_date_str, dropoff_date_str):
    pickup = parse_date(pickup_date_str)
    dropoff = parse_date(dropoff_date_str)
    if pickup and dropoff and dropoff >= pickup:
        return (dropoff - pickup).days + 1
    return 0
def generate_new_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except Exception:
            continue
    return str(max_id + 1)
def filter_vehicles(vehicles, location_city=None, vehicle_type=None, date_range=None):
    # Filter vehicles by availability, location, type, and date range
    filtered = []
    rentals = read_rentals()
    for v in vehicles:
        if v['status'].lower() != 'available':
            continue
        if vehicle_type and vehicle_type.lower() != 'all' and v['vehicle_type'].lower() != vehicle_type.lower():
            continue
        # Location filtering is approximate: check if vehicle is available at location city
        if location_city and location_city.lower() != 'all':
            # We assume vehicle is available at location if any rental pickup_location matches city or vehicle is available
            # Since no direct vehicle-location mapping, we skip strict filtering here
            pass
        # Date range filtering: exclude vehicles with conflicting rentals
        if date_range:
            start_date, end_date = date_range
            conflict = False
            for r in rentals:
                if r['vehicle_id'] == v['vehicle_id'] and r['status'].lower() in ['active', 'confirmed']:
                    r_start = parse_date(r['pickup_date'])
                    r_end = parse_date(r['dropoff_date'])
                    if r_start and r_end:
                        # Check overlap
                        if not (end_date < r_start or start_date > r_end):
                            conflict = True
                            break
            if conflict:
                continue
        filtered.append(v)
    return filtered
# --- Routes ---
@app.route('/')
def dashboard():
    vehicles = read_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'].lower() == 'available'][:3]
    promotions = [
        "10% off rentals longer than 7 days!",
        "Free GPS with every SUV rental this month!",
        "Special: Luxury cars at 20% off!"
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)
@app.route('/vehicle_search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    selected_location = None
    selected_vehicle_type = None
    date_range = None
    filtered_vehicles = vehicles
    if request.method == 'POST':
        selected_location = request.form.get('location-filter')
        selected_vehicle_type = request.form.get('vehicle-type-filter')
        date_range_input = request.form.get('date-range-input')
        start_date = None
        end_date = None
        if date_range_input:
            parts = date_range_input.split(' to ')
            if len(parts) == 2:
                start_date = parse_date(parts[0])
                end_date = parse_date(parts[1])
        if start_date and end_date:
            date_range = (start_date, end_date)
        filtered_vehicles = filter_vehicles(vehicles, location_city=selected_location, vehicle_type=selected_vehicle_type, date_range=date_range)
    else:
        filtered_vehicles = [v for v in vehicles if v['status'].lower() == 'available']
    return render_template('vehicle_search.html',
                           vehicles=filtered_vehicles,
                           locations=locations,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           date_range=request.form.get('date-range-input') if request.method == 'POST' else '')
@app.route('/vehicle_details/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    # For simplicity, no reviews data source, so empty list
    vehicle_reviews = []
    return render_template('vehicle_details.html', vehicle=vehicle, vehicle_reviews=vehicle_reviews)
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    locations = read_locations()
    total_price = None
    pickup_location = None
    dropoff_location = None
    pickup_date = None
    dropoff_date = None
    if request.method == 'POST':
        pickup_location = request.form.get('pickup-location')
        dropoff_location = request.form.get('dropoff-location')
        pickup_date = request.form.get('pickup-date')
        dropoff_date = request.form.get('dropoff-date')
        pd = parse_date(pickup_date)
        dd = parse_date(dropoff_date)
        if not pickup_location or not dropoff_location:
            flash("Please select both pickup and dropoff locations.", "error")
        elif not pickup_date or not dropoff_date:
            flash("Please select both pickup and dropoff dates.", "error")
        elif not pd or not dd or dd < pd:
            flash("Invalid pickup or dropoff dates.", "error")
        else:
            days = calculate_days(pickup_date, dropoff_date)
            total_price = days * vehicle['daily_rate']
            if 'calculate-price-button' in request.form:
                flash(f"Total price calculated: ${total_price:.2f}", "info")
            elif 'proceed-to-insurance-button' in request.form:
                # Pass booking info to insurance options page via query parameters
                return redirect(url_for('insurance_options',
                                        vehicle_id=vehicle_id,
                                        pickup_location=pickup_location,
                                        dropoff_location=dropoff_location,
                                        pickup_date=pickup_date,
                                        dropoff_date=dropoff_date,
                                        total_price=total_price))
    return render_template('booking.html',
                           vehicle=vehicle,
                           locations=locations,
                           total_price=total_price,
                           pickup_location=pickup_location,
                           dropoff_location=dropoff_location,
                           pickup_date=pickup_date,
                           dropoff_date=dropoff_date)
@app.route('/insurance_options', methods=['GET', 'POST'])
def insurance_options():
    insurance_plans = read_insurance()
    vehicle_id = request.args.get('vehicle_id') or request.form.get('vehicle_id')
    pickup_location = request.args.get('pickup_location') or request.form.get('pickup_location')
    dropoff_location = request.args.get('dropoff_location') or request.form.get('dropoff_location')
    pickup_date = request.args.get('pickup_date') or request.form.get('pickup_date')
    dropoff_date = request.args.get('dropoff_date') or request.form.get('dropoff_date')
    total_price = request.args.get('total_price') or request.form.get('total_price')
    if not all([vehicle_id, pickup_location, dropoff_location, pickup_date, dropoff_date, total_price]):
        flash("Missing booking information. Please start again.", "error")
        return redirect(url_for('dashboard'))
    selected_insurance_id = ''
    insurance_description = ''
    insurance_price = 0.0
    if request.method == 'POST':
        selected_insurance_id = request.form.get('selected-insurance')
        if not selected_insurance_id:
            flash("Please select an insurance plan.", "error")
        else:
            plan = get_insurance_by_id(selected_insurance_id)
            if not plan:
                flash("Selected insurance plan not found.", "error")
            else:
                days = calculate_days(pickup_date, dropoff_date)
                insurance_price = plan['daily_cost'] * days
                total_price_float = float(total_price) + insurance_price
                # Read existing data
                rentals = read_rentals()
                reservations = read_reservations()
                customers = read_customers()
                # Use guest customer with id '0' or create if not exists
                guest_customer = next((c for c in customers if c['customer_id'] == '0'), None)
                if not guest_customer:
                    guest_customer = {
                        'customer_id': '0',
                        'name': 'Guest User',
                        'email': '',
                        'phone': '',
                        'driver_license': '',
                        'license_expiry': ''
                    }
                    customers.append(guest_customer)
                    # Append guest customer to file
                    path = os.path.join(DATA_DIR, 'customers.txt')
                    with open(path, 'a', encoding='utf-8') as f:
                        line = '|'.join([
                            guest_customer['customer_id'],
                            guest_customer['name'],
                            guest_customer['email'],
                            guest_customer['phone'],
                            guest_customer['driver_license'],
                            guest_customer['license_expiry']
                        ])
                        f.write(line + '\n')
                new_rental_id = generate_new_id(rentals, 'rental_id')
                new_reservation_id = generate_new_id(reservations, 'reservation_id')
                new_rental = {
                    'rental_id': new_rental_id,
                    'vehicle_id': vehicle_id,
                    'customer_id': guest_customer['customer_id'],
                    'pickup_date': pickup_date,
                    'dropoff_date': dropoff_date,
                    'pickup_location': pickup_location,
                    'dropoff_location': dropoff_location,
                    'total_price': total_price_float,
                    'status': 'Active'
                }
                rentals.append(new_rental)
                write_rentals(rentals)
                new_reservation = {
                    'reservation_id': new_reservation_id,
                    'rental_id': new_rental_id,
                    'vehicle_id': vehicle_id,
                    'customer_id': guest_customer['customer_id'],
                    'status': 'Confirmed',
                    'insurance_id': selected_insurance_id,
                    'special_requests': ''
                }
                reservations.append(new_reservation)
                write_reservations(reservations)
                # Update vehicle status to 'Rented'
                vehicles = read_vehicles()
                for v in vehicles:
                    if v['vehicle_id'] == vehicle_id:
                        v['status'] = 'Rented'
                        break
                write_vehicles(vehicles)
                flash("Booking successful! Your reservation is confirmed.", "success")
                return redirect(url_for('dashboard'))
    if selected_insurance_id:
        plan = get_insurance_by_id(selected_insurance_id)
        if plan:
            insurance_description = plan['description']
            days = calculate_days(pickup_date, dropoff_date)
            insurance_price = plan['daily_cost'] * days
    return render_template('insurance_options.html',
                           insurance_plans=insurance_plans,
                           selected_insurance_id=selected_insurance_id,
                           insurance_description=insurance_description,
                           insurance_price=insurance_price,
                           vehicle_id=vehicle_id,
                           pickup_location=pickup_location,
                           dropoff_location=dropoff_location,
                           pickup_date=pickup_date,
                           dropoff_date=dropoff_date,
                           total_price=total_price)
@app.route('/rental_history', methods=['GET', 'POST'])
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()
    customers = read_customers()
    status_filter = request.form.get('status-filter', 'All') if request.method == 'POST' else 'All'
    filtered_rentals = []
    for r in rentals:
        if status_filter != 'All' and r['status'].lower() != status_filter.lower():
            continue
        vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
        customer = next((c for c in customers if c['customer_id'] == r['customer_id']), None)
        rental_info = r.copy()
        rental_info['vehicle'] = vehicle['make'] + ' ' + vehicle['model'] if vehicle else 'Unknown'
        rental_info['customer_name'] = customer['name'] if customer else 'Unknown'
        filtered_rentals.append(rental_info)
    return render_template('rental_history.html',
                           rentals=filtered_rentals,
                           status_filter=status_filter)
@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = read_reservations()
    rentals = read_rentals()
    vehicles = read_vehicles()
    sort_by_date = request.args.get('sort-by-date', 'no')
    enriched_reservations = []
    for r in reservations:
        vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
        rental = next((rent for rent in rentals if rent['rental_id'] == r['rental_id']), None)
        res_info = r.copy()
        res_info['vehicle'] = vehicle['make'] + ' ' + vehicle['model'] if vehicle else 'Unknown'
        res_info['pickup_date'] = rental['pickup_date'] if rental else ''
        enriched_reservations.append(res_info)
    if sort_by_date.lower() == 'yes':
        enriched_reservations.sort(key=lambda x: parse_date(x['pickup_date']) or datetime.min)
    if request.method == 'POST':
        # Handle modify or cancel reservation buttons
        for key in request.form:
            if key.startswith('modify-reservation-button-'):
                reservation_id = key.replace('modify-reservation-button-', '')
                flash(f"Modify reservation {reservation_id} feature is not implemented yet.", "info")
                return redirect(url_for('my_reservations'))
            elif key.startswith('cancel-reservation-button-'):
                reservation_id = key.replace('cancel-reservation-button-', '')
                for r in reservations:
                    if r['reservation_id'] == reservation_id:
                        r['status'] = 'Cancelled'
                        write_reservations(reservations)
                        flash(f"Reservation {reservation_id} cancelled successfully.", "success")
                        return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=enriched_reservations)
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    if not reservations:
        flash("No reservations available to add requests.", "error")
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        selected_reservation_id = request.form.get('select-reservation')
        gps_option = request.form.get('gps-option-checkbox')
        driver_assistance = request.form.get('driver-assistance-checkbox')
        child_seat_quantity = request.form.get('child-seat-quantity', '0')
        special_notes = request.form.get('special-notes', '').strip()
        if not selected_reservation_id:
            flash("Please select a reservation to add requests.", "error")
            return redirect(url_for('special_requests'))
        reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
        if not reservation:
            flash("Selected reservation not found.", "error")
            return redirect(url_for('special_requests'))
        requests_list = []
        if driver_assistance:
            requests_list.append("Driver assistance requested")
        if gps_option:
            requests_list.append("GPS requested")
        if child_seat_quantity.isdigit() and int(child_seat_quantity) > 0:
            requests_list.append(f"Child seats: {child_seat_quantity}")
        if special_notes:
            requests_list.append(f"Notes: {special_notes}")
        reservation['special_requests'] = '; '.join(requests_list)
        write_reservations(reservations)
        flash("Special requests updated successfully.", "success")
        return redirect(url_for('my_reservations'))
    return render_template('special_requests.html', reservations=reservations)
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    locations = read_locations()
    hours_filter = 'All'
    search_input = ''
    if request.method == 'POST':
        hours_filter = request.form.get('hours-filter', 'All')
        search_input = request.form.get('search-location-input', '').strip()
    filtered_locations = locations
    if hours_filter != 'All':
        filtered_locations = [l for l in filtered_locations if l['hours'].lower() == hours_filter.lower()]
    if search_input:
        filtered_locations = [l for l in filtered_locations if search_input.lower() in l['city'].lower() or search_input.lower() in l['address'].lower()]
    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter=hours_filter,
                           search_input=search_input)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)