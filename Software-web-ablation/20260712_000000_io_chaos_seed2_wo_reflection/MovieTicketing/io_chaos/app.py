from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
MOVIES_FILE = 'data/movies.txt'
THEATERS_FILE = 'data/theaters.txt'
SHOWTIMES_FILE = 'data/showtimes.txt'
SEATS_FILE = 'data/seats.txt'
BOOKINGS_FILE = 'data/bookings.txt'
GENRES_FILE = 'data/genres.txt'


# Helper functions for loading and saving data

def load_movies():
    movies = []
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    movie = {
                        'movie_id': int(parts[0]),
                        'title': parts[1],
                        'director': parts[2],
                        'genre': parts[3],
                        'rating': float(parts[4]),
                        'duration': int(parts[5]),
                        'description': parts[6],
                        'release_date': parts[7]
                    }
                    movies.append(movie)
    except IOError:
        pass
    return movies


def load_theaters():
    theaters = []
    try:
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    theater = {
                        'theater_id': int(parts[0]),
                        'theater_name': parts[1],
                        'location': parts[2],
                        'city': parts[3],
                        'screens': int(parts[4]),
                        'facilities': parts[5]
                    }
                    theaters.append(theater)
    except IOError:
        pass
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    showtime = {
                        'showtime_id': int(parts[0]),
                        'movie_id': int(parts[1]),
                        'theater_id': int(parts[2]),
                        'showtime_date': parts[3],
                        'showtime_time': parts[4],
                        'price': float(parts[5]),
                        'available_seats': int(parts[6])
                    }
                    showtimes.append(showtime)
    except IOError:
        pass
    return showtimes


def load_seats():
    seats = []
    try:
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    seat = {
                        'seat_id': int(parts[0]),
                        'theater_id': int(parts[1]),
                        'screen_id': int(parts[2]),
                        'row': parts[3],
                        'column': int(parts[4]),
                        'seat_type': parts[5],
                        'status': parts[6]
                    }
                    seats.append(seat)
    except IOError:
        pass
    return seats


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    booking = {
                        'booking_id': int(parts[0]),
                        'showtime_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'booking_date': parts[4],
                        'total_price': float(parts[5]),
                        'status': parts[6],
                        'seats_booked': parts[7].split(',') if parts[7] else []
                    }
                    bookings.append(booking)
    except IOError:
        pass
    return bookings


def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats_booked']) if b['seats_booked'] else ''
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
                f.write(line)
    except IOError:
        pass


# Section 1: Flask routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Featured movies logic: could take first 3 highest rating movies for example
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    # Prepare data for template
    simple_featured = [{'movie_id': m['movie_id'], 'title': m['title'], 'genre': m['genre'], 'rating': m['rating']} for m in featured_movies]
    return render_template('dashboard.html', featured_movies=simple_featured)


@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    simple_movies = [{'movie_id': m['movie_id'], 'title': m['title'], 'genre': m['genre'], 'rating': m['rating'], 'duration': m['duration']} for m in movies]
    return render_template('movie_catalog.html', movies=simple_movies)


@app.route('/movies/search', methods=['POST'])
def movie_search():
    movies = load_movies()
    search_term = request.form.get('search_input', '').strip().lower()
    genre_filter = request.form.get('genre_filter', '').strip().lower()

    filtered = movies
    if search_term:
        filtered = [m for m in filtered if search_term in m['title'].lower() or search_term in m['genre'].lower()]
    if genre_filter:
        filtered = [m for m in filtered if m['genre'].lower() == genre_filter]

    simple_movies = [{'movie_id': m['movie_id'], 'title': m['title'], 'genre': m['genre'], 'rating': m['rating'], 'duration': m['duration']} for m in filtered]
    return render_template('movie_catalog.html', movies=simple_movies)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return 'Movie not found', 404
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/<int:movie_id>')
def select_showtime(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()

    # Filter showtimes for movie
    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]

    # Optional filter: theater and date from query args
    theater_filter = request.args.get('theater_filter', '').strip()
    date_filter = request.args.get('date_filter', '').strip()
    if theater_filter:
        try:
            theater_id_filter = int(theater_filter)
            filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] == theater_id_filter]
        except ValueError:
            pass
    if date_filter:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == date_filter]

    return render_template('select_showtime.html', showtimes=filtered_showtimes, theaters=theaters)


