from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Data file paths
MOVIES_FILE = "data/movies.txt"
THEATERS_FILE = "data/theaters.txt"
SHOWTIMES_FILE = "data/showtimes.txt"
SEATS_FILE = "data/seats.txt"
BOOKINGS_FILE = "data/bookings.txt"
GENRES_FILE = "data/genres.txt"

# Helper functions to load and save data with error handling

def load_movies():
    movies = []
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    except Exception:
        movies = []
    return movies


def load_theaters():
    theaters = []
    try:
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                theater = {
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': int(parts[4]),
                    'facilities': parts[5]
                }
                theaters.append(theater)
    except Exception:
        theaters = []
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
    except Exception:
        showtimes = []
    return showtimes


def load_seats():
    seats = []
    try:
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
    except Exception:
        seats = []
    return seats


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': parts[7]
                }
                bookings.append(booking)
    except Exception:
        bookings = []
    return bookings


def load_genres():
    genres = []
    try:
        with open(GENRES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genres.append(parts[1])
    except Exception:
        genres = []
    return genres


def save_seats(seats):
    try:
        with open(SEATS_FILE, 'w', encoding='utf-8') as f:
            for seat in seats:
                line = f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for booking in bookings:
                line = f"{booking['booking_id']}|{booking['showtime_id']}|{booking['customer_name']}|{booking['customer_email']}|{booking['booking_date']}|{booking['total_price']}|{booking['status']}|{booking['seats_booked']}\n"
                f.write(line)
        return True
    except Exception:
        return False


# Helper functions for lookups

def get_movie_by_id(movie_id):
    movies = load_movies()
    for movie in movies:
        if movie['movie_id'] == movie_id:
            return movie
    return None


def get_theater_by_id(theater_id):
    theaters = load_theaters()
    for theater in theaters:
        if theater['theater_id'] == theater_id:
            return theater
    return None


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()

    # featured_movies: top 5 rated movies
    featured_movies_sorted = sorted(movies, key=lambda m: m['rating'], reverse=True)[:5]
    featured_movies = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'rating': m['rating'],
        'duration': m['duration']
    } for m in featured_movies_sorted]

    # upcoming_releases: movies with release_date >= today, sorted ascending
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming = [m for m in movies if m['release_date'] >= today_str]
    upcoming_sorted = sorted(upcoming, key=lambda m: m['release_date'])
    upcoming_releases = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'release_date': m['release_date']
    } for m in upcoming_sorted]

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    movies_list = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'genre': m['genre'],
        'rating': m['rating'],
        'duration': m['duration']
    } for m in movies]

    return render_template('catalog.html', movies=movies_list, genres=genres)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if movie is None:
        return render_template('movie_details.html', movie=None)

    movie_context = {
        'movie_id': movie['movie_id'],
        'title': movie['title'],
        'director': movie['director'],
        'rating': movie['rating'],
        'description': movie['description']
    }
    return render_template('movie_details.html', movie=movie_context)


@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()

    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]

    showtimes_list = []
    theater_names_set = set()
    for s in filtered_showtimes:
        theater = get_theater_by_id(s['theater_id'])
        if theater is None:
            continue
        theater_names_set.add(theater['theater_name'])
        showtimes_list.append({
            'showtime_id': s['showtime_id'],
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'theater_name': theater['theater_name'],
            'price': s['price']
        })

    theaters_list = sorted(theater_names_set)

    return render_template('showtimes.html', showtimes=showtimes_list, theaters=theaters_list)


@app.route('/seat-selection/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if showtime is None:
        return render_template('seat_selection.html', seat_map=[], selected_showtime=None)

    movie = get_movie_by_id(showtime['movie_id'])
    theater = get_theater_by_id(showtime['theater_id'])
    if movie is None or theater is None:
        return render_template('seat_selection.html', seat_map=[], selected_showtime=None)

    seats = load_seats()
    seat_map = []
    for seat in seats:
        if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == 1:
            seat_map.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })

    selected_showtime = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'],
        'theater_name': theater['theater_name'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time']
    }

    return render_template('seat_selection.html', seat_map=seat_map, selected_showtime=selected_showtime)


