from flask import Flask, render_template, request, redirect, url_for
from typing import List, Optional, Dict
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Data Classes
class Vehicle:
    def __init__(self, vehicle_id:int, make:str, model:str, vehicle_type:str, daily_rate:float, seats:int, transmission:str, fuel_type:str, status:str):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.vehicle_type = vehicle_type
        self.daily_rate = daily_rate
        self.seats = seats
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.status = status

class Promotion:
    # Promotion structure not defined in design_spec, so minimal placeholder
    def __init__(self, title:str, description:str):
        self.title = title
        self.description = description

class Review:
    # Review structure not defined in design_spec; placeholder with example fields
    def __init__(self, review_id:int, vehicle_id:int, reviewer:str, rating:int, comment:str):
        self.review_id = review_id
        self.vehicle_id = vehicle_id
        self.reviewer = reviewer
        self.rating = rating
        self.comment = comment

class Insurance:
    def __init__(self, insurance_id:int, plan_name:str, description:str, daily_cost:float, coverage_limit:str, deductible:int):
        self.insurance_id = insurance_id
        self.plan_name = plan_name
        self.description = description
        self.daily_cost = daily_cost
        self.coverage_limit = coverage_limit
        self.deductible = deductible

class Rental:
    def __init__(self, rental_id:int, vehicle_id:int, customer_id:int, pickup_date:str, dropoff_date:str, pickup_location:str, dropoff_location:str, total_price:float, status:str):
        self.rental_id = rental_id
        self.vehicle_id = vehicle_id
        self.customer_id = customer_id
        self.pickup_date = pickup_date
        self.dropoff_date = dropoff_date
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.total_price = total_price
        self.status = status

class Reservation:
    def __init__(self, reservation_id:int, rental_id:int, vehicle_id:int, customer_id:int, status:str, insurance_id:int, special_requests:str):
        self.reservation_id = reservation_id
        self.rental_id = rental_id
        self.vehicle_id = vehicle_id
        self.customer_id = customer_id
        self.status = status
        self.insurance_id = insurance_id
        self.special_requests = special_requests

class Location:
    def __init__(self, location_id:int, city:str, address:str, phone:str, hours:str, available_vehicles:int):
        self.location_id = location_id
        self.city = city
        self.address = address
        self.phone = phone
        self.hours = hours
        self.available_vehicles = available_vehicles

