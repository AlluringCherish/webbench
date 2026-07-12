from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility functions to load data from files

def load_destinations():
    path = os.path.join(data_dir, 'destinations.txt')
    destinations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                dest_id, name, country, region, description, attractions, climate = parts
                destinations.append({
                    'dest_id': int(dest_id),
                    'name': name,
                    'country': country,
                    'region': region,
                    'description': description,
                    'attractions': attractions,
                    'climate': climate
                })
    except FileNotFoundError:
        pass
    return destinations


def load_itineraries():
    path = os.path.join(data_dir, 'itineraries.txt')
    itineraries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                itinerary_id, itinerary_name, destination, start_date, end_date, activities, status = parts
                itineraries.append({
                    'itinerary_id': int(itinerary_id),
                    'itinerary_name': itinerary_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'activities': activities,
                    'status': status
                })
    except FileNotFoundError:
        pass
    return itineraries


def load_hotels():
    path = os.path.join(data_dir, 'hotels.txt')
    hotels = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                hotel_id, name, city, rating, price_per_night, amenities, category = parts
                hotels.append({
                    'hotel_id': int(hotel_id),
                    'name': name,
                    'city': city,
                    'rating': float(rating),
                    'price_per_night': float(price_per_night),
                    'amenities': amenities,
                    'category': category
                })
    except FileNotFoundError:
        pass
    return hotels


def load_flights():
    path = os.path.join(data_dir, 'flights.txt')
    flights = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 9:
                    continue
                flight_id, airline, departure_city, arrival_city, departure_time, arrival_time, price, class_type, duration = parts
                flights.append({
                    'flight_id': int(flight_id),
                    'airline': airline,
                    'departure_city': departure_city,
                    'arrival_city': arrival_city,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'price': float(price),
                    'class_type': class_type,
                    'duration': duration
                })
    except FileNotFoundError:
        pass
    return flights


def load_packages():
    path = os.path.join(data_dir, 'packages.txt')
    packages = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                package_id, package_name, destination, duration_days, price, included_items, difficulty_level = parts
                packages.append({
                    'package_id': int(package_id),
                    'package_name': package_name,
                    'destination': destination,
                    'duration_days': int(duration_days),
                    'price': float(price)
                })
    except FileNotFoundError:
        pass
    return packages


def load_trips():
    path = os.path.join(data_dir, 'trips.txt')
    trips = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                trip_id, trip_name, destination, start_date, end_date, total_budget, status, created_date = parts
                trips.append({
                    'trip_id': int(trip_id),
                    'trip_name': trip_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'status': status
                })
    except FileNotFoundError:
        pass
    return trips


def load_bookings():
    path = os.path.join(data_dir, 'bookings.txt')
    bookings = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                booking_id, trip_id, booking_type, booking_date, amount, confirmation_number, status = parts
                bookings.append({
                    'booking_id': int(booking_id),
                    'trip_id': int(trip_id),
                    'booking_type': booking_type,
                    'booking_date': booking_date,
                    'amount': float(amount),
                    'confirmation_number': confirmation_number,
                    'status': status
                })
    except FileNotFoundError:
        pass
    return bookings


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    destinations = load_destinations()
    trips = load_trips()
    # featured_destinations: list of dict {dest_id:int, name:str, country:str}
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations
    ]

    # upcoming_trips: list of dict {trip_id:int, trip_name:str, start_date:str, end_date:str}
    # Consider trips with start_date in future - no date parsing requested, so just return all trips
    upcoming_trips = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'start_date': t['start_date'],
            'end_date': t['end_date']
        } for t in trips
    ]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations_data = load_destinations()
    selected_region = ''
    search_query = ''

    if request.method == 'POST':
        selected_region = request.form.get('region-filter', '')
        search_query = request.form.get('search-destination', '')

    filtered_destinations = destinations_data

    if selected_region:
        filtered_destinations = [d for d in filtered_destinations if d['region'] == selected_region]

    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query.lower() in d['name'].lower()]

    destinations_context = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']}
        for d in filtered_destinations
    ]

    return render_template('destinations.html', destinations=destinations_context, selected_region=selected_region, search_query=search_query)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_data = load_destinations()
    destination = None
    add_success = False

    for d in destinations_data:
        if d['dest_id'] == dest_id:
            destination = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions']
            }
            break

    if destination is None:
        # Could return 404 or redirect, but specification does not specify
        # Here just render template with empty dict
        destination = {'dest_id': dest_id, 'name': '', 'country': '', 'description': '', 'attractions': ''}

    if request.method == 'POST':
        # Simulate adding destination to trip
        add_success = True

    return render_template('destination_details.html', destination=destination, add_success=add_success)


@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()

    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = load_hotels()
    filters = {
        'destination': '',
        'check_in': '',
        'check_out': '',
        'price_filter': ''
    }
    if request.method == 'POST':
        filters['destination'] = request.form.get('destination-input', '')
        filters['check_in'] = request.form.get('check-in-date', '')
        filters['check_out'] = request.form.get('check-out-date', '')
        filters['price_filter'] = request.form.get('price-filter', '')

    return render_template('accommodations.html', hotels=hotels, filters=filters)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = load_flights()
    selected_filters = {
        'departure_city': '',
        'arrival_city': '',
        'dep_date': '',
        'flight_class': ''
    }
    if request.method == 'POST':
        selected_filters['departure_city'] = request.form.get('departure-city', '')
        selected_filters['arrival_city'] = request.form.get('arrival-city', '')
        selected_filters['dep_date'] = request.form.get('departure-date', '')
        selected_filters['flight_class'] = request.form.get('flight-class-filter', '')

    return render_template('transportation.html', flights=flights, selected_filters=selected_filters)


@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages = load_packages()
    package_filter = ''
    if request.method == 'POST':
        package_filter = request.form.get('duration-filter', '')

    filtered_packages = packages
    if package_filter:
        if package_filter == '3-5 days':
            filtered_packages = [p for p in packages if 3 <= p['duration_days'] <= 5]
        elif package_filter == '7-10 days':
            filtered_packages = [p for p in packages if 7 <= p['duration_days'] <= 10]
        elif package_filter == '14+ days':
            filtered_packages = [p for p in packages if p['duration_days'] >= 14]

    return render_template('packages.html', packages=filtered_packages, package_filter=package_filter)


@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_data = load_trips()

    return render_template('trips.html', trips=trips_data)


@app.route('/booking_confirmation')
def booking_confirmation():
    bookings = load_bookings()
    booking = None
    # Show the most recent booking as an example
    if bookings:
        b = bookings[-1]
        booking = {
            'confirmation_number': b['confirmation_number'],
            'booking_details': f"Type: {b['booking_type']}, Date: {b['booking_date']}, Amount: ${b['amount']:.2f}, Status: {b['status']}"
        }
    else:
        booking = {'confirmation_number': '', 'booking_details': ''}

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def travel_recommendations():
    destinations = load_destinations()
    trending_destinations = []
    # We map popularity from climate attribute? Spec does not provide how to get popularity
    # So we make dummy popularity as length of attractions or similar
    for d in destinations:
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'popularity': len(d['attractions'])  # dummy measure
        })
    selected_season = request.args.get('season', '')
    selected_budget = request.args.get('budget', '')

    return render_template('recommendations.html', trending_destinations=trending_destinations, selected_season=selected_season, selected_budget=selected_budget)


if __name__ == '__main__':
    app.run(debug=True)
