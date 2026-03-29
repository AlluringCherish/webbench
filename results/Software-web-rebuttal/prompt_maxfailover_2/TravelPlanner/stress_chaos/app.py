from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Utility loaders for data files

def load_destinations():
    filepath = os.path.join(data_dir, 'destinations.txt')
    destinations = []
    if not os.path.exists(filepath):
        return destinations
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    dest = {
                        'dest_id': int(parts[0]),
                        'name': parts[1],
                        'country': parts[2],
                        'region': parts[3],
                        'description': parts[4],
                        'attractions': [a.strip() for a in parts[5].split(',')] if parts[5] else [],
                        'climate': parts[6]
                    }
                    destinations.append(dest)
    except Exception:
        pass
    return destinations

def load_itineraries():
    filepath = os.path.join(data_dir, 'itineraries.txt')
    itineraries = []
    if not os.path.exists(filepath):
        return itineraries
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    filepath = os.path.join(data_dir, 'hotels.txt')
    hotels = []
    if not os.path.exists(filepath):
        return hotels
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    filepath = os.path.join(data_dir, 'flights.txt')
    flights = []
    if not os.path.exists(filepath):
        return flights
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
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
    filepath = os.path.join(data_dir, 'packages.txt')
    packages = []
    if not os.path.exists(filepath):
        return packages
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    package = {
                        'package_id': int(parts[0]),
                        'package_name': parts[1],
                        'destination': parts[2],
                        'duration_days': int(parts[3]),
                        'price': float(parts[4]),
                        'included_items': parts[5],
                        'difficulty_level': parts[6]
                    }
                    packages.append(package)
    except Exception:
        pass
    return packages

def load_trips():
    filepath = os.path.join(data_dir, 'trips.txt')
    trips = []
    if not os.path.exists(filepath):
        return trips
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
    filepath = os.path.join(data_dir, 'bookings.txt')
    bookings = []
    if not os.path.exists(filepath):
        return bookings
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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

# Routes

@app.route('/')
def dashboard_view():
    # Load needed data
    destinations = load_destinations()
    # featured_destinations: list of dict with keys: dest_id, name, country, image_url
    # From destinations.txt, featured destinations - choose all or some?
    # No indication of how to pick featured - we will show all with fields needed

    # Compose featured_destinations subset with required fields
    featured_destinations = []
    for d in destinations:
        item = {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            # No image_url in destinations.txt - spec says field named image_url is needed
            # As per spec, no image_url in data. However, must provide image_url key, maybe empty string
            'image_url': ''
        }
        featured_destinations.append(item)

    # upcoming_trips from trips.txt
    all_trips = load_trips()
    # trips list of dict with keys: trip_id, name, destination, start_date
    upcoming_trips = []
    for t in all_trips:
        upcoming_trips.append({
            'trip_id': t['trip_id'],
            'name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date']
        })

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations')
def destinations_view():
    search_query = request.args.get('search_query', '', type=str)
    selected_region = request.args.get('selected_region', '', type=str)

    all_destinations = load_destinations()
    # Filter by search_query in name case-insensitive
    filtered_destinations = []
    for d in all_destinations:
        if search_query.lower() in d['name'].lower():
            if selected_region == '' or d['region'] == selected_region:
                filtered_destinations.append(d)

    # Context variables destinations, search_query, selected_region
    return render_template('destinations.html', destinations=filtered_destinations, search_query=search_query, selected_region=selected_region)

