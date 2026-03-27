from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_DIR = 'data'

# Helper functions for data loading and saving

def load_movies():
    movies = []
    try:
        with open(os.path.join(DATA_DIR, 'movies.txt'), 'r', encoding='utf-8') as f:
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
        movies = []
    return movies


def load_theaters():
    theaters = []
    try:
        with open(os.path.join(DATA_DIR, 'theaters.txt'), 'r', encoding='utf-8') as f:
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
        with open(os.path.join(DATA_DIR, 'showtimes.txt'), 'r', encoding='utf-8') as f:
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
        showtimes = []
    return showtimes


def load_seats():
    seats = []
    try:
        with open(os.path.join(DATA_DIR, 'seats.txt'), 'r', encoding='utf-8') as f:
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
        seats = []
    return seats


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
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
                    'seats_booked': parts[7].split(',') if parts[7] else []
                }
                bookings.append(booking)
    except Exception:
        bookings = []
    return bookings


def load_genres():
    genres = []
    try:
        with open(os.path.join(DATA_DIR, 'genres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genres.append(parts[1])
    except Exception:
        genres = []
    return genres


def save_bookings(bookings):
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats_booked']) if b['seats_booked'] else ''
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']:.2f}|{b['status']}|{seats_str}\n"
                f.write(line)
    except Exception:
        pass


def save_showtimes(showtimes):
    try:
        with open(os.path.join(DATA_DIR, 'showtimes.txt'), 'w', encoding='utf-8') as f:
            for st in showtimes:
                line = f"{st['showtime_id']}|{st['movie_id']}|{st['theater_id']}|{st['showtime_date']}|{st['showtime_time']}|{st['price']:.2f}|{st['available_seats']}\n"
                f.write(line)
    except Exception:
        pass


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    movies = load_movies()
    today = datetime.today().strftime('%Y-%m-%d')
    # featured_movies: top 5 by rating
    featured = sorted(movies, key=lambda x: x['rating'], reverse=True)[:5]
    featured_movies = [{'movie_id': m['movie_id'], 'title': m['title'], 'poster_url': ''} for m in featured]

    # upcoming_releases: release_date > today, sorted ascending
    upcoming = [m for m in movies if m['release_date'] > today]
    upcoming_sorted = sorted(upcoming, key=lambda x: x['release_date'])[:5]
    upcoming_releases = [{'movie_id': m['movie_id'], 'title': m['title'], 'poster_url': ''} for m in upcoming_sorted]

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    search_query = request.args.get('search_query', '').strip()
    selected_genre = request.args.get('selected_genre', '').strip()

    filtered = movies
    if search_query:
        sq = search_query.lower()
        filtered = [m for m in filtered if sq in m['title'].lower() or sq in m['genre'].lower()]
    if selected_genre:
        filtered = [m for m in filtered if m['genre'].lower() == selected_genre.lower()]

    movies_list = []
    for m in filtered:
        movies_list.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster_url': ''
        })

    return render_template('movie_catalog.html', movies=movies_list, genres=genres, search_query=search_query, selected_genre=selected_genre)


@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


@app.route('/movies/<int:movie_id>/showtimes', methods=['GET'])
def select_showtime(movie_id):
    movies = load_movies()
    showtimes = load_showtimes()
    theaters = load_theaters()

    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    selected_theater = request.args.get('selected_theater')
    selected_date = request.args.get('selected_date')

    try:
        selected_theater_int = int(selected_theater) if selected_theater else None
    except:
        selected_theater_int = None

    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if selected_theater_int is not None:
        filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] == selected_theater_int]
    if selected_date:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == selected_date]

    return render_template('select_showtime.html', movie=movie, showtimes=filtered_showtimes,
                           selected_theater=selected_theater_int, selected_date=selected_date, theaters=theaters)


