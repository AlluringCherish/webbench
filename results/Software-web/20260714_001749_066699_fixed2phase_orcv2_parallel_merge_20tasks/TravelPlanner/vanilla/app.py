from flask import Flask, render_template, request, redirect, url_for, abort
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Utility functions for parsing and loading data

def load_pipe_delimited_file(filename, fieldnames):
    '''Load a pipe-delimited file and return a list of dicts with given fieldnames.'''
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().splitlines()
    data = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < len(fieldnames):
            continue  # skip malformed lines
        item = {}
        for i, field in enumerate(fieldnames):
            item[field] = parts[i]
        data.append(item)
    return data


def save_pipe_delimited_file(filename, fieldnames, records):
    '''Save list of dict records to pipe-delimited file.'''
    filepath = os.path.join(DATA_DIR, filename)
    lines = []
    for rec in records:
        parts = [str(rec.get(field, '')) for field in fieldnames]
        lines.append('|'.join(parts))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# Loading individual data

def load_destinations():
    fieldnames = ['dest_id', 'name', 'country', 'region', 'description', 'attractions', 'climate']
    raw_data = load_pipe_delimited_file('destinations.txt', fieldnames)
    # Convert dest_id to int
    for d in raw_data:
        d['dest_id'] = int(d['dest_id'])
    return raw_data


def load_itineraries():
    fieldnames = ['itinerary_id', 'itinerary_name', 'destination', 'start_date', 'end_date', 'activities', 'status']
    raw_data = load_pipe_delimited_file('itineraries.txt', fieldnames)
    for it in raw_data:
        it['itinerary_id'] = int(it['itinerary_id'])
    return raw_data


def save_itineraries(itineraries):
    fieldnames = ['itinerary_id', 'itinerary_name', 'destination', 'start_date', 'end_date', 'activities', 'status']
    save_pipe_delimited_file('itineraries.txt', fieldnames, itineraries)


def load_hotels():
    fieldnames = ['hotel_id', 'name', 'city', 'rating', 'price_per_night', 'amenities', 'category']
    raw_data = load_pipe_delimited_file('hotels.txt', fieldnames)
    for h in raw_data:
        h['hotel_id'] = int(h['hotel_id'])
        h['rating'] = float(h['rating'])
        h['price_per_night'] = float(h['price_per_night'])
    return raw_data


