from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility Functions for Reading and Writing Data Files

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
            fields = line.split('|')
            if len(fields) != 9:
                continue
            try:
                vehicle = {
                    'vehicle_id': int(fields[0]),
                    'make': fields[1],
                    'model': fields[2],
                    'vehicle_type': fields[3],
                    'daily_rate': f"{float(fields[4]):.2f}",
                    'seats': int(fields[5]),
                    'transmission': fields[6],
                    'fuel_type': fields[7],
                    'status': fields[8]
                }
                vehicles.append(vehicle)
            except ValueError:
                continue
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
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                customer = {
                    'customer_id': int(fields[0]),
                    'name': fields[1],
                    'email': fields[2],
                    'phone': fields[3],
                    'driver_license': fields[4],
                    'license_expiry': fields[5]
                }
                customers.append(customer)
            except ValueError:
                continue
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
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                location = {
                    'location_id': int(fields[0]),
                    'city': fields[1],
                    'address': fields[2],
                    'phone': fields[3],
                    'hours': fields[4],
                    'available_vehicles': int(fields[5])
                }
                locations.append(location)
            except ValueError:
                continue
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
            fields = line.split('|')
            if len(fields) != 9:
                continue
            try:
                rental = {
                    'rental_id': int(fields[0]),
                    'vehicle_id': int(fields[1]),
                    'customer_id': int(fields[2]),
                    'pickup_date': fields[3],
                    'dropoff_date': fields[4],
                    'pickup_location': fields[5],
                    'dropoff_location': fields[6],
                    'total_price': f"{float(fields[7]):.2f}",
                    'status': fields[8]
                }
                rentals.append(rental)
            except ValueError:
                continue
    return rentals


def read_insurances():
    insurances = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    if not os.path.exists(path):
        return insurances
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                insurance = {
                    'insurance_id': int(fields[0]),
                    'plan_name': fields[1],
                    'description': fields[2],
                    'daily_cost': float(fields[3]),
                    'coverage_limit': fields[4],
                    'deductible': float(fields[5])
                }
                insurances.append(insurance)
            except ValueError:
                continue
    return insurances


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
            fields = line.split('|')
            if len(fields) != 7:
                continue
            try:
                reservation = {
                    'reservation_id': int(fields[0]),
                    'rental_id': int(fields[1]),
                    'vehicle_id': int(fields[2]),
                    'customer_id': int(fields[3]),
                    'status': fields[4],
                    'insurance_id': int(fields[5]),
                    'special_requests': fields[6]
                }
                reservations.append(reservation)
            except ValueError:
                continue
    return reservations


def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for res in reservations:
                line = f"{res['reservation_id']}|{res['rental_id']}|{res['vehicle_id']}|{res['customer_id']}|{res['status']}|{res['insurance_id']}|{res['special_requests']}\n"
                f.write(line)
    except Exception:
        pass


