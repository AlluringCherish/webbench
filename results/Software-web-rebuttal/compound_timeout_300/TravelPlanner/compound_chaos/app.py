from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data from pipe-delimited text files

def load_destinations():
    filepath = 'data/destinations.txt'
    destinations = []
    if not os.path.exists(filepath):
        return destinations
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                dest_id = int(parts[0])
                destinations.append({
                    'dest_id': dest_id,
                    'name': parts[1],
                    'country': parts[2],
                    'region': parts[3],
                    'description': parts[4],
                    'attractions': [attraction.strip() for attraction in parts[5].split(',')] if parts[5].strip() else [],
                    'climate': parts[6]
                })
    except Exception:
        return []
    return destinations

def load_featured_destinations():
    all_dest = load_destinations()
    featured = []
    for d in all_dest[:3]:
        featured.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'image_url': f"/static/images/destinations/{d['dest_id']}.jpg"
        })
    return featured

def load_upcoming_trips():
    filepath = 'data/trips.txt'
    trips = []
    if not os.path.exists(filepath):
        return trips
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                trip_id = int(parts[0])
                trips.append({
                    'trip_id': trip_id,
                    'trip_name': parts[1],
                    'start_date': parts[3],
                    'end_date': parts[4]
                })
    except Exception:
        return []
    return trips

def load_regions():
    # Fixed regions per spec
    return ['Asia', 'Europe', 'Americas', 'Africa', 'Oceania']

def load_destinations_minimal():
    # For destinations page - subset fields plus image_url
    full_list = load_destinations()
    results = []
    for d in full_list:
        results.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region'],
            'image_url': f"/static/images/destinations/{d['dest_id']}.jpg"
        })
    return results

def load_itineraries():
    filepath = 'data/itineraries.txt'
    itineraries = []
    if not os.path.exists(filepath):
        return itineraries
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                itinerary_id = int(parts[0])
                itineraries.append({
                    'itinerary_id': itinerary_id,
                    'itinerary_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'activities': [a.strip() for a in parts[5].split(',')] if parts[5].strip() else [],
                    'status': parts[6]
                })
    except Exception:
        return []
    return itineraries

def load_hotels():
    filepath = 'data/hotels.txt'
    hotels = []
    if not os.path.exists(filepath):
        return hotels
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=7:
                    continue
                hotel_id = int(parts[0])
                try:
                    rating = float(parts[3])
                except Exception:
                    rating = 0.0
                try:
                    price_per_night = float(parts[4])
                except Exception:
                    price_per_night = 0.0
                hotels.append({
                    'hotel_id': hotel_id,
                    'name': parts[1],
                    'city': parts[2],
                    'rating': rating,
                    'price_per_night': price_per_night,
                    'amenities': [a.strip() for a in parts[5].split(',')] if parts[5].strip() else [],
                    'category': parts[6]
                })
    except Exception:
        return []
    return hotels

def load_flights():
    filepath = 'data/flights.txt'
    flights = []
    if not os.path.exists(filepath):
        return flights
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
                flight_id = int(parts[0])
                try:
                    price = float(parts[6])
                except Exception:
                    price = 0.0
                flights.append({
                    'flight_id': flight_id,
                    'airline': parts[1],
                    'departure_city': parts[2],
                    'arrival_city': parts[3],
                    'departure_time': parts[4],
                    'arrival_time': parts[5],
                    'price': price,
                    'class_type': parts[7],
                    'duration': parts[8]
                })
    except Exception:
        return []
    return flights

def load_packages():
    filepath = 'data/packages.txt'
    packages = []
    if not os.path.exists(filepath):
        return packages
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                package_id = int(parts[0])
                try:
                    duration_days = int(parts[3])
                except Exception:
                    duration_days = 0
                try:
                    price = float(parts[4])
                except Exception:
                    price = 0.0
                packages.append({
                    'package_id': package_id,
                    'package_name': parts[1],
                    'destination': parts[2],
                    'duration_days': duration_days,
                    'price': price,
                    'included_items': [i.strip() for i in parts[5].split(',')] if parts[5].strip() else [],
                    'difficulty_level': parts[6]
                })
    except Exception:
        return []
    return packages

