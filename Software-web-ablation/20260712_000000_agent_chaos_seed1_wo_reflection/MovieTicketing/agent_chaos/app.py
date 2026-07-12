from flask import Flask, render_template, redirect, url_for, request
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
MOVIES_FILE = 'data/movies.txt'
THEATERS_FILE = 'data/theaters.txt'
SHOWTIMES_FILE = 'data/showtimes.txt'
SEATS_FILE = 'data/seats.txt'
BOOKINGS_FILE = 'data/bookings.txt'
GENRES_FILE = 'data/genres.txt'

# Helper functions to load data

def load_movies():
    movies = []
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return movies


def load_theaters():
    theaters = []
    try:
        with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 6:
                    continue
                theater = {
                    'theater_id': int(row[0]),
                    'theater_name': row[1],
                    'location': row[2],
                    'city': row[3],
                    'screens': int(row[4]),
                    'facilities': row[5]
                }
                theaters.append(theater)
    except FileNotFoundError:
        pass
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 7:
                    continue
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
    except FileNotFoundError:
        pass
    return showtimes


def load_seats():
    seats = []
    try:
        with open(SEATS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 7:
                    continue
                seat = {
                    'seat_id': int(row[0]),
                    'theater_id': int(row[1]),
                    'screen_id': int(row[2]),
                    'row': row[3],
                    'column': int(row[4]),
                    'seat_type': row[5],
                    'status': row[6]
                }
                seats.append(seat)
    except FileNotFoundError:
        pass
    return seats


def load_bookings():
    bookings = []
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return bookings


def load_genres():
    genres = []
    try:
        with open(GENRES_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) < 3:
                    continue
                genre = {
                    'genre_id': int(row[0]),
                    'genre_name': row[1],
                    'description': row[2]
                }
                genres.append(genre)
    except FileNotFoundError:
        pass
    return genres

# Helper function to save bookings

def save_bookings(bookings):
    try:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for b in bookings:
                writer.writerow([
                    b['booking_id'],
                    b['showtime_id'],
                    b['customer_name'],
                    b['customer_email'],
                    b['booking_date'],
                    f"{b['total_price']:.2f}",
                    b['status'],
                    ','.join(b['seats_booked'])
                ])
    except Exception as e:
        print(f"Error saving bookings: {e}")

# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # For featured movies, select first 4 movies sorted by rating desc
    featured_sorted = sorted(movies, key=lambda x: x['rating'], reverse=True)
    featured_movies = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'rating': m['rating'],
            'duration': m['duration']
        } for m in featured_sorted[:4]
    ]
    return render_template('dashboard.html', featured_movies=featured_movies)

@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    # Construct movies list with possible poster_url property (not in data so omit)
    movie_list = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster_url': ''  # Optional; leave empty
        } for m in movies
    ]
    return render_template('movie_catalog.html', movies=movie_list, genres=genres)

@app.route('/movies/search', methods=['POST'])
def movie_search():
    search_term = request.form.get('search', '').strip().lower()
    selected_genre = request.form.get('genre', '').strip().lower()

    movies = load_movies()
    genres = load_genres()

    filtered_movies = []
    for m in movies:
        title_match = search_term in m['title'].lower() if search_term else True
        genre_match = (selected_genre == m['genre'].lower()) if selected_genre else True
        if title_match and genre_match:
            filtered_movies.append({
                'movie_id': m['movie_id'],
                'title': m['title'],
                'genre': m['genre'],
                'rating': m['rating'],
                'duration': m['duration'],
                'poster_url': ''  # Optional; leave empty
            })

    return render_template('movie_catalog.html', filtered_movies=filtered_movies, genres=genres)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    movie_dict = {
        'movie_id': movie['movie_id'],
        'title': movie['title'],
        'director': movie['director'],
        'genre': movie['genre'],
        'rating': movie['rating'],
        'duration': movie['duration'],
        'description': movie['description']
    }

    return render_template('movie_details.html', movie=movie_dict)

@app.route('/showtimes')
def showtime_selection():
    showtimes = load_showtimes()
    theaters = load_theaters()

    return render_template('showtime_selection.html', showtimes=showtimes, theaters=theaters)

@app.route('/select_showtime/<int:showtime_id>')
def select_showtime(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    seats = load_seats()
    # Filter seats for the theater of this showtime
    seats_filtered = [s for s in seats if s['theater_id'] == showtime['theater_id']]

    return render_template('seat_selection.html', seats=seats_filtered, showtime=showtime)

@app.route('/book_seats', methods=['POST'])
def book_seats():
    # Expecting 'showtime_id' and list of 'selected_seats' (seat row+col) from form
    showtime_id = request.form.get('showtime_id')
    selected_seats = request.form.getlist('selected_seats')

    if not showtime_id or not selected_seats:
        return "Missing booking data", 400

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == int(showtime_id)), None)
    if not showtime:
        return "Invalid showtime", 400

    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Invalid movie", 400

    total_price = showtime['price'] * len(selected_seats)

    booking_summary = {
        'movie_title': movie['title'],
        'showtime_datetime': f"{showtime['showtime_date']} {showtime['showtime_time']}",
        'seats': selected_seats,
        'total_price': total_price
    }

    # Pass showtime_id and seats to template to carry on confirming booking
    return render_template('booking_confirmation.html', booking_summary=booking_summary, showtime_id=int(showtime_id), seats=selected_seats)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    showtime_id = request.form.get('showtime_id')
    seats = request.form.getlist('seats')
    customer_name = request.form.get('customer_name')
    customer_email = request.form.get('customer_email')

    if not (showtime_id and seats and customer_name and customer_email):
        return "Incomplete booking data", 400

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == int(showtime_id)), None)
    if not showtime:
        return "Invalid showtime", 400

    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Invalid movie", 400

    bookings = load_bookings()
    new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

    booking_date_str = datetime.now().strftime('%Y-%m-%d')
    total_price = showtime['price'] * len(seats)
    seats_str = ','.join(seats)

    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': int(showtime_id),
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date_str,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats
    }

    bookings.append(new_booking)
    # Save to file
    save_bookings(bookings)

    return render_template('booking_confirmation.html', confirmation_status='Booking confirmed!', booking_id=new_booking_id)

@app.route('/bookings', methods=['GET'])
def booking_history():
    bookings = load_bookings()
    movies = load_movies()

    bookings_list = []
    for b in bookings:
        movie = next((m for m in movies if m['movie_id'] == load_showtime_movie_id(b['showtime_id'])), None)
        movie_title = movie['title'] if movie else 'Unknown'
        bookings_list.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status']
        })

    return render_template('booking_history.html', bookings=bookings_list)

# Helper to get movie_id from a showtime_id

def load_showtime_movie_id(showtime_id):
    showtimes = load_showtimes()
    st = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    return st['movie_id'] if st else None

@app.route('/bookings/<int:booking_id>', methods=['GET'])
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    movies = load_movies()
    showtimes = load_showtimes()

    movie = None
    showtime = None

    if booking:
        showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
        if showtime:
            movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)

    booking_dict = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'] if movie else 'Unknown',
        'showtime_date': showtime['showtime_date'] if showtime else '',
        'showtime_time': showtime['showtime_time'] if showtime else '',
        'seats_booked': booking['seats_booked'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price'],
        'status': booking['status']
    }

    return render_template('booking_details.html', booking=booking_dict)

@app.route('/theaters', methods=['GET'])
def theater_information():
    theaters = load_theaters()
    return render_template('theater_information.html', theaters=theaters)

if __name__ == '__main__':
    app.run()
