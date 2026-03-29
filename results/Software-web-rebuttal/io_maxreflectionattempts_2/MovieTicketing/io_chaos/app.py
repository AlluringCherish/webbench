from flask import Flask, render_template, redirect, url_for, request, session
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
MOVIES_FILE = 'data/movies.txt'
THEATERS_FILE = 'data/theaters.txt'
SHOWTIMES_FILE = 'data/showtimes.txt'
SEATS_FILE = 'data/seats.txt'
BOOKINGS_FILE = 'data/bookings.txt'
GENRES_FILE = 'data/genres.txt'


# Utility functions for data loading and saving

def load_movies():
    movies = []
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        pass
    return movies


def load_theaters():
    theaters = []
    try:
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        pass
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        pass
    return showtimes


def load_seats():
    seats = []
    try:
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        pass
    return seats


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
        pass
    return bookings


def load_genres():
    genres = []
    try:
        with open(GENRES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    except Exception:
        pass
    return genres


def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{b['seats_booked']}\n"
                f.write(line)
    except Exception:
        pass


# Flask route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Featured movies: Let's say top 3 by rating
    featured = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    featured_movies = [{'movie_id': m['movie_id'], 'title': m['title'], 'rating': m['rating']} for m in featured]
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    # transform genres to only genre_name field
    genres_simple = [{'genre_name': g['genre_name']} for g in genres]
    # The specification does not require filtering/searching in backend, just pass all
    # But frontend can use search-input and genre-filter
    movies_simple = [{'movie_id': m['movie_id'], 'title': m['title'], 'genre': m['genre'], 'rating': m['rating'], 'duration': m['duration']} for m in movies]
    return render_template('movie_catalog.html', movies=movies_simple, genres=genres_simple)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        # 404 not found could be handled, but spec doesn't mention it
        return redirect(url_for('movie_catalog'))
    return render_template('movie_details.html', movie=movie)


@app.route('/movies/<int:movie_id>/showtimes')
def select_showtime(movie_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes_all = load_showtimes()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        return redirect(url_for('movie_catalog'))

    # Get filter params from query string
    selected_theater_filter = request.args.get('theater', '')
    selected_date_filter = request.args.get('date', '')

    # Filter showtimes by movie_id
    showtimes = [st for st in showtimes_all if st['movie_id'] == movie_id]

    # Filter by theater name if filter present
    if selected_theater_filter:
        theater_ids = [t['theater_id'] for t in theaters if t['theater_name'] == selected_theater_filter]
        showtimes = [st for st in showtimes if st['theater_id'] in theater_ids]

    # Filter by date if filter present
    if selected_date_filter:
        showtimes = [st for st in showtimes if st['showtime_date'] == selected_date_filter]

    # Add theater_name field to each showtime
    theater_map = {t['theater_id']: t['theater_name'] for t in theaters}
    for st in showtimes:
        st['theater_name'] = theater_map.get(st['theater_id'], '')

    return render_template('select_showtime.html', movie=movie, showtimes=showtimes, theaters=theaters,
                           selected_theater_filter=selected_theater_filter, selected_date_filter=selected_date_filter)


@app.route('/showtimes/<int:showtime_id>/seats', methods=['GET'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    seats = load_seats()
    movies = load_movies()

    # Find showtime
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return redirect(url_for('dashboard'))

    # Find movie
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if movie is None:
        return redirect(url_for('dashboard'))

    # Find theater
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if theater is None:
        return redirect(url_for('dashboard'))

    # Filter seats by theater_id and screen_id=1 (screen_id is not in showtime or theater schema, assume screen_id=1 for all seats)
    # Specification doesn't mention screen selection, we assume screen_id=1 for simplicity
    relevant_seats = [seat for seat in seats if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == 1]

    # Mark seat_id to seat identity mapping for returning seat identifiers (row + column)
    seats_out = []
    for seat in relevant_seats:
        seat_dict = {
            'seat_id': seat['seat_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat['status']
        }
        seats_out.append(seat_dict)

    selected_seats = []
    if 'selected_seats' in session:
        selected_seats = session['selected_seats']

    showtime_out = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'],
        'theater_name': theater['theater_name'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'price': showtime['price']
    }

    return render_template('seat_selection.html', showtime=showtime_out, seats=seats_out, selected_seats=selected_seats)


@app.route('/showtimes/<int:showtime_id>/seats', methods=['POST'])
def submit_seat_selection(showtime_id):
    selected_seats = request.form.getlist('selected_seats')
    # Save selection in session
    session['selected_seats'] = selected_seats
    session['selected_showtime_id'] = showtime_id
    return redirect(url_for('booking_confirmation_get'))


@app.route('/booking/confirm', methods=['GET'])
def booking_confirmation_get():
    if 'selected_showtime_id' not in session or 'selected_seats' not in session:
        return redirect(url_for('dashboard'))

    showtime_id = session['selected_showtime_id']
    selected_seats = session['selected_seats']

    showtimes = load_showtimes()
    movies = load_movies()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return redirect(url_for('dashboard'))

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if movie is None:
        return redirect(url_for('dashboard'))

    total_price = showtime['price'] * len(selected_seats)

    booking_details = {
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'seats': selected_seats,
        'total_price': total_price
    }

    return render_template('booking_confirmation.html', booking_details=booking_details)


@app.route('/booking/confirm', methods=['POST'])
def booking_confirmation_post():
    if 'selected_showtime_id' not in session or 'selected_seats' not in session:
        return redirect(url_for('dashboard'))

    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    selected_seats = session.get('selected_seats', [])
    showtime_id = session.get('selected_showtime_id')

    if not customer_name or not customer_email or not selected_seats or showtime_id is None:
        # Basic validation fail, redirect back
        return redirect(url_for('booking_confirmation_get'))

    bookings = load_bookings()
    showtimes = load_showtimes()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return redirect(url_for('dashboard'))

    # Calculate total price
    total_price = showtime['price'] * len(selected_seats)

    # Create new booking ID
    if bookings:
        new_booking_id = max(b['booking_id'] for b in bookings) + 1
    else:
        new_booking_id = 1

    booking_date = datetime.date.today().isoformat()

    seats_booked_str = ','.join(selected_seats)

    # Add new booking
    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats_booked_str
    }

    bookings.append(new_booking)

    # Save bookings
    save_bookings(bookings)

    # Clear session selections
    session.pop('selected_seats', None)
    session.pop('selected_showtime_id', None)

    return redirect(url_for('booking_history'))


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()

    status_filter = request.args.get('status_filter', '')

    # Enhance bookings with movie titles and convert seats_booked to list
    bookings_out = []
    for b in bookings:
        movie = next((m for m in movies if m['movie_id'] == next((s['movie_id'] for s in load_showtimes() if s['showtime_id'] == b['showtime_id']), None)), None)
        if movie is None:
            continue
        if status_filter and b['status'] != status_filter:
            continue
        booking_dict = {
            'booking_id': b['booking_id'],
            'movie_title': movie['title'],
            'showtime_date': next((s['showtime_date'] for s in load_showtimes() if s['showtime_id'] == b['showtime_id']), ''),
            'seats': b['seats_booked'].split(',') if b['seats_booked'] else [],
            'status': b['status']
        }
        bookings_out.append(booking_dict)

    return render_template('booking_history.html', bookings=bookings_out, status_filter=status_filter)


@app.route('/bookings/<int:booking_id>')
def view_booking(booking_id):
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking is None:
        return redirect(url_for('booking_history'))

    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    if showtime is None:
        return redirect(url_for('booking_history'))

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if movie is None:
        return redirect(url_for('booking_history'))

    booking_out = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'seats': booking['seats_booked'].split(',') if booking['seats_booked'] else [],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price'],
        'status': booking['status']
    }

    return render_template('booking_details.html', booking=booking_out)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter', '')
    theaters_out = theaters
    if location_filter:
        theaters_out = [t for t in theaters if t['location'] == location_filter]
    return render_template('theater_information.html', theaters=theaters_out, location_filter=location_filter)


if __name__ == '__main__':
    app.run()
