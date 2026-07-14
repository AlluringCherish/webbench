from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to read/write data files

def read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return lines

def write_file_lines(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Read data entity lists

def read_destinations():
    data = read_file_lines('destinations.txt')
    destinations = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        dest = {
            'dest_id': int(parts[0]),
            'name': parts[1],
            'country': parts[2],
            'region': parts[3],
            'description': parts[4],
            'attractions': parts[5],
            'climate': parts[6],
        }
        destinations.append(dest)
    return destinations


def read_itineraries():
    data = read_file_lines('itineraries.txt')
    itineraries = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        it = {
            'itinerary_id': int(parts[0]),
            'itinerary_name': parts[1],
            'destination': parts[2],
            'start_date': parts[3],
            'end_date': parts[4],
            'activities': parts[5],
            'status': parts[6],
        }
        itineraries.append(it)
    return itineraries


def write_itineraries(itineraries):
    lines = []
    for it in itineraries:
        lines.append(f"{it['itinerary_id']}|{it['itinerary_name']}|{it['destination']}|{it['start_date']}|{it['end_date']}|{it['activities']}|{it['status']}")
    write_file_lines('itineraries.txt', lines)


def read_hotels():
    data = read_file_lines('hotels.txt')
    hotels = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        hotel = {
            'hotel_id': int(parts[0]),
            'name': parts[1],
            'city': parts[2],
            'rating': float(parts[3]),
            'price_per_night': float(parts[4]),
            'amenities': parts[5],
            'category': parts[6],
        }
        hotels.append(hotel)
    return hotels


def read_flights():
    data = read_file_lines('flights.txt')
    flights = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
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
            'duration': parts[8],
        }
        flights.append(flight)
    return flights


def read_packages():
    data = read_file_lines('packages.txt')
    packages = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        package = {
            'package_id': int(parts[0]),
            'package_name': parts[1],
            'destination': parts[2],
            'duration_days': int(parts[3]),
            'price': float(parts[4]),
            'included_items': parts[5],
            'difficulty_level': parts[6],
        }
        packages.append(package)
    return packages


def read_trips():
    data = read_file_lines('trips.txt')
    trips = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
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
            'created_date': parts[7],
        }
        trips.append(trip)
    return trips


def write_trips(trips):
    lines = []
    for trip in trips:
        lines.append(f"{trip['trip_id']}|{trip['trip_name']}|{trip['destination']}|{trip['start_date']}|{trip['end_date']}|{trip['total_budget']:.2f}|{trip['status']}|{trip['created_date']}")
    write_file_lines('trips.txt', lines)


def read_bookings():
    data = read_file_lines('bookings.txt')
    bookings = []
    for line in data:
        if not line.strip():
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        booking = {
            'booking_id': int(parts[0]),
            'trip_id': int(parts[1]),
            'booking_type': parts[2],
            'booking_date': parts[3],
            'amount': float(parts[4]),
            'confirmation_number': parts[5],
            'status': parts[6],
        }
        bookings.append(booking)
    return bookings

# Utility functions

def next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # For demo, show featured destinations (first 3) and upcoming trips
    destinations = read_destinations()
    featured_destinations = destinations[:3]
    trips = read_trips()
    # Upcoming trips: trips with start_date >= today sorted by start_date
    today = datetime.now().date()
    upcoming_trips = [trip for trip in trips if datetime.strptime(trip['start_date'], '%Y-%m-%d').date() >= today]
    upcoming_trips.sort(key=lambda x: x['start_date'])
    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = read_destinations()
    search_term = ''
    region_filter = ''

    if request.method == 'POST':
        search_term = request.form.get('search-destination', '').strip().lower()
        region_filter = request.form.get('region-filter', '')

    filtered = destinations

    if search_term:
        filtered = [d for d in filtered if search_term in d['name'].lower()]
    if region_filter:
        filtered = [d for d in filtered if d['region'] == region_filter]

    # Get unique regions for dropdown
    regions = sorted(set(d['region'] for d in destinations))

    return render_template('destinations.html',
                           destinations=filtered,
                           search_term=search_term,
                           region_filter=region_filter,
                           regions=regions)

