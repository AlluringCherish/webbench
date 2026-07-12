from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Helper functions to load data from files

def load_destinations():
    destinations = []
    file_path = os.path.join(DATA_DIR, 'destinations.txt')
    if not os.path.isfile(file_path):
        return destinations
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                dest_id = int(parts[0])
                name = parts[1]
                country = parts[2]
                region = parts[3]
                description = parts[4]
                attractions = parts[5]
                climate = parts[6]
                destinations.append({
                    'dest_id': dest_id,
                    'name': name,
                    'country': country,
                    'region': region,
                    'description': description,
                    'attractions': attractions,
                    'climate': climate
                })
            except Exception:
                continue
    return destinations


def load_itineraries():
    itineraries = []
    file_path = os.path.join(DATA_DIR, 'itineraries.txt')
    if not os.path.isfile(file_path):
        return itineraries
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                itinerary_id = int(parts[0])
                itinerary_name = parts[1]
                destination = parts[2]
                start_date = parts[3]
                end_date = parts[4]
                activities = parts[5]
                status = parts[6]
                itineraries.append({
                    'itinerary_id': itinerary_id,
                    'itinerary_name': itinerary_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'activities': activities,
                    'status': status
                })
            except Exception:
                continue
    return itineraries


def load_hotels():
    hotels = []
    file_path = os.path.join(DATA_DIR, 'hotels.txt')
    if not os.path.isfile(file_path):
        return hotels
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                hotel_id = int(parts[0])
                name = parts[1]
                city = parts[2]
                rating = float(parts[3])
                price_per_night = float(parts[4])
                amenities = parts[5]
                category = parts[6]
                hotels.append({
                    'hotel_id': hotel_id,
                    'name': name,
                    'city': city,
                    'rating': rating,
                    'price_per_night': price_per_night,
                    'amenities': amenities,
                    'category': category
                })
            except Exception:
                continue
    return hotels


def load_flights():
    flights = []
    file_path = os.path.join(DATA_DIR, 'flights.txt')
    if not os.path.isfile(file_path):
        return flights
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            try:
                flight_id = int(parts[0])
                airline = parts[1]
                departure_city = parts[2]
                arrival_city = parts[3]
                departure_time = parts[4]
                arrival_time = parts[5]
                price = float(parts[6])
                class_type = parts[7]
                duration = parts[8]
                flights.append({
                    'flight_id': flight_id,
                    'airline': airline,
                    'departure_city': departure_city,
                    'arrival_city': arrival_city,
                    'departure_time': departure_time,
                    'arrival_time': arrival_time,
                    'price': price,
                    'class_type': class_type,
                    'duration': duration
                })
            except Exception:
                continue
    return flights


def load_packages():
    packages = []
    file_path = os.path.join(DATA_DIR, 'packages.txt')
    if not os.path.isfile(file_path):
        return packages
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                package_id = int(parts[0])
                package_name = parts[1]
                destination = parts[2]
                duration_days = int(parts[3])
                price = float(parts[4])
                included_items = parts[5]
                difficulty_level = parts[6]
                packages.append({
                    'package_id': package_id,
                    'package_name': package_name,
                    'destination': destination,
                    'duration_days': duration_days,
                    'price': price,
                    'included_items': included_items,
                    'difficulty_level': difficulty_level
                })
            except Exception:
                continue
    return packages


def load_trips():
    trips = []
    file_path = os.path.join(DATA_DIR, 'trips.txt')
    if not os.path.isfile(file_path):
        return trips
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                trip_id = int(parts[0])
                trip_name = parts[1]
                destination = parts[2]
                start_date = parts[3]
                end_date = parts[4]
                total_budget = float(parts[5])
                status = parts[6]
                created_date = parts[7]
                trips.append({
                    'trip_id': trip_id,
                    'trip_name': trip_name,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_budget': total_budget,
                    'status': status,
                    'created_date': created_date
                })
            except Exception:
                continue
    return trips


