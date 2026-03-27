from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Utility functions to read and write data files

def read_vehicles():
    vehicles = []
    try:
        with open(f'{DATA_PATH}/vehicles.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
        with open(f'{DATA_PATH}/customers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    customer = {
                        'customer_id': int(parts[0]),
                        'name': parts[1],
                        'email': parts[2],
                        'phone': parts[3],
                        'driver_license': parts[4],
                        'license_expiry': parts[5],
                    }
                    customers.append(customer)
    except Exception:
        pass
    return customers

def read_locations():
    locations = []
    try:
        with open(f'{DATA_PATH}/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
        with open(f'{DATA_PATH}/rentals.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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

def read_insurance_plans():
    plans = []
    try:
        with open(f'{DATA_PATH}/insurance.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    plan = {
                        'insurance_id': int(parts[0]),
                        'plan_name': parts[1],
                        'description': parts[2],
                        'daily_cost': float(parts[3]),
                        'coverage_limit': parts[4],
                        'deductible': int(parts[5])
                    }
                    plans.append(plan)
    except Exception:
        pass
    return plans

def read_reservations():
    reservations = []
    try:
        with open(f'{DATA_PATH}/reservations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    try:
        with open(f'{DATA_PATH}/reservations.txt', 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass

def write_rentals(rentals):
    try:
        with open(f'{DATA_PATH}/rentals.txt', 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass

# Helper functions

def get_vehicle_by_id(vehicle_id):
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
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

# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    promotions = [
        {'title': 'Winter Special', 'description': 'Get 20% off on all SUVs!'},
        {'title': 'Early Bird', 'description': 'Book 30 days in advance and save 15%'}
    ]
    # Select featured vehicles as those with status Available, pick first 5
    featured_vehicles = [
        {'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']}
        for v in vehicles if v['status'] == 'Available'
    ][:5]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

# Search route
@app.route('/search')
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    # Extract filters from query params
    location_filter = request.args.get('location', '')
    vehicle_type_filter = request.args.get('vehicle_type', '')
    date_range_filter = request.args.get('date_range', '')

    filters = {
        'location': location_filter,
        'vehicle_type': vehicle_type_filter,
        'date_range': date_range_filter
    }

    # Filter vehicles by vehicle_type
    filtered_vehicles = [v for v in vehicles if (vehicle_type_filter == '' or v['vehicle_type'] == vehicle_type_filter)]

    # Filter vehicles by location - assume location filter matches any location's city
    # Since vehicles are not location-specific, this can be a no-op or only matches if location given
    # We'll let location filter not filter vehicles strictly, just pass locations and filter UI

    return render_template('search.html', vehicles=filtered_vehicles, locations=locations, vehicle_types=vehicle_types, filters=filters)

# Vehicle details route
@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    # For reviews, as no data source specified, create dummy reviews
    reviews = [
        {'reviewer': 'John Doe', 'rating': 5, 'comment': 'Great car, very clean.'},
        {'reviewer': 'Jane Smith', 'rating': 4, 'comment': 'Smooth ride and comfortable seats.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

# Booking route
@app.route('/book/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404
    locations = read_locations()
    price = None
    booking_data = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        dropoff_date = request.form.get('dropoff_date', '').strip()

        booking_data = {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }

        # Validate required fields
        err = None
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            err = 'All fields are required.'
        else:
            try:
                d1 = datetime.strptime(pickup_date, '%Y-%m-%d')
                d2 = datetime.strptime(dropoff_date, '%Y-%m-%d')
                if d2 < d1:
                    err = 'Dropoff date must be after pickup date.'
            except Exception:
                err = 'Date format must be YYYY-MM-DD.'

        if err:
            # render page with error message
            return render_template('booking.html', vehicle=vehicle, locations=locations, price=None, booking_data=booking_data, error=err)

        # Calculate price = days * daily_rate
        delta = (d2 - d1).days
        if delta <= 0:
            err = 'Rental duration must be at least one day.'
            return render_template('booking.html', vehicle=vehicle, locations=locations, price=None, booking_data=booking_data, error=err)

        price = delta * vehicle['daily_rate']

        # Show booking form with calculated price
        return render_template('booking.html', vehicle=vehicle, locations=locations, price=price, booking_data=booking_data)

    # GET method
    return render_template('booking.html', vehicle=vehicle, locations=locations)

# Insurance options route
@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance_plans()
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return "Reservation not found", 404

    selected_insurance = None

    if request.method == 'POST':
        selected_insurance_id = request.form.get('insurance_id')
        if not selected_insurance_id:
            error = 'Please select an insurance plan.'
            return render_template('insurance.html', insurance_plans=insurance_plans, reservation=reservation, selected_insurance=None, error=error)

        try:
            selected_insurance_id = int(selected_insurance_id)
        except ValueError:
            error = 'Invalid insurance selection.'
            return render_template('insurance.html', insurance_plans=insurance_plans, reservation=reservation, selected_insurance=None, error=error)

        # Find insurance plan
        plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
        if not plan:
            error = 'Selected insurance plan not found.'
            return render_template('insurance.html', insurance_plans=insurance_plans, reservation=reservation, selected_insurance=None, error=error)

        selected_insurance = plan

        # Confirm booking: update reservation with insurance and status Active
        reservations = read_reservations()
        changed = False
        for r in reservations:
            if r['reservation_id'] == reservation_id:
                r['insurance_id'] = selected_insurance_id
                r['status'] = 'Active'
                changed = True
                break
        if changed:
            write_reservations(reservations)

        return render_template('insurance.html', insurance_plans=insurance_plans, reservation=reservation, selected_insurance=selected_insurance, confirmed=True)

    # GET method
    selected_insurance = None
    if reservation['insurance_id'] != 0:
        selected_insurance = next((p for p in insurance_plans if p['insurance_id'] == reservation['insurance_id']), None)

    return render_template('insurance.html', insurance_plans=insurance_plans, reservation=reservation, selected_insurance=selected_insurance)

# Rental history route
@app.route('/history')
def rental_history():
    rentals = read_rentals()
    status_filter = request.args.get('status', '')
    if status_filter:
        rentals = [r for r in rentals if r['status'] == status_filter]
    return render_template('rental_history.html', rentals=rentals, status_filter=status_filter)

# Reservations management route
@app.route('/reservations')
def reservation_management():
    reservations = read_reservations()

    # Actions can be in query parameters
    action = request.args.get('action', '')
    reservation_id = request.args.get('reservation_id', '')

    if action and reservation_id:
        try:
            reservation_id_int = int(reservation_id)
        except ValueError:
            reservation_id_int = None

        if reservation_id_int is not None:
            # Read reservations again
            reservations = read_reservations()
            rentals = read_rentals()
            changed = False
            if action == 'cancel':
                # Cancel reservation and update rental status
                for r in reservations:
                    if r['reservation_id'] == reservation_id_int:
                        r['status'] = 'Cancelled'
                        changed = True
                        rental_id = r['rental_id']
                        # Update rental
                        for rental in rentals:
                            if rental['rental_id'] == rental_id:
                                rental['status'] = 'Cancelled'
                                break
                        break
            elif action == 'modify':
                # For this spec, no modify form provided, so just dummy placeholder or ignore
                pass

            if changed:
                write_reservations(reservations)
                write_rentals(rentals)
                # Redirect to avoid repeat action
                return redirect(url_for('reservation_management'))

    return render_template('reservations.html', reservations=reservations)

# Special requests route
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()

    if request.method == 'POST':
        selected_reservation_id = request.form.get('reservation_id', '')
        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        child_seat_quantity = request.form.get('child_seat_quantity', '0').strip()
        special_notes = request.form.get('special_notes', '').strip()

        try:
            child_seat_num = int(child_seat_quantity)
            if child_seat_num < 0:
                child_seat_num = 0
        except ValueError:
            child_seat_num = 0

        # Compose special requests string
        requests_list = []
        if driver_assistance:
            requests_list.append('Driver assistance requested')
        if gps_option:
            requests_list.append('GPS requested')
        if child_seat_num > 0:
            requests_list.append(f'Child seats: {child_seat_num}')
        if special_notes:
            requests_list.append(f'Notes: {special_notes}')

        special_requests_str = '; '.join(requests_list) if requests_list else ''

        # Update reservation special_requests
        try:
            reservation_id_int = int(selected_reservation_id)
        except ValueError:
            reservation_id_int = None

        if reservation_id_int is not None:
            changed = False
            for r in reservations:
                if r['reservation_id'] == reservation_id_int:
                    r['special_requests'] = special_requests_str
                    changed = True
                    break
            if changed:
                write_reservations(reservations)

        return redirect(url_for('special_requests'))

    return render_template('special_requests.html', reservations=reservations)

# Locations page route
@app.route('/locations')
def locations_page():
    locations = read_locations()

    hours_filter = request.args.get('hours_filter', '')
    search_query = request.args.get('search_query', '').lower()

    if hours_filter:
        locations = [loc for loc in locations if loc['hours'] == hours_filter]

    if search_query:
        locations = [loc for loc in locations if search_query in loc['city'].lower() or search_query in loc['address'].lower()]

    return render_template('locations.html', locations=locations, hours_filter=hours_filter, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
