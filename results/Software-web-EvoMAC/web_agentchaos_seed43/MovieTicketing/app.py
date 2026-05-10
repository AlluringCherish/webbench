'''
Backend implementation for the 'MovieTicketing' web application.
- Uses Flask to serve pages and handle routing.
- Reads and writes data from/to local text files in 'data' directory.
- Provides data to frontend templates for all 8 pages.
- Runs on local port 5000 with '/' route serving the Dashboard page.
- Added dedicated /showtimes route to display all upcoming showtimes across movies and theaters,
  with filtering options by theater and date, fulfilling the requirement for a distinct showtime selection page.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'evomac_secret_key_for_sessions'
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
def generate_new_booking_id():
    bookings = read_bookings()
    if not bookings:
        return '1'
    max_id = max(int(b['booking_id']) for b in bookings)
    return str(max_id + 1)
def update_showtime_available_seats(showtime_id, seats_booked_count):
    showtimes = read_showtimes()
    updated = False
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            s['available_seats'] = max(0, s['available_seats'] - seats_booked_count)
            updated = True
            break
    if updated:
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
def update_seat_statuses(theater_id, screen_id, seats_to_book):
    seats = read_seats()
    updated = False
    for seat in seats:
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
            seat_label = f"{seat['row']}{seat['column']}"
            if seat_label in seats_to_book and seat['status'] == 'Available':
                seat['status'] = 'Booked'
                updated = True
    if updated:
        path = os.path.join(DATA_DIR, 'seats.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for seat in seats:
                line = '|'.join([
                    seat['seat_id'],
                    seat['theater_id'],
                    seat['screen_id'],
                    seat['row'],
                    seat['column'],
                    seat['seat_type'],
                    seat['status']
                ])
                f.write(line + '\n')
# Routes
@app.route('/')
def dashboard():
    movies = read_movies()
    # Featured movies: top 3 by rating descending
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    # Upcoming releases: movies with release_date in future (>= today)
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming = [m for m in movies if m['release_date'] >= today_str]
    upcoming = sorted(upcoming, key=lambda m: m['release_date'])[:3]
    return render_template('dashboard.html',
                           featured_movies=featured_movies,
                           upcoming_releases=upcoming)
@app.route('/movies')
def movie_catalog():
    movies = read_movies()
    genres = read_genres()
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()
    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower() or search_query in m['genre'].lower()]
    if genre_filter and genre_filter != 'All':
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == genre_filter.lower()]
    return render_template('movie_catalog.html',
                           movies=filtered_movies,
                           genres=genres,
                           selected_genre=genre_filter,
                           search_query=search_query)
@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('movie_catalog'))
    return render_template('movie_details.html', movie=movie)
@app.route('/showtimes/<movie_id>', methods=['GET', 'POST'])
def showtime_selection(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found.', 'error')
        return redirect(url_for('movie_catalog'))
    showtimes = read_showtimes()
    theaters = read_theaters()
    # Filter showtimes for this movie
    showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    theater_filter = request.args.get('theater', '').strip()
    date_filter = request.args.get('date', '').strip()
    if theater_filter and theater_filter != 'All':
        # Find theater_id by name
        theater_ids = [t['theater_id'] for t in theaters if t['theater_name'] == theater_filter]
        if theater_ids:
            showtimes = [s for s in showtimes if s['theater_id'] in theater_ids]
        else:
            showtimes = []
    if date_filter:
        showtimes = [s for s in showtimes if s['showtime_date'] == date_filter]
    # Prepare theater names for dropdown
    theater_names = sorted(set(t['theater_name'] for t in theaters))
    return render_template('showtime_selection.html',
                           movie=movie,
                           showtimes=showtimes,
                           theaters=theater_names,
                           selected_theater=theater_filter,
                           selected_date=date_filter)
@app.route('/showtimes', methods=['GET', 'POST'])
def showtimes_overview():
    showtimes = read_showtimes()
    theaters = read_theaters()
    movies = {m['movie_id']: m for m in read_movies()}
    theater_filter = request.args.get('theater', '').strip()
    date_filter = request.args.get('date', '').strip()
    # Filter upcoming showtimes only (date >= today)
    today_str = datetime.now().strftime('%Y-%m-%d')
    showtimes = [s for s in showtimes if s['showtime_date'] >= today_str]
    if theater_filter and theater_filter != 'All':
        # Find theater_id by name
        theater_ids = [t['theater_id'] for t in theaters if t['theater_name'] == theater_filter]
        if theater_ids:
            showtimes = [s for s in showtimes if s['theater_id'] in theater_ids]
        else:
            showtimes = []
    if date_filter:
        showtimes = [s for s in showtimes if s['showtime_date'] == date_filter]
    # Prepare theater names for dropdown
    theater_names = sorted(set(t['theater_name'] for t in theaters))
    # Enrich showtimes with movie title and theater name
    enriched_showtimes = []
    for s in showtimes:
        movie_title = movies.get(s['movie_id'], {}).get('title', '')
        theater_name = next((t['theater_name'] for t in theaters if t['theater_id'] == s['theater_id']), '')
        enriched_showtimes.append({
            'showtime_id': s['showtime_id'],
            'movie_title': movie_title,
            'theater_name': theater_name,
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price'],
            'available_seats': s['available_seats']
        })
    return render_template('showtimes_overview.html',
                           showtimes=enriched_showtimes,
                           theaters=theater_names,
                           selected_theater=theater_filter,
                           selected_date=date_filter)
@app.route('/seats/<showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('dashboard'))
    movie = get_movie_by_id(showtime['movie_id'])
    theater = get_theater_by_id(showtime['theater_id'])
    if not movie or not theater:
        flash('Related movie or theater not found.', 'error')
        return redirect(url_for('dashboard'))
    # For seat map, we need seats for this theater and screen
    # Note: screen_id is not provided in showtimes.txt, assume screen_id = '1' for simplicity
    screen_id = '1'
    seats = get_seats_by_theater_and_screen(theater['theater_id'], screen_id)
    # Build seat map structure: rows and columns
    seat_map = {}
    rows = sorted(set(s['row'] for s in seats))
    cols = sorted(set(int(s['column']) for s in seats))
    for r in rows:
        seat_map[r] = {}
        for c in cols:
            seat_map[r][str(c)] = None
    for s in seats:
        seat_map[s['row']][s['column']] = s
    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            flash('Please select at least one seat.', 'error')
            return render_template('seat_selection.html',
                                   showtime=showtime,
                                   movie=movie,
                                   theater=theater,
                                   seat_map=seat_map,
                                   selected_seats=[])
        # Redirect to booking confirmation with selected seats as query param
        seats_str = ','.join(selected_seats)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=seats_str))
    return render_template('seat_selection.html',
                           showtime=showtime,
                           movie=movie,
                           theater=theater,
                           seat_map=seat_map,
                           selected_seats=[])
@app.route('/booking_confirmation/<showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        flash('Showtime not found.', 'error')
        return redirect(url_for('dashboard'))
    movie = get_movie_by_id(showtime['movie_id'])
    theater = get_theater_by_id(showtime['theater_id'])
    if not movie or not theater:
        flash('Related movie or theater not found.', 'error')
        return redirect(url_for('dashboard'))
    seats_str = request.args.get('seats', '')
    selected_seats = seats_str.split(',') if seats_str else []
    if not selected_seats:
        flash('No seats selected.', 'error')
        return redirect(url_for('seat_selection', showtime_id=showtime_id))
    total_price = len(selected_seats) * showtime['price']
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            flash('Please enter your name and email.', 'error')
            return render_template('booking_confirmation.html',
                                   showtime=showtime,
                                   movie=movie,
                                   theater=theater,
                                   selected_seats=selected_seats,
                                   total_price=total_price,
                                   customer_name=customer_name,
                                   customer_email=customer_email)
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
        # Update showtime available seats
        update_showtime_available_seats(showtime_id, len(selected_seats))
        # Update seat statuses
        update_seat_statuses(theater['theater_id'], '1', selected_seats)
        flash('Booking confirmed! Thank you for your purchase.', 'success')
        return redirect(url_for('booking_history'))
    return render_template('booking_confirmation.html',
                           showtime=showtime,
                           movie=movie,
                           theater=theater,
                           selected_seats=selected_seats,
                           total_price=total_price,
                           customer_name='',
                           customer_email='')
@app.route('/bookings')
def booking_history():
    status_filter = request.args.get('status', 'All')
    bookings = get_bookings_filtered(status_filter)
    movies = {m['movie_id']: m for m in read_movies()}
    # Enrich bookings with movie title and showtime date
    showtimes = {s['showtime_id']: s for s in read_showtimes()}
    enriched_bookings = []
    for b in bookings:
        movie_title = ''
        showtime_date = ''
        if b['showtime_id'] in showtimes:
            st = showtimes[b['showtime_id']]
            movie_title = movies.get(st['movie_id'], {}).get('title', '')
            showtime_date = f"{st['showtime_date']} {st['showtime_time']}"
        enriched_bookings.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'seats_booked': ','.join(b['seats_booked']),
            'status': b['status']
        })
    status_options = ['All', 'Confirmed', 'Cancelled', 'Completed']
    return render_template('booking_history.html',
                           bookings=enriched_bookings,
                           status_filter=status_filter,
                           status_options=status_options)
@app.route('/bookings/<booking_id>')
def booking_details(booking_id):
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
@app.route('/theaters')
def theater_information():
    theaters = read_theaters()
    location_filter = request.args.get('location', '').strip()
    if location_filter and location_filter != 'All':
        theaters = [t for t in theaters if t['city'].lower() == location_filter.lower()]
    locations = sorted(set(t['city'] for t in read_theaters()))
    return render_template('theater_information.html',
                           theaters=theaters,
                           locations=locations,
                           selected_location=location_filter)
# Navigation buttons redirect routes
@app.route('/dashboard')
def redirect_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/browse_movies')
def redirect_browse_movies():
    return redirect(url_for('movie_catalog'))
@app.route('/view_bookings')
def redirect_view_bookings():
    return redirect(url_for('booking_history'))
@app.route('/showtimes')
def redirect_showtimes():
    # Redirect to dedicated showtimes overview page
    return redirect(url_for('showtimes_overview'))
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)