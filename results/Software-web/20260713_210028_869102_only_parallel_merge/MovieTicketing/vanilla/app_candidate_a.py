from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkeyfortesting'

DATA_DIR = 'data'

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

# ROUTES

@app.route('/')
def dashboard():
    movies = load_movies()
    # Featured: 3 most recent by release_date descending
    featured = sorted(movies, key=lambda m: m['release_date'], reverse=True)[:3]
    return render_template('dashboard.html', featured_movies=featured)

@app.route('/catalog')
def catalog():
    movies = load_movies()
    genres = load_genres()
    search = request.args.get('search','').strip().lower()
    genre_filter = request.args.get('genre_filter','')

    filtered = movies
    if search:
        filtered = [m for m in filtered if search in m['title'].lower() or search in m['genre'].lower()]
    if genre_filter:
        filtered = [m for m in filtered if m['genre'].lower() == genre_filter.lower()]

    return render_template('catalog.html', movies=filtered, genres=genres, search=search, genre_filter=genre_filter)

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
    showtimes = load_showtimes()
    theaters = load_theaters()
    theater_filter = request.args.get('theater_filter','')
    date_filter = request.args.get('date_filter','')

    filtered = [s for s in showtimes if s['movie_id']==movie_id]

    if theater_filter:
        try:
            theater_id_filter = int(theater_filter)
            filtered = [s for s in filtered if s['theater_id']==theater_id_filter]
        except:
            pass

    if date_filter:
        filtered = [s for s in filtered if s['showtime_date']==date_filter]

    theater_dict = {t['theater_id']: t for t in theaters}
    return render_template('showtimes.html', showtimes=filtered,
                           theaters=theaters,
                           theater_filter=theater_filter,
                           date_filter=date_filter,
                           theater_dict=theater_dict,
                           movie_id=movie_id)