class Customer:
    def __init__(self, customer_id:int, name:str, email:str, phone:str, driver_license:str, license_expiry:str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.driver_license = driver_license
        self.license_expiry = license_expiry

# Utility functions to read/write data files

def read_vehicles() -> List[Vehicle]:
    vehicles = []
    path = os.path.join(DATA_DIR, 'vehicles.txt')
    if not os.path.isfile(path):
        return vehicles
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                vehicle = Vehicle(
                    vehicle_id=int(parts[0]),
                    make=parts[1],
                    model=parts[2],
                    vehicle_type=parts[3],
                    daily_rate=float(parts[4]),
                    seats=int(parts[5]),
                    transmission=parts[6],
                    fuel_type=parts[7],
                    status=parts[8]
                )
                vehicles.append(vehicle)
    except Exception:
        pass
    return vehicles


def read_promotions() -> List[Promotion]:
    # Not defined in design_spec about storage, so returning empty
    return []


def read_reviews(vehicle_id:int) -> List[Review]:
    # Reviews data not specified in design_spec, returning empty
    return []


def read_insurance_plans() -> List[Insurance]:
    plans = []
    path = os.path.join(DATA_DIR, 'insurance.txt')
    if not os.path.isfile(path):
        return plans
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                plan = Insurance(
                    insurance_id=int(parts[0]),
                    plan_name=parts[1],
                    description=parts[2],
                    daily_cost=float(parts[3]),
                    coverage_limit=parts[4],
                    deductible=int(parts[5])
                )
                plans.append(plan)
    except Exception:
        pass
    return plans


def read_rentals() -> List[Rental]:
    rentals = []
    path = os.path.join(DATA_DIR, 'rentals.txt')
    if not os.path.isfile(path):
        return rentals
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                rental = Rental(
                    rental_id=int(parts[0]),
                    vehicle_id=int(parts[1]),
                    customer_id=int(parts[2]),
                    pickup_date=parts[3],
                    dropoff_date=parts[4],
                    pickup_location=parts[5],
                    dropoff_location=parts[6],
                    total_price=float(parts[7]),
                    status=parts[8]
                )
                rentals.append(rental)
    except Exception:
        pass
    return rentals


def read_reservations() -> List[Reservation]:
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.isfile(path):
        return reservations
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                res = Reservation(
                    reservation_id=int(parts[0]),
                    rental_id=int(parts[1]),
                    vehicle_id=int(parts[2]),
                    customer_id=int(parts[3]),
                    status=parts[4],
                    insurance_id=int(parts[5]),
                    special_requests=parts[6]
                )
                reservations.append(res)
    except Exception:
        pass
    return reservations


def read_locations() -> List[Location]:
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.isfile(path):
        return locations
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                loc = Location(
                    location_id=int(parts[0]),
                    city=parts[1],
                    address=parts[2],
                    phone=parts[3],
                    hours=parts[4],
                    available_vehicles=int(parts[5])
                )
                locations.append(loc)
    except Exception:
        pass
    return locations


def read_customers() -> List[Customer]:
    customers = []
    path = os.path.join(DATA_DIR, 'customers.txt')
    if not os.path.isfile(path):
        return customers
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                cust = Customer(
                    customer_id=int(parts[0]),
                    name=parts[1],
                    email=parts[2],
                    phone=parts[3],
                    driver_license=parts[4],
                    license_expiry=parts[5]
                )
                customers.append(cust)
    except Exception:
        pass
    return customers


def write_reservations(reservations:List[Reservation]):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    lines = []
    for r in reservations:
        line = f'{r.reservation_id}|{r.rental_id}|{r.vehicle_id}|{r.customer_id}|{r.status}|{r.insurance_id}|{r.special_requests}'
        lines.append(line)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
    except Exception:
        pass


def write_rentals(rentals:List[Rental]):
    path = os.path.join(DATA_DIR, 'rentals.txt')
    lines = []
    for r in rentals:
        line = f'{r.rental_id}|{r.vehicle_id}|{r.customer_id}|{r.pickup_date}|{r.dropoff_date}|{r.pickup_location}|{r.dropoff_location}|{r.total_price}|{r.status}'
        lines.append(line)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
    except Exception:
        pass

# Assumption: Use a fixed customer ID for simplicity since no auth specified
DEFAULT_CUSTOMER_ID = 1

# Root redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    featured_vehicles = read_vehicles()  # No specification which are featured, so all
    promotions = read_promotions()
    return render_template('dashboard.html', featured_vehicles=featured_vehicles, promotions=promotions)

@app.route('/search', methods=['GET', 'POST'])
def vehicle_search():
    vehicles = read_vehicles()
    location_filter_options = list(set([loc.city for loc in read_locations()]))
    vehicle_type_filter_options = list(set([v.vehicle_type for v in vehicles]))
    selected_location = None
    selected_vehicle_type = None
    selected_date_range = None

    filtered_vehicles = vehicles

    if request.method == 'POST':
        selected_location = request.form.get('location_filter')
        selected_vehicle_type = request.form.get('vehicle_type_filter')
        selected_date_range = request.form.get('date_range_input')

        if selected_location:
            filtered_vehicles = [v for v in filtered_vehicles if v.status == 'Available' and selected_location in [loc.city for loc in read_locations() if loc.city == selected_location]]
            filtered_vehicles = [v for v in filtered_vehicles if selected_location in [loc.city for loc in read_locations()]]
        if selected_vehicle_type:
            filtered_vehicles = [v for v in filtered_vehicles if v.vehicle_type == selected_vehicle_type and v.status == 'Available']
        # No rental availability checking by date as no rental periods given

    return render_template('search.html', vehicles=filtered_vehicles,
                           location_filter_options=location_filter_options,
                           vehicle_type_filter_options=vehicle_type_filter_options,
                           selected_location=selected_location,
                           selected_vehicle_type=selected_vehicle_type,
                           selected_date_range=selected_date_range)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_details(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v.vehicle_id == vehicle_id), None)
    if not vehicle:
        return "Vehicle not found", 404
    reviews = read_reviews(vehicle_id)
    return render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)

