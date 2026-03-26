'''
Backend Python application for the TravelPlanner web application.
Implements all routes and data handling as per requirements.
Uses Flask framework and reads/writes data from/to local text files in 'data/' directory.
No authentication required; all features directly accessible.
'''
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
import io
app = Flask(__name__)
app.secret_key = 'travelplanner_secret_key'
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions to read and write data files
def read_destinations():
    path = os.path.join(DATA_DIR, 'destinations.txt')
    destinations = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
def read_itineraries():
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    itineraries = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
def write_itineraries(itineraries):
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for it in itineraries:
            line = '|'.join([
                it['itinerary_id'],
                it['itinerary_name'],
                it['destination'],
                it['start_date'],
                it['end_date'],
                it['activities'],
                it['status']
            ]) + '\n'
            f.write(line)
def read_hotels():
    path = os.path.join(DATA_DIR, 'hotels.txt')
    hotels = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    hotel = {
                        'hotel_id': parts[0],
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
    path = os.path.join(DATA_DIR, 'flights.txt')
    flights = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    return flights
def read_packages():
    path = os.path.join(DATA_DIR, 'packages.txt')
    packages = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    return packages
def read_trips():
    path = os.path.join(DATA_DIR, 'trips.txt')
    trips = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    trip = {
                        'trip_id': parts[0],
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
    path = os.path.join(DATA_DIR, 'trips.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for trip in trips:
            line = '|'.join([
                trip['trip_id'],
                trip['trip_name'],
                trip['destination'],
                trip['start_date'],
                trip['end_date'],
                f"{trip['total_budget']:.2f}",
                trip['status'],
                trip['created_date']
            ]) + '\n'
            f.write(line)
def read_bookings():
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    booking = {
                        'booking_id': parts[0],
                        'trip_id': parts[1],
                        'booking_type': parts[2],
                        'booking_date': parts[3],
                        'amount': float(parts[4]),
                        'confirmation_number': parts[5],
                        'status': parts[6]
                    }
                    bookings.append(booking)
    return bookings
def write_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = '|'.join([
                b['booking_id'],
                b['trip_id'],
                b['booking_type'],
                b['booking_date'],
                f"{b['amount']:.2f}",
                b['confirmation_number'],
                b['status']
            ]) + '\n'
            f.write(line)
def generate_new_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except (ValueError, KeyError):
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    destinations = read_destinations()
    trips = read_trips()
    today = datetime.date.today()
    upcoming_trips = []
    for trip in trips:
        try:
            start_date = datetime.datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
        except ValueError:
            continue
        if start_date >= today and trip['status'].lower() in ['planned', 'in progress']:
            upcoming_trips.append(trip)
    upcoming_trips.sort(key=lambda x: x['start_date'])
    # Featured destinations: top 3 or all if less than 3
    featured_destinations = destinations[:3] if len(destinations) >= 3 else destinations
    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)
@app.route('/destinations')
def destinations():
    destinations = read_destinations()
    search_query = request.args.get('search-destination', '').strip().lower()
    region_filter = request.args.get('region-filter', 'All')
    filtered = []
    for dest in destinations:
        if search_query and search_query not in dest['name'].lower() and search_query not in dest['country'].lower():
            continue
        if region_filter != 'All' and dest['region'] != region_filter:
            continue
        filtered.append(dest)
    return render_template('destinations.html',
                           destinations=filtered,
                           search_query=search_query,
                           region_filter=region_filter)
@app.route('/destination/<dest_id>')
def destination_details(dest_id):
    destinations = read_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        abort(404)
    return render_template('destination_details.html', destination=destination)
@app.route('/itinerary_planning', methods=['GET', 'POST'])
def itinerary_planning():
    itineraries = read_itineraries()
    destinations = read_destinations()
    if request.method == 'POST':
        itinerary_name = request.form.get('itinerary-name-input', '').strip()
        destination = request.form.get('destination-input', '').strip()
        start_date = request.form.get('start-date-input', '').strip()
        end_date = request.form.get('end-date-input', '').strip()
        activities = request.form.get('activities-input', '').strip()
        status = 'Planned'
        if not itinerary_name or not destination or not start_date or not end_date:
            flash("Please fill in all required fields.")
            return redirect(url_for('itinerary_planning'))
        new_id = generate_new_id(itineraries, 'itinerary_id')
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
        flash("Itinerary added successfully.")
        return redirect(url_for('itinerary_planning'))
    return render_template('itinerary_planning.html', itineraries=itineraries, destinations=destinations)
@app.route('/itinerary/delete/<itinerary_id>', methods=['POST'])
def delete_itinerary(itinerary_id):
    itineraries = read_itineraries()
    new_itineraries = [it for it in itineraries if it['itinerary_id'] != itinerary_id]
    if len(new_itineraries) == len(itineraries):
        flash("Itinerary not found.")
    else:
        write_itineraries(new_itineraries)
        flash("Itinerary deleted successfully.")
    return redirect(url_for('itinerary_planning'))
@app.route('/accommodations')
def accommodations():
    hotels = read_hotels()
    destination_input = request.args.get('destination-input', '').strip().lower()
    check_in_date = request.args.get('check-in-date', '')
    check_out_date = request.args.get('check-out-date', '')
    price_filter = request.args.get('price-filter', 'All')
    price_map = {
        'Budget': (0, 100),
        'Mid-range': (100, 300),
        'Luxury': (300, 10000)
    }
    filtered = []
    for hotel in hotels:
        if destination_input and destination_input not in hotel['city'].lower():
            continue
        if price_filter != 'All':
            low, high = price_map.get(price_filter, (0, 10000))
            if not (low <= hotel['price_per_night'] <= high):
                continue
        filtered.append(hotel)
    return render_template('accommodations.html',
                           hotels=filtered,
                           destination_input=destination_input,
                           check_in_date=check_in_date,
                           check_out_date=check_out_date,
                           price_filter=price_filter)
@app.route('/transportation')
def transportation():
    flights = read_flights()
    departure_city = request.args.get('departure-city', '').strip().lower()
    arrival_city = request.args.get('arrival-city', '').strip().lower()
    departure_date = request.args.get('departure-date', '')
    flight_class_filter = request.args.get('flight-class-filter', 'All')
    filtered = []
    for flight in flights:
        if departure_city and departure_city != flight['departure_city'].lower():
            continue
        if arrival_city and arrival_city != flight['arrival_city'].lower():
            continue
        if flight_class_filter != 'All' and flight['class_type'] != flight_class_filter:
            continue
        filtered.append(flight)
    return render_template('transportation.html',
                           flights=filtered,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           departure_date=departure_date,
                           flight_class_filter=flight_class_filter)
@app.route('/travel_packages')
def travel_packages():
    packages = read_packages()
    duration_filter = request.args.get('duration-filter', 'All')
    filtered = []
    for package in packages:
        if duration_filter == 'All':
            filtered.append(package)
        elif duration_filter == '3-5 days':
            if 3 <= package['duration_days'] <= 5:
                filtered.append(package)
        elif duration_filter == '7-10 days':
            if 7 <= package['duration_days'] <= 10:
                filtered.append(package)
        elif duration_filter == '14+ days':
            if package['duration_days'] >= 14:
                filtered.append(package)
    return render_template('travel_packages.html',
                           packages=filtered,
                           duration_filter=duration_filter)
@app.route('/travel_packages/<pkg_id>')
def travel_package_details(pkg_id):
    packages = read_packages()
    package = next((p for p in packages if p['package_id'] == pkg_id), None)
    if not package:
        abort(404)
    return render_template('travel_package_details.html', package=package)
@app.route('/travel_packages/<pkg_id>/book', methods=['POST'])
def book_package(pkg_id):
    packages = read_packages()
    package = next((p for p in packages if p['package_id'] == pkg_id), None)
    if not package:
        flash("Package not found.")
        return redirect(url_for('travel_packages'))
    trips = read_trips()
    bookings = read_bookings()
    new_trip_id = generate_new_id(trips, 'trip_id')
    new_booking_id = generate_new_id(bookings, 'booking_id')
    today_str = datetime.date.today().isoformat()
    confirmation_number = f"CONF{new_booking_id.zfill(3)}"
    new_trip = {
        'trip_id': new_trip_id,
        'trip_name': f"{package['package_name']} Trip",
        'destination': package['destination'],
        'start_date': today_str,
        'end_date': today_str,
        'total_budget': package['price'],
        'status': 'Pending',
        'created_date': today_str
    }
    trips.append(new_trip)
    write_trips(trips)
    new_booking = {
        'booking_id': new_booking_id,
        'trip_id': new_trip_id,
        'booking_type': 'Package',
        'booking_date': today_str,
        'amount': package['price'],
        'confirmation_number': confirmation_number,
        'status': 'Pending'
    }
    bookings.append(new_booking)
    write_bookings(bookings)
    flash("Package successfully booked.")
    return redirect(url_for('booking_confirmation', confirmation_number=confirmation_number))
@app.route('/trips')
def trip_management():
    trips = read_trips()
    return render_template('trip_management.html', trips=trips)
@app.route('/trips/<trip_id>')
def view_trip_details(trip_id):
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash("Trip not found.")
        return redirect(url_for('trip_management'))
    return render_template('trip_details.html', trip=trip)
@app.route('/trips/edit/<trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash("Trip not found.")
        return redirect(url_for('trip_management'))
    if request.method == 'POST':
        trip_name = request.form.get('trip-name-input', trip['trip_name']).strip()
        destination = request.form.get('destination-input', trip['destination']).strip()
        start_date = request.form.get('start-date-input', trip['start_date']).strip()
        end_date = request.form.get('end-date-input', trip['end_date']).strip()
        total_budget_str = request.form.get('total-budget-input', f"{trip['total_budget']:.2f}").strip()
        status = request.form.get('status-input', trip['status']).strip()
        try:
            total_budget = float(total_budget_str)
        except ValueError:
            flash("Invalid total budget value.")
            return redirect(url_for('edit_trip', trip_id=trip_id))
        trip['trip_name'] = trip_name
        trip['destination'] = destination
        trip['start_date'] = start_date
        trip['end_date'] = end_date
        trip['total_budget'] = total_budget
        trip['status'] = status
        write_trips(trips)
        flash("Trip updated successfully.")
        return redirect(url_for('trip_management'))
    return render_template('edit_trip.html', trip=trip)
@app.route('/trips/delete/<trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trips = read_trips()
    new_trips = [t for t in trips if t['trip_id'] != trip_id]
    if len(new_trips) == len(trips):
        flash("Trip not found.")
    else:
        write_trips(new_trips)
        flash("Trip deleted successfully.")
    return redirect(url_for('trip_management'))
@app.route('/booking_confirmation/<confirmation_number>')
def booking_confirmation(confirmation_number):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['confirmation_number'] == confirmation_number), None)
    if not booking:
        abort(404)
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html',
                           booking=booking,
                           trip=trip)
@app.route('/download_itinerary/<trip_id>')
def download_itinerary(trip_id):
    itineraries = read_itineraries()
    itinerary = next((it for it in itineraries if it['itinerary_id'] == trip_id), None)
    if not itinerary:
        abort(404)
    itinerary_text = f"Itinerary Name: {itinerary['itinerary_name']}\nDestination: {itinerary['destination']}\nStart Date: {itinerary['start_date']}\nEnd Date: {itinerary['end_date']}\nActivities: {itinerary['activities']}\nStatus: {itinerary['status']}\n"
    return send_file(io.BytesIO(itinerary_text.encode('utf-8')),
                     mimetype='text/plain',
                     as_attachment=True,
                     download_name=f"itinerary_{trip_id}.txt")
@app.route('/travel_recommendations')
def travel_recommendations():
    destinations = read_destinations()
    trips = read_trips()
    recommendation_season_filter = request.args.get('recommendation-season-filter', 'All')
    budget_filter = request.args.get('budget-filter', 'All')
    # Calculate popularity by counting planned trips per destination
    popularity = {}
    for trip in trips:
        if trip['status'].lower() == 'planned':
            dest = trip['destination']
            popularity[dest] = popularity.get(dest, 0) + 1
    # Season to climate mapping
    season_climate_map = {
        'Spring': ['Temperate'],
        'Summer': ['Tropical', 'Temperate'],
        'Fall': ['Temperate'],
        'Winter': ['Temperate']
    }
    # Budget to regions mapping (example)
    budget_region_map = {
        'Low': ['Americas', 'Africa'],
        'Medium': ['Asia', 'Oceania'],
        'High': ['Europe']
    }
    filtered = []
    for dest in destinations:
        # Filter by season/climate
        if recommendation_season_filter != 'All':
            allowed_climates = season_climate_map.get(recommendation_season_filter, [])
            if dest['climate'] not in allowed_climates:
                continue
        # Filter by budget/region
        if budget_filter != 'All':
            allowed_regions = budget_region_map.get(budget_filter, [])
            if dest['region'] not in allowed_regions:
                continue
        filtered.append(dest)
    # Sort by popularity descending
    filtered.sort(key=lambda d: popularity.get(d['name'], 0), reverse=True)
    trending = filtered[:5]  # top 5 trending destinations
    return render_template('travel_recommendations.html',
                           trending_destinations=trending,
                           recommendation_season_filter=recommendation_season_filter,
                           budget_filter=budget_filter)
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=5000)