def load_flights():
    fieldnames = ['flight_id', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price', 'class_type', 'duration']
    raw_data = load_pipe_delimited_file('flights.txt', fieldnames)
    for f in raw_data:
        f['flight_id'] = int(f['flight_id'])
        f['price'] = float(f['price'])
    return raw_data


def load_packages():
    fieldnames = ['package_id', 'package_name', 'destination', 'duration_days', 'price', 'included_items', 'difficulty_level']
    raw_data = load_pipe_delimited_file('packages.txt', fieldnames)
    for p in raw_data:
        p['package_id'] = int(p['package_id'])
        p['duration_days'] = int(p['duration_days'])
        p['price'] = float(p['price'])
    return raw_data


def load_trips():
    fieldnames = ['trip_id', 'trip_name', 'destination', 'start_date', 'end_date', 'total_budget', 'status', 'created_date']
    raw_data = load_pipe_delimited_file('trips.txt', fieldnames)
    for t in raw_data:
        t['trip_id'] = int(t['trip_id'])
        t['total_budget'] = float(t['total_budget'])
    return raw_data


def save_trips(trips):
    fieldnames = ['trip_id', 'trip_name', 'destination', 'start_date', 'end_date', 'total_budget', 'status', 'created_date']
    save_pipe_delimited_file('trips.txt', fieldnames, trips)


def load_bookings():
    fieldnames = ['booking_id', 'trip_id', 'booking_type', 'booking_date', 'amount', 'confirmation_number', 'status']
    raw_data = load_pipe_delimited_file('bookings.txt', fieldnames)
    for b in raw_data:
        b['booking_id'] = int(b['booking_id'])
        b['trip_id'] = int(b['trip_id'])
        b['amount'] = float(b['amount'])
    return raw_data


def save_bookings(bookings):
    fieldnames = ['booking_id', 'trip_id', 'booking_type', 'booking_date', 'amount', 'confirmation_number', 'status']
    save_pipe_delimited_file('bookings.txt', fieldnames, bookings)


# Helper functions

def get_destination_by_id(dest_id):
    destinations = load_destinations()
    for d in destinations:
        if d['dest_id'] == dest_id:
            return d
    return None


def get_itinerary_by_id(itinerary_id):
    itineraries = load_itineraries()
    for it in itineraries:
        if it['itinerary_id'] == itinerary_id:
            return it
    return None


def get_package_by_id(package_id):
    packages = load_packages()
    for p in packages:
        if p['package_id'] == package_id:
            return p
    return None


def get_trip_by_id(trip_id):
    trips = load_trips()
    for t in trips:
        if t['trip_id'] == trip_id:
            return t
    return None


def get_booking_by_confirmation(confirmation_number):
    bookings = load_bookings()
    for b in bookings:
        if b['confirmation_number'] == confirmation_number:
            return b
    return None


# Routes Implementation

@app.route('/')
@app.route('/dashboard')
def dashboard():
    '''Display main dashboard with featured destinations and upcoming trips.'''
    destinations = load_destinations()
    # For demonstration, featured destinations can be first 5
    featured_destinations = destinations[:5]

    # Upcoming trips: trips with start_date >= today and status Planned or In Progress or Booked
    trips = load_trips()
    today_str = datetime.now().strftime('%Y-%m-%d')
    def upcoming_trip_filter(trip):
        return trip['status'] in ['Planned', 'In Progress', 'Booked'] and trip['start_date'] >= today_str
    upcoming_trips = [trip for trip in trips if upcoming_trip_filter(trip)]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def list_destinations():
    '''List destinations with optional search and region filter.'''
    search_query = request.args.get('search_query', '').strip()
    region_filter = request.args.get('region_filter', '').strip()

    destinations = load_destinations()

    if search_query:
        search_lower = search_query.lower()
        destinations = [d for d in destinations if search_lower in d['name'].lower() or search_lower in d['country'].lower()]

    if region_filter and region_filter in ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']:
        destinations = [d for d in destinations if d['region'] == region_filter]

    return render_template('destinations.html', destinations=destinations, search_query=search_query, region_filter=region_filter)


@app.route('/destinations/<int:dest_id>')
def destination_details(dest_id):
    '''Show detailed info for a destination.'''
    destination = get_destination_by_id(dest_id)
    if not destination:
        abort(404)
    return render_template('destination_details.html', destination=destination)


@app.route('/destinations/<int:dest_id>/add-to-trip', methods=['POST'])
def add_destination_to_trip(dest_id):
    '''Add destination to a user's upcoming trip or itinerary. For simplicity, we add a new trip with this destination.'''
    destination = get_destination_by_id(dest_id)
    if not destination:
        abort(404)

    trips = load_trips()

    # For example, add as a new planned trip with default dates 7 days from today for duration 7 days
    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d')
    end_date = (today.replace(day=today.day + 7) if today.day <= 24 else today).strftime('%Y-%m-%d')  # naive day add

    # Generate a new trip_id
    max_id = max([trip['trip_id'] for trip in trips], default=0)
    new_trip = {
        'trip_id': max_id + 1,
        'trip_name': f"Trip to {destination['name']}",
        'destination': destination['name'],
        'start_date': start_date,
        'end_date': end_date,
        'total_budget': 0.0,
        'status': 'Planned',
        'created_date': today.strftime('%Y-%m-%d'),
    }
    trips.append(new_trip)
    save_trips(trips)

    return redirect(url_for('destination_details', dest_id=dest_id))


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    '''View and manage itineraries.'''
    if request.method == 'POST':
        # Create new itinerary
        itinerary_name = request.form.get('itinerary_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()

        if itinerary_name and destination and start_date and end_date:
            itineraries = load_itineraries()
            max_id = max([it['itinerary_id'] for it in itineraries], default=0)
            new_itinerary = {
                'itinerary_id': max_id + 1,
                'itinerary_name': itinerary_name,
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'activities': '',
                'status': 'Planned'
            }
            itineraries.append(new_itinerary)
            save_itineraries(itineraries)
            return redirect(url_for('itinerary'))

        # Could add activities handling via form or AJAX if specified (not implemented here)

    itineraries = load_itineraries()
    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/itinerary/<int:itinerary_id>/edit', methods=['GET', 'POST'])
def edit_itinerary(itinerary_id):
    '''Edit itinerary details and activities.'''
    itinerary = get_itinerary_by_id(itinerary_id)
    if not itinerary:
        abort(404)

    if request.method == 'POST':
        # Update itinerary from form
        itinerary_name = request.form.get('itinerary_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        activities = request.form.get('activities', '').strip()
        status = request.form.get('status', '').strip()

        if itinerary_name and destination and start_date and end_date and status:
            itineraries = load_itineraries()
            for it in itineraries:
                if it['itinerary_id'] == itinerary_id:
                    it['itinerary_name'] = itinerary_name
                    it['destination'] = destination
                    it['start_date'] = start_date
                    it['end_date'] = end_date
                    it['activities'] = activities
                    it['status'] = status
                    break
            save_itineraries(itineraries)
            return redirect(url_for('itinerary'))

    # GET display
    return render_template('edit_itinerary.html', itinerary=itinerary)


@app.route('/itinerary/<int:itinerary_id>/delete', methods=['POST'])
def delete_itinerary(itinerary_id):
    '''Delete an itinerary.'''
    itineraries = load_itineraries()
    itineraries = [it for it in itineraries if it['itinerary_id'] != itinerary_id]
    save_itineraries(itineraries)
    return redirect(url_for('itinerary'))


@app.route('/accommodations')
def search_accommodations():
    '''Search and browse hotels with filters city, price range.'''
    destination = request.args.get('destination', '').strip()
    check_in_date = request.args.get('check_in_date', '').strip()
    check_out_date = request.args.get('check_out_date', '').strip()
    price_filter = request.args.get('price_filter', '').strip()  # Budget, Mid-range, Luxury

    hotels = load_hotels()

    if destination:
        hotels = [h for h in hotels if h['city'].lower() == destination.lower()]
    if price_filter and price_filter in ['Budget', 'Mid-range', 'Luxury']:
        hotels = [h for h in hotels if h['category'] == price_filter]

    # We do not handle real date availability as no such data provided

    return render_template('accommodations.html', hotels=hotels, destination=destination,
                           check_in_date=check_in_date, check_out_date=check_out_date, price_filter=price_filter)


@app.route('/flights')
def search_flights():
    '''Search and display available flights.'''
    departure_city = request.args.get('departure_city', '').strip()
    arrival_city = request.args.get('arrival_city', '').strip()
    departure_date = request.args.get('departure_date', '').strip()
    flight_class = request.args.get('flight_class', '').strip()  # Economy, Business, First Class

    flights = load_flights()

    if departure_city:
        flights = [f for f in flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        flights = [f for f in flights if f['arrival_city'].lower() == arrival_city.lower()]
    if flight_class and flight_class in ['Economy', 'Business', 'First Class']:
        flights = [f for f in flights if f['class_type'] == flight_class]

    # No filtering by departure_date because flights.txt has no date info

    return render_template('flights.html', flights=flights, departure_city=departure_city,
                           arrival_city=arrival_city, departure_date=departure_date, flight_class=flight_class)


@app.route('/packages')
def list_packages():
    '''List travel packages filtered by duration.'''
    duration_filter = request.args.get('duration_filter', '').strip()  # 3-5 days, 7-10 days, 14+ days
    packages = load_packages()

    if duration_filter:
        def duration_match(p):
            days = p['duration_days']
            if duration_filter == '3-5 days':
                return 3 <= days <= 5
            elif duration_filter == '7-10 days':
                return 7 <= days <= 10
            elif duration_filter == '14+ days':
                return days >= 14
            return False

        packages = [p for p in packages if duration_match(p)]

    return render_template('packages.html', packages=packages, duration_filter=duration_filter)


@app.route('/packages/<int:package_id>')
def package_details(package_id):
    '''Show package details.'''
    package = get_package_by_id(package_id)
    if not package:
        abort(404)
    return render_template('package_details.html', package=package)


@app.route('/packages/<int:package_id>/book', methods=['POST'])
def book_package(package_id):
    '''Create a booking for selected package.'''
    package = get_package_by_id(package_id)
    if not package:
        abort(404)

    # Simplified booking logic:
    trips = load_trips()
    # For demo, link booking to first trip if any
    if not trips:
        return "No trips available to book package for.", 400

    trip = trips[0]

    bookings = load_bookings()
    max_id = max([b['booking_id'] for b in bookings], default=0)

    # Generate a confirmation number as e.g. PKG + booking_id
    confirmation_number = f"PKG{max_id + 1:03d}"

    today_str = datetime.now().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': max_id + 1,
        'trip_id': trip['trip_id'],
        'booking_type': 'Package',
        'booking_date': today_str,
        'amount': package['price'],
        'confirmation_number': confirmation_number,
        'status': 'Confirmed'
    }
    bookings.append(new_booking)
    save_bookings(bookings)

    return redirect(url_for('booking_confirmation', confirmation_number=confirmation_number))


@app.route('/trips')
def list_trips():
    '''List all trips.'''
    trips = load_trips()
    return render_template('trips.html', trips=trips)


@app.route('/trips/<int:trip_id>')
def trip_details(trip_id):
    '''Show trip details.'''
    trip = get_trip_by_id(trip_id)
    if not trip:
        abort(404)
    return render_template('trip_details.html', trip=trip)


@app.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
def edit_trip(trip_id):
    '''Edit trip details.'''
    trip = get_trip_by_id(trip_id)
    if not trip:
        abort(404)

    if request.method == 'POST':
        trip_name = request.form.get('trip_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        total_budget = request.form.get('total_budget', '').strip()
        status = request.form.get('status', '').strip()

        if trip_name and destination and start_date and end_date and total_budget and status:
            trips = load_trips()
            for t in trips:
                if t['trip_id'] == trip_id:
                    t['trip_name'] = trip_name
                    t['destination'] = destination
                    t['start_date'] = start_date
                    t['end_date'] = end_date
                    try:
                        t['total_budget'] = float(total_budget)
                    except ValueError:
                        t['total_budget'] = 0.0
                    t['status'] = status
                    break
            save_trips(trips)
            return redirect(url_for('list_trips'))

    return render_template('edit_trip.html', trip=trip)


@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    trips = load_trips()
    trips = [t for t in trips if t['trip_id'] != trip_id]
    save_trips(trips)
    return redirect(url_for('list_trips'))


@app.route('/booking/confirmation/<string:confirmation_number>')
def booking_confirmation(confirmation_number):
    booking = get_booking_by_confirmation(confirmation_number)
    if not booking:
        abort(404)
    # Optionally get related trip info
    trip = get_trip_by_id(booking['trip_id'])
    return render_template('booking_confirmation.html', booking=booking, trip=trip)


@app.route('/recommendations')
def recommendations():
    '''Travel recommendations page with filters.'''
    season_filter = request.args.get('season_filter', '').strip()  # Spring, Summer, Fall, Winter
    budget_filter = request.args.get('budget_filter', '').strip()  # Low, Medium, High

    # For demo, trending destinations sorted by popularity (simulate by dest_id desc)
    destinations = load_destinations()
    trending_destinations = sorted(destinations, key=lambda d: d['dest_id'], reverse=True)

    # Season and budget filters not explicitly defined in data, so just pass through

    return render_template('recommendations.html', trending_destinations=trending_destinations,
                           season_filter=season_filter, budget_filter=budget_filter)


@app.route('/back-to-dashboard')
def back_to_dashboard():
    '''Redirect back to dashboard.'''
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
