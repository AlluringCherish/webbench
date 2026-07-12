from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions for reading and writing pipe-delimited data files

def read_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r') as f:
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
                        'status': parts[8],
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
        with open('data/locations.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    location = {
                        'location_id': int(parts[0]),
                        'city': parts[1],
                        'address': parts[2],
                        'phone': parts[3],
                        'hours': parts[4],
                        'available_vehicles': int(parts[5]),
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
                        'status': parts[8],
                    }
                    rentals.append(rental)
    except Exception:
        pass
    return rentals

def write_rentals(rentals):
    try:
        with open('data/rentals.txt', 'w') as f:
            for rental in rentals:
                line = f"{rental['rental_id']}|{rental['vehicle_id']}|{rental['customer_id']}|{rental['pickup_date']}|{rental['dropoff_date']}|{rental['pickup_location']}|{rental['dropoff_location']}|{rental['total_price']}|{rental['status']}\n"
                f.write(line)
    except Exception:
        pass

def read_insurance():
    insurance_plans = []
    try:
        with open('data/insurance.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    plan = {
                        'insurance_id': int(parts[0]),
                        'plan_name': parts[1],
                        'description': parts[2],
                        'daily_cost': float(parts[3]),
                        'coverage_limit': parts[4],
                        'deductible': int(parts[5]),
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
                if line.strip():
                    parts = line.strip().split('|')
                    reservation = {
                        'reservation_id': int(parts[0]),
                        'rental_id': int(parts[1]),
                        'vehicle_id': int(parts[2]),
                        'customer_id': int(parts[3]),
                        'status': parts[4],
                        'insurance_id': int(parts[5]),
                        'special_requests': parts[6],
                    }
                    reservations.append(reservation)
    except Exception:
        pass
    return reservations

def write_reservations(reservations):
    try:
        with open('data/reservations.txt', 'w') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass

# -------------------- Routes --------------------

# / : redirect_to_dashboard
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))

# /dashboard : dashboard
@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    # Featured vehicles: example - vehicles with status Available, first 5
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:5]

    # Promotions - since no data source specified, hardcode example promotions
    promotions = [
        {'title': 'Winter Special', 'description': '20% off all SUVs this winter!'},
        {'title': 'Early Bird Discount', 'description': 'Book 30 days in advance and save 15%'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


# /search-vehicles : search_vehicles
@app.route('/search-vehicles', methods=['GET'])
def search_vehicles():
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
    vehicles = read_vehicles()

    # Get search filters from query params
    location_filter = request.args.get('location', '').strip()
    vehicle_type_filter = request.args.get('vehicle_type', '').strip()
    date_range = request.args.get('date_range', '').strip()  # Not used in filter logic here

    filtered_vehicles = vehicles
    if location_filter:
        # Filter vehicles that are available in location? Since location availability not in vehicle, skip filtering
        pass

    if vehicle_type_filter and vehicle_type_filter in vehicle_types:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == vehicle_type_filter]

    search_filters = {
        'location': location_filter,
        'vehicle_type': vehicle_type_filter,
        'date_range': date_range
    }

    return render_template('vehicle_search.html', locations=locations, vehicle_types=vehicle_types, filtered_vehicles=filtered_vehicles, search_filters=search_filters)


# /vehicle/<int:vehicle_id> : vehicle_details
@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)

    reviews = []  # No provided reviews data file, empty list

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


# /booking/<int:vehicle_id> : booking (GET, POST)
@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    locations = read_locations()

    calculated_price = None
    booking_form = None
    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        dropoff_date = request.form.get('dropoff_date', '').strip()
        customer_id_str = request.form.get('customer_id', '').strip()  # Not specified but needed?

        # Validate required fields
        errors = []
        if not pickup_location:
            errors.append('Pickup location is required.')
        if not dropoff_location:
            errors.append('Dropoff location is required.')
        if not pickup_date:
            errors.append('Pickup date is required.')
        if not dropoff_date:
            errors.append('Dropoff date is required.')

        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if pickup_dt > dropoff_dt:
                errors.append('Pickup date must be before dropoff date.')
        except Exception:
            errors.append('Invalid date format.')

        # If customer_id provided, parse int else set None
        try:
            customer_id = int(customer_id_str) if customer_id_str else None
        except Exception:
            customer_id = None

        if vehicle is None:
            errors.append('Invalid vehicle.')

        if errors:
            booking_form = {
                'errors': errors,
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'customer_id': customer_id_str
            }
        else:
            # Calculate price
            days = (dropoff_dt - pickup_dt).days + 1
            calculated_price = days * vehicle['daily_rate']

            booking_form = {
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'customer_id': customer_id_str
            }

    return render_template('booking.html', vehicle=vehicle, locations=locations, calculated_price=calculated_price, booking_form=booking_form)


