'''
Flask routes for 'MovieTicketing' application.
This code defines the root '/' route serving the Dashboard page,
loads featured movies from 'data/movies.txt', and renders the dashboard.html template.
All buttons in the frontend use Flask's url_for for navigation.
Additional routes for other pages are defined with descriptive names,
including catalog, movie details, showtimes, seat selection, booking confirmation,
booking history, and theater information pages.
Data is loaded from local text files in the 'data' directory.
'''
from flask import Flask, render_template, url_for, request, redirect
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
def load_movies():
    movies = []
    movies_file = os.path.join(DATA_DIR, 'movies.txt')
    if os.path.exists(movies_file):
        with open(movies_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                movie_id, title, director, genre, rating, duration, description, release_date = parts
                movies.append({
                    'movie_id': movie_id,
                    'title': title,
                    'director': director,
                    'genre': genre,
                    'rating': float(rating),
                    'duration': int(duration),
                    'description': description,
                    'release_date': release_date
                })
    return movies
def load_theaters():
    theaters = []
    theaters_file = os.path.join(DATA_DIR, 'theaters.txt')
    if os.path.exists(theaters_file):
        with open(theaters_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                theater_id, theater_name, location, city, screens, facilities = parts
                theaters.append({
                    'theater_id': theater_id,
                    'theater_name': theater_name,
                    'location': location,
                    'city': city,
                    'screens': int(screens),
                    'facilities': facilities
                })
    return theaters
def load_showtimes():
    showtimes = []
    showtimes_file = os.path.join(DATA_DIR, 'showtimes.txt')
    if os.path.exists(showtimes_file):
        with open(showtimes_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                showtime_id, movie_id, theater_id, showtime_date, showtime_time, price, available_seats = parts
                showtimes.append({
                    'showtime_id': showtime_id,
                    'movie_id': movie_id,
                    'theater_id': theater_id,
                    'showtime_date': showtime_date,
                    'showtime_time': showtime_time,
                    'price': float(price),
                    'available_seats': int(available_seats)
                })
    return showtimes
def load_seats():
    seats = []
    seats_file = os.path.join(DATA_DIR, 'seats.txt')
    if os.path.exists(seats_file):
        with open(seats_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                seat_id, theater_id, screen_id, row, column, seat_type, status = parts
                seats.append({
                    'seat_id': seat_id,
                    'theater_id': theater_id,
                    'screen_id': screen_id,
                    'row': row,
                    'column': column,
                    'seat_type': seat_type,
                    'status': status
                })
    return seats
def load_bookings():
    bookings = []
    bookings_file = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(bookings_file):
        with open(bookings_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
                booking_id, showtime_id, customer_name, customer_email, booking_date, total_price, status, seats_booked = parts
                bookings.append({
                    'booking_id': booking_id,
                    'showtime_id': showtime_id,
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'booking_date': booking_date,
                    'total_price': float(total_price),
                    'status': status,
                    'seats_booked': seats_booked.split(',') if seats_booked else []
                })
    return bookings
def load_genres():
    genres = []
    genres_file = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(genres_file):
        with open(genres_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                genre_id, genre_name, description = parts
                genres.append({
                    'genre_id': genre_id,
                    'genre_name': genre_name,
                    'description': description
                })
    return genres
@app.route('/')
def dashboard():
    # For simplicity, all movies are featured
    featured_movies = load_movies()
    # Sort upcoming releases by release_date ascending
    upcoming_releases = sorted(featured_movies, key=lambda m: m['release_date'])
    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)
@app.route('/catalog')
def catalog():
    movies = load_movies()
    genres = load_genres()
    search_query = request.args.get('search', '').lower()
    genre_filter = request.args.get('genre', '')
    filtered_movies = []
    for movie in movies:
        if search_query and search_query not in movie['title'].lower() and search_query not in movie['genre'].lower():
            continue
        if genre_filter and genre_filter != 'All' and movie['genre'] != genre_filter:
            continue
        filtered_movies.append(movie)
    return render_template('catalog.html', movies=filtered_movies, genres=genres, selected_genre=genre_filter, search_query=search_query)
@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)
@app.route('/showtimes/<movie_id>')
def showtimes(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    theater_filter = request.args.get('theater', '')
    date_filter = request.args.get('date', '')
    filtered_showtimes = []
    for showtime in showtimes:
        if showtime['movie_id'] != movie_id:
            continue
        if theater_filter and theater_filter != 'All' and showtime['theater_id'] != theater_filter:
            continue
        if date_filter and date_filter != '' and showtime['showtime_date'] != date_filter:
            continue
        filtered_showtimes.append(showtime)
    # Map theater_id to theater_name for display
    theater_dict = {t['theater_id']: t['theater_name'] for t in theaters}
    return render_template('showtimes.html', showtimes=filtered_showtimes, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter, theater_dict=theater_dict, movie_id=movie_id)
@app.route('/seats/<showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    seats = load_seats()
    # Filter seats for this theater and screen (assuming screen_id=1 for simplicity)
    # Since screen_id is not provided in showtimes.txt, assume screen_id=1 for all
    screen_id = '1'
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == screen_id]
    # Build seat map by row and column
    seat_map = {}
    for seat in theater_seats:
        row = seat['row']
        col = seat['column']
        if row not in seat_map:
            seat_map[row] = {}
        seat_map[row][col] = seat
    selected_seats = []
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            error = "Please select at least one seat."
            return render_template('seat_selection.html', showtime=showtime, theater=theater, seat_map=seat_map, selected_seats=selected_seats, error=error)
        # Redirect to booking confirmation with selected seats
        seats_str = ','.join(selected_seats)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=seats_str))
    return render_template('seat_selection.html', showtime=showtime, theater=theater, seat_map=seat_map, selected_seats=selected_seats)
@app.route('/booking_confirmation/<showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    seats_param = request.args.get('seats', '')
    selected_seats = seats_param.split(',') if seats_param else []
    price_per_seat = showtime['price']
    total_price = price_per_seat * len(selected_seats)
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            error = "Please enter your name and email."
            return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price, error=error)
        # Save booking to bookings.txt
        bookings = load_bookings()
        booking_id = str(int(bookings[-1]['booking_id']) + 1 if bookings else 1)
        booking_date = datetime.now().strftime('%Y-%m-%d')
        status = 'Confirmed'
        seats_booked_str = ','.join(selected_seats)
        booking_line = '|'.join([booking_id, showtime_id, customer_name, customer_email, booking_date, f"{total_price:.2f}", status, seats_booked_str])
        bookings_file = os.path.join(DATA_DIR, 'bookings.txt')
        with open(bookings_file, 'a', encoding='utf-8') as f:
            f.write(booking_line + '\n')
        # Update seats status to Booked in seats.txt (optional, since seats.txt is static here)
        # Update available seats in showtimes.txt (optional, not implemented here)
        return redirect(url_for('booking_history'))
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price)
@app.route('/booking_history')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()
    status_filter = request.args.get('status', 'All')
    filtered_bookings = []
    for booking in bookings:
        if status_filter != 'All' and booking['status'] != status_filter:
            continue
        filtered_bookings.append(booking)
    # Map movie_id to title for display
    movie_dict = {m['movie_id']: m['title'] for m in movies}
    return render_template('booking_history.html', bookings=filtered_bookings, movie_dict=movie_dict, status_filter=status_filter)
@app.route('/booking/<booking_id>')
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
    return render_template('booking_details.html', booking=booking, movie=movie, showtime=showtime)
@app.route('/theaters')
def theaters():
    theaters = load_theaters()
    location_filter = request.args.get('location', '')
    filtered_theaters = []
    for theater in theaters:
        if location_filter and location_filter != 'All' and theater['city'] != location_filter:
            continue
        filtered_theaters.append(theater)
    # Get unique locations for filter dropdown
    locations = sorted(set(t['city'] for t in theaters))
    return render_template('theaters.html', theaters=filtered_theaters, locations=locations, selected_location=location_filter)
if __name__ == '__main__':
    app.run(debug=True)