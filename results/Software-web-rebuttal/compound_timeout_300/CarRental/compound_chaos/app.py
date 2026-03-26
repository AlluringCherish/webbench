from flask import Flask, render_template, request, redirect, url_for, abort
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_PATH = 'data'
VEHICLES_FILE = os.path.join(DATA_PATH, 'vehicles.txt')
CUSTOMERS_FILE = os.path.join(DATA_PATH, 'customers.txt')
LOCATIONS_FILE = os.path.join(DATA_PATH, 'locations.txt')
RENTALS_FILE = os.path.join(DATA_PATH, 'rentals.txt')
INSURANCE_FILE = os.path.join(DATA_PATH, 'insurance.txt')
RESERVATIONS_FILE = os.path.join(DATA_PATH, 'reservations.txt')

# Utility functions for reading and writing pipe-delimited files

def read_vehicles() -> List[Dict[str, Any]]:
    vehicles = []
    try:
        with open(VEHICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue  # invalid line
                vehicle_id, make, model, vehicle_type, daily_rate, seats, transmission, fuel_type, status = parts
                try:
                    v = {
                        'vehicle_id': int(vehicle_id),
                        'make': make,
                        'model': model,
                        'vehicle_type': vehicle_type,
                        'daily_rate': float(daily_rate),
                        'seats': int(seats),
                        'transmission': transmission,
                        'fuel_type': fuel_type,
                        'status': status
                    }
                    vehicles.append(v)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return vehicles


def read_customers() -> List[Dict[str, Any]]:
    customers = []
    try:
        with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                customer_id, name, email, phone, driver_license, license_expiry = parts
                try:
                    c = {
                        'customer_id': int(customer_id),
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'driver_license': driver_license,
                        'license_expiry': license_expiry
                    }
                    customers.append(c)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return customers


def read_locations() -> List[Dict[str, Any]]:
    locations = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
                    continue
                location_id, city, address, phone, hours, available_vehicles = parts
                try:
                    loc = {
                        'location_id': int(location_id),
                        'city': city,
                        'address': address,
                        'phone': phone,
                        'hours': hours,
                        'available_vehicles': int(available_vehicles)
                    }
                    locations.append(loc)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return locations


def read_rentals() -> List[Dict[str, Any]]:
    rentals = []
    try:
        with open(RENTALS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=9:
                    continue
                rental_id, vehicle_id, customer_id, pickup_date, dropoff_date, pickup_location, dropoff_location, total_price, status = parts
                try:
                    r = {
                        'rental_id': int(rental_id),
                        'vehicle_id': int(vehicle_id),
                        'customer_id': int(customer_id),
                        'pickup_date': pickup_date,
                        'dropoff_date': dropoff_date,
                        'pickup_location': pickup_location,
                        'dropoff_location': dropoff_location,
                        'total_price': float(total_price),
                        'status': status
                    }
                    rentals.append(r)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return rentals


def read_insurance_plans() -> List[Dict[str, Any]]:
    plans = []
    try:
        with open(INSURANCE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=6:
                    continue
                insurance_id, plan_name, description, daily_cost, coverage_limit, deductible = parts
                try:
                    coverage_val = None
                    try:
                        coverage_val = int(coverage_limit)
                    except ValueError:
                        if coverage_limit.strip().lower() == 'unlimited':
                            coverage_val = 'Unlimited'
                        else:
                            coverage_val = coverage_limit
                    plan = {
                        'insurance_id': int(insurance_id),
                        'plan_name': plan_name,
                        'description': description,
                        'daily_cost': float(daily_cost),
                        'coverage_limit': coverage_val,
                        'deductible': int(deductible)
                    }
                    plans.append(plan)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return plans


def read_reservations() -> List[Dict[str, Any]]:
    reservations = []
    try:
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts)!=7:
                    continue
                reservation_id, rental_id, vehicle_id, customer_id, status, insurance_id, special_requests = parts
                try:
                    res = {
                        'reservation_id': int(reservation_id),
                        'rental_id': int(rental_id),
                        'vehicle_id': int(vehicle_id),
                        'customer_id': int(customer_id),
                        'status': status,
                        'insurance_id': int(insurance_id),
                        'special_requests': special_requests
                    }
                    reservations.append(res)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return reservations


def write_reservations(reservations: List[Dict[str, Any]]) -> None:
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
                f.write(line)
    except Exception:
        pass


def write_rentals(rentals: List[Dict[str, Any]]) -> None:
    try:
        with open(RENTALS_FILE, 'w', encoding='utf-8') as f:
            for r in rentals:
                line = f"{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['pickup_date']}|{r['dropoff_date']}|{r['pickup_location']}|{r['dropoff_location']}|{r['total_price']}|{r['status']}\n"
                f.write(line)
    except Exception:
        pass


# Helper functions

def get_vehicle_by_id(vehicle_id: int) -> Optional[Dict[str, Any]]:
    vehicles = read_vehicles()
    for v in vehicles:
        if v['vehicle_id'] == vehicle_id:
            return v
    return None


def get_location_names() -> List[str]:
    locations = read_locations()
    return [loc['city'] for loc in locations]


def parse_date(date_str: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None


def daterange(start_date: datetime, end_date: datetime) -> List[datetime]:
    days = []
    for n in range((end_date - start_date).days + 1):
        days.append(start_date + timedelta(n))
    return days


def calculate_price(daily_rate: float, pickup_date: str, dropoff_date: str) -> Optional[float]:
    start = parse_date(pickup_date)
    end = parse_date(dropoff_date)
    if not start or not end or end < start:
        return None
    days = (end - start).days + 1
    return round(daily_rate * days, 2)


def get_insurance_plan_by_id(insurance_id: int) -> Optional[Dict[str, Any]]:
    plans = read_insurance_plans()
    for p in plans:
        if p['insurance_id'] == insurance_id:
            return p
    return None


def get_rental_by_id(rental_id: int) -> Optional[Dict[str, Any]]:
    rentals = read_rentals()
    for r in rentals:
        if r['rental_id'] == rental_id:
            return r
    return None


def get_reservation_by_id(reservation_id: int) -> Optional[Dict[str, Any]]:
    reservations = read_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            return r
    return None


# ------------- ROUTES -------------

# / (root_redirect)
@app.route('/')
def root_redirect():
    # Redirect root to /dashboard
    return redirect(url_for('dashboard'))


# /dashboard (dashboard)
@app.route('/dashboard')
def dashboard():
    # For demonstration, featured vehicles: select available vehicles with lowest vehicle_id, max 4
    vehicles = read_vehicles()
    available_vehicles = [v for v in vehicles if v['status'].lower() == 'available']
    available_vehicles.sort(key=lambda x: x['vehicle_id'])
    featured_vehicles = []
    for v in available_vehicles[:4]:
        featured_vehicles.append({
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'daily_rate': v['daily_rate']
        })

    promotions = [
        '20% off on SUV rentals this weekend',
        'Free GPS with any Luxury vehicle',
        'Weekend special: Rent 3 days, get 1 day free'
    ]
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)


# /search-vehicles (search_vehicles)
@app.route('/search-vehicles')
def search_vehicles():
    locations = sorted({loc['city'] for loc in read_locations()})
    vehicle_types = ['Economy', 'Compact', 'Sedan', 'SUV', 'Luxury']

    selected_location = request.args.get('location', None)
    selected_vehicle_type = request.args.get('vehicle_type', None)
    date_range_start = request.args.get('start_date', None)
    date_range_end = request.args.get('end_date', None)

    rental_date_range = None
    if date_range_start and date_range_end:
        rental_date_range = (date_range_start, date_range_end)

    available_vehicles = []
    vehicles = read_vehicles()

    def vehicle_matches(v):
        if v['status'].lower() != 'available':
            return False
        if selected_location:
            # Check location availability: vehicles.txt does not associate locations directly,
            # so simplifying assumption: any vehicle can be rented in any location
            pass  # No filtering by location at vehicle level
        if selected_vehicle_type and selected_vehicle_type != v['vehicle_type']:
            return False
        return True

    available_vehicles = [v for v in vehicles if vehicle_matches(v)]

    # Further filter available_vehicles by availability on rental_date_range
    # rentals.txt contains active rentals, simple check for overlapping dates with requested date range
    if rental_date_range:
        start = parse_date(rental_date_range[0])
        end = parse_date(rental_date_range[1])
        if not start or not end or end < start:
            available_vehicles = []
        else:
            rentals = read_rentals()
            # Exclude vehicles with overlapping active rentals
            def overlaps(rental, start, end):
                r_start = parse_date(rental['pickup_date'])
                r_end = parse_date(rental['dropoff_date'])
                if not r_start or not r_end:
                    return False
                return not (r_end < start or r_start > end)

            unavailable_vehicle_ids = set()
            for rental in rentals:
                if rental['status'].lower() in ['active', 'confirmed'] and overlaps(rental, start, end):
                    unavailable_vehicle_ids.add(rental['vehicle_id'])

            available_vehicles = [v for v in available_vehicles if v['vehicle_id'] not in unavailable_vehicle_ids]

    # Prepare available_vehicles for template
    prepared_vehicles = []
    for v in available_vehicles:
        prepared_vehicles.append({
            'vehicle_id': v['vehicle_id'],
            'make': v['make'],
            'model': v['model'],
            'daily_rate': v['daily_rate'],
            'vehicle_type': v['vehicle_type']
        })

    return render_template('search_vehicles.html',
                           locations=locations,
                           vehicle_types=vehicle_types,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           rental_date_range=rental_date_range,
                           available_vehicles=prepared_vehicles)


# /vehicle-details/<int:vehicle_id> (vehicle_details)
@app.route('/vehicle-details/<int:vehicle_id>')
def vehicle_details(vehicle_id: int):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        abort(404)

    # vehicle_reviews - Not specified in data files. As no direct storage provided, simulate empty or
    # static example reviews to avoid error in template.
    vehicle_reviews = [
        {'review_id': 1, 'customer_name': 'Alice Johnson', 'rating': 5, 'comment': 'Great car, very comfortable!'},
        {'review_id': 2, 'customer_name': 'Bob Williams', 'rating': 4, 'comment': 'Good value for the price.'}
    ]

    return render_template('vehicle_details.html', vehicle=vehicle, vehicle_reviews=vehicle_reviews)


# /booking/<int:vehicle_id> (GET, POST) (booking)
@app.route('/booking/<int:vehicle_id>', methods=['GET','POST'])
def booking(vehicle_id: int):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle or vehicle['status'].lower() != 'available':
        abort(404)

    locations = read_locations()
    pickup_locations = [loc['city'] for loc in locations]
    dropoff_locations = pickup_locations.copy()  # Simplify same list

    pickup_date = None
    dropoff_date = None
    total_price = None

    if request.method == 'POST':
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')

        # Validate dates and locations
        start_dt = parse_date(pickup_date)
        end_dt = parse_date(dropoff_date)
        if not start_dt or not end_dt or end_dt < start_dt:
            total_price = None
        elif pickup_location not in pickup_locations or dropoff_location not in dropoff_locations:
            total_price = None
        else:
            total_price = calculate_price(vehicle['daily_rate'], pickup_date, dropoff_date)

        # Business rule: After calculating price, expect user to proceed to insurance options.
        # We do not redirect here, just show price. Confirmation/booking happens later.

    return render_template('booking.html',
                           vehicle=vehicle,
                           pickup_locations=pickup_locations,
                           dropoff_locations=dropoff_locations,
                           pickup_date=pickup_date,
                           dropoff_date=dropoff_date,
                           total_price=total_price)


# /insurance-options/<int:reservation_id> (GET, POST) (insurance_options)
@app.route('/insurance-options/<int:reservation_id>', methods=['GET','POST'])
def insurance_options(reservation_id: int):
    insurance_plans = read_insurance_plans()
    selected_insurance_id = None
    selected_insurance_description = None
    selected_insurance_price = None

    if request.method == 'POST':
        insurance_id_str = request.form.get('insurance_id')
        if insurance_id_str and insurance_id_str.isdigit():
            insurance_id = int(insurance_id_str)
            plan = get_insurance_plan_by_id(insurance_id)
            if plan:
                selected_insurance_id = plan['insurance_id']
                selected_insurance_description = plan['description']
                selected_insurance_price = plan['daily_cost']
                # Here business logic to update reservation insurance could be done
                reservations = read_reservations()
                for res in reservations:
                    if res['reservation_id'] == reservation_id:
                        res['insurance_id'] = selected_insurance_id
                        # Keeping special_requests intact
                        break
                write_reservations(reservations)

                # After confirm, could redirect elsewhere but spec not stating explicit confirm steps.
                # So stay on page showing selection.

    else:
        # On GET, load existing insurance for reservation if exists
        reservations = read_reservations()
        for res in reservations:
            if res['reservation_id'] == reservation_id:
                current_id = res.get('insurance_id')
                plan = get_insurance_plan_by_id(current_id) if current_id else None
                if plan:
                    selected_insurance_id = plan['insurance_id']
                    selected_insurance_description = plan['description']
                    selected_insurance_price = plan['daily_cost']
                break

    return render_template('insurance_options.html',
                           insurance_plans=insurance_plans,
                           selected_insurance_id=selected_insurance_id,
                           selected_insurance_description=selected_insurance_description,
                           selected_insurance_price=selected_insurance_price)


# /rental-history (rental_history)
@app.route('/rental-history')
def rental_history():
    rentals = read_rentals()
    status_filter_options = ["All", "Active", "Completed", "Cancelled"]
    selected_status_filter = request.args.get('status_filter', 'All')

    if selected_status_filter != "All":
        filtered_rentals = [r for r in rentals if r['status'].lower() == selected_status_filter.lower()]
    else:
        filtered_rentals = rentals

    # Preparing rentals for template with formatted vehicle info
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}

    prepared_rentals = []
    for r in filtered_rentals:
        vehicle = vehicles.get(r['vehicle_id'])
        vehicle_info = f"{vehicle['make']} {vehicle['model']}" if vehicle else 'Unknown'
        prepared_rentals.append({
            'rental_id': r['rental_id'],
            'vehicle_info': vehicle_info,
            'pickup_date': r['pickup_date'],
            'dropoff_date': r['dropoff_date'],
            'pickup_location': r['pickup_location'],
            'dropoff_location': r['dropoff_location'],
            'total_price': r['total_price'],
            'status': r['status']
        })

    return render_template('rental_history.html',
                           rentals=prepared_rentals,
                           status_filter_options=status_filter_options,
                           selected_status_filter=selected_status_filter)


# /rental-details/<int:rental_id> (rental_details)
@app.route('/rental-details/<int:rental_id>')
def rental_details(rental_id: int):
    rental = get_rental_by_id(rental_id)
    if not rental:
        abort(404)
    return render_template('rental_details.html', rental=rental)


# /my-reservations (my_reservations)
@app.route('/my-reservations')
def my_reservations():
    reservations = read_reservations()
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}

    prepared_reservations = []
    for res in reservations:
        vehicle = vehicles.get(res['vehicle_id'])
        if vehicle:
            vehicle_info = f"{vehicle['make']} {vehicle['model']}"
        else:
            vehicle_info = "Unknown"
        dates = None
        # Find linked rental for dates
        rental = get_rental_by_id(res['rental_id'])
        if rental:
            dates = f"{rental['pickup_date']} - {rental['dropoff_date']}"
        prepared_reservations.append({
            'reservation_id': res['reservation_id'],
            'vehicle_info': vehicle_info,
            'dates': dates or 'N/A',
            'status': res['status']
        })

    return render_template('my_reservations.html', reservations=prepared_reservations)