def write_rentals(rentals):
    path = os.path.join(DATA_DIR, 'rentals.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for rent in rentals:
                line = f"{rent['rental_id']}|{rent['vehicle_id']}|{rent['customer_id']}|{rent['pickup_date']}|{rent['dropoff_date']}|{rent['pickup_location']}|{rent['dropoff_location']}|{float(rent['total_price']):.2f}|{rent['status']}\n"
                f.write(line)
    except Exception:
        pass


@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    # For featured vehicles, let's pick first 3 available vehicles sorted by vehicle_id ascending
    featured_vehicles = [
        {
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'daily_rate': v['daily_rate']
        }
        for v in sorted(vehicles, key=lambda x: x['vehicle_id']) if v['status'].lower() == 'available'][:3]

    promotions = [
        "Winter Special - 20% off on SUVs",
        "Book 3 days, get 1 day free",
        "Free GPS with Luxury car rentals"
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/search')
def vehicle_search():
    vehicles = read_vehicles()
    locations = [location['city'] for location in read_locations()]
    return render_template('search.html', vehicles=vehicles, locations=locations)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break

    # For reviews: No files specified, so empty list
    reviews = []

    if vehicle is None:
        return "Vehicle not found", 404

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break
    if vehicle is None:
        return "Vehicle not found", 404

    locations = [loc['city'] for loc in read_locations()]

    if request.method == 'GET':
        return render_template('booking.html', vehicle=vehicle, locations=locations)
    else:
        # POST: process booking data
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        # Validate inputs
        errors = []
        if not pickup_location or pickup_location not in locations:
            errors.append('Invalid pickup location')
        if not dropoff_location or dropoff_location not in locations:
            errors.append('Invalid dropoff location')
        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
        except Exception:
            errors.append('Invalid pickup date')
        try:
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
        except Exception:
            errors.append('Invalid dropoff date')

        if not errors:
            if dropoff_dt < pickup_dt:
                errors.append('Dropoff date must be after pickup date')

        if errors:
            # Return form with errors
            return render_template('booking.html', vehicle=vehicle, locations=locations, errors=errors,
                                   pickup_location=pickup_location, dropoff_location=dropoff_location,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date)

        # Calculate total price
        days = (dropoff_dt - pickup_dt).days + 1
        total_price = float(vehicle['daily_rate']) * days

        # Create a new rental and reservation with dummy customer_id = 1 (since no auth)
        rentals = read_rentals()
        new_rental_id = max([r['rental_id'] for r in rentals], default=0) + 1
        new_rental = {
            'rental_id': new_rental_id,
            'vehicle_id': vehicle['vehicle_id'],
            'customer_id': 1,  # Placeholder customer
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': total_price,
            'status': 'Active'
        }
        rentals.append(new_rental)
        write_rentals(rentals)

        # Create reservation
        reservations = read_reservations()
        new_reservation_id = max([res['reservation_id'] for res in reservations], default=0) + 1
        # Initially no insurance and blank special requests
        new_reservation = {
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': vehicle['vehicle_id'],
            'customer_id': 1,  # Placeholder
            'status': 'Confirmed',
            'insurance_id': 0,
            'special_requests': ''
        }
        reservations.append(new_reservation)
        write_reservations(reservations)

        # Redirect to insurance options page with reservation_id
        return redirect(url_for('insurance_options', reservation_id=new_reservation_id))


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurances = read_insurances()
    reservations = read_reservations()
    reservation = None

    for res in reservations:
        if res['reservation_id'] == reservation_id:
            reservation = res
            break

    if reservation is None:
        return "Reservation not found", 404

    if request.method == 'GET':
        return render_template('insurance.html', insurances=insurances, selected_insurance_id=None)
    else:
        # POST: user selected insurance plan
        try:
            selected_insurance_id = int(request.form.get('selected_insurance_id', '0'))
        except ValueError:
            selected_insurance_id = 0

        available_ids = {i['insurance_id'] for i in insurances}
        if selected_insurance_id not in available_ids:
            # Invalid insurance selection
            errors = ['Invalid insurance selection']
            return render_template('insurance.html', insurances=insurances, selected_insurance_id=None, errors=errors)

        # Update reservation insurance_id
        reservation['insurance_id'] = selected_insurance_id
        # Change reservation status from Confirmed to Active
        if reservation['status'] == 'Confirmed':
            reservation['status'] = 'Active'
        write_reservations(reservations)

        # Redirect to reservations management page
        return redirect(url_for('reservations_management'))


@app.route('/history')
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()

    # Default filter
    status_filter = request.args.get('status_filter', 'All')

    # Join vehicle info
    vehicle_dict = {v['vehicle_id']: v for v in vehicles}

    filtered_rentals = []
    for rent in rentals:
        if status_filter != 'All' and rent['status'] != status_filter:
            continue
        vehicle = vehicle_dict.get(rent['vehicle_id'])
        if not vehicle:
            continue
        rental_info = {
            'rental_id': rent['rental_id'],
            'vehicle_make': vehicle['make'],
            'vehicle_model': vehicle['model'],
            'pickup_date': rent['pickup_date'],
            'dropoff_date': rent['dropoff_date'],
            'pickup_location': rent['pickup_location'],
            'dropoff_location': rent['dropoff_location'],
            'total_price': f"{float(rent['total_price']):.2f}",
            'status': rent['status'],
        }
        filtered_rentals.append(rental_info)

    return render_template('history.html', rentals=filtered_rentals, status_filter=status_filter)


@app.route('/reservations', methods=['GET', 'POST'])
def reservations_management():
    reservations = read_reservations()
    rentals = read_rentals()
    vehicles = read_vehicles()

    if request.method == 'POST':
        # Determine if modify or cancel
        form = request.form
        res_id_str = form.get('reservation_id')
        if not res_id_str:
            return redirect(url_for('reservations_management'))
        try:
            res_id = int(res_id_str)
        except ValueError:
            return redirect(url_for('reservations_management'))

        found_res = None
        for r in reservations:
            if r['reservation_id'] == res_id:
                found_res = r
                break

        if not found_res:
            return redirect(url_for('reservations_management'))

        # Cancellation request
        if 'cancel_reservation' in form:
            found_res['status'] = 'Cancelled'

            # Update linked rental status
            for rent in rentals:
                if rent['rental_id'] == found_res['rental_id']:
                    rent['status'] = 'Cancelled'
            write_reservations(reservations)
            write_rentals(rentals)

            return redirect(url_for('reservations_management'))

        # Modification request: fields allowed to modify - special_requests only (not specified other fields to modify)
        # Since no modification fields clearly specified except special_requests in special_requests page, here we skip other modification

        # Redirect back
        return redirect(url_for('reservations_management'))

    # GET
    vehicle_dict = {v['vehicle_id']: v for v in vehicles}
    reservations_context = []
    for res in reservations:
        vehicle = vehicle_dict.get(res['vehicle_id'])
        if not vehicle:
            continue
        reservations_context.append({
            'reservation_id': res['reservation_id'],
            'rental_id': res['rental_id'],
            'vehicle_make': vehicle['make'],
            'vehicle_model': vehicle['model'],
            'customer_id': res['customer_id'],
            'status': res['status'],
            'insurance_id': res['insurance_id'],
            'special_requests': res['special_requests']
        })

    return render_template('reservations.html', reservations=reservations_context)


@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    rentals = read_rentals()
    vehicles = read_vehicles()

    if request.method == 'GET':
        vehicle_dict = {v['vehicle_id']: v for v in vehicles}
        reservations_context = []
        for res in reservations:
            vehicle = vehicle_dict.get(res['vehicle_id'])
            if not vehicle:
                continue
            reservations_context.append({
                'reservation_id': res['reservation_id'],
                'rental_id': res['rental_id'],
                'vehicle_make': vehicle['make'],
                'vehicle_model': vehicle['model'],
                'status': res['status']
            })
        return render_template('requests.html', reservations=reservations_context)
    else:
        # POST
        form = request.form
        reservation_id_str = form.get('reservation_id')
        if not reservation_id_str:
            return redirect(url_for('special_requests'))
        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            return redirect(url_for('special_requests'))

        found_res = None
        for r in reservations:
            if r['reservation_id'] == reservation_id:
                found_res = r
                break

        if not found_res:
            return redirect(url_for('special_requests'))

        # Read special request fields
        driver_assistance = form.get('driver_assistance') == 'on'
        gps_option = form.get('gps_option') == 'on'
        child_seat_quantity_str = form.get('child_seat_quantity', '0')
        special_notes = form.get('special_notes', '').strip()

        try:
            child_seat_quantity = int(child_seat_quantity_str)
            if child_seat_quantity < 0:
                child_seat_quantity = 0
        except ValueError:
            child_seat_quantity = 0

        # Build special requests string
        requests_list = []
        if driver_assistance:
            requests_list.append('Driver assistance requested')
        if gps_option:
            requests_list.append('GPS requested')
        if child_seat_quantity > 0:
            requests_list.append(f'Child seats: {child_seat_quantity}')
        if special_notes:
            requests_list.append(f'Notes: {special_notes}')

        special_requests_str = '; '.join(requests_list)

        found_res['special_requests'] = special_requests_str

        write_reservations(reservations)

        return redirect(url_for('special_requests'))


@app.route('/locations')
def locations():
    locations = read_locations()

    hours_filter = request.args.get('hours_filter', 'All')
    if hours_filter == '24/7':
        filtered = [loc for loc in locations if loc['hours'] == '24/7']
    elif hours_filter == 'Business Hours':
        filtered = [loc for loc in locations if loc['hours'] != '24/7']
    elif hours_filter == 'Weekend':
        # No explicit weekend hours given, treat as empty if no weekend info
        filtered = locations
    else:
        filtered = locations

    search_query = request.args.get('search_query', '').strip().lower()
    if search_query:
        filtered = [loc for loc in filtered if search_query in loc['city'].lower() or search_query in loc['address'].lower()]

    return render_template('locations.html', locations=filtered, hours_filter=hours_filter, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