@app.route('/booking-confirmation', methods=['POST'])
def booking_confirmation():
    form = request.form
    customer_name = form.get('customer_name', '').strip()
    customer_email = form.get('customer_email', '').strip()
    showtime_id_str = form.get('showtime_id', '').strip()
    selected_seats_str = form.get('selected_seats', '').strip()

    error_message = None
    booking_summary = None

    if not customer_name or not customer_email or not showtime_id_str or not selected_seats_str:
        error_message = "Missing required booking information."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    try:
        showtime_id = int(showtime_id_str)
    except Exception:
        error_message = "Invalid showtime ID."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    selected_seats = [s.strip() for s in selected_seats_str.split(',') if s.strip()]
    if not selected_seats:
        error_message = "No seats selected."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if showtime is None:
        error_message = "Showtime not found."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    movie = get_movie_by_id(showtime['movie_id'])
    if movie is None:
        error_message = "Movie not found for showtime."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    seats = load_seats()
    seat_label_map = {}
    for seat in seats:
        if seat['theater_id'] == showtime['theater_id'] and seat['screen_id'] == 1:
            label = f"{seat['row']}{seat['column']}"
            seat_label_map[label] = seat

    for label in selected_seats:
        seat = seat_label_map.get(label)
        if seat is None or seat['status'] != 'Available':
            error_message = f"Seat {label} is not available."
            return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    total_price = len(selected_seats) * showtime['price']

    for label in selected_seats:
        seat_label_map[label]['status'] = 'Booked'

    if not save_seats(seats):
        error_message = "Failed to update seat bookings. Please try again."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    bookings = load_bookings()
    new_booking_id = 1
    if bookings:
        new_booking_id = max(b['booking_id'] for b in bookings) + 1

    booking_date = datetime.now().strftime('%Y-%m-%d')

    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': ','.join(selected_seats)
    }

    bookings.append(new_booking)

    if not save_bookings(bookings):
        error_message = "Failed to save booking. Please try again."
        return render_template('booking_confirmation.html', booking_summary=None, error_message=error_message)

    booking_summary = {
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'seats': selected_seats,
        'total_price': total_price
    }

    return render_template('booking_confirmation.html', booking_summary=booking_summary, error_message=None)


@app.route('/booking-history')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()
    movie_id_title_map = {m['movie_id']: m['title'] for m in movies}

    status_options = ["All", "Confirmed", "Cancelled", "Completed"]
    status_filter = request.args.get('status', 'All')

    filtered_bookings = []
    showtimes = load_showtimes()
    showtime_dict = {s['showtime_id']: s for s in showtimes}

    for b in bookings:
        if status_filter == "All" or b['status'] == status_filter:
            movie_title = "Unknown"
            showtime = showtime_dict.get(b['showtime_id'])
            if showtime:
                movie_title = movie_id_title_map.get(showtime['movie_id'], "Unknown")

            filtered_bookings.append({
                'booking_id': b['booking_id'],
                'movie_title': movie_title,
                'booking_date': b['booking_date'],
                'seats': b['seats_booked'],
                'status': b['status']
            })

    return render_template('bookings.html', bookings=filtered_bookings, status_options=status_options)


@app.route('/booking-history/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if booking is None:
        return render_template('booking_details.html', booking=None)

    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == booking['showtime_id']:
            showtime = s
            break

    movie_title = None
    if showtime:
        movie = get_movie_by_id(showtime['movie_id'])
        if movie:
            movie_title = movie['title']

    seats_list = [seat.strip() for seat in booking['seats_booked'].split(',') if seat.strip()]

    booking_context = {
        'booking_id': booking['booking_id'],
        'movie_title': movie_title,
        'showtime_date': showtime['showtime_date'] if showtime else None,
        'seats': seats_list,
        'status': booking['status'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price']
    }

    return render_template('booking_details.html', booking=booking_context)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    locations_set = set(t['location'] for t in theaters)
    locations = sorted(locations_set)
    return render_template('theater_information.html', theaters=theaters, locations=locations)


if __name__ == '__main__':
    app.run()
