from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions to read and write data files

def read_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r') as f:
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
        pass
    return vehicles

def read_customers():
    customers = []
    try:
        with open('data/customers.txt', 'r') as f:
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
        pass
    return customers

def read_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r') as f:
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
        pass
    return locations

def read_rentals():
    rentals = []
    try:
        with open('data/rentals.txt', 'r') as f:
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
        pass
    return rentals

def read_insurance_plans():
    plans = []
    try:
        with open('data/insurance.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
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
        with open('data/reservations.txt', 'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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

def write_vehicles(vehicles):
    try:
        with open('data/vehicles.txt', 'w') as f:
            for v in vehicles:
                line = f"{v['vehicle_id']}|{v['make']}|{v['model']}|{v['vehicle_type']}|{v['daily_rate']}|{v['seats']}|{v['transmission']}|{v['fuel_type']}|{v['status']}"
                f.write(line + '\n')
    except Exception:
        pass

def write_customers(customers):
    try:
        with open('data/customers.txt', 'w') as f:
            for c in customers:
                line = f"{c['customer_id']}|{c['name']}|{c['email']}|{c['phone']}|{c['driver_license']}|{c['license_expiry']}"
                f.write(line + '\n')
    except Exception:
        pass

def write_locations(locations):
    try:
        with open('data/locations.txt', 'w') as f:
            for l in locations:
                line = f"{l['location_id']}|{l['city']}|{l['address']}|{l['phone']}|{l['hours']}|{l['available_vehicles']}"
                f.write(line + '\n')
    except Exception:
        pass

def write_rentals(rentals):
    try:
        with open('data/rentals.txt', 'w') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}"
                f.write(line + '\n')
    except Exception:
        pass

def write_insurance_plans(plans):
    try:
        with open('data/insurance.txt', 'w') as f:
            for p in plans:
                line = f"{p['insurance_id']}|{p['plan_name']}|{p['description']}|{p['daily_cost']}|{p['coverage_limit']}|{p['deductible']}"
                f.write(line + '\n')
    except Exception:
        pass

def write_reservations(reservations):
    try:
        with open('data/reservations.txt', 'w') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}"
                f.write(line + '\n')
    except Exception:
        pass


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    vehicles = read_vehicles()
    featured_vehicles = []
    current_promotions = ["Winter Special - 20% off SUVs", "Free GPS for rentals over 3 days"]

    # Let's feature up to 3 vehicles with status Available, just pick some
    count = 0
    for v in vehicles:
        if v['status'] == 'Available':
            featured_vehicles.append({'vehicle_id': v['vehicle_id'], 'make': v['make'], 'model': v['model'], 'daily_rate': v['daily_rate']})
            count += 1
            if count >= 3:
                break

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, current_promotions=current_promotions)

