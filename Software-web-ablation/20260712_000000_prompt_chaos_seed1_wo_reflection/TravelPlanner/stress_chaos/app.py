from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading data from files

def load_destinations():
    path = os.path.join(DATA_DIR, 'destinations.txt')
    destinations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # dest_id|name|country|region|description|attractions|climate
                    fields = line.split('|')
                    dest = {
                        'dest_id': int(fields[0]),
                        'name': fields[1],
                        'country': fields[2],
                        'region': fields[3],
                        'description': fields[4],
                        'attractions': fields[5],
                        # climate is not used per context requirements
                    }
                    destinations.append(dest)
    except FileNotFoundError:
        destinations = []
    return destinations


def load_itineraries():
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    itineraries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
                    fields = line.split('|')
                    itinerary = {
                        'itinerary_id': int(fields[0]),
                        'itinerary_name': fields[1],
                        'destination': fields[2],
                        'start_date': fields[3],
                        'end_date': fields[4],
                        'activities': fields[5],
                        'status': fields[6]
                    }
                    itineraries.append(itinerary)
    except FileNotFoundError:
        itineraries = []
    return itineraries


def load_hotels():
    path = os.path.join(DATA_DIR, 'hotels.txt')
    hotels = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # hotel_id|name|city|rating|price_per_night|amenities|category
                    fields = line.split('|')
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
    except FileNotFoundError:
        hotels = []
    return hotels


def load_flights():
    path = os.path.join(DATA_DIR, 'flights.txt')
    flights = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
                    fields = line.split('|')
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
    except FileNotFoundError:
        flights = []
    return flights


def load_packages():
    path = os.path.join(DATA_DIR, 'packages.txt')
    packages = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # package_id|package_name|destination|duration_days|price|included_items|difficulty_level
                    fields = line.split('|')
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
    except FileNotFoundError:
        packages = []
    return packages


def load_trips():
    path = os.path.join(DATA_DIR, 'trips.txt')
    trips = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
                    fields = line.split('|')
                    trip = {
                        'trip_id': int(fields[0]),
                        'trip_name': fields[1],
                        'destination': fields[2],
                        'start_date': fields[3],
                        'end_date': fields[4],
                        'status': fields[6],  # using status from 7th field
                    }
                    trips.append(trip)
    except FileNotFoundError:
        trips = []
    return trips


def load_bookings():
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    # booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
                    fields = line.split('|')
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
    except FileNotFoundError:
        bookings = []
    return bookings


@app.route('/')
def dashboard():
    # Load destinations and trips
    destinations = load_destinations()
    trips = load_trips()

    # featured_destinations fields: dest_id, name, country
    # We pick first 3 destinations as featured for example
    featured_destinations = [{
        'dest_id': d['dest_id'],
        'name': d['name'],
        'country': d['country']
    } for d in destinations[:3]]

    # upcoming_trips fields: trip_id, trip_name, start_date, end_date
    # We pick trips sorted by start_date ascending and future or current date to simulate upcoming trips
    # For simplicity we'll just pick first 3 trips
    upcoming_trips = [{
        'trip_id': t['trip_id'],
        'trip_name': t['trip_name'],
        'start_date': t['start_date'],
        'end_date': t['end_date']
    } for t in trips[:3]]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations = load_destinations()
    # context fields: dest_id, name, country, region
    context_destinations = [{
        'dest_id': d['dest_id'],
        'name': d['name'],
        'country': d['country'],
        'region': d['region']
    } for d in destinations]
    return render_template('destinations.html', destinations=context_destinations)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        # Could show 404 or redirect to destinations
        return redirect(url_for('destinations'))

    if request.method == 'POST':
        # Add to trip post handling - not specified fully so just a placeholder
        # For now, just redirect back to this page
        return redirect(url_for('destination_details', dest_id=dest_id))

    # context fields: dest_id, name, country, description, attractions
    context_destination = {
        'dest_id': destination['dest_id'],
        'name': destination['name'],
        'country': destination['country'],
        'description': destination['description'],
        'attractions': destination['attractions']
    }
    return render_template('destination_details.html', destination=context_destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = load_itineraries()

    if request.method == 'POST':
        # Add activity handling - no specifics, just reload page for now
        return redirect(url_for('itinerary'))

    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations')
def accommodations():
    hotels = load_hotels()
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation')
def transportation():
    flights = load_flights()
    return render_template('transportation.html', flights=flights)


@app.route('/packages')
def travel_packages():
    packages = load_packages()
    return render_template('packages.html', packages=packages)


@app.route('/trips')
def trips():
    trips = load_trips()
    return render_template('trips.html', trips=trips)


@app.route('/booking_confirmation')
def booking_confirmation():
    bookings = load_bookings()
    # For demonstration, show first booking or empty dict
    booking = bookings[0] if bookings else {}
    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    # We do not have a specific data file for recommendations or trending destinations.
    # For demonstration, compose fake empty lists or example content.
    recommendations = []
    trending_destinations = []

    # To somewhat comply with design spec, we might derive trending from destinations by popularity rank
    # As no popularity rank is given, we fabricate popularity rank by ordering
    destinations = load_destinations()
    for idx, d in enumerate(destinations):
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'popularity rank': idx + 1  # popularity rank starting at 1
        })

    return render_template('recommendations.html', recommendations=recommendations, trending_destinations=trending_destinations)


if __name__ == '__main__':
    app.run(debug=True)
