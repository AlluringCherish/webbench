from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Utility functions to read and write PSV files

def read_psv_file(filename):
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        records = [line.split('|') for line in lines if line]
    return records


def write_psv_file(filename, records):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            f.write('|'.join(record) + '\n')


# Helper functions for each entity

def get_vehicles():
    raw = read_psv_file('vehicles.txt')
    keys = ['vehicle_id','make','model','vehicle_type','daily_rate','seats','transmission','fuel_type','status']
    vehicles = [dict(zip(keys, r)) for r in raw]
    return vehicles


def get_vehicle_by_id(vid):
    vehicles = get_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == str(vid):
            return v
    return None


def get_customers():
    raw = read_psv_file('customers.txt')
    keys = ['customer_id','name','email','phone','driver_license','license_expiry']
    customers = [dict(zip(keys, r)) for r in raw]
    return customers


def get_locations():
    raw = read_psv_file('locations.txt')
    keys = ['location_id','city','address','phone','hours','available_vehicles']
    locations = [dict(zip(keys, r)) for r in raw]
    return locations


def get_rentals():
    raw = read_psv_file('rentals.txt')
    keys = ['rental_id','vehicle_id','customer_id','pickup_date','dropoff_date','pickup_location','dropoff_location','total_price','status']
    rentals = [dict(zip(keys, r)) for r in raw]
    return rentals


def get_insurance_plans():
    raw = read_psv_file('insurance.txt')
    keys = ['insurance_id','plan_name','description','daily_cost','coverage_limit','deductible']
    plans = [dict(zip(keys, r)) for r in raw]
    return plans


def get_reservations():
    raw = read_psv_file('reservations.txt')
    keys = ['reservation_id','rental_id','vehicle_id','customer_id','status','insurance_id','special_requests']
    reservations = [dict(zip(keys, r)) for r in raw]
    return reservations


def write_reservations(reservations):
    records = []
    for r in reservations:
        rec = [r['reservation_id'], r['rental_id'], r['vehicle_id'], r['customer_id'], r['status'], r['insurance_id'], r['special_requests']]
        records.append(rec)
    write_psv_file('reservations.txt', records)


def write_rentals(rentals):
    records = []
    for r in rentals:
        rec = [r['rental_id'], r['vehicle_id'], r['customer_id'], r['pickup_date'], r['dropoff_date'], r['pickup_location'], r['dropoff_location'], r['total_price'], r['status']]
        records.append(rec)
    write_psv_file('rentals.txt', records)

# Dashboard page
@app.route('/')
def dashboard():
    vehicles = get_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:5]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles)

# Vehicle Search page
@app.route('/search')
def search_vehicles():
    location_filter = request.args.get('location_filter', '')
    vehicle_type_filter = request.args.get('vehicle_type_filter', '')
    date_range_input = request.args.get('date_range_input', '')

    vehicles = get_vehicles()
    locations = get_locations()

    # Filter by location (we assume vehicle availability linked to locations is not specified, so skip)
    # Filter by vehicle type
    if vehicle_type_filter:
        vehicles = [v for v in vehicles if v['vehicle_type'].lower() == vehicle_type_filter.lower() and v['status'] == 'Available']
    else:
        vehicles = [v for v in vehicles if v['status'] == 'Available']

    # No direct date filtering on vehicles for simplicity

    return render_template('search.html', vehicles=vehicles, locations=locations, 
                           selected_location=location_filter, selected_vehicle_type=vehicle_type_filter,
                           date_range_input=date_range_input)

# Vehicle Details page
@app.route('/vehicle/<vehicle_id>')
def vehicle_details(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404
    # No reviews data specified, pass empty list
    reviews = []
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

# Booking page
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    locations = get_locations()
    total_price = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location', '')
        dropoff_location = request.form.get('dropoff_location', '')
        pickup_date = request.form.get('pickup_date', '')
        dropoff_date = request.form.get('dropoff_date', '')

        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
            days = (dropoff_dt - pickup_dt).days
            if days <= 0:
                total_price = 'Invalid date range'
            else:
                total_price = days * float(vehicle['daily_rate'])
                total_price = f"${total_price:.2f}"
        except ValueError:
            total_price = 'Invalid date format'

        if request.form.get('calculate_price_button'):
            return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)

        if request.form.get('proceed_to_insurance_button'):
            # Save booking params in session or pass via query - simple pass via query for demo
            # We encode parameters in URL parameters
            params = f"pickup_location={pickup_location}&dropoff_location={dropoff_location}&pickup_date={pickup_date}&dropoff_date={dropoff_date}"
            return redirect(url_for('insurance_options', vehicle_id=vehicle_id) + '?' + params)

    return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)