@app.route('/bookings/showtime/<int:showtime_id>/seats')
def select_seats(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return 'Showtime not found', 404

    seats = load_seats()
    # Filter seats by theater and screen - assuming screen_id is 1 for simplicity as no detail in spec
    # We'll filter only by theater from showtime
    seat_map = [s for s in seats if s['theater_id'] == showtime['theater_id']]

    # Count available seats
    available_seats = len([s for s in seat_map if s['status'].lower() == 'available'])

    return render_template('seat_selection.html', seat_map=seat_map, available_seats=available_seats)


@app.route('/bookings/select', methods=['POST'])
def booking_confirmation():
    # Receive booking details from form
    # Required fields: movie_title, showtime_date, showtime_time, theater_name, seats_selected (list), total_price
    movie_title = request.form.get('movie_title', '')
    showtime_date = request.form.get('showtime_date', '')
    showtime_time = request.form.get('showtime_time', '')
    theater_name = request.form.get('theater_name', '')
    seats_selected = request.form.getlist('seats_selected')
    try:
        total_price = float(request.form.get('total_price', '0'))
    except ValueError:
        total_price = 0.0

    booking_summary = {
        'movie_title': movie_title,
        'showtime_date': showtime_date,
        'showtime_time': showtime_time,
        'theater_name': theater_name,
        'seats_selected': seats_selected,
        'total_price': total_price
    }

    if request.method == 'POST':
        # On POST, confirm booking and save it
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()

        if customer_name and customer_email and seats_selected:
            bookings = load_bookings()
            new_id = max([b['booking_id'] for b in bookings], default=0) + 1
            from datetime import datetime
            booking_date = datetime.now().strftime('%Y-%m-%d')
            new_booking = {
                'booking_id': new_id,
                'showtime_id': int(request.form.get('showtime_id', '0')),
                'customer_name': customer_name,
                'customer_email': customer_email,
                'booking_date': booking_date,
                'total_price': total_price,
                'status': 'Confirmed',
                'seats_booked': seats_selected
            }
            bookings.append(new_booking)
            save_bookings(bookings)
            return render_template('booking_confirmation.html', booking_summary=booking_summary, success=True)

    return render_template('booking_confirmation.html', booking_summary=booking_summary)


@app.route('/bookings/history')
def booking_history():
    bookings = load_bookings()
    filter_status = request.args.get('status_filter', '').strip().lower()
    filtered_bookings = bookings
    if filter_status:
        filtered_bookings = [b for b in bookings if b['status'].lower() == filter_status]

    # Prepare filter options for UI
    filter_options = list(set(b['status'] for b in bookings))

    return render_template('booking_history.html', bookings=filtered_bookings, filter_options=filter_options)


@app.route('/bookings/<int:booking_id>')
def view_booking(booking_id):
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    booking_detail = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking_detail:
        return 'Booking not found', 404

    # Get movie title from showtime
    showtime = next((s for s in showtimes if s['showtime_id'] == booking_detail['showtime_id']), None)
    movie_title = ''
    if showtime:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        if movie:
            movie_title = movie['title']

    # Construct booking_detail dict for template
    booking_detail_data = {
        'booking_id': booking_detail['booking_id'],
        'showtime_id': booking_detail['showtime_id'],
        'movie_title': movie_title,
        'customer_name': booking_detail['customer_name'],
        'customer_email': booking_detail['customer_email'],
        'booking_date': booking_detail['booking_date'],
        'total_price': booking_detail['total_price'],
        'status': booking_detail['status'],
        'seats_booked': booking_detail['seats_booked']
    }

    return render_template('booking_details.html', booking_detail=booking_detail_data)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter', '').strip().lower()
    filtered_theaters = theaters
    if location_filter:
        filtered_theaters = [t for t in theaters if t['location'].lower() == location_filter]

    return render_template('theater_information.html', theaters=filtered_theaters)


if __name__ == '__main__':
    app.run()
