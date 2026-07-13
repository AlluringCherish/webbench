from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'travelplanner_secret_key_for_sessions'

data_folder = 'data'

# Utility functions to read data files

def read_destinations():
    destinations = []
    filepath = os.path.join(data_folder, 'destinations.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    return destinations


def read_itineraries():
    itineraries = []
    filepath = os.path.join(data_folder, 'itineraries.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    return itineraries


def write_itineraries(itineraries):
    filepath = os.path.join(data_folder, 'itineraries.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for it in itineraries:
            line = f"{it['itinerary_id']}|{it['itinerary_name']}|{it['destination']}|{it['start_date']}|{it['end_date']}|{it['activities']}|{it['status']}"
            f.write(line + '\n')


def read_hotels():
    hotels = []
    filepath = os.path.join(data_folder, 'hotels.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    return hotels


def read_flights():
    flights = []
    filepath = os.path.join(data_folder, 'flights.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                    'duration': parts[8]
                }
                flights.append(flight)
    return flights


def read_packages():
    packages = []
    filepath = os.path.join(data_folder, 'packages.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    return packages


def read_trips():
    trips = []
    filepath = os.path.join(data_folder, 'trips.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
                    'created_date': parts[7]
                }
                trips.append(trip)
    return trips


def write_trips(trips):
    filepath = os.path.join(data_folder, 'trips.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for trip in trips:
            line = f"{trip['trip_id']}|{trip['trip_name']}|{trip['destination']}|{trip['start_date']}|{trip['end_date']}|{trip['total_budget']}|{trip['status']}|{trip['created_date']}"
            f.write(line + '\n')


def read_bookings():
    bookings = []
    filepath = os.path.join(data_folder, 'bookings.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    return bookings


def write_bookings(bookings):
    filepath = os.path.join(data_folder, 'bookings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for booking in bookings:
            line = f"{booking['booking_id']}|{booking['trip_id']}|{booking['booking_type']}|{booking['booking_date']}|{booking['amount']}|{booking['confirmation_number']}|{booking['status']}"
            f.write(line + '\n')


@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    destinations = read_destinations()
    trips = read_trips()
    today_str = datetime.today().strftime('%Y-%m-%d')
    # Featured destinations: for demo purpose show first 3
    featured_destinations = destinations[:3]
    # Upcoming trips (start_date >= today, status not Cancelled)
    upcoming_trips = [t for t in trips if t['start_date'] >= today_str and t['status'].lower() != 'cancelled']
    return render_template('dashboard.html', 
                           featured_destinations=featured_destinations, 
                           upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = read_destinations()
    search = request.args.get('search', '').lower()
    region_filter = request.args.get('region', '')

    filtered = destinations
    if search:
        filtered = [d for d in filtered if search in d['name'].lower() or search in d['country'].lower()]
    if region_filter and region_filter in ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']:
        filtered = [d for d in filtered if d['region'] == region_filter]

    return render_template('destinations.html', destinations=filtered, search=search, region_filter=region_filter)


@app.route('/destination/<int:dest_id>', methods=['GET', 'POST'])
def destination_detail(dest_id):
    destinations = read_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if destination is None:
        flash('Destination not found.')
        # show destinations page instead of redirect loop
        return redirect(url_for('destinations'))

    if request.method == 'POST':
        # Add to itinerary flow
        itineraries = read_itineraries()
        # We expect a form submission with itinerary fields or add this destination to a new or existing itinerary
        itinerary_name = request.form.get('itinerary_name', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        activities = request.form.get('activities', '').strip()
        status = 'Planned'

        if not itinerary_name or not start_date or not end_date:
            flash('Please provide itinerary name, start date and end date.')
            return redirect(url_for('destination_detail', dest_id=dest_id))

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.')
            return redirect(url_for('destination_detail', dest_id=dest_id))

        new_itinerary_id = 1
        if itineraries:
            new_itinerary_id = max(it['itinerary_id'] for it in itineraries) + 1

        new_itinerary = {
            'itinerary_id': new_itinerary_id,
            'itinerary_name': itinerary_name,
            'destination': destination['name'],
            'start_date': start_date,
            'end_date': end_date,
            'activities': activities,
            'status': status
        }
        itineraries.append(new_itinerary)
        write_itineraries(itineraries)
        flash('Itinerary added successfully.')
        return redirect(url_for('itinerary'))

    return render_template('destination_detail.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = read_itineraries()

    message = ''  # Initialize message variable

    if request.method == 'POST':
        # Handling add or update or delete
        action = request.form.get('action')
        if action == 'add':
            itinerary_name = request.form.get('itinerary_name', '').strip()
            destination = request.form.get('destination', '').strip()
            start_date = request.form.get('start_date', '').strip()
            end_date = request.form.get('end_date', '').strip()
            activities = request.form.get('activities', '').strip()
            status = request.form.get('status', 'Planned').strip()

            if not itinerary_name or not destination or not start_date or not end_date:
                flash('Please fill all required fields.')
                return redirect(url_for('itinerary'))

            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.')
                return redirect(url_for('itinerary'))

            new_id = 1
            if itineraries:
                new_id = max(it['itinerary_id'] for it in itineraries) + 1

            new_itinerary = {
                'itinerary_id': new_id,
                'itinerary_name': itinerary_name,
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'activities': activities,
                'status': status
            }
            itineraries.append(new_itinerary)
            write_itineraries(itineraries)
            flash('New itinerary added.')
            return redirect(url_for('itinerary'))

        elif action == 'delete':
            itinerary_id = int(request.form.get('itinerary_id', 0))
            itineraries = [it for it in itineraries if it['itinerary_id'] != itinerary_id]
            write_itineraries(itineraries)
            flash('Itinerary deleted.')
            return redirect(url_for('itinerary'))

        elif action == 'edit':
            itinerary_id = int(request.form.get('itinerary_id', 0))
            itinerary_name = request.form.get('itinerary_name', '').strip()
            destination = request.form.get('destination', '').strip()
            start_date = request.form.get('start_date', '').strip()
            end_date = request.form.get('end_date', '').strip()
            activities = request.form.get('activities', '').strip()
            status = request.form.get('status', 'Planned').strip()

            if not itinerary_name or not destination or not start_date or not end_date:
                flash('Please fill all required fields.')
                return redirect(url_for('itinerary'))

            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.')
                return redirect(url_for('itinerary'))

            for idx, it in enumerate(itineraries):
                if it['itinerary_id'] == itinerary_id:
                    itineraries[idx] = {
                        'itinerary_id': itinerary_id,
                        'itinerary_name': itinerary_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'activities': activities,
                        'status': status
                    }
                    break
            write_itineraries(itineraries)
            flash('Itinerary updated.')
            return redirect(url_for('itinerary'))

    # GET method
    return render_template('itinerary.html', itineraries=itineraries, message=message)


@app.route('/accommodations')
def accommodations():
    hotels = read_hotels()
    destination_input = request.args.get('destination', '').lower()
    check_in_date = request.args.get('check_in_date', '')
    check_out_date = request.args.get('check_out_date', '')
    price_filter = request.args.get('price_filter', '')

    filtered_hotels = hotels
    if destination_input:
        filtered_hotels = [h for h in filtered_hotels if destination_input in h['city'].lower()]
    if price_filter in ['Budget', 'Mid-range', 'Luxury']:
        filtered_hotels = [h for h in filtered_hotels if h['category'] == price_filter]

    return render_template('accommodations.html', hotels=filtered_hotels, destination_input=destination_input, check_in_date=check_in_date, check_out_date=check_out_date, price_filter=price_filter)

@app.route('/transportation')
def transportation():
    flights = read_flights()
    departure_city = request.args.get('departure_city', '').lower()
    arrival_city = request.args.get('arrival_city', '').lower()
    departure_date = request.args.get('departure_date', '')
    flight_class_filter = request.args.get('flight_class_filter', '')

    filtered_flights = flights
    if departure_city:
        filtered_flights = [f for f in filtered_flights if departure_city in f['departure_city'].lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if arrival_city in f['arrival_city'].lower()]
    if flight_class_filter in ['Economy', 'Business', 'First Class']:
        filtered_flights = [f for f in filtered_flights if f['class_type'] == flight_class_filter]

    return render_template('transportation.html', flights=filtered_flights, departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date, flight_class_filter=flight_class_filter)

@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages_data = read_packages()
    duration_filter = request.args.get('duration_filter', '') or request.args.get('duration', '')
    filtered_packages = packages_data

    if duration_filter == '3-5 days':
        filtered_packages = [p for p in packages_data if 3 <= p['duration_days'] <= 5]
    elif duration_filter == '7-10 days':
        filtered_packages = [p for p in packages_data if 7 <= p['duration_days'] <= 10]
    elif duration_filter == '14+ days':
        filtered_packages = [p for p in packages_data if p['duration_days'] >= 14]

    # Booking flow
    message = ''
    if request.method == 'POST':
        pkg_id = int(request.form.get('package_id'))
        # Fetch package
        package = next((p for p in packages_data if p['package_id'] == pkg_id), None)
        if package:
            # Add booking and trip
            bookings = read_bookings()
            trips = read_trips()

            max_booking_id = max([b['booking_id'] for b in bookings], default=0)
            max_trip_id = max([t['trip_id'] for t in trips], default=0)

            new_trip_id = max_trip_id + 1
            new_booking_id = max_booking_id + 1

            new_trip = {
                'trip_id': new_trip_id,
                'trip_name': package['package_name'],
                'destination': package['destination'],
                'start_date': '',
                'end_date': '',
                'total_budget': package['price'],
                'status': 'Booked',
                'created_date': datetime.today().strftime('%Y-%m-%d')
            }

            trips.append(new_trip)
            write_trips(trips)

            new_booking = {
                'booking_id': new_booking_id,
                'trip_id': new_trip_id,
                'booking_type': 'Package',
                'booking_date': datetime.today().strftime('%Y-%m-%d'),
                'amount': package['price'],
                'confirmation_number': f'CONF{new_booking_id:03}',
                'status': 'Confirmed'
            }
            bookings.append(new_booking)
            write_bookings(bookings)

            message = f'Package "{package["package_name"]}" booked successfully! Confirmation: CONF{new_booking_id:03}'

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter, message=message)

@app.route('/trips', methods=['GET', 'POST'])
def trips_page():
    trips = read_trips()
    message = ''

    if request.method == 'POST':
        form_type = request.form.get('action')  # fixed to 'action' to match form buttons
        trip_id = request.form.get('trip_id')
        if trip_id:
            trip_id = int(trip_id)

            if form_type == 'delete':
                trips = [t for t in trips if t['trip_id'] != trip_id]
                write_trips(trips)
                message = 'Trip deleted successfully.'
            elif form_type == 'edit':
                for t in trips:
                    if t['trip_id'] == trip_id:
                        t['trip_name'] = request.form.get('trip_name', t['trip_name'])
                        t['destination'] = request.form.get('destination', t['destination'])
                        t['start_date'] = request.form.get('start_date', t['start_date'])
                        t['end_date'] = request.form.get('end_date', t['end_date'])
                        try:
                            t['total_budget'] = float(request.form.get('total_budget', t['total_budget']))
                        except ValueError:
                            pass
                        t['status'] = request.form.get('status', t['status'])
                        write_trips(trips)
                        message = 'Trip updated successfully.'
                        break

    return render_template('trips.html', trips=trips, message=message)

@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    bookings = read_bookings()
    trips = read_trips()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html', booking=booking, trip=trip)

@app.route('/recommendations')
def recommendations():
    destinations = read_destinations()
    itineraries = read_itineraries()
    season_filter = request.args.get('season', '')
    budget_filter = request.args.get('budget', '')

    # For trending destinations, count itinerary frequency as popularity
    popularity_map = {}
    for it in itineraries:
        dest = it['destination']
        popularity_map[dest] = popularity_map.get(dest, 0) + 1

    trending_destinations = sorted(destinations, key=lambda d: popularity_map.get(d['name'], 0), reverse=True)

    # Filters do not affect trending for now, but could filter presented list as example
    if season_filter:
        # Could filter destinations by season - no data given, so skip actual filter
        pass
    if budget_filter:
        # Could filter destinations if had budget data - no data given, so skip actual filter
        pass

    return render_template('recommendations.html', trending_destinations=trending_destinations, season_filter=season_filter, budget_filter=budget_filter)


if __name__ == '__main__':
    app.run(debug=True)
