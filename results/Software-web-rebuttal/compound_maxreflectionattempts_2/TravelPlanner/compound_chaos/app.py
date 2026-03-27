from flask import Flask, render_template, redirect, url_for, request, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

def load_destinations():
    filepath = os.path.join('data', 'destinations.txt')
    destinations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                dest = {
                    'dest_id': int(fields[0]),
                    'name': fields[1],
                    'country': fields[2],
                    'region': fields[3],
                    'description': fields[4],
                    'attractions': fields[5],
                    'climate': fields[6]
                }
                destinations.append(dest)
    except FileNotFoundError:
        destinations = []
    return destinations

def load_itineraries():
    filepath = os.path.join('data', 'itineraries.txt')
    itineraries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                item = {
                    'itinerary_id': int(fields[0]),
                    'itinerary_name': fields[1],
                    'destination': fields[2],
                    'start_date': fields[3],
                    'end_date': fields[4],
                    'activities': fields[5],
                    'status': fields[6]
                }
                itineraries.append(item)
    except FileNotFoundError:
        itineraries = []
    return itineraries

def load_hotels():
    filepath = os.path.join('data', 'hotels.txt')
    hotels = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                try:
                    hotel = {
                        'hotel_id': int(fields[0]),
                        'name': fields[1],
                        'city': fields[2],
                        'rating': float(fields[3]),
                        'price_per_night': float(fields[4]),
                        'amenities': fields[5],
                        'category': fields[6]
                    }
                    hotels.append(hotel)
                except ValueError:
                    continue
    except FileNotFoundError:
        hotels = []
    return hotels

def load_flights():
    filepath = os.path.join('data', 'flights.txt')
    flights = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 9:
                    continue
                try:
                    flight = {
                        'flight_id': int(fields[0]),
                        'airline': fields[1],
                        'departure_city': fields[2],
                        'arrival_city': fields[3],
                        'departure_time': fields[4],
                        'arrival_time': fields[5],
                        'price': float(fields[6]),
                        'class_type': fields[7],
                        'duration': fields[8]
                    }
                    flights.append(flight)
                except ValueError:
                    continue
    except FileNotFoundError:
        flights = []
    return flights

def load_packages():
    filepath = os.path.join('data', 'packages.txt')
    packages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                try:
                    pkg = {
                        'package_id': int(fields[0]),
                        'package_name': fields[1],
                        'destination': fields[2],
                        'duration_days': int(fields[3]),
                        'price': float(fields[4]),
                        'included_items': fields[5],
                        'difficulty_level': fields[6]
                    }
                    packages.append(pkg)
                except ValueError:
                    continue
    except FileNotFoundError:
        packages = []
    return packages

def load_trips():
    filepath = os.path.join('data', 'trips.txt')
    trips = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 8:
                    continue
                try:
                    trip = {
                        'trip_id': int(fields[0]),
                        'trip_name': fields[1],
                        'destination': fields[2],
                        'start_date': fields[3],
                        'end_date': fields[4],
                        'total_budget': float(fields[5]),
                        'status': fields[6],
                        'created_date': fields[7]
                    }
                    trips.append(trip)
                except ValueError:
                    continue
    except FileNotFoundError:
        trips = []
    return trips

