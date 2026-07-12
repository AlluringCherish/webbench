from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for reading and writing data files

def read_vehicles():
    vehicles = []
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        # Could log error
        vehicles = []
    return vehicles


def read_customers():
    customers = []
    try:
        with open(os.path.join(DATA_DIR, 'customers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        customers = []
    return customers


def read_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        locations = []
    return locations


def read_rentals():
    rentals = []
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
        rentals = []
    return rentals


def write_rentals(rentals):
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}" + '\n'
                f.write(line)
        return True
    except Exception:
        return False


def read_insurance():
    insurance = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                # coverage_limit can be int or str 'Unlimited'
                try:
                    coverage_limit = int(parts[4])
                except ValueError:
                    coverage_limit = parts[4]
                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': coverage_limit,
                    'deductible': int(parts[5])
                }
                insurance.append(plan)
    except Exception:
        insurance = []
    return insurance


def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                res = {
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                }
                reservations.append(res)
    except Exception:
        reservations = []
    return reservations


def write_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}" + '\n'
                f.write(line)
        return True
    except Exception:
        return False


# Section 1 Routes Implementation

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # featured_vehicles: some available vehicles (take first 5 available vehicles)
    vehicles = read_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:5]

    # promotions can be a static list for now, example dicts
    promotions = [
        {'title': 'Winter Special', 'details': 'Get 20% off SUVs this winter!'},
        {'title': 'Weekend Discount', 'details': '15% off on bookings over 3 days'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/search-vehicles', methods=['GET'])
def search_vehicles():
    locations = read_locations()
    vehicles = read_vehicles()
    vehicle_types = sorted(list(set(v['vehicle_type'] for v in vehicles)))

    # Get filters from query string
    pickup_location = request.args.get('location', '')
    vehicle_type = request.args.get('vehicle_type', '')
    date_range = request.args.get('date_range', '')  # Not used to filter because no availability info per date given

    # Filter vehicles by location (simulate by status "Available") and type
    # But we don't have vehicle location on vehicle - can't filter by location realistically.
    filtered_vehicles = vehicles

    if vehicle_type:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'] == vehicle_type and v['status'] == 'Available']
    else:
        filtered_vehicles = [v for v in filtered_vehicles if v['status'] == 'Available']

    search_filters = {
        'location': pickup_location,
        'vehicle_type': vehicle_type,
        'date_range': date_range
    }

    return render_template('vehicle_search.html', locations=locations, vehicle_types=vehicle_types, filtered_vehicles=filtered_vehicles, search_filters=search_filters)


@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        abort(404)

    # reviews - not defined in data spec, so return empty
    reviews = []

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        abort(404)

    locations = read_locations()

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '').strip()
        dropoff_location = request.form.get('dropoff_location', '').strip()
        pickup_date = request.form.get('pickup_date', '').strip()
        dropoff_date = request.form.get('dropoff_date', '').strip()

        # Validate required fields
        errors = []
        if not pickup_location:
            errors.append('Pickup location is required.')
        if not dropoff_location:
            errors.append('Dropoff location is required.')
        # Validate dates format and logical sequence
        try:
            pd_obj = datetime.strptime(pickup_date, '%Y-%m-%d')
            dd_obj = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if pd_obj > dd_obj:
                errors.append('Pickup date must be before or equal to dropoff date.')
        except ValueError:
            errors.append('Invalid date format. Use YYYY-MM-DD.')

        if errors:
            # Show with errors but do not calculate price
            return render_template('booking.html', vehicle=vehicle, locations=locations,
                                   pickup_location=pickup_location, dropoff_location=dropoff_location,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, errors=errors)

        # Calculate total price
        days = (dd_obj - pd_obj).days + 1  # inclusive of pickup day
        total_price = round(vehicle['daily_rate'] * days, 2)

        # Save the data in session or pass to insurance options
        # Here we simulate creation of rental and reservation (no customer info: default customer_id=1)

        # Create new rental
        rentals = read_rentals()
        new_rental_id = max([r['rental_id'] for r in rentals], default=0) + 1

        # We fix customer_id to 1 since no login/auth specified
        new_rental = {
            'rental_id': new_rental_id,
            'vehicle_id': vehicle['vehicle_id'],
            'customer_id': 1,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': total_price,
            'status': 'Active'
        }

        rentals.append(new_rental)
        if not write_rentals(rentals):
            errors.append('Failed to save rental data.')
            return render_template('booking.html', vehicle=vehicle, locations=locations,
                                   pickup_location=pickup_location, dropoff_location=dropoff_location,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, errors=errors)

        # Create reservation with status 'Confirmed' and insurance_id 0
default insurance to 0 means no insurance selected yet
        reservations = read_reservations()
        new_reservation_id = max([r['reservation_id'] for r in reservations], default=0) + 1
        new_reservation = {
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': vehicle['vehicle_id'],
            'customer_id': 1,
            'status': 'Confirmed',
            'insurance_id': 0,
            'special_requests': ''
        }

        reservations.append(new_reservation)
        if not write_reservations(reservations):
            errors.append('Failed to save reservation data.')
            # Rollback rental
            rentals = [r for r in rentals if r['rental_id'] != new_rental_id]
            write_rentals(rentals)
            return render_template('booking.html', vehicle=vehicle, locations=locations,
                                   pickup_location=pickup_location, dropoff_location=dropoff_location,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, errors=errors)

        # Redirect to insurance options with new reservation_id
        return redirect(url_for('insurance_options', reservation_id=new_reservation_id))

    # GET
    return render_template('booking.html', vehicle=vehicle, locations=read_locations(),
                           pickup_location='', dropoff_location='', pickup_date='', dropoff_date='', total_price=None)


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance()
    reservations = read_reservations()

    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    selected_plan = None

    if request.method == 'POST':
        selected_plan_id_str = request.form.get('insurance_id')
        errors = []
        if not selected_plan_id_str or not selected_plan_id_str.isdigit():
            errors.append('Please select an insurance plan.')
        else:
            selected_plan_id = int(selected_plan_id_str)
            selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_plan_id), None)
            if selected_plan is None:
                errors.append('Selected insurance plan not found.')

        if errors:
            return render_template('insurance_options.html', insurance_plans=insurance_plans,
                                   selected_plan=selected_plan, reservation_id=reservation_id, errors=errors)

        # Update reservation insurance
        reservation['insurance_id'] = selected_plan['insurance_id']

        # Add insurance daily cost to total price of the rental
        rentals = read_rentals()
        rental = next((r for r in rentals if r['rental_id'] == reservation['rental_id']), None)
        if rental is None:
            errors.append('Associated rental not found.')
            return render_template('insurance_options.html', insurance_plans=insurance_plans,
                                   selected_plan=selected_plan, reservation_id=reservation_id, errors=errors)

        # Calculate rental days
        try:
            pd_obj = datetime.strptime(rental['pickup_date'], '%Y-%m-%d')
            dd_obj = datetime.strptime(rental['dropoff_date'], '%Y-%m-%d')
            days = (dd_obj - pd_obj).days + 1
        except Exception:
            days = 1

        rental['total_price'] = round(rental['total_price'] + selected_plan['daily_cost'] * days, 2)

        # Write updated rentals
        if not write_rentals(rentals):
            errors.append('Failed to update rental with insurance cost.')
            return render_template('insurance_options.html', insurance_plans=insurance_plans,
                                   selected_plan=selected_plan, reservation_id=reservation_id, errors=errors)

        # Write updated reservations
        if not write_reservations(reservations):
            errors.append('Failed to update reservation insurance info.')
            return render_template('insurance_options.html', insurance_plans=insurance_plans,
                                   selected_plan=selected_plan, reservation_id=reservation_id, errors=errors)

        # Update reservation status to Active
        reservation['status'] = 'Active'

        write_reservations(reservations)

        # Redirect to my reservations page
        return redirect(url_for('my_reservations'))

    # GET
    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_plan=None, reservation_id=reservation_id)


