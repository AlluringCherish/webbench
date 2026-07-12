from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions for reading and writing data files

def read_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        with open('data/customers.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        with open('data/locations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        with open('data/rentals.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
        with open('data/insurance.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        with open('data/reservations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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


def write_vehicles(vehicles):
    lines = []
    for v in vehicles:
        line = f"{v['vehicle_id']}|{v['make']}|{v['model']}|{v['vehicle_type']}|{v['daily_rate']}|{v['seats']}|{v['transmission']}|{v['fuel_type']}|{v['status']}"
        lines.append(line)
    with open('data/vehicles.txt', 'w') as f:
        f.write('\n'.join(lines))


def write_customers(customers):
    lines = []
    for c in customers:
        line = f"{c['customer_id']}|{c['name']}|{c['email']}|{c['phone']}|{c['driver_license']}|{c['license_expiry']}"
        lines.append(line)
    with open('data/customers.txt', 'w') as f:
        f.write('\n'.join(lines))


def write_locations(locations):
    lines = []
    for loc in locations:
        line = f"{loc['location_id']}|{loc['city']}|{loc['address']}|{loc['phone']}|{loc['hours']}|{loc['available_vehicles']}"
        lines.append(line)
    with open('data/locations.txt', 'w') as f:
        f.write('\n'.join(lines))


def write_rentals(rentals):
    lines = []
    for r in rentals:
        line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}"
        lines.append(line)
    with open('data/rentals.txt', 'w') as f:
        f.write('\n'.join(lines))


def write_insurance(insurance_plans):
    lines = []
    for ins in insurance_plans:
        line = f"{ins['insurance_id']}|{ins['plan_name']}|{ins['description']}|{ins['daily_cost']}|{ins['coverage_limit']}|{ins['deductible']}"
        lines.append(line)
    with open('data/insurance.txt', 'w') as f:
        f.write('\n'.join(lines))


def write_reservations(reservations):
    lines = []
    for res in reservations:
        line = f"{res['reservation_id']}|{res['rental_id']}|{res['vehicle_id']}|{res['customer_id']}|{res['status']}|{res['insurance_id']}|{res['special_requests']}"
        lines.append(line)
    with open('data/reservations.txt', 'w') as f:
        f.write('\n'.join(lines))


# Helper functions

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1


def find_vehicle(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None


def find_reservation(reservation_id):
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None


def find_rental(rental_id):
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None


def find_customer(customer_id):
    customers = read_customers()
    for c in customers:
        if c['customer_id'] == customer_id:
            return c
    return None


def find_insurance(insurance_id):
    insurance_plans = read_insurance()
    for ins in insurance_plans:
        if ins['insurance_id'] == insurance_id:
            return ins
    return None


# Flask Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # For demo: featured vehicles - just first 3 available vehicles
    vehicles = read_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:3]
    # promotions - for demo, static list
    promotions = [
        {'title': 'Winter Special', 'details': '10% off all SUVs this month!'},
        {'title': 'Weekend Deal', 'details': 'Rent for 3 days, get 1 free day!'}
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/vehicles')
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    selected_location = request.args.get('location')
    selected_vehicle_type = request.args.get('vehicle_type')
    date_range_start = request.args.get('start_date')
    date_range_end = request.args.get('end_date')
    selected_date_range = None

    # Filter vehicles by selected filters
    filtered_vehicles = vehicles
    if selected_location:
        # Filter vehicles that available in that location
        # We assume all vehicles are generally available; specifics beyond current data
        pass
    if selected_vehicle_type:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == selected_vehicle_type]
    if date_range_start and date_range_end:
        selected_date_range = (date_range_start, date_range_end)

    return render_template('vehicle_search.html', vehicles=filtered_vehicles, locations=locations, vehicle_types=vehicle_types,
                           selected_location=selected_location or None,
                           selected_vehicle_type=selected_vehicle_type or None,
                           selected_date_range=selected_date_range)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if vehicle is None:
        return "Vehicle not found", 404
    # For demo, reviews empty list - no data source described
    reviews = []
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = find_vehicle(vehicle_id)
    if vehicle is None:
        return "Vehicle not found", 404

    locations = read_locations()
    form_errors = {}
    total_price = None

    if request.method == 'POST':
        pickup_location_id = request.form.get('pickup_location')
        dropoff_location_id = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        # Validate inputs
        if not pickup_location_id or not dropoff_location_id or not pickup_date or not dropoff_date:
            form_errors['missing'] = "All booking fields are required."
        else:
            try:
                pickup_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d')
                dropoff_date_obj = datetime.strptime(dropoff_date, '%Y-%m-%d')
                if dropoff_date_obj <= pickup_date_obj:
                    form_errors['date'] = "Dropoff date must be after pickup date."
            except ValueError:
                form_errors['date_format'] = "Invalid date format."

        # Validate locations
        pickup_location_obj = None
        dropoff_location_obj = None
        try:
            pickup_location_obj = next(loc for loc in locations if str(loc['location_id']) == pickup_location_id)
        except StopIteration:
            form_errors['pickup_location'] = "Invalid pickup location."
        try:
            dropoff_location_obj = next(loc for loc in locations if str(loc['location_id']) == dropoff_location_id)
        except StopIteration:
            form_errors['dropoff_location'] = "Invalid dropoff location."

        if not form_errors:
            # Calculate total price based on rental days * daily_rate
            days = (dropoff_date_obj - pickup_date_obj).days
            total_price = round(days * vehicle['daily_rate'],2)

            # Create rental and reservation on proceed to insurance? No, we create rental and reservation at confirmation in insurance?
            # Here for this route: just display total price and wait for user to confirm booking by post?
            # Per design, proceed to insurance after booking created, so create minimal reservation and rental here?
            # But booking.html only calculates price; final confirm after insurance selection

    return render_template('booking.html', vehicle=vehicle, locations=locations,
                           total_price=total_price, form_errors=form_errors or None)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance()
    reservation = find_reservation(reservation_id)
    form_errors = {}

    if reservation is None:
        return "Reservation not found", 404

    selected_insurance_id = reservation['insurance_id'] if reservation['insurance_id'] > 0 else None
    insurance_description = None
    insurance_price = None

    if request.method == 'POST':
        selected_insurance_id_str = request.form.get('insurance_id')
        try:
            selected_insurance_id = int(selected_insurance_id_str)
        except (TypeError, ValueError):
            selected_insurance_id = None
            form_errors['insurance'] = "Please select an insurance plan."

        if selected_insurance_id:
            insurance_plan = next((plan for plan in insurance_plans if plan['insurance_id'] == selected_insurance_id), None)
            if insurance_plan is None:
                form_errors['insurance'] = "Selected insurance plan is invalid."
            else:
                insurance_description = insurance_plan['description']
                insurance_price = insurance_plan['daily_cost']

        if not form_errors:
            # Update reservation insurance and confirm booking
            reservation['insurance_id'] = selected_insurance_id
            # Change reservation status to Active
            reservation['status'] = 'Active'

            # Save updated reservation
            reservations = read_reservations()
            for i, res in enumerate(reservations):
                if res['reservation_id'] == reservation_id:
                    reservations[i] = reservation
                    break
            write_reservations(reservations)

            # Redirect to reservations page
            return redirect(url_for('reservations_page'))

    else:
        if selected_insurance_id:
            insurance_plan = next((plan for plan in insurance_plans if plan['insurance_id'] == selected_insurance_id), None)
            if insurance_plan:
                insurance_description = insurance_plan['description']
                insurance_price = insurance_plan['daily_cost']

    return render_template('insurance_options.html', insurance_plans=insurance_plans,
                           selected_insurance_id=selected_insurance_id,
                           insurance_description=insurance_description,
                           insurance_price=insurance_price,
                           reservation_id=reservation_id,
                           form_errors=form_errors or None)


@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    status_filter = request.args.get('status', 'All')
    if status_filter and status_filter != 'All':
        rentals = [r for r in rentals if r['status'] == status_filter]
    return render_template('rental_history.html', rentals=rentals, status_filter=status_filter)


@app.route('/reservations')
def reservations_page():
    reservations = read_reservations()
    return render_template('reservations.html', reservations=reservations)


@app.route('/reservation/modify/<int:reservation_id>', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    # Although not detailed, we assume modification means changing special requests or status?
    # Since instructions say modify handled in reservations.html, just redirect to /reservations
    return redirect(url_for('reservations_page'))


@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    found = False
    for i, res in enumerate(reservations):
        if res['reservation_id'] == reservation_id:
            # Change status to Cancelled
            res['status'] = 'Cancelled'
            reservations[i] = res
            found = True
            break
    if found:
        write_reservations(reservations)
    return redirect(url_for('reservations_page'))


@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    form_errors = {}
    form_data = {}

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        child_seat_quantity = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes', '').strip()

        try:
            reservation_id = int(reservation_id_str)
            form_data['reservation_id'] = reservation_id
        except (TypeError, ValueError):
            form_errors['reservation_id'] = 'Invalid reservation selected.'

        form_data['driver_assistance'] = driver_assistance
        form_data['gps_option'] = gps_option

        try:
            child_seat_qty_int = int(child_seat_quantity) if child_seat_quantity else 0
            if child_seat_qty_int < 0:
                form_errors['child_seat_quantity'] = 'Child seat quantity cannot be negative.'
            form_data['child_seat_quantity'] = child_seat_qty_int
        except ValueError:
            form_errors['child_seat_quantity'] = 'Child seat quantity must be a number.'

        form_data['special_notes'] = special_notes

        if not form_errors:
            # Update special requests for the reservation
            reservations = read_reservations()
            updated = False
            for i, res in enumerate(reservations):
                if res['reservation_id'] == form_data.get('reservation_id'):
                    # Compose special requests string
                    requests_list = []
                    if driver_assistance:
                        requests_list.append('Driver assistance requested')
                    if gps_option:
                        requests_list.append('GPS requested')
                    if form_data['child_seat_quantity'] > 0:
                        requests_list.append(f"Child seats: {form_data['child_seat_quantity']}")
                    if special_notes:
                        requests_list.append(f"Notes: {special_notes}")
                    special_requests_str = '; '.join(requests_list)

                    res['special_requests'] = special_requests_str
                    reservations[i] = res
                    updated = True
                    break
            if updated:
                write_reservations(reservations)
            return redirect(url_for('special_requests'))

    return render_template('special_requests.html', reservations=reservations, form_data=form_data or None, form_errors=form_errors or None)


@app.route('/locations')
def locations_page():
    locations = read_locations()
    filtered_hours = request.args.get('hours')
    search_query = request.args.get('search')

    filtered_locations = locations

    if filtered_hours:
        if filtered_hours == '24/7':
            filtered_locations = [loc for loc in filtered_locations if loc['hours'] == '24/7']
        elif filtered_hours == 'Business Hours':
            filtered_locations = [loc for loc in filtered_locations if '09:00-18:00' in loc['hours']]
        elif filtered_hours == 'Weekend':
            # No data for weekend specifics, pass through as is
            pass

    if search_query:
        search_lower = search_query.lower()
        filtered_locations = [loc for loc in filtered_locations if search_lower in loc['city'].lower() or search_lower in loc['address'].lower()]

    return render_template('locations.html', locations=filtered_locations, filtered_hours=filtered_hours or None, search_query=search_query or None)


if __name__ == '__main__':
    app.run(debug=True)
