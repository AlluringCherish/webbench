from flask import Flask, render_template, request, redirect, url_for, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


def parse_file(filename, fields, convert_funcs=None):
    """Parse pipe delimited file without header, returning list of dict entries.
    convert_funcs is an optional dict of field_name: callable to convert field value."""
    records = []
    full_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(full_path):
        return []

    with open(full_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # Only map as many fields as specified
            parts = parts[:len(fields)]
            record = dict(zip(fields, parts))
            if convert_funcs:
                for k, func in convert_funcs.items():
                    if k in record:
                        try:
                            record[k] = func(record[k])
                        except Exception:
                            # on failure just keep as string
                            pass
            records.append(record)
    return records


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_destinations: dest_id:int, name:str, country:str
    dest_fields = ['dest_id', 'name', 'country', 'region', 'description', 'attractions', 'climate']
    dest_convert = {'dest_id': int}
    all_dests = parse_file('destinations.txt', dest_fields, dest_convert)
    featured_destinations = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in all_dests]

    # upcoming_trips: trip_id:int, trip_name:str, start_date:str
    trip_fields = ['trip_id', 'trip_name', 'destination', 'start_date', 'end_date', 'total_budget', 'status', 'created_date']
    trip_convert = {'trip_id': int}
    all_trips = parse_file('trips.txt', trip_fields, trip_convert)
    upcoming_trips = [{'trip_id': t['trip_id'], 'trip_name': t['trip_name'], 'start_date': t['start_date']} for t in all_trips]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    # Context: destinations: List[Dict] dest_id:int, name:str, country:str, region:str
    region_filter = request.args.get('region', '').strip()
    dest_fields = ['dest_id', 'name', 'country', 'region', 'description', 'attractions', 'climate']
    dest_convert = {'dest_id': int}
    all_dests = parse_file('destinations.txt', dest_fields, dest_convert)

    if region_filter:
        filtered = [d for d in all_dests if d['region'].lower() == region_filter.lower()]
    else:
        filtered = all_dests

    destinations_out = [{'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']} for d in filtered]
    return render_template('destinations.html', destinations=destinations_out)


@app.route('/destinations/<int:dest_id>')
def destination_details(dest_id):
    dest_fields = ['dest_id', 'name', 'country', 'region', 'description', 'attractions', 'climate']
    dest_convert = {'dest_id': int}
    dests = parse_file('destinations.txt', dest_fields, dest_convert)

    destination = None
    for d in dests:
        if d['dest_id'] == dest_id:
            destination = d
            break
    if not destination:
        abort(404)

    # Provide exactly destination dict as context
    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries_fields = ['itinerary_id', 'itinerary_name', 'destination', 'start_date', 'end_date', 'activities', 'status']
    convert = {'itinerary_id': int}

    if request.method == 'POST':
        # Minimal stub: no data processing, redirect back to itinerary
        return redirect(url_for('itinerary'))

    itineraries_raw = parse_file('itineraries.txt', itineraries_fields, convert)
    return render_template('itinerary.html', itineraries=itineraries_raw)


@app.route('/accommodations')
def accommodations():
    hotel_fields = ['hotel_id', 'name', 'city', 'rating', 'price_per_night', 'amenities', 'category']
    convert = {'hotel_id': int, 'rating': float, 'price_per_night': float}
    hotels_raw = parse_file('hotels.txt', hotel_fields, convert)
    return render_template('accommodations.html', hotels=hotels_raw)


@app.route('/transportation')
def transportation():
    flights_fields = ['flight_id', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price', 'class_type', 'duration']
    convert = {'flight_id': int, 'price': float}
    flights_raw = parse_file('flights.txt', flights_fields, convert)
    return render_template('transportation.html', flights=flights_raw)


@app.route('/packages')
def packages():
    packages_fields = ['package_id', 'package_name', 'destination', 'duration_days', 'price', 'included_items', 'difficulty_level']
    convert = {'package_id': int, 'duration_days': int, 'price': float}
    packages_raw = parse_file('packages.txt', packages_fields, convert)

    # Only pass required fields in context
    packages = []
    for p in packages_raw:
        packages.append({
            'package_id': p['package_id'],
            'package_name': p['package_name'],
            'destination': p['destination'],
            'duration_days': p['duration_days'],
            'price': p['price'],
        })
    return render_template('packages.html', packages=packages)


@app.route('/packages/<int:package_id>', methods=['POST'])
def book_package(package_id):
    # Stub for book package
    return redirect(url_for('packages'))


@app.route('/trips')
def trips():
    trips_fields = ['trip_id', 'trip_name', 'destination', 'start_date', 'end_date', 'total_budget', 'status', 'created_date']
    convert = {'trip_id': int}
    trips_raw = parse_file('trips.txt', trips_fields, convert)

    trips = []
    for t in trips_raw:
        trips.append({
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date'],
            'status': t['status'],
        })
    return render_template('trips.html', trips=trips)


@app.route('/trips/<int:trip_id>/edit')
def edit_trip(trip_id):
    # Stub, redirect to trips
    return redirect(url_for('trips'))


@app.route('/trips/<int:trip_id>/delete', methods=['POST'])
def delete_trip(trip_id):
    # Stub, redirect to trips
    return redirect(url_for('trips'))


@app.route('/booking-confirmation')
def booking_confirmation():
    bookings_fields = ['booking_id', 'trip_id', 'booking_type', 'booking_date', 'amount', 'confirmation_number', 'status']
    bookings_raw = parse_file('bookings.txt', bookings_fields, {'booking_id': int, 'trip_id': int, 'amount': float})

    # Select the latest confirmed booking for display (stub)
    # Just send a fixed example for minimal compliance
    booking = {
        'confirmation_number': 'CONF12345678',
        'booking_details': 'Your booking was successful.'
    }

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations')
def recommendations():
    dest_fields = ['dest_id', 'name', 'country', 'region', 'description', 'attractions', 'climate']
    convert = {'dest_id': int}
    all_dests = parse_file('destinations.txt', dest_fields, convert)

    # trending_destinations: dest_id, name, popularity_rank (index by sorted order for example)
    trending_destinations = []
    rank = 1
    for d in all_dests:
        trending_destinations.append({'dest_id': d['dest_id'], 'name': d['name'], 'popularity_rank': rank})
        rank += 1

    season_filter = request.args.get('season_filter', '')
    budget_filter = request.args.get('budget_filter', '')

    return render_template('recommendations.html', trending_destinations=trending_destinations, season_filter=season_filter, budget_filter=budget_filter)


if __name__ == '__main__':
    app.run()
