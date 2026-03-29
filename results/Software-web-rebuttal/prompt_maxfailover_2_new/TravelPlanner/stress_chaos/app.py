from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def load_pipe_delimited_data(filename):
    data_list = []
    if not os.path.exists(filename):
        # File missing, return empty list
        return data_list
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            data_list.append(fields)
    return data_list

@app.route('/')
def dashboard():
    raw_destinations = load_pipe_delimited_data('data/destinations.txt')
    featured_destinations = []
    for line in raw_destinations:
        if len(line) >= 4:
            dest_id = int(line[0])
            name = line[1]
            country = line[2]
            featured_destinations.append({'dest_id': dest_id, 'name': name, 'country': country})

    raw_trips = load_pipe_delimited_data('data/trips.txt')
    upcoming_trips = []
    for line in raw_trips:
        if len(line) >= 8:
            trip_id = int(line[0])
            trip_name = line[1]
            start_date = line[3]
            end_date = line[4]
            upcoming_trips.append({'trip_id': trip_id, 'trip_name': trip_name, 'start_date': start_date, 'end_date': end_date})

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    search_query = ''
    region_filter = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        region_filter = request.form.get('region_filter', '')
    raw = load_pipe_delimited_data('data/destinations.txt')
    destinations = []
    for line in raw:
        if len(line) >= 7:
            dest_id = int(line[0])
            name = line[1]
            country = line[2]
            region = line[3]
            if region_filter and region != region_filter:
                continue
            if search_query:
                if search_query.lower() not in name.lower() and search_query.lower() not in country.lower():
                    continue
            destinations.append({'dest_id': dest_id, 'name': name, 'country': country, 'region': region})

    return render_template('destinations.html', destinations=destinations, search_query=search_query, region_filter=region_filter)

