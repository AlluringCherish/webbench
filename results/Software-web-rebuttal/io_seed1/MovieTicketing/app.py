'''
Main backend Python application file for MovieTicketing web application.
Handles routing, data processing, reading and writing to local text files in the data/ directory,
and rendering HTML templates. Implements all required pages and business logic.
NOTE: The current data format for showtimes.txt does not include screen_id.
For seat selection and booking, we assume screen_id = '1' for all showtimes.
This is a simplification and may need adjustment if theaters have multiple screens.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'evomac_secret_key_for_flash_messages'  # Needed for flashing messages
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# Utility functions for reading and writing data files
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
                'facilities': parts[5].split(', ') if parts[5] else []
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
def generate_new_booking_id():
    bookings = read_bookings()
    if not bookings:
        return '1'
    max_id = max(int(b['booking_id']) for b in bookings)
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    movies = read_movies()
    # Featured movies: top 3 by rating, upcoming releases: release_date in future sorted ascending
    today_str = datetime.now().strftime('%Y-%m-%d')
    featured = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    upcoming = [m for m in movies if m['release_date'] > today_str]
    upcoming = sorted(upcoming, key=lambda m: m['release_date'])[:3]
    return render_template('dashboard.html',
                           page_title='Movie Ticketing Dashboard',
                           featured_movies=featured,
                           upcoming_releases=upcoming)
@app.route('/movies')
def movie_catalog():
    movies = read_movies()
    genres = get_genre_names()
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()
    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower() or search_query in m['genre'].lower()]
    if genre_filter and genre_filter != 'All':
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == genre_filter.lower()]
    return render_template('movie_catalog.html',
                           page_title='Movie Catalog',
                           movies=filtered_movies,
                           genres=['All'] + genres,
                           selected_genre=genre_filter,
                           search_query=search_query)
@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('movie_catalog'))
    return render_template('movie_details.html',
                           page_title='Movie Details',
                           movie=movie)
@app.route('/showtimes')
def showtime_selection():
    showtimes = read_showtimes()
    movies = {m['movie_id']: m for m in read_movies()}
    theaters = {t['theater_id']: t for t in read_theaters()}
    # Filters
    theater_filter = request.args.get('theater', '').strip()
    date_filter = request.args.get('date', '').strip()
    movie_filter = request.args.get('movie', '').strip()
    filtered_showtimes = showtimes
    if theater_filter and theater_filter != 'All':
        filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] == theater_filter]
    if date_filter:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == date_filter]
    if movie_filter and movie_filter != 'All':
        filtered_showtimes = [s for s in filtered_showtimes if s['movie_id'] == movie_filter]
    # Prepare showtimes with movie and theater info
    showtimes_display = []
    for s in filtered_showtimes:
        movie = movies.get(s['movie_id'])
        theater = theaters.get(s['theater_id'])
        if movie and theater:
            showtimes_display.append({
                'showtime_id': s['showtime_id'],
                'movie_title': movie['title'],
                'theater_name': theater['theater_name'],
                'showtime_date': s['showtime_date'],
                'showtime_time': s['showtime_time'],
                'price': s['price'],
                'available_seats': s['available_seats']
            })
    theater_options = ['All'] + [t['theater_id'] for t in theaters.values()]
    movie_options = ['All'] + [m['movie_id'] for m in movies.values()]
    # For dropdown display, map theater_id to name and movie_id to title
    theater_names = {t['theater_id']: t['theater_name'] for t in theaters.values()}
    movie_titles = {m['movie_id']: m['title'] for m in movies.values()}
    return render_template('showtime_selection.html',
                           page_title='Select Showtime',
                           showtimes=showtimes_display,
                           theater_filter=theater_filter or 'All',
                           date_filter=date_filter,
                           theater_options=theater_options,
                           theater_names=theater_names,
                           movie_filter=movie_filter or 'All',
                           movie_options=movie_options,
                           movie_titles=movie_titles)
@app.route('/select_seats/<showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('showtime_selection'))
    theater_id = showtime['theater_id']
    # NOTE: The current data format for showtimes.txt does not include screen_id.
    # For seat selection and booking, we assume screen_id = '1' for all showtimes.
    # This is a simplification and may need adjustment if theaters have multiple screens.
    screen_id = '1'
    seats = get_seats_by_theater_and_screen(theater_id, screen_id)
    # Build seat map: group seats by row, sorted by column
    seat_map = {}
    for seat in seats:
        row = seat['row']
        if row not in seat_map:
            seat_map[row] = []
        seat_map[row].append(seat)
    # Sort seats in each row by column (column is string, but likely numeric)
    for row in seat_map:
        try:
            seat_map[row].sort(key=lambda s: int(s['column']))
        except ValueError:
            seat_map[row].sort(key=lambda s: s['column'])
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            flash('Please select at least one seat.', 'error')
            return redirect(url_for('seat_selection', showtime_id=showtime_id))
        # Store selected seats in session or pass via query string or form
        # Since no session specified, we pass via POST redirect pattern using query parameters
        seats_str = ','.join(selected_seats)
        return redirect(url_for('confirm_booking', showtime_id=showtime_id, seats=seats_str))
    return render_template('seat_selection.html',
                           page_title='Select Seats',
                           showtime=showtime,
                           seat_map=seat_map)
@app.route('/confirm_booking', methods=['GET', 'POST'])
def confirm_booking():
    showtime_id = request.args.get('showtime_id') or request.form.get('showtime_id')
    seats_str = request.args.get('seats') or request.form.get('seats')
    if not showtime_id or not seats_str:
        flash('Missing showtime or seats information.', 'error')
        return redirect(url_for('dashboard'))
    selected_seats = seats_str.split(',')
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('dashboard'))
    movie = get_movie_by_id(showtime['movie_id'])
    theater = get_theater_by_id(showtime['theater_id'])
    # Calculate total price
    total_price = showtime['price'] * len(selected_seats)
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            flash('Please provide your name and email.', 'error')
            return redirect(url_for('confirm_booking', showtime_id=showtime_id, seats=seats_str))
        # Check seat availability again before booking
        seats = read_seats()
        # Find seats matching selected seats in this theater and screen
        # We assume screen_id = '1' as before
        theater_id = showtime['theater_id']
        screen_id = '1'
        seat_status_map = {}
        for seat in seats:
            if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
                seat_label = f"{seat['row']}{seat['column']}"
                seat_status_map[seat_label] = seat['status']
        for seat_label in selected_seats:
            if seat_status_map.get(seat_label) != 'Available':
                flash(f"Seat {seat_label} is no longer available.", 'error')
                return redirect(url_for('seat_selection', showtime_id=showtime_id))
        # Update seats status to Booked
        for seat in seats:
            seat_label = f"{seat['row']}{seat['column']}"
            if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id and seat_label in selected_seats:
                seat['status'] = 'Booked'
        write_seats(seats)
        # Update showtime available seats
        showtimes = read_showtimes()
        for s in showtimes:
            if s['showtime_id'] == showtime_id:
                s['available_seats'] = max(0, s['available_seats'] - len(selected_seats))
                break
        write_showtimes(showtimes)
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
        flash('Booking confirmed successfully!', 'success')
        return redirect(url_for('booking_history'))
    return render_template('booking_confirmation.html',
                           page_title='Booking Confirmation',
                           movie=movie,
                           theater=theater,
                           showtime=showtime,
                           selected_seats=selected_seats,
                           total_price=total_price,
                           seats_str=seats_str)
@app.route('/bookings')
def booking_history():
    status_filter = request.args.get('status', 'All')
    bookings = get_bookings_filtered(status_filter)
    showtimes = {s['showtime_id']: s for s in read_showtimes()}
    movies = {m['movie_id']: m for m in read_movies()}
    # Prepare bookings display data
    bookings_display = []
    for b in bookings:
        showtime = showtimes.get(b['showtime_id'])
        movie_title = movies.get(showtime['movie_id'])['title'] if showtime and showtime['movie_id'] in movies else 'Unknown'
        bookings_display.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status']
        })
    status_options = ['All', 'Confirmed', 'Cancelled', 'Completed']
    return render_template('booking_history.html',
                           page_title='Booking History',
                           bookings=bookings_display,
                           status_filter=status_filter,
                           status_options=status_options)
@app.route('/theaters')
def theater_information():
    theaters = read_theaters()
    location_filter = request.args.get('location', 'All')
    if location_filter != 'All':
        theaters = [t for t in theaters if t['city'] == location_filter]
    # Get unique locations for filter dropdown
    locations = sorted(set(t['city'] for t in read_theaters()))
    locations = ['All'] + locations
    return render_template('theater_information.html',
                           page_title='Theater Information',
                           theaters=theaters,
                           location_filter=location_filter,
                           locations=locations)
# Run the app on local port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)