from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

data_dir = 'data'

# Helper functions for data loading and saving

def load_movies():
    movies = []
    try:
        with open(os.path.join(data_dir, 'movies.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    except Exception as e:
        print(f"Error loading movies: {e}")
    return movies


def load_theaters():
    theaters = []
    try:
        with open(os.path.join(data_dir, 'theaters.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    theater = {
                        'theater_id': int(parts[0]),
                        'theater_name': parts[1],
                        'location': parts[2],
                        'city': parts[3],
                        'screens': int(parts[4]),
                        'facilities': parts[5]
                    }
                    theaters.append(theater)
    except Exception as e:
        print(f"Error loading theaters: {e}")
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(os.path.join(data_dir, 'showtimes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    except Exception as e:
        print(f"Error loading showtimes: {e}")
    return showtimes


def load_seats():
    seats = []
    try:
        with open(os.path.join(data_dir, 'seats.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    seat = {
                        'seat_id': int(parts[0]),
                        'theater_id': int(parts[1]),
                        'screen_id': int(parts[2]),
                        'row': parts[3],
                        'column': parts[4],
                        'seat_type': parts[5],
                        'status': parts[6]
                    }
                    seats.append(seat)
    except Exception as e:
        print(f"Error loading seats: {e}")
    return seats


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(data_dir, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
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
    except Exception as e:
        print(f"Error loading bookings: {e}")
    return bookings


def load_genres():
    genres = []
    try:
        with open(os.path.join(data_dir, 'genres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    genre = {
                        'genre_id': int(parts[0]),
                        'genre_name': parts[1],
                        'description': parts[2]
                    }
                    genres.append(genre)
    except Exception as e:
        print(f"Error loading genres: {e}")
    return genres


def save_bookings(bookings):
    try:
        with open(os.path.join(data_dir, 'bookings.txt'), 'w', encoding='utf-8') as f:
            for booking in bookings:
                line = f"{booking['booking_id']}|{booking['showtime_id']}|{booking['customer_name']}|{booking['customer_email']}|{booking['booking_date']}|{booking['total_price']}|{booking['status']}|{booking['seats_booked']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving bookings: {e}")

# Root route redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Featured movies: Choose top 5 by rating descending
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:5]
    # Upcoming releases: release_date > today, sorted by release_date ascending
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming_releases = [m for m in movies if m['release_date'] > today_str]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m['release_date'])[:5]
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)

# Movie Catalog
@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    selected_genre = request.args.get('genre', default='')
    search_query = request.args.get('search', default='')

    filtered_movies = movies
    if selected_genre:
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == selected_genre.lower()]
    if search_query:
        sq = search_query.lower()
        filtered_movies = [m for m in filtered_movies if sq in m['title'].lower() or sq in m['genre'].lower()]

    return render_template('movie_catalog.html', movies=filtered_movies, genres=genres, selected_genre=selected_genre, search_query=search_query)

# Movie Details
@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie, movie_id=movie_id)

# Showtime Selection
@app.route('/movies/<int:movie_id>/showtimes')
def showtime_selection(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        return "Movie not found", 404

    showtimes = load_showtimes()
    theaters = load_theaters()

    selected_theater = request.args.get('theater', default='')
    selected_date = request.args.get('date', default='')

    filtered_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]

    if selected_theater:
        filtered_showtimes = [st for st in filtered_showtimes 
                              if any(t['theater_name'].lower() == selected_theater.lower() and t['theater_id'] == st['theater_id'] for t in theaters)]
    if selected_date:
        filtered_showtimes = [st for st in filtered_showtimes if st['showtime_date'] == selected_date]

    return render_template('showtime_selection.html', movie=movie, showtimes=filtered_showtimes, theaters=theaters, selected_theater=selected_theater, selected_date=selected_date)

# Showtime Select POST
@app.route('/showtimes/select', methods=['POST'])
def showtime_select():
    # form: showtime_id (int)
    showtime_id = request.form.get('showtime_id')
    if not showtime_id or not showtime_id.isdigit():
        return "Invalid showtime_id", 400
    showtime_id = int(showtime_id)
    return redirect(url_for('seat_selection', showtime_id=showtime_id))

# Seat Selection
@app.route('/seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    seats = load_seats()
    theaters = load_theaters()
    # Find the theater for the showtime
    theater_id = showtime['theater_id']
    theater = next((t for t in theaters if t['theater_id'] == theater_id), None)

    # Filter seats for the theater and screen_id; screen_id is not present in showtime, 
    # assume screen_id=1 as not specified otherwise
    screen_id = 1
    seats_map = [
        {
            'seat_id': seat['seat_id'],
            'theater_id': seat['theater_id'],
            'screen_id': seat['screen_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat['status']
        } for seat in seats 
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id
    ]

    # selected_seats from query parameter: comma separated seat IDs (e.g. A1,B4)
    selected_seats = request.args.get('selected_seats', '')
    if selected_seats:
        selected_seats = selected_seats.split(',')
    else:
        selected_seats = []

    return render_template('seat_selection.html', showtime=showtime, seats_map=seats_map, selected_seats=selected_seats)

# Booking Confirmation GET
@app.route('/booking/confirm', methods=['GET'])
def booking_confirmation_get():
    showtime_id = request.args.get('showtime_id')
    selected_seats_str = request.args.get('selected_seats', '')
    if not showtime_id or not showtime_id.isdigit():
        return "Invalid showtime_id", 400
    showtime_id = int(showtime_id)

    selected_seats = selected_seats_str.split(',') if selected_seats_str else []

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    # price_total = price * number of seats
    price_total = showtime['price'] * len(selected_seats)

    return render_template('booking_confirmation.html', showtime=showtime, selected_seats=selected_seats, price_total=price_total)

# Booking Confirmation POST
@app.route('/booking/confirm', methods=['POST'])
def booking_confirmation_post():
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    showtime_id = request.form.get('showtime_id')
    selected_seats_raw = request.form.getlist('selected_seats')

    if not (customer_name and customer_email and showtime_id and selected_seats_raw):
        return "Missing booking information", 400

    if not showtime_id.isdigit():
        return "Invalid showtime_id", 400

    showtime_id = int(showtime_id)
    selected_seats = selected_seats_raw

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    # Load existing bookings to generate new booking_id
    bookings = load_bookings()
    max_booking_id = max([b['booking_id'] for b in bookings], default=0)
    new_booking_id = max_booking_id + 1

    booking_date = datetime.now().strftime('%Y-%m-%d')
    total_price = showtime['price'] * len(selected_seats)
    status = 'Confirmed'
    seats_booked = ','.join(selected_seats)

    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': status,
        'seats_booked': seats_booked
    }

    bookings.append(new_booking)
    save_bookings(bookings)

    return redirect(url_for('booking_history'))

# Booking History
@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    status_filter = request.args.get('status', default='All')

    filtered_bookings = bookings
    if status_filter != 'All':
        filtered_bookings = [b for b in filtered_bookings if b['status'] == status_filter]

    return render_template('booking_history.html', bookings=filtered_bookings, status_filter=status_filter)

# Booking Details
@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking is None:
        return "Booking not found", 404
    return render_template('booking_details.html', booking=booking)

# Theater Info
@app.route('/theaters')
def theater_info():
    theaters = load_theaters()
    # Distinct locations based on city field
    locations = sorted(list(set(t['city'] for t in theaters)))
    selected_location = request.args.get('location', default='')
    filtered_theaters = theaters
    if selected_location:
        filtered_theaters = [t for t in theaters if t['city'].lower() == selected_location.lower()]
    else:
        filtered_theaters = theaters

    return render_template('theater_info.html', theaters=filtered_theaters, locations=locations, selected_location=selected_location)

# Back to dashboard from theaters
@app.route('/theaters/back-to-dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()
