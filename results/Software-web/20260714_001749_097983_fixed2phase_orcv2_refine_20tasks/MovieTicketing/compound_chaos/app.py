from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

data_dir = 'data'

# Helper functions to read and write pipe-delimited data files

def read_file(filename):
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        records = [line.split('|') for line in lines if line]
    return records


def write_file(filename, records):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            f.write('|'.join(record) + '\n')


def get_movies():
    movies_raw = read_file('movies.txt')
    movies = []
    for r in movies_raw:
        movies.append({
            'movie_id': int(r[0]),
            'title': r[1],
            'director': r[2],
            'genre': r[3],
            'rating': float(r[4]),
            'duration': int(r[5]),
            'description': r[6],
            'release_date': r[7]
        })
    return movies


def get_genres():
    genres_raw = read_file('genres.txt')
    genres = []
    for r in genres_raw:
        genres.append({'genre_id': int(r[0]), 'genre_name': r[1], 'description': r[2]})
    return genres


def get_theaters():
    theaters_raw = read_file('theaters.txt')
    theaters = []
    for r in theaters_raw:
        theaters.append({
            'theater_id': int(r[0]),
            'theater_name': r[1],
            'location': r[2],
            'city': r[3],
            'screens': int(r[4]),
            'facilities': [f.strip() for f in r[5].split(',')] if r[5].strip() else []
        })
    return theaters


def get_showtimes():
    showtimes_raw = read_file('showtimes.txt')
    showtimes = []
    for r in showtimes_raw:
        showtimes.append({
            'showtime_id': int(r[0]),
            'movie_id': int(r[1]),
            'theater_id': int(r[2]),
            'showtime_date': r[3],
            'showtime_time': r[4],
            'price': float(r[5]),
            'available_seats': int(r[6])
        })
    return showtimes


def get_seats():
    seats_raw = read_file('seats.txt')
    seats = []
    for r in seats_raw:
        seats.append({
            'seat_id': int(r[0]),
            'theater_id': int(r[1]),
            'screen_id': int(r[2]),
            'row': r[3],
            'column': int(r[4]),
            'seat_type': r[5],
            'status': r[6]
        })
    return seats


def get_bookings():
    bookings_raw = read_file('bookings.txt')
    bookings = []
    for r in bookings_raw:
        bookings.append({
            'booking_id': int(r[0]),
            'showtime_id': int(r[1]),
            'customer_name': r[2],
            'customer_email': r[3],
            'booking_date': r[4],
            'total_price': float(r[5]),
            'status': r[6],
            'seats_booked': r[7].split(',') if r[7] else []
        })
    return bookings


# Dashboard Page
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Featured movies: show 3 top rated movies as recommendations
    movies = get_movies()
    featured = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured_movies=featured)


# Movie Catalog Page
@app.route('/catalog')
def catalog():
    search_query = request.args.get('search', '').strip().lower()
    selected_genre = request.args.get('genre', '')
    movies = get_movies()
    genres = get_genres()

    filtered_movies = movies
    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower() or search_query in m['genre'].lower()]
    if selected_genre and selected_genre != 'All':
        filtered_movies = [m for m in filtered_movies if m['genre'] == selected_genre]

    return render_template('catalog.html', movies=filtered_movies, genres=genres, selected_genre=selected_genre, search_query=search_query)


# Movie Details Page
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movies = get_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)


# Showtime Selection Page
@app.route('/showtimes/<int:movie_id>')
def showtimes(movie_id):
    theater_filter = request.args.get('theater', '')
    date_filter = request.args.get('date', '')

    showtimes = get_showtimes()
    theaters = get_theaters()

    filtered_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
    if theater_filter:
        filtered_showtimes = [st for st in filtered_showtimes if str(st['theater_id']) == theater_filter]
    if date_filter:
        filtered_showtimes = [st for st in filtered_showtimes if st['showtime_date'] == date_filter]

    return render_template('showtime_selection.html', showtimes=filtered_showtimes, theaters=theaters, theater_filter=theater_filter, date_filter=date_filter, movie_id=movie_id)