@app.route('/booking/<int:vehicle_id>', methods=['GET', 'POST'])
def booking(vehicle_id):
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v.vehicle_id == vehicle_id and v.status == 'Available'), None)
    if not vehicle:
        return "Vehicle not found or unavailable", 404

    pickup_location_options = [loc.city for loc in read_locations()]
    dropoff_location_options = pickup_location_options.copy()

    pickup_date = None
    dropoff_date = None
    total_price = None

    if request.method == 'POST':
        pickup_location = request.form.get('pickup_location')
        dropoff_location = request.form.get('dropoff_location')
        pickup_date = request.form.get('pickup_date')
        dropoff_date = request.form.get('dropoff_date')
        # Basic validation
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            error_msg = 'All booking fields are required.'
            return render_template('booking.html', vehicle=vehicle, pickup_location_options=pickup_location_options, dropoff_location_options=dropoff_location_options,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, reservation_id=None, error=error_msg)

        # Calculate rental days
        from datetime import datetime
        try:
            d_pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
            d_dropoff = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if d_dropoff < d_pickup:
                error_msg = 'Dropoff date must be after pickup date.'
                return render_template('booking.html', vehicle=vehicle, pickup_location_options=pickup_location_options, dropoff_location_options=dropoff_location_options,
                                       pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, reservation_id=None, error=error_msg)

            num_days = (d_dropoff - d_pickup).days + 1
            total_price = round(vehicle.daily_rate * num_days, 2)
        except Exception:
            error_msg = 'Invalid date format.'
            return render_template('booking.html', vehicle=vehicle, pickup_location_options=pickup_location_options, dropoff_location_options=dropoff_location_options,
                                   pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=None, reservation_id=None, error=error_msg)

        # Create new rental record
        rentals = read_rentals()
        new_rental_id = max([r.rental_id for r in rentals], default=0) + 1
        new_rental = Rental(
            rental_id=new_rental_id,
            vehicle_id=vehicle.vehicle_id,
            customer_id=DEFAULT_CUSTOMER_ID,
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            total_price=total_price,
            status='Active'
        )
        rentals.append(new_rental)
        write_rentals(rentals)

        # Create a reservation linked to rental
        reservations = read_reservations()
        new_reservation_id = max([r.reservation_id for r in reservations], default=0) + 1
        new_reservation = Reservation(
            reservation_id=new_reservation_id,
            rental_id=new_rental_id,
            vehicle_id=vehicle.vehicle_id,
            customer_id=DEFAULT_CUSTOMER_ID,
            status='Confirmed',
            insurance_id=0,  # No insurance selected yet
            special_requests=""
        )
        reservations.append(new_reservation)
        write_reservations(reservations)

        return redirect(url_for('insurance_options', reservation_id=new_reservation_id))

    return render_template('booking.html', vehicle=vehicle, pickup_location_options=pickup_location_options, dropoff_location_options=dropoff_location_options,
                           pickup_date=pickup_date, dropoff_date=dropoff_date, total_price=total_price, reservation_id=None)

@app.route('/insurance/<int:reservation_id>', methods=['GET', 'POST'])
def insurance_options(reservation_id):
    insurance_plans = read_insurance_plans()
    selected_plan = None
    reservations = read_reservations()
    reservation = next((r for r in reservations if r.reservation_id == reservation_id), None)
    if not reservation:
        return "Reservation not found", 404

    if request.method == 'POST':
        selected_id_str = request.form.get('insurance_plan')
        if selected_id_str:
            try:
                selected_id = int(selected_id_str)
                plan = next((p for p in insurance_plans if p.insurance_id == selected_id), None)
                if plan:
                    selected_plan = plan
                    # Update reservation with insurance
                    reservation.insurance_id = plan.insurance_id
                    # Update reservation status to Active when insurance confirmed
                    reservation.status = 'Active'
                    # Save reservations
                    write_reservations(reservations)
                    return redirect(url_for('reservations'))
            except ValueError:
                pass

    # GET Method or if no valid POST selection
    selected_plan = next((p for p in insurance_plans if p.insurance_id == reservation.insurance_id), None)
    return render_template('insurance.html', insurance_plans=insurance_plans, selected_plan=selected_plan, reservation_id=reservation_id)

@app.route('/history')
def rental_history():
    rentals = read_rentals()
    status_filter_options = ["All", "Active", "Completed", "Cancelled"]
    selected_status = request.args.get('status', 'All')
    filtered_rentals = rentals
    if selected_status != "All":
        filtered_rentals = [r for r in rentals if r.status == selected_status]
    return render_template('history.html', rentals=filtered_rentals, status_filter_options=status_filter_options, selected_status=selected_status)

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    reservations_list = read_reservations()
    if request.method == 'POST':
        # No specific POST functionality described in design_spec for this route
        pass
    return render_template('reservations.html', reservations=reservations_list)

