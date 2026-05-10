'''
Main backend application for MovieTicketing web application.
Handles routing, data processing, reading/writing local text files in data/,
and rendering HTML templates for all eight pages.
No authentication required; all features directly accessible.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'movie_ticketing_secret_key'  # Needed for flashing messages
DATA_DIR = 'data'
# Utility functions to read and write data files
def read_movies():
    movies = []
    path = os.path.join(DATA_DIR, 'movies.txt')
    if not os.path.exists(path):
        return movies
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            movie = {
                'movie_id': parts[0],
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
def read_theaters():
    theaters = []
    path = os.path.join(DATA_DIR, 'theaters.txt')
    if not os.path.exists(path):
        return theaters
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            theater = {
                'theater_id': parts[0],
                'theater_name': parts[1],
                'location': parts[2],
                'city': parts[3],
                'screens': int(parts[4]),
                'facilities': parts[5]
            }
            theaters.append(theater)
    return theaters
def read_showtimes():
    showtimes = []
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    if not os.path.exists(path):
        return showtimes
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            showtime = {
                'showtime_id': parts[0],
                'movie_id': parts[1],
                'theater_id': parts[2],
                'showtime_date': parts[3],
                'showtime_time': parts[4],
                'price': float(parts[5]),
                'available_seats': int(parts[6])
            }
            showtimes.append(showtime)
    return showtimes
def read_seats():
    seats = []
    path = os.path.join(DATA_DIR, 'seats.txt')
    if not os.path.exists(path):
        return seats
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            seat = {
                'seat_id': parts[0],
                'theater_id': parts[1],
                'screen_id': parts[2],
                'row': parts[3],
                'column': parts[4],
                'seat_type': parts[5],
                'status': parts[6]
            }
            seats.append(seat)
    return seats
def read_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if not os.path.exists(path):
        return bookings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            booking = {
                'booking_id': parts[0],
                'showtime_id': parts[1],
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
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if not os.path.exists(path):
        return genres
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            genre = {
                'genre_id': parts[0],
                'genre_name': parts[1],
                'description': parts[2]
            }
            genres.append(genre)
    return genres
def write_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            seats_str = ','.join(b['seats_booked'])
            line = '|'.join([
                b['booking_id'],
                b['showtime_id'],
                b['customer_name'],
                b['customer_email'],
                b['booking_date'],
                f"{b['total_price']:.2f}",
                b['status'],
                seats_str
            ])
            f.write(line + '\n')
def write_showtimes(showtimes):
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in showtimes:
            line = '|'.join([
                s['showtime_id'],
                s['movie_id'],
                s['theater_id'],
                s['showtime_date'],
                s['showtime_time'],
                f"{s['price']:.2f}",
                str(s['available_seats'])
            ])
            f.write(line + '\n')
def write_seats(seats):
    path = os.path.join(DATA_DIR, 'seats.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in seats:
            line = '|'.join([
                s['seat_id'],
                s['theater_id'],
                s['screen_id'],
                s['row'],
                s['column'],
                s['seat_type'],
                s['status']
            ])
            f.write(line + '\n')
# Helper functions
def get_movie_by_id(movie_id):
    movies = read_movies()
    for m in movies:
        if m['movie_id'] == movie_id:
            return m
    return None
def get_theater_by_id(theater_id):
    theaters = read_theaters()
    for t in theaters:
        if t['theater_id'] == theater_id:
            return t
    return None
def get_showtime_by_id(showtime_id):
    showtimes = read_showtimes()
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            return s
    return None
def get_seats_by_theater_and_screen(theater_id, screen_id):
    seats = read_seats()
    filtered = [s for s in seats if s['theater_id'] == theater_id and s['screen_id'] == screen_id]
    return filtered
def get_bookings_filtered(status_filter=None):
    bookings = read_bookings()
    if status_filter and status_filter != 'All':
        bookings = [b for b in bookings if b['status'] == status_filter]
    return bookings
def get_genre_names():
    genres = read_genres()
    return [g['genre_name'] for g in genres]
def get_movies_filtered(search_term=None, genre_filter=None):
    movies = read_movies()
    filtered = movies
    if search_term:
        search_term_lower = search_term.lower()
        filtered = [m for m in filtered if search_term_lower in m['title'].lower() or search_term_lower in m['genre'].lower()]
    if genre_filter and genre_filter != 'All':
        filtered = [m for m in filtered if m['genre'] == genre_filter]
    return filtered
def get_showtimes_filtered(movie_id=None, theater_filter=None, date_filter=None):
    showtimes = read_showtimes()
    filtered = showtimes
    if movie_id:
        filtered = [s for s in filtered if s['movie_id'] == movie_id]
    if theater_filter and theater_filter != 'All':
        filtered = [s for s in filtered if s['theater_id'] == theater_filter]
    if date_filter:
        filtered = [s for s in filtered if s['showtime_date'] == date_filter]
    return filtered
def generate_new_booking_id():
    bookings = read_bookings()
    if not bookings:
        return '1'
    max_id = max(int(b['booking_id']) for b in bookings)
    return str(max_id + 1)
def update_seat_statuses(seats_to_book, theater_id, screen_id):
    seats = read_seats()
    seat_map = {(s['row'], s['column']): s for s in seats if s['theater_id'] == theater_id and s['screen_id'] == screen_id}
    for seat_code in seats_to_book:
        if len(seat_code) < 2:
            continue
        row = seat_code[0]
        col = seat_code[1:]
        seat = seat_map.get((row, col))
        if seat and seat['status'] == 'Available':
            seat['status'] = 'Booked'
    # Write back updated seats
    write_seats(seats)
def reduce_showtime_available_seats(showtime_id, count):
    showtimes = read_showtimes()
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            s['available_seats'] = max(0, s['available_seats'] - count)
            break
    write_showtimes(showtimes)
# Routes
@app.route('/')
def dashboard():
    # Show featured movies and upcoming releases
    movies = read_movies()
    # For featured movies, pick top 3 by rating descending
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    # Upcoming releases: movies with release_date in future (>= today)
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming_releases = [m for m in movies if m['release_date'] >= today_str]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m['release_date'])[:3]
    return render_template('dashboard.html',
                           featured_movies=featured_movies,
                           upcoming_releases=upcoming_releases)
@app.route('/movie_catalog', methods=['GET', 'POST'])
def movie_catalog():
    genres = get_genre_names()
    genres.insert(0, 'All')
    search_term = request.args.get('search', '').strip()
    genre_filter = request.args.get('genre', 'All')
    movies = get_movies_filtered(search_term=search_term, genre_filter=genre_filter)
    return render_template('movie_catalog.html',
                           movies=movies,
                           genres=genres,
                           selected_genre=genre_filter,
                           search_term=search_term)
@app.route('/movie_details/<movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('movie_catalog'))
    return render_template('movie_details.html', movie=movie)
@app.route('/showtime_selection/<movie_id>', methods=['GET'])
def showtime_selection(movie_id):
    theaters = read_theaters()
    theater_filter = request.args.get('theater', 'All')
    date_filter = request.args.get('date', '')
    showtimes = get_showtimes_filtered(movie_id=movie_id, theater_filter=theater_filter, date_filter=date_filter)
    # Enrich showtimes with theater name
    theater_dict = {t['theater_id']: t['theater_name'] for t in theaters}
    for s in showtimes:
        s['theater_name'] = theater_dict.get(s['theater_id'], 'Unknown')
    theater_options = ['All'] + [t['theater_id'] for t in theaters]
    return render_template('showtime_selection.html',
                           showtimes=showtimes,
                           theater_filter=theater_filter,
                           date_filter=date_filter,
                           theaters=theaters,
                           movie_id=movie_id)
@app.route('/seat_selection/<showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('dashboard'))
    theater_id = showtime['theater_id']
    # We do not have screen_id in showtimes.txt, but seats.txt requires screen_id.
    # The data format for seats.txt includes screen_id, but showtimes.txt does not.
    # We must assume screen_id = 1 for all showtimes for simplicity (since no screen_id in showtimes).
    screen_id = '1'
    seats = get_seats_by_theater_and_screen(theater_id, screen_id)
    # Build seat map by row and column
    seat_map = {}
    rows = set()
    cols = set()
    for seat in seats:
        row = seat['row']
        col = seat['column']
        rows.add(row)
        cols.add(col)
        seat_map[(row, col)] = seat
    rows = sorted(rows)
    # Sort columns as integers if possible, else lex
    try:
        cols = sorted(cols, key=lambda x: int(x))
    except:
        cols = sorted(cols)
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            flash('Please select at least one seat.', 'error')
            return redirect(request.url)
        # Store selected seats and showtime_id in session or pass via query string
        # Since no session specified, pass via query string for confirmation page
        seats_str = ','.join(selected_seats)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=seats_str))
    return render_template('seat_selection.html',
                           showtime=showtime,
                           seat_map=seat_map,
                           rows=rows,
                           cols=cols)
@app.route('/booking_confirmation/<showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('dashboard'))
    movie = get_movie_by_id(showtime['movie_id'])
    theater = get_theater_by_id(showtime['theater_id'])
    seats_str = request.args.get('seats', '')
    selected_seats = seats_str.split(',') if seats_str else []
    if not selected_seats:
        flash('No seats selected.', 'error')
        return redirect(url_for('seat_selection', showtime_id=showtime_id))
    total_price = showtime['price'] * len(selected_seats)
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            flash('Please enter your name and email.', 'error')
            return redirect(request.url)
        # Create new booking
        bookings = read_bookings()
        new_booking_id = generate_new_booking_id()
        booking_date = datetime.now().strftime('%Y-%m-%d')
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
        write_bookings(bookings)
        # Update seat statuses
        update_seat_statuses(selected_seats, theater['theater_id'], '1')
        # Reduce available seats in showtime
        reduce_showtime_available_seats(showtime_id, len(selected_seats))
        flash('Booking confirmed successfully!', 'success')
        return redirect(url_for('booking_history'))
    return render_template('booking_confirmation.html',
                           showtime=showtime,
                           movie=movie,
                           theater=theater,
                           selected_seats=selected_seats,
                           total_price=total_price)
@app.route('/booking_history', methods=['GET'])
def booking_history():
    status_filter = request.args.get('status', 'All')
    bookings = get_bookings_filtered(status_filter=status_filter)
    # Enrich bookings with movie title and showtime date/time
    movies = {m['movie_id']: m['title'] for m in read_movies()}
    showtimes = {s['showtime_id']: s for s in read_showtimes()}
    enriched_bookings = []
    for b in bookings:
        showtime = showtimes.get(b['showtime_id'])
        movie_title = movies.get(showtime['movie_id']) if showtime else 'Unknown'
        booking_info = b.copy()
        booking_info['movie_title'] = movie_title
        booking_info['showtime_date'] = showtime['showtime_date'] if showtime else ''
        booking_info['showtime_time'] = showtime['showtime_time'] if showtime else ''
        enriched_bookings.append(booking_info)
    return render_template('booking_history.html',
                           bookings=enriched_bookings,
                           status_filter=status_filter)
@app.route('/booking_history/view/<booking_id>')
def view_booking(booking_id):
    bookings = read_bookings()
    booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            booking = b
            break
    if not booking:
        flash('Booking not found.', 'error')
        return redirect(url_for('booking_history'))
    showtime = get_showtime_by_id(booking['showtime_id'])
    movie = get_movie_by_id(showtime['movie_id']) if showtime else None
    theater = get_theater_by_id(showtime['theater_id']) if showtime else None
    return render_template('booking_details.html',
                           booking=booking,
                           showtime=showtime,
                           movie=movie,
                           theater=theater)
@app.route('/theater_information', methods=['GET'])
def theater_information():
    theaters = read_theaters()
    location_filter = request.args.get('location', 'All')
    if location_filter != 'All':
        theaters = [t for t in theaters if t['city'] == location_filter]
    # Get unique cities for filter dropdown
    cities = sorted(set(t['city'] for t in read_theaters()))
    cities.insert(0, 'All')
    return render_template('theater_information.html',
                           theaters=theaters,
                           location_filter=location_filter,
                           cities=cities)
# Navigation routes for buttons on dashboard and other pages
@app.route('/navigate_to_catalog')
def navigate_to_catalog():
    return redirect(url_for('movie_catalog'))
@app.route('/navigate_to_bookings')
def navigate_to_bookings():
    return redirect(url_for('booking_history'))
@app.route('/navigate_to_showtimes')
def navigate_to_showtimes():
    # Redirect to showtime selection page without movie filter (show all)
    # Since showtime_selection requires movie_id, redirect to movie_catalog instead
    return redirect(url_for('movie_catalog'))
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# Run the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)