@app.route('/vehicles')
def vehicle_search():
    vehicles = read_vehicles()
    locations = read_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']
    vehicles_simple = []
    for v in vehicles:
        vehicles_simple.append({
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'vehicle_type': v['vehicle_type'],
            'daily_rate': v['daily_rate']
        })
    return render_template('vehicle_search.html', vehicles=vehicles_simple, locations=locations, vehicle_types=vehicle_types)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break
    if not vehicle:
        abort(404)

    # Simulate reviews (no data file for reviews, so static example)
    reviews = [
        {'reviewer_name': 'John Doe', 'rating': 5, 'comment': 'Great car, very comfortable.'},
        {'reviewer_name': 'Jane Smith', 'rating': 4, 'comment': 'Smooth ride and fuel efficient.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    locations = read_locations()
    pickup_locations = locations
    dropoff_locations = locations
    calculated_price = None
    booking_data = {}

    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break
    if not vehicle:
        abort(404)

    if request.method == 'POST':
        booking_data = {
            'pickup_location_id': request.form.get('pickup_location_id'),
            'dropoff_location_id': request.form.get('dropoff_location_id'),
            'pickup_date': request.form.get('pickup_date'),
            'dropoff_date': request.form.get('dropoff_date')
        }
        try:
            pickup_date_obj = datetime.strptime(booking_data['pickup_date'], '%Y-%m-%d')
            dropoff_date_obj = datetime.strptime(booking_data['dropoff_date'], '%Y-%m-%d')
            if dropoff_date_obj < pickup_date_obj:
                calculated_price = None
            else:
                days = (dropoff_date_obj - pickup_date_obj).days + 1
                calculated_price = days * vehicle['daily_rate']
        except Exception:
            calculated_price = None

    return render_template('booking.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations, calculated_price=calculated_price, booking_data=booking_data)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance_plans()
    selected_insurance = None

    if request.method == 'POST':
        selected_id_str = request.form.get('selected_insurance_id')
        if selected_id_str:
            try:
                selected_id = int(selected_id_str)
                for plan in insurance_plans:
                    if plan['insurance_id'] == selected_id:
                        selected_insurance = plan
                        break
                # Update reservation with selected insurance
                reservations = read_reservations()
                updated = False
                for res in reservations:
                    if res['reservation_id'] == reservation_id:
                        if selected_insurance:
                            res['insurance_id'] = selected_insurance['insurance_id']
                        updated = True
                        break
                if updated:
                    write_reservations(reservations)
                    return redirect(url_for('rental_history'))
            except Exception:
                pass

    else:
        # On GET, find currently selected insurance for reservation
        reservations = read_reservations()
        reservation = None
        for res in reservations:
            if res['reservation_id'] == reservation_id:
                reservation = res
                break
        if reservation and reservation['insurance_id']:
            for plan in insurance_plans:
                if plan['insurance_id'] == reservation['insurance_id']:
                    selected_insurance = plan
                    break

    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance)

@app.route('/history')
def rental_history():
    rentals = read_rentals()
    status_filter_options = ['All', 'Active', 'Completed', 'Cancelled']

    status_filter = request.args.get('status_filter', 'All')
    if status_filter != 'All':
        filtered = []
        for r in rentals:
            if r['status'] == status_filter:
                filtered.append(r)
        rentals = filtered

    return render_template('rental_history.html', rentals=rentals, status_filter_options=status_filter_options)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations_management():
    reservations = read_reservations()

    if request.method == 'POST':
        action = request.form.get('action')
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str:
            return redirect(url_for('reservations_management'))
        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            return redirect(url_for('reservations_management'))

        if action == 'modify':
            # For simplification, just update status if supplied
            new_status = request.form.get('new_status')
            updated = False
            for res in reservations:
                if res['reservation_id'] == reservation_id:
                    if new_status:
                        res['status'] = new_status
                        updated = True
                        break
            if updated:
                write_reservations(reservations)
        elif action == 'cancel':
            updated = False
            for res in reservations:
                if res['reservation_id'] == reservation_id:
                    res['status'] = 'Cancelled'
                    updated = True
                    break
            if updated:
                write_reservations(reservations)

        return redirect(url_for('reservations_management'))

    return render_template('reservations_management.html', reservations=reservations)

@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    submitted_request_status = None

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str:
            submitted_request_status = 'No reservation selected.'
            return render_template('special_requests.html', reservations=reservations, submitted_request_status=submitted_request_status)
        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            submitted_request_status = 'Invalid reservation ID.'
            return render_template('special_requests.html', reservations=reservations, submitted_request_status=submitted_request_status)

        driver_assistance = request.form.get('driver_assistance')
        gps_option = request.form.get('gps_option')
        child_seat_quantity = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes')

        parts = []
        if driver_assistance == 'on':
            parts.append('Driver assistance requested')
        if gps_option == 'on':
            parts.append('GPS requested')
        if child_seat_quantity:
            try:
                qty = int(child_seat_quantity)
                if qty > 0:
                    parts.append(f'Child seat(s): {qty}')
            except Exception:
                pass
        if special_notes:
            parts.append(f'Notes: {special_notes}')

        combined_requests = '; '.join(parts) if parts else ''

        updated = False
        for res in reservations:
            if res['reservation_id'] == reservation_id:
                res['special_requests'] = combined_requests
                updated = True
                break
        if updated:
            write_reservations(reservations)
            submitted_request_status = 'Special requests updated successfully.'
        else:
            submitted_request_status = 'Reservation not found.'

    return render_template('special_requests.html', reservations=reservations, submitted_request_status=submitted_request_status)

@app.route('/locations')
def locations_page():
    locations = read_locations()
    hours_filter_options = ['All', '24/7', '09:00-18:00']
    # For simplicity no filtering implemented, just pass all
    return render_template('locations.html', locations=locations, hours_filter_options=hours_filter_options)


if __name__ == '__main__':
    app.run(debug=True)
