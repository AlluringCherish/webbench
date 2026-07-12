from flask import Flask, render_template, redirect, url_for, request
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Utils functions to load data

def load_movies():
    movies = []
    path = os.path.join(DATA_DIR, 'movies.txt')
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 8:
                    continue
                movie = {
                    'movie_id': int(row[0]),
                    'title': row[1],
                    'director': row[2],
                    'genre': row[3],
                    'rating': float(row[4]),
                    'duration': int(row[5]),
                    'description': row[6],
                    'release_date': row[7]
                }
                movies.append(movie)
    except Exception as e:
        print(f'Error loading movies: {e}')
    return movies


def load_theaters():
    theaters = []
    path = os.path.join(DATA_DIR, 'theaters.txt')
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 6:
                    continue
                theater = {
                    'theater_id': int(row[0]),
                    'name': row[1],
                    'location': row[2],
                    'city': row[3],
                    'screens': int(row[4]),
                    'facilities': row[5]
                }
                theaters.append(theater)
    except Exception as e:
        print(f'Error loading theaters: {e}')
    return theaters


def load_showtimes():
    showtimes = []
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 7:
                    continue
                showtime = {
                    'showtime_id': int(row[0]),
                    'movie_id': int(row[1]),
                    'theater_id': int(row[2]),
                    'date': row[3],
                    'time': row[4],
                    'price': float(row[5]),
                    'available_seats': int(row[6])
                }
                showtimes.append(showtime)
    except Exception as e:
        print(f'Error loading showtimes: {e}')
    return showtimes


def load_seats():
    seats = []
    path = os.path.join(DATA_DIR, 'seats.txt')
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 7:
                    continue
                seat = {
                    'seat_id': row[0],
                    'theater_id': int(row[1]),
                    'screen_id': int(row[2]),
                    'row': row[3],
                    'column': row[4],
                    'seat_type': row[5],
                    'status': row[6]
                }
                seats.append(seat)
    except Exception as e:
        print(f'Error loading seats: {e}')
    return seats


def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 8:
                    continue
                booking = {
                    'booking_id': int(row[0]),
                    'showtime_id': int(row[1]),
                    'customer_name': row[2],
                    'customer_email': row[3],
                    'booking_date': row[4],
                    'total_price': float(row[5]),
                    'status': row[6],
                    'seats_booked': row[7].split(',') if row[7] else []
                }
                bookings.append(booking)
    except Exception as e:
        print(f'Error loading bookings: {e}')
    return bookings


def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for b in bookings:
                row = [
                    b['booking_id'],
                    b['showtime_id'],
                    b['customer_name'],
                    b['customer_email'],
                    b['booking_date'],
                    f"{b['total_price']:.2f}",
                    b['status'],
                    ','.join(b['seats_booked'])
                ]
                writer.writerow(row)
    except Exception as e:
        print(f'Error saving bookings: {e}')


def save_showtimes(showtimes):
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    try:
        with open(path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for s in showtimes:
                row = [
                    s['showtime_id'],
                    s['movie_id'],
                    s['theater_id'],
                    s['date'],
                    s['time'],
                    f"{s['price']:.2f}",
                    s['available_seats']
                ]
                writer.writerow(row)
    except Exception as e:
        print(f'Error saving showtimes: {e}')

# Helper to get next booking_id

def next_booking_id(bookings):
    if not bookings:
        return 1
    return max(b['booking_id'] for b in bookings) + 1

# Root route redirect to dashboard

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # For simplicity, mark first 5 movies as featured
    featured_movies = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'poster_url': ''  # No poster_url in data, leave empty or could derive
        } for m in movies[:5]
    ]
    # The task says etc. not detailed explicitly, so we only pass featured_movies
    return render_template('dashboard.html', featured_movies=featured_movies)

# MOVIE CATALOG
@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    # Provide movies list with movie_id, title, genre, rating, duration, poster_url(empty since not in data)
    movie_list = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster_url': ''
        } for m in movies
    ]
    return render_template('movie_catalog.html', movies=movie_list)

# MOVIE DETAILS
@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    # Provide movie dict with movie_id, title, director, rating, description
    movie_dict = {
        'movie_id': movie['movie_id'],
        'title': movie['title'],
        'director': movie['director'],
        'rating': movie['rating'],
        'description': movie['description']
    }
    return render_template('movie_details.html', movie=movie_dict)

# SHOWTIME SELECTION
@app.route('/movies/<int:movie_id>/showtimes')
def showtime_selection(movie_id):
    showtimes_all = load_showtimes()
    theaters = load_theaters()
    # Filter showtimes by movie_id
    showtimes_filtered = [
        {
            'showtime_id': s['showtime_id'],
            'date': s['date'],
            'time': s['time'],
            'theater_name': next((t['name'] for t in theaters if t['theater_id'] == s['theater_id']), 'Unknown'),
            'price': s['price']
        }
        for s in showtimes_all if s['movie_id'] == movie_id
    ]
    return render_template('showtime_selection.html', showtimes=showtimes_filtered)

