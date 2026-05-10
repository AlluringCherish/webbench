'''
Main backend application implementing the TravelPlanner web app using Flask.
Handles routing for ten pages, processes user inputs, reads/writes data from/to local text files in the 'data/' directory,
and renders frontend templates with dynamic content.
'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import datetime
from fpdf import FPDF
import io
app = Flask(__name__)
app.secret_key = 'travelplanner_secret_key'
DATA_DIR = 'data'
# Utility functions to read/write data files
def read_destinations():
    path = os.path.join(DATA_DIR, 'destinations.txt')
    destinations = []
    if not os.path.exists(path):
        return destinations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
            destination = {
                'dest_id': parts[0],
                'name': parts[1],
                'country': parts[2],
                'region': parts[3],
                'description': parts[4],
                'attractions': parts[5],
                'climate': parts[6]
            }
            destinations.append(destination)
    return destinations
def read_itineraries():
    path = os.path.join(DATA_DIR, 'itineraries.txt')
    itineraries = []
    if not os.path.exists(path):
        return itineraries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
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
            ])
            f.write(line + '\n')
def read_hotels():
    path = os.path.join(DATA_DIR, 'hotels.txt')
    hotels = []
    if not os.path.exists(path):
        return hotels
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
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
    if not os.path.exists(path):
        return flights
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 9:
                continue
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
    if not os.path.exists(path):
        return packages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
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
    if not os.path.exists(path):
        return trips
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
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
            ])
            f.write(line + '\n')
def read_bookings():
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
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
            ])
            f.write(line + '\n')
def generate_new_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            cur_id = int(item[id_key])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    trips = read_trips()
    upcoming_trips = []
    today = datetime.date.today()
    for trip in trips:
        try:
            start_date = datetime.datetime.strptime(trip['start_date'], '%Y-%m-%d').date()
            if start_date >= today:
                upcoming_trips.append(trip)
        except:
            continue
    upcoming_trips = sorted(upcoming_trips, key=lambda x: x['start_date'])[:3]
    destinations = read_destinations()
    # For featured destinations, pick first 3 for simplicity
    featured_destinations = destinations[:3]
    return render_template('dashboard.html',
                           upcoming_trips=upcoming_trips,
                           featured_destinations=featured_destinations)
@app.route('/destinations')
def destinations():
    destinations = read_destinations()
    search_query = request.args.get('search', '').strip().lower()
    region_filter = request.args.get('region', '').strip()
    filtered_destinations = destinations
    if search_query:
        filtered_destinations = [d for d in filtered_destinations if search_query in d['name'].lower() or search_query in d['country'].lower()]
    if region_filter:
        filtered_destinations = [d for d in filtered_destinations if d['region'].lower() == region_filter.lower()]
    return render_template('destinations.html',
                           destinations=filtered_destinations,
                           search_query=search_query,
                           region_filter=region_filter)
@app.route('/destination/<dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = read_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if not destination:
        flash('Destination not found.', 'error')
        return redirect(url_for('destinations'))
    if request.method == 'POST':
        # Add destination to itinerary (simplified: redirect to itinerary page with prefill)
        return redirect(url_for('itinerary', prefill_destination=destination['name']))
    return render_template('destination_details.html', destination=destination)
@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = read_itineraries()
    destinations = read_destinations()
    prefill_destination = request.args.get('prefill_destination', '')
    if request.method == 'POST':
        itinerary_id = request.form.get('itinerary_id', '')
        itinerary_name = request.form.get('itinerary_name_input', '').strip()
        destination = request.form.get('destination_input', '').strip()
        start_date = request.form.get('start_date_input', '').strip()
        end_date = request.form.get('end_date_input', '').strip()
        activities = request.form.get('activities_input', '').strip()
        status = request.form.get('status_input', 'Planned').strip()
        if not itinerary_name or not destination or not start_date or not end_date:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('itinerary', prefill_destination=destination))
        if itinerary_id:  # Update existing
            found = False
            for it in itineraries:
                if it['itinerary_id'] == itinerary_id:
                    it['itinerary_name'] = itinerary_name
                    it['destination'] = destination
                    it['start_date'] = start_date
                    it['end_date'] = end_date
                    it['activities'] = activities
                    it['status'] = status
                    found = True
                    break
            if found:
                write_itineraries(itineraries)
                flash('Itinerary updated successfully.', 'success')
            else:
                flash('Itinerary not found.', 'error')
        else:  # Create new
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
            flash('New itinerary created successfully.', 'success')
        return redirect(url_for('itinerary'))
    return render_template('itinerary.html',
                           itineraries=itineraries,
                           destinations=destinations,
                           prefill_destination=prefill_destination)
@app.route('/itinerary/delete/<itinerary_id>', methods=['POST'])
def delete_itinerary(itinerary_id):
    itineraries = read_itineraries()
    new_itineraries = [it for it in itineraries if it['itinerary_id'] != itinerary_id]
    if len(new_itineraries) == len(itineraries):
        flash('Itinerary not found.', 'error')
    else:
        write_itineraries(new_itineraries)
        flash('Itinerary deleted successfully.', 'success')
    return redirect(url_for('itinerary'))
@app.route('/accommodations')
def accommodations():
    hotels = read_hotels()
    destination_input = request.args.get('destination', '').strip().lower()
    check_in_date = request.args.get('check_in_date', '').strip()
    check_out_date = request.args.get('check_out_date', '').strip()
    price_filter = request.args.get('price_filter', '').strip().lower()
    filtered_hotels = hotels
    if destination_input:
        filtered_hotels = [h for h in filtered_hotels if h['city'].lower() == destination_input]
    if price_filter:
        if price_filter == 'budget':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] < 100]
        elif price_filter == 'mid-range':
            filtered_hotels = [h for h in filtered_hotels if 100 <= h['price_per_night'] <= 300]
        elif price_filter == 'luxury':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] > 300]
    return render_template('accommodations.html',
                           hotels=filtered_hotels,
                           destination=destination_input,
                           check_in_date=check_in_date,
                           check_out_date=check_out_date,
                           price_filter=price_filter)
@app.route('/transportation')
def transportation():
    flights = read_flights()
    departure_city = request.args.get('departure_city', '').strip().lower()
    arrival_city = request.args.get('arrival_city', '').strip().lower()
    departure_date = request.args.get('departure_date', '').strip()
    flight_class_filter = request.args.get('flight_class_filter', '').strip()
    filtered_flights = flights
    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city]
    if flight_class_filter:
        filtered_flights = [f for f in filtered_flights if f['class_type'].lower() == flight_class_filter.lower()]
    return render_template('transportation.html',
                           flights=filtered_flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           departure_date=departure_date,
                           flight_class_filter=flight_class_filter)
@app.route('/packages')
def packages():
    packages = read_packages()
    duration_filter = request.args.get('duration_filter', '').strip()
    filtered_packages = packages
    if duration_filter:
        if duration_filter == '3-5 days':
            filtered_packages = [p for p in filtered_packages if 3 <= p['duration_days'] <= 5]
        elif duration_filter == '7-10 days':
            filtered_packages = [p for p in filtered_packages if 7 <= p['duration_days'] <= 10]
        elif duration_filter == '14+ days':
            filtered_packages = [p for p in filtered_packages if p['duration_days'] >= 14]
    return render_template('packages.html',
                           packages=filtered_packages,
                           duration_filter=duration_filter)
@app.route('/package/<pkg_id>', methods=['GET'])
def package_details(pkg_id):
    packages = read_packages()
    package = next((p for p in packages if p['package_id'] == pkg_id), None)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('packages'))
    return render_template('package_details.html', package=package)
@app.route('/package/book/<pkg_id>', methods=['POST'])
def book_package(pkg_id):
    packages = read_packages()
    trips = read_trips()
    bookings = read_bookings()
    package = next((p for p in packages if p['package_id'] == pkg_id), None)
    if not package:
        flash('Package not found.', 'error')
        return redirect(url_for('packages'))
    new_trip_id = generate_new_id(trips, 'trip_id')
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    trip_name = f"{package['package_name']} Trip"
    new_trip = {
        'trip_id': new_trip_id,
        'trip_name': trip_name,
        'destination': package['destination'],
        'start_date': '',
        'end_date': '',
        'total_budget': package['price'],
        'status': 'Pending',
        'created_date': today_str
    }
    trips.append(new_trip)
    write_trips(trips)
    new_booking_id = generate_new_id(bookings, 'booking_id')
    confirmation_number = f"CONF{new_booking_id.zfill(3)}"
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
    flash('Package booked successfully. Please check your trip details.', 'success')
    return redirect(url_for('trips'))
@app.route('/trips')
def trips():
    trips = read_trips()
    return render_template('trips.html', trips=trips)
@app.route('/trip/<trip_id>')
def view_trip(trip_id):
    trips = read_trips()
    bookings = read_bookings()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('trips'))
    trip_bookings = [b for b in bookings if b['trip_id'] == trip_id]
    return render_template('trip_details.html', trip=trip, bookings=trip_bookings)
@app.route('/trip/edit/<trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('trips'))
    if request.method == 'POST':
        trip_name = request.form.get('trip_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        total_budget = request.form.get('total_budget', '').strip()
        status = request.form.get('status', '').strip()
        if not trip_name or not destination or not start_date or not end_date or not total_budget:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('edit_trip', trip_id=trip_id))
        try:
            total_budget_val = float(total_budget)
        except:
            flash('Invalid budget value.', 'error')
            return redirect(url_for('edit_trip', trip_id=trip_id))
        trip['trip_name'] = trip_name
        trip['destination'] = destination
        trip['start_date'] = start_date
        trip['end_date'] = end_date
        trip['total_budget'] = total_budget_val
        trip['status'] = status
        write_trips(trips)
        flash('Trip updated successfully.', 'success')
        return redirect(url_for('view_trip', trip_id=trip_id))
    return render_template('edit_trip.html', trip=trip)
@app.route('/trip/delete/<trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trips = read_trips()
    bookings = read_bookings()
    new_trips = [t for t in trips if t['trip_id'] != trip_id]
    if len(new_trips) == len(trips):
        flash('Trip not found.', 'error')
    else:
        write_trips(new_trips)
        new_bookings = [b for b in bookings if b['trip_id'] != trip_id]
        write_bookings(new_bookings)
        flash('Trip and related bookings deleted successfully.', 'success')
    return redirect(url_for('trips'))
@app.route('/booking/confirmation/<confirmation_number>')
def booking_confirmation(confirmation_number):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['confirmation_number'] == confirmation_number), None)
    if not booking:
        flash('Booking not found.', 'error')
        return redirect(url_for('dashboard'))
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == booking['trip_id']), None)
    return render_template('booking_confirmation.html', booking=booking, trip=trip)
@app.route('/itinerary/download/<trip_id>')
def download_itinerary(trip_id):
    trips = read_trips()
    itineraries = read_itineraries()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('trips'))
    related_itineraries = [it for it in itineraries if it['destination'].lower() == trip['destination'].lower()]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Trip Itinerary: {trip['trip_name']}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Destination: {trip['destination']}", ln=True)
    pdf.cell(0, 10, f"Start Date: {trip['start_date']}", ln=True)
    pdf.cell(0, 10, f"End Date: {trip['end_date']}", ln=True)
    pdf.cell(0, 10, f"Total Budget: ${trip['total_budget']:.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "Planned Itineraries:", ln=True)
    if related_itineraries:
        for it in related_itineraries:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"{it['itinerary_name']} ({it['start_date']} to {it['end_date']})", ln=True)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, f"Activities: {it['activities']}")
            pdf.ln(5)
    else:
        pdf.cell(0, 10, "No itineraries found for this destination.", ln=True)
    pdf_output = pdf.output(dest='S').encode('latin1')
    return send_file(io.BytesIO(pdf_output),
                     mimetype='application/pdf',
                     as_attachment=True,
                     download_name=f"{trip['trip_name']}_itinerary.pdf")
@app.route('/booking/share/<trip_id>', methods=['POST'])
def share_trip(trip_id):
    # For simplicity, just flash a message that sharing is done.
    # Real implementation would integrate email or social media APIs.
    trips = read_trips()
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('trips'))
    flash(f"Trip '{trip['trip_name']}' shared successfully (simulated).", 'success')
    return redirect(url_for('trips'))
@app.route('/recommendations')
def recommendations():
    destinations = read_destinations()
    season_filter = request.args.get('season_filter', '').strip()
    budget_filter = request.args.get('budget_filter', '').strip()
    filtered_destinations = destinations
    if season_filter:
        season = season_filter.lower()
        if season == 'summer':
            filtered_destinations = [d for d in filtered_destinations if d['climate'].lower() in ['tropical', 'temperate']]
        elif season == 'winter':
            filtered_destinations = [d for d in filtered_destinations if d['climate'].lower() == 'temperate']
        else:
            filtered_destinations = [d for d in filtered_destinations if d['climate'].lower() == 'temperate']
    # Budget filter is ignored here as no budget data in destinations
    trending_destinations = destinations[:5]  # For demo, top 5 as trending
    return render_template('recommendations.html',
                           trending_destinations=trending_destinations,
                           season_filter=season_filter,
                           budget_filter=budget_filter,
                           destinations=filtered_destinations)
# Navigation helpers for buttons that redirect to other pages
@app.route('/navigate/browse_destinations')
def navigate_browse_destinations():
    return redirect(url_for('destinations'))
@app.route('/navigate/plan_itinerary')
def navigate_plan_itinerary():
    return redirect(url_for('itinerary'))
@app.route('/navigate/back_to_dashboard')
def navigate_back_to_dashboard():
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)