@app.route('/rental-history', methods=['GET'])
def rental_history():
    rentals = read_rentals()
    status_filter = request.args.get('status_filter', '')
    if status_filter:
        filtered = [r for r in rentals if r['status'].lower() == status_filter.lower()]
    else:
        filtered = rentals
    return render_template('rental_history.html', rentals=filtered, status_filter=status_filter)


@app.route('/my-reservations', methods=['GET'])
def my_reservations():
    reservations = read_reservations()
    return render_template('reservations.html', reservations=reservations)


@app.route('/modify-reservation/<int:reservation_id>', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    action_result = None

    if request.method == 'POST':
        # Possible modifications: update status or special_requests
        status = request.form.get('status')
        special_requests = request.form.get('special_requests')
        if status:
            reservation['status'] = status
        if special_requests is not None:
            reservation['special_requests'] = special_requests

        if write_reservations(reservations):
            action_result = 'Reservation updated successfully.'
        else:
            action_result = 'Failed to update reservation.'

    return render_template('modify_reservation.html', reservation=reservation, action_result=action_result)


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation is None:
        abort(404)

    # Update reservation status to Cancelled
    reservation['status'] = 'Cancelled'
    write_reservations(reservations)

    return redirect(url_for('my_reservations'))


@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    submitted_request_result = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance')
        gps_option = request.form.get('gps_option')
        child_seat_quantity_str = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes', '')

        errors = []
        if not reservation_id_str or not reservation_id_str.isdigit():
            errors.append('Please select a reservation.')
        else:
            reservation_id = int(reservation_id_str)
            reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
            if reservation is None:
                errors.append('Reservation not found.')

        try:
            child_seat_quantity = int(child_seat_quantity_str) if child_seat_quantity_str else 0
            if child_seat_quantity < 0:
                errors.append('Child seat quantity cannot be negative.')
        except Exception:
            errors.append('Invalid child seat quantity.')

        if errors:
            submitted_request_result = ' '.join(errors)
            return render_template('special_requests.html', reservations=reservations, submitted_request_result=submitted_request_result)

        # Construct special_requests string
        requests_list = []
        if driver_assistance == 'on':
            requests_list.append('Driver assistance requested')
        if gps_option == 'on':
            requests_list.append('GPS requested')
        if child_seat_quantity > 0:
            requests_list.append(f'Child seats: {child_seat_quantity}')
        if special_notes.strip():
            requests_list.append(special_notes.strip())

        special_requests_str = '; '.join(requests_list)

        # Update the reservation special_requests
        if reservation:
            reservation['special_requests'] = special_requests_str
            if write_reservations(reservations):
                submitted_request_result = 'Special requests updated successfully.'
            else:
                submitted_request_result = 'Failed to update special requests.'

    return render_template('special_requests.html', reservations=reservations, submitted_request_result=submitted_request_result)


@app.route('/locations', methods=['GET'])
def locations():
    locations_list = read_locations()
    hours_filter = request.args.get('hours', '')
    search_location_input = request.args.get('search', '').strip().lower()

    # Filter by hours
    if hours_filter:
        locations_list = [loc for loc in locations_list if loc['hours'] == hours_filter]

    # Filter by search input matching city or address
    if search_location_input:
        locations_list = [loc for loc in locations_list if search_location_input in loc['city'].lower() or search_location_input in loc['address'].lower()]

    filters = {
        'hours': hours_filter,
        'search': search_location_input
    }

    return render_template('locations.html', locations_list=locations_list, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
