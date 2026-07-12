from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
REGION_OPTIONS = ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']
RECOMMENDATION_SEASONS = ['Spring', 'Summer', 'Fall', 'Winter']
BUDGET_RANGES = ['Low', 'Medium', 'High']

# Helper functions to load data from files

def load_destinations():
    destinations = []
    path = os.path.join(DATA_DIR, 'destinations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    except (FileNotFoundError, IOError):
        pass
    return destinations


def load_itineraries():
    itineraries = []
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    except (FileNotFoundError, IOError):
        pass
    return itineraries


def load_hotels():
    hotels = []
    path = os.path.join(DATA_DIR, 'hotels.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                try:
                    hotel = {
                        'hotel_id': int(parts[0]),
                        'name': parts[1],
                        'city': parts[2],
                        'rating': float(parts[3]),
                        'price_per_night': float(parts[4]),
                        'amenities': parts[5],
                        'category': parts[6]
                    }
                except ValueError:
                    continue
                hotels.append(hotel)
    except (FileNotFoundError, IOError):
        pass
    return hotels


def load_flights():
    flights = []
    path = os.path.join(DATA_DIR, 'flights.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                except ValueError:
                    continue
                flights.append(flight)
    except (FileNotFoundError, IOError):
        pass
    return flights


def load_packages():
    packages = []
    path = os.path.join(DATA_DIR, 'packages.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                except ValueError:
                    continue
                packages.append(package)
    except (FileNotFoundError, IOError):
        pass
    return packages


def load_trips():
    trips = []
    path = os.path.join(DATA_DIR, 'trips.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                except ValueError:
                    continue
                trips.append(trip)
    except (FileNotFoundError, IOError):
        pass
    return trips


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
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
                except ValueError:
                    continue
                bookings.append(booking)
    except (FileNotFoundError, IOError):
        pass
    return bookings


# Routes Implementation

@app.route('/')
def dashboard():
    # featured_destinations:
    # Only keys needed: dest_id, name, country
    destinations = load_destinations()
    featured_destinations = [{
        'dest_id': d['dest_id'],
        'name': d['name'],
        'country': d['country']
    } for d in destinations]

    # upcoming_trips with keys (trip_id, trip_name, start_date, end_date)
    trips = load_trips()
    upcoming_trips = [{
        'trip_id': t['trip_id'],
        'trip_name': t['trip_name'],
        'start_date': t['start_date'],
        'end_date': t['end_date']
    } for t in trips]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations_data = load_destinations()
    # Context variables: destinations and region_options
    return render_template('destinations.html', destinations=destinations_data, region_options=REGION_OPTIONS)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_data = load_destinations()
    destination = next((d for d in destinations_data if d['dest_id'] == dest_id), None)
    if not destination:
        return "Destination not found", 404

    if request.method == 'POST':
        # Action: add destination to trip
        # No further detail specified for data processing - just acknowledge here
        # Normally this would handle form data and redirect or respond accordingly
        return redirect(url_for('destination_details', dest_id=dest_id))

    # context variable 'destination' with keys as specified
    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_list = load_itineraries()
    if request.method == 'POST':
        # Add activity button POST handling - no detail specified
        # Just redirect to same page for now
        return redirect(url_for('itinerary'))

    return render_template('itinerary.html', itineraries=itineraries_list)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels_list = load_hotels()
    if request.method == 'POST':
        # No detailed form requirements given
        return redirect(url_for('accommodations'))

    return render_template('accommodations.html', hotels=hotels_list)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights_list = load_flights()
    if request.method == 'POST':
        # No detailed form requirements given
        return redirect(url_for('transportation'))

    return render_template('transportation.html', flights=flights_list)


@app.route('/packages')
def packages():
    packages_list = load_packages()
    return render_template('packages.html', packages=packages_list)


@app.route('/trips')
def trips():
    trips_list = load_trips()
    return render_template('trips.html', trips=trips_list)


@app.route('/booking-confirmation/<int:trip_id>')
def booking_confirmation(trip_id):
    bookings_list = load_bookings()
    booking = next((b for b in bookings_list if b['trip_id'] == trip_id), None)
    if not booking:
        return "Booking not found", 404
    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    destinations_data = load_destinations()
    # trending_destinations: keys (dest_id, name, country, popularity_rank)
    # popularity_rank not in original data, simulate by sorting by dest_id ascending and rank by index + 1
    sorted_dest = sorted(destinations_data, key=lambda d: d['dest_id'])
    trending_destinations = []
    for i, d in enumerate(sorted_dest):
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'popularity_rank': i + 1
        })

    return render_template('recommendations.html', trending_destinations=trending_destinations, recommendation_seasons=RECOMMENDATION_SEASONS, budget_ranges=BUDGET_RANGES)


if __name__ == '__main__':
    app.run(debug=True)