# /modify-reservation/<int:reservation_id> (GET, POST) (modify_reservation)
@app.route('/modify-reservation/<int:reservation_id>', methods=['GET','POST'])
def modify_reservation(reservation_id: int):
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        abort(404)

    if request.method == 'POST':
        # Example: Allow modifying status or special_requests only
        status = request.form.get('status')
        special_requests = request.form.get('special_requests')

        if status:
            reservation['status'] = status
        if special_requests is not None:
            reservation['special_requests'] = special_requests

        # Update reservations file
        reservations = read_reservations()
        for i, res in enumerate(reservations):
            if res['reservation_id'] == reservation_id:
                reservations[i] = reservation
                break
        write_reservations(reservations)

        return redirect(url_for('my_reservations'))

    return render_template('modify_reservation.html', reservation=reservation)


# /cancel-reservation/<int:reservation_id> (POST) (cancel_reservation)
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id: int):
    reservations = read_reservations()
    found = False
    for res in reservations:
        if res['reservation_id'] == reservation_id:
            res['status'] = 'Cancelled'
            found = True
            break
    if found:
        write_reservations(reservations)
    return redirect(url_for('my_reservations'))


# /special-requests (GET, POST) (special_requests)
@app.route('/special-requests', methods=['GET','POST'])
def special_requests():
    reservations = read_reservations()
    prepared_reservations = []
    # For dropdown, display reservation_id and short description (vehicle info + dates)
    vehicles = {v['vehicle_id']: v for v in read_vehicles()}
    rentals = {r['rental_id']: r for r in read_rentals()}
    for res in reservations:
        vehicle = vehicles.get(res['vehicle_id'])
        rental = rentals.get(res['rental_id'])
        desc = 'Reservation ' + str(res['reservation_id'])
        if vehicle:
            desc += f" - {vehicle['make']} {vehicle['model']}"
        if rental:
            desc += f" ({rental['pickup_date']} to {rental['dropoff_date']})"
        prepared_reservations.append({
            'reservation_id': res['reservation_id'],
            'description': desc
        })

    submission_status = None
    if request.method == 'POST':
        selected_reservation_id_str = request.form.get('reservation_id')
        driver_assistance = request.form.get('driver_assistance')
        gps_option = request.form.get('gps_option')
        child_seat_qty = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes')

        # Validate reservation id
        try:
            selected_reservation_id = int(selected_reservation_id_str)
        except Exception:
            selected_reservation_id = None

        if selected_reservation_id is None:
            submission_status = 'Invalid reservation selected.'
        else:
            # Update special_requests text by appending or modifying
            reservations = read_reservations()
            updated = False
            for i, res in enumerate(reservations):
                if res['reservation_id'] == selected_reservation_id:
                    parts = []
                    if driver_assistance == 'on':
                        parts.append('Driver assistance requested')
                    if gps_option == 'on':
                        parts.append('GPS option selected')
                    if child_seat_qty and child_seat_qty.isdigit() and int(child_seat_qty) > 0:
                        parts.append(f'Child seats: {int(child_seat_qty)}')
                    if special_notes and special_notes.strip():
                        parts.append(f'Notes: {special_notes.strip()}')

                    combined = '; '.join(parts) if parts else 'None'
                    res['special_requests'] = combined
                    reservations[i] = res
                    updated = True
                    break
            if updated:
                write_reservations(reservations)
                submission_status = 'Special requests updated successfully.'
            else:
                submission_status = 'Reservation not found.'

    return render_template('special_requests.html',
                           reservations=prepared_reservations,
                           submission_status=submission_status)