@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    add_status = ''
    # Load all destinations and find the one with dest_id
    raw = load_pipe_delimited_data('data/destinations.txt')
    destination = None
    for line in raw:
        if len(line) >= 7 and int(line[0]) == dest_id:
            destination = {
                'dest_id': int(line[0]), 'name': line[1], 'country': line[2], 'description': line[4],
                'attractions': line[5], 'climate': line[6]
            }
            break
    if not destination:
        return redirect(url_for('destinations'))
    if request.method == 'POST':
        # 'Add to trip' action, simulate success message
        add_status = f"Destination {destination['name']} added to your trip successfully."

    return render_template('destination_details.html', destination=destination, add_status=add_status)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    # Load itineraries
    if request.method == 'POST':
        # Add a new activity from form
        itinerary_name = request.form.get('itinerary_name', '').strip()
        destination = request.form.get('destination', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        activities = request.form.get('activities', '').strip()
        status = request.form.get('status', 'Planned').strip()
        # Normally here would save to data store, but per spec no write
        # Just redirect to GET
        return redirect(url_for('itinerary'))

    raw = load_pipe_delimited_data('data/itineraries.txt')
    itineraries = []
    for line in raw:
        if len(line) >= 7:
            itineraries.append({
                'itinerary_id': int(line[0]),
                'itinerary_name': line[1],
                'destination': line[2],
                'start_date': line[3],
                'end_date': line[4],
                'activities': line[5],
                'status': line[6],
            })
    return render_template('itinerary.html', itineraries=itineraries)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    # default search params
    search_params = {'destination': '', 'check_in_date': '', 'check_out_date': '', 'price_filter': ''}
    if request.method == 'POST':
        search_params['destination'] = request.form.get('destination', '').strip()
        search_params['check_in_date'] = request.form.get('check_in_date', '').strip()
        search_params['check_out_date'] = request.form.get('check_out_date', '').strip()
        search_params['price_filter'] = request.form.get('price_filter', '')
    raw = load_pipe_delimited_data('data/hotels.txt')
    hotels = []
    for line in raw:
        if len(line) >= 7:
            hotel_id = int(line[0])
            name = line[1]
            city = line[2]
            rating = float(line[3])
            price_per_night = float(line[4])
            amenities = line[5]
            category = line[6]
            if search_params['destination'] and search_params['destination'].lower() not in city.lower():
                continue
            if search_params['price_filter'] and category != search_params['price_filter']:
                continue
            hotels.append({
                'hotel_id': hotel_id, 'name': name, 'city': city, 'rating': rating,
                'price_per_night': price_per_night, 'amenities': amenities, 'category': category
            })
    return render_template('accommodations.html', hotels=hotels, search_params=search_params)

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    search_params = {'departure_city': '', 'arrival_city': '', 'departure_date': '', 'flight_class_filter': ''}
    if request.method == 'POST':
        search_params['departure_city'] = request.form.get('departure_city', '').strip()
        search_params['arrival_city'] = request.form.get('arrival_city', '').strip()
        search_params['departure_date'] = request.form.get('departure_date', '').strip()
        search_params['flight_class_filter'] = request.form.get('flight_class_filter', '')
    raw = load_pipe_delimited_data('data/flights.txt')
    flights = []
    for line in raw:
        if len(line) >= 9:
            flight_id = int(line[0])
            airline = line[1]
            dep_city = line[2]
            arr_city = line[3]
            dep_time = line[4]
            arr_time = line[5]
            price = float(line[6])
            class_type = line[7]
            duration = line[8]
            if search_params['departure_city'] and search_params['departure_city'].lower() != dep_city.lower():
                continue
            if search_params['arrival_city'] and search_params['arrival_city'].lower() != arr_city.lower():
                continue
            if search_params['flight_class_filter'] and search_params['flight_class_filter'] != class_type:
                continue
            flights.append({
                'flight_id': flight_id, 'airline': airline, 'departure_city': dep_city, 'arrival_city': arr_city,
                'departure_time': dep_time, 'arrival_time': arr_time, 'price': price, 'class_type': class_type, 'duration': duration
            })
    return render_template('transportation.html', flights=flights, search_params=search_params)

@app.route('/packages')
def packages():
    filter_duration = request.args.get('filter_duration', '')
    raw = load_pipe_delimited_data('data/packages.txt')
    packages = []
    for line in raw:
        if len(line) >= 7:
            duration_days = int(line[3])
            if filter_duration:
                # filter_duration values: '3-5 days', '7-10 days', '14+ days'
                if filter_duration == '3-5 days' and not (3 <= duration_days <= 5):
                    continue
                elif filter_duration == '7-10 days' and not (7 <= duration_days <= 10):
                    continue
                elif filter_duration == '14+ days' and duration_days < 14:
                    continue
            packages.append({
                'package_id': int(line[0]), 'package_name': line[1], 'destination': line[2],
                'duration_days': duration_days, 'price': float(line[4]), 'included_items': line[5], 'difficulty_level': line[6]
            })
    return render_template('packages.html', packages=packages, filter_duration=filter_duration)

@app.route('/packages/<int:pkg_id>', methods=['GET','POST'])
def package_details(pkg_id):
    raw = load_pipe_delimited_data('data/packages.txt')
    package = None
    for line in raw:
        if len(line) >= 7 and int(line[0]) == pkg_id:
            package = {
                'package_id': int(line[0]), 'package_name': line[1], 'destination': line[2],
                'duration_days': int(line[3]), 'price': float(line[4]), 'included_items': line[5], 'difficulty_level': line[6]
            }
            break
    if not package:
        return redirect(url_for('packages'))
    if request.method == 'POST':
        # simulate booking then redirect to confirmation page or dashboard
        return redirect(url_for('dashboard'))
    return render_template('package_details.html', package=package)

@app.route('/trips')
def trips():
    raw = load_pipe_delimited_data('data/trips.txt')
    trips = []
    for line in raw:
        if len(line) >= 8:
            trips.append({
                'trip_id': int(line[0]), 'trip_name': line[1], 'destination': line[2],
                'start_date': line[3], 'end_date': line[4], 'status': line[6], 'total_budget': float(line[5])
            })
    return render_template('trips.html', trips=trips)

@app.route('/trips/<int:trip_id>')
def trip_details(trip_id):
    trip = None
    trips_raw = load_pipe_delimited_data('data/trips.txt')
    for line in trips_raw:
        if len(line) >= 8 and int(line[0]) == trip_id:
            trip = {
                'trip_id': int(line[0]), 'trip_name': line[1], 'destination': line[2],
                'start_date': line[3], 'end_date': line[4], 'total_budget': float(line[5]), 'status': line[6], 'created_date': line[7]
            }
            break
    if not trip:
        return redirect(url_for('trips'))
    bookings = []
    bookings_raw = load_pipe_delimited_data('data/bookings.txt')
    for line in bookings_raw:
        if len(line) >= 7 and int(line[1]) == trip_id:
            bookings.append({
                'booking_id': int(line[0]), 'booking_type': line[2], 'booking_date': line[3],
                'amount': float(line[4]), 'confirmation_number': line[5], 'status': line[6]
            })
    return render_template('trip_details.html', trip=trip, bookings=bookings)

@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    # Per spec no persistence, just redirect to trips after delete
    # In real app remove from data store
    return redirect(url_for('trips'))

@app.route('/recommendations')
def recommendations():
    season_filter = request.args.get('season_filter', '')
    budget_filter = request.args.get('budget_filter', '')
    raw = load_pipe_delimited_data('data/destinations.txt')
    trending_destinations = []
    for line in raw:
        if len(line) >= 7:
            # popularity_rank is not directly in destinations.txt but spec defines it
            # Given that on Section 1 it's listed, we only have region, not popularity_rank in destinations file
            # So we simulate popularity_rank from position
            trending_destinations.append({
                'dest_id': int(line[0]), 'name': line[1], 'country': line[2], 'popularity_rank': 0
            })
    return render_template('recommendations.html', trending_destinations=trending_destinations, season_filter=season_filter, budget_filter=budget_filter)

@app.route('/booking-confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    bookings_raw = load_pipe_delimited_data('data/bookings.txt')
    booking = None
    for line in bookings_raw:
        if len(line) >= 7 and int(line[0]) == booking_id:
            booking = {
                'booking_id': int(line[0]), 'trip_id': int(line[1]), 'booking_type': line[2], 'booking_date': line[3],
                'amount': float(line[4]), 'confirmation_number': line[5], 'status': line[6]
            }
            break
    if not booking:
        return redirect(url_for('dashboard'))
    trip = None
    trips_raw = load_pipe_delimited_data('data/trips.txt')
    for line in trips_raw:
        if len(line) >= 8 and int(line[0]) == booking['trip_id']:
            trip = {
                'trip_id': int(line[0]), 'trip_name': line[1], 'destination': line[2],
                'start_date': line[3], 'end_date': line[4], 'total_budget': float(line[5]), 'status': line[6], 'created_date': line[7]
            }
            break
    return render_template('booking_confirmation.html', booking=booking, trip=trip)

if __name__ == '__main__':
    app.run(debug=True)