def load_trips():
    filepath = 'data/trips.txt'
    trips = []
    if not os.path.exists(filepath):
        return trips
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                trip_id = int(parts[0])
                try:
                    total_budget = float(parts[5])
                except Exception:
                    total_budget = 0.0
                trips.append({
                    'trip_id': trip_id,
                    'trip_name': parts[1],
                    'destination': parts[2],
                    'start_date': parts[3],
                    'end_date': parts[4],
                    'total_budget': total_budget,
                    'status': parts[6],
                    'created_date': parts[7]
                })
    except Exception:
        return []
    return trips

def load_booking(booking_id):
    filepath = 'data/bookings.txt'
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                b_id = int(parts[0])
                if b_id == booking_id:
                    try:
                        amount = float(parts[4])
                    except Exception:
                        amount = 0.0
                    return {
                        'booking_id': b_id,
                        'trip_id': int(parts[1]),
                        'booking_type': parts[2],
                        'booking_date': parts[3],
                        'amount': amount,
                        'confirmation_number': parts[5],
                        'status': parts[6]
                    }
    except Exception:
        return None
    return None

# Routes implementations

@app.route('/', methods=['GET'])
def dashboard_page():
    # Per spec, root route '/' is GET and returns dashboard.html with context variables
    featured_destinations = load_featured_destinations()
    upcoming_trips = load_upcoming_trips()
    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET'])
def destinations_page():
    destinations = load_destinations_minimal()
    regions = load_regions()
    return render_template('destinations.html', destinations=destinations, regions=regions)

@app.route('/destination/<int:dest_id>', methods=['GET', 'POST'])
def destination_details_page(dest_id):
    destinations = load_destinations()
    destination = next((d for d in destinations if d['dest_id'] == dest_id), None)
    if destination is None:
        return redirect(url_for('destinations_page'))
    if request.method == 'POST':
        # add-to-trip-button triggers POST, redirect to itinerary_page
        return redirect(url_for('itinerary_page'))
    return render_template('destination_details.html', destination=destination)

@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_page():
    itineraries = load_itineraries()
    regions = load_regions()
    if request.method == 'POST':
        # add-activity-button triggers POST, per spec no data persistence required
        return redirect(url_for('itinerary_page'))
    return render_template('itinerary.html', itineraries=itineraries, regions=regions)

@app.route('/accommodations', methods=['GET'])
def accommodations_page():
    hotels = load_hotels()
    return render_template('accommodations.html', hotels=hotels)

@app.route('/transportation', methods=['GET'])
def transportation_page():
    flights = load_flights()
    return render_template('transportation.html', flights=flights)

@app.route('/packages', methods=['GET'])
def packages_page():
    packages = load_packages()
    durations = ['3-5 days', '7-10 days', '14+ days']
    return render_template('packages.html', packages=packages, durations=durations)

@app.route('/trips', methods=['GET'])
def trips_page():
    trips = load_trips()
    return render_template('trips.html', trips=trips)

@app.route('/booking-confirmation/<int:booking_id>', methods=['GET'])
def booking_confirmation_page(booking_id):
    booking = load_booking(booking_id)
    if booking is None:
        return redirect(url_for('dashboard_page'))
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/recommendations', methods=['GET'])
def recommendations_page():
    recommendations = []  # No file specified, empty list
    trending_destinations = []
    destinations = load_destinations()
    for d in destinations:
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'popularity': len(d['attractions'])  # dummy popularity
        })
    return render_template('recommendations.html', recommendations=recommendations, trending_destinations=trending_destinations)

if __name__ == '__main__':
    app.run(debug=True)