# /locations (locations)
@app.route('/locations')
def locations():
    locations = read_locations()
    hours_filter_options = ["24/7", "Business Hours", "Weekend"]
    selected_hours_filter = request.args.get('hours_filter', None)
    search_query = request.args.get('search_query', None)

    # Filter locations based on hours
    def hours_filter(loc):
        if not selected_hours_filter:
            return True
        hf = selected_hours_filter.strip().lower()
        lh = loc['hours'].strip().lower()
        if hf == '24/7':
            return lh == '24/7'
        elif hf == 'business hours':
            # Accept hours that are not 24/7 and containing time ranges
            return lh != '24/7' and ('09:00' in lh or '18:00' in lh or '-' in lh)
        elif hf == 'weekend':
            # No exact weekend but if string contains 'weekend'
            return 'weekend' in lh
        return True

    filtered_locations = [loc for loc in locations if hours_filter(loc)]

    # Filter locations by search query in city or address
    if search_query and search_query.strip():
        sq = search_query.strip().lower()
        filtered_locations = [loc for loc in filtered_locations if sq in loc['city'].lower() or sq in loc['address'].lower()]

    return render_template('locations.html',
                           locations=filtered_locations,
                           hours_filter_options=hours_filter_options,
                           selected_hours_filter=selected_hours_filter,
                           search_query=search_query)


# /location-details/<int:location_id> (location_details)
@app.route('/location-details/<int:location_id>')
def location_details(location_id: int):
    locations = read_locations()
    location = None
    for loc in locations:
        if loc['location_id'] == location_id:
            location = loc
            break
    if not location:
        abort(404)
    return render_template('location_details.html', location=location)


if __name__ == '__main__':
    app.run(debug=True)
