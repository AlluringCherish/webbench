from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions for data handling

def read_vehicles():
    vehicles = []
    try:
        with open('data/vehicles.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) < 2:
                    continue
                # Since schema is not explicit, using all fields as is
                vehicle = {
                    'vehicle_id': fields[0],
                    'name': fields[1],
                }
                vehicles.append(vehicle)
    except Exception:
        pass  # Graceful error handling
    return vehicles


def read_customers():
    customers = []
    try:
        with open('data/customers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 6:
                    continue
                customer = {
                    'customer_id': fields[0],
                    'name': fields[1],
                    'email': fields[2],
                    'phone': fields[3],
                    'driver_license': fields[4],
                    'license_expiry': fields[5],
                }
                customers.append(customer)
    except Exception:
        pass
    return customers


def read_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) < 4:
                    continue
                location = {
                    'location_id': fields[0],
                    'address': fields[1],
                    'phone': fields[2],
                    'hours': fields[3],
                    'capacity': fields[4] if len(fields) > 4 else None
                }
                locations.append(location)
    except Exception:
        pass
    return locations


def read_insurances():
    insurances = []
    try:
        with open('data/insurance.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) != 6:
                    continue
                insurance = {
                    'insurance_id': fields[0],
                    'plan_name': fields[1],
                    'description': fields[2],
                    'daily_cost': fields[3],
                    'coverage_limit': fields[4],
                    'deductible': fields[5],
                }
                insurances.append(insurance)
    except Exception:
        pass
    return insurances


def read_reservations():
    reservations = []
    try:
        with open('data/reservations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) < 7:
                    continue
                reservation = {
                    'reservation_id': fields[0],
                    'customer_id': fields[1],
                    'vehicle_id': fields[2],
                    'insurance_id': fields[3],
                    'status': fields[4],
                    'num_days': fields[5],
                    'notes': fields[6],
                }
                reservations.append(reservation)
    except Exception:
        pass
    return reservations


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Read vehicles for featured recommendations
    featured_vehicles = read_vehicles()[:5]  # Limiting 5 for demo
    promotions = []  # Placeholder for promotions data - not specified
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


@app.route('/vehicles', methods=['GET'])
def vehicles():
    # Optional filter vehicle_type from query
    vehicle_type = request.args.get('vehicle_type')
    vehicles_list = read_vehicles()
    filtered_vehicles = vehicles_list
    if vehicle_type:
        # No detailed schema to filter on type, assuming filtering by name containing type
        filtered_vehicles = [v for v in vehicles_list if vehicle_type.lower() in v['name'].lower()]
    selected_filters = {'vehicle_type': vehicle_type} if vehicle_type else {}
    return render_template('vehicles.html', vehicles=filtered_vehicles, selected_filters=selected_filters)


@app.route('/vehicle/<vehicle_id>', methods=['GET'])
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    backend_reviews = []  # No schema or source provided for reviews
    if vehicle is None:
        return "Vehicle not found", 404
    return render_template('vehicle_details.html', vehicle=vehicle, customer_reviews=backend_reviews)


@app.route('/booking', methods=['GET', 'POST'])
def booking_page():
    locations = read_locations()
    if request.method == 'POST':
        # Process booking form
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        total_price = request.form.get('total_price')

        # Basic validation
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date or not total_price:
            error = 'All booking fields are required.'
            return render_template('booking_page.html', locations=locations, error=error)

        # Normally, would save reservation here

        return redirect(url_for('insurance_selection'))

    return render_template('booking_page.html', locations=locations)


@app.route('/insurance', methods=['GET', 'POST'])
def insurance_selection():
    insurances = read_insurances()
    if request.method == 'POST':
        selected_plan = request.form.get('insurance_plan')
        if not selected_plan:
            error = 'Please select an insurance plan.'
            return render_template('insurance_selection.html', insurances=insurances, error=error)

        return redirect(url_for('dashboard'))

    return render_template('insurance_selection.html', insurances=insurances)


@app.route('/history', methods=['GET'])
def rental_history():
    rental_history = read_reservations()
    filter_status = request.args.get('filter_status')
    if filter_status:
        rental_history = [r for r in rental_history if r['status'].lower() == filter_status.lower()]
    return render_template('history.html', rental_history=rental_history, filter_status=filter_status)


@app.route('/reservations', methods=['GET', 'POST'])
def reservation_management():
    reservations = read_reservations()
    if request.method == 'POST':
        # Placeholder for reservation modifications/cancellations
        # Actual implementations depend on form data and actions
data = request.form
        # For example, cancel or update reservation
        return redirect(url_for('reservation_management'))

    return render_template('reservations.html', reservations=reservations)


@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    if request.method == 'POST':
        request_type = request.form.get('request_type')
        details = request.form.get('details')
        if not request_type or not details:
            error = 'Both request type and details are required.'
            return render_template('special_requests.html', error=error)
        # Process special request: save or handle
        return redirect(url_for('special_requests'))

    user_requests = []  # Placeholder for user request history
    return render_template('special_requests.html', user_requests=user_requests)


@app.route('/locations', methods=['GET'])
def locations():
    locations_list = read_locations()
    return render_template('locations.html', locations=locations_list)


if __name__ == '__main__':
    app.run(debug=True)
