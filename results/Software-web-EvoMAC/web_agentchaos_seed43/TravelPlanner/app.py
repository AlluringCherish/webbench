'''
Main application file for TravelPlanner web application.
Defines the root route '/' to serve the Dashboard page as the first page of the website,
and other routes for the different pages as per requirements.
Implements data loading and processing for each page from local text files.
Ensures navigation and data integration for all 10 required pages.
'''
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import datetime
import io
from fpdf import FPDF
app = Flask(__name__)
DATA_DIR = 'data'
def load_destinations():
    destinations = []
    try:
        with open(os.path.join(DATA_DIR, 'destinations.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return destinations
def load_trips():
    trips = []
    try:
        with open(os.path.join(DATA_DIR, 'trips.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return trips
def load_itineraries():
    itineraries = []
    try:
        with open(os.path.join(DATA_DIR, 'itineraries.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return itineraries
def load_hotels():
    hotels = []
    try:
        with open(os.path.join(DATA_DIR, 'hotels.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
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
    except FileNotFoundError:
        pass
    return hotels
def load_flights():
    flights = []
    try:
        with open(os.path.join(DATA_DIR, 'flights.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return flights
def load_packages():
    packages = []
    try:
        with open(os.path.join(DATA_DIR, 'packages.txt'), 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return packages
def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
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
                            'amount': float(parts[4]),
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }
                        bookings.append(booking)
    except FileNotFoundError:
        pass
    return bookings
def save_itineraries(itineraries):
    try:
        with open(os.path.join(DATA_DIR, 'itineraries.txt'), 'w', encoding='utf-8') as f:
            for it in itineraries:
                line = '|'.join([
                    it['itinerary_id'],
                    it['itinerary_name'],
                    it['destination'],
                    it['start_date'],
                    it['end_date'],
                    it['activities'],
                    it['status']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error saving itineraries: {e}")
def save_trips(trips):
    try:
        with open(os.path.join(DATA_DIR, 'trips.txt'), 'w', encoding='utf-8') as f:
            for trip in trips:
                line = '|'.join([
                    trip['trip_id'],
                    trip['trip_name'],
                    trip['destination'],
                    trip['start_date'],
                    trip['end_date'],
                    trip['total_budget'],
                    trip['status'],
                    trip['created_date']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error saving trips: {e}")
def save_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for booking in bookings:
                line = '|'.join([
                    booking['booking_id'],
                    booking['trip_id'],
                    booking['booking_type'],
                    booking['booking_date'],
                    f"{booking['amount']:.2f}",
                    booking['confirmation_number'],
                    booking['status']
                ])
                f.write(line + '\n')
    except Exception as e:
        print(f"Error saving bookings: {e}")
@app.route('/')
def dashboard():
    '''
    Root route serving the Dashboard page as the first page of the website.
    Loads featured destinations and upcoming trips to display.
    '''
    destinations = load_destinations()
    featured_destinations = destinations[:3]  # first 3 featured
    trips = load_trips()
    # Filter upcoming trips: start_date >= today
    today = datetime.date.today()
    upcoming_trips = []
    for trip in trips:
        try:
            start_date = datetime.datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
            if start_date >= today:
                upcoming_trips.append(trip)
        except:
            continue
    upcoming_trips = upcoming_trips[:3]
    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)
@app.route('/destinations', methods=['GET'])
def destinations_page():
    '''
    Displays all available travel destinations with search and filter capabilities.
    '''
    destinations = load_destinations()
    search_query = request.args.get('search', '').strip().lower()
    region_filter = request.args.get('region', '').strip()
    filtered_destinations = destinations
    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query in d['name'].lower() or search_query in d['country'].lower()]
    if region_filter and region_filter != 'All':
        filtered_destinations = [d for d in filtered_destinations if d['region'] == region_filter]
    regions = ['All', 'Asia', 'Europe', 'Americas', 'Africa', 'Oceania']
    return render_template('destinations.html',
                           destinations=filtered_destinations,
                           search_query=search_query,
                           region_filter=region_filter,
                           regions=regions)
@app.route('/destination/<dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    '''
    Displays detailed information about a specific destination.
    Allows adding destination to trip (redirects to itinerary page with pre-filled destination).
    '''
    destinations = load_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        return "Destination not found", 404
    if request.method == 'POST':
        # Add to trip: redirect to itinerary page with destination pre-filled
        return redirect(url_for('itinerary_page', destination=destination['name']))
    return render_template('destination_details.html',
                           destination=destination)
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_page():
    '''
    Page for users to create and manage travel itineraries with activities and schedules.
    Supports adding new itinerary and deleting existing ones.
    '''
    itineraries = load_itineraries()
    destinations = [d['name'] for d in load_destinations()]
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            # Add new itinerary
            itinerary_name = request.form.get('itinerary_name', '').strip()
            destination = request.form.get('destination', '').strip()
            start_date = request.form.get('start_date', '').strip()
            end_date = request.form.get('end_date', '').strip()
            activities = request.form.get('activities', '').strip()
            status = 'Planned'
            if itinerary_name and destination and start_date and end_date:
                # Generate new itinerary_id
                if itineraries:
                    new_id = str(int(max(it['itinerary_id'] for it in itineraries)) + 1)
                else:
                    new_id = '1'
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
                save_itineraries(itineraries)
                return redirect(url_for('itinerary_page'))
        elif action == 'delete':
            # Delete itinerary by id
            del_id = request.form.get('delete_id')
            itineraries = [it for it in itineraries if it['itinerary_id'] != del_id]
            save_itineraries(itineraries)
            return redirect(url_for('itinerary_page'))
    # Pre-fill destination if passed as query param
    prefill_destination = request.args.get('destination', '')
    return render_template('itinerary_planning.html',
                           itineraries=itineraries,
                           destinations=destinations,
                           prefill_destination=prefill_destination)
@app.route('/accommodations', methods=['GET'])
def accommodations_page():
    '''
    Page for searching and browsing hotel options with filters and pricing.
    '''
    hotels = load_hotels()
    destination_input = request.args.get('destination', '').strip()
    check_in_date = request.args.get('check_in_date', '').strip()
    check_out_date = request.args.get('check_out_date', '').strip()
    price_filter = request.args.get('price_filter', '').strip()
    filtered_hotels = hotels
    if destination_input:
        filtered_hotels = [h for h in filtered_hotels if h['city'].lower() == destination_input.lower()]
    if price_filter and price_filter != 'All':
        filtered_hotels = [h for h in filtered_hotels if h['category'] == price_filter]
    price_categories = ['All', 'Budget', 'Mid-range', 'Luxury']
    return render_template('accommodations.html',
                           hotels=filtered_hotels,
                           destination_input=destination_input,
                           check_in_date=check_in_date,
                           check_out_date=check_out_date,
                           price_filter=price_filter,
                           price_categories=price_categories)
@app.route('/transportation', methods=['GET'])
def transportation_page():
    '''
    Page for searching and booking flights with departure and arrival options.
    '''
    flights = load_flights()
    departure_city = request.args.get('departure_city', '').strip()
    arrival_city = request.args.get('arrival_city', '').strip()
    departure_date = request.args.get('departure_date', '').strip()
    flight_class_filter = request.args.get('flight_class_filter', '').strip()
    filtered_flights = flights
    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city.lower()]
    if flight_class_filter and flight_class_filter != 'All':
        filtered_flights = [f for f in filtered_flights if f['class_type'] == flight_class_filter]
    flight_classes = ['All', 'Economy', 'Business', 'First Class']
    return render_template('transportation.html',
                           flights=filtered_flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           departure_date=departure_date,
                           flight_class_filter=flight_class_filter,
                           flight_classes=flight_classes)
@app.route('/packages', methods=['GET', 'POST'])
def packages_page():
    '''
    Displays pre-designed travel packages with complete trip information.
    Supports filtering by duration and booking packages.
    '''
    packages = load_packages()
    duration_filter = request.args.get('duration_filter', '').strip()
    filtered_packages = packages
    if duration_filter and duration_filter != 'All':
        if duration_filter == '3-5 days':
            filtered_packages = [p for p in filtered_packages if 3 <= p['duration_days'] <= 5]
        elif duration_filter == '7-10 days':
            filtered_packages = [p for p in filtered_packages if 7 <= p['duration_days'] <= 10]
        elif duration_filter == '14+ days':
            filtered_packages = [p for p in filtered_packages if p['duration_days'] >= 14]
    duration_options = ['All', '3-5 days', '7-10 days', '14+ days']
    if request.method == 'POST':
        # Booking a package
        pkg_id = request.form.get('package_id')
        package = next((p for p in packages if p['package_id'] == pkg_id), None)
        if package:
            # Create a new trip and booking for the package
            trips = load_trips()
            bookings = load_bookings()
            # Generate new trip_id
            if trips:
                new_trip_id = str(int(max(t['trip_id'] for t in trips)) + 1)
            else:
                new_trip_id = '1'
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            new_trip = {
                'trip_id': new_trip_id,
                'trip_name': package['package_name'],
                'destination': package['destination'],
                'start_date': '',  # User to fill later
                'end_date': '',
                'total_budget': f"{package['price']:.2f}",
                'status': 'Pending',
                'created_date': today_str
            }
            trips.append(new_trip)
            save_trips(trips)
            # Create booking
            if bookings:
                new_booking_id = str(int(max(b['booking_id'] for b in bookings)) + 1)
            else:
                new_booking_id = '1'
            new_booking = {
                'booking_id': new_booking_id,
                'trip_id': new_trip_id,
                'booking_type': 'Package',
                'booking_date': today_str,
                'amount': package['price'],
                'confirmation_number': f"CONF{new_booking_id.zfill(3)}",
                'status': 'Pending'
            }
            bookings.append(new_booking)
            save_bookings(bookings)
            return redirect(url_for('booking_confirmation_page', confirmation_number=new_booking['confirmation_number']))
    return render_template('travel_packages.html',
                           packages=filtered_packages,
                           duration_filter=duration_filter,
                           duration_options=duration_options)
@app.route('/trips', methods=['GET', 'POST'])
def trips_page():
    '''
    Displays all created trips with options to view, edit, or delete them.
    '''
    trips = load_trips()
    if request.method == 'POST':
        action = request.form.get('action')
        trip_id = request.form.get('trip_id')
        if action == 'delete':
            trips = [t for t in trips if t['trip_id'] != trip_id]
            save_trips(trips)
            return redirect(url_for('trips_page'))
        elif action == 'edit':
            # For simplicity, redirect to itinerary page with trip info to edit
            trip = next((t for t in trips if t['trip_id'] == trip_id), None)
            if trip:
                # Redirect to itinerary page with trip name as itinerary name and destination prefilled
                return redirect(url_for('itinerary_page', destination=trip['destination']))
    return render_template('trip_management.html',
                           trips=trips)
@app.route('/booking-confirmation', methods=['GET'])
def booking_confirmation_page():
    '''
    Displays booking confirmation details with reservation information.
    Supports downloading itinerary as PDF and sharing trip details.
    '''
    confirmation_number = request.args.get('confirmation_number', '')
    bookings = load_bookings()
    booking = next((b for b in bookings if b['confirmation_number'] == confirmation_number), None)
    if not booking:
        return "Booking not found", 404
    trips = load_trips()
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html',
                           booking=booking,
                           trip=trip)
@app.route('/download-itinerary/<trip_id>')
def download_itinerary(trip_id):
    '''
    Generates and sends a PDF itinerary for the given trip_id.
    '''
    trips = load_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        return "Trip not found", 404
    itineraries = load_itineraries()
    itinerary = next((it for it in itineraries if it['destination'] == trip['destination'] and it['start_date'] == trip['start_date']), None)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Trip Itinerary: {trip['trip_name']}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Destination: {trip['destination']}", ln=True)
    pdf.cell(0, 10, f"Start Date: {trip['start_date']}", ln=True)
    pdf.cell(0, 10, f"End Date: {trip['end_date']}", ln=True)
    pdf.cell(0, 10, f"Total Budget: ${trip['total_budget']}", ln=True)
    pdf.cell(0, 10, f"Status: {trip['status']}", ln=True)
    pdf.ln(10)
    if itinerary:
        pdf.cell(0, 10, "Activities:", ln=True)
        activities = itinerary['activities'].split(',') if itinerary['activities'] else []
        for act in activities:
            pdf.cell(0, 10, f"- {act.strip()}", ln=True)
    else:
        pdf.cell(0, 10, "No itinerary activities found.", ln=True)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return send_file(pdf_output, attachment_filename=f"itinerary_{trip_id}.pdf", as_attachment=True)
@app.route('/recommendations', methods=['GET'])
def recommendations_page():
    '''
    Displays personalized travel recommendations and trending destinations.
    Supports filtering by travel season and budget range.
    '''
    destinations = load_destinations()
    # For trending destinations, rank by popularity - here we simulate by order in file
    trending_destinations = destinations[:5]
    recommendation_season_filter = request.args.get('recommendation_season_filter', '').strip()
    budget_filter = request.args.get('budget_filter', '').strip()
    # Filter trending destinations by season and budget (simulate with climate and region)
    filtered_destinations = trending_destinations
    # Season filter (Spring, Summer, Fall, Winter) - simulate by climate
    if recommendation_season_filter and recommendation_season_filter != 'All':
        # Simple mapping: Temperate = Spring/Fall, Tropical = Summer, Winter = Winter
        season_map = {
            'Spring': ['Temperate'],
            'Summer': ['Tropical'],
            'Fall': ['Temperate'],
            'Winter': ['Cold', 'Temperate']  # Assume Temperate can be winter too
        }
        allowed_climates = season_map.get(recommendation_season_filter, [])
        filtered_destinations = [d for d in filtered_destinations if d['climate'] in allowed_climates]
    # Budget filter (Low, Medium, High) - simulate by region or climate (no direct data)
    # For demo, Low = Americas, Medium = Asia, High = Europe/Oceania/Africa
    if budget_filter and budget_filter != 'All':
        budget_map = {
            'Low': ['Americas'],
            'Medium': ['Asia'],
            'High': ['Europe', 'Oceania', 'Africa']
        }
        allowed_regions = budget_map.get(budget_filter, [])
        filtered_destinations = [d for d in filtered_destinations if d['region'] in allowed_regions]
    seasons = ['All', 'Spring', 'Summer', 'Fall', 'Winter']
    budgets = ['All', 'Low', 'Medium', 'High']
    return render_template('travel_recommendations.html',
                           trending_destinations=filtered_destinations,
                           recommendation_season_filter=recommendation_season_filter,
                           budget_filter=budget_filter,
                           seasons=seasons,
                           budgets=budgets)
# Navigation routes for buttons that redirect to other pages
@app.route('/navigate/<page>')
def navigate(page):
    '''
    Helper route to navigate to pages via buttons.
    '''
    page_map = {
        'destinations': 'destinations_page',
        'itinerary': 'itinerary_page',
        'accommodations': 'accommodations_page',
        'transportation': 'transportation_page',
        'packages': 'packages_page',
        'trips': 'trips_page',
        'booking-confirmation': 'booking_confirmation_page',
        'recommendations': 'recommendations_page',
        'dashboard': 'dashboard'
    }
    endpoint = page_map.get(page)
    if endpoint:
        return redirect(url_for(endpoint))
    else:
        return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)