from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'some_secret_key'

DATA_DIR = 'data'

# Utility functions for loading data

def load_movies():
    movies = []
    filepath = os.path.join(DATA_DIR, 'movies.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
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
        # File not found or error, return empty
        pass
    return movies


def load_theaters():
    theaters = []
    filepath = os.path.join(DATA_DIR, 'theaters.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
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
        pass
    return theaters


def load_showtimes():
    showtimes = []
    filepath = os.path.join(DATA_DIR, 'showtimes.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
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
        pass
    return showtimes


def load_seats():
    seats = []
    filepath = os.path.join(DATA_DIR, 'seats.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
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
        pass
    return seats


def load_bookings():
    bookings = []
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    seats_booked_list = parts[7].split(',') if parts[7] else []
                    booking = {
                        'booking_id': int(parts[0]),
                        'showtime_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'booking_date': parts[4],
                        'total_price': float(parts[5]),
                        'status': parts[6],
                        'seats_booked': seats_booked_list
                    }
                    bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_genres():
    genres = []
    filepath = os.path.join(DATA_DIR, 'genres.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) ==3:
                    genre = {
                        'genre_id': int(parts[0]),
                        'genre_name': parts[1],
                        'description': parts[2]
                    }
                    genres.append(genre)
    except Exception:
        pass
    return genres

# Utility function to save bookings back to file

def save_bookings(bookings):
    filepath = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    str(b['booking_id']),
                    str(b['showtime_id']),
                    b['customer_name'],
                    b['customer_email'],
                    b['booking_date'],
                    f"{b['total_price']:.2f}",
                    b['status'],
                    ','.join(b['seats_booked'])
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# --- Route Implementations ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    movies = load_movies()
    # Featured movies: top 5 movies by rating
    sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)
    featured_movies = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'genre': m['genre'],
        'rating': m['rating']
    } for m in sorted_movies[:5]]

    # Upcoming releases: movies with release_date >= today sorted by release_date ascending
    today_str = datetime.today().strftime('%Y-%m-%d')
    upcoming = [m for m in movies if m['release_date'] >= today_str]
    upcoming_releases_sorted = sorted(upcoming, key=lambda x: x['release_date'])
    upcoming_releases = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'release_date': m['release_date']
    } for m in upcoming_releases_sorted]

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    movies_list = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'genre': m['genre'],
        'rating': m['rating'],
        'duration': m['duration']
    } for m in movies]
    return render_template('movie_catalog.html', movies=movies_list)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = None
    for m in movies:
        if m['movie_id'] == movie_id:
            movie = m
            break
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


@app.route('/movies/<int:movie_id>/showtimes')
def showtime_selection(movie_id):
    showtimes_all = load_showtimes()
    theaters_all = load_theaters()

    # Filter showtimes for this movie
    showtimes_filtered = [s for s in showtimes_all if s['movie_id'] == movie_id]

    # Build theaters dictionary for quick name lookup
    theaters_dict = {t['theater_id']: t for t in theaters_all}

    # Construct showtimes list with theater_name field
    showtimes = []
    for s in showtimes_filtered:
        theater = theaters_dict.get(s['theater_id'], {'theater_name': 'Unknown'})
        showtimes.append({
            'showtime_id': s['showtime_id'],
            'theater_id': s['theater_id'],
            'theater_name': theater['theater_name'],
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        })

    theaters = [{'theater_id': t['theater_id'], 'theater_name': t['theater_name']} for t in theaters_all]

    return render_template('showtime_selection.html', showtimes=showtimes, theaters=theaters)


