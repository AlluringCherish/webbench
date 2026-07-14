from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Helper functions to load and save data

def load_destinations():
    destinations = []
    path = os.path.join(DATA_DIR, 'destinations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # dest_id|name|country|region|description|attractions|climate
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


def load_itineraries():
    itineraries = []
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
                    itn = {
                        'itinerary_id': int(parts[0]),
                        'itinerary_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'activities': parts[5],
                        'status': parts[6],
                    }
                    itineraries.append(itn)
    return itineraries


def save_itineraries(itineraries):
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for itn in itineraries:
            line = f"{itn['itinerary_id']}|{itn['itinerary_name']}|{itn['destination']}|{itn['start_date']}|{itn['end_date']}|{itn['activities']}|{itn['status']}\n"
            f.write(line)


def load_hotels():
    hotels = []
    path = os.path.join(DATA_DIR, 'hotels.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # hotel_id|name|city|rating|price_per_night|amenities|category
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


def load_flights():
    flights = []
    path = os.path.join(DATA_DIR, 'flights.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
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


def load_packages():
    packages = []
    path = os.path.join(DATA_DIR, 'packages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # package_id|package_name|destination|duration_days|price|included_items|difficulty_level
                    pkg = {
                        'package_id': int(parts[0]),
                        'package_name': parts[1],
                        'destination': parts[2],
                        'duration_days': int(parts[3]),
                        'price': float(parts[4]),
                        'included_items': parts[5],
                        'difficulty_level': parts[6],
                    }
                    packages.append(pkg)
    return packages


def load_trips():
    trips = []
    path = os.path.join(DATA_DIR, 'trips.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
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


def save_trips(trips):
    path = os.path.join(DATA_DIR, 'trips.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for t in trips:
            line = f"{t['trip_id']}|{t['trip_name']}|{t['destination']}|{t['start_date']}|{t['end_date']}|{t['total_budget']}|{t['status']}|{t['created_date']}\n"
            f.write(line)


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    # booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
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

# Route: / and /dashboard (GET) - Render Dashboard page
@app.route('/')
@app.route('/dashboard')
def dashboard():
    destinations = load_destinations()[:3]  # top 3 featured
    trips = load_trips()[:3]  # upcoming trips (simplified)
    return render_template('dashboard.html',
                           destinations=destinations,
                           trips=trips)

# Route: /destinations (GET, POST)
@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = load_destinations()
    filtered = destinations
    search_query = ''
    region_filter = ''
    if request.method == 'POST':
        search_query = request.form.get('search_destination', '').strip().lower()
        region_filter = request.form.get('region_filter', '')
        if search_query:
            filtered = [d for d in filtered if search_query in d['name'].lower()]
        if region_filter:
            filtered = [d for d in filtered if d['region'] == region_filter]
    regions = sorted({d['region'] for d in destinations})
    return render_template('destinations.html', destinations=filtered, search_query=search_query, region_filter=region_filter, regions=regions)

# Route: /destination/<int:dest_id> (GET, POST)
@app.route('/destination/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = load_destinations()
    dest = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not dest:
        return "Destination not found", 404
    message = ''
    if request.method == 'POST':
        # Add to trip action
        trip_name = request.form.get('trip_name', 'Unnamed Trip')
        itineraries = load_itineraries()
        new_id = max([itn['itinerary_id'] for itn in itineraries] or [0]) + 1
        new_itinerary = {
            'itinerary_id': new_id,
            'itinerary_name': trip_name,
            'destination': dest['name'],
            'start_date': '',
            'end_date': '',
            'activities': '',
            'status': 'Planned'
        }
        itineraries.append(new_itinerary)
        save_itineraries(itineraries)
        message = f"Destination added to itinerary '{trip_name}'."
    return render_template('destination_details.html', destination=dest, message=message)

# Route: /itinerary (GET, POST)
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = load_itineraries()
    message = ''
    if request.method == 'POST':
        itinerary_name = request.form.get('itinerary_name_input', '').strip()
        start_date = request.form.get('start_date_input', '')
        end_date = request.form.get('end_date_input', '')
        add_activity = request.form.get('add_activity', '')

        # For simplicity, add new itinerary if name present
        if itinerary_name:
            new_id = max([itn['itinerary_id'] for itn in itineraries] or [0]) + 1
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
            save_itineraries(itineraries)
            message = f"Itinerary '{itinerary_name}' created."

    return render_template('itinerary.html', itineraries=itineraries, message=message)

# Route: /accommodations (GET, POST)
@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = load_hotels()
    filtered = hotels
    destination_input = ''
    check_in_date = ''
    check_out_date = ''
    price_filter = ''

    if request.method == 'POST':
        destination_input = request.form.get('destination_input', '').strip().lower()
        check_in_date = request.form.get('check_in_date', '')
        check_out_date = request.form.get('check_out_date', '')
        price_filter = request.form.get('price_filter', '')

        if destination_input:
            filtered = [h for h in filtered if h['city'].lower() == destination_input]

        if price_filter:
            try:
                max_price = float(price_filter)
                filtered = [h for h in filtered if h['price_per_night'] <= max_price]
            except ValueError:
                pass

    return render_template('accommodations.html', hotels=filtered, destination_input=destination_input,
                           check_in_date=check_in_date, check_out_date=check_out_date, price_filter=price_filter)

# Route: /transportation (GET, POST)
@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = load_flights()
    filtered = flights
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    flight_class_filter = ''

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').strip().lower()
        arrival_city = request.form.get('arrival_city', '').strip().lower()
        departure_date = request.form.get('departure_date', '')
        flight_class_filter = request.form.get('flight_class_filter', '')

        if departure_city:
            filtered = [f for f in filtered if f['departure_city'].lower() == departure_city]
        if arrival_city:
            filtered = [f for f in filtered if f['arrival_city'].lower() == arrival_city]
        if flight_class_filter:
            filtered = [f for f in filtered if f['class_type'] == flight_class_filter]

    return render_template('transportation.html', flights=filtered, departure_city=departure_city,
                           arrival_city=arrival_city, departure_date=departure_date, flight_class_filter=flight_class_filter)

# Route: /packages (GET, POST)
@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages = load_packages()
    filtered = packages
    duration_filter = ''
    message = ''

    if request.method == 'POST':
        duration_filter = request.form.get('duration_filter', '')
        book_pkg_id = request.form.get('book_package_id', '')

        if duration_filter:
            try:
                dur = int(duration_filter)
                filtered = [p for p in filtered if p['duration_days'] == dur]
            except ValueError:
                pass
        if book_pkg_id:
            # Redirect to booking route
            return redirect(url_for('book_package', pkg_id=int(book_pkg_id)))

    return render_template('packages.html', packages=filtered, duration_filter=duration_filter, message=message)

# Route: /packages/<int:pkg_id> (GET)
@app.route('/packages/<int:pkg_id>')
def package_details(pkg_id):
    packages = load_packages()
    pkg = next((p for p in packages if p['package_id'] == pkg_id), None)
    if not pkg:
        return "Package not found", 404
    return render_template('package_details.html', package=pkg)

# Route: /packages/<int:pkg_id>/book (POST)
@app.route('/packages/<int:pkg_id>/book', methods=['POST'])
def book_package(pkg_id):
    trips = load_trips()
    bookings = load_bookings()
    new_booking_id = max([b['booking_id'] for b in bookings] or [0]) + 1
    trip_id = request.form.get('trip_id', type=int)

    if not trip_id or not any(t['trip_id'] == trip_id for t in trips):
        return "Invalid trip selection", 400

    booking_date = datetime.now().strftime('%Y-%m-%d')
    amount = 0.0
    packages = load_packages()
    pkg = next((p for p in packages if p['package_id'] == pkg_id), None)
    if pkg:
        amount = pkg['price']

    confirmation_number = f"CONF{new_booking_id:03d}"
    new_booking = {
        'booking_id': new_booking_id,
        'trip_id': trip_id,
        'booking_type': 'Package',
        'booking_date': booking_date,
        'amount': amount,
        'confirmation_number': confirmation_number,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)

    # Save bookings
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['trip_id']}|{b['booking_type']}|{b['booking_date']}|{b['amount']}|{b['confirmation_number']}|{b['status']}\n"
            f.write(line)
    return redirect(url_for('booking_confirmation', confirmation_number=confirmation_number))

# Route: /trips (GET, POST)
@app.route('/trips', methods=['GET', 'POST'])
def trips_page():
    trips = load_trips()
    message = ''
    if request.method == 'POST':
        action = request.form.get('action', '')
        trip_id = request.form.get('trip_id', type=int)

        if action == 'edit' and trip_id:
            trips_list = [t for t in trips if t['trip_id'] != trip_id]
            # Edit logic placeholder - simplified: change trip name
            new_name = request.form.get('trip_name', '')
            for t in trips:
                if t['trip_id'] == trip_id:
                    t['trip_name'] = new_name
            save_trips(trips)
            message = f"Trip {trip_id} updated."

        elif action == 'delete' and trip_id:
            trips = [t for t in trips if t['trip_id'] != trip_id]
            save_trips(trips)
            message = f"Trip {trip_id} deleted."

    return render_template('trips.html', trips=trips, message=message)

# Route: /trips/<int:trip_id> (GET)
@app.route('/trips/<int:trip_id>')
def trip_details(trip_id):
    trips = load_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        return "Trip not found", 404
    return render_template('trip_details.html', trip=trip)

# Route: /booking-confirmation (GET)
@app.route('/booking-confirmation')
def booking_confirmation():
    confirmation_number = request.args.get('confirmation_number')
    bookings = load_bookings()
    booking = next((b for b in bookings if b['confirmation_number'] == confirmation_number), None)
    if not booking:
        return "Booking not found", 404
    trips = load_trips()
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html', booking=booking, trip=trip)

# Route: /recommendations (GET, POST)
@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    destinations = load_destinations()
    trending_destinations = destinations[:5]  # Simplified
    season_filter = ''
    budget_filter = ''
    filtered = destinations
    if request.method == 'POST':
        season_filter = request.form.get('recommendation_season_filter', '')
        budget_filter = request.form.get('budget_filter', '')
        # Simplified filter by budget and season
        if budget_filter:
            try:
                budget_num = float(budget_filter)
                filtered = [d for d in filtered if len(d['description']) < budget_num*10]
            except ValueError:
                pass
        if season_filter:
            filtered = [d for d in filtered if season_filter.lower() in d['climate'].lower()]
    return render_template('recommendations.html',
                           destinations=filtered, trending_destinations=trending_destinations,
                           season_filter=season_filter, budget_filter=budget_filter)

if __name__ == '__main__':
    app.run(debug=True)
