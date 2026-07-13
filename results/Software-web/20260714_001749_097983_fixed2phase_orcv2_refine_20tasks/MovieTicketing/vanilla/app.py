from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Helper function to read data files
# Each returns list of dicts

def read_movies():
    path = os.path.join(data_dir, 'movies.txt')
    movies = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                movie = {
                    'movie_id': int(parts[0]),
                    "title": parts[1],
                    "director": parts[2],
                    "genre": parts[3],
                    "rating": float(parts[4]),
                    "duration": int(parts[5]),
                    "description": parts[6],
                    "release_date": parts[7]
                }
                movies.append(movie)
    return movies


def read_theaters():
    path = os.path.join(data_dir, 'theaters.txt')
    theaters = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                theater = {
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': int(parts[4]),
                    'facilities': parts[5].split(', ')
                }
                theaters.append(theater)
    return theaters


def read_showtimes():
    path = os.path.join(data_dir, 'showtimes.txt')
    showtimes = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
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
    return showtimes


def read_seats():
    path = os.path.join(data_dir, 'seats.txt')
    seats = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
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
    return seats


def read_bookings():
    path = os.path.join(data_dir, 'bookings.txt')
    bookings = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
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
    return bookings


def read_genres():
    path = os.path.join(data_dir, 'genres.txt')
    genres = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    return genres

# Save bookings with overwrite

def save_bookings(bookings):
    path = os.path.join(data_dir, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            seats_str = ','.join(b['seats_booked'])
            line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
            f.write(line)


# Helper to get next ID

def next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1


# Routes Implementation

@app.route('/')
def dashboard():
    # Show dashboard with featured movies: show 5 highest rated recent movies
    movies = read_movies()
    # Sort by rating desc, then release_date desc
    movies_sorted = sorted(movies, key=lambda m: (m['rating'], m['release_date']), reverse=True)
    featured_movies = movies_sorted[:5]
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/catalog', methods=['GET'])
def movie_catalog():
    movies = read_movies()
    genres = read_genres()
    # Optional filters
    search = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')

    # Filter movies
    filtered = movies
    if search:
        filtered = [m for m in filtered if search in m['title'].lower() or search in m['genre'].lower()]
    if genre_filter and genre_filter != 'All':
        filtered = [m for m in filtered if m['genre'] == genre_filter]

    return render_template('movie_catalog.html', movies=filtered, genres=genres, search=search, genre_filter=genre_filter)


@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movies = read_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes', methods=['GET'])
def showtime_selection():
    showtimes = read_showtimes()
    movies = {m['movie_id']: m for m in read_movies()}
    theaters = read_theaters()
    theater_filter = request.args.get('theater', '')
    date_filter = request.args.get('date', '')

    filtered = showtimes
    if theater_filter:
        try:
            tid = int(theater_filter)
            filtered = [s for s in filtered if s['theater_id'] == tid]
        except ValueError:
            pass
    if date_filter:
        filtered = [s for s in filtered if s['showtime_date'] == date_filter]

    # Deduplicate list of theaters for filter dropdown
    return render_template('showtime_selection.html', showtimes=filtered, movies=movies, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter)


@app.route('/seat_selection/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtimes = read_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    theaters = read_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    seats = read_seats()

    # Filter seats for that theater
    theater_seats = [s for s in seats if s['theater_id'] == showtime['theater_id']]

    # Using POST to handle seat selection save is out of scope, proceed with GET display
    # Group seats by row for display
    seats_by_row = {}
    for seat in theater_seats:
        row = seat['row']
        if row not in seats_by_row:
            seats_by_row[row] = []
        seats_by_row[row].append(seat)

    # Sort seats by column
    for row in seats_by_row:
        seats_by_row[row].sort(key=lambda x: x['column'])

    return render_template('seat_selection.html', showtime=showtime, seats_by_row=seats_by_row)


@app.route('/booking_confirmation/<int:showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtimes = read_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movies = {m['movie_id']: m for m in read_movies()}
    movie = movies.get(showtime['movie_id'])
    bookings = read_bookings()

    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        seats_selected = request.form.get('seats_selected', '')

        if not (customer_name and customer_email and seats_selected):
            error = "Please provide name, email, and select seats."
            return render_template('booking_confirmation.html', showtime=showtime, movie=movie, error=error)

        seats_list = seats_selected.split(',')

        # Calculate total price
        total_price = showtime['price'] * len(seats_list)

        # Save booking
        bookings = read_bookings()
        new_booking_id = next_id(bookings, 'booking_id')
        booking_date = datetime.now().strftime('%Y-%m-%d')
        new_booking = {
            'booking_id': new_booking_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_list
        }
        bookings.append(new_booking)
        save_bookings(bookings)

        return redirect(url_for('booking_history'))

    # GET render form
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie)


@app.route('/booking_history', methods=['GET'])
def booking_history():
    bookings = read_bookings()
    showtimes = {s['showtime_id']: s for s in read_showtimes()}
    movies = {m['movie_id']: m for m in read_movies()}

    # Filter by status
    status_filter = request.args.get('status', 'All')
    filtered = bookings
    if status_filter and status_filter != 'All':
        filtered = [b for b in filtered if b['status'] == status_filter]

    return render_template('booking_history.html', bookings=filtered, showtimes=showtimes, movies=movies, status_filter=status_filter)


@app.route('/booking/<int:booking_id>')
def view_booking(booking_id):
    bookings = read_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = {s['showtime_id']: s for s in read_showtimes()}
    showtime = showtimes.get(booking['showtime_id'])
    movies = {m['movie_id']: m for m in read_movies()}
    movie = movies.get(showtime['movie_id']) if showtime else None

    return render_template('booking_confirmation.html', booking=booking, showtime=showtime, movie=movie, view_only=True)


@app.route('/theaters', methods=['GET'])
def theater_info():
    theaters = read_theaters()
    location_filter = request.args.get('location', '')

    filtered = theaters
    if location_filter and location_filter != 'All':
        filtered = [t for t in theaters if t['city'] == location_filter]

    # Extract list of cities
    cities = list(sorted(set(t['city'] for t in theaters)))

    return render_template('theater_info.html', theaters=filtered, cities=cities, location_filter=location_filter)


@app.route('/dashboard')
def redirect_dashboard():
    return redirect(url_for('dashboard'))


# Run app
if __name__ == '__main__':
    app.run(debug=True)
