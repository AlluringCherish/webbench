from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Utility functions to load data files safely

def load_destinations():
    destinations = []
    try:
        with open(os.path.join(DATA_PATH, 'destinations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    dest_id, name, country, region, description, attractions, climate = parts
                    destinations.append({
                        'dest_id': int(dest_id),
                        'name': name,
                        'country': country,
                        'region': region,
                        'description': description,
                        'attractions': attractions,
                        'climate': climate
                    })
    except FileNotFoundError:
        # If file missing, return empty list
        return []
    return destinations


def load_itineraries():
    itineraries = []
    try:
        with open(os.path.join(DATA_PATH, 'itineraries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    itinerary_id, itinerary_name, destination, start_date, end_date, activities, status = parts
                    itineraries.append({
                        'itinerary_id': int(itinerary_id),
                        'itinerary_name': itinerary_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'activities': activities,
                        'status': status
                    })
    except FileNotFoundError:
        return []
    return itineraries


def load_hotels():
    hotels = []
    try:
        with open(os.path.join(DATA_PATH, 'hotels.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    hotel_id, name, city, rating, price_per_night, amenities, category = parts
                    hotels.append({
                        'hotel_id': int(hotel_id),
                        'name': name,
                        'city': city,
                        'rating': float(rating),
                        'price_per_night': float(price_per_night),
                        'amenities': amenities,
                        'category': category
                    })
    except FileNotFoundError:
        return []
    return hotels


def load_flights():
    flights = []
    try:
        with open(os.path.join(DATA_PATH, 'flights.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 9:
                    flight_id, airline, departure_city, arrival_city, departure_time, arrival_time, price, class_type, duration = parts
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
    except FileNotFoundError:
        return []
    return flights


def load_packages():
    packages = []
    try:
        with open(os.path.join(DATA_PATH, 'packages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    package_id, package_name, destination, duration_days, price, included_items, difficulty_level = parts
                    packages.append({
                        'package_id': int(package_id),
                        'package_name': package_name,
                        'destination': destination,
                        'duration_days': int(duration_days),
                        'price': float(price),
                        'included_items': included_items,
                        'difficulty_level': difficulty_level
                    })
    except FileNotFoundError:
        return []
    return packages


def load_trips():
    trips = []
    try:
        with open(os.path.join(DATA_PATH, 'trips.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    trip_id, trip_name, destination, start_date, end_date, total_budget, status, created_date = parts
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
    except FileNotFoundError:
        return []
    return trips


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_PATH, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    booking_id, trip_id, booking_type, booking_date, amount, confirmation_number, status = parts
                    bookings.append({
                        'booking_id': int(booking_id),
                        'trip_id': int(trip_id),
                        'booking_type': booking_type,
                        'booking_date': booking_date,
                        'amount': float(amount),
                        'confirmation_number': confirmation_number,
                        'status': status
                    })
    except FileNotFoundError:
        return []
    return bookings


@app.route('/')
def dashboard():
    # Load featured destinations - to keep only required fields:
    all_destinations = load_destinations()
    featured_destinations = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in all_destinations]

    # Load upcoming trips with limited fields
    all_trips = load_trips()
    # Assuming upcoming trips includes trips with start_date in future or status not Completed/Cancelled
    # Spec does not say filter criteria, so show all trips
    upcoming_trips = [{'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'destination': t['destination'], 'start_date': t['start_date']} for t in all_trips]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    all_destinations = load_destinations()
    region_filter = None
    search_query = None

    if request.method == 'POST':
        region_filter = request.form.get('region_filter')
        if region_filter == '':
            region_filter = None
        search_query = request.form.get('search_query')
        if search_query == '':
            search_query = None
    else:
        # GET could have args for filtering
        region_filter = request.args.get('region_filter')
        if region_filter == '':
            region_filter = None
        search_query = request.args.get('search_query')
        if search_query == '':
            search_query = None

    filtered_destinations = []
    for d in all_destinations:
        if region_filter and d['region'] != region_filter:
            continue
        if search_query and search_query.lower() not in d['name'].lower():
            continue
        filtered_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        })

    return render_template('destinations.html', destinations=filtered_destinations, region_filter=region_filter, search_query=search_query)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    all_destinations = load_destinations()
    destination = None
    for d in all_destinations:
        if d['dest_id'] == dest_id:
            destination = d
            break
    
    if not destination:
        # destination not found, could render 404 template or 404
        return "Destination not found", 404

    if request.method == 'POST':
        # Add-to-trip action, no navigation change
        # Since no storage mechanism specified, no actual addition done
        # Just re-render details page
        pass

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = load_itineraries()
    if request.method == 'POST':
        # Handle new activity add or itinerary creation or edits
        # Spec doesn't detail exact fields, so no data mutation performed
        pass

    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET'])
def accommodations():
    hotels = load_hotels()
    filters = {}
    # Spec says filters dict context variable, but no filter extraction method specified
    # We provide empty dict by default
    return render_template('accommodations.html', hotels=hotels, filters=filters)


@app.route('/transportation', methods=['GET'])
def transportation():
    flights = load_flights()
    filters = {}
    # Spec says filters context dict, no filtering implemented
    return render_template('transportation.html', flights=flights, filters=filters)


@app.route('/packages', methods=['GET'])
def packages():
    packages_data = load_packages()
    filters = {}
    return render_template('packages.html', packages=packages_data, filters=filters)


@app.route('/trips', methods=['GET'])
def trips():
    trips_data = load_trips()
    return render_template('trips.html', trips=trips_data)


@app.route('/booking_confirmation', methods=['GET'])
def booking_confirmation():
    bookings = load_bookings()
    # For simplicity showing the first booking as the current booking
    booking = None
    if bookings:
        b = bookings[0]
        # Construct booking_details as a string summarizing fields (HTML or formatted string)
        details = f"Booking Type: {b['booking_type']}, Date: {b['booking_date']}, Amount: ${b['amount']:.2f}, Status: {b['status']}"
        booking = {'confirmation_number': b['confirmation_number'], 'booking_details': details}
    else:
        booking = {'confirmation_number': 'N/A', 'booking_details': 'No bookings available.'}

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET'])
def recommendations():
    all_destinations = load_destinations()
    # trending_destinations: List[Dict]{dest_id:int, name:str, popularity:int}
    # Popularity field is not in original destinations file, so we simulate based on first 3 destinations with example values
    trending_destinations = []
    for d in all_destinations[:3]:
        trending_destinations.append({'dest_id': d['dest_id'], 'name': d['name'], 'popularity': 100 - d['dest_id']*10})
    filters = {}
    return render_template('recommendations.html', trending_destinations=trending_destinations, filters=filters)


if __name__ == '__main__':
    app.run(debug=True)