@app.route('/movies/<int:movie_id>/showtimes/select/<int:showtime_id>', methods=['GET'])
def seat_selection(movie_id, showtime_id):
    showtimes = load_showtimes()
    seats = load_seats()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id and s['movie_id'] == movie_id), None)
    if not showtime:
        return "Showtime not found", 404

    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404

    # Assume screen_id = 1 (no screen selection in spec)
    screen_id = 1

    seats_map = [s for s in seats if s['theater_id'] == theater['theater_id'] and s['screen_id'] == screen_id]

    return render_template('seat_selection.html', showtime=showtime, seats_map=seats_map)


@app.route('/movies/<int:movie_id>/showtimes/select/<int:showtime_id>/booking', methods=['GET', 'POST'])
def booking_confirmation(movie_id, showtime_id):
    movies = load_movies()
    showtimes = load_showtimes()
    theaters = load_theaters()
    bookings = load_bookings()

    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id and s['movie_id'] == movie_id), None)
    if not showtime:
        return "Showtime not found", 404

    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404

    if request.method == 'GET':
        seats_selected_raw = request.args.get('seats_selected', '')
        seats_selected = seats_selected_raw.split(',') if seats_selected_raw else []

        total_price = len(seats_selected) * showtime['price'] if seats_selected else 0.0

        booking_details = {
            'movie_title': movie['title'],
            'showtime_date': showtime['showtime_date'],
            'showtime_time': showtime['showtime_time'],
            'theater_name': theater['theater_name'],
            'seats_selected': seats_selected,
            'total_price': total_price
        }
        return render_template('booking_confirmation.html', booking_details=booking_details)

    else:  # POST
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        seats_selected_raw = request.form.get('seats_selected', '')
        seats_selected = seats_selected_raw.split(',') if seats_selected_raw else []

        if not customer_name or not customer_email or not seats_selected:
            return "Missing booking information", 400

        # New booking ID
        max_id = max([b['booking_id'] for b in bookings], default=0)
        new_id = max_id + 1

        total_price = len(seats_selected) * showtime['price']
        booking_date = datetime.today().strftime('%Y-%m-%d')

        new_booking = {
            'booking_id': new_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected
        }

        bookings.append(new_booking)
        save_bookings(bookings)

        # Update available seats on showtime
        new_available_seats = max(0, showtime['available_seats'] - len(seats_selected))
        for st in showtimes:
            if st['showtime_id'] == showtime_id:
                st['available_seats'] = new_available_seats
        save_showtimes(showtimes)

        return redirect(url_for('booking_history'))


@app.route('/bookings', methods=['GET'])
def booking_history():
    bookings = load_bookings()
    status_filter = request.args.get('status_filter', '').strip()

    filtered = bookings
    if status_filter:
        filtered = [b for b in bookings if b['status'].lower() == status_filter.lower()]

    movies = load_movies()
    showtimes = load_showtimes()

    showtime_to_movie = {s['showtime_id']: s['movie_id'] for s in showtimes}
    movie_map = {m['movie_id']: m['title'] for m in movies}

    bookings_list = []
    for b in filtered:
        movie_title = movie_map.get(showtime_to_movie.get(b['showtime_id'], None), 'Unknown')
        bookings_list.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings_list, status_filter=status_filter)


@app.route('/bookings/<int:booking_id>', methods=['GET'])
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()

    showtime = next((st for st in showtimes if st['showtime_id'] == booking['showtime_id']), None)
    movie = None
    theater = None

    if showtime:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    booking_dict = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'] if movie else 'Unknown',
        'showtime_date': showtime['showtime_date'] if showtime else 'Unknown',
        'showtime_time': showtime['showtime_time'] if showtime else 'Unknown',
        'theater_name': theater['theater_name'] if theater else 'Unknown',
        'seats_booked': booking['seats_booked'],
        'total_price': booking['total_price'],
        'status': booking['status'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email']
    }

    return render_template('booking_details.html', booking=booking_dict)


@app.route('/theaters', methods=['GET'])
def theater_information():
    theaters = load_theaters()
    selected_location = request.args.get('selected_location', '').strip()

    if selected_location:
        filtered = [t for t in theaters if t['location'].lower() == selected_location.lower()]
    else:
        filtered = theaters

    return render_template('theater_information.html', theaters=filtered, selected_location=selected_location)


if __name__ == '__main__':
    app.run()