def load_bookings():
    filepath = os.path.join('data', 'bookings.txt')
    bookings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 7:
                    continue
                try:
                    booking = {
                        'booking_id': int(fields[0]),
                        'trip_id': int(fields[1]),
                        'booking_type': fields[2],
                        'booking_date': fields[3],
                        'amount': float(fields[4]),
                        'confirmation_number': fields[5],
                        'status': fields[6]
                    }
                    bookings.append(booking)
                except ValueError:
                    continue
    except FileNotFoundError:
        bookings = []
    return bookings


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    destinations = load_destinations()
    # featured destinations: select first 3 for example
    featured_destinations = []
    for dest in destinations[:3]:
        featured_destinations.append({
            'dest_id': dest['dest_id'],
            'name': dest['name'],
            'country': dest['country']
        })

    trips = load_trips()
    # upcoming trips: trips with start_date >= today and sort ascending
    # But since no current date given, return first 3 trips as upcoming
    # with required keys
    upcoming_trips = []
    for trip in trips[:3]:
        upcoming_trips.append({
            'trip_id': trip['trip_id'],
            'trip_name': trip['trip_name'],
            'start_date': trip['start_date']
        })
    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = load_destinations()
    regions = ["Asia", "Europe", "Americas", "Africa", "Oceania"]
    search_query = ''
    selected_region = None

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_region = request.form.get('selected_region', None)
    else:
        search_query = request.args.get('search_query', '').strip()
        selected_region = request.args.get('selected_region', None)

    # Filter destinations by search_query and selected_region
    filtered_destinations = []
    for dest in destinations:
        matches_search = True
        matches_region = True
        if search_query:
            lower_search = search_query.lower()
            if lower_search not in dest['name'].lower() and lower_search not in dest['country'].lower():
                matches_search = False
        if selected_region and selected_region in regions:
            if dest['region'] != selected_region:
                matches_region = False
        if matches_search and matches_region:
            filtered_destinations.append(dest)

    return render_template('destinations.html', destinations=filtered_destinations, search_query=search_query, selected_region=selected_region, regions=regions)