@app.route('/reservations/modify/<int:reservation_id>', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    reservations_list = read_reservations()
    reservation = next((r for r in reservations_list if r.reservation_id == reservation_id), None)
    if not reservation:
        return "Reservation not found", 404

    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v.vehicle_id == reservation.vehicle_id), None)

    if request.method == 'POST':
        new_status = request.form.get('status')
        # Validate status
        if new_status and new_status in ['Confirmed', 'Active', 'Cancelled']:
            reservation.status = new_status
            write_reservations(reservations_list)
            return redirect(url_for('reservations'))

    return render_template('modify_reservation.html', reservation=reservation, vehicle=vehicle)

@app.route('/reservations/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations_list = read_reservations()
    reservation = next((r for r in reservations_list if r.reservation_id == reservation_id), None)
    if reservation:
        reservation.status = 'Cancelled'
        write_reservations(reservations_list)
    return redirect(url_for('reservations'))

@app.route('/special_requests', methods=['GET', 'POST'])
def special_requests():
    reservations_for_selection = read_reservations()
    special_request_form = {}

    if request.method == 'POST':
        reservation_id_str = request.form.get('reservation_id')
        if not reservation_id_str:
            error_msg = 'Please select a reservation.'
            return render_template('special_requests.html', reservations_for_selection=reservations_for_selection, special_request_form=special_request_form, error=error_msg)

        try:
            reservation_id = int(reservation_id_str)
        except ValueError:
            error_msg = 'Invalid reservation selected.'
            return render_template('special_requests.html', reservations_for_selection=reservations_for_selection, special_request_form=special_request_form, error=error_msg)

        reservation = next((r for r in reservations_for_selection if r.reservation_id == reservation_id), None)
        if not reservation:
            error_msg = 'Reservation not found.'
            return render_template('special_requests.html', reservations_for_selection=reservations_for_selection, special_request_form=special_request_form, error=error_msg)

        driver_assistance = request.form.get('driver_assistance_checkbox')
        gps_option = request.form.get('gps_option_checkbox')
        child_seat_qty = request.form.get('child_seat_quantity')
        special_notes = request.form.get('special_notes')

        # Build special requests string
        reqs = []
        if driver_assistance == 'on':
            reqs.append('Driver assistance requested')
        if gps_option == 'on':
            reqs.append('GPS option requested')
        if child_seat_qty and child_seat_qty.isdigit() and int(child_seat_qty) > 0:
            reqs.append(f'Child seat quantity: {child_seat_qty}')
        if special_notes:
            reqs.append(f'Notes: {special_notes}')

        reservation.special_requests = '; '.join(reqs)

        # Save updated reservations
        write_reservations(reservations_for_selection)

        message = 'Special requests updated successfully.'
        return render_template('special_requests.html', reservations_for_selection=reservations_for_selection, special_request_form={}, message=message)

    return render_template('special_requests.html', reservations_for_selection=reservations_for_selection, special_request_form=special_request_form)

@app.route('/locations')
def locations():
    locations_list = read_locations()
    hours_filter_options = ["24/7", "Business Hours", "Weekend"]
    selected_hours_filter = request.args.get('hours_filter', None)
    search_location_query = request.args.get('search_location_query', None)

    filtered_locations = locations_list
    if selected_hours_filter:
        if selected_hours_filter == '24/7':
            filtered_locations = [loc for loc in filtered_locations if loc.hours == '24/7']
        elif selected_hours_filter == 'Business Hours':
            # Assuming Business Hours means 09:00-18:00 as example
            filtered_locations = [loc for loc in filtered_locations if loc.hours == '09:00-18:00']
        elif selected_hours_filter == 'Weekend':
            # No explicit weekend hours defined, so filter not applied
            filtered_locations = [loc for loc in filtered_locations if loc.hours.lower().find('weekend') != -1]

    if search_location_query:
        lower_q = search_location_query.lower()
        filtered_locations = [loc for loc in filtered_locations if lower_q in loc.city.lower() or lower_q in loc.address.lower()]

    return render_template('locations.html', locations=filtered_locations, hours_filter_options=hours_filter_options, selected_hours_filter=selected_hours_filter, search_location_query=search_location_query)

if __name__ == '__main__':
    app.run(debug=True)