@app.route('/seats/<int:showtime_id>', methods=['GET','POST'])
def seats(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id']==showtime_id), None)
    if not showtime:
        flash("Showtime not found.")
        return redirect(url_for('dashboard'))

    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id']==showtime['theater_id']), None)
    if not theater:
        flash("Theater not found.")
        return redirect(url_for('dashboard'))

    seats_all = load_seats()
    theater_seats = [s for s in seats_all if s['theater_id']==theater['theater_id']]
    # Group seats by row, sorted by column:
    seat_map = {}
    for s in theater_seats:
        seat_map.setdefault(s['row'], []).append(s)
    for r in seat_map:
        seat_map[r].sort(key=lambda x: x['column'])
    sorted_rows = sorted(seat_map.keys())

    if request.method == 'POST':
        selected_seats = request.form.get('selected_seats','')
        if not selected_seats:
            flash("Please select at least one seat.")
            return redirect(url_for('seats', showtime_id=showtime_id))
        seats_list = selected_seats.split(',')
        # Validate seats availability
        booked_seat_codes = {seat['row']+str(seat['column']) for seat in seats_all if seat['status'].lower()=='booked' and seat['theater_id']==theater['theater_id']}
        for seat_code in seats_list:
            if seat_code in booked_seat_codes:
                flash(f"Seat {seat_code} is already booked.")
                return redirect(url_for('seats', showtime_id=showtime_id))
        # Redirect to confirm booking with params
        return redirect(url_for('confirm_booking', showtime_id=showtime_id, seats=selected_seats))

    return render_template('seats.html', showtime=showtime, theater=theater,
                           seat_map=seat_map, rows=sorted_rows)

@app.route('/confirm-booking', methods=['GET','POST'])
def confirm_booking():
    if request.method == 'GET':
        showtime_id = request.args.get('showtime_id')
        seats = request.args.get('seats','')
        if not showtime_id or not seats:
            flash("Booking info missing. Please select seats first.")
            return redirect(url_for('dashboard'))
        try:
            showtime_id_int = int(showtime_id)
        except:
            flash("Invalid showtime.")
            return redirect(url_for('dashboard'))

        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id']==showtime_id_int), None)
        if not showtime:
            flash("Showtime not found.")
            return redirect(url_for('dashboard'))

        movies = load_movies()
        movie = next((m for m in movies if m['movie_id']==showtime['movie_id']), None)
        if not movie:
            flash('Movie not found.')
            return redirect(url_for('dashboard'))

        seats_list = seats.split(',')
        return render_template('confirm_booking.html',
                               showtime=showtime,
                               movie=movie,
                               seats=seats_list)

    elif request.method == 'POST':
        showtime_id = request.form.get('showtime_id')
        seats = request.form.get('seats')
        customer_name = request.form.get('customer_name','').strip()
        customer_email = request.form.get('customer_email','').strip()

        if not (showtime_id and seats and customer_name and customer_email):
            flash("All fields are required.")
            return redirect(request.url)

        try:
            showtime_id_int = int(showtime_id)
        except:
            flash("Invalid showtime.")
            return redirect(url_for('dashboard'))

        seats_list = seats.split(',')

        showtimes = load_showtimes()
        showtime = next((s for s in showtimes if s['showtime_id']==showtime_id_int), None)
        if not showtime:
            flash("Showtime not found.")
            return redirect(url_for('dashboard'))

        # Check seats availability to avoid double booking
        seats_all = load_seats()
        theater_id = showtime['theater_id']
        booked_seats_set = {s['row']+str(s['column']) for s in seats_all if s['theater_id']==theater_id and s['status'].lower() == 'booked'}
        for seat_code in seats_list:
            if seat_code in booked_seats_set:
                flash(f"Seat {seat_code} is already booked.")
                return redirect(url_for('seats', showtime_id=showtime_id_int))

        bookings = load_bookings()
        next_booking_id = get_next_id(bookings, 'booking_id')
        booking_date = datetime.now().strftime('%Y-%m-%d')
        total_price = showtime['price'] * len(seats_list)

        # Add new booking record
        bookings.append({
            'booking_id': next_booking_id,
            'showtime_id': showtime_id_int,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats
        })

        # Write bookings back
        lines = []
        for b in bookings:
            lines.append([
                str(b['booking_id']),
                str(b['showtime_id']),
                b['customer_name'],
                b['customer_email'],
                b['booking_date'],
                f"{b['total_price']:.2f}",
                b['status'],
                b['seats_booked']
            ])
        write_data_file('bookings.txt', lines)

        # Update seats.txt to mark selected seats booked
        for seat in seats_all:
            seat_code = seat['row'] + str(seat['column'])
            if seat['theater_id'] == theater_id and seat_code in seats_list:
                seat['status'] = 'Booked'
        seat_lines = []
        for s in seats_all:
            seat_lines.append([
                str(s['seat_id']),
                str(s['theater_id']),
                str(s['screen_id']),
                s['row'],
                str(s['column']),
                s['seat_type'],
                s['status']
            ])
        write_data_file('seats.txt', seat_lines)

        flash("Booking confirmed!")
        return redirect(url_for('dashboard'))

@app.route('/bookings')
def bookings():
    bookings = load_bookings()
    movies = load_movies()
    showtimes = load_showtimes()
    movie_dict = {m['movie_id']: m for m in movies}
    showtime_dict = {s['showtime_id']: s for s in showtimes}

    status_filter = request.args.get('status_filter','').lower()
    filtered = bookings
    if status_filter and status_filter != 'all':
        filtered = [b for b in bookings if b['status'].lower() == status_filter]

    # We'll pass showtime_dict and movie_dict for template to map booking->showtime->movie->title
    return render_template('bookings.html',
                           bookings=filtered,
                           movie_dict=movie_dict,
                           showtime_dict=showtime_dict,
                           status_filter=status_filter)

@app.route('/theaters')
def theaters():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter','').strip()
    filtered = theaters
    if location_filter:
        filtered = [t for t in theaters if location_filter.lower() in (t['location'].lower() + ' ' + t['city'].lower())]

    locations = sorted(set([t['location'] for t in theaters] + [t['city'] for t in theaters]))

    facilities_display = ''
    if len(filtered)==1:
        facilities_display = filtered[0]['facilities']

    return render_template('theaters.html',
                           theaters=filtered,
                           locations=locations,
                           location_filter=location_filter,
                           facilities_display=facilities_display)

if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
