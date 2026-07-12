from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.secret_key = 'hardcoded_secret_key'

DATA_DIR = 'data'

# Data file paths
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.txt')
THEATERS_FILE = os.path.join(DATA_DIR, 'theaters.txt')
SHOWTIMES_FILE = os.path.join(DATA_DIR, 'showtimes.txt')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.txt')
GENRES_FILE = os.path.join(DATA_DIR, 'genres.txt')
SEATS_FILE = os.path.join(DATA_DIR, 'seats.txt')

# Data structure notes based on spec (Section 3):
# movies.txt columns: movie_id|title|director|genre|rating|duration|description|release_date|poster
# theaters.txt columns: theater_id|theater_name|location|city|screens|facilities
# showtimes.txt columns: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
# bookings.txt columns: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
# genres.txt columns: genre_id|genre_name|description
# seats.txt columns: seat_id|theater_id|screen_id|row|column|seat_type|status


def read_pipe_delimited_file(file_path, expected_fields):
    """Generic loader for pipe-delimited files with no header."""
    records = []
    if not os.path.exists(file_path):
        # Gracefully handle missing file
        return records
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != expected_fields:
                    # skip malformed lines
                    continue
                records.append(parts)
    except Exception:
        # Handle read error gracefully
        return []
    return records


def write_pipe_delimited_file(file_path, list_of_lists):
    """Write list of lists to pipe-delimited file without header."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for record in list_of_lists:
                line = '|'.join(str(x) for x in record)
                f.write(line + '\n')
        return True
    except Exception:
        return False


# Load data helpers

def load_movies():
    # movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str, poster:str
    movies_raw = read_pipe_delimited_file(MOVIES_FILE, 9)
    movies = []
    for row in movies_raw:
        try:
            movie = {
                'movie_id': int(row[0]),
                'title': row[1],
                'director': row[2],
                'genre': row[3],
                'rating': float(row[4]),
                'duration': int(row[5]),
                'description': row[6],
                'release_date': row[7],
                'poster': row[8]
            }
            movies.append(movie)
        except Exception:
            continue
    return movies


def load_theaters():
    # theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str
    theaters_raw = read_pipe_delimited_file(THEATERS_FILE, 6)
    theaters = []
    for row in theaters_raw:
        try:
            theater = {
                'theater_id': int(row[0]),
                'theater_name': row[1],
                'location': row[2],
                'city': row[3],
                'screens': int(row[4]),
                'facilities': row[5]
            }
            theaters.append(theater)
        except Exception:
            continue
    return theaters


def load_showtimes():
    # showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float, available_seats:int
    showtimes_raw = read_pipe_delimited_file(SHOWTIMES_FILE, 7)
    showtimes = []
    for row in showtimes_raw:
        try:
            showtime = {
                'showtime_id': int(row[0]),
                'movie_id': int(row[1]),
                'theater_id': int(row[2]),
                'showtime_date': row[3],
                'showtime_time': row[4],
                'price': float(row[5]),
                'available_seats': int(row[6])
            }
            showtimes.append(showtime)
        except Exception:
            continue
    return showtimes


def load_bookings():
    # booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked
    bookings_raw = read_pipe_delimited_file(BOOKINGS_FILE, 8)
    bookings = []
    for row in bookings_raw:
        try:
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
        except Exception:
            continue
    return bookings


def load_genres():
    # genre_id|genre_name|description
    genres_raw = read_pipe_delimited_file(GENRES_FILE, 3)
    genres = []
    for row in genres_raw:
        try:
            genre = {
                'genre_id': int(row[0]),
                'genre_name': row[1],
                'description': row[2]
            }
            genres.append(genre)
        except Exception:
            continue
    return genres


def load_seats():
    # seat_id|theater_id|screen_id|row|column|seat_type|status
    seats_raw = read_pipe_delimited_file(SEATS_FILE, 7)
    seats = []
    for row in seats_raw:
        try:
            seat = {
                'seat_id': int(row[0]),
                'theater_id': int(row[1]),
                'screen_id': int(row[2]),
                'row': row[3],
                'column': row[4],
                'seat_type': row[5],
                'status': row[6]
            }
            seats.append(seat)
        except Exception:
            continue
    return seats


def save_bookings(bookings):
    # bookings: list of booking dicts
    bookings_list = []
    for b in bookings:
        seats_booked_str = ','.join(b['seats_booked']) if b['seats_booked'] else ''
        record = [
            str(b['booking_id']), str(b['showtime_id']), b['customer_name'], b['customer_email'],
            b['booking_date'], f'{b["total_price"]:.2f}', b['status'], seats_booked_str
        ]
        bookings_list.append(record)
    return write_pipe_delimited_file(BOOKINGS_FILE, bookings_list)


@app.route('/')
def root_redirect():
    # root redirects immediately to dashboard page
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Display dashboard page
    # Load all movies and display featured or full list as spec implies
    movies = load_movies()
    return render_template('dashboard.html', movies=movies)


@app.route('/movies')
def movie_catalog():
    # Show movies catalog
    movies = load_movies()
    genres = load_genres()

    # Optionally filter by genre
    genre_filter = request.args.get('genre')
    if genre_filter:
        movies = [m for m in movies if m['genre'].lower() == genre_filter.lower()]

    return render_template('catalog.html', movies=movies, genres=genres, selected_genre=genre_filter)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    # Showtimes for this movie
    showtimes = load_showtimes()
    theaters = load_theaters()

    movie_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    # Add theater info to showtime
    for st in movie_showtimes:
        theater = next((t for t in theaters if t['theater_id'] == st['theater_id']), None)
        st['theater_name'] = theater['theater_name'] if theater else ''

    return render_template('movie_details.html', movie=movie, showtimes=movie_showtimes)


@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    # Display showtimes for movie and allow filter by date
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    showtimes = load_showtimes()
    theaters = load_theaters()
    selected_date = request.args.get('date')

    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if selected_date:
        # Filter by date
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == selected_date]

    # Add theater info to each showtime
    for s in filtered_showtimes:
        theater = next((t for t in theaters if t['theater_id'] == s['theater_id']), None)
        s['theater_name'] = theater['theater_name'] if theater else ''

    return render_template('showtimes.html', movie=movie, showtimes=filtered_showtimes, selected_date=selected_date)


@app.route('/select-seats/<int:showtime_id>')
def seat_selection(showtime_id):
    # Display seat selection page for given showtime
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404

    seats = load_seats()
    # Filter seats by theater_id
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater['theater_id']]

    return render_template('seat_selection.html', showtime=showtime, theater=theater, seats=theater_seats)


@app.route('/confirm-booking/<int:showtime_id>', methods=['POST'])
def confirm_booking_post(showtime_id):
    # Handles booking confirmation POST
    # Selected seat ids expected in form key 'selected_seats' (comma separated string or multiple values)
    selected_seats_raw = request.form.get('selected_seats')
    customer_name = request.form.get('customer_name')
    customer_email = request.form.get('customer_email')

    if not selected_seats_raw or not customer_name or not customer_email:
        return "Missing required booking data", 400

    if ',' in selected_seats_raw:
        selected_seats = [s.strip() for s in selected_seats_raw.split(',') if s.strip()]
    else:
        selected_seats = [selected_seats_raw.strip()]

    if len(selected_seats) == 0:
        return "No seats selected", 400

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    # Calculate total price
    total_price = len(selected_seats) * showtime['price']

    bookings = load_bookings()
    new_booking_id = (max([b['booking_id'] for b in bookings]) + 1) if bookings else 1

    booking_date = datetime.date.today().strftime('%Y-%m-%d')

    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': selected_seats
    }

    bookings.append(new_booking)

    # Save bookings back
    if not save_bookings(bookings):
        return "Failed to save booking", 500

    # Booking confirmation page
    return render_template('booking_confirmation.html', booking=new_booking, showtime=showtime)


@app.route('/booking-history')
def booking_history():
    # List all bookings
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    # Join related info
    for booking in bookings:
        showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
        booking['showtime'] = showtime
        if showtime:
            movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
            booking['movie'] = movie
        else:
            booking['movie'] = None

    return render_template('booking_history.html', bookings=bookings)


@app.route('/booking-history/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)

    return render_template('booking_details.html', booking=booking, showtime=showtime)


if __name__ == '__main__':
    app.run()