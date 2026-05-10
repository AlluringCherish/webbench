'''
Main backend application for CarRental web application.
Defines all routes corresponding to frontend pages, including the root '/' route serving the Dashboard page.
Ensures all frontend navigation URLs correspond exactly to backend routes.
Enhances booking to insurance flow by preserving booking data in session.
'''
from flask import Flask, render_template, request, redirect, url_for, session
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management
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
def read_insurance():
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
    return insurance_plans
def read_rentals():
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
                        'total_price': float(parts[7]),
                        'status': parts[8]
                    }
                    rentals.append(rental)
    except FileNotFoundError:
        pass
    return rentals
def read_reservations():
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
    return reservations
@app.route('/')
def dashboard():
    '''
    Route for Dashboard page - root route '/'
    Loads featured vehicles and promotions (static for now)
    '''
    vehicles = read_vehicles()
    # For featured vehicles, pick first 3 available vehicles
    featured_vehicles = [v for v in vehicles if v['status'] == 'Available'][:3]
    promotions = [
        "10% off for rentals over 7 days!",
        "Free GPS with every SUV rental!",
        "Weekend special: Luxury cars at 20% discount!"
    ]
    return render_template('dashboard.html',
                           featured_vehicles=featured_vehicles,
                           promotions=promotions)
@app.route('/search')
def vehicle_search():
    '''
    Route for Vehicle Search page
    Supports optional query parameters for filtering
    '''
    vehicles = read_vehicles()
    locations = read_locations()
    # Get filters from query parameters
    location_filter = request.args.get('location', '')
    vehicle_type_filter = request.args.get('vehicle_type', '')
    date_range = request.args.get('date_range', '')
    filtered_vehicles = vehicles
    if vehicle_type_filter:
        filtered_vehicles = [v for v in filtered_vehicles if v['vehicle_type'].lower() == vehicle_type_filter.lower()]
    # Location filter is for pickup location, but vehicles.txt does not have location info
    # So we skip filtering vehicles by location here, or could be enhanced later
    return render_template('vehicle_search.html',
                           vehicles=filtered_vehicles,
                           locations=locations,
                           location_filter=location_filter,
                           vehicle_type_filter=vehicle_type_filter,
                           date_range=date_range)
@app.route('/vehicle/<vehicle_id>')
def vehicle_details(vehicle_id):
    '''
    Route for Vehicle Details page
    Shows detailed info for a specific vehicle
    '''
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    # For simplicity, no reviews data file, so empty list
    vehicle_reviews = []
    return render_template('vehicle_details.html',
                           vehicle=vehicle,
                           vehicle_reviews=vehicle_reviews)
@app.route('/booking/<vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    '''
    Route for Booking page
    GET: Show booking form for vehicle
    POST: Process booking data and store in session for next step
    '''
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    locations = read_locations()
    if request.method == 'POST':
        # Process booking form submission
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        # Calculate total price (simplified)
        from datetime import datetime
        try:
            pd = datetime.strptime(pickup_date, '%Y-%m-%d')
            dd = datetime.strptime(dropoff_date, '%Y-%m-%d')
            days = (dd - pd).days
            if days < 1:
                days = 1
        except Exception:
            days = 1
        total_price = days * vehicle['daily_rate']
        # Store booking info in session to preserve context
        session['booking'] = {
            'vehicle_id': vehicle['vehicle_id'],
            'make': vehicle['make'],
            'model': vehicle['model'],
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'days': days,
            'total_price': total_price
        }
        return render_template('booking.html',
                               vehicle=vehicle,
                               locations=locations,
                               pickup_location=pickup_location,
                               dropoff_location=dropoff_location,
                               pickup_date=pickup_date,
                               dropoff_date=dropoff_date,
                               total_price=total_price,
                               price_calculated=True)
    else:
        # Clear any previous booking info on GET
        session.pop('booking', None)
        return render_template('booking.html',
                               vehicle=vehicle,
                               locations=locations,
                               price_calculated=False)
@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options():
    '''
    Route for Insurance Options page
    GET: Show insurance plans with booking context if available
    POST: Process insurance selection (not fully implemented)
    '''
    insurance_plans = read_insurance()
    booking = session.get('booking')
    if not booking:
        # If no booking info, redirect to dashboard or booking start
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        selected_insurance_id = request.form.get('insurance_id')
        selected_plan = next((p for p in insurance_plans if p['insurance_id'] == selected_insurance_id), None)
        if not selected_plan:
            return "Invalid insurance selection", 400
        # Store selected insurance in session
        session['booking']['insurance_id'] = selected_insurance_id
        session['booking']['insurance_plan_name'] = selected_plan['plan_name']
        session['booking']['insurance_daily_cost'] = selected_plan['daily_cost']
        # For demo, just render confirmation page or redirect
        return render_template('insurance_options.html',
                               insurance_plans=insurance_plans,
                               selected_plan=selected_plan,
                               confirmed=True,
                               booking=booking)
    else:
        return render_template('insurance_options.html',
                               insurance_plans=insurance_plans,
                               selected_plan=None,
                               confirmed=False,
                               booking=booking)
@app.route('/history')
def rental_history():
    '''
    Route for Rental History page
    Supports optional status filter
    '''
    rentals = read_rentals()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    status_filter = request.args.get('status', 'All')
    filtered_rentals = rentals
    if status_filter and status_filter != 'All':
        filtered_rentals = [r for r in rentals if r['status'] == status_filter]
    # Enrich rentals with vehicle info
    for r in filtered_rentals:
        r['vehicle'] = vehicles.get(r['vehicle_id'], {})
    return render_template('rental_history.html',
                           rentals=filtered_rentals,
                           status_filter=status_filter)
@app.route('/reservations')
def reservations():
    '''
    Route for Reservation Management page
    '''
    reservations = read_reservations()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    # Enrich reservations with vehicle info
    for res in reservations:
        res['vehicle'] = vehicles.get(res['vehicle_id'], {})
    return render_template('reservations.html',
                           reservations=reservations)
@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    '''
    Route for Special Requests page
    GET: Show form
    POST: Process special requests submission (not fully implemented)
    '''
    reservations = read_reservations()
    if request.method == 'POST':
        reservation_id = request.form.get('select_reservation')
        driver_assistance = request.form.get('driver_assistance_checkbox')
        gps_option = request.form.get('gps_option_checkbox')
        child_seat_quantity = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes')
        # For demo, just acknowledge submission
        return render_template('special_requests.html',
                               reservations=reservations,
                               submitted=True)
    else:
        return render_template('special_requests.html',
                               reservations=reservations,
                               submitted=False)
@app.route('/locations')
def locations():
    '''
    Route for Locations page
    Supports optional filters and search
    '''
    locations = read_locations()
    hours_filter = request.args.get('hours_filter', '')
    search_location = request.args.get('search_location', '').lower()
    filtered_locations = locations
    if hours_filter:
        filtered_locations = [loc for loc in filtered_locations if loc['hours'] == hours_filter]
    if search_location:
        filtered_locations = [loc for loc in filtered_locations if search_location in loc['city'].lower() or search_location in loc['address'].lower()]
    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter=hours_filter,
                           search_location=search_location)
if __name__ == '__main__':
    app.run(debug=True)