@app.route('/showtimes/<int:showtime_id>/seats')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if not showtime:
        return "Showtime not found", 404

    theaters = load_theaters()
    theater = None
    for t in theaters:
        if t['theater_id'] == showtime['theater_id']:
            theater = t
            break
    if not theater:
        return "Theater not found", 404

    seats_all = load_seats()
    # Filter seats for this theater
    seats_filtered = [seat for seat in seats_all if seat['theater_id'] == theater['theater_id']]

    # We create seat_map as list of seat dicts as specified
    seat_map = []
    for seat in seats_filtered:
        seat_map.append({
            'seat_id': seat['seat_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat['status']
        })

    selected_seats = []  # Initially empty

    return render_template('seat_selection.html', seat_map=seat_map, selected_seats=selected_seats)


@app.route('/bookings/confirm', methods=['GET', 'POST'])
def booking_confirmation():
    error_message = None

    if request.method == 'GET':
        # To display booking confirmation, expect parameters in query string indicating previous selections
        movie_title = request.args.get('movie_title', '')
        showtime_date = request.args.get('showtime_date', '')
        showtime_time = request.args.get('showtime_time', '')
        theater_name = request.args.get('theater_name', '')
        seats_selected = request.args.get('seats_selected', '')  # comma separated

        seats_selected_list = seats_selected.split(',') if seats_selected else []

        total_price = 0.0
        # Try to estimate total price if possible by looking up showtime price
        # But since query doesn't have showtime_id, we skip for GET

        booking_summary = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats_selected': seats_selected_list,
            'total_price': total_price
        }

        return render_template('booking_confirmation.html', booking_summary=booking_summary, error_message=None)

    # POST method: receive form submission with booking details
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    movie_title = request.form.get('movie_title', '').strip()
    showtime_date = request.form.get('showtime_date', '').strip()
    showtime_time = request.form.get('showtime_time', '').strip()
    theater_name = request.form.get('theater_name', '').strip()
    seats_selected = request.form.get('seats_selected', '').strip()  # comma separated seat IDs

    if not customer_name or not customer_email or not seats_selected:
        error_message = 'Please provide your name, email, and select at least one seat.'
        booking_summary = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats_selected': seats_selected.split(',') if seats_selected else [],
            'total_price': 0.0
        }
        return render_template('booking_confirmation.html', booking_summary=booking_summary, error_message=error_message)

    seats_selected_list = seats_selected.split(',')

    # Find showtime to get price
    showtimes = load_showtimes()
    showtime_obj = None
    for s in showtimes:
        if s['showtime_date'] == showtime_date and s['showtime_time'] == showtime_time and theater_name and s['price'] >= 0:
            # This is a bit uncertain since no showtime_id provided in POST. We search by date/time & theater_name
            theaters = load_theaters()
            theater_ids = [t['theater_id'] for t in theaters if t['theater_name'] == theater_name]
            if s['theater_id'] in theater_ids:
                showtime_obj = s
                break
    
    if not showtime_obj:
        error_message = 'Showtime not found. Cannot confirm booking.'
        booking_summary = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats_selected': seats_selected_list,
            'total_price': 0.0
        }
        return render_template('booking_confirmation.html', booking_summary=booking_summary, error_message=error_message)

    # Calculate total price
    total_price = showtime_obj['price'] * len(seats_selected_list)

    # Load bookings
    bookings = load_bookings()
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1
    booking_date = datetime.today().strftime('%Y-%m-%d')

    # Create new booking record
    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_obj['showtime_id'],
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats_selected_list
    }

    bookings.append(new_booking)
    saved = save_bookings(bookings)

    booking_summary = {
        'movie_title': movie_title,
        'showtime_date': showtime_date,
        'showtime_time': showtime_time,
        'theater_name': theater_name,
        'seats_selected': seats_selected_list,
        'total_price': total_price
    }

    if not saved:
        error_message = 'Failed to save booking. Please try again.'

    return render_template('booking_confirmation.html', booking_summary=booking_summary, error_message=error_message)


@app.route('/bookings/history')
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    # Build lookup dicts
    showtime_dict = {s['showtime_id']: s for s in showtimes}
    movie_dict = {m['movie_id']: m for m in movies}

    bookings_list = []
    for b in bookings:
        s = showtime_dict.get(b['showtime_id'])
        if not s:
            continue
        movie = movie_dict.get(s['movie_id'])
        movie_title = movie['title'] if movie else 'Unknown'

        bookings_list.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings_list)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        return "Booking not found", 404

    showtimes = load_showtimes()
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == booking['showtime_id']:
            showtime = s
            break
    if not showtime:
        return "Showtime not found", 404

    movies = load_movies()
    movie = None
    for m in movies:
        if m['movie_id'] == showtime['movie_id']:
            movie = m
            break
    if not movie:
        return "Movie not found", 404

    theaters = load_theaters()
    theater = None
    for t in theaters:
        if t['theater_id'] == showtime['theater_id']:
            theater = t
            break
    if not theater:
        return "Theater not found", 404

    booking_detail = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'theater_name': theater['theater_name'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'seats_booked': booking['seats_booked'],
        'status': booking['status']
    }

    return render_template('booking_details.html', booking=booking_detail)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    return render_template('theater_information.html', theaters=theaters)


if __name__ == '__main__':
    app.run()