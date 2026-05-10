'''
Backend implementation for the 'CarRental' web application.
Provides routing and data handling for all pages and functionalities as specified.
Uses Flask framework, reads and writes data from/to local text files in 'data' directory.
Website accessible on local port 5000, starting at '/' route (Dashboard page).
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'evomac_secret_key_for_sessions'
DATA_DIR = 'data'
# Utility functions to read and write data files
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
# Helper to get next ID for rentals and reservations
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
# Route: Dashboard page
@app.route('/')
def dashboard():
    vehicles = read_vehicles()
    # Featured vehicles: pick first 3 available vehicles as example
    featured = [v for v in vehicles if v['status'].lower() == 'available'][:3]
    promotions = [
        "10% off on all SUV rentals this weekend!",
        "Free GPS with every Luxury car booking!",
        "Book 3 days, get 1 day free on Economy cars."
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured,
                           promotions=promotions)
# Route: Vehicle Search page
@app.route('/search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    # Filters from request args or form
    selected_location = request.args.get('location_filter', '')
    selected_type = request.args.get('vehicle_type_filter', '')
    date_range = request.args.get('date_range_input', '')
    filtered_vehicles = [v for v in vehicles if v['status'].lower() == 'available']
    if selected_location:
        # Filter vehicles by availability at location
        # Since vehicles.txt does not have location info, we assume all vehicles available at all locations
        # So no filtering by location on vehicles, but we keep the filter for UI
        pass
    if selected_type:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'].lower() == selected_type.lower()]
    # date_range is not used to filter vehicles here because availability by date is not specified in data
    # Could be extended to check rentals overlapping dates
    return render_template('vehicle_search.html',
                           vehicles=filtered_vehicles,
                           locations=locations,
                           selected_location=selected_location,
                           selected_type=selected_type,
                           date_range=date_range)
# Route: Vehicle Details page
@app.route('/vehicle/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    # Vehicle specs: engine is not in data, so we omit or fake it
    vehicle_specs = {
        'seats': vehicle['seats'],
        'transmission': vehicle['transmission'],
        'fuel_type': vehicle['fuel_type']
    }
    # Reviews: no data file for reviews, so we show static example reviews
    vehicle_reviews = [
        {"author": "John D.", "comment": "Great car, very comfortable."},
        {"author": "Emily R.", "comment": "Smooth ride and fuel efficient."}
    ]
    return render_template('vehicle_details.html',
                           vehicle=vehicle,
                           vehicle_specs=vehicle_specs,
                           vehicle_reviews=vehicle_reviews)
# Route: Booking page
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    locations = read_locations()
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')
        action = request.form.get('action', '')
        # Validate dates
        try:
            pd = datetime.strptime(pickup_date, '%Y-%m-%d')
            dd = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dd < pd:
                flash("Dropoff date must be after pickup date.", "error")
                return render_template('booking.html', vehicle=vehicle, locations=locations)
        except Exception:
            flash("Invalid date format. Use YYYY-MM-DD.", "error")
            return render_template('booking.html', vehicle=vehicle, locations=locations)
        # Calculate price if requested
        total_price = None
        if action == 'calculate_price':
            days = (dd - pd).days + 1
            total_price = days * vehicle['daily_rate']
            return render_template('booking.html', vehicle=vehicle, locations=locations,
                                   pickup_location=pickup_location,
                                   dropoff_location=dropoff_location,
                                   pickup_date=pickup_date,
                                   dropoff_date=dropoff_date,
                                   total_price=total_price)
        # Proceed to insurance selection
        if action == 'proceed_to_insurance':
            # Save booking info temporarily in session or pass via query parameters
            # Since no authentication, we use query parameters for simplicity
            # Pass vehicle_id, pickup_location, dropoff_location, pickup_date, dropoff_date, total_price
            days = (dd - pd).days + 1
            total_price = days * vehicle['daily_rate']
            return redirect(url_for('insurance_options',
                                    vehicle_id=vehicle_id,
                                    pickup_location=pickup_location,
                                    dropoff_location=dropoff_location,
                                    pickup_date=pickup_date,
                                    dropoff_date=dropoff_date,
                                    total_price=total_price))
    else:
        # GET request
        return render_template('booking.html', vehicle=vehicle, locations=locations)
# Route: Insurance Options page
@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options():
    insurance_plans = read_insurance()
    # Retrieve booking info from query parameters or form hidden fields
    vehicle_id = request.args.get('vehicle_id') or request.form.get('vehicle_id')
    pickup_location = request.args.get('pickup_location') or request.form.get('pickup_location')
    dropoff_location = request.args.get('dropoff_location') or request.form.get('dropoff_location')
    pickup_date = request.args.get('pickup_date') or request.form.get('pickup_date')
    dropoff_date = request.args.get('dropoff_date') or request.form.get('dropoff_date')
    total_price_str = request.args.get('total_price') or request.form.get('total_price')
    if not all([vehicle_id, pickup_location, dropoff_location, pickup_date, dropoff_date, total_price_str]):
        flash("Missing booking information. Please start booking again.", "error")
        return redirect(url_for('dashboard'))
    try:
        total_price = float(total_price_str)
    except:
        total_price = 0.0
    # Calculate rental days and pass to template
    try:
        pd = datetime.strptime(pickup_date, '%Y-%m-%d')
        dd = datetime.strptime(dropoff_date, '%Y-%m-%d')
        rental_days = (dd - pd).days + 1
        if rental_days < 1:
            rental_days = 1
    except:
        rental_days = 1
    selected_insurance_id = None
    insurance_description = ''
    insurance_price = 0.0
    if request.method == 'POST':
        selected_insurance_id = request.form.get('selected_insurance')
        if not selected_insurance_id:
            flash("Please select an insurance plan.", "error")
            return render_template('insurance_options.html',
                                   insurance_plans=insurance_plans,
                                   vehicle_id=vehicle_id,
                                   pickup_location=pickup_location,
                                   dropoff_location=dropoff_location,
                                   pickup_date=pickup_date,
                                   dropoff_date=dropoff_date,
                                   total_price=total_price,
                                   rental_days=rental_days,
                                   insurance_description=insurance_description,
                                   insurance_price=insurance_price,
                                   selected_insurance_id=selected_insurance_id)
        # Find selected insurance plan
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
        if not selected_plan:
            flash("Selected insurance plan not found.", "error")
            return render_template('insurance_options.html',
                                   insurance_plans=insurance_plans,
                                   vehicle_id=vehicle_id,
                                   pickup_location=pickup_location,
                                   dropoff_location=dropoff_location,
                                   pickup_date=pickup_date,
                                   dropoff_date=dropoff_date,
                                   total_price=total_price,
                                   rental_days=rental_days,
                                   insurance_description=insurance_description,
                                   insurance_price=insurance_price,
                                   selected_insurance_id=selected_insurance_id)
        # Calculate total rental days
        insurance_cost = rental_days * selected_plan['daily_cost']
        final_price = total_price + insurance_cost
        # Create new rental and reservation entries
        rentals = read_rentals()
        reservations = read_reservations()
        customers = read_customers()
        vehicles = read_vehicles()
        # Since no authentication, assign a default customer or create a dummy customer
        # For demo, create a dummy customer with id=0
        customer_id = '0'
        # Generate new rental_id and reservation_id
        new_rental_id = get_next_id(rentals, 'rental_id')
        new_reservation_id = get_next_id(reservations, 'reservation_id')
        # Create rental record
        rental_record = {
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': final_price,
            'status': 'Active'
        }
        rentals.append(rental_record)
        write_rentals(rentals)
        # Create reservation record
        reservation_record = {
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'status': 'Confirmed',
            'insurance_id': selected_insurance_id,
            'special_requests': ''
        }
        reservations.append(reservation_record)
        write_reservations(reservations)
        flash(f"Booking confirmed! Total price: ${final_price:.2f}", "success")
        return redirect(url_for('dashboard'))
    # GET request: show insurance options
    return render_template('insurance_options.html',
                           insurance_plans=insurance_plans,
                           vehicle_id=vehicle_id,
                           pickup_location=pickup_location,
                           dropoff_location=dropoff_location,
                           pickup_date=pickup_date,
                           dropoff_date=dropoff_date,
                           total_price=total_price,
                           rental_days=rental_days,
                           insurance_description=insurance_description,
                           insurance_price=insurance_price,
                           selected_insurance_id=selected_insurance_id)
# Route: Rental History page
@app.route('/history', methods=['GET'])
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()
    # No authentication, so show all rentals
    status_filter = request.args.get('status_filter', 'All').lower()
    filtered_rentals = rentals
    if status_filter != 'all':
        filtered_rentals = [r for r in rentals if r['status'].lower() == status_filter]
    # Enrich rentals with vehicle info
    for r in filtered_rentals:
        vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
        r['vehicle_display'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else "Unknown"
    return render_template('rental_history.html',
                           rentals=filtered_rentals,
                           status_filter=status_filter.capitalize())
# Route: View rental details (from rental history)
@app.route('/rental/<rental_id>')
def rental_details(rental_id):
    rentals = read_rentals()
    vehicles = read_vehicles()
    rental = next((r for r in rentals if r['rental_id'] == rental_id), None)
    if not rental:
        flash("Rental not found.", "error")
        return redirect(url_for('rental_history'))
    vehicle = next((v for v in vehicles if v['vehicle_id'] == rental['vehicle_id']), None)
    return render_template('rental_details.html',
                           rental=rental,
                           vehicle=vehicle)
# Route: Reservation Management page
@app.route('/reservations', methods=['GET', 'POST'])
def reservations_page():
    reservations = read_reservations()
    rentals = read_rentals()
    vehicles = read_vehicles()
    # Enrich reservations with vehicle and rental info
    for res in reservations:
        vehicle = next((v for v in vehicles if v['vehicle_id'] == res['vehicle_id']), None)
        rental = next((r for r in rentals if r['rental_id'] == res['rental_id']), None)
        res['vehicle_display'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else "Unknown"
        res['pickup_date'] = rental['pickup_date'] if rental else ''
        res['dropoff_date'] = rental['dropoff_date'] if rental else ''
        res['rental_status'] = rental['status'] if rental else ''
    if request.method == 'POST':
        # Handle modify or cancel reservation
        action = request.form.get('action')
        reservation_id = request.form.get('reservation_id')
        if not reservation_id:
            flash("Reservation ID missing.", "error")
            return redirect(url_for('reservations_page'))
        reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
        if not reservation:
            flash("Reservation not found.", "error")
            return redirect(url_for('reservations_page'))
        if action == 'cancel':
            # Cancel reservation and associated rental
            reservation['status'] = 'Cancelled'
            rentals = read_rentals()
            rental = next((r for r in rentals if r['rental_id'] == reservation['rental_id']), None)
            if rental:
                rental['status'] = 'Cancelled'
                write_rentals(rentals)
            write_reservations(reservations)
            flash("Reservation cancelled.", "success")
            return redirect(url_for('reservations_page'))
        elif action == 'modify':
            # For simplicity, redirect to booking page for the vehicle to modify dates/locations
            # We pass vehicle_id and reservation_id for context
            return redirect(url_for('booking', vehicle_id=reservation['vehicle_id']))
    # GET request: show reservations
    sort_by_date = request.args.get('sort_by_date', 'no')
    if sort_by_date == 'yes':
        reservations.sort(key=lambda r: r['pickup_date'])
    return render_template('reservations.html',
                           reservations=reservations)
# Route: Special Requests page
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    if request.method == 'POST':
        selected_reservation_id = request.form.get('select_reservation')
        driver_assistance = request.form.get('driver_assistance_checkbox')
        gps_option = request.form.get('gps_option_checkbox')
        child_seat_quantity = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '').strip()
        if not selected_reservation_id:
            flash("Please select a reservation to add requests.", "error")
            return redirect(url_for('special_requests'))
        reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
        if not reservation:
            flash("Reservation not found.", "error")
            return redirect(url_for('special_requests'))
        # Build special requests string
        requests_list = []
        if driver_assistance == 'on':
            requests_list.append("Driver assistance requested")
        if gps_option == 'on':
            requests_list.append("GPS option requested")
        try:
            qty = int(child_seat_quantity)
            if qty > 0:
                requests_list.append(f"{qty} child seat(s) requested")
        except:
            pass
        if special_notes:
            requests_list.append(f"Notes: {special_notes}")
        reservation['special_requests'] = '; '.join(requests_list) if requests_list else ''
        write_reservations(reservations)
        flash("Special requests updated.", "success")
        return redirect(url_for('special_requests'))
    # GET request: show form
    return render_template('special_requests.html',
                           reservations=reservations)
# Route: Locations page
@app.route('/locations', methods=['GET'])
def locations_page():
    locations = read_locations()
    hours_filter = request.args.get('hours_filter', '')
    search_location = request.args.get('search_location_input', '').lower()
    filtered_locations = locations
    if hours_filter:
        if hours_filter == '24/7':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'] == '24/7']
        elif hours_filter == 'Business Hours':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'] == '09:00-18:00']
        elif hours_filter == 'Weekend':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'].lower() == 'weekend']
    if search_location:
        filtered_locations = [loc for loc in filtered_locations if search_location in loc['city'].lower() or search_location in loc['address'].lower()]
    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter=hours_filter,
                           search_location=search_location)
# Route: Location detail button (view location details)
@app.route('/location/<location_id>')
def location_detail(location_id):
    locations = read_locations()
    location = next((loc for loc in locations if loc['location_id'] == location_id), None)
    if not location:
        flash("Location not found.", "error")
        return redirect(url_for('locations_page'))
    return render_template('location_detail.html', location=location)
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)