# Insurance Options page
@app.route('/insurance/<vehicle_id>', methods=['GET', 'POST'])
def insurance_options(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return "Vehicle not found", 404

    insurance_plans = get_insurance_plans()

    pickup_location = request.args.get('pickup_location', '')
    dropoff_location = request.args.get('dropoff_location', '')
    pickup_date = request.args.get('pickup_date', '')
    dropoff_date = request.args.get('dropoff_date', '')

    daily_cost = None
    description = None

    if request.method == 'POST':
        selected_plan_id = request.form.get('insurance_plan')
        plan = next((p for p in insurance_plans if p['insurance_id'] == selected_plan_id), None)
        if not plan:
            return "Invalid insurance plan", 400

        # Calculate days
        try:
            pickup_dt = datetime.strptime(pickup_date, '%Y-%m-%d')
            dropoff_dt = datetime.strptime(dropoff_date, '%Y-%m-%d')
            days = (dropoff_dt - pickup_dt).days
            if days <= 0:
                return "Invalid date range", 400
        except ValueError:
            return "Invalid date format", 400

        # Calculate total price with insurance
        rental_price = days * float(vehicle['daily_rate'])
        insurance_price = days * float(plan['daily_cost'])
        total_price = rental_price + insurance_price

        # Create rental and reservation records
        # Generate new rental_id and reservation_id
        rentals = get_rentals()
        reservations = get_reservations()

        new_rental_id = str(int(rentals[-1]['rental_id']) + 1) if rentals else '1'
        new_reservation_id = str(int(reservations[-1]['reservation_id']) + 1) if reservations else '1'

        customer_id = '1'  # default customer for demo
        rental_record = {
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': f'{total_price:.2f}',
            'status': 'Active'
        }

        rentals.append(rental_record)
        write_rentals(rentals)

        reservation_record = {
            'reservation_id': new_reservation_id,
            'rental_id': new_rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': customer_id,
            'status': 'Confirmed',
            'insurance_id': selected_plan_id,
            'special_requests': ''
        }

        reservations.append(reservation_record)
        write_reservations(reservations)

        return redirect(url_for('reservations'))

    return render_template('insurance.html', vehicle=vehicle, insurance_plans=insurance_plans, 
                           pickup_location=pickup_location, dropoff_location=dropoff_location,
                           pickup_date=pickup_date, dropoff_date=dropoff_date)

# Rental History page
@app.route('/history')
def rental_history():
    rentals = get_rentals()
    vehicles = get_vehicles()
    vehicle_dict = {v['vehicle_id']: v for v in vehicles}

    status_filter = request.args.get('status_filter', 'All')

    if status_filter != 'All':
        filtered_rentals = [r for r in rentals if r['status'] == status_filter]
    else:
        filtered_rentals = rentals

    # Enhance rentals with vehicle info
    enhanced = []
    for r in filtered_rentals:
        v = vehicle_dict.get(r['vehicle_id'], {})
        enhanced.append({'rental': r, 'vehicle': v})

    return render_template('history.html', rentals=enhanced, status_filter=status_filter)

# Reservation Management page
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    reservations_list = get_reservations()
    vehicles = get_vehicles()
    vehicle_dict = {v['vehicle_id']: v for v in vehicles}

    sort_by_date = request.args.get('sort', '') == 'date'

    # Sorting by date (ascending by pickup_date in rentals linked)
    rentals = get_rentals()
    rental_dict = {r['rental_id']: r for r in rentals}

    merged = []
    for res in reservations_list:
        rent = rental_dict.get(res['rental_id'], {})
        vehicle = vehicle_dict.get(res['vehicle_id'], {})
        merged.append({'reservation': res, 'rental': rent, 'vehicle': vehicle})

    if sort_by_date:
        merged.sort(key=lambda x: x['rental'].get('pickup_date',''))

    if request.method == 'POST':
        # Handle cancel and modify
        action = request.form.get('action')
        reservation_id = request.form.get('reservation_id')
        if action == 'cancel' and reservation_id:
            for res in reservations_list:
                if res['reservation_id'] == reservation_id:
                    res['status'] = 'Cancelled'
                    break
            write_reservations(reservations_list)
            return redirect(url_for('reservations'))

        if action == 'modify' and reservation_id:
            # For simplicity, just redirect to booking page of the vehicle
            res = next((r for r in reservations_list if r['reservation_id'] == reservation_id), None)
            if res:
                return redirect(url_for('booking', vehicle_id=res['vehicle_id']))

    return render_template('reservations.html', reservations=merged, sort_by_date=sort_by_date)

# Special Requests page
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations_list = get_reservations()

    if request.method == 'POST':
        reservation_id = request.form.get('select_reservation')
        driver_assistance = request.form.get('driver_assistance_checkbox')
        gps_option = request.form.get('gps_option_checkbox')
        child_seat_quantity = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes')

        # Construct special requests string
        requests = []
        if driver_assistance == 'on':
            requests.append('Driver assistance requested')
        if gps_option == 'on':
            requests.append('GPS requested')
        if child_seat_quantity and child_seat_quantity.isdigit() and int(child_seat_quantity) > 0:
            requests.append(f'Child seat x{child_seat_quantity}')
        if special_notes:
            requests.append(special_notes)

        reservations_list_updated = []
        for res in reservations_list:
            if res['reservation_id'] == reservation_id:
                existing = res['special_requests']
                combined = existing
                if existing and requests:
                    combined += '; '
                combined += '; '.join(requests)
                res['special_requests'] = combined
            reservations_list_updated.append(res)

        write_reservations(reservations_list_updated)

        return redirect(url_for('special_requests'))

    return render_template('special_requests.html', reservations=reservations_list)

# Locations page
@app.route('/locations', methods=['GET','POST'])
def locations():
    locations_list = get_locations()
    hours_filter = request.args.get('hours_filter', '24/7')
    search_location = request.args.get('search_location', '')

    # Filter by hours
    if hours_filter != '24/7':
        locations_list = [loc for loc in locations_list if loc['hours'] == hours_filter]

    # Filter by search term in city or address
    if search_location:
        locations_list = [loc for loc in locations_list if search_location.lower() in loc['city'].lower() or
                          search_location.lower() in loc['address'].lower()]

    if request.method == 'POST':
        # Potentially handle add/edit location if needed, but not specified
        pass

    return render_template('locations.html', locations=locations_list, hours_filter=hours_filter, search_location=search_location)

if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
