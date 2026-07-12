from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
DESTINATIONS_FILE = os.path.join(DATA_DIR, 'destinations.txt')
ITINERARIES_FILE = os.path.join(DATA_DIR, 'itineraries.txt')
HOTELS_FILE = os.path.join(DATA_DIR, 'hotels.txt')
FLIGHTS_FILE = os.path.join(DATA_DIR, 'flights.txt')
PACKAGES_FILE = os.path.join(DATA_DIR, 'packages.txt')
TRIPS_FILE = os.path.join(DATA_DIR, 'trips.txt')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.txt')

# Helper functions to read pipe-delimited files

def read_destinations():
    destinations = []
    try:
        with open(DESTINATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
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


def read_itineraries():
    itineraries = []
    try:
        with open(ITINERARIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
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


def read_hotels():
    hotels = []
    try:
        with open(HOTELS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        hotels = []
    return hotels


def read_flights():
    flights = []
    try:
        with open(FLIGHTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        flights = []
    return flights


def read_packages():
    packages = []
    try:
        with open(PACKAGES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                try:
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        packages = []
    return packages


def read_trips():
    trips = []
    try:
        with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        trips = []
    return trips


def read_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        bookings = []
    return bookings


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    destinations = read_destinations()
    featured_destinations = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations]

    trips = read_trips()
    upcoming_trips = sorted([
        {'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'destination': t['destination'], 'start_date': t['start_date']}
        for t in trips
    ], key=lambda x: x['start_date'])

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = read_destinations()
    return render_template('destinations.html', destinations=destinations)


@app.route('/destinations/<int:dest_id>', methods=['GET'])
def destination_details(dest_id):
    destinations = read_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        destination = {}
    destination_context = {
        'name': destination.get('name', ''),
        'country': destination.get('country', ''),
        'description': destination.get('description', ''),
        'attractions': destination.get('attractions', '')
    }
    return render_template('destination_details.html', destination=destination_context)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_planning():
    if request.method == 'POST':
        pass  # add-activity-button handling not detailed
    itineraries = read_itineraries()
    return render_template('itinerary_planning.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = read_hotels()
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = read_flights()
    return render_template('transportation.html', flights=flights)


@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages = read_packages()
    return render_template('packages.html', packages=packages)


@app.route('/trips', methods=['GET'])
def trip_management():
    trips = read_trips()
    return render_template('trips.html', trips=trips)


@app.route('/booking-confirmation', methods=['GET'])
def booking_confirmation():
    bookings = read_bookings()
    booking_info = {}
    if bookings:
        b = bookings[0]
        booking_info = {
            'confirmation_number': b.get('confirmation_number', ''),
            'booking_details': f"{b.get('booking_type', '')} booked from {b.get('booking_date', '')}"
        }
    return render_template('booking_confirmation.html', booking_info=booking_info)


@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations():
    recommendations = []
    trending_destinations = []
    destinations = read_destinations()
    pop_scores = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    for i, d in enumerate(destinations):
        score = pop_scores[i % len(pop_scores)]
        trending_destinations.append({'dest_id': d['dest_id'], 'name': d['name'], 'popularity': score})
    return render_template('recommendations.html', recommendations=recommendations, trending_destinations=trending_destinations)


if __name__ == '__main__':
    app.run(debug=True)
