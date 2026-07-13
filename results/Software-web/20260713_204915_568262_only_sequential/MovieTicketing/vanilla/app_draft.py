from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Data Classes for clarity (not strictly necessary but helpful)
class Movie:
    def __init__(self, movie_id, title, director, genre, rating, duration, description, release_date):
        self.movie_id = movie_id
        self.title = title
        self.director = director
        self.genre = genre
        self.rating = rating
        self.duration = duration
        self.description = description
        self.release_date = release_date

class Theater:
    def __init__(self, theater_id, theater_name, location, city, screens, facilities):
        self.theater_id = theater_id
        self.theater_name = theater_name
        self.location = location
        self.city = city
        self.screens = screens
        self.facilities = facilities

class Showtime:
    def __init__(self, showtime_id, movie_id, theater_id, showtime_date, showtime_time, price, available_seats):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.theater_id = theater_id
        self.showtime_date = showtime_date
        self.showtime_time = showtime_time
        self.price = price
        self.available_seats = available_seats

class Seat:
    def __init__(self, seat_id, theater_id, screen_id, row, column, seat_type, status):
        self.seat_id = seat_id
        self.theater_id = theater_id
        self.screen_id = screen_id
        self.row = row
        self.column = column
        self.seat_type = seat_type
        self.status = status

class Booking:
    def __init__(self, booking_id, showtime_id, customer_name, customer_email, booking_date, total_price, status, seats_booked):
        self.booking_id = booking_id
        self.showtime_id = showtime_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.booking_date = booking_date
        self.total_price = total_price
        self.status = status
        self.seats_booked = seats_booked

class Genre:
    def __init__(self, genre_id, genre_name, description):
        self.genre_id = genre_id
        self.genre_name = genre_name
        self.description = description

# Helper functions to load data

def load_movies():
    movies = []
    path = os.path.join(DATA_DIR, 'movies.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    movie = Movie(
                        int(parts[0]), parts[1], parts[2], parts[3],
                        float(parts[4]), int(parts[5]), parts[6], parts[7]
                    )
                    movies.append(movie)
    return movies

def load_theaters():
    theaters = []
    path = os.path.join(DATA_DIR, 'theaters.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    facilities = [fac.strip() for fac in parts[5].split(',')] if parts[5] else []
                    theater = Theater(
                        int(parts[0]), parts[1], parts[2], parts[3], int(parts[4]), facilities
                    )
                    theaters.append(theater)
    return theaters

def load_showtimes():
    showtimes = []
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    showtime = Showtime(
                        int(parts[0]), int(parts[1]), int(parts[2]), parts[3], parts[4], float(parts[5]), int(parts[6])
                    )
                    showtimes.append(showtime)
    return showtimes

def load_seats():
    seats = []
    path = os.path.join(DATA_DIR, 'seats.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    seat = Seat(
                        int(parts[0]), int(parts[1]), int(parts[2]), parts[3], int(parts[4]), parts[5], parts[6]
                    )
                    seats.append(seat)
    return seats

def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    booking = Booking(
                        int(parts[0]), int(parts[1]), parts[2], parts[3], parts[4], float(parts[5]), parts[6], parts[7].split(',') if parts[7] else []
                    )
                    bookings.append(booking)
    return bookings

def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    genre = Genre(int(parts[0]), parts[1], parts[2])
                    genres.append(genre)
    return genres

# Route definitions

@app.route('/')
def root():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    movies = load_movies()
    # Featured movies: top 3 by rating
    featured_movies = sorted(movies, key=lambda m: m.rating, reverse=True)[:3]
    # Upcoming releases: movies with release_date in future
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming_releases = [m for m in movies if m.release_date > today_str]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m.release_date)[:3]
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)

@app.route('/catalog', methods=['GET', 'POST'])
def movie_catalog_page():
    movies = load_movies()
    genres = load_genres()
    selected_genre = ''
    search_query = ''
    if request.method == 'POST':
        selected_genre = request.form.get('genre-filter', '')
        search_query = request.form.get('search-input', '')
    # Filter by genre
    if selected_genre and selected_genre != 'All':
        movies = [m for m in movies if m.genre == selected_genre]
    # Search by title or genre (simplistic contains)
    if search_query:
        sq = search_query.lower()
        movies = [m for m in movies if sq in m.title.lower() or sq in m.genre.lower()]
    genre_names = [g.genre_name for g in genres]
    genre_names = ['All'] + genre_names
    return render_template('catalog.html', movies=movies, genres=genre_names, selected_genre=selected_genre, search_query=search_query)

