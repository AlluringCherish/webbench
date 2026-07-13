from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to load data

def load_movies():
    movies = []
    path = os.path.join(DATA_DIR, 'movies.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 8:
                    continue
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
    return movies

def load_theaters():
    theaters = []
    path = os.path.join(DATA_DIR, 'theaters.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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
                    'facilities': parts[5]
                }
                theaters.append(theater)
    return theaters

def load_showtimes():
    showtimes = []
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                try:
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
                except:
                    continue
    return showtimes

def load_seats():
    seats = []
    path = os.path.join(DATA_DIR, 'seats.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                try:
                    seat = {
                        'seat_id': int(parts[0]),
                        'theater_id': int(parts[1]),
                        'screen_id': int(parts[2]),
                        'row': parts[3],
                        'column': int(parts[4]),
                        'seat_type': parts[5],
                        'status': parts[6]  # 'Available' or 'Booked'
                    }
                    seats.append(seat)
                except:
                    continue
    return seats

def load_bookings():
    bookings = []
    path = os.path.join(DATA_DIR, 'bookings.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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

def load_genres():
    genres = []
    path = os.path.join(DATA_DIR, 'genres.txt')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                line=line.strip()
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

# Save bookings

def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bookings:
            line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{','.join(b['seats_booked'])}"
            f.write(line + "\n")

# Save seats

def save_seats(seats):
    path = os.path.join(DATA_DIR, 'seats.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for s in seats:
            line = f"{s['seat_id']}|{s['theater_id']}|{s['screen_id']}|{s['row']}|{s['column']}|{s['seat_type']}|{s['status']}"
            f.write(line + "\n")

# Helpers for seat identification

def seat_code(row, col):
    return f"{row}{col}"

def seat_id_from_code(seat_code_str):
    # e.g. A1 -> row=A, col=1
    if len(seat_code_str) < 2:
        return None
    row = seat_code_str[0]
    try:
        col = int(seat_code_str[1:])
    except:
        return None
    return (row, col)

@app.route('/')
def dashboard():
    """Render the Dashboard page with featured movies and navigation."""
    movies = load_movies()
    # Featured movies are arbitrarily those with rating >= 8.5 and recent (let's say release_date >= 2010)
    featured_movies = [m for m in movies if m['rating'] >= 8.5]
    featured_movies = sorted(featured_movies, key=lambda x: x['rating'], reverse=True)[:5]
    return render_template('dashboard.html', featured_movies=featured_movies)

@app.route('/catalog')
def catalog():
    """Display movie catalog with search and genre filter."""
    movies = load_movies()
    genres = load_genres()

    # Get filters from request args
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()

    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower() or search_query in m['genre'].lower()]
    if genre_filter and genre_filter.lower() != 'all':
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == genre_filter.lower()]

    return render_template('catalog.html', movies=filtered_movies, genres=genres, selected_genre=genre_filter, search_query=search_query)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/showtimes/<int:movie_id>')
def showtimes(movie_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes = load_showtimes()

    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    # Filters
    theater_filter = request.args.get('theater', '').strip()
    date_filter = request.args.get('date', '').strip()

    filt_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if theater_filter and theater_filter.lower() != 'all':
        try:
            t_id = int(theater_filter)
            filt_showtimes = [s for s in filt_showtimes if s['theater_id'] == t_id]
        except:
            pass
    if date_filter:
        filt_showtimes = [s for s in filt_showtimes if s['showtime_date'] == date_filter]

    # Theater dictionary for name lookup
    theater_dict = {t['theater_id']: t for t in theaters}

    return render_template('showtimes.html', movie=movie, showtimes=filt_showtimes, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter, theater_dict=theater_dict)

@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes = load_showtimes()
    seats = load_seats()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    # Filter seats for this theater and screen id (assuming screen_id is 1, as not specified in showtimes)
    # Since showtimes.txt does not have screen_id, we must assume all seats are for screen_id=1 for showtime's theater
    screen_id = 1
    available_seats = [s for s in seats if s['theater_id'] == theater['theater_id'] and s['screen_id'] == screen_id]

    # Determine seat status overridden by bookings for this showtime
    bookings = load_bookings()
    booked_seats = []
    for b in bookings:
        if b['showtime_id'] == showtime_id and b['status'].lower() == 'confirmed':
            booked_seats.extend(b['seats_booked'])
    # Mark these seats as booked
    seat_status_map = {}
    for s in available_seats:
        seat_code_str = seat_code(s['row'], s['column'])
        seat_status_map[seat_code_str] = s['status']
    for bseat in booked_seats:
        seat_status_map[bseat] = 'Booked'

    # GET method: show seat map
    if request.method == 'GET':
        # Organize seats by row and sort by column
        rows = {}
        for s in available_seats:
            rows.setdefault(s['row'], []).append(s)
        for r in rows:
            rows[r].sort(key=lambda x: x['column'])
        sorted_rows = sorted(rows.items())
        return render_template('seat_selection.html', showtime=showtime, movie=movie, theater=theater,
                               seat_status_map=seat_status_map, rows=sorted_rows)
    else:
        # POST: no seat selection submission here, reservation is confirmed at /confirm-booking
        pass

@app.route('/confirm-booking', methods=['GET', 'POST'])
def confirm_booking():
    if request.method == 'GET':
        # Expect parameters: showtime_id, selected_seats comma joined
        showtime_id_str = request.args.get('showtime_id', '')
        selected_seats_str = request.args.get('selected_seats', '')
        if not showtime_id_str or not selected_seats_str:
            return redirect(url_for('dashboard'))
        try:
            showtime_id = int(showtime_id_str)
            selected_seats = [s.strip() for s in selected_seats_str.split(',') if s.strip()]
        except:
            return redirect(url_for('dashboard'))

        movies = load_movies()
        theaters = load_theaters()
        showtimes = load_showtimes()

        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if not showtime:
            return "Showtime not found", 404
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

        total_price = showtime['price'] * len(selected_seats)

        return render_template('booking_confirmation.html', showtime=showtime, movie=movie, theater=theater,
                               selected_seats=selected_seats, total_price=total_price)
    else:
        # POST: Process the booking submission
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        showtime_id = request.form.get('showtime_id', '')
        seats_selected = request.form.get('selected_seats', '')

        if not customer_name or not customer_email or not showtime_id or not seats_selected:
            return "All booking details are required.", 400

        try:
            showtime_id = int(showtime_id)
            seats_selected_list = [s.strip() for s in seats_selected.split(',') if s.strip()]
        except:
            return "Invalid data", 400

        # Load data
        bookings = load_bookings()
        seats = load_seats()
        showtimes = load_showtimes()

        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
        if not showtime:
            return "Showtime not found", 404

        # Check seat availability
        booked_seats = []
        for b in bookings:
            if b['showtime_id'] == showtime_id and b['status'].lower() == 'confirmed':
                booked_seats.extend(b['seats_booked'])
        for seat_code_ in seats_selected_list:
            if seat_code_ in booked_seats:
                return f"Seat {seat_code_} already booked", 400

        # Add new booking
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1

        booking_date = datetime.now().strftime('%Y-%m-%d')
        total_price = showtime['price'] * len(seats_selected_list)

        new_booking = {
            'booking_id': new_booking_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected_list
        }

        bookings.append(new_booking)

        # Update seats status is not required globally because seats.txt status is static, booking records track booking
        # Save bookings
        save_bookings(bookings)

        return redirect(url_for('booking_history'))

@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()

    # Get status filter
    status_filter = request.args.get('status', '').strip().lower()

    filtered_bookings = bookings
    if status_filter and status_filter != 'all':
        filtered_bookings = [b for b in bookings if b['status'].lower() == status_filter]

    # Create mapping movie_id to title
    movie_map = {m['movie_id']: m['title'] for m in movies}

    return render_template('booking_history.html', bookings=filtered_bookings, movie_map=movie_map, status_filter=status_filter)

@app.route('/theaters')
def theaters():
    theaters = load_theaters()

    # Filter by location
    location_filter = request.args.get('location', '').strip()

    filtered_theaters = theaters
    if location_filter and location_filter.lower() != 'all':
        filtered_theaters = [t for t in theaters if t['location'].lower() == location_filter.lower()]

    # Get distinct locations for dropdown
    locations = sorted(set(t['location'] for t in theaters))

    return render_template('theater_information.html', theaters=filtered_theaters, locations=locations, selected_location=location_filter)

# API endpoint to get seat availability status for a showtime
@app.route('/api/seats/<int:showtime_id>')
def api_seat_status(showtime_id):
    bookings = load_bookings()
    seats = load_seats()
    showtimes = load_showtimes()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return jsonify({'error': 'Showtime not found'}), 404

    theater_id = showtime['theater_id']
    screen_id = 1 # assumed

    available_seats = [s for s in seats if s['theater_id'] == theater_id and s['screen_id'] == screen_id]

    booked_seats = []
    for b in bookings:
        if b['showtime_id'] == showtime_id and b['status'].lower() == 'confirmed':
            booked_seats.extend(b['seats_booked'])

    seat_status_map = {}
    for s in available_seats:
        code = seat_code(s['row'], s['column'])
        seat_status_map[code] = 'Available'
    for bseat in booked_seats:
        seat_status_map[bseat] = 'Booked'

    return jsonify(seat_status_map)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
