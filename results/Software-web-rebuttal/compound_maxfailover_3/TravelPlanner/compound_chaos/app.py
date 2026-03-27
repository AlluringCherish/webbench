from flask import Flask, render_template, request, redirect, url_for, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading data from files

def load_destinations():
    filepath = os.path.join(DATA_DIR, 'destinations.txt')
    destinations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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
    except (IOError, OSError):
        # Unable to read file, return empty list
        destinations = []
    return destinations


def load_itineraries():
    filepath = os.path.join(DATA_DIR, 'itineraries.txt')
    itineraries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
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
    except (IOError, OSError):
        itineraries = []
    return itineraries


def load_hotels():
    filepath = os.path.join(DATA_DIR, 'hotels.txt')
    hotels = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
                    hotel = {
                        'hotel_id': int(parts[0]),
                        'name': parts[1],
                        'city': parts[2],
                        'rating': float(parts[3]),
                        'price_per_night': float(parts[4]),
                        'amenities': parts[5],  # as string comma separated
                        'category': parts[6]
                    }
                    hotels.append(hotel)
                except ValueError:
                    continue
    except (IOError, OSError):
        hotels = []
    return hotels


def load_flights():
    filepath = os.path.join(DATA_DIR, 'flights.txt')
    flights = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                try:
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
                except ValueError:
                    continue
    except (IOError, OSError):
        flights = []
    return flights


def load_packages():
    filepath = os.path.join(DATA_DIR, 'packages.txt')
    packages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                try:
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
                except ValueError:
                    continue
    except (IOError, OSError):
        packages = []
    return packages


def load_trips():
    filepath = os.path.join(DATA_DIR, 'trips.txt')
    trips = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
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
                except ValueError:
                    continue
    except (IOError, OSError):
        trips = []
    return trips


def load_bookings():
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                try:
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
                except ValueError:
                    continue
    except (IOError, OSError):
        bookings = []
    return bookings


# =================== ROUTES ======================

@app.route('/')
def dashboard():
    # Load destinations and trips data
    destinations = load_destinations()
    trips = load_trips()

    # featured_destinations: list of dict {dest_id, name, country} -- choose top 3 for example
    # We'll assume first 3 destinations as featured
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']}
        for d in destinations[:3]
    ]
    
    # upcoming_trips: list of dict {trip_id, trip_name, start_date, end_date}
    # For simplicity, pick trips with start_date >= today's date?
    # Since we don't have date parsing requirement and no current date info, repurpose all trips as upcoming_trips - leave full trips list
    upcoming_trips = [
        {'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'start_date': t['start_date'], 'end_date': t['end_date']}
        for t in trips
    ]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations_list = load_destinations()
    search_query = ''
    region_filter = ''

    if request.method == 'POST':
        # Extract filter/search query params
        search_query = request.form.get('search_query', '').strip()
        region_filter = request.form.get('region_filter', '').strip()
    else:
        # GET method: no filters
        search_query = ''
        region_filter = ''

    filtered_destinations = destinations_list

    if search_query:
        filter_lower = search_query.lower()
        filtered_destinations = [d for d in filtered_destinations if filter_lower in d['name'].lower() or filter_lower in d['country'].lower()]

    if region_filter and region_filter in ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']:
        filtered_destinations = [d for d in filtered_destinations if d['region'] == region_filter]

    # Distinct on fields for context: dest_id, name, country, region
    context_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']}
        for d in filtered_destinations
    ]

    return render_template('destinations.html', destinations=context_destinations, search_query=search_query, region_filter=region_filter)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_list = load_destinations()
    destination = None
    for d in destinations_list:
        if d['dest_id'] == dest_id:
            # dict with keys: dest_id, name, country, description, attractions, climate
            destination = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions'],
                'climate': d['climate']
            }
            break
    if destination is None:
        abort(404)

    if request.method == 'POST':
        # 'add-to-trip-button' triggers addition to a trip
        # Spec says POST triggers addition to itinerary or equivalent.
        # We'll redirect POST to /itinerary endpoint for planning (as per design or a redirect after POST).
        # For simplicity, redirect to itinerary page.
        return redirect(url_for('plan_itinerary'))

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()

    if request.method == 'POST':
        # Handle add activity form or edits (not fully specified), so no data persistence.
        # For this implementation, just redirect back to GET view after POST.
        return redirect(url_for('plan_itinerary'))

    # Context variable: list of dict {itinerary_id, itinerary_name, destination, start_date, end_date, activities, status}
    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = load_hotels()
    filters = {
        'destination': '',
        'check_in': '',
        'check_out': '',
        'price_range': ''
    }

    if request.method == 'POST':
        filters['destination'] = request.form.get('destination', '').strip()
        filters['check_in'] = request.form.get('check_in', '').strip()
        filters['check_out'] = request.form.get('check_out', '').strip()
        filters['price_range'] = request.form.get('price_range', '').strip()
    else:
        filters = {'destination': '', 'check_in': '', 'check_out': '', 'price_range': ''}

    filtered_hotels = hotels

    if filters['destination']:
        filtered_hotels = [h for h in filtered_hotels if h['city'].lower() == filters['destination'].lower()]

    # price_range filter expected formats are not specified precisely; we'll assume formats like "< 100", "100-200", "> 200"
    # For now, simple implementation:
    if filters['price_range']:
        price_filter = filters['price_range'].strip()
        try:
            if price_filter.startswith('<'):
                max_price = float(price_filter[1:].strip())
                filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] < max_price]
            elif price_filter.startswith('>'):
                min_price = float(price_filter[1:].strip())
                filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] > min_price]
            elif '-' in price_filter:
                parts = price_filter.split('-')
                min_price = float(parts[0].strip())
                max_price = float(parts[1].strip())
                filtered_hotels = [h for h in filtered_hotels if min_price <= h['price_per_night'] <= max_price]
        except Exception:
            pass

    return render_template('accommodations.html', hotels=filtered_hotels, filters=filters)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = load_flights()
    filters = {
        'departure_city': '',
        'arrival_city': '',
        'departure_date': '',  # no date in flight data, just in filter
        'flight_class': ''
    }

    if request.method == 'POST':
        filters['departure_city'] = request.form.get('departure_city', '').strip()
        filters['arrival_city'] = request.form.get('arrival_city', '').strip()
        filters['departure_date'] = request.form.get('departure_date', '').strip()
        filters['flight_class'] = request.form.get('flight_class', '').strip()
    else:
        filters = {'departure_city': '', 'arrival_city': '', 'departure_date': '', 'flight_class': ''}

    filtered_flights = flights

    if filters['departure_city']:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == filters['departure_city'].lower()]
    if filters['arrival_city']:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == filters['arrival_city'].lower()]
    if filters['flight_class']:
        filtered_flights = [f for f in filtered_flights if f['class_type'].lower() == filters['flight_class'].lower()]

    # departure_date filter present in filters but no flight date info available in data so ignored in this implementation

    return render_template('transportation.html', flights=filtered_flights, filters=filters)


