from flask import Flask, request, jsonify, render_template, abort
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)

def load_vehicles():
    vehicles = []
    try:
        with open(get_file_path('vehicles.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return vehicles

def save_vehicles(vehicles):
    with open(get_file_path('vehicles.txt'), 'w', encoding='utf-8') as f:
        for v in vehicles:
            line = f"{v['vehicle_id']}|{v['make']}|{v['model']}|{v['vehicle_type']}|{v['daily_rate']:.2f}|{v['seats']}|{v['transmission']}|{v['fuel_type']}|{v['status']}"
            f.write(line + '\n')

# Other load/save functions omitted but unchanged

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return None

def date_ranges_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

@app.route('/dashboard')
def dashboard():
    vehicles = load_vehicles()
    featured_vehicles = [v for v in vehicles if v['status'].lower() == 'available']
    promotions = [
        {"title":"Save 10% on SUVs this weekend!", "description":"Save 10% on SUVs this weekend!"},
        {"title":"Book for 7+ days and get 1 day free!", "description":"Book for 7+ days and get 1 day free!"},
        {"title":"Free GPS on luxury vehicle rentals", "description":"Free GPS on luxury vehicle rentals"}
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions, page_title='Car Rental Dashboard')

@app.route('/vehicles/search', methods=['GET'])
def vehicle_search():
    location = request.args.get('location')
    vehicle_type = request.args.get('vehicle_type')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    vehicles = load_vehicles()
    rentals = load_rentals()

    available_vehicles = [v for v in vehicles if v['status'].lower() == 'available']

    if location:
        pass  # Location filtering logic as before

    if vehicle_type:
        vt_lower = vehicle_type.lower()
        available_vehicles = [v for v in available_vehicles if v['vehicle_type'].lower() == vt_lower]

    if start_date_str and end_date_str:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        if not start_date or not end_date or start_date > end_date:
            return jsonify({'error': 'Invalid date range'}), 400
        filtered_vehicles = []
        for vehicle in available_vehicles:
            vehicle_id = vehicle['vehicle_id']
            overlapping = False
            for rental in rentals:
                if rental['vehicle_id'] == vehicle_id and rental['status'].lower() in ['active', 'confirmed']:
                    rental_start = parse_date(rental['pickup_date'])
                    rental_end = parse_date(rental['dropoff_date'])
                    if date_ranges_overlap(start_date, end_date, rental_start, rental_end):
                        overlapping = True
                        break
            if not overlapping:
                filtered_vehicles.append(vehicle)
        available_vehicles = filtered_vehicles

    return jsonify(available_vehicles)

@app.route('/vehicles/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        abort(404, 'Vehicle not found')
    reviews = []
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews, page_title='Vehicle Details')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        vehicle_id = request.args.get('vehicle_id', type=int)
        locations = load_locations()
        vehicle = None
        if vehicle_id:
            vehicles = load_vehicles()
            vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
        return render_template('booking.html', locations=locations, vehicle=vehicle, page_title='Book Your Rental')
    else:
        data = request.get_json()
        required_fields = ['vehicle_id', 'pickup_location', 'dropoff_location', 'pickup_date', 'dropoff_date', 'customer_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        vehicle_id = data['vehicle_id']
        pickup_location = data['pickup_location']
        dropoff_location = data['dropoff_location']
        pickup_date = parse_date(data['pickup_date'])
        dropoff_date = parse_date(data['dropoff_date'])
        customer_id = data['customer_id']

        if not pickup_date or not dropoff_date or pickup_date > dropoff_date:
            return jsonify({'error': 'Invalid date range'}), 400

        rentals = load_rentals()
        for rental in rentals:
            if rental['vehicle_id'] == vehicle_id and rental['status'].lower() in ['active', 'confirmed']:
                rental_pickup = parse_date(rental['pickup_date'])
                rental_dropoff = parse_date(rental['dropoff_date'])
                if date_ranges_overlap(pickup_date, dropoff_date, rental_pickup, rental_dropoff):
                    return jsonify({'error': 'Vehicle not available for the selected dates'}), 400

        vehicles = load_vehicles()
        vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
        if not vehicle or vehicle['status'].lower() != 'available':
            return jsonify({'error': 'Vehicle not available'}), 400

        days = (dropoff_date - pickup_date).days + 1
        total_price = vehicle['daily_rate'] * days

        return jsonify({'total_price': round(total_price, 2)})

@app.route('/insurance', methods=['GET'])
def insurance_options():
    insurance_plans = load_insurance()
    return render_template('insurance.html', insurance_plans=insurance_plans, page_title='Select Insurance Coverage')

@app.route('/booking/confirm', methods=['POST'])
def booking_confirm():
    # Implementation unchanged
    pass

@app.route('/rentals/history', methods=['GET'])
def rental_history():
    customer_id = request.args.get('customer_id', type=int)
    status_filter = request.args.get('status', 'All').lower()
    rentals = load_rentals()
    vehicles = load_vehicles()
    vehicle_map = {v['vehicle_id']: v for v in vehicles}
    filtered = []
    for rental in rentals:
        if customer_id and rental['customer_id'] != customer_id:
            continue
        if status_filter != 'all' and rental['status'].lower() != status_filter:
            continue
        rental['vehicle'] = vehicle_map.get(rental['vehicle_id'])
        filtered.append(rental)
    return render_template('rental_history.html', rentals=filtered, page_title='Rental History')

# Other routes unchanged

if __name__ == '__main__':
    app.run(debug=True)
