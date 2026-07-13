from flask import Flask, render_template, request, redirect, url_for
import os
import datetime

app = Flask(__name__)
DATA_FOLDER = 'data'

# Utility functions for reading and writing data

def read_data(filename):
    path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return [line.split('|') for line in lines if line]


def write_data(filename, data_lines):
    path = os.path.join(DATA_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for line in data_lines:
            f.write('|'.join(line) + '\n')


@app.route('/')
def dashboard():
    # Load featured destinations (for simplicity, first 3 destinations)
    destinations = read_data('destinations.txt')
    featured_destinations = destinations[:3]

    # Load upcoming trips (trips with start_date >= today)
    trips = read_data('trips.txt')
    today = datetime.date.today()
    upcoming_trips = [trip for trip in trips if datetime.date.fromisoformat(trip[3]) >= today]
    upcoming_trips.sort(key=lambda x: x[3])

    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations = read_data('destinations.txt')
    search_query = ''
    region_filter = ''

    if request.method == 'POST':
        search_query = request.form.get('search_destination', '').lower()
        region_filter = request.form.get('region_filter', '')

    # Filter destinations
    filtered = []
    for d in destinations:
        name = d[1].lower()
        country = d[2].lower()
        region = d[3]
        if search_query and search_query not in name and search_query not in country:
            continue
        if region_filter and region != region_filter:
            continue
        filtered.append(d)

    return render_template('destinations.html',
                           destinations=filtered,
                           search_query=search_query,
                           region_filter=region_filter)


@app.route('/destination/<dest_id>')
def destination_details(dest_id):
    destinations = read_data('destinations.txt')
    destination = next((d for d in destinations if d[0] == dest_id), None)
    if not destination:
        return "Destination not found", 404

    return render_template('destination_details.html', destination=destination)


@app.route('/add_to_trip/<dest_id>', methods=['POST'])
def add_to_trip(dest_id):
    # For demonstration, just redirect to itinerary page (no real add logic)
    # Stub: could be expanded to add the destination to an itinerary
    return redirect(url_for('itinerary'))


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = read_data('itineraries.txt')

    if request.method == 'POST':
        # Add or update itinerary
        itinerary_id = request.form.get('itinerary_id')
        itinerary_name = request.form.get('itinerary_name_input', '').strip()
        destination = request.form.get('destination_input', '').strip()
        start_date = request.form.get('start_date_input', '').strip()
        end_date = request.form.get('end_date_input', '').strip()
        activities = request.form.get('activities_input', '').strip()

        if not itinerary_name or not destination or not start_date or not end_date:
            # Missing mandatory fields
            return redirect(url_for('itinerary'))

        if itinerary_id:
            # Update existing itinerary
            new_itineraries = []
            for it in itineraries:
                if it[0] == itinerary_id:
                    new_itineraries.append([
                        itinerary_id,
                        itinerary_name,
                        destination,
                        start_date,
                        end_date,
                        activities,
                        it[6] if len(it) > 6 else 'Planned'
                    ])
                else:
                    new_itineraries.append(it)
            itineraries = new_itineraries
        else:
            # Add new itinerary
            new_id = str(max([int(it[0]) for it in itineraries] + [0]) + 1)
            itineraries.append([
                new_id,
                itinerary_name,
                destination,
                start_date,
                end_date,
                activities,
                'Planned'
            ])

        write_data('itineraries.txt', itineraries)
        return redirect(url_for('itinerary'))

    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = read_data('hotels.txt')
    filtered_hotels = hotels
    destination = ''
    check_in = ''
    check_out = ''
    price_filter = ''

    if request.method == 'POST':
        destination = request.form.get('destination_input', '').lower()
        check_in = request.form.get('check_in_date', '')
        check_out = request.form.get('check_out_date', '')
        price_filter = request.form.get('price_filter', '')

        filtered_hotels = []
        for h in hotels:
            city = h[2].lower()
            category = h[6]
            if destination and destination not in city:
                continue
            if price_filter and price_filter != category:
                continue
            filtered_hotels.append(h)

    return render_template('accommodations.html', hotels=filtered_hotels,
                           destination_input=destination,
                           check_in_date=check_in,
                           check_out_date=check_out,
                           price_filter=price_filter)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = read_data('flights.txt')
    filtered_flights = flights
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    flight_class_filter = ''

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').lower()
        arrival_city = request.form.get('arrival_city', '').lower()
        departure_date = request.form.get('departure_date', '')
        flight_class_filter = request.form.get('flight_class_filter', '')

        filtered_flights = []
        for f in flights:
            dep_city = f[2].lower()
            arr_city = f[3].lower()
            class_type = f[7]
            if departure_city and departure_city not in dep_city:
                continue
            if arrival_city and arrival_city not in arr_city:
                continue
            if flight_class_filter and flight_class_filter != class_type:
                continue
            filtered_flights.append(f)

    return render_template('transportation.html', flights=filtered_flights,
                           departure_city=departure_city,
                           arrival_city=arrival_city,
                           departure_date=departure_date,
                           flight_class_filter=flight_class_filter)


@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages = read_data('packages.txt')
    duration_filter = ''

    if request.method == 'POST':
        duration_filter = request.form.get('duration_filter', '')

    filtered_packages = []
    for p in packages:
        duration = int(p[3])
        if duration_filter:
            if duration_filter == '3-5 days' and not (3 <= duration <= 5):
                continue
            elif duration_filter == '7-10 days' and not (7 <= duration <= 10):
                continue
            elif duration_filter == '14+ days' and not (duration >= 14):
                continue
        filtered_packages.append(p)

    return render_template('packages.html', packages=filtered_packages, duration_filter=duration_filter)


@app.route('/trips')
def trips():
    trips = read_data('trips.txt')
    return render_template('trips.html', trips=trips)


@app.route('/booking_confirmation/<booking_id>')
def booking_confirmation(booking_id):
    bookings = read_data('bookings.txt')
    trips = read_data('trips.txt')

    booking = next((b for b in bookings if b[0] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    trip = next((t for t in trips if t[0] == booking[1]), None)

    details = {
        'booking_id': booking[0],
        'trip_name': trip[1] if trip else 'Unknown',
        'booking_type': booking[2],
        'booking_date': booking[3],
        'amount': booking[4],
        'confirmation_number': booking[5],
        'status': booking[6],
    }

    return render_template('booking_confirmation.html', details=details)


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    destinations = read_data('destinations.txt')
    trending_destinations = destinations[:3]  # Simplified trending
    season_filter = ''
    budget_filter = ''

    if request.method == 'POST':
        season_filter = request.form.get('recommendation_season_filter', '')
        budget_filter = request.form.get('budget_filter', '')

    # Filtering logic could be more advanced based on season and budget
    # For now, just passing all filtered by budget could be checked with climate or region
    filtered_trending = []
    for d in trending_destinations:
        # Example dummy filters (not fully implemented)
        if budget_filter:
            # Reject destinations that are tropical if budget is low for demo
            if budget_filter == 'Low' and d[6].lower() == 'tropical':
                continue
        filtered_trending.append(d)

    return render_template('recommendations.html', trending_destinations=filtered_trending,
                           season_filter=season_filter,
                           budget_filter=budget_filter)


if __name__ == '__main__':
    app.run(debug=True)
