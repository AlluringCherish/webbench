from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from files

def load_destinations():
    filepath = 'data/destinations.txt'
    destinations = []
    if not os.path.exists(filepath):
        return destinations

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # dest_id|name|country|region|description|attractions|climate
                fields = line.strip().split('|')
                if len(fields) < 7:
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
    except Exception:
        destinations = []
    return destinations


def load_itineraries():
    filepath = 'data/itineraries.txt'
    itineraries = []
    if not os.path.exists(filepath):
        return itineraries

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
                fields = line.strip().split('|')
                if len(fields) < 7:
                    continue
                itin = {
                    'itinerary_id': int(fields[0]),
                    'itinerary_name': fields[1],
                    'destination': fields[2],
                    'start_date': fields[3],
                    'end_date': fields[4],
                    'activities': fields[5],
                    'status': fields[6]
                }
                itineraries.append(itin)
    except Exception:
        itineraries = []
    return itineraries


def load_hotels():
    filepath = 'data/hotels.txt'
    hotels = []
    if not os.path.exists(filepath):
        return hotels

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # hotel_id|name|city|rating|price_per_night|amenities|category
                fields = line.strip().split('|')
                if len(fields) < 7:
                    continue
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
    except Exception:
        hotels = []
    return hotels


def load_flights():
    filepath = 'data/flights.txt'
    flights = []
    if not os.path.exists(filepath):
        return flights

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
                fields = line.strip().split('|')
                if len(fields) < 9:
                    continue
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
    except Exception:
        flights = []
    return flights


def load_packages():
    filepath = 'data/packages.txt'
    packages = []
    if not os.path.exists(filepath):
        return packages

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # package_id|package_name|destination|duration_days|price|included_items|difficulty_level
                fields = line.strip().split('|')
                if len(fields) < 7:
                    continue
                package = {
                    'package_id': int(fields[0]),
                    'package_name': fields[1],
                    'destination': fields[2],
                    'duration_days': int(fields[3]),
                    'price': float(fields[4]),
                    'included_items': fields[5],
                    'difficulty_level': fields[6]
                }
                packages.append(package)
    except Exception:
        packages = []
    return packages


def load_trips():
    filepath = 'data/trips.txt'
    trips = []
    if not os.path.exists(filepath):
        return trips

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
                fields = line.strip().split('|')
                if len(fields) < 8:
                    continue
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
    except Exception:
        trips = []
    return trips


def load_bookings():
    filepath = 'data/bookings.txt'
    bookings = []
    if not os.path.exists(filepath):
        return bookings

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
                fields = line.strip().split('|')
                if len(fields) < 7:
                    continue
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
    except Exception:
        bookings = []
    return bookings


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # featured_destinations: List[Dict] (dest_id:int, name:str, country:str)
    # upcoming_trips: List[Dict] (trip_id:int, trip_name:str, start_date:str, end_date:str)

    destinations = load_destinations()
    trips = load_trips()

    # Select featured_destinations to just fields required: dest_id, name, country
    featured_destinations = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations]

    # upcoming_trips from trips with limited fields
    upcoming_trips = [{'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'start_date': t['start_date'], 'end_date': t['end_date']} for t in trips]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    # destinations: List[Dict] (dest_id:int, name:str, country:str, region:str)
    destinations_full = load_destinations()
    destinations_list = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']} for d in destinations_full]

    # POST could be for search/filter but not specified to handle POST details, so ignore

    return render_template('destinations.html', destinations=destinations_list)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    # destination: Dict (dest_id:int, name:str, country:str, description:str, attractions:str)
    destinations = load_destinations()
    destination = None
    for d in destinations:
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
        # Could return 404 or fallback, but spec doesn't mention error handling, so empty context
        destination = {'dest_id': dest_id, 'name': '', 'country': '', 'description': '', 'attractions': ''}

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    # itineraries: List[Dict] (itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str)
    itineraries = load_itineraries()

    if request.method == 'POST':
        # Add activity button triggers activity add POST - not specified details on form data or persistence
        # Just reload page with existing data
        pass

    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    # hotels: List[Dict] (hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str)
    hotels = load_hotels()
    # POST form handling not specified, just render
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    # flights: List[Dict] (flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str)
    flights = load_flights()
    # POST form handling not specified, just render
    return render_template('transportation.html', flights=flights)


@app.route('/packages', methods=['GET', 'POST'])
def packages():
    # packages: List[Dict] (package_id:int, package_name:str, destination:str, duration_days:int, price:float, included_items:str)
    packages_list = load_packages()

    return render_template('packages.html', packages=packages_list)


@app.route('/trips', methods=['GET', 'POST'])
def trips():
    # trips: List[Dict] (trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str)
    trips_list = load_trips()

    return render_template('trips.html', trips=trips_list)


@app.route('/booking-confirmation', methods=['GET'])
def booking_confirmation():
    # booking: Dict (confirmation_number:str, booking_details:str)
    # Show latest confirmed booking (assuming latest by booking_id)
    bookings = load_bookings()
    latest_booking = None
    if bookings:
        latest_booking = max(bookings, key=lambda b: b['booking_id'])
        booking = {
            'confirmation_number': latest_booking['confirmation_number'],
            'booking_details': f"{latest_booking['booking_type']} booking on {latest_booking['booking_date']} amount ${latest_booking['amount']:.2f} status {latest_booking['status']}"
        }
    else:
        booking = {'confirmation_number': '', 'booking_details': ''}

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET'])
def recommendations():
    # trending_destinations: List[Dict] (dest_id:int, name:str, popularity_rank:int)
    # filters: Dict (season:str, budget:str)

    destinations = load_destinations()

    # We do not have popularity_rank in destinations, so for demo assign popularity_rank by dest_id ascending
    trending_destinations = [{'dest_id': d['dest_id'], 'name': d['name'], 'popularity_rank': idx+1} for idx, d in enumerate(sorted(destinations, key=lambda x: x['dest_id']))]

    # Simple filters dictionary; no actual filter from request asked, use empty defaults
    filters = {'season': '', 'budget': ''}

    return render_template('recommendations.html', trending_destinations=trending_destinations, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
