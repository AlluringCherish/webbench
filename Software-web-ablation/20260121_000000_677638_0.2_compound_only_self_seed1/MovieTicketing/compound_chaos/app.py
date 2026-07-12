from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_dir = 'data'

# Utility functions to load data files

def load_movies():
    movies = []
    path = os.path.join(data_dir, 'movies.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                movies.append({
                    'movie_id': int(parts[0]),
                    'title': parts[1],
                    'director': parts[2],
                    'genre': parts[3],
                    'rating': float(parts[4]),
                    'duration': int(parts[5]),
                    'description': parts[6],
                    'release_date': parts[7]
                })
    except FileNotFoundError:
        pass
    return movies

def load_theaters():
    theaters = []
    path = os.path.join(data_dir, 'theaters.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                theaters.append({
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': int(parts[4]),
                    'facilities': parts[5]
                })
    except FileNotFoundError:
        pass
    return theaters

def load_showtimes():
    showtimes = []
    path = os.path.join(data_dir, 'showtimes.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                showtimes.append({
                    'showtime_id': int(parts[0]),
                    'movie_id': int(parts[1]),
                    'theater_id': int(parts[2]),
                    'showtime_date': parts[3],
                    'showtime_time': parts[4],
                    'price': float(parts[5]),
                    'available_seats': int(parts[6])
                })
    except FileNotFoundError:
        pass
    return showtimes

def load_seats():
    seats = []
    path = os.path.join(data_dir, 'seats.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                seats.append({
                    'seat_id': int(parts[0]),
                    'theater_id': int(parts[1]),
                    'screen_id': int(parts[2]),
                    'row': parts[3],
                    'column': parts[4],
                    'seat_type': parts[5],
                    'status': parts[6]
                })
    except FileNotFoundError:
        pass
    return seats

def load_bookings():
    bookings = []
    path = os.path.join(data_dir, 'bookings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                bookings.append({
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': parts[7].split(',') if parts[7] else []
                })
    except FileNotFoundError:
        pass
    return bookings

def load_genres():
    genres = []
    path = os.path.join(data_dir, 'genres.txt')
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                genres.append({
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                })
    except FileNotFoundError:
        pass
    return genres

# Utility function to save bookings

def save_bookings(bookings):
    path = os.path.join(data_dir, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as file:
            for booking in bookings:
                seats_str = ','.join(booking['seats_booked'])
                file.write(f"{booking['booking_id']}|{booking['showtime_id']}|{booking['customer_name']}|{booking['customer_email']}|{booking['booking_date']}|{booking['total_price']}|{booking['status']}|{seats_str}\n")
    except Exception:
        pass

# Flask routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    today = datetime.now().date()
    upcoming_releases = [m for m in movies if datetime.strptime(m['release_date'], '%Y-%m-%d').date() > today]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m['release_date'])[:3]
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)

@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    search_query = request.args.get('search_query', '').strip()
    selected_genre = request.args.get('selected_genre', '').strip()
    filtered_movies = movies
    if selected_genre:
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == selected_genre.lower()]
    if search_query:
        sq = search_query.lower()
        filtered_movies = [m for m in filtered_movies if sq in m['title'].lower() or sq in m['genre'].lower()]
    return render_template('movie_catalog.html', movies=filtered_movies, genres=genres, selected_genre=selected_genre, search_query=search_query)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    genres = load_genres()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie, genres=genres)

@app.route('/showtimes/<int:movie_id>')
def showtime_selection(movie_id):
    movies = load_movies()
    showtimes = load_showtimes()
    theaters = load_theaters()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    selected_theater = request.args.get('selected_theater', '').strip()
    selected_date = request.args.get('selected_date', '').strip()
    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if selected_theater:
        try:
            tid = int(selected_theater)
            filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] == tid]
        except ValueError:
            pass
    if selected_date:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == selected_date]
    return render_template('showtime_selection.html', movie=movie, showtimes=filtered_showtimes, theaters=theaters, selected_theater=selected_theater, selected_date=selected_date)

@app.route('/select-seats/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404
    seats = load_seats()
    screen_id = 1
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == screen_id]
    selected_seats_param = request.args.get('selected_seats', '').strip()
    selected_seats = selected_seats_param.split(',') if selected_seats_param else []
    return render_template('seat_selection.html', showtime=showtime, seats=theater_seats, selected_seats=selected_seats)

@app.route('/confirm-booking/<int:showtime_id>', methods=['GET'])
def booking_confirmation(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404
    selected_seats_param = request.args.get('selected_seats', '').strip()
    selected_seats = selected_seats_param.split(',') if selected_seats_param else []
    total_price = len(selected_seats) * showtime['price']
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price)

@app.route('/confirm-booking/<int:showtime_id>', methods=['POST'])
def confirm_booking(showtime_id):
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    selected_seats = request.form.getlist('selected_seats')
    if not customer_name or not customer_email or not selected_seats:
        flash('All fields including seat selection are required.')
        seats_param = ','.join(selected_seats)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, selected_seats=seats_param))
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404
    bookings = load_bookings()
    new_id = max((b['booking_id'] for b in bookings), default=0) + 1
    total_price = len(selected_seats) * showtime['price']
    booking_date = datetime.now().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': new_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': selected_seats
    }
    bookings.append(new_booking)
    save_bookings(bookings)
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price)

@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    selected_status = request.args.get('selected_status', '').strip()
    filtered = bookings
    if selected_status:
        filtered = [b for b in bookings if b['status'].lower() == selected_status.lower()]
    return render_template('booking_history.html', bookings=filtered, selected_status=selected_status)

@app.route('/bookings/<int:booking_id>')
def view_booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    movies = load_movies()
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    movie = next((m for m in movies if showtime and m['movie_id'] == showtime['movie_id']), None)
    return render_template('booking_details.html', booking=booking, movie=movie, showtime=showtime)

@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    selected_location = request.args.get('selected_location', '').strip()
    filtered = theaters
    if selected_location:
        filtered = [t for t in theaters if t['location'].lower() == selected_location.lower()]
    return render_template('theater_information.html', theaters=filtered, selected_location=selected_location)

if __name__ == '__main__':
    app.run()