# Seat Selection Page
@app.route('/seats/<int:showtime_id>', methods=['GET', 'POST'])
def seat_selection(showtime_id):
    showtimes = get_showtimes()
    showtime = next((st for st in showtimes if st['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    theaters = get_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404

    seats = get_seats()
    # For simplicity, screen_id is assumed to be 1 for all
    relevant_seats = [s for s in seats if s['theater_id'] == theater['theater_id'] and s['screen_id'] == 1]

    # Build seat map by rows
    seat_map = {}
    for seat in relevant_seats:
        row = seat['row']
        if row not in seat_map:
            seat_map[row] = []
        seat_map[row].append(seat)
    for row in seat_map:
        seat_map[row] = sorted(seat_map[row], key=lambda s: s['column'])

    if request.method == 'POST':
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            error = "Please select at least one seat."
            return render_template('seat_selection.html', showtime=showtime, seat_map=seat_map, selected_seats=[], error=error)
        return redirect(url_for('booking_confirmation', showtime_id=showtime_id, seats=','.join(selected_seats)))

    return render_template('seat_selection.html', showtime=showtime, seat_map=seat_map, selected_seats=[]) 


# Booking Confirmation Page
@app.route('/booking_confirmation/<int:showtime_id>', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    seats_param = request.args.get('seats', '')
    seats_selected = seats_param.split(',') if seats_param else []

    showtimes = get_showtimes()
    showtime = next((st for st in showtimes if st['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movies = get_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404

    theaters = get_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    total_price = showtime['price'] * len(seats_selected)

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        if not customer_name or not customer_email:
            error = "Please fill in all customer details."
            return render_template('booking_confirmation.html', showtime=showtime, movie=movie, theater=theater, seats_selected=seats_selected, total_price=total_price, error=error)

        bookings = get_bookings()
        new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1
        booking_date = datetime.now().strftime('%Y-%m-%d')
        booking_record = [
            str(new_booking_id),
            str(showtime_id),
            customer_name,
            customer_email,
            booking_date,
            f'{total_price:.2f}',
            'Confirmed',
            ','.join(seats_selected)
        ]
        bookings.append({
            'booking_id': new_booking_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats_selected
        })
        # Save booking
        bookings_raw = read_file('bookings.txt')
        bookings_raw.append('|'.join(booking_record))
        write_file('bookings.txt', [line.split('|') for line in bookings_raw])

        # Update seats status to Booked (simplified: assume seat labels are row+col)
        seats = get_seats()
        for seat_label in seats_selected:
            row = seat_label[0]
            col = int(seat_label[1:])
            for seat in seats:
                if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == 1 and seat['row'] == row and seat['column'] == col:
                    seat['status'] = 'Booked'
        # Write seats file back
        seat_records = []
        for seat in seats:
            seat_records.append([
                str(seat['seat_id']),
                str(seat['theater_id']),
                str(seat['screen_id']),
                seat['row'],
                str(seat['column']),
                seat['seat_type'],
                seat['status']
            ])
        write_file('seats.txt', seat_records)

        return redirect(url_for('dashboard'))

    return render_template('booking_confirmation.html', showtime=showtime, movie=movie, theater=theater, seats_selected=seats_selected, total_price=total_price)


# Booking History Page
@app.route('/bookings')
def bookings():
    status_filter = request.args.get('status', 'All')
    bookings = get_bookings()
    movies = get_movies()

    # Filter bookings by status
    if status_filter != 'All':
        bookings = [b for b in bookings if b['status'] == status_filter]

    # Enhance bookings with movie title and date from showtime
    showtimes = get_showtimes()
    for booking in bookings:
        showtime = next((st for st in showtimes if st['showtime_id'] == booking['showtime_id']), None)
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None) if showtime else None
        booking['movie_title'] = movie['title'] if movie else 'Unknown'
        booking['showtime_date'] = showtime['showtime_date'] if showtime else ''

    return render_template('booking_history.html', bookings=bookings, status_filter=status_filter)


# Theater Information Page
@app.route('/theaters')
def theaters():
    location_filter = request.args.get('location', '')
    theaters = get_theaters()
    if location_filter:
        theaters = [t for t in theaters if t['city'] == location_filter]

    # Collect all unique cities for filter dropdown
    cities = sorted(set([t['city'] for t in get_theaters()]))

    return render_template('theater_information.html', theaters=theaters, cities=cities, location_filter=location_filter)


if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