@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages = load_packages()
    duration_filter = ''

    if request.method == 'POST':
        duration_filter = request.form.get('duration_filter', '').strip()
    else:
        duration_filter = ''

    filtered_packages = packages

    if duration_filter:
        # duration_filter options: 3-5 days, 7-10 days, 14+ days
        if duration_filter == '3-5 days':
            filtered_packages = [p for p in filtered_packages if 3 <= p['duration_days'] <= 5]
        elif duration_filter == '7-10 days':
            filtered_packages = [p for p in filtered_packages if 7 <= p['duration_days'] <=10]
        elif duration_filter == '14+ days':
            filtered_packages = [p for p in filtered_packages if p['duration_days'] >= 14]

    # Context variable fields: package_id, package_name, destination, duration_days, price
    context_packages = [
        {
            'package_id': p['package_id'],
            'package_name': p['package_name'],
            'destination': p['destination'],
            'duration_days': p['duration_days'],
            'price': p['price']
        }
        for p in filtered_packages
    ]

    return render_template('packages.html', packages=context_packages, duration_filter=duration_filter)


@app.route('/packages/<int:pkg_id>', methods=['GET'])
def package_details(pkg_id):
    packages = load_packages()
    package = None
    for p in packages:
        if p['package_id'] == pkg_id:
            # dict {package_id, package_name, destination, duration_days, price, included_items, difficulty_level}
            package = {
                'package_id': p['package_id'],
                'package_name': p['package_name'],
                'destination': p['destination'],
                'duration_days': p['duration_days'],
                'price': p['price'],
                'included_items': p['included_items'],
                'difficulty_level': p['difficulty_level']
            }
            break
    if package is None:
        abort(404)
    return render_template('package_details.html', package=package)


@app.route('/packages/<int:pkg_id>/book', methods=['POST'])
def book_package(pkg_id):
    # Since no persistence defined, simulate booking creation and redirect
    # Generate a fake booking_id for redirect
    # Redirect to booking_confirmation with query parameter booking_id

    booking_id = pkg_id  # Use pkg_id as booking_id for simplicity

    # Redirect as per spec
    return redirect(url_for('booking_confirmation') + f'?booking_id={booking_id}')


@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_list = load_trips()

    if request.method == 'POST':
        # No detailed post handling defined
        return redirect(url_for('trips'))

    return render_template('trips.html', trips=trips_list)


@app.route('/trips/<int:trip_id>', methods=['GET', 'POST'])
def trip_details(trip_id):
    trips_list = load_trips()
    trip = None
    for t in trips_list:
        if t['trip_id'] == trip_id:
            trip = t
            break
    if trip is None:
        abort(404)

    bookings = load_bookings()
    # Filter bookings for this trip
    trip_bookings = [b for b in bookings if b['trip_id'] == trip_id]

    return render_template('trip_details.html', trip=trip, bookings=trip_bookings)


@app.route('/booking_confirmation', methods=['GET'])
def booking_confirmation():
    booking_id_param = request.args.get('booking_id', None)
    booking = None
    bookings = load_bookings()
    if booking_id_param:
        try:
            booking_id_val = int(booking_id_param)
            for b in bookings:
                if b['booking_id'] == booking_id_val:
                    booking = b
                    break
        except (ValueError, TypeError):
            booking = None

    if booking is None:
        abort(404)

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations():
    destinations = load_destinations()
    recommendations = []
    season_filter = ''
    budget_filter = ''

    if request.method == 'POST':
        season_filter = request.form.get('season', '').strip()
        budget_filter = request.form.get('budget', '').strip()
    else:
        season_filter = ''
        budget_filter = ''

    # We'll simulate recommendations from destinations with popularity_rank.
    # Since popularity_rank is not in data, assign a dummy value sorted by dest_id ascending

    recommendations = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'popularity_rank': i+1
        }
        for i, d in enumerate(sorted(destinations, key=lambda x: x['dest_id']))
    ]

    # Filter recommendations:
    # No specifics how season or budget affect recommendations, don't filter actually.

    filters = {
        'season': season_filter,
        'budget': budget_filter
    }

    return render_template('recommendations.html', recommendations=recommendations, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