@app.route('/destination/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = read_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        return "Destination not found", 404

    if request.method == 'POST':
        # Add destination to a trip (create if needed)
        trip_name = request.form.get('trip_name', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        if trip_name and start_date and end_date:
            trips = read_trips()
            trip_id = next_id(trips, 'trip_id')
            new_trip = {
                'trip_id': trip_id,
                'trip_name': trip_name,
                'destination': destination['name'],
                'start_date': start_date,
                'end_date': end_date,
                'total_budget': 0.0,
                'status': 'Planned',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
            }
            trips.append(new_trip)
            write_trips(trips)
            return redirect(url_for('trips'))

    return render_template('destination_details.html', destination=destination)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = read_itineraries()

    if request.method == 'POST':
        itinerary_name = request.form.get('itinerary-name-input', '').strip()
        start_date = request.form.get('start-date-input', '')
        end_date = request.form.get('end-date-input', '')
        add_activity = request.form.get('add-activity-input', '').strip()

        # Create new itinerary or update existing
        if itinerary_name and start_date and end_date:
            # Check existing by name
            existing = next((it for it in itineraries if it['itinerary_name'] == itinerary_name), None)
            if existing:
                # Update
                if add_activity:
                    if existing['activities']:
                        existing['activities'] += ', ' + add_activity
                    else:
                        existing['activities'] = add_activity
                existing['start_date'] = start_date
                existing['end_date'] = end_date
            else:
                new_id = next_id(itineraries, 'itinerary_id')
                new_itinerary = {
                    'itinerary_id': new_id,
                    'itinerary_name': itinerary_name,
                    'destination': '',
                    'start_date': start_date,
                    'end_date': end_date,
                    'activities': add_activity,
                    'status': 'Planned'
                }
                itineraries.append(new_itinerary)
            write_itineraries(itineraries)
        return redirect(url_for('itinerary'))

    return render_template('itinerary.html', itineraries=itineraries)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = read_hotels()
    destination = ''
    check_in = ''
    check_out = ''
    price_filter = ''

    if request.method == 'POST':
        destination = request.form.get('destination-input', '').strip()
        check_in = request.form.get('check-in-date', '')
        check_out = request.form.get('check-out-date', '')
        price_filter = request.form.get('price-filter', '')  # Expecting categories

    filtered_hotels = hotels
    if destination:
        filtered_hotels = [h for h in filtered_hotels if h['city'].lower() == destination.lower()]
    if price_filter:
        # price_filter might be e.g. '<100', '100-200', '>200' for demo
        if price_filter == '<100':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] < 100]
        elif price_filter == '100-200':
            filtered_hotels = [h for h in filtered_hotels if 100 <= h['price_per_night'] <= 200]
        elif price_filter == '>200':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] > 200]

    return render_template('accommodations.html', hotels=filtered_hotels, destination=destination, check_in=check_in, check_out=check_out, price_filter=price_filter)

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = read_flights()
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    flight_class_filter = ''

    if request.method == 'POST':
        departure_city = request.form.get('departure-city', '').strip()
        arrival_city = request.form.get('arrival-city', '').strip()
        departure_date = request.form.get('departure-date', '')
        flight_class_filter = request.form.get('flight-class-filter', '')

    filtered_flights = flights
    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city.lower()]
    if flight_class_filter:
        filtered_flights = [f for f in filtered_flights if f['class_type'] == flight_class_filter]

    # Note: No filtering by departure_date in example data or spec

    return render_template('transportation.html', flights=filtered_flights, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date, flight_class_filter=flight_class_filter)

@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages_list = read_packages()
    duration_filter = ''

    if request.method == 'POST':
        duration_filter = request.form.get('duration-filter', '')

    filtered_packages = packages_list
    if duration_filter:
        try:
            duration_days = int(duration_filter)
            filtered_packages = [p for p in filtered_packages if p['duration_days'] == duration_days]
        except ValueError:
            filtered_packages = packages_list

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter)

@app.route('/packages/<int:pkg_id>', methods=['GET'])
def package_details(pkg_id):
    packages_list = read_packages()
    package = next((p for p in packages_list if p['package_id'] == pkg_id), None)
    if not package:
        return "Package not found", 404
    return render_template('package_details.html', package=package)

