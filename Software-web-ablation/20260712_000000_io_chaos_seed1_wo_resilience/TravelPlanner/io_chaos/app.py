from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def read_destinations():
    destinations = []
    path = os.path.join('data', 'destinations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    dest = {
                        'dest_id': int(parts[0]),
                        'name': parts[1],
                        'country': parts[2],
                        'region': parts[3],
                        'description': parts[4],
                        'attractions': parts[5],
                        'climate': parts[6]
                    }
                    destinations.append(dest)
    except (FileNotFoundError, IOError):
        destinations = []
    return destinations

def read_itineraries():
    itineraries = []
    path = os.path.join('data', 'itineraries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    itin = {
                        'itinerary_id': int(parts[0]),
                        'itinerary_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'activities': parts[5],
                        'status': parts[6]
                    }
                    itineraries.append(itin)
    except (FileNotFoundError, IOError):
        itineraries = []
    return itineraries

def read_hotels():
    hotels = []
    path = os.path.join('data', 'hotels.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    hotel = {
                        'hotel_id': int(parts[0]),
                        'name': parts[1],
                        'city': parts[2],
                        'rating': float(parts[3]),
                        'price_per_night': float(parts[4]),
                        'amenities': parts[5],
                        'category': parts[6]
                    }
                    hotels.append(hotel)
    except (FileNotFoundError, IOError):
        hotels = []
    return hotels

def read_flights():
    flights = []
    path = os.path.join('data', 'flights.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    flight = {
                        'flight_id': int(parts[0]),
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
    except (FileNotFoundError, IOError):
        flights = []
    return flights

def read_packages():
    packages = []
    path = os.path.join('data', 'packages.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    package = {
                        'package_id': int(parts[0]),
                        'package_name': parts[1],
                        'destination': parts[2],
                        'duration_days': int(parts[3]),
                        'price': float(parts[4]),
                        'included_items': parts[5],
                        'difficulty_level': parts[6]
                    }
                    packages.append(package)
    except (FileNotFoundError, IOError):
        packages = []
    return packages

def read_trips():
    trips = []
    path = os.path.join('data', 'trips.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    trip = {
                        'trip_id': int(parts[0]),
                        'trip_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'total_budget': float(parts[5]),
                        'status': parts[6],
                        'created_date': parts[7]
                    }
                    trips.append(trip)
    except (FileNotFoundError, IOError):
        trips = []
    return trips

def read_bookings():
    bookings = []
    path = os.path.join('data', 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    booking = {
                        'booking_id': int(parts[0]),
                        'trip_id': int(parts[1]),
                        'booking_type': parts[2],
                        'booking_date': parts[3],
                        'amount': float(parts[4]),
                        'confirmation_number': parts[5],
                        'status': parts[6]
                    }
                    bookings.append(booking)
    except (FileNotFoundError, IOError):
        bookings = []
    return bookings

@app.route('/')
def dashboard():
    # Featured Destinations: choose 3 top destinations for sample
    destinations = read_destinations()
    featured_destinations = []
    for dest in destinations[:3]:
        featured_destinations.append({
            'dest_id': dest['dest_id'],
            'name': dest['name'],
            'country': dest['country']
        })

    # Upcoming trips (example: trips in future dates)
    trips = read_trips()
    upcoming_trips = []
    for trip in trips[:3]:
        upcoming_trips.append({
            'trip_id': trip['trip_id'],
            'trip_name': trip['trip_name'],
            'destination': trip['destination'],
            'dates': f"{trip['start_date']} to {trip['end_date']}"
        })

    return redirect(url_for('dashboard')) if False else render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET', 'POST'])
def destinations():
    destinations_data = read_destinations()
    destinations = []
    for d in destinations_data:
        destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        })
    return render_template('destinations.html', destinations=destinations)

@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details(dest_id):
    destinations = read_destinations()
    destination = None
    for d in destinations:
        if d['dest_id'] == dest_id:
            destination = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions'],
                'climate': d['climate']
            }
            break
    if not destination:
        # If destination not found, redirect to /destinations
        return redirect(url_for('destinations'))

    if request.method == 'POST':
        # Handle add-to-trip action here if needed (not specified in detail)
        # For now, just redirect to itinerary page
        return redirect(url_for('itinerary'))

    return render_template('destination_details.html', destination=destination)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    itineraries = read_itineraries()
    return render_template('itinerary.html', itineraries=itineraries)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels = read_hotels()
    return render_template('accommodations.html', hotels=hotels)

@app.route('/transportation', methods=['GET', 'POST'])
def transportation():
    flights = read_flights()
    return render_template('transportation.html', flights=flights)

@app.route('/packages', methods=['GET', 'POST'])
def packages():
    packages_list = read_packages()
    return render_template('packages.html', packages=packages_list)

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    trips_list = read_trips()
    return render_template('trips.html', trips=trips_list)

@app.route('/bookings/confirmation')
def booking_confirmation():
    # For demonstration, use the first booking from file
    bookings = read_bookings()
    booking = None
    if bookings:
        b = bookings[0]
        booking = {
            'confirmation_number': b['confirmation_number'],
            'booking_details': f"Booking for trip ID {b['trip_id']} - Type: {b['booking_type']} - Date: {b['booking_date']} - Amount: ${b['amount']:.2f}"
        }
    else:
        booking = {'confirmation_number': '', 'booking_details': 'No booking found.'}
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/recommendations')
def recommendations():
    destinations = read_destinations()
    trending_destinations = []
    # For simple demo, assign popularity as length of attractions
    for dest in destinations[:5]:
        trending_destinations.append({
            'dest_id': dest['dest_id'],
            'name': dest['name'],
            'popularity': len(dest['attractions'])
        })
    return render_template('recommendations.html', trending_destinations=trending_destinations)

if __name__ == '__main__':
    app.run(debug=True)
