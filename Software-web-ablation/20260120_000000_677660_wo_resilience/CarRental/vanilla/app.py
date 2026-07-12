from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to read and write pipe-delimited data files

def read_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
        # If error reading file, return empty list
        pass
    return vehicles


def read_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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


def read_insurance():
    insurance_plans = []
    try:
        with open('data/insurance.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                plan = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': parts[5]
                }
                insurance_plans.append(plan)
    except Exception:
        pass
    return insurance_plans


def read_rentals():
    rentals = []
    try:
        with open('data/rentals.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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


def read_reservations():
    reservations = []
    try:
        with open('data/reservations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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


def write_reservations(reservations):
    try:
        with open('data/reservations.txt', 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass


def write_special_requests_to_reservations(reservations):
    # We can call write_reservations(reservations) as it includes special_requests
    write_reservations(reservations)


# ROUTES

@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_vehicles: List of dicts: vehicle_id (int as str), make, model, daily_rate (str)
    vehicles = read_vehicles()
    featured_vehicles = []
    try:
        # Select first 5 available vehicles as featured for example
        count = 0
        for v in vehicles:
            if v['status'].lower() == 'available':
                featured_vehicles.append({
                    'vehicle_id': str(v['vehicle_id']),
                    'make': v['make'],
                    'model': v['model'],
                    'daily_rate': f"{v['daily_rate']:.2f}"
                })
                count += 1
                if count >= 5:
                    break
    except Exception:
        featured_vehicles = []

    # promotions: list of promotional strings - no data source defined, use sample
    promotions = [
        "Winter Sale: 20% off on all SUVs",
        "Free GPS with every luxury car rental",
        "Weekend special: Rent 3 days, pay for 2"
    ]

    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/search')
def search_vehicles():
    vehicles = read_vehicles()
    locations = list({loc['city'] for loc in read_locations()})
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    # Filters from query parameters
    selected_location = request.args.get('location')
    selected_type = request.args.get('type')

    filtered_vehicles = []
    for v in vehicles:
        if v['status'].lower() != 'available':
            continue
        if selected_location:
            # We don't have direct vehicle-location link, so assume all vehicles available everywhere
            pass
        if selected_type and selected_type != '' and v['vehicle_type'] != selected_type:
            continue
        filtered_vehicles.append({
            'vehicle_id': str(v['vehicle_id']),
            'make': v['make'],
            'model': v['model'],
            'daily_rate': f"{v['daily_rate']:.2f}"
        })

    return render_template('vehicle_search.html', locations=sorted(locations), vehicle_types=vehicle_types, vehicles=filtered_vehicles)


@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id: int):
    vehicles = read_vehicles()
    vehicle = None
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            vehicle = v
            break

    if not vehicle:
        return "Vehicle not found", 404

    # Convert seats (int) to str as per context variable spec
    vehicle_context = {
        'make': vehicle['make'],
        'model': vehicle['model'],
        'vehicle_type': vehicle['vehicle_type'],
        'daily_rate': f"{vehicle['daily_rate']:.2f}",
        'seats': vehicle['seats'],
        'transmission': vehicle['transmission'],
        'fuel_type': vehicle['fuel_type'],
        'status': vehicle['status']
    }

    # Reviews not specified in data files, no source - provide empty list
    reviews = []

    return render_template('vehicle_details.html', vehicle=vehicle_context, reviews=reviews)


@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    locations = list({loc['city'] for loc in read_locations()})
    if request.method == 'POST':
        # Receive booking POST data
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')

        booking_data = {
            'pickup_location': pickup_location or '',
            'dropoff_location': dropoff_location or '',
            'pickup_date': pickup_date or '',
            'dropoff_date': dropoff_date or ''
        }

        # Normally booking would create rental/reservation and redirect to insurance
        # But no customer info in spec - just show booking data dictionary and redirect for now

        # TODO: without customer id provided, cannot make rental or reservation.
        # For now, simulate a fake reservation_id (e.g. incremental or 1) to redirect.

        # We'll create a new rental_id and reservation_id assuming the last +1
        # We'll create a minimal dummy rental and reservation with status 'Pending', customer_id 1 (default)

        try:
            rentals = read_rentals()
            reservations = read_reservations()
            vehicles = read_vehicles()

            max_rental_id = max([r['rental_id'] for r in rentals], default=0)
            max_reservation_id = max([r['reservation_id'] for r in reservations], default=0)
            max_customer_id = 1  # Since no customer info specified

            rental_id = max_rental_id + 1
            reservation_id = max_reservation_id + 1

            # Find vehicle for daily_rate and to validate availability
            vehicle = next((veg for veg in vehicles if veg['vehicle_id'] == vehicle_id), None)
            if not vehicle or vehicle['status'].lower() != 'available':
                return "Vehicle not available", 400

            # Calculate total price
            from datetime import datetime
            try:
                dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                delta = (dt_dropoff - dt_pickup).days
                if delta <= 0:
                    return "Invalid date range", 400
                total_price = vehicle['daily_rate'] * delta
            except Exception:
                return "Invalid date format", 400

            # Create new rental entry
            rental_entry = {
                'rental_id': rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': max_customer_id,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'pickup_location': pickup_location or '',
                'dropoff_location': dropoff_location or '',
                'total_price': total_price,
                'status': 'Pending'
            }

            # Add to rentals list
            rentals.append(rental_entry)

            # Update reservations with new entry, insurance_id default 0, special_requests empty
            reservation_entry = {
                'reservation_id': reservation_id,
                'rental_id': rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': max_customer_id,
                'status': 'Pending',
                'insurance_id': 0,
                'special_requests': ''
            }

            reservations.append(reservation_entry)

            # Write updated data back
            try:
                with open('data/rentals.txt', 'w', encoding='utf-8') as f:
                    for r in rentals:
                        f.write(f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']:.2f}|{r['status']}\n")

                write_reservations(reservations)
            except Exception:
                return "Failed to save booking data", 500

            # Redirect to insurance options page with reservation_id
            return redirect(url_for('insurance_options', reservation_id=reservation_id))

        except Exception:
            return "Error processing booking", 500

    return render_template('booking.html', vehicle_id=vehicle_id, locations=sorted(locations))


@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance()

    if request.method == 'POST':
        selected_plan_id = request.form.get('selected_plan_id')
        if not selected_plan_id:
            return "No insurance plan selected", 400
        try:
            selected_plan_id = int(selected_plan_id)
        except ValueError:
            return "Invalid insurance plan id", 400

        # Update reservation to set insurance_id and status Confirmed
        reservations = read_reservations()
        updated = False
        for r in reservations:
            if r['reservation_id'] == reservation_id:
                r['insurance_id'] = selected_plan_id
                r['status'] = 'Confirmed'
                updated = True
                break
        if not updated:
            return "Reservation not found", 404

        write_reservations(reservations)

        # Confirmed, redirect to reservation_management page
        return redirect(url_for('reservation_management'))

    # For GET, just show insurance plans
    return render_template('insurance_options.html', insurance_plans=insurance_plans)


@app.route('/rental_history')
def rental_history():
    rentals = read_rentals()
    vehicles = read_vehicles()
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}

    context_rentals = []
    for r in rentals:
        context_rentals.append({
            'rental_id': str(r['rental_id']),
            'vehicle': vehicle_map.get(r['vehicle_id'], 'Unknown'),
            'pickup_date': r['pickup_date'],
            'dropoff_date': r['dropoff_date'],
            'pickup_location': r['pickup_location'],
            'dropoff_location': r['dropoff_location'],
            'status': r['status']
        })

    return render_template('rental_history.html', rentals=context_rentals)


@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    vehicles = read_vehicles()
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}

    if request.method == 'POST':
        action = request.form.get('action')
        reservation_id = request.form.get('reservation_id')
        try:
            reservation_id = int(reservation_id)
        except Exception:
            return "Invalid reservation id", 400

        updated = False
        for r in reservations:
            if r['reservation_id'] == reservation_id:
                if action == 'modify':
                    # No details provided on modification specifics, simulate change to 'Modified' if allowed
                    if r['status'].lower() in ['confirmed', 'active']:
                        r['status'] = 'Modified'
                        updated = True
                elif action == 'cancel':
                    if r['status'].lower() not in ['cancelled', 'completed']:
                        r['status'] = 'Cancelled'
                        updated = True
                break

        if updated:
            write_reservations(reservations)
        return redirect(url_for('reservation_management'))

    context_reservations = []
    for r in reservations:
        context_reservations.append({
            'reservation_id': str(r['reservation_id']),
            'vehicle': vehicle_map.get(r['vehicle_id'], 'Unknown'),
            'pickup_date': '',  # Not in reservation tables, but rental has dates
            'dropoff_date': '',
            'status': r['status'],
            'insurance_id': str(r.get('insurance_id', 0)),
            'special_requests': r.get('special_requests', '')
        })

    # Augment pickup_date and dropoff_date from rentals
    rentals = read_rentals()
    rental_map = {r['rental_id']: r for r in rentals}
    for cr in context_reservations:
        try:
            res_id = int(cr['reservation_id'])
            res = next(r for r in reservations if r['reservation_id'] == res_id)
            rental = rental_map.get(res['rental_id'], None)
            if rental:
                cr['pickup_date'] = rental['pickup_date']
                cr['dropoff_date'] = rental['dropoff_date']
        except Exception:
            pass

    return render_template('reservations.html', reservations=context_reservations)


@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations = read_reservations()
    vehicles = read_vehicles()
    vehicle_map = {v['vehicle_id']: f"{v['make']} {v['model']}" for v in vehicles}

    context_reservations = []
    for r in reservations:
        context_reservations.append({
            'reservation_id': str(r['reservation_id']),
            'vehicle': vehicle_map.get(r['vehicle_id'], 'Unknown'),
            'pickup_date': '',
            'dropoff_date': '',
            'status': r['status']
        })

    # Augment pickup_date and dropoff_date from rentals
    rentals = read_rentals()
    rental_map = {r['rental_id']: r for r in rentals}
    for cr in context_reservations:
        try:
            res_id = int(cr['reservation_id'])
            res = next(r for r in reservations if r['reservation_id'] == res_id)
            rental = rental_map.get(res['rental_id'], None)
            if rental:
                cr['pickup_date'] = rental['pickup_date']
                cr['dropoff_date'] = rental['dropoff_date']
        except Exception:
            pass

    if request.method == 'POST':
        form = request.form
        try:
            reservation_id = int(form.get('reservation_id', '0'))
            driver_assistance = form.get('driver_assistance') == 'on'
            gps_option = form.get('gps_option') == 'on'
            child_seats = form.get('child_seats', '0')
            notes = form.get('notes', '')

            try:
                child_seats = int(child_seats)
                if child_seats < 0:
                    child_seats = 0
            except Exception:
                child_seats = 0

            # Find reservation to update
            updated = False
            for r in reservations:
                if r['reservation_id'] == reservation_id:
                    # Construct special requests string
                    specials = []
                    if driver_assistance:
                        specials.append('Driver assistance requested')
                    if gps_option:
                        specials.append('GPS option requested')
                    if child_seats > 0:
                        specials.append(f'{child_seats} child seat(s)')
                    if notes.strip() != '':
                        specials.append(notes.strip())
                    r['special_requests'] = '; '.join(specials)
                    updated = True
                    break

            if updated:
                write_reservations(reservations)
            else:
                return "Reservation not found", 404

            return redirect(url_for('special_requests'))
        except Exception:
            return "Invalid form submission", 400

    return render_template('special_requests.html', reservations=context_reservations)


@app.route('/locations')
def locations_page():
    locations = read_locations()
    context_locations = []
    for loc in locations:
        context_locations.append({
            'location_id': str(loc['location_id']),
            'city': loc['city'],
            'address': loc['address'],
            'phone': loc['phone'],
            'hours': loc['hours'],
            'available_vehicles': str(loc['available_vehicles'])
        })
    return render_template('locations.html', locations=context_locations)


if __name__ == '__main__':
    app.run(debug=True)