@app.route('/packages/<int:pkg_id>/book', methods=['POST'])
def book_package(pkg_id):
    packages_list = read_packages()
    package = next((p for p in packages_list if p['package_id'] == pkg_id), None)
    if not package:
        return "Package not found", 404
    # For demo purpose, create a new trip and a booking
    trip_name = request.form.get('trip_name', f"Trip for {package['package_name']}")
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')
    if not (trip_name and start_date and end_date):
        return "Missing booking details", 400

    trips = read_trips()
    trip_id = next_id(trips, 'trip_id')
    new_trip = {
        'trip_id': trip_id,
        'trip_name': trip_name,
        'destination': package['destination'],
        'start_date': start_date,
        'end_date': end_date,
        'total_budget': package['price'],
        'status': 'Booked',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
    }
    trips.append(new_trip)
    write_trips(trips)

    bookings = read_bookings()
    booking_id = next_id(bookings, 'booking_id')
    new_booking = {
        'booking_id': booking_id,
        'trip_id': trip_id,
        'booking_type': 'Package',
        'booking_date': datetime.now().strftime('%Y-%m-%d'),
        'amount': package['price'],
        'confirmation_number': f"CONF{booking_id:03d}",
        'status': 'Confirmed'
    }
    bookings.append(new_booking)
    # Write bookings to file
    lines = []
    for b in bookings:
        lines.append(f"{b['booking_id']}|{b['trip_id']}|{b['booking_type']}|{b['booking_date']}|{b['amount']:.2f}|{b['confirmation_number']}|{b['status']}")
    write_file_lines('bookings.txt', lines)

    return redirect(url_for('booking_confirmation', confirmation_number=new_booking['confirmation_number']))

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_list = read_trips()

    if request.method == 'POST':
        action = request.form.get('action')
        trip_id = int(request.form.get('trip_id', 0))

        if action == 'delete':
            trips_list = [t for t in trips_list if t['trip_id'] != trip_id]
            write_trips(trips_list)
        elif action == 'edit':
            # For simplicity, simulate edit by updating name and status
            new_name = request.form.get('trip_name', '').strip()
            new_status = request.form.get('trip_status', '').strip()
            for t in trips_list:
                if t['trip_id'] == trip_id:
                    if new_name:
                        t['trip_name'] = new_name
                    if new_status:
                        t['status'] = new_status
                    break
            write_trips(trips_list)

        return redirect(url_for('trips'))

    return render_template('trips.html', trips=trips_list)

@app.route('/trips/<int:trip_id>', methods=['GET'])
def trip_details(trip_id):
    trips_list = read_trips()
    trip = next((t for t in trips_list if t['trip_id'] == trip_id), None)
    if not trip:
        return "Trip not found", 404
    bookings = read_bookings()
    trip_bookings = [b for b in bookings if b['trip_id'] == trip_id]
    return render_template('trip_details.html', trip=trip, bookings=trip_bookings)

@app.route('/booking-confirmation', methods=['GET'])
def booking_confirmation():
    confirmation_number = request.args.get('confirmation_number', '')
    bookings = read_bookings()
    booking = next((b for b in bookings if b['confirmation_number'] == confirmation_number), None)
    if not booking:
        return "Booking not found", 404
    trips_list = read_trips()
    trip = next((t for t in trips_list if t['trip_id'] == booking['trip_id']), None)

    return render_template('booking_confirmation.html', booking=booking, trip=trip)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    destinations = read_destinations()
    season_filter = ''
    budget_filter = ''

    if request.method == 'POST':
        season_filter = request.form.get('recommendation-season-filter', '')
        budget_filter = request.form.get('budget-filter', '')

    filtered_destinations = destinations

    # Simple filters: climate matches season, and price filter on packages
    if season_filter:
        filtered_destinations = [d for d in filtered_destinations if season_filter.lower() in d['climate'].lower()]

    if budget_filter:
        try:
            budget_limit = float(budget_filter)
            packages_list = read_packages()
            affordable_dest_ids = {p['destination'] for p in packages_list if p['price'] <= budget_limit}
            filtered_destinations = [d for d in filtered_destinations if d['name'] in affordable_dest_ids]
        except ValueError:
            pass

    return render_template('recommendations.html',
                           destinations=filtered_destinations,
                           season_filter=season_filter,
                           budget_filter=budget_filter)

if __name__ == '__main__':
    app.run(debug=True)