@app.route('/destinations/<int:dest_id>', methods=['GET'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = None
    for dest in destinations:
        if dest['dest_id'] == dest_id:
            destination = dest
            break
    if destination is None:
        abort(404)
    return render_template('destination_details.html', destination=destination)

@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()
    selected_destination = None

    if request.method == 'POST':
        # Possible processing of form data could be implemented here
        # But no form POST details provided, so ignore and just reload data
        pass

    # Selected destination can come from query parameter
    selected_destination = request.args.get('selected_destination', None)

    return render_template('itinerary.html', itineraries=itineraries, selected_destination=selected_destination)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = load_hotels()
    price_ranges = ["Budget", "Mid-range", "Luxury"]
    destination_input = ''
    check_in_date = None
    check_out_date = None
    price_filter = None

    if request.method == 'POST':
        destination_input = request.form.get('destination_input', '').strip()
        check_in_date = request.form.get('check_in_date')
        check_out_date = request.form.get('check_out_date')
        price_filter = request.form.get('price_filter', None)
    else:
        destination_input = request.args.get('destination_input', '').strip()
        check_in_date = request.args.get('check_in_date')
        check_out_date = request.args.get('check_out_date')
        price_filter = request.args.get('price_filter', None)

    filtered_hotels = []
    for hotel in hotels:
        matches_destination = True
        matches_price = True

        if destination_input:
            if destination_input.lower() not in hotel['city'].lower():
                matches_destination = False
        if price_filter:
            if price_filter not in price_ranges:
                matches_price = True
            else:
                # Apply filter by category == price_filter
                if hotel['category'] != price_filter:
                    matches_price = False

        if matches_destination and matches_price:
            filtered_hotels.append(hotel)

    return render_template('accommodations.html', hotels=filtered_hotels, destination_input=destination_input, check_in_date=check_in_date, check_out_date=check_out_date, price_filter=price_filter, price_ranges=price_ranges)

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = load_flights()
    class_options = ["Economy", "Business", "First Class"]
    departure_city = ''
    arrival_city = ''
    departure_date = None
    flight_class_filter = None

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').strip()
        arrival_city = request.form.get('arrival_city', '').strip()
        departure_date = request.form.get('departure_date')
        flight_class_filter = request.form.get('flight_class_filter', None)
    else:
        departure_city = request.args.get('departure_city', '').strip()
        arrival_city = request.args.get('arrival_city', '').strip()
        departure_date = request.args.get('departure_date')
        flight_class_filter = request.args.get('flight_class_filter', None)

    filtered_flights = []
    for flight in flights:
        matches_departure = True
        matches_arrival = True
        matches_class = True
        if departure_city:
            if departure_city.lower() not in flight['departure_city'].lower():
                matches_departure = False
        if arrival_city:
            if arrival_city.lower() not in flight['arrival_city'].lower():
                matches_arrival = False
        if flight_class_filter and flight_class_filter in class_options:
            if flight['class_type'] != flight_class_filter:
                matches_class = False
        if matches_departure and matches_arrival and matches_class:
            filtered_flights.append(flight)

    return render_template('transportation.html', flights=filtered_flights, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date, flight_class_filter=flight_class_filter, class_options=class_options)

@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages_list = load_packages()
    duration_options = ["3-5 days", "7-10 days", "14+ days"]
    duration_filter = None

    if request.method == 'POST':
        duration_filter = request.form.get('duration_filter', None)
    else:
        duration_filter = request.args.get('duration_filter', None)

    filtered_packages = []
    for pkg in packages_list:
        matches_duration = True
        if duration_filter in duration_options:
            # Map string to duration ranges
            if duration_filter == '3-5 days':
                if not (3 <= pkg['duration_days'] <= 5):
                    matches_duration = False
            elif duration_filter == '7-10 days':
                if not (7 <= pkg['duration_days'] <= 10):
                    matches_duration = False
            elif duration_filter == '14+ days':
                if not (pkg['duration_days'] >= 14):
                    matches_duration = False
        if matches_duration:
            filtered_packages.append(pkg)

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter, duration_options=duration_options)

@app.route('/trips', methods=['GET', 'POST'])
def manage_trips():
    trips = load_trips()
    if request.method == 'POST':
        # Possibly handle deletion or edits, but not specified so ignore
        pass
    # Simplify: just return trips
    # We deliver trips with keys: trip_id, trip_name, destination, start_date, end_date, status
    trips_list = []
    for trip in trips:
        trips_list.append({
            'trip_id': trip['trip_id'],
            'trip_name': trip['trip_name'],
            'destination': trip['destination'],
            'start_date': trip['start_date'],
            'end_date': trip['end_date'],
            'status': trip['status']
        })
    return render_template('trips.html', trips=trips_list)

@app.route('/confirmation', methods=['GET'])
def booking_confirmation():
    bookings = load_bookings()
    confirmation_number = ''
    booking_details = {}

    # Let's assume a query param ?confirmation_number=... is provided to identify booking
    confirmation_number_param = request.args.get('confirmation_number', '')
    if confirmation_number_param:
        for booking in bookings:
            if booking['confirmation_number'] == confirmation_number_param:
                confirmation_number = booking['confirmation_number']
                booking_details = {
                    'booking_id': booking['booking_id'],
                    'trip_id': booking['trip_id'],
                    'booking_type': booking['booking_type'],
                    'booking_date': booking['booking_date'],
                    'amount': booking['amount'],
                    'status': booking['status']
                }
                break

    return render_template('confirmation.html', confirmation_number=confirmation_number, booking_details=booking_details)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    destinations = load_destinations()
    season_options = ["Spring", "Summer", "Fall", "Winter"]
    budget_options = ["Low", "Medium", "High"]
    season_filter = None
    budget_filter = None

    trending_destinations = destinations[:3] if destinations else []

    if request.method == 'POST':
        season_filter = request.form.get('season_filter', None)
        budget_filter = request.form.get('budget_filter', None)
    else:
        season_filter = request.args.get('season_filter', None)
        budget_filter = request.args.get('budget_filter', None)

    # No specification on filtering logic, so return trending as is

    return render_template('recommendations.html', trending_destinations=trending_destinations, season_filter=season_filter, budget_filter=budget_filter, season_options=season_options, budget_options=budget_options)

if __name__ == '__main__':
    app.run(debug=True)
