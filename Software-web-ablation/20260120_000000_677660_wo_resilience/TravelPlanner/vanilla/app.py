from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from pipe-delimited text files

def load_destinations():
    destinations = []
    try:
        with open('data/destinations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except (IOError, FileNotFoundError):
        destinations = []
    return destinations


def load_itineraries():
    itineraries = []
    try:
        with open('data/itineraries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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
    except (IOError, FileNotFoundError):
        itineraries = []
    return itineraries


def load_hotels():
    hotels = []
    try:
        with open('data/hotels.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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
    except (IOError, FileNotFoundError):
        hotels = []
    return hotels


def load_flights():
    flights = []
    try:
        with open('data/flights.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
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
    except (IOError, FileNotFoundError):
        flights = []
    return flights


def load_packages():
    packages = []
    try:
        with open('data/packages.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
    except (IOError, FileNotFoundError):
        packages = []
    return packages


def load_trips():
    trips = []
    try:
        with open('data/trips.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
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
    except (IOError, FileNotFoundError):
        trips = []
    return trips


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
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
    except (IOError, FileNotFoundError):
        bookings = []
    return bookings


# Flask Routes

@app.route('/')
def dashboard():
    # Load destinations and trips for dashboard
    destinations = load_destinations()
    trips = load_trips()

    # featured_destinations: list of dict {dest_id:int, name:str, country:str}
    # We pick first 3 destinations for featured (or less if not enough)
    featured_destinations = []
    for d in destinations[:3]:
        featured_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country']
        })

    # upcoming_trips: list of dict {trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str}
    # We include only trips with status Booked or Planned as upcoming
    upcoming_trips = []
    for t in trips:
        if t['status'] in ['Booked', 'Planned', 'In Progress']:
            upcoming_trips.append({
                'trip_id': t['trip_id'],
                'trip_name': t['trip_name'],
                'destination': t['destination'],
                'start_date': t['start_date'],
                'end_date': t['end_date']
            })

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations_data = load_destinations()
    # destinations: list of dict {dest_id:int, name:str, country:str, region:str}
    destinations_list = []
    for d in destinations_data:
        destinations_list.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        })
    return render_template('destinations.html', destinations=destinations_list)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_data = load_destinations()
    destination = None
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
    if not destination:
        abort(404)

    if request.method == 'POST':
        # POST action to add destination to trip
        # We don't have explicit storage actions, so just a placeholder
        # Navigation stays on same page
        # No changes done on backend as per spec
        pass

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()
    if request.method == 'POST':
        # form data to add/edit itinerary
        # Since no storage is specified, we do not save data
        # Keep showing the list as is
        pass
    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations')
def accommodations():
    hotels = load_hotels()
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation')
def transportation():
    flights = load_flights()
    return render_template('transportation.html', flights=flights)


@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages_data = load_packages()

    if request.method == 'POST':
        # POST to book package
        # No database or persistent storage, so placeholder action
        # After booking, assume redirect stays on packages page
        pass

    packages_list = []
    for p in packages_data:
        packages_list.append({
            'package_id': p['package_id'],
            'package_name': p['package_name'],
            'destination': p['destination'],
            'duration_days': p['duration_days'],
            'price': p['price']
        })

    return render_template('packages.html', packages=packages_list)


@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_data = load_trips()
    if request.method == 'POST':
        # POST to delete trip
        # Since no persistent storage or DB, we do not alter data
        # Just render the trips list
        pass

    trips_list = []
    for t in trips_data:
        trips_list.append({
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date'],
            'status': t['status']
        })

    return render_template('trips.html', trips=trips_list)


@app.route('/booking_confirmation')
def booking_confirmation():
    bookings = load_bookings()
    # Just take the most recent confirmed booking
    booking = None
    for b in bookings:
        if b['status'] == 'Confirmed':
            booking = {
                'confirmation_number': b['confirmation_number'],
                'booking_details': f"Type: {b['booking_type']}, Date: {b['booking_date']}, Amount: {b['amount']}"
            }
            break

    if not booking:
        booking = {'confirmation_number': '', 'booking_details': ''}

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    destinations = load_destinations()
    # trending_destinations: list of dict {dest_id:int, name:str, popularity_rank:int}
    # For simplicity, pick top 3 destinations sorted by dest_id asc as popularity rank
    trending_destinations = []
    sorted_dests = sorted(destinations, key=lambda d: d['dest_id'])[:3]
    rank = 1
    for d in sorted_dests:
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'popularity_rank': rank
        })
        rank += 1

    # filters: dict {recommendation_season:str, budget:str}
    # Since filters values are not stored or passed by user, just set defaults
    filters = {'recommendation_season': 'Summer', 'budget': 'Medium'}

    return render_template('recommendations.html', trending_destinations=trending_destinations, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
