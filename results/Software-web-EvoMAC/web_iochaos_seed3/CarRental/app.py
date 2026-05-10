'''
Main backend application for CarRental web application.
Defines all routes including root '/' serving the Dashboard page.
Ensures all frontend navigation URLs correspond exactly to backend routes.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
def read_vehicles():
    vehicles = []
    try:
        with open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    vehicle = {
                        'vehicle_id': parts[0],
                        'make': parts[1],
                        'model': parts[2],
                        'vehicle_type': parts[3],
                        'daily_rate': float(parts[4]),
                        'seats': parts[5],
                        'transmission': parts[6],
                        'fuel_type': parts[7],
                        'status': parts[8]
                    }
                    vehicles.append(vehicle)
    except FileNotFoundError:
        pass
    return vehicles
def read_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    location = {
                        'location_id': parts[0],
                        'city': parts[1],
                        'address': parts[2],
                        'phone': parts[3],
                        'hours': parts[4],
                        'available_vehicles': parts[5]
                    }
                    locations.append(location)
    except FileNotFoundError:
        pass
    return locations
def read_promotions():
    # For demonstration, static promotions
    return [
        {'title': 'Winter Special', 'description': '10% off all SUVs!'},
        {'title': 'Weekend Deal', 'description': 'Rent 2 days, get 1 free!'}
    ]
@app.route('/')
def dashboard():
    '''
    Root route serving the Dashboard page.
    Displays featured vehicles, promotions, and navigation buttons.
    '''
    vehicles = read_vehicles()
    # For featured vehicles, pick first 3 available vehicles
    featured = [v for v in vehicles if v['status'] == 'Available'][:3]
    promotions = read_promotions()
    return render_template('dashboard.html', featured_vehicles=featured, promotions=promotions)
@app.route('/search-vehicles')
def search_vehicles():
    '''
    Vehicle Search Page route.
    Displays all available vehicles with filters.
    '''
    vehicles = read_vehicles()
    locations = read_locations()
    return render_template('vehicle_search.html', vehicles=vehicles, locations=locations)
@app.route('/vehicle-details/<vehicle_id>')
def vehicle_details(vehicle_id):
    '''
    Vehicle Details Page route.
    Displays detailed info about a specific vehicle.
    '''
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    # For demo, static reviews
    reviews = [
        {'user': 'Alice', 'comment': 'Great car! Smooth ride.'},
        {'user': 'Bob', 'comment': 'Comfortable and fuel efficient.'}
    ]
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    '''
    Booking Page route.
    Allows user to select pickup/dropoff locations and dates.
    '''
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    locations = read_locations()
    total_price = None
    if request.method == 'POST':
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        # Calculate days difference
        from datetime import datetime
        try:
            d1 = datetime.strptime(pickup_date, '%Y-%m-%d')
            d2 = datetime.strptime(dropoff_date, '%Y-%m-%d')
            days = (d2 - d1).days
            if days < 1:
                total_price = 0
            else:
                total_price = days * vehicle['daily_rate']
        except Exception:
            total_price = 0
        return render_template('booking.html', vehicle=vehicle, locations=locations,
                               total_price=total_price, pickup_date=pickup_date,
                               dropoff_date=dropoff_date, pickup_location=pickup_location,
                               dropoff_location=dropoff_location)
    return render_template('booking.html', vehicle=vehicle, locations=locations, total_price=total_price)
@app.route('/insurance-options', methods=['GET', 'POST'])
def insurance_options():
    '''
    Insurance Options Page route.
    Displays insurance plans and allows selection.
    '''
    insurance_plans = []
    try:
        with open(os.path.join(DATA_DIR, 'insurance.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    plan = {
                        'insurance_id': parts[0],
                        'plan_name': parts[1],
                        'description': parts[2],
                        'daily_cost': float(parts[3]),
                        'coverage_limit': parts[4],
                        'deductible': parts[5]
                    }
                    insurance_plans.append(plan)
    except FileNotFoundError:
        pass
    selected_plan = None
    if request.method == 'POST':
        selected_id = request.form.get('insurance_plan')
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_id), None)
        # Here you would handle booking confirmation logic
        return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_plan=selected_plan, confirmed=True)
    return render_template('insurance_options.html', insurance_plans=insurance_plans, selected_plan=selected_plan, confirmed=False)
@app.route('/rental-history')
def rental_history():
    '''
    Rental History Page route.
    Displays all previous rentals with filter by status.
    '''
    status_filter = request.args.get('status', 'All')
    rentals = []
    try:
        with open(os.path.join(DATA_DIR, 'rentals.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    rental = {
                        'rental_id': parts[0],
                        'vehicle_id': parts[1],
                        'customer_id': parts[2],
                        'pickup_date': parts[3],
                        'dropoff_date': parts[4],
                        'pickup_location': parts[5],
                        'dropoff_location': parts[6],
                        'total_price': parts[7],
                        'status': parts[8]
                    }
                    if status_filter == 'All' or rental['status'] == status_filter:
                        rentals.append(rental)
    except FileNotFoundError:
        pass
    return render_template('rental_history.html', rentals=rentals, status_filter=status_filter)
@app.route('/my-reservations')
def my_reservations():
    '''
    Reservation Management Page route.
    Displays current and upcoming reservations.
    '''
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    reservation = {
                        'reservation_id': parts[0],
                        'rental_id': parts[1],
                        'vehicle_id': parts[2],
                        'customer_id': parts[3],
                        'status': parts[4],
                        'insurance_id': parts[5],
                        'special_requests': parts[6]
                    }
                    reservations.append(reservation)
    except FileNotFoundError:
        pass
    sort_by_date = request.args.get('sort', None)
    # Sorting logic can be added here if needed
    return render_template('reservations.html', reservations=reservations)
@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    '''
    Special Requests Page route.
    Allows users to add special requests to their reservation.
    '''
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    reservation = {
                        'reservation_id': parts[0],
                        'rental_id': parts[1],
                        'vehicle_id': parts[2],
                        'customer_id': parts[3],
                        'status': parts[4],
                        'insurance_id': parts[5],
                        'special_requests': parts[6]
                    }
                    reservations.append(reservation)
    except FileNotFoundError:
        pass
    message = ''
    if request.method == 'POST':
        reservation_id = request.form.get('select_reservation')
        driver_assistance = request.form.get('driver_assistance') == 'on'
        gps_option = request.form.get('gps_option') == 'on'
        child_seat_quantity = request.form.get('child_seat_quantity', '0')
        special_notes = request.form.get('special_notes', '')
        # Update the special_requests field for the selected reservation in reservations.txt
        updated_reservations = []
        for res in reservations:
            if res['reservation_id'] == reservation_id:
                # Compose special requests string
                requests_list = []
                if driver_assistance:
                    requests_list.append('Driver assistance requested')
                if gps_option:
                    requests_list.append('GPS option requested')
                if child_seat_quantity and child_seat_quantity != '0':
                    requests_list.append(f'Child seats: {child_seat_quantity}')
                if special_notes.strip():
                    requests_list.append(f'Notes: {special_notes.strip()}')
                res['special_requests'] = '; '.join(requests_list) if requests_list else ''
            updated_reservations.append(res)
        # Write back updated reservations to file
        try:
            with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
                for res in updated_reservations:
                    line = '|'.join([
                        res['reservation_id'],
                        res['rental_id'],
                        res['vehicle_id'],
                        res['customer_id'],
                        res['status'],
                        res['insurance_id'],
                        res['special_requests']
                    ])
                    f.write(line + '\n')
            message = 'Special requests submitted successfully.'
            reservations = updated_reservations
        except Exception:
            message = 'Failed to submit special requests.'
    return render_template('special_requests.html', reservations=reservations, message=message)
@app.route('/locations')
def locations():
    '''
    Locations Page route.
    Displays all rental pickup and dropoff locations with filters.
    '''
    locations = read_locations()
    hours_filter = request.args.get('hours', None)
    search_query = request.args.get('search', '').lower()
    filtered_locations = []
    for loc in locations:
        if hours_filter and hours_filter != 'All':
            if hours_filter == '24/7' and loc['hours'] != '24/7':
                continue
            elif hours_filter == 'Business Hours' and loc['hours'] == '24/7':
                continue
            elif hours_filter == 'Weekend' and loc['hours'] == '24/7':
                continue
        if search_query:
            if search_query not in loc['city'].lower() and search_query not in loc['address'].lower():
                continue
        filtered_locations.append(loc)
    return render_template('locations.html', locations=filtered_locations, hours_filter=hours_filter, search_query=search_query)
if __name__ == '__main__':
    app.run(debug=True)