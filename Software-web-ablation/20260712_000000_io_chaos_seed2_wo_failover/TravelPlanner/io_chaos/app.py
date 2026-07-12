from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions to load data from data files as per schema specifications
import os

def load_destinations():
    filepath = 'data/destinations.txt'
    destinations = []
    if not os.path.isfile(filepath):
        return destinations
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                dest = {
                    'dest_id': int(parts[0]),
                    'name': parts[1],
                    'country': parts[2],
                    'region': parts[3],
                    'description': parts[4],
                    'attractions': parts[5],
                    'climate': parts[6]
                }
                destinations.append(dest)
    except Exception:
        pass
    return destinations

def load_itineraries():
    filepath = 'data/itineraries.txt'
    itineraries = []
    if not os.path.isfile(filepath):
        return itineraries
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                itinerary = {
                    'itinerary_id': int(parts[0]),
                    'itinerary_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'activities': parts[5],
                    'status': parts[6]
                }
                itineraries.append(itinerary)
    except Exception:
        pass
    return itineraries

def load_hotels():
    filepath = 'data/hotels.txt'
    hotels = []
    if not os.path.isfile(filepath):
        return hotels
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                hotel = {
                    'hotel_id': int(parts[0]),
                    'name': parts[1],
                    'city': parts[2],
                    'rating': float(parts[3]),
                    'price_per_night': float(parts[4]),
                    'amenities': parts[5],
                    'category': parts[6]
                }
                hotels.append(hotel)
    except Exception:
        pass
    return hotels

def load_flights():
    filepath = 'data/flights.txt'
    flights = []
    if not os.path.isfile(filepath):
        return flights
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 9:
                    continue
                flight = {
                    'flight_id': int(parts[0]),
                    'airline': parts[1],
                    'departure_city': parts[2],
                    'arrival_city': parts[3],
                    'departure_time': parts[4],
                    'arrival_time': parts[5],
                    'price': float(parts[6]),
                    'class_type': parts[7],
                    'duration': parts[8]
                }
                flights.append(flight)
    except Exception:
        pass
    return flights

def load_packages():
    filepath = 'data/packages.txt'
    packages = []
    if not os.path.isfile(filepath):
        return packages
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                package = {
                    'package_id': int(parts[0]),
                    'package_name': parts[1],
                    'destination': parts[2],
                    'duration_days': int(parts[3]),
                    'price': float(parts[4])
                }
                packages.append(package)
    except Exception:
        pass
    return packages

def load_trips():
    filepath = 'data/trips.txt'
    trips = []
    if not os.path.isfile(filepath):
        return trips
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                trip = {
                    'trip_id': int(parts[0]),
                    'trip_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'total_budget': float(parts[5]),
                    'status': parts[6],
                    'created_date': parts[7]
                }
                trips.append(trip)
    except Exception:
        pass
    return trips

def load_bookings():
    filepath = 'data/bookings.txt'
    bookings = []
    if not os.path.isfile(filepath):
        return bookings
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'trip_id': int(parts[1]),
                    'booking_type': parts[2],
                    'booking_date': parts[3],
                    'amount': float(parts[4]),
                    'confirmation_number': parts[5],
                    'status': parts[6]
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings

@app.route('/')
def dashboard():
    # featured_destinations: list of dict {dest_id:int, name:str, country:str}
    # upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
    destinations = load_destinations()
    trips = load_trips()

    # Compose featured_destinations (e.g., first 5 from destinations with minimal fields)
    featured_destinations = [{
        'dest_id': d['dest_id'],
        'name': d['name'],
        'country': d['country']
    } for d in destinations[:5]]

    # Compose upcoming_trips (filter trips with start_date in the future or any status, just display all here as example)
    upcoming_trips = [{
        'trip_id': t['trip_id'],
        'trip_name': t['trip_name'],
        'destination': t['destination'],
        'start_date': t['start_date'],
        'end_date': t['end_date'],
        'status': t['status']
    } for t in trips[:5]]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations_all = load_destinations()
    search_query = ''
    region_filter = ''
    filtered_destinations = destinations_all

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        region_filter = request.form.get('region_filter', '').strip()

        def matches_search(d):
            if not search_query:
                return True
            return search_query.lower() in d['name'].lower()

        def matches_region(d):
            if not region_filter:
                return True
            return d['region'] == region_filter

        filtered_destinations = [d for d in destinations_all if matches_search(d) and matches_region(d)]

    return render_template('destinations.html', destinations=filtered_destinations, search_query=search_query, region_filter=region_filter)

