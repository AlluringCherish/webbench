'''
Main Flask application for TravelPlanner web application.
Starts from the Dashboard page and provides routing to all pages.
Data is loaded from local text files in the 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
app = Flask(__name__)
DATA_DIR = 'data'
def load_destinations():
    destinations = []
    filepath = os.path.join(DATA_DIR, 'destinations.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        dest = {
                            'dest_id': parts[0],
                            'name': parts[1],
                            'country': parts[2],
                            'region': parts[3],
                            'description': parts[4],
                            'attractions': parts[5],
                            'climate': parts[6]
                        }
                        destinations.append(dest)
    return destinations
def load_itineraries():
    itineraries = []
    filepath = os.path.join(DATA_DIR, 'itineraries.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        itinerary = {
                            'itinerary_id': parts[0],
                            'itinerary_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'activities': parts[5],
                            'status': parts[6]
                        }
                        itineraries.append(itinerary)
    return itineraries
def load_trips():
    trips = []
    filepath = os.path.join(DATA_DIR, 'trips.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        trip = {
                            'trip_id': parts[0],
                            'trip_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'total_budget': parts[5],
                            'status': parts[6],
                            'created_date': parts[7]
                        }
                        trips.append(trip)
    return trips
@app.route('/')
def dashboard():
    '''
    Route for the Dashboard page.
    Loads featured destinations and upcoming trips to display.
    '''
    destinations = load_destinations()
    # For featured destinations, pick first 3 for example
    featured_destinations = destinations[:3]
    trips = load_trips()
    # For upcoming trips, filter trips with start_date in future (simple approach)
    from datetime import datetime
    today = datetime.today().date()
    upcoming_trips = []
    for trip in trips:
        try:
            start_date = datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
            if start_date >= today:
                upcoming_trips.append(trip)
        except:
            continue
    # Sort upcoming trips by start_date ascending
    upcoming_trips = sorted(upcoming_trips, key=lambda x: x['start_date'])[:3]
    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)
@app.route('/destinations')
def destinations_page():
    '''
    Route for the Destinations page.
    Supports search by name or country and filter by region.
    '''
    destinations = load_destinations()
    search_query = request.args.get('search', '').strip().lower()
    region_filter = request.args.get('region', '').strip()
    filtered_destinations = []
    for dest in destinations:
        if search_query:
            if search_query not in dest['name'].lower() and search_query not in dest['country'].lower():
                continue
        if region_filter and region_filter != 'All':
            if dest['region'] != region_filter:
                continue
        filtered_destinations.append(dest)
    regions = ['All', 'Asia', 'Europe', 'Americas', 'Africa', 'Oceania']
    return render_template('destinations.html',
                           destinations=filtered_destinations,
                           search_query=search_query,
                           region_filter=region_filter,
                           regions=regions)
@app.route('/destination/<dest_id>')
def destination_details(dest_id):
    '''
    Route for Destination Details page.
    Shows detailed info about a specific destination.
    '''
    destinations = load_destinations()
    destination = None
    for dest in destinations:
        if dest['dest_id'] == dest_id:
            destination = dest
            break
    if not destination:
        return "Destination not found", 404
    return render_template('destination_details.html', destination=destination)
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_page():
    '''
    Route for Itinerary Planning page.
    Allows creating and managing itineraries.
    '''
    itineraries = load_itineraries()
    if request.method == 'POST':
        # Add new itinerary
        itinerary_name = request.form.get('itinerary_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        activities = request.form.get('activities', '').strip()
        status = 'Planned'
        if itinerary_name and destination and start_date and end_date:
            # Generate new itinerary_id
            new_id = 1
            if itineraries:
                new_id = max(int(i['itinerary_id']) for i in itineraries) + 1
            new_itinerary = f"{new_id}|{itinerary_name}|{destination}|{start_date}|{end_date}|{activities}|{status}\n"
            filepath = os.path.join(DATA_DIR, 'itineraries.txt')
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(new_itinerary)
            return redirect(url_for('itinerary_page'))
    return render_template('itinerary.html', itineraries=itineraries)
@app.route('/accommodations')
def accommodations_page():
    '''
    Route for Accommodations page.
    Supports search and filter by destination, dates, and price range.
    '''
    hotels = []
    filepath = os.path.join(DATA_DIR, 'hotels.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        hotel = {
                            'hotel_id': parts[0],
                            'name': parts[1],
                            'city': parts[2],
                            'rating': parts[3],
                            'price_per_night': float(parts[4]),
                            'amenities': parts[5],
                            'category': parts[6]
                        }
                        hotels.append(hotel)
    destination_input = request.args.get('destination', '').strip().lower()
    price_filter = request.args.get('price', '').strip()
    filtered_hotels = []
    for hotel in hotels:
        if destination_input and destination_input not in hotel['city'].lower():
            continue
        if price_filter:
            if price_filter == 'Budget' and hotel['category'] != 'Budget':
                continue
            elif price_filter == 'Mid-range' and hotel['category'] != 'Mid-range':
                continue
            elif price_filter == 'Luxury' and hotel['category'] != 'Luxury':
                continue
        filtered_hotels.append(hotel)
    price_ranges = ['Budget', 'Mid-range', 'Luxury']
    return render_template('accommodations.html',
                           hotels=filtered_hotels,
                           destination_input=destination_input,
                           price_filter=price_filter,
                           price_ranges=price_ranges)
@app.route('/transportation')
def transportation_page():
    '''
    Route for Transportation page.
    Allows searching and booking flights.
    '''
    flights = []
    filepath = os.path.join(DATA_DIR, 'flights.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 9:
                        flight = {
                            'flight_id': parts[0],
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
    departure_city = request.args.get('departure_city', '').strip().lower()
    arrival_city = request.args.get('arrival_city', '').strip().lower()
    flight_class_filter = request.args.get('flight_class', '').strip()
    filtered_flights = []
    for flight in flights:
        if departure_city and departure_city not in flight['departure_city'].lower():
            continue
        if arrival_city and arrival_city not in flight['arrival_city'].lower():
            continue
        if flight_class_filter and flight_class_filter != 'All':
            if flight['class_type'] != flight_class_filter:
                continue
        filtered_flights.append(flight)
    flight_classes = ['All', 'Economy', 'Business', 'First Class']
    return render_template('transportation.html',
                           flights=filtered_flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           flight_class_filter=flight_class_filter,
                           flight_classes=flight_classes)
@app.route('/packages')
def packages_page():
    '''
    Route for Travel Packages page.
    Displays pre-designed travel packages with filters.
    '''
    packages = []
    filepath = os.path.join(DATA_DIR, 'packages.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        package = {
                            'package_id': parts[0],
                            'package_name': parts[1],
                            'destination': parts[2],
                            'duration_days': int(parts[3]),
                            'price': float(parts[4]),
                            'included_items': parts[5],
                            'difficulty_level': parts[6]
                        }
                        packages.append(package)
    duration_filter = request.args.get('duration', '').strip()
    filtered_packages = []
    for pkg in packages:
        if duration_filter:
            if duration_filter == '3-5 days' and not (3 <= pkg['duration_days'] <= 5):
                continue
            elif duration_filter == '7-10 days' and not (7 <= pkg['duration_days'] <= 10):
                continue
            elif duration_filter == '14+ days' and not (pkg['duration_days'] >= 14):
                continue
        filtered_packages.append(pkg)
    duration_options = ['All', '3-5 days', '7-10 days', '14+ days']
    return render_template('packages.html',
                           packages=filtered_packages,
                           duration_filter=duration_filter,
                           duration_options=duration_options)
@app.route('/trips')
def trips_page():
    '''
    Route for Trip Management page.
    Displays all created trips with options.
    '''
    trips = load_trips()
    return render_template('trips.html', trips=trips)
@app.route('/booking_confirmation/<booking_id>')
def booking_confirmation_page(booking_id):
    '''
    Route for Booking Confirmation page.
    Displays booking confirmation details.
    '''
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        booking = {
                            'booking_id': parts[0],
                            'trip_id': parts[1],
                            'booking_type': parts[2],
                            'booking_date': parts[3],
                            'amount': parts[4],
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }
                        bookings.append(booking)
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return "Booking not found", 404
    return render_template('booking_confirmation.html', booking=booking)
@app.route('/recommendations')
def recommendations_page():
    '''
    Route for Travel Recommendations page.
    Displays personalized recommendations and trending destinations.
    '''
    destinations = load_destinations()
    # For trending destinations, pick top 3 by example (no popularity data, so first 3)
    trending_destinations = destinations[:3]
    recommendation_season_filter = request.args.get('season', '').strip()
    budget_filter = request.args.get('budget', '').strip()
    # Filtering logic can be expanded; here we just pass filters to template
    seasons = ['All', 'Spring', 'Summer', 'Fall', 'Winter']
    budgets = ['All', 'Low', 'Medium', 'High']
    return render_template('recommendations.html',
                           trending_destinations=trending_destinations,
                           recommendation_season_filter=recommendation_season_filter,
                           budget_filter=budget_filter,
                           seasons=seasons,
                           budgets=budgets)
if __name__ == '__main__':
    app.run(debug=True)