@app.route('/movie/<int:movie_id>')
def movie_details_page(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m.movie_id == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/showtimes/<int:movie_id>', methods=['GET', 'POST'])
def showtime_selection_page(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    selected_theater = None
    selected_date = None
    if request.method == 'POST':
        theater_filter = request.form.get('theater-filter')
        date_filter = request.form.get('date-filter')
        if theater_filter and theater_filter != 'All':
            try:
                selected_theater = int(theater_filter)
            except ValueError:
                selected_theater = None
        if date_filter:
            selected_date = date_filter
    filtered_showtimes = [st for st in showtimes if (movie_id == 0 or st.movie_id == movie_id)]
    if selected_theater is not None:
        filtered_showtimes = [st for st in filtered_showtimes if st.theater_id == selected_theater]
    if selected_date:
        filtered_showtimes = [st for st in filtered_showtimes if st.showtime_date == selected_date]
    return render_template('showtimes.html', showtimes=filtered_showtimes, theaters=theaters, selected_theater=selected_theater, selected_date=selected_date)

@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection_page(showtime_id):
    showtimes = load_showtimes()
    seats = load_seats()
    showtime = next((st for st in showtimes if st.showtime_id == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    # Filter seats by theater and screen
    # We don't have screen info in showtime, assume screen 1 for demo
    theater_id = showtime.theater_id
    # For demo, consider screen_id = 1
    screen_id = 1
    relevant_seats = [s for s in seats if s.theater_id == theater_id and s.screen_id == screen_id]

    selected_seats = []
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')

    return render_template('seat_selection.html', seats=relevant_seats, selected_seats=selected_seats, showtime=showtime)

@app.route('/booking/confirm', methods=['GET', 'POST'])
def booking_confirmation_page():
    booking_summary = {}
    customer_name = ''
    customer_email = ''
    if request.method == 'POST':
        customer_name = request.form.get('customer-name')
        customer_email = request.form.get('customer-email')
        seats = request.form.get('selected-seats')  # comma separated seat codes
        showtime_id = request.form.get('showtime-id')
        if customer_name and customer_email and seats and showtime_id:
            # Save booking
            bookings = load_bookings()
            new_booking_id = max([b.booking_id for b in bookings], default=0) + 1
            showtimes = load_showtimes()
            showtime = next((st for st in showtimes if str(st.showtime_id) == showtime_id), None)
            if showtime:
                total_price = len(seats.split(',')) * showtime.price
                today_str = datetime.now().strftime('%Y-%m-%d')
                new_booking = Booking(
                    new_booking_id,
                    showtime.showtime_id,
                    customer_name,
                    customer_email,
                    today_str,
                    total_price,
                    'Confirmed',
                    seats.split(',')
                )
                bookings.append(new_booking)
                # Write back to file
                with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
                    for b in bookings:
                        f.write(f"{b.booking_id}|{b.showtime_id}|{b.customer_name}|{b.customer_email}|{b.booking_date}|{b.total_price}|{b.status}|{','.join(b.seats_booked)}\n")
                return redirect(url_for('booking_history_page'))
        else:
            booking_summary = {
                'showtime_id': showtime_id,
                'seats': seats,
                'customer_name': customer_name,
                'customer_email': customer_email
            }
    else:
        # GET method - gather info from query parameters or session (simplified here)
        booking_summary = request.args

    return render_template('booking_confirmation.html', booking_summary=booking_summary, customer_name=customer_name, customer_email=customer_email)

@app.route('/bookings')
def booking_history_page():
    bookings = load_bookings()
    movies = load_movies()
    selected_status = request.args.get('status-filter', 'All')
    if selected_status != 'All':
        bookings = [b for b in bookings if b.status == selected_status]
    # Attach movie title for display
    movie_dict = {m.movie_id: m for m in movies}
    return render_template('booking_history.html', bookings=bookings, selected_status=selected_status)

@app.route('/booking/<int:booking_id>')
def booking_details_page(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b.booking_id == booking_id), None)
    if not booking:
        return "Booking not found", 404
    return render_template('booking_details.html', booking=booking)

@app.route('/theaters')
def theater_information_page():
    theaters = load_theaters()
    selected_location = request.args.get('theater-location-filter')
    if selected_location and selected_location != 'All':
        theaters = [t for t in theaters if t.location == selected_location]
    return render_template('theaters.html', theaters=theaters, selected_location=selected_location)

if __name__ == '__main__':
    app.run(debug=True)
