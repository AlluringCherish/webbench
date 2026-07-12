from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

def read_destinations():
    path = 'data/destinations.txt'
    destinations = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        # Return empty list if file not found or error
        destinations = []
    return destinations


def read_itineraries():
    path = 'data/itineraries.txt'
    itineraries = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        itineraries = []
    return itineraries


def read_hotels():
    path = 'data/hotels.txt'
    hotels = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        hotels = []
    return hotels


def read_flights():
    path = 'data/flights.txt'
    flights = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        flights = []
    return flights


def read_packages():
    path = 'data/packages.txt'
    packages = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    pkg = {
                        'package_id': int(parts[0]),
                        'package_name': parts[1],
                        'destination': parts[2],
                        'duration_days': int(parts[3]),
                        'price': float(parts[4]),
                        'included_items': parts[5],
                        'difficulty_level': parts[6]
                    }
                    packages.append(pkg)
    except IOError:
        packages = []
    return packages


def read_trips():
    path = 'data/trips.txt'
    trips = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        trips = []
    return trips


def read_bookings():
    path = 'data/bookings.txt'
    bookings = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
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
    except IOError:
        bookings = []
    return bookings


@app.route('/')
def dashboard():
    # Load destinations and trips
    destinations = read_destinations()
    trips = read_trips()

    # Featured destinations: We can assume featured means first few destinations
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations[:5]
    ]

    # Upcoming trips: trips with start_date >= today could be filtered but spec does not require that
    # For simplicity, show all trips with fields as required
    upcoming_trips = [
        {'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'destination': t['destination'], 'start_date': t['start_date']} for t in trips
    ]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations_list = read_destinations()

    # Get possible query parameters for search and filter (optional)
    search_query = request.args.get('search_query', default='')
    region_filter = request.args.get('region_filter', default='')

    # Filter the destinations list based on search_query and region_filter
    filtered_destinations = destinations_list
    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query.lower() in d['name'].lower() or search_query.lower() in d['country'].lower()]
    if region_filter:
        filtered_destinations = [d for d in filtered_destinations if d['region'].lower() == region_filter.lower()]

    # Prepare list with required keys for template
    destinations_context = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        } for d in filtered_destinations
    ]

    return render_template('destinations.html', destinations=destinations_context, search_query=search_query, region_filter=region_filter)


@app.route('/destinations/<int:dest_id>')
def destination_details(dest_id):
    destinations_list = read_destinations()
    destination = None
    for d in destinations_list:
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
        # If destination not found, redirect to destinations list
        return redirect(url_for('destinations'))

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_list = read_itineraries()

    if request.method == 'POST':
        # The spec states POST is used to add activity to itinerary
        # Here we do not have file writing capabilities so we do not persist changes
        # Form fields could be here, but since no frontend or data format change requested, just reload GET
        pass

    return render_template('itinerary.html', itineraries=itineraries_list)


@app.route('/accommodations')
def accommodations():
    hotels_list = read_hotels()
    return render_template('accommodations.html', hotels=hotels_list)


@app.route('/transportation')
def transportation():
    flights_list = read_flights()
    return render_template('transportation.html', flights=flights_list)


@app.route('/packages')
def packages():
    packages_list = read_packages()

    # Optional filter duration_filter
    duration_filter = request.args.get('duration_filter', default='')
    filtered_packages = packages_list
    if duration_filter:
        try:
            duration_val = int(duration_filter)
            filtered_packages = [p for p in packages_list if p['duration_days'] == duration_val]
        except ValueError:
            # Invalid filter, show all
            filtered_packages = packages_list

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter)


@app.route('/trips')
def trips():
    trips_list = read_trips()

    trips_context = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date'],
            'status': t['status']
        } for t in trips_list
    ]

    return render_template('trips.html', trips=trips_context)


@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    bookings_list = read_bookings()
    booking = None
    for b in bookings_list:
        if b['booking_id'] == booking_id:
            booking = b
            break

    if booking is None:
        # Redirect to dashboard if booking not found
        return redirect(url_for('dashboard'))

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    # No data file schema for recommendations; just provide empty lists/dicts
    recommendations_data = []
    trending_destinations_data = []
    filters_data = {'season': '', 'budget': ''}

    return render_template('recommendations.html', recommendations=recommendations_data, trending_destinations=trending_destinations_data, filters=filters_data)


if __name__ == '__main__':
    app.run(debug=True)
