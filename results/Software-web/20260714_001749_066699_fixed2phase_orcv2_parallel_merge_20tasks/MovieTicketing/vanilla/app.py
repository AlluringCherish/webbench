from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import os
import threading

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # For development convenience

# Data file paths
MOVIES_FILE = 'movies.txt'
THEATERS_FILE = 'theaters.txt'
SHOWTIMES_FILE = 'showtimes.txt'
SEATS_FILE = 'seats.txt'
BOOKINGS_FILE = 'bookings.txt'
GENRES_FILE = 'genres.txt'

file_lock = threading.Lock()  # To handle concurrent file writes

# Utility functions for file I/O and data parsing

def parse_pipe_delimited(line, fields_num=None):
    parts = line.strip().split('|')
    if fields_num is not None and len(parts) != fields_num:
        return None
    return parts

def read_movies():
    movies = []
    if not os.path.exists(MOVIES_FILE):
        return movies
    with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 8)
            if parts:
                movie = {
                    'movie_id': int(parts[0]),
                    'title': parts[1],
                    'director': parts[2],
                    'genre': parts[3],
                    'rating': parts[4],
                    'duration': parts[5],
                    'description': parts[6],
                    'release_date': parts[7],
                    'poster_url': f'/static/posters/{parts[0]}.jpg'  # convention for posters
                }
                movies.append(movie)
    return movies

def read_theaters():
    theaters = []
    if not os.path.exists(THEATERS_FILE):
        return theaters
    with open(THEATERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 6)
            if parts:
                theater = {
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': parts[4],
                    'facilities': parts[5].split(',') if parts[5] else []
                }
                theaters.append(theater)
    return theaters

def read_genres():
    genres = []
    if not os.path.exists(GENRES_FILE):
        return genres
    with open(GENRES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 3)
            if parts:
                genre_name = parts[1]
                genres.append(genre_name)
    return genres

def read_showtimes():
    showtimes = []
    if not os.path.exists(SHOWTIMES_FILE):
        return showtimes
    with open(SHOWTIMES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 7)
            if parts:
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
                except ValueError:
                    continue
    return showtimes

