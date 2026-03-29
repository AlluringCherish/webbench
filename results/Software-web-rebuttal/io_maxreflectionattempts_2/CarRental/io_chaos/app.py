from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Helper functions to read/write data files

def read_vehicles():
    vehicles = []
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=9:
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
        pass
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
                if len(parts) !=6:
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
        pass
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
                if len(parts) !=6:
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
        pass
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
                if len(parts) !=9:
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
        pass
    return rentals

def write_rentals(rentals):
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w', encoding='utf-8') as f:
            for rental in rentals:
                line = '|'.join([
                    str(rental['rental_id']),
                    str(rental['vehicle_id']),
                    str(rental['customer_id']),
                    rental['pickup_date'],
                    rental['dropoff_date'],
                    rental['pickup_location'],
                    rental['dropoff_location'],
                    f"{rental['total_price']:.2f}",
                    rental['status']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_insurance():
    insurance_plans = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                coverage_limit_raw = parts[4]
                try:
                    coverage_limit = int(coverage_limit_raw)
                except ValueError:
                    coverage_limit = coverage_limit_raw

                try:
                    deductible = float(parts[5])
                except ValueError:
                    deductible = 0

                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': coverage_limit,
                    'deductible': deductible
                }
                insurance_plans.append(plan)
    except Exception:
        pass
    return insurance_plans


def read_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
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
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = '|'.join([
                    str(r['reservation_id']),
                    str(r['rental_id']),
                    str(r['vehicle_id']),
                    str(r['customer_id']),
                    r['status'],
                    str(r['insurance_id']),
                    r['special_requests']
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # featured_vehicles: example: select Available vehicles sorted by daily_rate ascending limit 5
    vehicles = [v for v in read_vehicles() if v['status'].lower() == 'available']
    featured_vehicles = sorted(vehicles, key=lambda v: v['daily_rate'])[:5]

    # promotions: dummy promotions list for demo
    promotions = [
        {'title': 'Winter Sale', 'description': 'Get 20% off on all SUV rentals!'},
        {'title': 'Free GPS Upgrade', 'description': 'Free GPS upgrade with every compact car rental.'}
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

@app.route('/search')
def vehicle_search():
    vehicles = read_vehicles()
    locations = sorted({loc['city'] for loc in read_locations()})
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    return render_template('search.html', vehicles=vehicles, locations=locations, vehicle_types=vehicle_types)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = None
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break

    vehicle_reviews = []  # As no reviews.txt specified, empty list

    return render_template('vehicle_details.html', vehicle=vehicle, vehicle_reviews=vehicle_reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    locations = sorted({loc['city'] for loc in read_locations()})
    pickup_location = ''
    dropoff_location = ''
    pickup_date = ''
    dropoff_date = ''
    total_price = 0.0

    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')
        total_price = 0.0

        # Validate dates
        try:
            pd = datetime.datetime.strptime(pickup_date, '%Y-%m-%d')
            dd = datetime.datetime.strptime(dropoff_date, '%Y-%m-%d')
            if dd < pd:
                return render_template('booking.html', locations=locations, pickup_location=pickup_location,
                                       dropoff_location=dropoff_location, pickup_date=pickup_date,
                                       dropoff_date=dropoff_date, total_price=total_price,
                                       error='Dropoff date must be after pickup date.', vehicle_id=vehicle_id)
            days = (dd - pd).days
            if days == 0:
                days = 1
            total_price = days * vehicle['daily_rate']
        except ValueError:
            return render_template('booking.html', locations=locations, pickup_location=pickup_location,
                                   dropoff_location=dropoff_location, pickup_date=pickup_date, dropoff_date=dropoff_date,
                                   total_price=total_price, error='Invalid date format.', vehicle_id=vehicle_id)

    return render_template('booking.html', locations=locations, pickup_location=pickup_location,
                           dropoff_location=dropoff_location, pickup_date=pickup_date,
                           dropoff_date=dropoff_date, total_price=total_price)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance()
    selected_insurance_id = None

    if request.method == 'POST':
        try:
            selected_insurance_id = int(request.form.get('selected_insurance_id', ''))
        except (ValueError, TypeError):
            selected_insurance_id = None

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_insurance_id=selected_insurance_id)

@app.route('/history')
def rental_history():
    rentals = read_rentals()
    filter_status = request.args.get('filter_status', 'All')

    if filter_status not in ['All', 'Active', 'Completed', 'Cancelled']:
        filter_status = 'All'

    if filter_status != 'All':
        rentals = [r for r in rentals if r['status'] == filter_status]

    return render_template('rental_history.html', rentals=rentals, filter_status=filter_status)

@app.route('/reservations')
def reservation_management():
    reservations = read_reservations()

    return render_template('reservations.html', reservations=reservations)

@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    special_requests_form_data = {}

    if request.method == 'POST':
        reservation_id_raw = request.form.get('reservation_id', '')
        driver_assistance = request.form.get('driver_assistance', '')
        gps_option = request.form.get('gps_option', '')
        child_seat_quantity = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '')

        try:
            reservation_id = int(reservation_id_raw)
        except ValueError:
            reservation_id = None

        special_requests_str_parts = []
        if driver_assistance == 'on':
            special_requests_str_parts.append('Driver assistance requested')
        if gps_option == 'on':
            special_requests_str_parts.append('GPS requested')
        try:
            csq = int(child_seat_quantity)
            if csq > 0:
                special_requests_str_parts.append(f'Child seats: {csq}')
        except ValueError:
            pass
        if special_notes.strip():
            special_requests_str_parts.append(f'Notes: {special_notes.strip()}')

        special_requests_str = '; '.join(special_requests_str_parts)

        if reservation_id is not None:
            updated = False
            for r in reservations:
                if r['reservation_id'] == reservation_id:
                    r['special_requests'] = special_requests_str
                    updated = True
                    break
            if updated:
                write_reservations(reservations)

        special_requests_form_data = {
            'reservation_id': reservation_id_raw,
            'driver_assistance': driver_assistance == 'on',
            'gps_option': gps_option == 'on',
            'child_seat_quantity': child_seat_quantity,
            'special_notes': special_notes
        }

    return render_template('special_requests.html', reservations=reservations, special_requests_form_data=special_requests_form_data)

@app.route('/locations')
def locations_page():
    locations = read_locations()

    filtered_hours = request.args.get('filtered_hours', '')
    search_query = request.args.get('search_query', '')

    if filtered_hours:
        filtered_hours_lower = filtered_hours.lower()
        def hours_filter(loc):
            return filtered_hours_lower in loc['hours'].lower()
        locations = list(filter(hours_filter, locations))

    if search_query:
        query_lower = search_query.lower()
        def search_filter(loc):
            return query_lower in loc['city'].lower() or query_lower in loc['address'].lower()
        locations = list(filter(search_filter, locations))

    return render_template('locations.html', locations=locations,
                           filtered_hours=filtered_hours, search_query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
