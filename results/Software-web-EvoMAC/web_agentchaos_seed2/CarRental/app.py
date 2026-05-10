'''
Main backend application for CarRental web application.
Handles routing, business logic, and data file operations.
No authentication; all features directly accessible.
Starts at Dashboard page at route '/'.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'car_rental_secret_key'  # Needed for flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing data files
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
# Helper to get next ID for rentals, reservations
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
# Helper to parse date string to datetime.date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None
# Helper to format date to string
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')
# Helper to calculate days between two dates inclusive
def rental_days(pickup_date_str, dropoff_date_str):
    pickup = parse_date(pickup_date_str)
    dropoff = parse_date(dropoff_date_str)
    if pickup and dropoff and dropoff >= pickup:
        return (dropoff - pickup).days + 1
    return 0
# Helper to find vehicle by id
def find_vehicle(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None
# Helper to find insurance plan by id
def find_insurance(insurance_id):
    plans = read_insurance()
    for p in plans:
        if p['insurance_id'] == insurance_id:
            return p
    return None
# Helper to find reservation by id
def find_reservation(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None
# Helper to find rental by id
def find_rental(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None
# Helper to find location by id
def find_location(location_id):
    locations = read_locations()
    for l in locations:
        if l['location_id'] == location_id:
            return l
    return None
# Helper to get all unique pickup locations from rentals and locations
def get_all_pickup_locations():
    locations = read_locations()
    return [loc['city'] for loc in locations]
# Helper to get all vehicle types
def get_all_vehicle_types():
    # From requirements: Economy, Compact, Sedan, SUV, Luxury
    return ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
# Helper to check vehicle availability for given date range and location
def is_vehicle_available(vehicle_id, pickup_date_str, dropoff_date_str, pickup_location):
    rentals = read_rentals()
    pickup_date = parse_date(pickup_date_str)
    dropoff_date = parse_date(dropoff_date_str)
    if not pickup_date or not dropoff_date or dropoff_date < pickup_date:
        return False
    for rental in rentals:
        if rental['vehicle_id'] == vehicle_id and rental['status'] in ['Active', 'Confirmed', 'Pending']:
            # Check date overlap
            existing_pickup = parse_date(rental['pickup_date'])
            existing_dropoff = parse_date(rental['dropoff_date'])
            if existing_pickup is None or existing_dropoff is None:
                continue
            # Overlap if not (new dropoff < existing pickup or new pickup > existing dropoff)
            if not (dropoff_date < existing_pickup or pickup_date > existing_dropoff):
                # Also check pickup location matches rental pickup location
                if rental['pickup_location'] == pickup_location:
                    return False
    return True
# ROUTES
@app.route('/')
def dashboard():
    vehicles = read_vehicles()
    # Featured vehicles: pick first 3 available vehicles as example
    featured = [v for v in vehicles if v['status'] == 'Available'][:3]
    # Promotions: static example promotions
    promotions = [
        "10% off for rentals over 7 days!",
        "Free GPS on all SUV rentals this month!",
        "Weekend special: Rent 2 days, get 1 day free!"
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured,
                           promotions=promotions)
@app.route('/vehicle_search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = get_all_pickup_locations()
    vehicle_types = get_all_vehicle_types()
    # Filters from query parameters or form
    selected_location = request.args.get('location_filter', '')
    selected_type = request.args.get('vehicle_type_filter', '')
    date_range = request.args.get('date_range_input', '')  # Expected format: "YYYY-MM-DD to YYYY-MM-DD"
    filtered_vehicles = [v for v in vehicles if v['status'] == 'Available']
    # Filter by location: we interpret location filter as pickup location availability
    if selected_location:
        # We filter vehicles that are available at that location by checking rentals and locations
        # Since vehicles.txt does not have location info, we assume all vehicles are available at all locations
        # But we can filter by availability in rentals for that location and date range
        # For simplicity, we just keep all vehicles (no location restriction)
        pass
    # Filter by vehicle type
    if selected_type and selected_type in vehicle_types:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == selected_type]
    # Filter by date range availability
    if date_range:
        # Parse date range: expected "YYYY-MM-DD to YYYY-MM-DD"
        parts = date_range.split('to')
        if len(parts) == 2:
            pickup_date = parts[0].strip()
            dropoff_date = parts[1].strip()
            available_vehicles = []
            for v in filtered_vehicles:
                if is_vehicle_available(v['vehicle_id'], pickup_date, dropoff_date, selected_location):
                    available_vehicles.append(v)
            filtered_vehicles = available_vehicles
    return render_template('vehicle_search.html',
                           vehicles=filtered_vehicles,
                           location_filter=selected_location,
                           vehicle_type_filter=selected_type,
                           date_range_input=date_range,
                           locations=locations,
                           vehicle_types=vehicle_types)
@app.route('/vehicle_details/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    # For simplicity, no real reviews data, show empty or static reviews
    reviews = [
        {"author": "John Doe", "comment": "Great car, very comfortable."},
        {"author": "Jane Smith", "comment": "Smooth ride and fuel efficient."}
    ]
    return render_template('vehicle_details.html',
                           vehicle=vehicle,
                           vehicle_reviews=reviews)
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if not vehicle:
        flash("Vehicle not found.", "error")
        return redirect(url_for('vehicle_search'))
    locations = read_locations()
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')
        # Validate inputs
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            flash("All booking fields are required.", "error")
            return redirect(request.url)
        # Check date validity
        pd = parse_date(pickup_date)
        dd = parse_date(dropoff_date)
        if not pd or not dd or dd < pd:
            flash("Invalid pickup or dropoff dates.", "error")
            return redirect(request.url)
        # Check vehicle availability
        if not is_vehicle_available(vehicle_id, pickup_date, dropoff_date, pickup_location):
            flash("Vehicle is not available for the selected dates and location.", "error")
            return redirect(request.url)
        # Calculate total price
        days = rental_days(pickup_date, dropoff_date)
        total_price = days * vehicle['daily_rate']
        # Store booking info temporarily in session or pass via query string to insurance page
        # Since no authentication, we simulate a customer_id = 1 (default)
        customer_id = '1'
        # Create rental record with status 'Pending' (will be confirmed after insurance)
        rentals = read_rentals()
        new_rental_id = get_next_id(rentals, 'rental_id')
        new_rental = {
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': total_price,
            'status': 'Pending'
        }
        rentals.append(new_rental)
        write_rentals(rentals)
        # Redirect to insurance selection with rental_id
        return redirect(url_for('insurance', rental_id=new_rental_id))
    # GET request
    return render_template('booking.html',
                           vehicle=vehicle,
                           locations=locations)
@app.route('/insurance/<rental_id>', methods=['GET', 'POST'])
def insurance(rental_id):
    rental = find_rental(rental_id)
    if not rental:
        flash("Rental not found.", "error")
        return redirect(url_for('dashboard'))
    insurance_plans = read_insurance()
    if request.method == 'POST':
        selected_insurance_id = request.form.get('insurance_option')
        if not selected_insurance_id:
            flash("Please select an insurance plan.", "error")
            return redirect(request.url)
        plan = find_insurance(selected_insurance_id)
        if not plan:
            flash("Selected insurance plan not found.", "error")
            return redirect(request.url)
        # Update rental total price by adding insurance cost * rental days
        days = rental_days(rental['pickup_date'], rental['dropoff_date'])
        insurance_cost = plan['daily_cost'] * days
        rental['total_price'] += insurance_cost
        # Update rental status to Confirmed
        rental['status'] = 'Confirmed'
        # Save updated rental
        rentals = read_rentals()
        for i, r in enumerate(rentals):
            if r['rental_id'] == rental_id:
                rentals[i] = rental
                break
        write_rentals(rentals)
        # Create reservation record
        reservations = read_reservations()
        new_reservation_id = get_next_id(reservations, 'reservation_id')
        new_reservation = {
            'reservation_id': new_reservation_id,
            'rental_id': rental_id,
            'vehicle_id': rental['vehicle_id'],
            'customer_id': rental['customer_id'],
            'status': 'Confirmed',
            'insurance_id': selected_insurance_id,
            'special_requests': ''
        }
        reservations.append(new_reservation)
        write_reservations(reservations)
        flash("Booking confirmed! Thank you for your reservation.", "success")
        return redirect(url_for('reservations'))
    # GET request
    return render_template('insurance.html',
                           rental=rental,
                           insurance_plans=insurance_plans)
@app.route('/rental_history')
def rental_history():
    rentals = read_rentals()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    status_filter = request.args.get('status_filter', 'All')
    filtered_rentals = rentals
    if status_filter != 'All':
        filtered_rentals = [r for r in rentals if r['status'] == status_filter]
    # Enrich rentals with vehicle info
    for r in filtered_rentals:
        r['vehicle'] = vehicles.get(r['vehicle_id'], None)
    return render_template('rental_history.html',
                           rentals=filtered_rentals,
                           status_filter=status_filter)
@app.route('/rental_history/<rental_id>')
def rental_details(rental_id):
    rental = find_rental(rental_id)
    if not rental:
        flash("Rental not found.", "error")
        return redirect(url_for('rental_history'))
    vehicle = find_vehicle(rental['vehicle_id'])
    insurance = None
    reservations = read_reservations()
    reservation = None
    for res in reservations:
        if res['rental_id'] == rental_id:
            reservation = res
            insurance = find_insurance(res['insurance_id'])
            break
    return render_template('vehicle_details.html',
                           vehicle=vehicle,
                           rental=rental,
                           insurance=insurance,
                           reservation=reservation,
                           vehicle_reviews=[])
@app.route('/reservations')
def reservations():
    reservations = read_reservations()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    # Enrich reservations with vehicle info
    for r in reservations:
        r['vehicle'] = vehicles.get(r['vehicle_id'], None)
    return render_template('reservations.html',
                           reservations=reservations)
@app.route('/reservations/modify/<reservation_id>', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    reservation = find_reservation(reservation_id)
    if not reservation:
        flash("Reservation not found.", "error")
        return redirect(url_for('reservations'))
    rental = find_rental(reservation['rental_id'])
    vehicle = find_vehicle(reservation['vehicle_id'])
    locations = read_locations()
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            flash("All fields are required.", "error")
            return redirect(request.url)
        pd = parse_date(pickup_date)
        dd = parse_date(dropoff_date)
        if not pd or not dd or dd < pd:
            flash("Invalid dates.", "error")
            return redirect(request.url)
        # Check availability excluding current rental
        rentals = read_rentals()
        for r in rentals:
            if r['vehicle_id'] == vehicle['vehicle_id'] and r['rental_id'] != rental['rental_id'] and r['status'] in ['Active', 'Confirmed', 'Pending']:
                existing_pickup = parse_date(r['pickup_date'])
                existing_dropoff = parse_date(r['dropoff_date'])
                if existing_pickup is None or existing_dropoff is None:
                    continue
                if not (dd < existing_pickup or pd > existing_dropoff):
                    flash("Vehicle not available for the selected dates.", "error")
                    return redirect(request.url)
        # Update rental info
        rental['pickup_location'] = pickup_location
        rental['dropoff_location'] = dropoff_location
        rental['pickup_date'] = pickup_date
        rental['dropoff_date'] = dropoff_date
        # Recalculate total price (without insurance cost)
        days = rental_days(pickup_date, dropoff_date)
        daily_rate = vehicle['daily_rate']
        base_price = days * daily_rate
        # Add insurance cost if any
        insurance = find_insurance(reservation['insurance_id'])
        insurance_cost = 0
        if insurance:
            insurance_cost = insurance['daily_cost'] * days
        rental['total_price'] = base_price + insurance_cost
        # Save rental
        for i, r in enumerate(rentals):
            if r['rental_id'] == rental['rental_id']:
                rentals[i] = rental
                break
        write_rentals(rentals)
        flash("Reservation modified successfully.", "success")
        return redirect(url_for('reservations'))
    # GET request: show form with current rental info
    return render_template('booking.html',
                           vehicle=vehicle,
                           locations=locations,
                           rental=rental,
                           modify=True)
@app.route('/reservations/cancel/<reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    rentals = read_rentals()
    found = False
    for i, r in enumerate(reservations):
        if r['reservation_id'] == reservation_id:
            reservations[i]['status'] = 'Cancelled'
            # Also update rental status
            rental_id = r['rental_id']
            for j, rent in enumerate(rentals):
                if rent['rental_id'] == rental_id:
                    rentals[j]['status'] = 'Cancelled'
                    break
            found = True
            break
    if found:
        write_reservations(reservations)
        write_rentals(rentals)
        flash("Reservation cancelled.", "success")
    else:
        flash("Reservation not found.", "error")
    return redirect(url_for('reservations'))
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
            flash("Please select a reservation.", "error")
            return redirect(request.url)
        # Find reservation
        reservation = None
        for r in reservations:
            if r['reservation_id'] == selected_reservation_id:
                reservation = r
                break
        if not reservation:
            flash("Reservation not found.", "error")
            return redirect(request.url)
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
        special_requests_str = '; '.join(requests_list) if requests_list else ''
        # Update reservation special_requests
        for i, r in enumerate(reservations):
            if r['reservation_id'] == selected_reservation_id:
                reservations[i]['special_requests'] = special_requests_str
                break
        write_reservations(reservations)
        flash("Special requests submitted.", "success")
        return redirect(url_for('reservations'))
    # GET request
    # Enrich reservations with vehicle info for dropdown display
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    enriched_reservations = []
    for r in reservations:
        v = vehicles.get(r['vehicle_id'])
        display_name = f"Reservation {r['reservation_id']} - {v['make']} {v['model']}" if v else f"Reservation {r['reservation_id']}"
        enriched_reservations.append({'reservation_id': r['reservation_id'], 'display_name': display_name})
    return render_template('special_requests.html',
                           reservations=enriched_reservations)
@app.route('/locations', methods=['GET'])
def locations():
    locations = read_locations()
    hours_filter = request.args.get('hours_filter', '')
    search_input = request.args.get('search_location_input', '').strip().lower()
    filtered_locations = locations
    # Filter by hours
    if hours_filter:
        if hours_filter == '24/7':
            filtered_locations = [l for l in filtered_locations if l['hours'] == '24/7']
        elif hours_filter == 'Business Hours':
            filtered_locations = [l for l in filtered_locations if l['hours'] == '09:00-18:00']
        elif hours_filter == 'Weekend':
            filtered_locations = [l for l in filtered_locations if l['hours'].lower().find('weekend') != -1]
    # Filter by search input (city or name)
    if search_input:
        filtered_locations = [l for l in filtered_locations if search_input in l['city'].lower() or search_input in l['address'].lower()]
    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter=hours_filter,
                           search_location_input=search_input)
@app.route('/locations/<location_id>')
def location_details(location_id):
    location = find_location(location_id)
    if not location:
        flash("Location not found.", "error")
        return redirect(url_for('locations'))
    return render_template('locations.html',
                           locations=[location],
                           single_location=True)
if __name__ == '__main__':
    app.run(port=5000, debug=True)