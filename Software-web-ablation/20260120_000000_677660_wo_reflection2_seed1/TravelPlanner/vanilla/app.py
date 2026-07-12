from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Helper functions to load data from files

def load_destinations():
    dest_file = os.path.join(data_dir, 'destinations.txt')
    destinations = []
    try:
        with open(dest_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: dest_id(int), name(str), country(str), region(str), description(str), attractions(str), climate(str)
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
    except FileNotFoundError:
        pass
    return destinations

def load_itineraries():
    itin_file = os.path.join(data_dir, 'itineraries.txt')
    itineraries = []
    try:
        with open(itin_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: itinerary_id(int), itinerary_name(str), destination(str), start_date(str), end_date(str), activities(str), status(str)
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
    except FileNotFoundError:
        pass
    return itineraries

def load_hotels():
    hotel_file = os.path.join(data_dir, 'hotels.txt')
    hotels = []
    try:
        with open(hotel_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: hotel_id(int), name(str), city(str), rating(float), price_per_night(float), amenities(str), category(str)
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
    except FileNotFoundError:
        pass
    return hotels

def load_flights():
    flights_file = os.path.join(data_dir, 'flights.txt')
    flights = []
    try:
        with open(flights_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: flight_id(int), airline(str), departure_city(str), arrival_city(str), departure_time(str), arrival_time(str), price(float), class_type(str), duration(str)
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
    except FileNotFoundError:
        pass
    return flights

def load_packages():
    packages_file = os.path.join(data_dir, 'packages.txt')
    packages = []
    try:
        with open(packages_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: package_id(int), package_name(str), destination(str), duration_days(int), price(float), included_items(str), difficulty_level(str)
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
    except FileNotFoundError:
        pass
    return packages

def load_trips():
    trips_file = os.path.join(data_dir, 'trips.txt')
    trips = []
    try:
        with open(trips_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: trip_id(int), trip_name(str), destination(str), start_date(str), end_date(str), total_budget(float), status(str), created_date(str)
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
    except FileNotFoundError:
        pass
    return trips

def load_bookings():
    bookings_file = os.path.join(data_dir, 'bookings.txt')
    bookings = []
    try:
        with open(bookings_file, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # Fields: booking_id(int), trip_id(int), booking_type(str), booking_date(str), amount(float), confirmation_number(str), status(str)
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
    except FileNotFoundError:
        pass
    return bookings


# Root route redirects to dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# /dashboard GET
@app.route('/dashboard')
def dashboard():
    destinations = load_destinations()
    trips = load_trips()
    # featured_destinations: List[Dict]{dest_id:int, name:str, country:str}
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations[:5]
    ]
    # upcoming_trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str}
    upcoming_trips = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
        } for t in trips if t['status'].lower() in ('planned', 'booked', 'in progress')
    ]
    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


# /destinations GET,POST
@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations_data = load_destinations()
    # destinations: List[Dict]{dest_id:int, name:str, country:str, region:str}
    destinations_context = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region'],
        } for d in destinations_data
    ]
    # POST could handle search/filter in future; currently just render
    return render_template('destinations.html', destinations=destinations_context)


# /destinations/<int:dest_id> GET,POST
@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations_data = load_destinations()
    destination = None
    for d in destinations_data:
        if d['dest_id'] == dest_id:
            # destination: Dict{name:str, country:str, description:str, attractions:str}
            destination = {
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions'],
            }
            break
    if destination is None:
        # If dest_id not found, show 404
        return "Destination not found", 404

    # POST could handle add-to-trip action
    if request.method == 'POST':
        # Placeholder for adding to trip logic
        # For now, just reload page
        return render_template('destination_details.html', destination=destination)

    return render_template('destination_details.html', destination=destination)


# /itinerary GET,POST
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_data = load_itineraries()
    # itineraries: List[Dict]{itinerary_id:int, itinerary_name:str, destination:str, start_date:str, end_date:str, activities:str, status:str}
    itineraries = [
        {
            'itinerary_id': i['itinerary_id'],
            'itinerary_name': i['itinerary_name'],
            'destination': i['destination'],
            'start_date': i['start_date'],
            'end_date': i['end_date'],
            'activities': i['activities'],
            'status': i['status']
        } for i in itineraries_data
    ]
    # POST can be used to add activity or other edits
    # For now, just render
    return render_template('itinerary.html', itineraries=itineraries)


# /accommodations GET,POST
@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels_data = load_hotels()
    # hotels: List[Dict]{hotel_id:int, name:str, city:str, rating:float, price_per_night:float, amenities:str, category:str}
    hotels = [
        {
            'hotel_id': h['hotel_id'],
            'name': h['name'],
            'city': h['city'],
            'rating': h['rating'],
            'price_per_night': h['price_per_night'],
            'amenities': h['amenities'],
            'category': h['category']
        } for h in hotels_data
    ]
    # POST could handle search and filter
    return render_template('accommodations.html', hotels=hotels)


# /transportation GET,POST
@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights_data = load_flights()
    # flights: List[Dict]{flight_id:int, airline:str, departure_city:str, arrival_city:str, departure_time:str, arrival_time:str, price:float, class_type:str, duration:str}
    flights = [
        {
            'flight_id': f['flight_id'],
            'airline': f['airline'],
            'departure_city': f['departure_city'],
            'arrival_city': f['arrival_city'],
            'departure_time': f['departure_time'],
            'arrival_time': f['arrival_time'],
            'price': f['price'],
            'class_type': f['class_type'],
            'duration': f['duration']
        } for f in flights_data
    ]
    # POST could filter flights or search
    return render_template('transportation.html', flights=flights)


# /packages GET,POST
@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages_data = load_packages()
    # packages: List[Dict]{package_id:int, package_name:str, destination:str, duration_days:int, price:float}
    packages = [
        {
            'package_id': p['package_id'],
            'package_name': p['package_name'],
            'destination': p['destination'],
            'duration_days': p['duration_days'],
            'price': p['price']
        } for p in packages_data
    ]
    # POST could handle booking or filtering
    return render_template('packages.html', packages=packages)


# /trips GET,POST
@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_data = load_trips()
    # trips: List[Dict]{trip_id:int, trip_name:str, destination:str, start_date:str, end_date:str, status:str}
    trips_context = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date'],
            'status': t['status']
        } for t in trips_data
    ]
    # POST can be used for add/edit/delete trip actions
    return render_template('trips.html', trips=trips_context)