# /insurance/<int:reservation_id> : insurance_options (GET, POST)
@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    insurance_plans = read_insurance()
    selected_insurance = None

    if reservation is None:
        return "Reservation not found", 404

    if request.method == 'POST':
        selected_id_str = request.form.get('insurance_id')
        try:
            selected_id = int(selected_id_str)
            selected_insurance = next((p for p in insurance_plans if p['insurance_id'] == selected_id), None)
            if selected_insurance:
                # Update reservation insurance_id
                reservation['insurance_id'] = selected_insurance['insurance_id']
                # Here no persistent customer or rental updates specified beyond reservation insurance
                write_reservations(reservations)
                return redirect(url_for('rental_history'))
        except Exception:
            pass

    else:
        # Get selected insurance for reservation
        selected_insurance = next((p for p in insurance_plans if p['insurance_id'] == reservation['insurance_id']), None)

    return render_template('insurance_options.html', reservation=reservation, insurance_plans=insurance_plans, selected_insurance=selected_insurance)


# /rental-history : rental_history
@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()

    filtered_status = request.args.get('status', 'All')

    if filtered_status != 'All':
        rentals = [r for r in rentals if r['status'] == filtered_status]

    return render_template('rental_history.html', rentals=rentals, filtered_status=filtered_status)


# /my-reservations : reservation_management (GET, POST)
@app.route('/my-reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    vehicles = read_vehicles()
    rentals = read_rentals()

    if request.method == 'POST':
        # Actions: modify or cancel reservation
        action = request.form.get('action', '').strip()
        reservation_id_str = request.form.get('reservation_id', '').strip()

        try:
            reservation_id = int(reservation_id_str)
        except Exception:
            reservation_id = None

        reservation = None
        if reservation_id is not None:
            reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)

        if reservation is None:
            return render_template('reservation_management.html', reservations=reservations)

        if action == 'modify':
            # Modification details could be in form but spec does not specify fields to modify - so no actual update
            # We skip modification details due to spec limit
            pass
        elif action == 'cancel':
            # Mark reservation and related rental as cancelled
            reservation['status'] = 'Cancelled'
            # Also cancel linked rental
            rental = next((rent for rent in rentals if rent['rental_id'] == reservation['rental_id']), None)
            if rental:
                rental['status'] = 'Cancelled'
                write_rentals(rentals)
            write_reservations(reservations)

    return render_template('reservation_management.html', reservations=reservations)


# /special-requests : special_requests (GET, POST)
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    submitted_request = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id', '').strip()
        driver_assistance_str = request.form.get('driver_assistance')
        gps_option_str = request.form.get('gps_option')
        child_seat_quantity_str = request.form.get('child_seat_quantity', '0').strip()
        special_notes = request.form.get('special_notes', '').strip()

        try:
            reservation_id = int(reservation_id_str)
        except Exception:
            reservation_id = None

        driver_assistance = bool(driver_assistance_str)
        gps_option = bool(gps_option_str)

        try:
            child_seat_quantity = int(child_seat_quantity_str)
            if child_seat_quantity < 0:
                child_seat_quantity = 0
        except Exception:
            child_seat_quantity = 0

        special_requests_texts = []
        if driver_assistance:
            special_requests_texts.append('Driver assistance requested')
        if gps_option:
            special_requests_texts.append('GPS option requested')
        if child_seat_quantity > 0:
            special_requests_texts.append(f'Child seats requested: {child_seat_quantity}')
        if special_notes:
            special_requests_texts.append(f'Notes: {special_notes}')

        combined_requests = '; '.join(special_requests_texts)

        # Update reservation special_requests
        reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
        if reservation:
            reservation['special_requests'] = combined_requests
            write_reservations(reservations)

        submitted_request = {
            'reservation_id': reservation_id,
            'driver_assistance': driver_assistance,
            'gps_option': gps_option,
            'child_seat_quantity': child_seat_quantity,
            'special_notes': special_notes,
        }

    return render_template('special_requests.html', reservations=reservations, submitted_request=submitted_request)


# /locations : locations_page
@app.route('/locations')
def locations_page():
    locations = read_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    # Run app
    app.run(debug=True)
