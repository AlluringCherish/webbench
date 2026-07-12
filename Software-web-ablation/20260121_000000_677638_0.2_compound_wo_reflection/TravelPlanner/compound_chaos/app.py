from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

import os

def read_destinations():
    destinations = []
    try:
        with open('data/destinations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                dest_id_str, name, country, region, description, attractions, climate = parts
                try:
                    dest_id = int(dest_id_str)
                except ValueError:
                    continue
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
        destinations = []
    return destinations


def read_itineraries():
    itineraries = []
    try:
        with open('data/itineraries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                itinerary_id_str, itinerary_name, destination, start_date, end_date, activities, status = parts
                try:
                    itinerary_id = int(itinerary_id_str)
                except ValueError:
                    continue
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
        itineraries = []
    return itineraries


def read_hotels():
    hotels = []
    try:
        with open('data/hotels.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                hotel_id_str, name, city, rating_str, price_str, amenities, category = parts
                try:
                    hotel_id = int(hotel_id_str)
                    rating = float(rating_str)
                    price_per_night = float(price_str)
                except ValueError:
                    continue
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
        hotels = []
    return hotels


def read_flights():
    flights = []
    try:
        with open('data/flights.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 9:
                    continue
                flight_id_str, airline, departure_city, arrival_city, departure_time, arrival_time, price_str, class_type, duration = parts
                try:
                    flight_id = int(flight_id_str)
                    price = float(price_str)
                except ValueError:
                    continue
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
        flights = []
    return flights


def read_packages():
    packages = []
    try:
        with open('data/packages.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                package_id_str, package_name, destination, duration_days_str, price_str, included_items, difficulty_level = parts
                try:
                    package_id = int(package_id_str)
                    duration_days = int(duration_days_str)
                    price = float(price_str)
                except ValueError:
                    continue
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
        packages = []
    return packages


def read_trips():
    trips = []
    try:
        with open('data/trips.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                trip_id_str, trip_name, destination, start_date, end_date, total_budget_str, status, created_date = parts
                try:
                    trip_id = int(trip_id_str)
                    total_budget = float(total_budget_str)
                except ValueError:
                    continue
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
        trips = []
    return trips


def read_bookings():
    bookings = []
    try:
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                booking_id_str, trip_id_str, booking_type, booking_date, amount_str, confirmation_number, status = parts
                try:
                    booking_id = int(booking_id_str)
                    trip_id = int(trip_id_str)
                    amount = float(amount_str)
                except ValueError:
                    continue
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
        bookings = []
    return bookings


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    # Load featured destinations (example: dest_id, name, country) from destinations.txt
    destinations = read_destinations()
    # Use first two destinations as featured for example
    featured_destinations = []
    for dest in destinations[:2]:
        featured_destinations.append({
            'dest_id': dest['dest_id'],
            'name': dest['name'],
            'country': dest['country']
        })

    # Load upcoming trips (example: trip_id, trip_name, start_date) from trips.txt
    trips = read_trips()
    # We consider upcoming trips as trips with start_date in future or all trips for demo, take first one for example
    upcoming_trips = []
    if trips:
        # Let's take trips which start later than today as upcoming (using string compare, basic)
        from datetime import datetime
        today_str = datetime.today().strftime('%Y-%m-%d')
        for trip in trips:
            if trip['start_date'] >= today_str:
                upcoming_trips.append({
                    'trip_id': trip['trip_id'],
                    'trip_name': trip['trip_name'],
                    'start_date': trip['start_date']
                })
        # fallback if none upcoming
        if not upcoming_trips:
            trip = trips[0]
            upcoming_trips.append({
                'trip_id': trip['trip_id'],
                'trip_name': trip['trip_name'],
                'start_date': trip['start_date']
            })

    return render_template('dashboard.html', featured_destinations=featured_destinations, upcoming_trips=upcoming_trips)


@app.route('/destinations', methods=['GET', 'POST'])
def destinations_page():
    destinations = read_destinations()
    selected_region = ''
    search_query = ''

    if request.method == 'POST':
        selected_region = request.form.get('region_filter', '').strip()
        search_query = request.form.get('search_destination', '').strip()

    # Filter destinations by region if selected
    if selected_region:
        destinations = [d for d in destinations if d['region'].lower() == selected_region.lower()]

    # Filter destinations by search query if provided (case insensitive substring match on name)
    if search_query:
        sq_lower = search_query.lower()
        destinations = [d for d in destinations if sq_lower in d['name'].lower()]

    # For context variables destinations: List[Dict[str, Any]] with keys dest_id, name, country, region
    destinations_for_context = []
    for d in destinations:
        destinations_for_context.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'country': d['country'],
            'region': d['region']
        })

    return render_template('destinations.html', destinations=destinations_for_context, selected_region=selected_region, search_query=search_query)


@app.route('/destinations/<int:dest_id>', methods=['GET', 'POST'])
def destination_details_page(dest_id):
    destinations = read_destinations()
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
        # If not found, can redirect to destinations page
        return redirect(url_for('destinations_page'))

    if request.method == 'POST':
        # POST for add to trip action (no implementation details specified)
        # For demonstration, we redirect back to this detail page
        return redirect(url_for('destination_details_page', dest_id=dest_id))

    return render_template('destination_details.html', destination=destination)


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_planning_page():
    itineraries = read_itineraries()

    if request.method == 'POST':
        # POST for creating/editing itinerary (no implementation details specified)
        # Redirect back to itinerary page
        return redirect(url_for('itinerary_planning_page'))

    # Context variable: itineraries with keys itinerary_id, itinerary_name, start_date, end_date, status
    itineraries_for_context = []
    for it in itineraries:
        itineraries_for_context.append({
            'itinerary_id': it['itinerary_id'],
            'itinerary_name': it['itinerary_name'],
            'start_date': it['start_date'],
            'end_date': it['end_date'],
            'status': it['status']
        })

    return render_template('itinerary.html', itineraries=itineraries_for_context)


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations_page():
    hotels = read_hotels()
    search_destination = ''
    check_in_date = ''
    check_out_date = ''
    selected_price_filter = ''

    if request.method == 'POST':
        search_destination = request.form.get('search_destination', '').strip()
        check_in_date = request.form.get('check_in_date', '').strip()
        check_out_date = request.form.get('check_out_date', '').strip()
        selected_price_filter = request.form.get('price_filter', '').strip()

    # Filter hotels by destination if specified (case insensitive exact match city)
    filtered_hotels = hotels
    if search_destination:
        filtered_hotels = [h for h in hotels if h['city'].lower() == search_destination.lower()]

    # Filter by price filter if specified
    # Price categories mapping for example:
    # Budget: <100, Mid-range: 100-300, Luxury: >300
    if selected_price_filter:
        if selected_price_filter.lower() == 'budget':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] < 100]
        elif selected_price_filter.lower() == 'mid-range':
            filtered_hotels = [h for h in filtered_hotels if 100 <= h['price_per_night'] <= 300]
        elif selected_price_filter.lower() == 'luxury':
            filtered_hotels = [h for h in filtered_hotels if h['price_per_night'] > 300]

    return render_template('accommodations.html', hotels=filtered_hotels, search_destination=search_destination,
                           check_in_date=check_in_date, check_out_date=check_out_date,
                           selected_price_filter=selected_price_filter)


@app.route('/transportation', methods=['GET', 'POST'])
def transportation_page():
    flights = read_flights()
    departure_city = ''
    arrival_city = ''
    departure_date = ''
    selected_class_filter = ''

    if request.method == 'POST':
        departure_city = request.form.get('departure_city', '').strip()
        arrival_city = request.form.get('arrival_city', '').strip()
        departure_date = request.form.get('departure_date', '').strip()
        selected_class_filter = request.form.get('flight_class_filter', '').strip()

    # Filter flights by departure_city and arrival_city if specified (case insensitive exact match)
    filtered_flights = flights
    if departure_city:
        filtered_flights = [f for f in filtered_flights if f['departure_city'].lower() == departure_city.lower()]
    if arrival_city:
        filtered_flights = [f for f in filtered_flights if f['arrival_city'].lower() == arrival_city.lower()]

    # Filter by class type
    if selected_class_filter:
        filtered_flights = [f for f in filtered_flights if f['class_type'].lower() == selected_class_filter.lower()]

    return render_template('transportation.html', available_flights=filtered_flights, departure_city=departure_city,
                           arrival_city=arrival_city, departure_date=departure_date, selected_class_filter=selected_class_filter)


@app.route('/packages', methods=['GET'])
def travel_packages_page():
    packages = read_packages()
    selected_duration_filter = ''

    # Filter packages by duration filter if specified in query param
    selected_duration_filter = request.args.get('duration_filter', '').strip()
    if selected_duration_filter:
        # Example duration filter strings: "3-5 days", "6-10 days"
        try:
            parts = selected_duration_filter.split(' ')[0].split('-')
            if len(parts) == 2:
                min_days = int(parts[0])
                max_days = int(parts[1])
                packages = [p for p in packages if min_days <= p['duration_days'] <= max_days]
        except Exception:
            pass

    return render_template('packages.html', packages=packages, selected_duration_filter=selected_duration_filter)


@app.route('/trips', methods=['GET', 'POST'])
def trip_management_page():
    trips = read_trips()

    if request.method == 'POST':
        # POST for edit/delete actions
        # No implementation details, redirect back to trips
        return redirect(url_for('trip_management_page'))

    return render_template('trips.html', trips=trips)


@app.route('/booking-confirmation/<int:booking_id>', methods=['GET'])
def booking_confirmation_page(booking_id):
    bookings = read_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = {
                'booking_id': b['booking_id'],
                'confirmation_number': b['confirmation_number'],
                'booking_date': b['booking_date'],
                'amount': b['amount'],
                'details': f"{b['booking_type']} booking for trip {b['trip_id']}"
            }
            break

    if booking is None:
        # If not found, redirect to dashboard
        return redirect(url_for('dashboard_page'))

    return render_template('booking_confirmation.html', booking=booking)


@app.route('/recommendations', methods=['GET', 'POST'])
def travel_recommendations_page():
    destinations = read_destinations()
    trending_destinations = []

    # For trending_destinations: List[Dict[str, Any]] with keys dest_id, name, popularity_rank
    # As popularity rank is not in data, fake it by ordering by dest_id ascending
    sorted_dest = sorted(destinations, key=lambda d: d['dest_id'])
    rank = 1
    for d in sorted_dest:
        trending_destinations.append({
            'dest_id': d['dest_id'],
            'name': d['name'],
            'popularity_rank': rank
        })
        rank += 1

    selected_season_filter = ''
    selected_budget_filter = ''

    if request.method == 'POST':
        selected_season_filter = request.form.get('recommendation_season_filter', '').strip()
        selected_budget_filter = request.form.get('budget_filter', '').strip()

    return render_template('recommendations.html', trending_destinations=trending_destinations,
                           selected_season_filter=selected_season_filter,
                           selected_budget_filter=selected_budget_filter)


if __name__ == '__main__':
    app.run(debug=True)