@app.route('/destinations/<int:dest_id>')
def destination_details(dest_id):
    destinations_all = load_destinations()
    destination = None
    for d in destinations_all:
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
        return redirect(url_for('destinations'))
    return render_template('destination_details.html', destination=destination)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_all = load_itineraries()

    if request.method == 'POST':
        # According to spec, add_activity_button triggers POST or client-side addition
        # No specific POST field details given, so no changes to data file
        # Just reload the page for now
        pass

    return render_template('itinerary.html', itineraries=itineraries_all)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels_all = load_hotels()
    destination_query = ''
    check_in_date = ''
    check_out_date = ''
    price_filter = ''
    filtered_hotels = hotels_all

    if request.method == 'POST':
        destination_query = request.form.get('destination_query', '').strip()
        check_in_date = request.form.get('check_in_date', '').strip()
        check_out_date = request.form.get('check_out_date', '').strip()
        price_filter = request.form.get('price_filter', '').strip()

        def matches_destination(h):
            if not destination_query:
                return True
            return destination_query.lower() in h['city'].lower()

        def matches_price(h):
            if not price_filter:
                return True
            # Assuming price_filter is a string like "0-100", "101-200" etc.
            try:
                low, high = price_filter.split('-')
                low = float(low)
                high = float(high)
                return low <= h['price_per_night'] <= high
            except Exception:
                return True

        filtered_hotels = [h for h in hotels_all if matches_destination(h) and matches_price(h)]

    return render_template('accommodations.html', hotels=filtered_hotels, destination_query=destination_query, check_in_date=check_in_date, check_out_date=check_out_date, price_filter=price_filter)

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights_all = load_flights()
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    flight_class_filter = ''
    filtered_flights = flights_all

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').strip()
        arrival_city = request.form.get('arrival_city', '').strip()
        departure_date = request.form.get('departure_date', '').strip()
        flight_class_filter = request.form.get('flight_class_filter', '').strip()

        def matches_departure_city(f):
            if not departure_city:
                return True
            return departure_city.lower() in f['departure_city'].lower()

        def matches_arrival_city(f):
            if not arrival_city:
                return True
            return arrival_city.lower() in f['arrival_city'].lower()

        def matches_class(f):
            if not flight_class_filter:
                return True
            return f['class_type'].lower() == flight_class_filter.lower()

        filtered_flights = [f for f in flights_all if matches_departure_city(f) and matches_arrival_city(f) and matches_class(f)]

    return render_template('transportation.html', flights=filtered_flights, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date, flight_class_filter=flight_class_filter)

@app.route('/packages')
def packages():
    packages_all = load_packages()
    duration_filter = request.args.get('duration_filter', '').strip()

    filtered_packages = packages_all
    if duration_filter:
        try:
            duration_int = int(duration_filter)
            filtered_packages = [p for p in packages_all if p['duration_days'] == duration_int]
        except Exception:
            pass

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter)

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_all = load_trips()
    if request.method == 'POST':
        # POST deletion trigger
        trip_id_str = request.form.get('delete_trip_id', '').strip()
        # No file modification as per spec, just reload
        pass
    return render_template('trips.html', trips=trips_all)

@app.route('/booking-confirmation')
def booking_confirmation():
    # Fetch booking confirmation by query param pkg_id or default first booking
    pkg_id = request.args.get('pkg_id', None)
    bookings_all = load_bookings()
    booking = None
    # Find booking with confirmation_number by pkg_id? No direct pkg_id in booking. Return first booking.
    if bookings_all:
        booking = {
            'confirmation_number': bookings_all[0]['confirmation_number'],
            'booking_details': f"Booking details for confirmation {bookings_all[0]['confirmation_number']}"
        }
    else:
        booking = {'confirmation_number': '', 'booking_details': ''}
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    recommendations_list = [
        {'name': 'Paris', 'popularity_rank': 1},
        {'name': 'Tokyo', 'popularity_rank': 2},
        {'name': 'Rio de Janeiro', 'popularity_rank': 3}
    ]
    filters = {'season': '', 'budget': ''}

    if request.method == 'POST':
        filters['season'] = request.form.get('season', '').strip()
        filters['budget'] = request.form.get('budget', '').strip()
        # Filter recommendations based on filters is not specified, so not altering list

    return render_template('recommendations.html', recommendations=recommendations_list, filters=filters)

if __name__ == '__main__':
    app.run(debug=True)