# /booking-confirmation GET
@app.route('/booking-confirmation')
def booking_confirmation():
    bookings = load_bookings()
    trips_data = load_trips()
    # Get query param for confirmation number
    confirmation_number = request.args.get('confirmation_number')
    booking_info = None
    if confirmation_number:
        for b in bookings:
            if b['confirmation_number'] == confirmation_number:
                # Compose booking dict as required
                booking_info = {
                    'confirmation_number': b['confirmation_number'],
                    'booking_details': f"Booking Type: {b['booking_type']}, Date: {b['booking_date']}, Amount: {b['amount']}, Status: {b['status']}"
                }
                break
    if booking_info is None:
        # Default empty or not found
        booking_info = {'confirmation_number': '', 'booking_details': 'No booking found'}
    return render_template('booking_confirmation.html', booking=booking_info)


# /recommendations GET,POST
@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations():
    # For recommendations, data structure is general
    destinations_data = load_destinations()
    # Create trending_destinations: List[Dict]{dest_id:int, name:str, country:str, popularity:int}
    # We don't have popularity in destinations file, simulate by sorting by dest_id descending
    trending_destinations = [
        {
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'popularity': d['dest_id'] * 10  # mock popularity
        } for d in sorted(destinations_data, key=lambda x: x['dest_id'], reverse=True)[:5]
    ]
    # recommendations - generic list of Dict
    recommendations = []
    # POST could apply filters and produce recommendations
    return render_template('recommendations.html', recommendations=recommendations, trending_destinations=trending_destinations)


if __name__ == '__main__':
    app.run(debug=True)
