from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

def load_destinations():
    destinations = []
    try:
        with open('data/destinations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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
    except (FileNotFoundError, IOError):
        destinations = []
    return destinations


def load_itineraries():
    itineraries = []
    try:
        with open('data/itineraries.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        itineraries = []
    return itineraries


def load_hotels():
    hotels = []
    try:
        with open('data/hotels.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        hotels = []
    return hotels


def load_flights():
    flights = []
    try:
        with open('data/flights.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        flights = []
    return flights


def load_packages():
    packages = []
    try:
        with open('data/packages.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        packages = []
    return packages


def load_trips():
    trips = []
    try:
        with open('data/trips.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        trips = []
    return trips


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
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
    except (FileNotFoundError, IOError):
        bookings = []
    return bookings


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    destinations = load_destinations()
    # featured_destinations: select a subset or all (assumed all for now)
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations
    ]

    trips = load_trips()
    # upcoming_trips: filter trips with start_date in future would be ideal, but no date info processing specified
    upcoming_trips = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'start_date': t['start_date'],
            'end_date': t['end_date']
        } for t in trips
    ]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations_list = load_destinations()
    # context variable destinations includes dest_id, name, country, region
    destinations_slim = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        } for d in destinations_list
    ]
    return render_template('destinations.html', destinations=destinations_slim)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_list = load_destinations()
    destination = None
    for d in destinations_list:
        if d['dest_id'] == dest_id:
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
        # Optional: could return 404, but spec does not say
        return redirect(url_for('destinations'))

    if request.method == 'POST':
        # Add to trip logic is frontend handled button
        # For backend, assuming it adds destination to some trip or processing
        # Spec does not specify detailed post processing, so just redirect back
        return redirect(url_for('destination_details', dest_id=dest_id))

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_list = load_itineraries()

    # POST handling for add activity is frontend handled, no form data specified
    if request.method == 'POST':
        # Since no form structure specified, do nothing backend side
        # redirect back GET
        return redirect(url_for('itinerary'))

    return render_template('itinerary.html', itineraries=itineraries_list)


@app.route('/accommodations')
def accommodations():
    hotels_list = load_hotels()
    return render_template('accommodations.html', hotels=hotels_list)


@app.route('/transportation')
def transportation():
    flights_list = load_flights()
    return render_template('transportation.html', flights=flights_list)


@app.route('/packages')
def packages():
    packages_list = load_packages()
    return render_template('packages.html', packages=packages_list)


@app.route('/packages/<int:package_id>')
def package_details(package_id):
    packages_list = load_packages()
    package = None
    for p in packages_list:
        if p['package_id'] == package_id:
            package = p
            break

    if package is None:
        # Redirect to packages list if not found
        return redirect(url_for('packages'))

    return render_template('package_details.html', package=package)


@app.route('/trips')
def trips():
    trips_list = load_trips()
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
        return redirect(url_for('trips'))

    # POST for edits/deletes
    if request.method == 'POST':
        # No specific editing/deleting logic documented
        return redirect(url_for('trip_details', trip_id=trip_id))

    return render_template('trip_details.html', trip=trip)


@app.route('/booking-confirmation')
def booking_confirmation():
    bookings_list = load_bookings()
    # Spec not clear about which booking to show, so showing first booking if any
    booking = bookings_list[0] if bookings_list else None
    if booking is None:
        # Redirect to dashboard if no bookings
        return redirect(url_for('dashboard'))

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    destinations_list = load_destinations()
    # trending_destinations: select dest_id, name, country, popularity is not in destinations, assume fake popularity 0
    # but spec examples have popularity, so try to derive popularity as 0
    # Instead: We do not have popularity field in destinations.txt, not specified where from.
    # For demonstration, we assign popularity as 0
    trending_destinations = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'popularity': 0
        } for d in destinations_list
    ]
    filters = {'season': '', 'budget': ''}

    return render_template('recommendations.html', trending_destinations=trending_destinations, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