@app.route('/destination/<int:dest_id>')
def destination_detail_view(dest_id):
    all_destinations = load_destinations()
    destination = None
    for d in all_destinations:
        if d['dest_id'] == dest_id:
            destination = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'region': d['region'],
                'description': d['description']
            }
            attractions = d['attractions']
            break
    if destination is None:
        # Destination not found
        destination = {
            'dest_id': dest_id,
            'name': '',
            'country': '',
            'region': '',
            'description': ''
        }
        attractions = []

    # Pass destination (dict) and attractions (list of str)
    return render_template('destination_detail.html', destination=destination, attractions=attractions)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_view():
    form_errors = {}
    if request.method == 'POST':
        # Not detailed in spec about the POST form fields or processing
        # So for spec compliance, keep handling but do nothing (or minimal validation)
        # We do not save data since not specified
        pass
    itineraries = load_itineraries()
    # context variables: itineraries (list of dict), form_errors (dict)
    return render_template('itinerary.html', itineraries=itineraries, form_errors=form_errors)

@app.route('/accommodations')
def accommodations_view():
    # Filters from query params
    filters = {
        'destination': request.args.get('destination', '', type=str),
        'check_in_date': request.args.get('check_in_date', '', type=str),
        'check_out_date': request.args.get('check_out_date', '', type=str),
        'price_filter': request.args.get('price_filter', '', type=str)
    }
    hotels = load_hotels()

    # Filter hotels by filters
    filtered_hotels = []
    for h in hotels:
        if filters['destination'] and filters['destination'].lower() != h['city'].lower():
            continue
        if filters['price_filter']:
            try:
                price_limit = float(filters['price_filter'])
                if h['price_per_night'] > price_limit:
                    continue
            except Exception:
                # If price_filter is not a valid float, ignore filter
                pass
        filtered_hotels.append(h)

    return render_template('accommodations.html', hotels=filtered_hotels, filters=filters)

@app.route('/transportation')
def transportation_view():
    filters = {
        'departure_city': request.args.get('departure_city', '', type=str),
        'arrival_city': request.args.get('arrival_city', '', type=str),
        'departure_date': request.args.get('departure_date', '', type=str),
        'flight_class_filter': request.args.get('flight_class_filter', '', type=str)
    }
    flights = load_flights()

    filtered_flights = []
    for f in flights:
        if filters['departure_city'] and filters['departure_city'].lower() != f['departure_city'].lower():
            continue
        if filters['arrival_city'] and filters['arrival_city'].lower() != f['arrival_city'].lower():
            continue
        if filters['flight_class_filter'] and filters['flight_class_filter'].lower() != f['class_type'].lower():
            continue
        # Spec does not mention departure_date filtering by exact date, so ignoring for now
        filtered_flights.append(f)

    return render_template('transportation.html', flights=filtered_flights, filters=filters)

@app.route('/packages')
def packages_view():
    duration_filter = request.args.get('duration_filter', '', type=str)
    packages = load_packages()
    filtered_packages = []
    for p in packages:
        if duration_filter:
            try:
                duration_val = int(duration_filter)
                if p['duration_days'] != duration_val:
                    continue
            except Exception:
                # ignore invalid filter
                pass
        filtered_packages.append(p)

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter)

@app.route('/trips')
def trips_view():
    trips = load_trips()
    return render_template('trips.html', trips=trips)

@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation_view(booking_id):
    bookings = load_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    trips = load_trips()
    trip = None
    if booking:
        for t in trips:
            if t['trip_id'] == booking['trip_id']:
                trip = t
                break
    if booking is None:
        # fallback empty dicts
        booking = {}
    if trip is None:
        trip = {}

    return render_template('booking_confirmation.html', booking=booking, trip=trip)

@app.route('/recommendations')
def recommendations_view():
    filters = {
        'recommendation_season_filter': request.args.get('recommendation_season_filter', '', type=str),
        'budget_filter': request.args.get('budget_filter', '', type=str)
    }
    # There is no explicit data file for recommendations.
    # We assume recommendations are combinations from destinations and trips or dummy empty list
    # Spec only says recommendations is list of dict for recommended trips/destinations

    recommendations = []
    # For a minimal implementation, no filtering or data sourcing since no data source provided

    return render_template('recommendations.html', recommendations=recommendations, filters=filters)

if __name__ == '__main__':
    app.run(debug=True)
