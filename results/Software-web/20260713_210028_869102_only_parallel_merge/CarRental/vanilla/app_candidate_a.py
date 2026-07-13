from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
data_dir = 'data'

# --- Helper functions to read and write data files ---

def read_vehicles():
    vehicles = []
    path = os.path.join(data_dir, 'vehicles.txt')
    if not os.path.exists(path):
        return vehicles
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 9:
                vehicle_id, make, model, vehicle_type, daily_rate, seats, transmission, fuel_type, status = fields
                vehicles.append({
                    'vehicle_id': int(vehicle_id),
                    'make': make,
                    'model': model,
                    'vehicle_type': vehicle_type,
                    'daily_rate': float(daily_rate),
                    'seats': seats,
                    'transmission': transmission,
                    'fuel_type': fuel_type,
                    'status': status
                })
    return vehicles

def read_customers():
    customers = []
    path = os.path.join(data_dir, 'customers.txt')
    if not os.path.exists(path):
        return customers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 6:
                customer_id, name, email, phone, driver_license, license_expiry = fields
                customers.append({
                    'customer_id': int(customer_id),
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'driver_license': driver_license,
                    'license_expiry': license_expiry
                })
    return customers

def read_locations():
    locations = []
    path = os.path.join(data_dir, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 6:
                location_id, city, address, phone, hours, available_vehicles = fields
                locations.append({
                    'location_id': int(location_id),
                    'city': city,
                    'address': address,
                    'phone': phone,
                    'hours': hours,
                    'available_vehicles': int(available_vehicles)
                })
    return locations

def read_rentals():
    rentals = []
    path = os.path.join(data_dir, 'rentals.txt')
    if not os.path.exists(path):
        return rentals
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 9:
                rental_id, vehicle_id, customer_id, pickup_date, dropoff_date, pickup_location, dropoff_location, total_price, status = fields
                rentals.append({
                    'rental_id': int(rental_id),
                    'vehicle_id': int(vehicle_id),
                    'customer_id': int(customer_id),
                    'pickup_date': pickup_date,
                    'dropoff_date': dropoff_date,
                    'pickup_location': pickup_location,
                    'dropoff_location': dropoff_location,
                    'total_price': float(total_price),
                    'status': status
                })
    return rentals

def read_insurance():
    insurance_plans = []
    path = os.path.join(data_dir, 'insurance.txt')
    if not os.path.exists(path):
        return insurance_plans
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 6:
                insurance_id, plan_name, description, daily_cost, coverage_limit, deductible = fields
                insurance_plans.append({
                    'insurance_id': int(insurance_id),
                    'plan_name': plan_name,
                    'description': description,
                    'daily_cost': float(daily_cost),
                    'coverage_limit': coverage_limit,
                    'deductible': deductible
                })
    return insurance_plans

def read_reservations():
    reservations = []
    path = os.path.join(data_dir, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 7:
                reservation_id, rental_id, vehicle_id, customer_id, status, insurance_id, special_requests = fields
                reservations.append({
                    'reservation_id': int(reservation_id),
                    'rental_id': int(rental_id),
                    'vehicle_id': int(vehicle_id),
                    'customer_id': int(customer_id),
                    'status': status,
                    'insurance_id': int(insurance_id) if insurance_id.isdigit() else None,
                    'special_requests': special_requests
                })
    return reservations

def write_rentals(rentals):
    path = os.path.join(data_dir, 'rentals.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in rentals:
            line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}\n"
            f.write(line)

def write_reservations(reservations):
    path = os.path.join(data_dir, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            insurance_id = str(r['insurance_id']) if r['insurance_id'] is not None else ''
            line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{insurance_id}|{r['special_requests']}\n"
            f.write(line)

# Utility to get next IDs
def get_next_rental_id():
    rentals = read_rentals()
    if not rentals:
        return 1
    return max(r['rental_id'] for r in rentals) + 1

def get_next_reservation_id():
    reservations = read_reservations()
    if not reservations:
        return 1
    return max(r['reservation_id'] for r in reservations) + 1

# For this app, we assume a fixed customer (for example, customer_id=1) since no auth
DEFAULT_CUSTOMER_ID = 1

# --- Flask Routes Implementation ---

@app.route('/')
@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    # Let's show first 3 vehicles as featured
    featured = vehicles[:3] if len(vehicles) >= 3 else vehicles
    promotions = [
        "Winter special: 20% off SUV rentals",
        "Book 3 days, get 1 day free",
        "Free GPS rental for weekend bookings"
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured,
                           promotions=promotions)

@app.route('/search-vehicles', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    filtered_vehicles = vehicles
    selected_location = None
    selected_type = None
    date_range = ''
    if request.method == 'POST':
        selected_location = request.form.get('location-filter')
        selected_type = request.form.get('vehicle-type-filter')
        date_range = request.form.get('date-range-input')

        # Filter vehicles by vehicle_type and availability status
        if selected_type and selected_type != 'All':
            filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == selected_type and v['status'] == 'Available']
        else:
            filtered_vehicles = [v for v in filtered_vehicles if v['status'] == 'Available']
        # Note: Location filter is not linked with vehicle availability in data, just filter by location name matches locations
        if selected_location and selected_location != 'All':
            # This filter on pickup location city name
            filtered_vehicles = filtered_vehicles  # no direct vehicle location info available, ignore practical filter

    else:
        # On GET, show available vehicles
        filtered_vehicles = [v for v in vehicles if v['status'] == 'Available']

    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    return render_template('search_vehicles.html',
                           vehicles=filtered_vehicles,
                           locations=locations,
                           vehicle_types=vehicle_types,
                           selected_location=selected_location,
                           selected_type=selected_type,
                           date_range=date_range)

@app.route('/vehicle-details/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        flash('Vehicle not found.')
        return redirect(url_for('vehicle_search'))
    # Sample placeholder reviews
    reviews = [
        {'user': 'Alice', 'comment': 'Great car, smooth ride!'},
        {'user': 'Bob', 'comment': 'Comfortable and fuel efficient.'}
    ]
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        flash('Vehicle not found.')
        return redirect(url_for('vehicle_search'))
    locations = read_locations()
    total_price = None
    days = 0
    if request.method == 'POST':
        pickup_location = request.form.get('pickup-location')
        dropoff_location = request.form.get('dropoff-location')
        pickup_date = request.form.get('pickup-date')
        dropoff_date = request.form.get('dropoff-date')
        action = request.form.get('action')

        if not (pickup_location and dropoff_location and pickup_date and dropoff_date):
            flash('Please fill in all booking details.')
            return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)

        try:
            pickup_dt = datetime.datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dropoff_dt < pickup_dt:
                flash('Dropoff date must be after pickup date.')
                return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)
            days = (dropoff_dt - pickup_dt).days + 1
        except ValueError:
            flash('Invalid date format.')
            return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)

        if action == 'calculate_price':
            total_price = days * vehicle['daily_rate']
            flash(f'Total rental price calculated: ${total_price:.2f}')
            return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price,
                                   pickup_location=pickup_location, dropoff_location=dropoff_location,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date)
        elif action == 'proceed_to_insurance':
            total_price = days * vehicle['daily_rate']
            # Create new rental and reservation entries (temporary, incomplete)
            rentals = read_rentals()
            reservations = read_reservations()
            new_rental_id = get_next_rental_id()
            new_reservation_id = get_next_reservation_id()

            # We assign default customer ID as no auth
            rental_entry = {
                'rental_id': new_rental_id,
                'vehicle_id': vehicle['vehicle_id'],
                'customer_id': DEFAULT_CUSTOMER_ID,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location,
                'total_price': total_price,
                'status': 'Pending'
            }

            rentals.append(rental_entry)
            write_rentals(rentals)

            reservation_entry = {
                'reservation_id': new_reservation_id,
                'rental_id': new_rental_id,
                'vehicle_id': vehicle['vehicle_id'],
                'customer_id': DEFAULT_CUSTOMER_ID,
                'status': 'Pending',
                'insurance_id': None,
                'special_requests': ''
            }
            reservations.append(reservation_entry)
            write_reservations(reservations)

            flash('Booking information saved. Please select insurance options.')
            return redirect(url_for('insurance_options', reservation_id=new_reservation_id))

    return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if not reservation:
        flash('Reservation not found.')
        return redirect(url_for('dashboard'))

    insurance_plans = read_insurance()
    selected_insurance_id = reservation.get('insurance_id')
    selected_plan = None
    insurance_price = 0.0
    rental = None
    rentals = read_rentals()
    rental = next((r for r in rentals if r['rental_id'] == reservation['rental_id']), None)

    days = 0
    if rental:
        try:
            pickup_dt = datetime.datetime.strptime(rental['pickup_date'], '%Y-%m-%d')
            dropoff_dt = datetime.datetime.strptime(rental['dropoff_date'], '%Y-%m-%d')
            days = (dropoff_dt - pickup_dt).days + 1
        except Exception:
            days = 0

    if request.method == 'POST':
        selected_insurance_id = request.form.get('selected-insurance')
        if selected_insurance_id and selected_insurance_id.isdigit():
            selected_insurance_id = int(selected_insurance_id)
            selected_plan = next((i for i in insurance_plans if i['insurance_id'] == selected_insurance_id), None)
            if selected_plan:
                insurance_price = selected_plan['daily_cost'] * days
                # Update reservation with insurance and confirm booking
                reservation['insurance_id'] = selected_insurance_id
                reservation['status'] = 'Confirmed'
                # Update rental status as Confirmed
                if rental:
                    rental['status'] = 'Confirmed'

                # Write updates back to files
                write_reservations(reservations)
                write_rentals(rentals)
                flash('Booking confirmed with insurance selected.')
                return redirect(url_for('reservations'))

    if selected_insurance_id:
        selected_plan = next((i for i in insurance_plans if i['insurance_id'] == selected_insurance_id), None)
        if selected_plan:
            insurance_price = selected_plan['daily_cost'] * days

    return render_template('insurance_options.html',
                           reservation=reservation,
                           insurance_plans=insurance_plans,
                           selected_plan=selected_plan,
                           insurance_price=insurance_price)