# SEAT SELECTION GET
@app.route('/showtimes/<int:showtime_id>/seats', methods=['GET'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    seats = load_seats()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    # Get theater and screen from showtime
    theater_id = showtime['theater_id']
    # Assuming screen_id can be 1 or get from seats for the theater - seats.txt has screen_id field

    # For simplicity, get screen_id of first seat with this theater
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater_id]
    screen_id = None
    if theater_seats:
        screen_id = theater_seats[0]['screen_id']

    # Filter seats for this theater and screen
    seat_map = [
        {
            'seat_id': seat['seat_id'],
            'status': seat['status']
        }
        for seat in seats if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id
    ]
    selected_seats = []
    return render_template('seat_selection.html', seat_map=seat_map, selected_seats=selected_seats)

# SEAT SELECTION POST
@app.route('/showtimes/<int:showtime_id>/seats', methods=['POST'])
def seat_selection_post(showtime_id):
    showtimes = load_showtimes()
    bookings = load_bookings()
    seats = load_seats()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    theater_id = showtime['theater_id']
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater_id]
    screen_id = None
    if theater_seats:
        screen_id = theater_seats[0]['screen_id']

    selected_seats = request.form.getlist('selected_seats')

    errors = None

    # Validate seats availability
    seat_map = []
    seat_status_lookup = {}
    for seat in seats:
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
            seat_status_lookup[seat['seat_id']] = seat['status']

    for seat_id in selected_seats:
        if seat_id not in seat_status_lookup:
            errors = "One or more selected seats are invalid."
            break
        if seat_status_lookup[seat_id] != 'Available':
            errors = f"Seat {seat_id} is not available."
            break

    if errors:
        # re-render with errors and current seat_map and selected seats
        seat_map = [
            {
                'seat_id': s['seat_id'],
                'status': s['status']
            }
            for s in seats if s['theater_id'] == theater_id and s['screen_id'] == screen_id
        ]
        return render_template('seat_selection.html', errors=errors, seat_map=seat_map, selected_seats=selected_seats)

    # If valid, proceed to booking confirmation
    # Save selected seats in session or a mechanism is not specified. We'll simulate by passing params in redirect with comma joined
    seats_param = ','.join(selected_seats)
    return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=seats_param))

# BOOKING CONFIRMATION GET
@app.route('/booking/confirm')
def booking_confirmation():
    # Get showtime_id and seats from query parameters
    showtime_id = request.args.get('showtime_id', type=int)
    seats_param = request.args.get('seats', '')
    selected_seats = seats_param.split(',') if seats_param else []

    showtimes = load_showtimes()
    movies = load_movies()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404

    booking_summary = {
        'movie': movie['title'],
        'showtime': f"{showtime['date']} {showtime['time']}",
        'seats': selected_seats,
        'total': len(selected_seats) * showtime['price']
    }
    return render_template('booking_confirmation.html', booking_summary=booking_summary)

# BOOKING CONFIRMATION POST
@app.route('/booking/confirm', methods=['POST'])
def booking_confirmation_post():
    showtime_id = request.args.get('showtime_id', type=int)
    seats_param = request.args.get('seats', '')
    selected_seats = seats_param.split(',') if seats_param else []

    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()

    errors = None

    if not customer_name or not customer_email:
        errors = 'Customer name and email are required.'
    elif '@' not in customer_email:
        errors = 'Invalid email address.'

    if errors:
        # Re-render with error
        showtimes = load_showtimes()
        movies = load_movies()

        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        movie = None
        if showtime:
            movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)

        booking_summary = {
            'movie': movie['title'] if movie else 'Unknown',
            'showtime': f"{showtime['date']} {showtime['time']}" if showtime else 'Unknown',
            'seats': selected_seats,
            'total': len(selected_seats) * showtime['price'] if showtime else 0
        }

        return render_template('booking_confirmation.html', errors=errors, booking_summary=booking_summary)

    # Save booking
    showtimes = load_showtimes()
    bookings = load_bookings()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    # Create booking
    booking_id = next_booking_id(bookings)
    booking_date = datetime.now().strftime('%Y-%m-%d')
    total_price = len(selected_seats) * showtime['price']

    booking = {
        'booking_id': booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': selected_seats
    }
    # Update seat status to Booked in seats file
    seats = load_seats()
    seat_ids_set = set(selected_seats)
    for seat in seats:
        if seat['seat_id'] in seat_ids_set and seat['status'] == 'Available':
            seat['status'] = 'Booked'

    # Reduce available seats in showtime
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            s['available_seats'] -= len(selected_seats)
            break

    bookings.append(booking)

    # Save back data
    save_bookings(bookings)
    save_showtimes(showtimes)

    confirmation_status = 'Booking confirmed successfully!'
    return render_template('booking_confirmation.html', confirmation_status=confirmation_status)

# BOOKING HISTORY
@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()
    # Prepare a list with required fields booking_id, movie, date, seats, status
    bookings_list = []
    for b in bookings:
        showtime = next((s for s in load_showtimes() if s['showtime_id'] == b['showtime_id']), None)
        movie = next((m for m in movies if showtime and m['movie_id'] == showtime['movie_id']), None)
        bookings_list.append({
            'booking_id': b['booking_id'],
            'movie': movie['title'] if movie else 'Unknown',
            'date': b['booking_date'],
            'seats': ','.join(b['seats_booked']),
            'status': b['status']
        })
    return render_template('booking_history.html', bookings=bookings_list)

# BOOKING DETAILS
@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()

    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    movie = None
    theater = None
    if showtime:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    booking_detail = {
        'booking_id': booking['booking_id'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'booking_date': booking['booking_date'],
        'total_price': booking['total_price'],
        'status': booking['status'],
        'seats_booked': booking['seats_booked'],
        'movie_title': movie['title'] if movie else 'Unknown',
        'showtime_date': showtime['date'] if showtime else 'Unknown',
        'showtime_time': showtime['time'] if showtime else 'Unknown',
        'theater_name': theater['name'] if theater else 'Unknown',
        'theater_location': theater['location'] if theater else 'Unknown'
    }

    return render_template('booking_details.html', booking=booking_detail)

# THEATER INFORMATION
@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    theater_list = [
        {
            'theater_id': t['theater_id'],
            'name': t['name'],
            'location': t['location'],
            'screens': t['screens'],
            'facilities': t['facilities']
        } for t in theaters
    ]
    return render_template('theater_information.html', theaters=theater_list)


if __name__ == '__main__':
    app.run()
