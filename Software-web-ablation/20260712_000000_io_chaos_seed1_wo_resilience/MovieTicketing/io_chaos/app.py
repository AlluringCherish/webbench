from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Data file paths
MOVIES_FILE = 'data/movies.txt'
THEATERS_FILE = 'data/theaters.txt'
SHOWTIMES_FILE = 'data/showtimes.txt'
SEATS_FILE = 'data/seats.txt'
BOOKINGS_FILE = 'data/bookings.txt'
GENRES_FILE = 'data/genres.txt'


# Utility functions for loading data

def load_movies():
    movies = []
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    return movies


def load_theaters():
    theaters = []
    if os.path.exists(THEATERS_FILE):
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    return theaters


def load_showtimes():
    showtimes = []
    if os.path.exists(SHOWTIMES_FILE):
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        try:
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
                        except ValueError:
                            continue
    return showtimes


def load_seats():
    seats = []
    if os.path.exists(SEATS_FILE):
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 7:
                        try:
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
                        except ValueError:
                            continue
    return seats


def load_bookings():
    bookings = []
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 8:
                        try:
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
                        except ValueError:
                            continue
    return bookings


def load_genres():
    genres = []
    if os.path.exists(GENRES_FILE):
        with open(GENRES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        try:
                            genre = {
                                'genre_id': int(parts[0]),
                                'genre_name': parts[1]
                            }
                            genres.append(genre)
                        except ValueError:
                            continue
    return genres


# Save data functions

def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for booking in bookings:
                seats_str = ','.join(booking['seats_booked'])
                line = f"{booking['booking_id']}|{booking['showtime_id']}|{booking['customer_name']}|{booking['customer_email']}|{booking['booking_date']}|{booking['total_price']}|{booking['status']}|{seats_str}\n"
                f.write(line)
        return True
    except Exception:
        return False


def save_seats(seats):
    try:
        with open(SEATS_FILE, 'w', encoding='utf-8') as f:
            for seat in seats:
                line = f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Featured movies: Let's pick top 5 by rating descending
    featured = sorted(movies, key=lambda m: m['rating'], reverse=True)[:5]
    # We only need movie_id, title, genre, rating, duration for featured_movies context
    featured_movies = [{
        'movie_id': fm['movie_id'],
        'title': fm['title'],
        'genre': fm['genre'],
        'rating': fm['rating'],
        'duration': fm['duration']
    } for fm in featured]
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    # movies context needs movie_id, title, genre, rating, duration
    movies_context = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'genre': m['genre'],
        'rating': m['rating'],
        'duration': m['duration']
    } for m in movies]
    genres_context = genres  # genre_id, genre_name
    return render_template('catalog.html', movies=movies_context, genres=genres_context)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    showtimes = load_showtimes()
    theaters = load_theaters()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    # showtimes for this movie
    movie_showtimes = []
    for st in showtimes:
        if st['movie_id'] == movie_id:
            theater_name = next((t['theater_name'] for t in theaters if t['theater_id'] == st['theater_id']), '')
            movie_showtimes.append({
                'showtime_id': st['showtime_id'],
                'theater_name': theater_name,
                'showtime_date': st['showtime_date'],
                'showtime_time': st['showtime_time'],
                'price': st['price']
            })

    return render_template('movie_details.html', movie=movie, showtimes=movie_showtimes)


@app.route('/showtimes/select/<int:movie_id>')
def select_showtime(movie_id):
    showtimes_all = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()

    selected_movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not selected_movie:
        return "Movie not found", 404

    # Filter showtimes for movie
    showtimes_filtered = []
    for st in showtimes_all:
        if st['movie_id'] == movie_id:
            showtimes_filtered.append({
                'showtime_id': st['showtime_id'],
                'theater_id': st['theater_id'],
                'showtime_date': st['showtime_date'],
                'showtime_time': st['showtime_time'],
                'price': st['price'],
                'available_seats': st['available_seats']
            })

    theaters_context = [{
        'theater_id': t['theater_id'],
        'theater_name': t['theater_name']
    } for t in theaters]

    selected_movie_context = {
        'movie_id': selected_movie['movie_id'],
        'title': selected_movie['title']
    }

    return render_template('showtime_selection.html', showtimes=showtimes_filtered, theaters=theaters_context, selected_movie=selected_movie_context)


@app.route('/showtimes/select/<int:showtime_id>/seats')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    seats = load_seats()

    selected_showtime = next((st for st in showtimes if st['showtime_id'] == showtime_id), None)
    if not selected_showtime:
        return "Showtime not found", 404

    selected_theater = next((t for t in theaters if t['theater_id'] == selected_showtime['theater_id']), None)
    if not selected_theater:
        return "Theater not found", 404

    # We assume screen_id=1 for now since schema has screen_id in seats but showtimes.txt doesn't specify screen
    # To be consistent, filter seats by theater_id and screen_id=1
    seats_map = []
    for seat in seats:
        if seat['theater_id'] == selected_theater['theater_id'] and seat['screen_id'] == 1:
            seats_map.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })

    selected_showtime_context = {
        'showtime_id': selected_showtime['showtime_id'],
        'movie_id': selected_showtime['movie_id'],
        'theater_id': selected_showtime['theater_id'],
        'showtime_date': selected_showtime['showtime_date'],
        'showtime_time': selected_showtime['showtime_time'],
        'price': selected_showtime['price']
    }

    selected_theater_context = {
        'theater_id': selected_theater['theater_id'],
        'theater_name': selected_theater['theater_name'],
        'location': selected_theater['location'],
        'city': selected_theater['city'],
        'screens': selected_theater['screens'],
        'facilities': selected_theater['facilities']
    }

    return render_template('seat_selection.html', seats_map=seats_map, selected_showtime=selected_showtime_context, selected_theater=selected_theater_context)


