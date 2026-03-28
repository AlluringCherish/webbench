from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime
from typing import List, Dict, Optional

app = Flask(__name__)

# ----------- Data Loading Helpers -----------

def load_vehicles() -> List[Dict]:
    vehicles = []
    try:
        with open('vehicles.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'vehicle_id', 'make', 'model', 'vehicle_type', 'daily_rate', 'seats', 'transmission', 'fuel_type', 'status'
            ])
            for row in reader:
                try:
                    vehicles.append({
                        'vehicle_id': int(row['vehicle_id']),
                        'make': row['make'],
                        'model': row['model'],
                        'vehicle_type': row['vehicle_type'],
                        'daily_rate': float(row['daily_rate']),
                        'seats': int(row['seats']),
                        'transmission': row['transmission'],
                        'fuel_type': row['fuel_type'],
                        'status': row['status']
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return vehicles

def load_customers() -> List[Dict]:
    customers = []
    try:
        with open('customers.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'customer_id', 'name', 'email', 'phone', 'driver_license', 'license_expiry'
            ])
            for row in reader:
                try:
                    customers.append({
                        'customer_id': int(row['customer_id']),
                        'name': row['name'],
                        'email': row['email'],
                        'phone': row['phone'],
                        'driver_license': row['driver_license'],
                        'license_expiry': row['license_expiry']  # as string YYYY-MM-DD
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return customers

def load_locations() -> List[Dict]:
    locations = []
    try:
        with open('locations.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'location_id', 'city', 'address', 'phone', 'hours', 'available_vehicles'
            ])
            for row in reader:
                try:
                    locations.append({
                        'location_id': int(row['location_id']),
                        'city': row['city'],
                        'address': row['address'],
                        'phone': row['phone'],
                        'hours': row['hours'],
                        'available_vehicles': int(row['available_vehicles'])
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return locations

def load_rentals() -> List[Dict]:
    rentals = []
    try:
        with open('rentals.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'rental_id', 'vehicle_id', 'customer_id', 'pickup_date', 'dropoff_date',
                'pickup_location', 'dropoff_location', 'total_price', 'status'
            ])
            for row in reader:
                try:
                    # validate dates
                    datetime.strptime(row['pickup_date'], '%Y-%m-%d')
                    datetime.strptime(row['dropoff_date'], '%Y-%m-%d')
                    rentals.append({
                        'rental_id': int(row['rental_id']),
                        'vehicle_id': int(row['vehicle_id']),
                        'customer_id': int(row['customer_id']),
                        'pickup_date': row['pickup_date'],
                        'dropoff_date': row['dropoff_date'],
                        'pickup_location': row['pickup_location'],
                        'dropoff_location': row['dropoff_location'],
                        'total_price': float(row['total_price']),
                        'status': row['status']
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return rentals

def load_insurance() -> List[Dict]:
    plans = []
    try:
        with open('insurance.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'insurance_id', 'plan_name', 'description', 'daily_cost', 'coverage_limit', 'deductible'
            ])
            for row in reader:
                try:
                    # coverage_limit may be int or string "Unlimited"
                    coverage_limit = row['coverage_limit']
                    try:
                        coverage_limit_val = float(coverage_limit)
                    except ValueError:
                        coverage_limit_val = coverage_limit  # keep as string
                    plans.append({
                        'insurance_id': int(row['insurance_id']),
                        'plan_name': row['plan_name'],
                        'description': row['description'],
                        'daily_cost': float(row['daily_cost']),
                        'coverage_limit': coverage_limit_val,
                        'deductible': float(row['deductible'])
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return plans

def load_reservations() -> List[Dict]:
    reservations = []
    try:
        with open('reservations.txt', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|', fieldnames=[
                'reservation_id', 'rental_id', 'vehicle_id', 'customer_id',
                'status', 'insurance_id', 'special_requests'
            ])
            for row in reader:
                try:
                    reservations.append({
                        'reservation_id': int(row['reservation_id']),
                        'rental_id': int(row['rental_id']),
                        'vehicle_id': int(row['vehicle_id']),
                        'customer_id': int(row['customer_id']),
                        'status': row['status'],
                        'insurance_id': int(row['insurance_id']) if row['insurance_id'] != '' else None,
                        'special_requests': row['special_requests']
                    })
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return reservations

# ----------- Routes -----------

@app.route('/')
def root_redirect():
    # Redirect root to dashboard
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    featured_vehicles = load_vehicles()[:5]  # Show first 5 vehicles as featured
    promotions = [
        {'title': 'Spring Special', 'description': 'Save 10% on all SUV rentals!'},
        {'title': 'Weekend Deal', 'description': 'Get free GPS on rentals over 3 days!'}
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

@app.route('/search')
def vehicle_search():
    vehicles = load_vehicles()
    locations = load_locations()
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    # Get filters
    filters = {
        'location': request.args.get('location', ''),
        'vehicle_type': request.args.get('vehicle_type', ''),
        'date_range': request.args.get('date_range', '')  # Not used for availability here as no inventory data
    }

    # Filter vehicles by vehicle_type
    if filters['vehicle_type']:
        vehicles = [v for v in vehicles if v['vehicle_type'] == filters['vehicle_type']]

    # Filter vehicles by location availability approximation: vehicle must be "Available" and location exists
    if filters['location']:
        # Find vehicle IDs available in the location per locations.txt availability
        try:
            loc = next(l for l in locations if l['city'].lower() == filters['location'].lower())
        except StopIteration:
            loc = None
        if loc:
            # Only keep vehicles that are Available and assume location availability means status Available
            vehicles = [v for v in vehicles if v['status'] == 'Available']
        else:
            # No location match, no vehicles
            vehicles = []

    return render_template('search.html', vehicles=vehicles, locations=locations, vehicle_types=vehicle_types, filters=filters)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id: int):
    vehicles = load_vehicles()
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404

    # No review data provided, empty list
    reviews = []

    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    pickup_locations = load_locations()
    dropoff_locations = pickup_locations  # Assume same locations for dropoff

    calculated_price: Optional[float] = None

    if request.method == 'POST':
        try:
            vehicle_id = int(request.form.get('vehicle_id'))
            pickup_location = request.form.get('pickup_location')
            dropoff_location = request.form.get('dropoff_location')
            pickup_date_str = request.form.get('pickup_date')
            dropoff_date_str = request.form.get('dropoff_date')

            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d')
            dropoff_date = datetime.strptime(dropoff_date_str, '%Y-%m-%d')

            if dropoff_date < pickup_date:
                return "Dropoff date cannot be before pickup date", 400

            days = (dropoff_date - pickup_date).days + 1

            vehicles = load_vehicles()
            vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
            if not vehicle:
                return "Invalid vehicle selected", 400

            calculated_price = round(days * vehicle['daily_rate'], 2)

        except Exception:
            return "Invalid form data", 400

        return render_template('booking.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations, calculated_price=calculated_price)

    # GET
    return render_template('booking.html', pickup_locations=pickup_locations, dropoff_locations=dropoff_locations, calculated_price=None)

@app.route('/insurance', methods=['GET', 'POST'])
def insurance_options():
    insurance_plans = load_insurance()
    selected_insurance = None

    if request.method == 'POST':
        try:
            insurance_id = int(request.form.get('insurance_id'))
            selected_insurance = next((p for p in insurance_plans if p['insurance_id'] == insurance_id), None)
        except Exception:
            selected_insurance = None

    return render_template('insurance.html', insurance_plans=insurance_plans, selected_insurance=selected_insurance)

@app.route('/rental-history')
def rental_history():
    rentals = load_rentals()
    status_filter = request.args.get('status_filter', 'All')

    if status_filter and status_filter != 'All':
        rentals = [r for r in rentals if r['status'].lower() == status_filter.lower()]

    return render_template('rental_history.html', rentals=rentals, status_filter=status_filter)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations_management():
    reservations = load_reservations()

    if request.method == 'POST':
        # Processing POST actions like cancel, modify can be added here
        # For simplicity, no action implemented
        pass

    return render_template('reservations.html', reservations=reservations)

@app.route('/special-requests', methods=['GET', 'POST'])
def special_requests():
    reservations = load_reservations()
    form_data = None

    if request.method == 'POST':
        try:
            reservation_id = int(request.form.get('reservation_id'))
            driver_assistance = request.form.get('driver_assistance_checkbox') == 'on'
            gps_option = request.form.get('gps_option_checkbox') == 'on'
            child_seat_qty = request.form.get('child_seat_quantity', '0')
            try:
                child_seat_qty = int(child_seat_qty)
            except ValueError:
                child_seat_qty = 0
            special_notes = request.form.get('special_notes', '')

            # Combine special requests into a single string
            requests_list = []
            if driver_assistance:
                requests_list.append('Driver assistance requested')
            if gps_option:
                requests_list.append('GPS requested')
            if child_seat_qty > 0:
                requests_list.append(f'Child seats requested: {child_seat_qty}')
            if special_notes:
                requests_list.append(f'Notes: {special_notes}')

            special_requests_text = '; '.join(requests_list) if requests_list else ''

            # Update reservation's special_requests field
            for res in reservations:
                if res['reservation_id'] == reservation_id:
                    res['special_requests'] = special_requests_text
                    break

            # Save back to reservations.txt
            with open('reservations.txt', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter='|')
                for res in reservations:
                    insurance_id_value = res['insurance_id'] if res['insurance_id'] is not None else ''
                    writer.writerow([
                        res['reservation_id'], res['rental_id'], res['vehicle_id'], res['customer_id'],
                        res['status'], insurance_id_value, res['special_requests']
                    ])

            form_data = {
                'reservation_id': reservation_id,
                'special_requests': special_requests_text
            }

        except Exception:
            form_data = None

    return render_template('special_requests.html', reservations=reservations, form_data=form_data)

@app.route('/locations')
def locations_page():
    locations = load_locations()
    hours_filter = request.args.get('hours_filter', '')
    search_query = request.args.get('search_query', '').strip().lower()

    if hours_filter:
        locations = [l for l in locations if l['hours'] == hours_filter]

    if search_query:
        locations = [l for l in locations if search_query in l['city'].lower() or search_query in l['address'].lower()]

    return render_template('locations.html', locations=locations, hours_filter=hours_filter, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
