from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read/write pipe delimited files

def read_pipe_delimited_file(filename):
    path = os.path.join(DATA_DIR, filename)
    data = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    data.append(parts)
    except FileNotFoundError:
        # Gracefully handle missing file
        return []
    return data


def write_pipe_delimited_file(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write('|'.join(str(x) for x in record) + '\n')


@app.route('/')
def dashboard():
    # Load featured destinations and upcoming trips
    destinations = []
    trips = []
    raw_dests = read_pipe_delimited_file('destinations.txt')
    raw_trips = read_pipe_delimited_file('trips.txt')
    # For featured dests, show first 3
    for row in raw_dests[:3]:
        if len(row) == 7:
            dest = {
                'dest_id': int(row[0]),
                'name': row[1],
                'country': row[2],
                'region': row[3],
                'description': row[4],
                'attractions': row[5],
                'climate': row[6]
            }
            destinations.append(dest)
    # For upcoming trips, get trips with start_date > today in list maybe first 3
    today = datetime.today().date()
    future_trips = []
    for row in raw_trips:
        if len(row) == 8:
            start_date = None
            try:
                start_date = datetime.strptime(row[3], '%Y-%m-%d').date()
            except:
                start_date = None
            if start_date and start_date >= today:
                trip = {
                    'trip_id': int(row[0]),
                    'trip_name': row[1],
                    'destination': row[2],
                    'start_date': row[3],
                    'end_date': row[4],
                    'total_budget': row[5],
                    'status': row[6],
                    'created_date': row[7]
                }
                future_trips.append(trip)
    future_trips.sort(key=lambda x: x['start_date'])
    trips = future_trips[:3]

    return render_template('dashboard.html',
                           page_title='Travel Planner Dashboard',
                           destinations=destinations,
                           trips=trips)


@app.route('/destinations')
def destinations():
    # Get query params from GET if any filtering (search, region filter)
    search_query = request.args.get('search', '').strip().lower()
    region_filter = request.args.get('region', '').strip()

    raw_dests = read_pipe_delimited_file('destinations.txt')
    destinations = []
    for row in raw_dests:
        if len(row) != 7:
            continue
        dest = {
            'dest_id': int(row[0]),
            'name': row[1],
            'country': row[2],
            'region': row[3],
            'description': row[4],
            'attractions': row[5],
            'climate': row[6]
        }
        # Apply search filter by name or country
        if search_query:
            if search_query not in dest['name'].lower() and search_query not in dest['country'].lower():
                continue
        # Apply region filter if given
        if region_filter and region_filter != dest['region']:
            continue
        destinations.append(dest)

    return render_template('destinations.html',
                           page_title='Travel Destinations',
                           destinations=destinations,
                           search_query=search_query,
                           region_filter=region_filter)


@app.route('/destinations/<int:dest_id>')
def destination_details(dest_id):
    raw_dests = read_pipe_delimited_file('destinations.txt')
    destination = None
    for row in raw_dests:
        if len(row) == 7 and int(row[0]) == dest_id:
            destination = {
                'dest_id': int(row[0]),
                'name': row[1],
                'country': row[2],
                'region': row[3],
                'description': row[4],
                'attractions': row[5],
                'climate': row[6]
            }
            break
    if not destination:
        # Return to destinations page if not found
        return redirect(url_for('destinations'))
    return render_template('destination_details.html',
                           page_title='Destination Details',
                           destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    if request.method == 'POST':
        # Parse form to add or update itinerary
        # Expect form fields: itinerary_name_input, start_date_input, end_date_input, add activity
        # We treat adding a new itinerary or adding activity to existing
        itinerary_name = request.form.get('itinerary-name-input', '').strip()
        start_date = request.form.get('start-date-input', '').strip()
        end_date = request.form.get('end-date-input', '').strip()
        add_activity = request.form.get('add-activity-button')  # If clicked, button returns this key
        activity_desc = request.form.get('activity-desc', '').strip() if add_activity else ''

        itineraries = read_pipe_delimited_file('itineraries.txt')

        # Validation minimal: check itinerary name and dates on new
        if itinerary_name and start_date and end_date:
            # If adding activity requires finding existing itinerary? Here we just add new itinerary
            # Generate new itinerary_id
            max_id = 0
            for row in itineraries:
                try:
                    max_id = max(max_id, int(row[0]))
                except:
                    pass
            new_id = max_id + 1
            activities = activity_desc if activity_desc else ''
            # Status default to Planned
            new_itinerary = [str(new_id), itinerary_name, '', start_date, end_date, activities, 'Planned']

            # Since destinations is a field, try to find destination by itinerary_name maybe?
            # This specification unclear; so we keep destination empty or consider itinerary_name includes?
            # Here just set empty

            itineraries.append(new_itinerary)
            write_pipe_delimited_file('itineraries.txt', itineraries)

        return redirect(url_for('itinerary'))

    # GET display all itineraries
    raw_itineraries = read_pipe_delimited_file('itineraries.txt')
    itineraries = []
    for row in raw_itineraries:
        if len(row) == 7:
            itinerary = {
                'itinerary_id': int(row[0]),
                'itinerary_name': row[1],
                'destination': row[2],
                'start_date': row[3],
                'end_date': row[4],
                'activities': row[5],
                'status': row[6]
            }
            itineraries.append(itinerary)

    return render_template('itinerary.html',
                           page_title='Plan Your Itinerary',
                           itineraries=itineraries)


@app.route('/accommodations')
def accommodations():
    destination_city = request.args.get('destination', '').strip()
    price_filter = request.args.get('price', '').strip()

    raw_hotels = read_pipe_delimited_file('hotels.txt')
    hotels = []
    for row in raw_hotels:
        if len(row) != 7:
            continue
        # Filter by city if set
        if destination_city and destination_city.lower() != row[2].lower():
            continue
        # Filter by price category
        # Categories mapped from price_filter dropdown: Budget, Mid-range, Luxury
        # We'll assume hotel category field corresponds
        if price_filter and price_filter != row[6]:
            continue
        hotel = {
            'hotel_id': int(row[0]),
            'name': row[1],
            'city': row[2],
            'rating': float(row[3]),
            'price_per_night': row[4],
            'amenities': row[5],
            'category': row[6]
        }
        hotels.append(hotel)

    return render_template('accommodations.html',
                           page_title='Search Accommodations',
                           hotels=hotels,
                           selected_city=destination_city,
                           price_filter=price_filter)


@app.route('/transportation')
def transportation():
    departure_city = request.args.get('departure', '').strip()
    arrival_city = request.args.get('arrival', '').strip()
    flight_class = request.args.get('flight_class', '').strip()

    raw_flights = read_pipe_delimited_file('flights.txt')
    flights = []
    for row in raw_flights:
        if len(row) != 9:
            continue
        if departure_city and departure_city.lower() != row[2].lower():
            continue
        if arrival_city and arrival_city.lower() != row[3].lower():
            continue
        if flight_class and flight_class != row[7]:
            continue
        flight = {
            'flight_id': int(row[0]),
            'airline': row[1],
            'departure_city': row[2],
            'arrival_city': row[3],
            'departure_time': row[4],
            'arrival_time': row[5],
            'price': row[6],
            'class_type': row[7],
            'duration': row[8]
        }
        flights.append(flight)

    return render_template('transportation.html',
                           page_title='Book Flights',
                           flights=flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           flight_class=flight_class)


@app.route('/packages')
def packages():
    duration_filter = request.args.get('duration', '').strip()

    raw_packages = read_pipe_delimited_file('packages.txt')
    packages = []
    for row in raw_packages:
        if len(row) != 7:
            continue
        # Filter by duration
        try:
            dur = int(row[3])
        except:
            dur = 0
        if duration_filter:
            if duration_filter == '3-5 days' and not (3 <= dur <= 5):
                continue
            elif duration_filter == '7-10 days' and not (7 <= dur <= 10):
                continue
            elif duration_filter == '14+ days' and dur < 14:
                continue
        package = {
            'package_id': int(row[0]),
            'package_name': row[1],
            'destination': row[2],
            'duration_days': dur,
            'price': row[4],
            'included_items': row[5],
            'difficulty_level': row[6]
        }
        packages.append(package)

    return render_template('packages.html',
                           page_title='Travel Packages',
                           packages=packages,
                           duration_filter=duration_filter)


@app.route('/trips')
def trips():
    raw_trips = read_pipe_delimited_file('trips.txt')
    trips_data = []
    for row in raw_trips:
        if len(row) != 8:
            continue
        trip = {
            'trip_id': int(row[0]),
            'trip_name': row[1],
            'destination': row[2],
            'start_date': row[3],
            'end_date': row[4],
            'total_budget': row[5],
            'status': row[6],
            'created_date': row[7]
        }
        trips_data.append(trip)

    return render_template('trips.html',
                           page_title='My Trips',
                           trips=trips_data)


@app.route('/booking-confirmation')
def booking_confirmation():
    # This page expects some way to identify current booking - we pick latest booking for demo
    raw_bookings = read_pipe_delimited_file('bookings.txt')
    if not raw_bookings:
        booking = None
    else:
        # Use last booking record as default confirmation
        last = raw_bookings[-1]
        if len(last) == 7:
            booking = {
                'booking_id': int(last[0]),
                'trip_id': int(last[1]),
                'booking_type': last[2],
                'booking_date': last[3],
                'amount': last[4],
                'confirmation_number': last[5],
                'status': last[6]
            }
        else:
            booking = None

    return render_template('booking_confirmation.html',
                           page_title='Booking Confirmation',
                           booking=booking)


@app.route('/recommendations')
def recommendations():
    season = request.args.get('season', '').strip()
    budget = request.args.get('budget', '').strip()

    # For trending destinations, pick top 3 destinations sorted by popularity or id (mock)
    raw_dests = read_pipe_delimited_file('destinations.txt')
    trending = []
    for row in raw_dests[:3]:
        if len(row) != 7:
            continue
        trending.append({
            'dest_id': int(row[0]),
            'name': row[1],
            'country': row[2],
            'region': row[3],
            'description': row[4],
            'attractions': row[5],
            'climate': row[6]
        })

    # Normally we would filter based on season and budget

    return render_template('recommendations.html',
                           page_title='Travel Recommendations',
                           trending_destinations=trending,
                           season_filter=season,
                           budget_filter=budget)


# Since travel packages details and booking process are noted but no detailed route,
# we provide placeholder route to handle book-package POST and view details redirect

@app.route('/packages/<int:pkg_id>/book', methods=['POST'])
def book_package(pkg_id):
    # Simulate booking process and add a booking entry
    raw_packages = read_pipe_delimited_file('packages.txt')
    package = None
    for row in raw_packages:
        if len(row) == 7 and int(row[0]) == pkg_id:
            package = row
            break
    if not package:
        return redirect(url_for('packages'))

    # Read existing bookings
    bookings = read_pipe_delimited_file('bookings.txt')
    max_id = 0
    for b in bookings:
        try:
            max_id = max(max_id, int(b[0]))
        except:
            pass
    new_id = max_id + 1

    # Create booking record
    # Fields: booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
    # We'll create a new trip for this package too,
    trips = read_pipe_delimited_file('trips.txt')
    max_trip_id = 0
    for t in trips:
        try:
            max_trip_id = max(max_trip_id, int(t[0]))
        except:
            pass
    new_trip_id = max_trip_id + 1

    # For demo uses: we use package destination, dummy dates and budget
    today_str = datetime.today().strftime('%Y-%m-%d')
    trip_name = package[1]
    trip_destination = package[2]
    start_date = today_str
    end_date = today_str
    total_budget = package[4]
    status = 'Booked'
    created_date = today_str
    trips.append([str(new_trip_id), trip_name, trip_destination, start_date, end_date, total_budget, status, created_date])
    write_pipe_delimited_file('trips.txt', trips)

    booking_date = today_str
    amount = package[4]
    confirmation_number = f'CONF{str(new_id).zfill(3)}'
    booking_type = 'Package'
    status = 'Confirmed'

    bookings.append([str(new_id), str(new_trip_id), booking_type, booking_date, amount, confirmation_number, status])
    write_pipe_delimited_file('bookings.txt', bookings)

    return redirect(url_for('booking_confirmation'))


@app.route('/packages/<int:pkg_id>/view')
def view_package_details(pkg_id):
    # Not fully specified, just redirect to packages page currently
    return redirect(url_for('packages'))


@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    trips = read_pipe_delimited_file('trips.txt')
    trips = [row for row in trips if len(row) == 8 and int(row[0]) != trip_id]
    write_pipe_delimited_file('trips.txt', trips)
    return redirect(url_for('trips'))


@app.route('/trips/<int:trip_id>/edit', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trips = read_pipe_delimited_file('trips.txt')
    trip = None
    for row in trips:
        if len(row) == 8 and int(row[0]) == trip_id:
            trip = row
            break
    if not trip:
        return redirect(url_for('trips'))

    if request.method == 'POST':
        trip_name = request.form.get('trip_name', trip[1]).strip()
        destination = request.form.get('destination', trip[2]).strip()
        start_date = request.form.get('start_date', trip[3]).strip()
        end_date = request.form.get('end_date', trip[4]).strip()
        total_budget = request.form.get('total_budget', trip[5]).strip()
        status = request.form.get('status', trip[6]).strip()

        # Update the trip data
        for i, r in enumerate(trips):
            if len(r) == 8 and int(r[0]) == trip_id:
                trips[i] = [str(trip_id), trip_name, destination, start_date, end_date, total_budget, status, r[7]]
                break

        write_pipe_delimited_file('trips.txt', trips)
        return redirect(url_for('trips'))

    # GET render edit trip form (assumed same template as trips for list)
    trip_dict = {
        'trip_id': int(trip[0]),
        'trip_name': trip[1],
        'destination': trip[2],
        'start_date': trip[3],
        'end_date': trip[4],
        'total_budget': trip[5],
        'status': trip[6],
        'created_date': trip[7]
    }
    return render_template('trips.html',
                           page_title='Edit Trip',
                           edit_trip=trip_dict)


@app.route('/destinations/<int:dest_id>/add-to-trip', methods=['POST'])
def add_destination_to_trip(dest_id):
    # Adds destination to a trip - Since no user session, we add to a new trip with default values or latest trip
    trips = read_pipe_delimited_file('trips.txt')
    max_trip_id = 0
    for t in trips:
        try:
            max_trip_id = max(max_trip_id, int(t[0]))
        except:
            pass

    new_trip_id = max_trip_id + 1

    raw_dests = read_pipe_delimited_file('destinations.txt')
    destination = None
    for row in raw_dests:
        if len(row) == 7 and int(row[0]) == dest_id:
            destination = row
            break
    if not destination:
        return redirect(url_for('destinations'))

    today_str = datetime.today().strftime('%Y-%m-%d')
    trip_name = f'Trip to {destination[1]}'
    trip_destination = destination[1]
    start_date = today_str
    end_date = today_str
    total_budget = '0.00'
    status = 'Planned'
    created_date = today_str
    trips.append([str(new_trip_id), trip_name, trip_destination, start_date, end_date, total_budget, status, created_date])
    write_pipe_delimited_file('trips.txt', trips)
    return redirect(url_for('trips'))


if __name__ == '__main__':
    app.run(debug=True)
