from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to load data from text files

def load_destinations():
    destinations = []
    path = os.path.join(DATA_DIR, 'destinations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    dest_id, name, country, region, description, attractions, climate = fields
                    destinations.append({
                        'dest_id': int(dest_id),
                        'name': name,
                        'country': country,
                        'region': region,
                        'description': description,
                        'attractions': attractions,
                        'climate': climate
                    })
    return destinations

def load_itineraries():
    itineraries = []
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    itinerary_id, itinerary_name, destination, start_date, end_date, activities, status = fields
                    itineraries.append({
                        'itinerary_id': int(itinerary_id),
                        'itinerary_name': itinerary_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'activities': activities,
                        'status': status
                    })
    return itineraries

def load_hotels():
    hotels = []
    path = os.path.join(DATA_DIR, 'hotels.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    hotel_id, name, city, rating, price_per_night, amenities, category = fields
                    hotels.append({
                        'hotel_id': int(hotel_id),
                        'name': name,
                        'city': city,
                        'rating': float(rating),
                        'price_per_night': float(price_per_night),
                        'amenities': amenities,
                        'category': category
                    })
    return hotels

def load_flights():
    flights = []
    path = os.path.join(DATA_DIR, 'flights.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 9:
                    flight_id, airline, departure_city, arrival_city, departure_time, arrival_time, price, class_type, duration = fields
                    flights.append({
                        'flight_id': int(flight_id),
                        'airline': airline,
                        'departure_city': departure_city,
                        'arrival_city': arrival_city,
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'price': float(price),
                        'class_type': class_type,
                        'duration': duration
                    })
    return flights

def load_packages():
    packages = []
    path = os.path.join(DATA_DIR, 'packages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    package_id, package_name, destination, duration_days, price, included_items, difficulty_level = fields
                    packages.append({
                        'package_id': int(package_id),
                        'package_name': package_name,
                        'destination': destination,
                        'duration_days': int(duration_days),
                        'price': float(price),
                        'included_items': included_items,
                        'difficulty_level': difficulty_level
                    })
    return packages

def load_trips():
    trips = []
    path = os.path.join(DATA_DIR, 'trips.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 8:
                    trip_id, trip_name, destination, start_date, end_date, total_budget, status, created_date = fields
                    trips.append({
                        'trip_id': int(trip_id),
                        'trip_name': trip_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'total_budget': float(total_budget),
                        'status': status,
                        'created_date': created_date
                    })
    return trips

def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    booking_id, trip_id, booking_type, booking_date, amount, confirmation_number, status = fields
                    bookings.append({
                        'booking_id': int(booking_id),
                        'trip_id': int(trip_id),
                        'booking_type': booking_type,
                        'booking_date': booking_date,
                        'amount': float(amount),
                        'confirmation_number': confirmation_number,
                        'status': status
                    })
    return bookings

# Save functions for itineraries, trips, bookings (for modifications)

def save_itineraries(itineraries):
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for it in itineraries:
            line = '|'.join([
                str(it['itinerary_id']), it['itinerary_name'], it['destination'], it['start_date'], it['end_date'], it['activities'], it['status']
            ])
            f.write(line + '\n')

def save_trips(trips):
    path = os.path.join(DATA_DIR, 'trips.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for trip in trips:
            line = '|'.join([
                str(trip['trip_id']), trip['trip_name'], trip['destination'], trip['start_date'], trip['end_date'], 
                f"{trip['total_budget']:.2f}", trip['status'], trip['created_date']
            ])
            f.write(line + '\n')

def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for booking in bookings:
            line = '|'.join([
                str(booking['booking_id']), str(booking['trip_id']), booking['booking_type'], booking['booking_date'], 
                f"{booking['amount']:.2f}", booking['confirmation_number'], booking['status']
            ])
            f.write(line + '\n')

# Routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    destinations = load_destinations()
    trips = load_trips()
    today = datetime.today().date()
    upcoming_trips = [t for t in trips if datetime.strptime(t['start_date'], '%Y-%m-%d').date() >= today and t['status'].lower() != 'cancelled']
    # Featured destinations: we pick first 3 for simplicity
    featured_destinations = destinations[:3]
    return render_template('dashboard.html', 
                           featured_destinations=featured_destinations, 
                           upcoming_trips=upcoming_trips)

@app.route('/destinations')
def destinations():
    destinations = load_destinations()
    # Support GET search/filter params
    search_query = request.args.get('search', '').lower()
    region_filter = request.args.get('region', '')
    filtered_destinations = destinations
    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query in d['name'].lower() or search_query in d['country'].lower()]
    if region_filter and region_filter in ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']:
        filtered_destinations = [d for d in filtered_destinations if d['region'] == region_filter]
    return render_template('destinations.html', destinations=filtered_destinations, search_query=search_query, region_filter=region_filter)

@app.route('/destination/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        return "Destination not found", 404
    message = ''
    if request.method == 'POST':
        # Add to trip flow: simple add a new itinerary with blank placeholders
        itineraries = load_itineraries()
        max_id = max([it['itinerary_id'] for it in itineraries], default=0)
        new_itinerary = {
            'itinerary_id': max_id + 1,
            'itinerary_name': f"New Trip to {destination['name']}",
            'destination': destination['name'],
            'start_date': '',
            'end_date': '',
            'activities': '',
            'status': 'Planned'
        }
        itineraries.append(new_itinerary)
        save_itineraries(itineraries)
        message = 'Destination added to your itineraries.'
    return render_template('destination_details.html', destination=destination, message=message)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = load_itineraries()
    message = ''
    if request.method == 'POST':
        # Handle creating new itinerary or adding activity or editing/deleting itinerary
        form_type = request.form.get('form_type')

        if form_type == 'add_itinerary':
            # Add new itinerary
            max_id = max([it['itinerary_id'] for it in itineraries], default=0)
            itinerary_name = request.form.get('itinerary_name', '').strip()
            destination = request.form.get('destination', '').strip()
            start_date = request.form.get('start_date', '')
            end_date = request.form.get('end_date', '')
            if itinerary_name and destination and start_date and end_date:
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
                message = 'Itinerary added successfully.'

        elif form_type == 'add_activity':
            # Add activity to selected itinerary
            itinerary_id = request.form.get('itinerary_id')
            activity = request.form.get('activity', '').strip()
            if itinerary_id and activity:
                itinerary_id = int(itinerary_id)
                for it in itineraries:
                    if it['itinerary_id'] == itinerary_id:
                        if it['activities']:
                            it['activities'] += ', ' + activity
                        else:
                            it['activities'] = activity
                        save_itineraries(itineraries)
                        message = 'Activity added.'
                        break

        elif form_type == 'edit_itinerary':
            itinerary_id = request.form.get('itinerary_id')
            if itinerary_id:
                itinerary_id = int(itinerary_id)
                for it in itineraries:
                    if it['itinerary_id'] == itinerary_id:
                        it['itinerary_name'] = request.form.get('itinerary_name', it['itinerary_name'])
                        it['destination'] = request.form.get('destination', it['destination'])
                        it['start_date'] = request.form.get('start_date', it['start_date'])
                        it['end_date'] = request.form.get('end_date', it['end_date'])
                        it['activities'] = request.form.get('activities', it['activities'])
                        it['status'] = request.form.get('status', it['status'])
                        save_itineraries(itineraries)
                        message = 'Itinerary updated.'
                        break

        elif form_type == 'delete_itinerary':
            itinerary_id = request.form.get('itinerary_id')
            if itinerary_id:
                itinerary_id = int(itinerary_id)
                itineraries = [it for it in itineraries if it['itinerary_id'] != itinerary_id]
                save_itineraries(itineraries)
                message = 'Itinerary deleted.'

    return render_template('itinerary.html', itineraries=itineraries, message=message)

@app.route('/accommodations')
def accommodations():
    hotels = load_hotels()
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
    flights = load_flights()
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
    packages_data = load_packages()
    duration_filter = request.args.get('duration_filter', '')
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
            bookings = load_bookings()
            trips = load_trips()

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
            save_trips(trips)

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
            save_bookings(bookings)

            message = f'Package "{package["package_name"]}" booked successfully! Confirmation: CONF{new_booking_id:03}'

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter, message=message)

@app.route('/trips', methods=['GET', 'POST'])
def trips_page():
    trips = load_trips()
    message = ''

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        trip_id = request.form.get('trip_id')
        if trip_id:
            trip_id = int(trip_id)

            if form_type == 'delete_trip':
                trips = [t for t in trips if t['trip_id'] != trip_id]
                save_trips(trips)
                message = 'Trip deleted successfully.'
            elif form_type == 'edit_trip':
                for t in trips:
                    if t['trip_id'] == trip_id:
                        t['trip_name'] = request.form.get('trip_name', t['trip_name'])
                        t['destination'] = request.form.get('destination', t['destination'])
                        t['start_date'] = request.form.get('start_date', t['start_date'])
                        t['end_date'] = request.form.get('end_date', t['end_date'])
                        t['total_budget'] = float(request.form.get('total_budget', t['total_budget']))
                        t['status'] = request.form.get('status', t['status'])
                        save_trips(trips)
                        message = 'Trip updated successfully.'
                        break

    return render_template('trips.html', trips=trips, message=message)

@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    bookings = load_bookings()
    trips = load_trips()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html', booking=booking, trip=trip)

@app.route('/recommendations')
def recommendations():
    destinations = load_destinations()
    itineraries = load_itineraries()
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
