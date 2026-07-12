from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from pipe-delimited files

def load_destinations():
    destinations = []
    try:
        with open(os.path.join(DATA_DIR, 'destinations.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                destinations.append({
                    'dest_id': int(parts[0]),
                    'name': parts[1],
                    'country': parts[2],
                    'region': parts[3],
                    'description': parts[4],
                    'attractions': parts[5],
                    'climate': parts[6]
                })
    except FileNotFoundError:
        destinations = []
    return destinations


def load_itineraries():
    itineraries = []
    try:
        with open(os.path.join(DATA_DIR, 'itineraries.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                itineraries.append({
                    'itinerary_id': int(parts[0]),
                    'itinerary_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'activities': parts[5],
                    'status': parts[6]
                })
    except FileNotFoundError:
        itineraries = []
    return itineraries


def load_hotels():
    hotels = []
    try:
        with open(os.path.join(DATA_DIR, 'hotels.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                hotels.append({
                    'hotel_id': int(parts[0]),
                    'name': parts[1],
                    'city': parts[2],
                    'rating': float(parts[3]),
                    'price_per_night': float(parts[4]),
                    'amenities': parts[5],
                    'category': parts[6]
                })
    except FileNotFoundError:
        hotels = []
    return hotels


def load_flights():
    flights = []
    try:
        with open(os.path.join(DATA_DIR, 'flights.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=9:
                    continue
                flights.append({
                    'flight_id': int(parts[0]),
                    'airline': parts[1],
                    'departure_city': parts[2],
                    'arrival_city': parts[3],
                    'departure_time': parts[4],
                    'arrival_time': parts[5],
                    'price': float(parts[6]),
                    'class_type': parts[7],
                    'duration': parts[8]
                })
    except FileNotFoundError:
        flights = []
    return flights


def load_packages():
    packages = []
    try:
        with open(os.path.join(DATA_DIR, 'packages.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) != 7:
                    continue
                packages.append({
                    'package_id': int(parts[0]),
                    'package_name': parts[1],
                    'destination': parts[2],
                    'duration_days': int(parts[3]),
                    'price': float(parts[4]),
                    'included_items': parts[5],
                    'difficulty_level': parts[6]
                })
    except FileNotFoundError:
        packages = []
    return packages


def load_trips():
    trips = []
    try:
        with open(os.path.join(DATA_DIR, 'trips.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts)!=8:
                    continue
                trips.append({
                    'trip_id': int(parts[0]),
                    'trip_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'total_budget': float(parts[5]),
                    'status': parts[6],
                    'created_date': parts[7]
                })
    except FileNotFoundError:
        trips = []
    return trips


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts=line.split('|')
                if len(parts) !=7:
                    continue
                bookings.append({
                    'booking_id': int(parts[0]),
                    'trip_id': int(parts[1]),
                    'booking_type': parts[2],
                    'booking_date': parts[3],
                    'amount': float(parts[4]),
                    'confirmation_number': parts[5],
                    'status': parts[6]
                })
    except FileNotFoundError:
        bookings = []
    return bookings


# Flask routes

@app.route('/', methods=['GET'])
def dashboard():
    destinations = load_destinations()
    featured_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country']} for d in destinations[:3]
    ]
    trips = load_trips()
    upcoming_trips = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date']
        } for t in trips
    ]
    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET'])
def destinations():
    destinations_data = load_destinations()
    destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'country': d['country'], 'region': d['region']} for d in destinations_data
    ]
    return render_template('destinations.html', destinations=destinations)


@app.route('/destinations/<int:dest_id>', methods=['GET'])
def destination_details(dest_id):
    destinations = load_destinations()
    destination = None
    for d in destinations:
        if d['dest_id'] == dest_id:
            destination = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions']
            }
            break
    if destination is None:
        return redirect(url_for('destinations'))
    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    if request.method == 'POST':
        # Minimal POST: just redirect back
        return redirect(url_for('plan_itinerary'))
    itineraries_data = load_itineraries()
    itineraries = [
        {
            'itinerary_id': it['itinerary_id'],
            'itinerary_name': it['itinerary_name'],
            'destination': it['destination'],
            'start_date': it['start_date'],
            'end_date': it['end_date'],
            'status': it['status']
        } for it in itineraries_data
    ]
    return render_template('itinerary.html', itineraries=itineraries)


@app.route('/accommodations', methods=['GET'])
def accommodations():
    hotels_data = load_hotels()
    hotels = [
        {
            'hotel_id': h['hotel_id'],
            'name': h['name'],
            'city': h['city'],
            'rating': h['rating'],
            'price_per_night': h['price_per_night'],
            'amenities': h['amenities'],
            'category': h['category']
        } for h in hotels_data
    ]
    return render_template('accommodations.html', hotels=hotels)


@app.route('/transportation', methods=['GET'])
def transportation():
    flights_data = load_flights()
    flights = [
        {
            'flight_id': f['flight_id'],
            'airline': f['airline'],
            'departure_city': f['departure_city'],
            'arrival_city': f['arrival_city'],
            'departure_time': f['departure_time'],
            'arrival_time': f['arrival_time'],
            'price': f['price'],
            'class_type': f['class_type'],
            'duration': f['duration']
        } for f in flights_data
    ]
    return render_template('transportation.html', flights=flights)


@app.route('/packages', methods=['GET'])
def travel_packages():
    packages_data = load_packages()
    packages = [
        {
            'package_id': p['package_id'],
            'package_name': p['package_name'],
            'destination': p['destination'],
            'duration_days': p['duration_days'],
            'price': p['price']
        } for p in packages_data
    ]
    return render_template('packages.html', packages=packages)


@app.route('/trips', methods=['GET'])
def trip_management():
    trips_data = load_trips()
    trips = [
        {
            'trip_id': t['trip_id'],
            'trip_name': t['trip_name'],
            'destination': t['destination'],
            'start_date': t['start_date'],
            'end_date': t['end_date'],
            'status': t['status']
        } for t in trips_data
    ]
    return render_template('trips.html', trips=trips)


@app.route('/booking-confirmation', methods=['GET'])
def booking_confirmation():
    bookings = load_bookings()
    if bookings:
        last = bookings[-1]
        booking = {
            'confirmation_number': last['confirmation_number'],
            'booking_details': f"Type: {last['booking_type']}, Date: {last['booking_date']}, Amount: {last['amount']}, Status: {last['status']}"
        }
    else:
        booking = {'confirmation_number': '', 'booking_details': ''}
    return render_template('confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET'])
def travel_recommendations():
    destinations_data = load_destinations()
    trending_destinations = [
        {'dest_id': d['dest_id'], 'name': d['name'], 'popularity': 0} for d in destinations_data
    ]
    return render_template('recommendations.html', trending_destinations=trending_destinations)


if __name__ == '__main__':
    app.run(debug=True)
