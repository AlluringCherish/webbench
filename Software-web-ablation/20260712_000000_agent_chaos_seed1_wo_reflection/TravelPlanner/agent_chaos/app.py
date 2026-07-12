from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper function to load destinations data

def load_destinations():
    destinations = []
    path = os.path.join(DATA_DIR, 'destinations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    dest_id = int(parts[0])
                    name = parts[1]
                    country = parts[2]
                    region = parts[3]
                    description = parts[4]
                    attractions = [a.strip() for a in parts[5].split(',')] if parts[5] else []
                    climate = parts[6]
                    destinations.append({
                        'dest_id': dest_id,
                        'name': name,
                        'country': country,
                        'region': region,
                        'description': description,
                        'attractions': attractions,
                        'climate': climate
                    })
    except FileNotFoundError:
        destinations = []
    return destinations

# Helper function to load itineraries

def load_itineraries():
    itineraries = []
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    itinerary_id = int(parts[0])
                    itinerary_name = parts[1]
                    destination = parts[2]
                    start_date = parts[3]
                    end_date = parts[4]
                    activities = [a.strip() for a in parts[5].split(',')] if parts[5] else []
                    status = parts[6]
                    itineraries.append({
                        'itinerary_id': itinerary_id,
                        'itinerary_name': itinerary_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'activities': activities,
                        'status': status
                    })
    except FileNotFoundError:
        itineraries = []
    return itineraries

# Helper function to load hotels

def load_hotels():
    hotels = []
    path = os.path.join(DATA_DIR, 'hotels.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    hotel_id = int(parts[0])
                    name = parts[1]
                    city = parts[2]
                    rating = float(parts[3])
                    price_per_night = float(parts[4])
                    amenities = [a.strip() for a in parts[5].split(',')] if parts[5] else []
                    category = parts[6]
                    hotels.append({
                        'hotel_id': hotel_id,
                        'name': name,
                        'city': city,
                        'rating': rating,
                        'price_per_night': price_per_night,
                        'amenities': amenities,
                        'category': category
                    })
    except FileNotFoundError:
        hotels = []
    return hotels

# Helper function to load flights

def load_flights():
    flights = []
    path = os.path.join(DATA_DIR, 'flights.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    flight_id = int(parts[0])
                    airline = parts[1]
                    departure_city = parts[2]
                    arrival_city = parts[3]
                    departure_time = parts[4]
                    arrival_time = parts[5]
                    price = float(parts[6])
                    class_type = parts[7]
                    duration = parts[8]
                    flights.append({
                        'flight_id': flight_id,
                        'airline': airline,
                        'departure_city': departure_city,
                        'arrival_city': arrival_city,
                        'departure_time': departure_time,
                        'arrival_time': arrival_time,
                        'price': price,
                        'class_type': class_type,
                        'duration': duration
                    })
    except FileNotFoundError:
        flights = []
    return flights

# Helper function to load packages

def load_packages():
    packages = []
    path = os.path.join(DATA_DIR, 'packages.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    package_id = int(parts[0])
                    package_name = parts[1]
                    destination = parts[2]
                    duration_days = int(parts[3])
                    price = float(parts[4])
                    included_items = [item.strip() for item in parts[5].split(',')] if parts[5] else []
                    difficulty_level = parts[6]
                    packages.append({
                        'package_id': package_id,
                        'package_name': package_name,
                        'destination': destination,
                        'duration_days': duration_days,
                        'price': price,
                        'included_items': included_items,
                        'difficulty_level': difficulty_level
                    })
    except FileNotFoundError:
        packages = []
    return packages

# Helper function to load trips

def load_trips():
    trips = []
    path = os.path.join(DATA_DIR, 'trips.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    trip_id = int(parts[0])
                    trip_name = parts[1]
                    destination = parts[2]
                    start_date = parts[3]
                    end_date = parts[4]
                    total_budget = float(parts[5])
                    status = parts[6]
                    created_date = parts[7]
                    trips.append({
                        'trip_id': trip_id,
                        'trip_name': trip_name,
                        'destination': destination,
                        'start_date': start_date,
                        'end_date': end_date,
                        'total_budget': total_budget,
                        'status': status,
                        'created_date': created_date
                    })
    except FileNotFoundError:
        trips = []
    return trips

# Helper function to load bookings

def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    booking_id = int(parts[0])
                    trip_id = int(parts[1])
                    booking_type = parts[2]
                    booking_date = parts[3]
                    amount = float(parts[4])
                    confirmation_number = parts[5]
                    status = parts[6]
                    bookings.append({
                        'booking_id': booking_id,
                        'trip_id': trip_id,
                        'booking_type': booking_type,
                        'booking_date': booking_date,
                        'amount': amount,
                        'confirmation_number': confirmation_number,
                        'status': status
                    })
    except FileNotFoundError:
        bookings = []
    return bookings


# 1. Dashboard page
@app.route('/')
def dashboard():
    # Featured destinations: we pick the first 5 destinations summaries
    all_destinations = load_destinations()
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']}
        for d in all_destinations[:5]
    ]
    # Upcoming trips: trips that have start_date in future (no database, so consider all trips) and sort by start_date ascending
    all_trips = load_trips()
    upcoming_trips = sorted(
        [
            {'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'start_date': t['start_date']}
            for t in all_trips
        ],
        key=lambda x: x['start_date']
    )
    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


# 2. Destinations page
@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    all_destinations = load_destinations()
    search_query = ''
    selected_region = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        selected_region = request.form.get('selected_region', '').strip()

    # Filter destinations based on search_query and selected_region
    filtered_destinations = all_destinations
    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query.lower() in d['name'].lower()]
    if selected_region:
        filtered_destinations = [d for d in filtered_destinations if d['region'] == selected_region]

    # Prepare list with keys required: dest_id, name, country, region
    destinations_list = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']}
        for d in filtered_destinations
    ]

    return render_template('destinations.html', destinations=destinations_list, search_query=search_query, selected_region=selected_region)


# 3. Destination details page
@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)

    if not destination:
        # If not found, redirect to destinations page
        return redirect(url_for('destinations'))

    if request.method == 'POST':
        # Add destination to trip (for now, simulate success - no DB)
        # Implementation assumes form submit or ajax call handled elsewhere
        # Redirect back to same details page after POST
        return redirect(url_for('destination_details', dest_id=dest_id))

    return render_template('destination_details.html', destination=destination)


# 4. Itinerary planning page
@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()

    if request.method == 'POST':
        # Handle form data to add activity or create itinerary (simulation - no persistent storage)
        # Redirect back to itinerary page
        return redirect(url_for('plan_itinerary'))

    return render_template('itinerary.html', itineraries=itineraries)


# 5. Accommodations page
@app.route('/accommodations', methods=['GET', 'POST'])
def search_accommodations():
    hotels = load_hotels()
    search_destination = ''
    check_in_date = ''
    check_out_date = ''
    selected_price_filter = ''

    if request.method == 'POST':
        search_destination = request.form.get('search_destination', '').strip()
        check_in_date = request.form.get('check_in_date', '').strip()
        check_out_date = request.form.get('check_out_date', '').strip()
        selected_price_filter = request.form.get('selected_price_filter', '').strip()

    # Filter hotels based on search_destination and price filter
    filtered_hotels = hotels
    if search_destination:
        filtered_hotels = [h for h in filtered_hotels if search_destination.lower() in h['city'].lower()]

    if selected_price_filter:
        if selected_price_filter == 'Budget':
            filtered_hotels = [h for h in filtered_hotels if h['category'] == 'Budget']
        elif selected_price_filter == 'Mid-range':
            filtered_hotels = [h for h in filtered_hotels if h['category'] == 'Mid-range']
        elif selected_price_filter == 'Luxury':
            filtered_hotels = [h for h in filtered_hotels if h['category'] == 'Luxury']

    return render_template('accommodations.html', hotels=filtered_hotels,
                           search_destination=search_destination,
                           check_in_date=check_in_date,
                           check_out_date=check_out_date,
                           selected_price_filter=selected_price_filter)


# 6. Transportation page
@app.route('/transportation', methods=['GET', 'POST'])
def book_flights():
    flights = load_flights()
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    selected_class_filter = ''

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').strip()
        arrival_city = request.form.get('arrival_city', '').strip()
        departure_date = request.form.get('departure_date', '').strip()
        selected_class_filter = request.form.get('selected_class_filter', '').strip()

    filtered_flights = flights

    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city.lower()]
    if selected_class_filter:
        filtered_flights = [f for f in filtered_flights if f['class_type'] == selected_class_filter]

    return render_template('transportation.html',
                           flights=filtered_flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           departure_date=departure_date,
                           selected_class_filter=selected_class_filter)


# 7. Travel Packages page
@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages = load_packages()
    selected_duration_filter = ''

    if request.method == 'POST':
        selected_duration_filter = request.form.get('selected_duration_filter', '').strip()
        # Filter packages based on duration
        filtered_packages = []
        if selected_duration_filter == '3-5 days':
            filtered_packages = [p for p in packages if 3 <= p['duration_days'] <= 5]
        elif selected_duration_filter == '7-10 days':
            filtered_packages = [p for p in packages if 7 <= p['duration_days'] <= 10]
        elif selected_duration_filter == '14+ days':
            filtered_packages = [p for p in packages if p['duration_days'] >= 14]
        else:
            filtered_packages = packages
    else:
        filtered_packages = packages

    return render_template('packages.html', packages=filtered_packages, selected_duration_filter=selected_duration_filter)


# 8. Trip Management page
@app.route('/trips', methods=['GET', 'POST'])
def manage_trips():
    trips = load_trips()

    if request.method == 'POST':
        # Simulate edit/delete actions
        # Redirect back to trips page
        return redirect(url_for('manage_trips'))

    return render_template('trips.html', trips=trips)


# 9. Booking Confirmation page
@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        # If no such booking, redirect to dashboard
        return redirect(url_for('dashboard'))
    return render_template('booking_confirmation.html', booking=booking)


# 10. Travel Recommendations page
@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations():
    trending_destinations = [
        # Dummy trending with ranking fields
        {'dest_id': 1, 'name': 'Paris', 'ranking': 1},
        {'dest_id': 2, 'name': 'Tokyo', 'ranking': 2},
        {'dest_id': 3, 'name': 'Rio de Janeiro', 'ranking': 3}
    ]
    selected_season_filter = ''
    selected_budget_filter = ''

    if request.method == 'POST':
        selected_season_filter = request.form.get('selected_season_filter', '').strip()
        selected_budget_filter = request.form.get('selected_budget_filter', '').strip()
        # In a real app, we'd filter trending destinations; here we keep static for demo

    return render_template('recommendations.html',
                           trending_destinations=trending_destinations,
                           selected_season_filter=selected_season_filter,
                           selected_budget_filter=selected_budget_filter)


if __name__ == '__main__':
    app.run(debug=True)