@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()
    status_filter = request.args.get('status-filter', 'All')

    # Filter rentals by status if applied
    if status_filter != 'All':
        filtered_rentals = [r for r in rentals if r['status'].lower() == status_filter.lower()]
    else:
        filtered_rentals = rentals

    # Add vehicle info to rentals
    for r in filtered_rentals:
        vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
        r['vehicle_info'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else 'Unknown'

    return render_template('rental_history.html',
                           rentals=filtered_rentals,
                           status_filter=status_filter)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    reservations = read_reservations()
    rentals = read_rentals()
    vehicles = read_vehicles()

    # Join vehicle and rental info for display
    for r in reservations:
        vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
        rental = next((rent for rent in rentals if rent['rental_id'] == r['rental_id']), None)
        r['vehicle_info'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else 'Unknown'
        r['pickup_date'] = rental['pickup_date'] if rental else ''
        r['dropoff_date'] = rental['dropoff_date'] if rental else ''

    if request.method == 'POST':
        # Handle modify or cancel actions or sorting
        action = request.form.get('action')
        reservation_id = request.form.get('reservation_id')

        if action == 'cancel' and reservation_id:
            try:
                reservation_id_int = int(reservation_id)
            except ValueError:
                flash('Invalid reservation ID for cancellation.')
                return redirect(url_for('reservations'))
            r = next((res for res in reservations if res['reservation_id'] == reservation_id_int), None)
            if r:
                r['status'] = 'Cancelled'
                # Also cancel related rental
                rel_rental = next((rent for rent in rentals if rent['rental_id'] == r['rental_id']), None)
                if rel_rental:
                    rel_rental['status'] = 'Cancelled'
                write_reservations(reservations)
                write_rentals(rentals)
                flash(f'Reservation {reservation_id} cancelled.')
            return redirect(url_for('reservations'))
        elif action == 'sort_by_date':
            reservations.sort(key=lambda x: x['pickup_date'] or '', reverse=False)
            flash('Reservations sorted by pickup date.')
            return render_template('reservations.html', reservations=reservations)

    return render_template('reservations.html', reservations=reservations)

@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    reservations_select = [(r['reservation_id'], f"Reservation {r['reservation_id']} (Status: {r['status']})") for r in reservations]
    message = ''
    if request.method == 'POST':
        selected_reservation_id = request.form.get('select-reservation')
        driver_assistance = request.form.get('driver-assistance-checkbox')
        gps_option = request.form.get('gps-option-checkbox')
        child_seats = request.form.get('child-seat-quantity')
        special_notes = request.form.get('special-notes', '').strip()

        if not selected_reservation_id:
            flash('Please select a reservation to add special requests.')
            return redirect(url_for('special_requests'))

        try:
            reservation_id_int = int(selected_reservation_id)
        except ValueError:
            flash('Invalid reservation selected.')
            return redirect(url_for('special_requests'))

        r = next((res for res in reservations if res['reservation_id'] == reservation_id_int), None)
        if not r:
            flash('Reservation not found.')
            return redirect(url_for('special_requests'))

        # Compose special requests description
        requests_list = []
        if driver_assistance:
            requests_list.append('Driver assistance requested')
        if gps_option:
            requests_list.append('GPS option selected')
        if child_seats and child_seats.isdigit() and int(child_seats) > 0:
            requests_list.append(f'Child seats needed: {child_seats}')
        if special_notes:
            requests_list.append(f'Notes: {special_notes}')

        r['special_requests'] = '; '.join(requests_list)
        write_reservations(reservations)
        flash('Special requests updated successfully.')
        return redirect(url_for('special_requests'))

    return render_template('special_requests.html', reservations=reservations_select, message=message)

@app.route('/locations')
def locations():
    locations = read_locations()
    filter_hours = request.args.get('hours-filter')
    search_input = request.args.get('search-location-input', '').strip().lower()

    filtered_locations = locations
    # Filter by hours
    if filter_hours and filter_hours != 'All':
        if filter_hours == '24/7':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'].strip() == '24/7']
        elif filter_hours == 'Business Hours':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'] != '24/7' and '09' in loc['hours']]
        elif filter_hours == 'Weekend':
            # Assuming weekend means different hours contain weekend indication - we'll do a simple check substring weekend
            filtered_locations = [loc for loc in filtered_locations if 'Weekend' in loc['hours']]

    # Search by city or name (address) substring
    if search_input:
        filtered_locations = [loc for loc in filtered_locations if 
                              search_input in loc['city'].lower() or search_input in loc['address'].lower()]

    return render_template('locations.html',
                           locations=filtered_locations,
                           filter_hours=filter_hours,
                           search_input=search_input)

if __name__ == '__main__':
    app.run(debug=True)
