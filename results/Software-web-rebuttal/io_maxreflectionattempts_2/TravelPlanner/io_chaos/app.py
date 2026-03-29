from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from files

def load_destinations():
    destinations = []
    try:
        with open('data/destinations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # dest_id|name|country|region|description|attractions|climate
                if len(parts) != 7:
                    continue
                dest_id = int(parts[0])
                name = parts[1]
                country = parts[2]
                region = parts[3]
                description = parts[4]
                attractions = parts[5]
                # climate = parts[6]  # Not used
                destination = {
                    'dest_id': dest_id,
                    'name': name,
                    'country': country,
                    'region': region,
                    'description': description,
                    'attractions': attractions
                }
                destinations.append(destination)
    except (IOError, FileNotFoundError):
        # Return empty list if file missing
        destinations = []
    return destinations


def load_itineraries():
    itineraries = []
    try:
        with open('data/itineraries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # itinerary_id|itinerary_name|destination|start_date|end_date|activities|status
                if len(parts) != 7:
                    continue
                itinerary_id = int(parts[0])
                itinerary_name = parts[1]
                destination = parts[2]
                start_date = parts[3]
                end_date = parts[4]
                activities = parts[5]
                status = parts[6]
                itinerary = {
                    'itinerary_id': itinerary_id,
                    'itinerary_name': itinerary_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'activities': activities,
                    'status': status
                }
                itineraries.append(itinerary)
    except (IOError, FileNotFoundError):
        itineraries = []
    return itineraries


def load_hotels():
    hotels = []
    try:
        with open('data/hotels.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # hotel_id|name|city|rating|price_per_night|amenities|category
                if len(parts) != 7:
                    continue
                hotel_id = int(parts[0])
                name = parts[1]
                city = parts[2]
                try:
                    rating = float(parts[3])
                except ValueError:
                    rating = 0.0
                try:
                    price_per_night = float(parts[4])
                except ValueError:
                    price_per_night = 0.0
                amenities = parts[5]
                # category = parts[6] # Not used
                hotel = {
                    'hotel_id': hotel_id,
                    'name': name,
                    'city': city,
                    'rating': rating,
                    'price_per_night': price_per_night,
                    'amenities': amenities
                }
                hotels.append(hotel)
    except (IOError, FileNotFoundError):
        hotels = []
    return hotels


def load_flights():
    flights = []
    try:
        with open('data/flights.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # flight_id|airline|departure_city|arrival_city|departure_time|arrival_time|price|class_type|duration
                if len(parts) != 9:
                    continue
                flight_id = int(parts[0])
                airline = parts[1]
                departure_city = parts[2]
                arrival_city = parts[3]
                departure_time = parts[4]
                arrival_time = parts[5]
                try:
                    price = float(parts[6])
                except ValueError:
                    price = 0.0
                class_type = parts[7]
                # duration = parts[8]  # Not used
                flight = {
                    'flight_id': flight_id,
                    'airline': airline,
                    'departure_city': departure_city,
                    'arrival_city': arrival_city,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'price': price,
                    'class_type': class_type
                }
                flights.append(flight)
    except (IOError, FileNotFoundError):
        flights = []
    return flights


def load_packages():
    packages = []
    try:
        with open('data/packages.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # package_id|package_name|destination|duration_days|price|included_items|difficulty_level
                if len(parts) != 7:
                    continue
                package_id = int(parts[0])
                package_name = parts[1]
                destination = parts[2]
                try:
                    duration_days = int(parts[3])
                except ValueError:
                    duration_days = 0
                try:
                    price = float(parts[4])
                except ValueError:
                    price = 0.0
                # included_items = parts[5]  # Not used
                # difficulty_level = parts[6]  # Not used
                package = {
                    'package_id': package_id,
                    'package_name': package_name,
                    'destination': destination,
                    'duration_days': duration_days,
                    'price': price
                }
                packages.append(package)
    except (IOError, FileNotFoundError):
        packages = []
    return packages


def load_trips():
    trips = []
    try:
        with open('data/trips.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # trip_id|trip_name|destination|start_date|end_date|total_budget|status|created_date
                if len(parts) != 8:
                    continue
                trip_id = int(parts[0])
                trip_name = parts[1]
                destination = parts[2]
                start_date = parts[3]
                end_date = parts[4]
                # total_budget = float(parts[5]) # Not used
                status = parts[6]
                # created_date = parts[7] # Not used
                trip = {
                    'trip_id': trip_id,
                    'trip_name': trip_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'status': status
                }
                trips.append(trip)
    except (IOError, FileNotFoundError):
        trips = []
    return trips


def load_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                # booking_id|trip_id|booking_type|booking_date|amount|confirmation_number|status
                if len(parts) != 7:
                    continue
                # booking_id = int(parts[0]) # Not used
                # trip_id = int(parts[1]) # Not used
                # booking_type = parts[2] # Not used
                booking_date = parts[3]
                try:
                    amount = float(parts[4])
                except ValueError:
                    amount = 0.0
                confirmation_number = parts[5]
                # status = parts[6] # Not used
                booking = {
                    'confirmation_number': confirmation_number,
                    'booking_date': booking_date,
                    'amount': amount,
                    'locations': ''  # We will deduce locations from trips separately if needed
                }
                bookings.append(booking)
    except (IOError, FileNotFoundError):
        bookings = []
    return bookings


@app.route('/')
def root():
    # Redirect to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    destinations = load_destinations()
    trips = load_trips()

    # Featured destinations: list of dicts with dest_id, name, country
    featured_destinations = [
        {"dest_id": d["dest_id"], "name": d["name"], "country": d["country"]} 
        for d in destinations
    ]

    # Upcoming trips: list of dicts with trip_id, trip_name, start_date
    # We can consider upcoming as trips with start_date >= today (But no date logic provided, so just list all)
    upcoming_trips = [
        {"trip_id": t["trip_id"], "trip_name": t["trip_name"], "start_date": t["start_date"]} 
        for t in trips
    ]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET'])
def destinations():
    destinations = load_destinations()
    # Need: dest_id, name, country, region
    ctx_destinations = [
        {"dest_id": d["dest_id"], "name": d["name"], "country": d["country"], "region": d["region"]} 
        for d in destinations
    ]
    return render_template('destinations.html', destinations=ctx_destinations)


@app.route('/destinations/<int:dest_id>', methods=['GET'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = None
    for d in destinations:
        if d['dest_id'] == dest_id:
            destination = d
            break
    if destination is None:
        # If destination not found, show empty or 404
        # Here render with empty dict
        destination = {"dest_id": 0, "name": "", "country": "", "description": "", "attractions": ""}
    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    # POST is to add activities likely, but no data handling specified, so just load itineraries
    itineraries = load_itineraries()
    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET'])
def accommodations():
    hotels = load_hotels()
    # hotels: hotel_id, name, city, rating, price_per_night, amenities
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation', methods=['GET'])
def transportation():
    flights = load_flights()
    # flights: flight_id, airline, departure_city, arrival_city, departure_time, arrival_time, price, class_type
    return render_template('transportation.html', flights=flights)


@app.route('/packages', methods=['GET'])
def travel_packages():
    packages = load_packages()
    # packages: package_id, package_name, destination, duration_days, price
    return render_template('packages.html', packages=packages)


@app.route('/trips', methods=['GET'])
def trips():
    trips_data = load_trips()
    # trips: trip_id, trip_name, destination, start_date, end_date, status
    return render_template('trips.html', trips=trips_data)


@app.route('/bookings/confirmation', methods=['GET'])
def booking_confirmation():
    bookings = load_bookings()
    trips_data = load_trips()

    # We'll show the most recent confirmed booking if available
    booking = None
    if bookings:
        # Use the last booking entry (assuming latest booking at end of file)
        booking = bookings[-1]

        # Attempt to find trip destinations for the booking
        # The design says booking context locations:str, so gather trip destination if possible by matching booking confirmation number
        # No direct link, so locations empty string as fallback
    else:
        booking = {"confirmation_number": "", "booking_date": "", "amount": 0.0, "locations": ""}

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET'])
def recommendations():
    destinations = load_destinations()
    # trending_destinations: dest_id, name, popularity_rank
    # We do not have popularity_rank in data file, so fabricate it by sorting by dest_id ascending as rank
    trending_destinations = []
    sorted_dest = sorted(destinations, key=lambda d: d['dest_id'])
    rank = 1
    for d in sorted_dest:
        trending_destinations.append({"dest_id": d['dest_id'], "name": d['name'], "popularity_rank": rank})
        rank += 1

    season_filter_options = ["Spring", "Summer", "Fall", "Winter"]
    budget_filter_options = ["Low", "Medium", "High"]

    return render_template('recommendations.html', trending_destinations=trending_destinations, 
                           season_filter_options=season_filter_options, budget_filter_options=budget_filter_options)


if __name__ == '__main__':
    app.run(debug=True)
