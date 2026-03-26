'''
Main backend application for CarRental web application.
Handles routing, data reading/writing from local text files,
and rendering HTML templates for all nine pages.
Includes navigation improvements for better user experience.
'''
import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
app = Flask(__name__)
DATA_DIR = 'data'
def read_vehicles():
    vehicles = []
    filepath = os.path.join(DATA_DIR, 'vehicles.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 9:
                    continue
                vehicle = {
                    'vehicle_id': row[0],
                    'make': row[1],
                    'model': row[2],
                    'vehicle_type': row[3],
                    'daily_rate': float(row[4]),
                    'seats': int(row[5]),
                    'transmission': row[6],
                    'fuel_type': row[7],
                    'status': row[8]
                }
                vehicles.append(vehicle)
    except FileNotFoundError:
        print("Warning: vehicles.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading vehicles.txt: {e}")
    return vehicles
def read_customers():
    customers = []
    filepath = os.path.join(DATA_DIR, 'customers.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 6:
                    continue
                customer = {
                    'customer_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'driver_license': row[4],
                    'license_expiry': row[5]
                }
                customers.append(customer)
    except FileNotFoundError:
        print("Warning: customers.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading customers.txt: {e}")
    return customers
def read_locations():
    locations = []
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 6:
                    continue
                location = {
                    'location_id': row[0],
                    'city': row[1],
                    'address': row[2],
                    'phone': row[3],
                    'hours': row[4],
                    'available_vehicles': int(row[5])
                }
                locations.append(location)
    except FileNotFoundError:
        print("Warning: locations.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading locations.txt: {e}")
    return locations
def read_rentals():
    rentals = []
    filepath = os.path.join(DATA_DIR, 'rentals.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 9:
                    continue
                rental = {
                    'rental_id': row[0],
                    'vehicle_id': row[1],
                    'customer_id': row[2],
                    'pickup_date': row[3],
                    'dropoff_date': row[4],
                    'pickup_location': row[5],
                    'dropoff_location': row[6],
                    'total_price': float(row[7]),
                    'status': row[8]
                }
                rentals.append(rental)
    except FileNotFoundError:
        print("Warning: rentals.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading rentals.txt: {e}")
    return rentals
def read_insurance():
    insurance_plans = []
    filepath = os.path.join(DATA_DIR, 'insurance.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 6:
                    continue
                plan = {
                    'insurance_id': row[0],
                    'plan_name': row[1],
                    'description': row[2],
                    'daily_cost': float(row[3]),
                    'coverage_limit': row[4],
                    'deductible': row[5]
                }
                insurance_plans.append(plan)
    except FileNotFoundError:
        print("Warning: insurance.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading insurance.txt: {e}")
    return insurance_plans
def read_reservations():
    reservations = []
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) != 7:
                    continue
                reservation = {
                    'reservation_id': row[0],
                    'rental_id': row[1],
                    'vehicle_id': row[2],
                    'customer_id': row[3],
                    'status': row[4],
                    'insurance_id': row[5],
                    'special_requests': row[6]
                }
                reservations.append(reservation)
    except FileNotFoundError:
        print("Warning: reservations.txt not found in data directory.")
    except Exception as e:
        print(f"Error reading reservations.txt: {e}")
    return reservations
def write_reservations(reservations):
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for res in reservations:
                writer.writerow([
                    res['reservation_id'],
                    res['rental_id'],
                    res['vehicle_id'],
                    res['customer_id'],
                    res['status'],
                    res['insurance_id'],
                    res['special_requests']
                ])
    except Exception as e:
        print(f"Error writing reservations.txt: {e}")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.route('/')
def dashboard():
    try:
        vehicles = read_vehicles()
        # Featured vehicles: first 3 available vehicles
        featured_vehicles = [v for v in vehicles if v['status'].lower() == 'available'][:3]
        promotions = [
            "10% off on all rentals over 7 days!",
            "Free GPS with every SUV rental!",
            "Luxury cars at economy prices this weekend!"
        ]
        return render_template('dashboard.html',
                               featured_vehicles=featured_vehicles,
                               promotions=promotions)
    except Exception as e:
        print(f"Error rendering dashboard.html: {e}")
        abort(500)
@app.route('/vehicle_search')
def vehicle_search():
    try:
        vehicles = read_vehicles()
        locations = read_locations()
        location_filter = request.args.get('location_filter', '').strip()
        vehicle_type_filter = request.args.get('vehicle_type_filter', '').strip()
        date_range = request.args.get('date_range_input', '').strip()
        filtered_vehicles = [v for v in vehicles if v['status'].lower() == 'available']
        if location_filter:
            # Filter vehicles by availability at location
            # Since vehicles.txt does not have location info, we skip this filter realistically
            # But we can simulate by checking if location has available vehicles > 0
            loc = next((loc for loc in locations if loc['city'].lower() == location_filter.lower()), None)
            if loc and loc['available_vehicles'] == 0:
                filtered_vehicles = []
            # else no filtering by location on vehicles
        if vehicle_type_filter:
            filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'].lower() == vehicle_type_filter.lower()]
        # date_range input is not used for filtering here as no booking logic yet
        return render_template('vehicle_search.html',
                               locations=locations,
                               filtered_vehicles=filtered_vehicles,
                               location_filter=location_filter,
                               vehicle_type_filter=vehicle_type_filter,
                               date_range=date_range)
    except Exception as e:
        print(f"Error rendering vehicle_search.html: {e}")
        abort(500)
@app.route('/vehicle_details/<vehicle_id>')
def vehicle_details(vehicle_id):
    try:
        vehicles = read_vehicles()
        vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
        if not vehicle:
            abort(404)
        # Example specs (engine not in data, so hardcoded)
        vehicle_specs = {
            'engine': '2.5L 4-cylinder',
            'seats': vehicle['seats'],
            'transmission': vehicle['transmission']
        }
        # Example reviews (static)
        vehicle_reviews = [
            {'author': 'John Doe', 'comment': 'Great car, very comfortable!'},
            {'author': 'Jane Smith', 'comment': 'Smooth ride and fuel efficient.'}
        ]
        return render_template('vehicle_details.html',
                               vehicle=vehicle,
                               vehicle_specs=vehicle_specs,
                               vehicle_reviews=vehicle_reviews)
    except Exception as e:
        print(f"Error rendering vehicle_details.html: {e}")
        abort(500)
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    try:
        vehicles = read_vehicles()
        locations = read_locations()
        if request.method == 'GET':
            vehicle_id = request.args.get('vehicle_id', '')
            selected_vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None) if vehicle_id else None
            return render_template('booking.html',
                                   booking_page=True,
                                   selected_vehicle=selected_vehicle,
                                   locations=locations,
                                   total_price=None,
                                   pickup_location='',
                                   dropoff_location='',
                                   pickup_date='',
                                   dropoff_date='')
        else:
            # POST
            action = request.form.get('action', '')
            vehicle_id = request.form.get('vehicle_id', '')
            pickup_location = request.form.get('pickup_location', '')
            dropoff_location = request.form.get('dropoff_location', '')
            pickup_date = request.form.get('pickup_date', '')
            dropoff_date = request.form.get('dropoff_date', '')
            selected_vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
            if not selected_vehicle:
                abort(404)
            if action == 'calculate_price':
                # Calculate total price
                try:
                    dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                    dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                    days = (dt_dropoff - dt_pickup).days
                    if days <= 0:
                        total_price = 0.0
                    else:
                        total_price = days * selected_vehicle['daily_rate']
                except Exception:
                    total_price = 0.0
                return render_template('booking.html',
                                       booking_page=True,
                                       selected_vehicle=selected_vehicle,
                                       locations=locations,
                                       total_price=total_price,
                                       pickup_location=pickup_location,
                                       dropoff_location=dropoff_location,
                                       pickup_date=pickup_date,
                                       dropoff_date=dropoff_date)
            elif action == 'proceed_to_insurance':
                # Redirect to insurance options page with booking info as query params
                return redirect(url_for('insurance_options',
                                        vehicle_id=vehicle_id,
                                        pickup_location=pickup_location,
                                        dropoff_location=dropoff_location,
                                        pickup_date=pickup_date,
                                        dropoff_date=dropoff_date))
            else:
                # Unknown action, reload booking page
                return redirect(url_for('booking'))
    except Exception as e:
        print(f"Error rendering booking.html: {e}")
        abort(500)
@app.route('/insurance_options', methods=['GET', 'POST'])
def insurance_options():
    try:
        insurance_plans = read_insurance()
        vehicles = read_vehicles()
        vehicle_id = request.args.get('vehicle_id') or request.form.get('vehicle_id')
        pickup_location = request.args.get('pickup_location') or request.form.get('pickup_location')
        dropoff_location = request.args.get('dropoff_location') or request.form.get('dropoff_location')
        pickup_date = request.args.get('pickup_date') or request.form.get('pickup_date')
        dropoff_date = request.args.get('dropoff_date') or request.form.get('dropoff_date')
        selected_vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None) if vehicle_id else None
        if not selected_vehicle:
            abort(404)
        selected_insurance_id = None
        insurance_price = None
        insurance_description = ''
        if request.method == 'POST':
            selected_insurance_id = request.form.get('selected_insurance')
            if selected_insurance_id:
                selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
                if selected_plan:
                    try:
                        dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                        dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                        days = (dt_dropoff - dt_pickup).days
                        if days <= 0:
                            days = 1
                        insurance_price = days * selected_plan['daily_cost']
                        insurance_description = selected_plan['description']
                    except Exception:
                        insurance_price = 0.0
                        insurance_description = selected_plan['description']
                # Here booking confirmation logic would be implemented
                # For now, redirect to dashboard after confirmation
                return redirect(url_for('dashboard'))
        else:
            # GET: default select first insurance plan if any
            if insurance_plans:
                selected_plan = insurance_plans[0]
                selected_insurance_id = selected_plan['insurance_id']
                insurance_description = selected_plan['description']
                try:
                    dt_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
                    dt_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
                    days = (dt_dropoff - dt_pickup).days
                    if days <= 0:
                        days = 1
                    insurance_price = days * selected_plan['daily_cost']
                except Exception:
                    insurance_price = 0.0
        return render_template('insurance_options.html',
                               insurance_plans=insurance_plans,
                               selected_insurance_id=selected_insurance_id,
                               insurance_description=insurance_description,
                               insurance_price=insurance_price,
                               vehicle=selected_vehicle,
                               pickup_location=pickup_location,
                               dropoff_location=dropoff_location,
                               pickup_date=pickup_date,
                               dropoff_date=dropoff_date)
    except Exception as e:
        print(f"Error rendering insurance_options.html: {e}")
        abort(500)
@app.route('/rental_history')
def rental_history():
    try:
        rentals = read_rentals()
        vehicles = read_vehicles()
        status_filter = request.args.get('status_filter', 'All').lower()
        filtered_rentals = rentals
        if status_filter != 'all':
            filtered_rentals = [r for r in rentals if r['status'].lower() == status_filter]
        # Enrich rentals with vehicle model
        for r in filtered_rentals:
            vehicle = next((v for v in vehicles if v['vehicle_id'] == r['vehicle_id']), None)
            r['vehicle_model'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else "Unknown"
        return render_template('rental_history.html',
                               rentals=filtered_rentals,
                               status_filter=status_filter.capitalize())
    except Exception as e:
        print(f"Error rendering rental_history.html: {e}")
        abort(500)
@app.route('/rental_history/<rental_id>')
def rental_detail(rental_id):
    try:
        rentals = read_rentals()
        vehicles = read_vehicles()
        rental = next((r for r in rentals if r['rental_id'] == rental_id), None)
        if not rental:
            abort(404)
        vehicle = next((v for v in vehicles if v['vehicle_id'] == rental['vehicle_id']), None)
        return render_template('rental_detail.html',
                               rental=rental,
                               vehicle=vehicle)
    except Exception as e:
        print(f"Error rendering rental_detail.html: {e}")
        abort(500)
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    try:
        vehicles = read_vehicles()
        reservations = read_reservations()
        if request.method == 'POST':
            # Handle cancel reservation
            cancel_reservation_id = request.form.get('cancel_reservation_id')
            if cancel_reservation_id:
                updated = False
                for res in reservations:
                    if res['reservation_id'] == cancel_reservation_id:
                        res['status'] = 'Cancelled'
                        updated = True
                        break
                if updated:
                    write_reservations(reservations)
                return redirect(url_for('reservations'))
        # Enrich reservations with vehicle info
        for res in reservations:
            vehicle = next((v for v in vehicles if v['vehicle_id'] == res['vehicle_id']), None)
            res['vehicle_name'] = f"{vehicle['make']} {vehicle['model']}" if vehicle else "Unknown"
        return render_template('reservations.html',
                               reservations=reservations)
    except Exception as e:
        print(f"Error rendering reservations.html: {e}")
        abort(500)
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    try:
        reservations = read_reservations()
        if request.method == 'POST':
            selected_reservation_id = request.form.get('select_reservation')
            driver_assistance = request.form.get('driver_assistance_checkbox')
            gps_option = request.form.get('gps_option_checkbox')
            child_seat_quantity = request.form.get('child_seat_quantity', '0')
            special_notes = request.form.get('special_notes', '').strip()
            if not selected_reservation_id:
                # No reservation selected, reload page
                return redirect(url_for('special_requests'))
            # Compose special requests string
            requests_list = []
            if driver_assistance == 'on':
                requests_list.append('Driver assistance requested')
            if gps_option == 'on':
                requests_list.append('GPS option requested')
            try:
                qty = int(child_seat_quantity)
                if qty > 0:
                    requests_list.append(f'{qty} child seat(s) needed')
            except Exception:
                pass
            if special_notes:
                requests_list.append(special_notes)
            special_requests_str = '; '.join(requests_list)
            # Update reservations.txt
            updated = False
            for res in reservations:
                if res['reservation_id'] == selected_reservation_id:
                    res['special_requests'] = special_requests_str
                    updated = True
                    break
            if updated:
                write_reservations(reservations)
            return redirect(url_for('special_requests'))
        else:
            # GET
            selected_reservation_id = request.args.get('selected_reservation')
            selected_reservation = None
            if selected_reservation_id:
                selected_reservation = next((r for r in reservations if r['reservation_id'] == selected_reservation_id), None)
            return render_template('special_requests.html',
                                   reservations=reservations,
                                   selected_reservation=selected_reservation)
    except Exception as e:
        print(f"Error rendering special_requests.html: {e}")
        abort(500)
@app.route('/locations')
def locations():
    try:
        locations = read_locations()
        hours_filter = request.args.get('hours_filter', '').strip()
        search_location = request.args.get('search_location_input', '').strip().lower()
        filtered_locations = locations
        if hours_filter:
            if hours_filter == '24/7':
                filtered_locations = [loc for loc in filtered_locations if loc['hours'] == '24/7']
            elif hours_filter == 'Business Hours':
                filtered_locations = [loc for loc in filtered_locations if loc['hours'] == '09:00-18:00']
            elif hours_filter == 'Weekend':
                filtered_locations = [loc for loc in filtered_locations if loc['hours'].lower().find('weekend') != -1]
        if search_location:
            filtered_locations = [loc for loc in filtered_locations if search_location in loc['city'].lower() or search_location in loc['address'].lower()]
        return render_template('locations.html',
                               locations=filtered_locations,
                               hours_filter=hours_filter,
                               search_location=search_location)
    except Exception as e:
        print(f"Error rendering locations.html: {e}")
        abort(500)
@app.route('/location_detail/<location_id>')
def location_detail(location_id):
    try:
        locations = read_locations()
        location = next((loc for loc in locations if loc['location_id'] == location_id), None)
        if not location:
            abort(404)
        return render_template('location_detail.html',
                               location=location)
    except Exception as e:
        print(f"Error rendering location_detail.html: {e}")
        abort(500)
if __name__ == '__main__':
    app.run(debug=True, port=5000)