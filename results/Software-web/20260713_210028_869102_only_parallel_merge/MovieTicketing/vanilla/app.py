from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkeyfortesting'

DATA_DIR = 'data'

# Utility functions for data loading and saving

def read_data_file(filename):
    path = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(path):
        return data
    with open(path, encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                data.append(line.split('|'))
    return data

def write_data_file(filename, data_lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for items in data_lines:
            f.write('|'.join(items) + '\n')

# Loading functions

def load_movies():
    raw = read_data_file('movies.txt')
    movies = []
    for m in raw:
        if len(m)<8:
            continue
        try:
            movies.append({
                'movie_id': int(m[0]),
                'title': m[1],
                'director': m[2],
                'genre': m[3],
                'rating': float(m[4]),
                'duration': int(m[5]),
                'description': m[6],
                'release_date': m[7]
            })
        except:
            continue
    return movies

def load_theaters():
    raw = read_data_file('theaters.txt')
    theaters = []
    for t in raw:
        if len(t)<6:
            continue
        try:
            theaters.append({
                'theater_id': int(t[0]),
                'theater_name': t[1],
                'location': t[2],
                'city': t[3],
                'screens': int(t[4]),
                'facilities': t[5]
            })
        except:
            continue
    return theaters

def load_showtimes():
    raw = read_data_file('showtimes.txt')
    showtimes = []
    for s in raw:
        if len(s)<7:
            continue
        try:
            showtimes.append({
                'showtime_id': int(s[0]),
                'movie_id': int(s[1]),
                'theater_id': int(s[2]),
                'showtime_date': s[3],
                'showtime_time': s[4],
                'price': float(s[5]),
                'available_seats': int(s[6])
            })
        except:
            continue
    return showtimes

def load_seats():
    raw = read_data_file('seats.txt')
    seats = []
    for s in raw:
        if len(s)<7:
            continue
        try:
            seats.append({
                'seat_id': int(s[0]),
                'theater_id': int(s[1]),
                'screen_id': int(s[2]),
                'row': s[3],
                'column': int(s[4]),
                'seat_type': s[5],
                'status': s[6]
            })
        except:
            continue
    return seats

def load_bookings():
    raw = read_data_file('bookings.txt')
    bookings = []
    for b in raw:
        if len(b)<8:
            continue
        try:
            seats_list = b[7].split(',') if b[7] else []
            bookings.append({
                'booking_id': int(b[0]),
                'showtime_id': int(b[1]),
                'customer_name': b[2],
                'customer_email': b[3],
                'booking_date': b[4],
                'total_price': float(b[5]),
                'status': b[6],
                'seats_booked': seats_list
            })
        except:
            continue
    return bookings

def load_genres():
    raw = read_data_file('genres.txt')
    genres = []
    for g in raw:
        if len(g)<3:
            continue
        try:
            genres.append({
                'genre_id': int(g[0]),
                'genre_name': g[1],
                'description': g[2]
            })
        except:
            continue
    return genres

def get_next_id(list_of_dicts, field):
    if not list_of_dicts:
        return 1
    return max(item[field] for item in list_of_dicts) + 1

# Saving functions

def save_bookings(bookings):
    lines = []
    for b in bookings:
        seats_str = ",".join(b['seats_booked']) if isinstance(b['seats_booked'], list) else b['seats_booked']
        lines.append([
            str(b['booking_id']),
            str(b['showtime_id']),
            b['customer_name'],
            b['customer_email'],
            b['booking_date'],
            f"{b['total_price']:.2f}",
            b['status'],
            seats_str
        ])
    write_data_file('bookings.txt', lines)

def save_seats(seats):
    lines = []
    for s in seats:
        lines.append([
            str(s['seat_id']),
            str(s['theater_id']),
            str(s['screen_id']),
            s['row'],
            str(s['column']),
            s['seat_type'],
            s['status']
        ])
    write_data_file('seats.txt', lines)

# Helper seat code functions

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

# ROUTES

@app.route('/')
def dashboard():
    movies = load_movies()
    # Combined criteria: featured = top 3 latest release_date descending OR top 5 rating >= 8.5
    latest_featured = sorted(movies, key=lambda m: m['release_date'], reverse=True)[:3]
    rating_featured = sorted([m for m in movies if m['rating'] >= 8.5], key=lambda m: m['rating'], reverse=True)[:5]
    # Merge unique by movie_id
    featured_dict = {}
    for m in latest_featured + rating_featured:
        featured_dict[m['movie_id']] = m
    featured = list(featured_dict.values())
    return render_template('dashboard.html', featured_movies=featured)

@app.route('/catalog')
def catalog():
    movies = load_movies()
    genres = load_genres()
    # Use parameter names from spec: search, genre
    search = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', '').strip()

    filtered = movies
    if search:
        filtered = [m for m in filtered if search in m['title'].lower() or search in m['genre'].lower()]
    if genre_filter and genre_filter.lower() != 'all':
        filtered = [m for m in filtered if m['genre'].lower() == genre_filter.lower()]

    return render_template('catalog.html', movies=filtered, genres=genres, search_query=search, selected_genre=genre_filter)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id']==movie_id), None)
    if not movie:
        flash('Movie not found.')
        return redirect(url_for('catalog'))
    return render_template('movie_details.html', movie=movie)

@app.route('/showtimes/<int:movie_id>')
def showtimes(movie_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes = load_showtimes()

    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        flash('Movie not found.')
        return redirect(url_for('catalog'))

    theater_filter = request.args.get('theater', '').strip()
    date_filter = request.args.get('date', '').strip()

    filtered = [s for s in showtimes if s['movie_id'] == movie_id]

    if theater_filter and theater_filter.lower() != 'all':
        try:
            t_id = int(theater_filter)
            filtered = [s for s in filtered if s['theater_id'] == t_id]
        except:
            pass
    if date_filter:
        filtered = [s for s in filtered if s['showtime_date'] == date_filter]

    theater_dict = {t['theater_id']: t for t in theaters}

    return render_template('showtimes.html', movie=movie, showtimes=filtered, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter, theater_dict=theater_dict)

@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        flash('Showtime not found.')
        return redirect(url_for('dashboard'))

    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        flash('Theater not found.')
        return redirect(url_for('dashboard'))

    seats_all = load_seats()
    screen_id = 1
    available_seats = [s for s in seats_all if s['theater_id'] == theater['theater_id'] and s['screen_id'] == screen_id]

    bookings = load_bookings()
    booked_seats = []
    for b in bookings:
        if b['showtime_id'] == showtime_id and b['status'].lower() == 'confirmed':
            booked_seats.extend(b['seats_booked'])

    seat_status_map = {}
    for s in available_seats:
        seat_code_str = seat_code(s['row'], s['column'])
        seat_status_map[seat_code_str] = s['status']
    for bs in booked_seats:
        seat_status_map[bs] = 'Booked'

    if request.method == 'GET':
        rows = {}
        for s in available_seats:
            rows.setdefault(s['row'], []).append(s)
        for r in rows:
            rows[r].sort(key=lambda x: x['column'])
        sorted_rows = sorted(rows.keys())

        # Convert rows dict with lists to use in template with key list separately
        return render_template('seat_selection.html', showtime=showtime, movie=next((m for m in load_movies() if m['movie_id'] == showtime['movie_id']), None), theater=theater, seat_status_map=seat_status_map, rows=sorted_rows, seat_map=rows)
    else:
        # POST not implemented, handled via confirm booking
        flash('Invalid request method.')
        return redirect(url_for('dashboard'))

@app.route('/confirm-booking', methods=['GET', 'POST'])
def confirm_booking():
    if request.method == 'GET':
        showtime_id = request.args.get('showtime_id')
        seats = request.args.get('seats', '') or request.args.get('selected_seats', '')
        if not showtime_id or not seats:
            flash('Booking info missing. Please select seats first.')
            return redirect(url_for('dashboard'))
        try:
            showtime_id_int = int(showtime_id)
        except:
            flash('Invalid showtime.')
            return redirect(url_for('dashboard'))

        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id_int), None)
        if not showtime:
            flash('Showtime not found.')
            return redirect(url_for('dashboard'))

        movies = load_movies()
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        theaters = load_theaters()
        theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

        seats_list = seats.split(',')
        seats_list = [s.strip() for s in seats_list if s.strip()]

        total_price = showtime['price'] * len(seats_list)

        return render_template('confirm_booking.html', showtime=showtime, movie=movie, theater=theater, selected_seats=seats_list, total_price=total_price)

    else:
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        showtime_id = request.form.get('showtime_id', '')
        seats_selected = request.form.get('selected_seats', '')

        if not customer_name or not customer_email or not showtime_id or not seats_selected:
            flash('All booking details are required.')
            return redirect(request.url)

        try:
            showtime_id_int = int(showtime_id)
            seats_selected_list = [s.strip() for s in seats_selected.split(',') if s.strip()]
        except:
            flash('Invalid data.')
            return redirect(url_for('dashboard'))

        bookings = load_bookings()
        seats = load_seats()
        showtimes = load_showtimes()

        showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id_int), None)
        if not showtime:
            flash('Showtime not found.')
            return redirect(url_for('dashboard'))

        # Check if seats are already booked in bookings
        booked_seats = []
        for b in bookings:
            if b['showtime_id'] == showtime_id_int and b['status'].lower() == 'confirmed':
                booked_seats.extend(b['seats_booked'])
        for seat_code_ in seats_selected_list:
            if seat_code_ in booked_seats:
                flash(f'Seat {seat_code_} is already booked.')
                return redirect(url_for('seat_selection', showtime_id=showtime_id_int))

        next_booking_id = get_next_id(bookings, 'booking_id')
        booking_date = datetime.now().strftime('%Y-%m-%d')
        total_price = showtime['price'] * len(seats_selected_list)

        new_booking = {
            'booking_id': next_booking_id,
            'showtime_id': showtime_id_int,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected_list
        }

        bookings.append(new_booking)

        # Update seats.txt status for booked seats
        for seat in seats:
            seat_code_str = seat_code(seat['row'], seat['column'])
            if seat['theater_id'] == showtime['theater_id'] and seat_code_str in seats_selected_list:
                seat['status'] = 'Booked'
        save_seats(seats)
        save_bookings(bookings)

        flash('Booking confirmed!')
        return redirect(url_for('dashboard'))

@app.route('/bookings')
def bookings():
    bookings_data = load_bookings()
    movies = load_movies()
    showtimes = load_showtimes()
    movie_dict = {m['movie_id']: m for m in movies}
    showtime_dict = {s['showtime_id']: s for s in showtimes}

    status_filter = request.args.get('status_filter', '').lower()
    filtered = bookings_data
    if status_filter and status_filter != 'all':
        filtered = [b for b in bookings_data if b['status'].lower() == status_filter]

    return render_template('bookings.html', bookings=filtered, movie_dict=movie_dict, showtime_dict=showtime_dict, status_filter=status_filter)

@app.route('/theaters')
def theaters():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter', '').strip()
    filtered = theaters
    if location_filter:
        filtered = [t for t in theaters if location_filter.lower() in (t['location'].lower() + ' ' + t['city'].lower())]

    locations = sorted(set([t['location'] for t in theaters] + [t['city'] for t in theaters]))

    facilities_display = ''
    if len(filtered) == 1:
        facilities_display = filtered[0]['facilities']

    return render_template('theaters.html', theaters=filtered, locations=locations, location_filter=location_filter, facilities_display=facilities_display)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