@app.route('/booking/confirm', methods=['GET', 'POST'])
def booking_confirmation():
    if request.method == 'GET':
        # Expect query parameters: movie_title, showtime_date, showtime_time, theater_name, seats_selected (comma-separated), total_price
        movie_title = request.args.get('movie_title', '')
        showtime_date = request.args.get('showtime_date', '')
        showtime_time = request.args.get('showtime_time', '')
        theater_name = request.args.get('theater_name', '')
        seats_selected_raw = request.args.get('seats_selected', '')
        total_price_raw = request.args.get('total_price', '0')

        seats_selected = [s.strip() for s in seats_selected_raw.split(',') if s.strip()] if seats_selected_raw else []
        try:
            total_price = float(total_price_raw)
        except ValueError:
            total_price = 0.0

        booking_details = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats_selected': seats_selected,
            'total_price': total_price
        }

        return render_template('booking_confirmation.html', booking_details=booking_details)
    else:
        # POST: form data for booking
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        movie_title = request.form.get('movie_title', '').strip()
        showtime_date = request.form.get('showtime_date', '').strip()
        showtime_time = request.form.get('showtime_time', '').strip()
        theater_name = request.form.get('theater_name', '').strip()
        seats_selected_raw = request.form.get('seats_selected', '')
        try:
            total_price = float(request.form.get('total_price', '0'))
        except ValueError:
            total_price = 0.0

        seats_selected = [s.strip() for s in seats_selected_raw.split(',') if s.strip()] if seats_selected_raw else []

        # Validation
        error_msg = None
        if not customer_name or not customer_email or not seats_selected or total_price <= 0:
            error_msg = 'Please fill in all required booking information correctly.'

        if error_msg:
            return render_template('booking_confirmation.html', success=False, error_msg=error_msg)

        # Load bookings to determine new booking_id
        bookings = load_bookings()
        next_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

        # Map movie_title + showtime_date + showtime_time + theater_name to a showtime_id
        showtimes = load_showtimes()
        theaters = load_theaters()

        # Find the matching theater_id by theater_name
        theater_obj = next((t for t in theaters if t['theater_name'] == theater_name), None)
        if not theater_obj:
            error_msg = 'Theater not found.'
            return render_template('booking_confirmation.html', success=False, error_msg=error_msg)

        # Find showtime_id by matching showtime_date, showtime_time, theater_id
        showtime_obj = None
        for st in showtimes:
            if st['showtime_date'] == showtime_date and st['showtime_time'] == showtime_time and st['theater_id'] == theater_obj['theater_id']:
                showtime_obj = st
                break
        if not showtime_obj:
            error_msg = 'Showtime not found.'
            return render_template('booking_confirmation.html', success=False, error_msg=error_msg)

        # Check seat availability and update seat status
        seats = load_seats()

        # Get seat_ids for seats_selected in the theater and screen_id=1
        selected_seat_ids = []
        for seat in seats:
            seat_label = seat['row'] + str(seat['column'])
            if seat_label in seats_selected and seat['theater_id'] == theater_obj['theater_id'] and seat['screen_id'] == 1:
                selected_seat_ids.append(seat['seat_id'])

        # Make sure all requested seats are available
        unavailable_seats = []
        for seat in seats:
            if seat['seat_id'] in selected_seat_ids:
                if seat['status'].lower() != 'available':
                    unavailable_seats.append(seat['row'] + str(seat['column']))

        if unavailable_seats:
            error_msg = 'Some selected seats are no longer available: ' + ', '.join(unavailable_seats)
            return render_template('booking_confirmation.html', success=False, error_msg=error_msg)

        # Update seats to booked
        for seat in seats:
            if seat['seat_id'] in selected_seat_ids:
                seat['status'] = 'Booked'

        save_seats(seats)

        # Add booking entry
        from datetime import datetime
        booking_date = datetime.now().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': next_booking_id,
            'showtime_id': showtime_obj['showtime_id'],
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected
        }

        bookings.append(new_booking)
        save_bookings(bookings)

        return render_template('booking_confirmation.html', success=True, error_msg=None)


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()

    # Map bookings fields: booking_id, movie_title, booking_date, seats_booked (str), status
    bookings_context = []
    for b in bookings:
        movie = next((m for m in movies if m['movie_id'] == load_showtimes()[[st['showtime_id'] for st in load_showtimes()].index(b['showtime_id'])]['movie_id']), None)
        movie_title = movie['title'] if movie else 'Unknown'
        seats_str = ','.join(b['seats_booked']) if b['seats_booked'] else ''
        bookings_context.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': seats_str,
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings_context)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    movies = load_movies()
    showtimes = load_showtimes()
    theaters = load_theaters()

    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtime = next((st for st in showtimes if st['showtime_id'] == booking['showtime_id']), None)
    if not showtime:
        return "Showtime not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404

    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    # For showtime context theater_name
    showtime_context = {
        'showtime_id': showtime['showtime_id'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'theater_name': theater['theater_name'] if theater else ''
    }

    # booking fields: booking_id, customer_name, customer_email, booking_date, total_price, status, seats_booked (list of str)
    booking_context = booking

    movie_context = {
        'movie_id': movie['movie_id'],
        'title': movie['title']
    }

    return render_template('booking_details.html', booking=booking_context, movie=movie_context, showtime=showtime_context)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    return render_template('theater_information.html', theaters=theaters)


if __name__ == '__main__':
    app.run()