def load_bookings():
    bookings = []
    file_path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.isfile(file_path):
        return bookings
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            try:
                booking_id = int(parts[0])
                trip_id = int(parts[1])
                booking_type = parts[2]
                booking_date = parts[3]
                amount = float(parts[4])
                confirmation_number = parts[5]
                status = parts[6]
                bookings.append({
                    'booking_id': booking_id,
                    'trip_id': trip_id,
                    'booking_type': booking_type,
                    'booking_date': booking_date,
                    'amount': amount,
                    'confirmation_number': confirmation_number,
                    'status': status
                })
            except Exception:
                continue
    return bookings


# Routes implementation

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    destinations_all = load_destinations()
    featured_destinations = []
    if len(destinations_all) >= 2:
        featured_destinations = [
            {"dest_id": destinations_all[0]["dest_id"], "name": destinations_all[0]["name"], "country": destinations_all[0]["country"]},
            {"dest_id": destinations_all[1]["dest_id"], "name": destinations_all[1]["name"], "country": destinations_all[1]["country"]}
        ]
    elif len(destinations_all) == 1:
        featured_destinations = [
            {"dest_id": destinations_all[0]["dest_id"], "name": destinations_all[0]["name"], "country": destinations_all[0]["country"]}
        ]

    trips_all = load_trips()
    upcoming_trips = []
    if trips_all:
        trips_sorted = sorted(trips_all, key=lambda t: t['start_date'])
        for trip in trips_sorted:
            upcoming_trips.append({
                "trip_id": trip["trip_id"],
                "trip_name": trip["trip_name"],
                "destination": trip["destination"],
                "start_date": trip["start_date"],
                "end_date": trip["end_date"]
            })
        upcoming_trips = upcoming_trips[:1]

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)

@app.route('/destinations', methods=['GET'])
def destinations():
    destinations_all = load_destinations()
    regions = ["Asia", "Europe", "Americas", "Africa", "Oceania"]
    selected_region = request.args.get('region')
    if selected_region == '':
        selected_region = None
    search_query = request.args.get('search')
    if search_query == '':
        search_query = None
    filtered_destinations = destinations_all
    if selected_region is not None:
        filtered_destinations = [d for d in filtered_destinations if d['region'] == selected_region]
    if search_query is not None:
        sq = search_query.lower()
        filtered_destinations = [d for d in filtered_destinations if sq in d['name'].lower() or sq in d['country'].lower()]
    filtered_dest_context = [{"dest_id": d["dest_id"], "name": d["name"], "country": d["country"]} for d in filtered_destinations]
    return render_template('destinations.html',
                           destinations=filtered_dest_context,
                           regions=regions,
                           selected_region=selected_region,
                           search_query=search_query)

@app.route('/destinations/<int:dest_id>', methods=['GET'])
def destination_details(dest_id):
    destinations_all = load_destinations()
    destination_data = None
    for d in destinations_all:
        if d['dest_id'] == dest_id:
            destination_data = {
                'dest_id': d['dest_id'],
                'name': d['name'],
                'country': d['country'],
                'description': d['description'],
                'attractions': d['attractions']
            }
            break
    if destination_data is None:
        return redirect(url_for('destinations'))
    return render_template('destination_details.html', destination=destination_data)

@app.route('/itinerary', methods=['GET', 'POST'])
def plan_itinerary():
    itineraries = load_itineraries()
    if request.method == 'POST':
        itinerary_id = request.form.get('itinerary_id')
        new_activity = request.form.get('new_activity')
        if itinerary_id and new_activity:
            try:
                itinerary_id_int = int(itinerary_id)
                for itinerary in itineraries:
                    if itinerary['itinerary_id'] == itinerary_id_int:
                        if itinerary['activities']:
                            itinerary['activities'] += ', ' + new_activity
                        else:
                            itinerary['activities'] = new_activity
                        break
            except Exception:
                pass
    return render_template('itinerary.html', itineraries=itineraries)

@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    hotels_all = load_hotels()
    price_ranges = ["Budget", "Mid-range", "Luxury"]
    if request.method == 'POST':
        destination = request.form.get('destination', '')
        check_in_date = request.form.get('check_in_date', '')
        check_out_date = request.form.get('check_out_date', '')
        price_filter = request.form.get('price_filter') or None
    else:
        destination = ''
        check_in_date = ''
        check_out_date = ''
        price_filter = None
    filtered_hotels = hotels_all
    if destination:
        filtered_hotels = [h for h in filtered_hotels if h['city'].lower() == destination.lower()]
    if price_filter:
        filtered_hotels = [h for h in filtered_hotels if h['category'] == price_filter]
    search_params = {
        'destination': destination,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'price_filter': price_filter
    }
    return render_template('accommodations.html', hotels=filtered_hotels, price_ranges=price_ranges, search_params=search_params)