def read_seats():
    seats = []
    if not os.path.exists(SEATS_FILE):
        return seats
    with open(SEATS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 7)
            if parts:
                seat = {
                    'seat_id': parts[0],
                    'theater_id': int(parts[1]),
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
    if not os.path.exists(BOOKINGS_FILE):
        return bookings
    with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = parse_pipe_delimited(line, 8)
            if parts:
                try:
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
                except ValueError:
                    continue
    return bookings

def write_showtimes(showtimes):
    with file_lock:
        with open(SHOWTIMES_FILE, 'w', encoding='utf-8') as f:
            for s in showtimes:
                line = f"{s['showtime_id']}|{s['movie_id']}|{s['theater_id']}|{s['showtime_date']}|{s['showtime_time']}|{s['price']}|{s['available_seats']}\n"
                f.write(line)

def write_bookings(bookings):
    with file_lock:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats_booked'])
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
                f.write(line)

def generate_new_booking_id(bookings):
    if not bookings:
        return 1
    return max(b['booking_id'] for b in bookings) + 1

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

### Route Implementations ###

@app.route('/dashboard', methods=['GET'])
def dashboard():
    movies = read_movies()
    featured_movies = movies[:5]
    featured_movies_context = [{'movie_id': m['movie_id'], 'title': m['title'], 'poster_url': m['poster_url']} for m in featured_movies]
    return render_template('dashboard.html', featured_movies=featured_movies_context)

@app.route('/movies', methods=['GET'])
def movie_catalog():
    search_query = request.args.get('search', '').strip()
    selected_genre = request.args.get('genre', '').strip()
    movies = read_movies()
    genres = read_genres()
    filtered_movies = []
    for m in movies:
        matches_search = True
        if search_query:
            sq = search_query.lower()
            if sq not in m['title'].lower() and sq not in m['genre'].lower():
                matches_search = False
        matches_genre = True
        if selected_genre and selected_genre.lower() != 'all':
            if m['genre'].lower() != selected_genre.lower():
                matches_genre = False
        if matches_search and matches_genre:
            filtered_movies.append(m)
    movies_context = [{'movie_id': m['movie_id'], 'title': m['title'], 'poster_url': m['poster_url'],
                       'rating': m['rating'], 'duration': m['duration'], 'genre': m['genre']} for m in filtered_movies]
    genres_dropdown = ['All'] + genres if genres else []
    return render_template('movie_catalog.html', movies=movies_context, genres=genres_dropdown,
                           search_query=search_query, selected_genre=selected_genre)

@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/showtimes/<int:movie_id>', methods=['GET'])
def showtime_selection(movie_id):
    theater_id = request.args.get('theater_id')
    date = request.args.get('date')
    showtimes = read_showtimes()
    theaters = read_theaters()
    filtered_showtimes = []
    for s in showtimes:
        if s['movie_id'] != movie_id:
            continue
        if theater_id:
            try:
                if s['theater_id'] != int(theater_id):
                    continue
            except ValueError:
                pass
        if date:
            if s['showtime_date'] != date:
                continue
        theater = get_theater_by_id(s['theater_id'])
        theater_name = theater['theater_name'] if theater else 'Unknown'
        showtime_obj = {
            'showtime_id': s['showtime_id'],
            'movie_id': s['movie_id'],
            'theater_name': theater_name,
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price'],
            'available_seats': s['available_seats']
        }
        filtered_showtimes.append(showtime_obj)
    movie = get_movie_by_id(movie_id)
    return render_template('showtime_selection.html', showtimes=filtered_showtimes, theaters=theaters,
                           selected_theater_id=int(theater_id) if theater_id and theater_id.isdigit() else None,
                           selected_date=date,
                           movie=movie)

@app.route('/seats/<int:showtime_id>', methods=['GET'])
def seat_selection(showtime_id):
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        return "Showtime not found", 404
    theater_id = showtime['theater_id']
    seats = read_seats()
    bookings = read_bookings()
    theater_seats = [seat for seat in seats if seat['theater_id'] == theater_id]
    booked_seat_ids = set()
    for booking in bookings:
        if booking['showtime_id'] == showtime_id and booking['status'].lower() == 'confirmed':
            booked_seat_ids.update(booking['seats_booked'])
    seats_context = []
    for seat in theater_seats:
        seat_status = 'Available'
        if seat['seat_id'] in booked_seat_ids:
            seat_status = 'Booked'
        else:
            if seat['status'].lower() != 'available':
                seat_status = 'Booked'
        seat_info = {
            'seat_id': seat['seat_id'],
            'row': seat['row'],
            'column': seat['column'],
            'seat_type': seat['seat_type'],
            'status': seat_status
        }
        seats_context.append(seat_info)
    selected_seats = []
    return render_template('seat_selection.html', showtime=showtime, seats=seats_context, selected_seats=selected_seats)

@app.route('/bookings/confirm', methods=['POST'])
def booking_confirmation():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    showtime_id = data.get('showtime_id')
    customer_name = data.get('customer_name', '').strip()
    customer_email = data.get('customer_email', '').strip()
    selected_seats_csv = data.get('seats', '')
    if not showtime_id or not customer_name or not customer_email or not selected_seats_csv:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        showtime_id = int(showtime_id)
    except ValueError:
        return jsonify({'error': 'Invalid showtime_id'}), 400
    selected_seats = [s.strip() for s in selected_seats_csv.split(',') if s.strip()]
    if not selected_seats:
        return jsonify({'error': 'No seats selected'}), 400
    showtime = get_showtime_by_id(showtime_id)
    if not showtime:
        return jsonify({'error': 'Showtime not found'}), 404
    bookings = read_bookings()
    seats = read_seats()
    theater_id = showtime['theater_id']
    booked_seat_ids = set()
    for booking in bookings:
        if booking['showtime_id'] == showtime_id and booking['status'].lower() == 'confirmed':
            booked_seat_ids.update(booking['seats_booked'])
    theater_seat_ids = set([seat['seat_id'] for seat in seats if seat['theater_id'] == theater_id])
    for seat in selected_seats:
        if seat not in theater_seat_ids:
            return jsonify({'error': f'Seat {seat} does not exist'}), 400
        if seat in booked_seat_ids:
            return jsonify({'error': f'Seat {seat} is already booked'}), 400
    total_price = round(showtime['price'] * len(selected_seats), 2)
    new_booking_id = generate_new_booking_id(bookings)
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
    showtimes = read_showtimes()
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            s['available_seats'] = max(0, s['available_seats'] - len(selected_seats))
            break
    write_showtimes(showtimes)
    movie = get_movie_by_id(showtime['movie_id'])
    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, selected_seats=selected_seats, total_price=total_price)

@app.route('/bookings', methods=['GET'])
def booking_history():
    status_filter = request.args.get('status', 'All')
    bookings = read_bookings()
    movies = {m['movie_id']: m['title'] for m in read_movies()}
    status_options = ['All', 'Confirmed', 'Cancelled', 'Completed']
    status_filter = status_filter if status_filter in status_options else 'All'
    filtered_bookings = []
    for b in bookings:
        if status_filter != 'All' and b['status'] != status_filter:
            continue
        filtered_bookings.append({
            'booking_id': b['booking_id'],
            'movie_title': movies.get(get_showtime_by_id(b['showtime_id'])['movie_id'], 'Unknown') if get_showtime_by_id(b['showtime_id']) else 'Unknown',
            'booking_date': b['booking_date'],
            'seats_booked': ','.join(b['seats_booked']),
            'status': b['status']
        })
    return render_template('booking_history.html', bookings=filtered_bookings, status_options=status_options, selected_status=status_filter)

@app.route('/theaters', methods=['GET'])
def theater_information():
    location_filter = request.args.get('location', '').strip()
    theaters = read_theaters()
    filtered_theaters = [t for t in theaters if not location_filter or t['city'].lower() == location_filter.lower()]
    locations = sorted(set(t['city'] for t in theaters))
    return render_template('theater_information.html', theaters=filtered_theaters, locations=locations, selected_location=location_filter)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