@app.route('/flights', methods=['GET', 'POST'])
def book_flights():
    flights_all = load_flights()
    flight_classes = ["Economy", "Business", "First Class"]
    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '')
        arrival_city = request.form.get('arrival_city', '')
        departure_date = request.form.get('departure_date', '')
        flight_class_filter = request.form.get('flight_class_filter') or None
    else:
        departure_city = ''
        arrival_city = ''
        departure_date = ''
        flight_class_filter = None
    filtered_flights = flights_all
    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city.lower()]
    if flight_class_filter:
        filtered_flights = [f for f in filtered_flights if f['class_type'] == flight_class_filter]
    search_params = {
        'departure_city': departure_city,
        'arrival_city': arrival_city,
        'departure_date': departure_date,
        'flight_class_filter': flight_class_filter
    }
    return render_template('flights.html', available_flights=filtered_flights, flight_classes=flight_classes, search_params=search_params)

@app.route('/packages', methods=['GET', 'POST'])
def travel_packages():
    packages_all = load_packages()
    duration_filters = ["3-5 days", "7-10 days", "14+ days"]
    selected_duration_filter = None
    if request.method == 'POST':
        selected_duration_filter = request.form.get('duration_filter') or None
    if selected_duration_filter:
        if selected_duration_filter == "3-5 days":
            filtered_packages = [p for p in packages_all if 3 <= p['duration_days'] <= 5]
        elif selected_duration_filter == "7-10 days":
            filtered_packages = [p for p in packages_all if 7 <= p['duration_days'] <= 10]
        elif selected_duration_filter == "14+ days":
            filtered_packages = [p for p in packages_all if p['duration_days'] >= 14]
        else:
            filtered_packages = packages_all
    else:
        filtered_packages = packages_all
    return render_template('packages.html',
                           packages=filtered_packages,
                           duration_filters=duration_filters,
                           selected_duration_filter=selected_duration_filter)

@app.route('/trips', methods=['GET', 'POST'])
def manage_trips():
    trips_all = load_trips()
    if request.method == 'POST':
        action = request.form.get('action')
        trip_id_str = request.form.get('trip_id')
        if action == 'delete' and trip_id_str:
            try:
                trip_id = int(trip_id_str)
                trips_all = [t for t in trips_all if t['trip_id'] != trip_id]
            except Exception:
                pass
    return render_template('trips.html', trips=trips_all)

@app.route('/confirmation/<int:booking_id>', methods=['GET'])
def booking_confirmation(booking_id):
    bookings_all = load_bookings()
    booking_data = None
    for b in bookings_all:
        if b['booking_id'] == booking_id:
            booking_data = b
            break
    if booking_data is None:
        return redirect(url_for('dashboard'))
    return render_template('confirmation.html', booking=booking_data)

@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations():
    trending_destinations = []
    destinations_all = load_destinations()
    if len(destinations_all) >= 2:
        trending_destinations = [
            {"dest_id": destinations_all[0]["dest_id"], "name": destinations_all[0]["name"], "popularity_rank": 1},
            {"dest_id": destinations_all[1]["dest_id"], "name": destinations_all[1]["name"], "popularity_rank": 2}
        ]
    elif len(destinations_all) == 1:
        trending_destinations = [
            {"dest_id": destinations_all[0]["dest_id"], "name": destinations_all[0]["name"], "popularity_rank": 1}
        ]
    seasons = ["Spring", "Summer", "Fall", "Winter"]
    budgets = ["Low", "Medium", "High"]
    selected_season = None
    selected_budget = None
    if request.method == 'POST':
        selected_season = request.form.get('season') or None
        selected_budget = request.form.get('budget') or None
    return render_template('recommendations.html',
                           trending_destinations=trending_destinations,
                           seasons=seasons,
                           budgets=budgets,
                           selected_season=selected_season,
                           selected_budget=selected_budget)


if __name__ == '__main__':
    app.run(debug=True)
