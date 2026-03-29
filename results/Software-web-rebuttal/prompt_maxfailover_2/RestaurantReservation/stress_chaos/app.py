from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data files

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    username, email, phone, full_name = parts
                    users[username] = {
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'full_name': full_name
                    }
    return users


def load_menu():
    dishes = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
                    try:
                        dish = {
                            'dish_id': dish_id,
                            'name': name,
                            'category': category,
                            'price': float(price),
                            'description': description,
                            'ingredients': ingredients,
                            'dietary': dietary,
                            'avg_rating': float(avg_rating)
                        }
                        dishes.append(dish)
                    except ValueError:
                        # Skip invalid numeric data
                        continue
    return dishes


def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id, username, guest_name, phone, email, party_size, date, time_, special_requests, status = parts
                    try:
                        res = {
                            'reservation_id': reservation_id,
                            'username': username,
                            'guest_name': guest_name,
                            'phone': phone,
                            'email': email,
                            'party_size': int(party_size),
                            'date': date,
                            'time': time_,
                            'special_requests': special_requests,
                            'status': status
                        }
                        reservations.append(res)
                    except ValueError:
                        # Skip invalid numeric data
                        continue
    return reservations


def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id, username, party_size, join_time, status = parts
                    try:
                        wait = {
                            'waitlist_id': waitlist_id,
                            'username': username,
                            'party_size': int(party_size),
                            'join_time': join_time,
                            'status': status
                        }
                        waitlist.append(wait)
                    except ValueError:
                        continue
    return waitlist


def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id, username, dish_id, rating, review_text, review_date = parts
                    try:
                        review = {
                            'review_id': review_id,
                            'username': username,
                            'dish_id': dish_id,
                            'rating': int(rating),
                            'review_text': review_text,
                            'review_date': review_date
                        }
                        reviews.append(review)
                    except ValueError:
                        continue
    return reviews

# Helper functions to save data

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                r['reservation_id'],
                r['username'],
                r['guest_name'],
                r['phone'],
                r['email'],
                str(r['party_size']),
                r['date'],
                r['time'],
                r['special_requests'],
                r['status']
            ])
            f.write(line + '\n')


def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = '|'.join([
                w['waitlist_id'],
                w['username'],
                str(w['party_size']),
                w['join_time'],
                w['status']
            ])
            f.write(line + '\n')


def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                r['review_id'],
                r['username'],
                r['dish_id'],
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ])
            f.write(line + '\n')


def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([
                u['username'],
                u['email'],
                u['phone'],
                u['full_name']
            ])
            f.write(line + '\n')


# Since there is no explicit user authentication in specification,
# We assume a fixed logged-in username for all user-specific pages.
# This is a simulation for the purpose of the backend implementation.
LOGGED_IN_USERNAME = 'john_diner'


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USERNAME
    return render_template('dashboard.html', username=username)


@app.route('/menu')
def menu():
    dishes = load_menu()
    return render_template('menu.html', dishes=dishes)


@app.route('/dish/<string:dish_id>')
def dish_details(dish_id):
    dishes = load_menu()
    dish = next((d for d in dishes if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        try:
            party_size = int(request.form.get('party_size', '1'))
        except ValueError:
            party_size = 1
        reservation_date = request.form.get('reservation_date', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        special_requests = request.form.get('special_requests', '').strip()

        # Validate required fields minimally
        if not guest_name or not reservation_date or not phone or not email:
            error_msg = "Missing required reservation fields."
            return render_template('reservation.html', error=error_msg)

        # Generate new reservation_id (max + 1 numeric)
        reservations = load_reservations()
        max_id = 0
        for r in reservations:
            try:
                rid = int(r['reservation_id'])
                if rid > max_id:
                    max_id = rid
            except ValueError:
                continue
        new_id = str(max_id + 1)

        # Extract date and time parts
        # reservation_date input is date or datetime, from spec it is date field (but design says date/time input)
        datetime_obj = None
        try:
            datetime_obj = datetime.strptime(reservation_date, '%Y-%m-%d')
            time_str = '19:00'  # Default time if time not given?
        except ValueError:
            try:
                datetime_obj = datetime.strptime(reservation_date, '%Y-%m-%dT%H:%M')
                time_str = datetime_obj.strftime('%H:%M')
            except ValueError:
                # Invalid date format
                error_msg = "Invalid date/time format for reservation."
                return render_template('reservation.html', error=error_msg)

        date_str = datetime_obj.strftime('%Y-%m-%d')
        time_value = time_str

        # Append new reservation
        reservations.append({
            'reservation_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': date_str,
            'time': time_value,
            'special_requests': special_requests,
            'status': 'Upcoming'
        })

        # Save reservations to file
        save_reservations(reservations)

        return redirect(url_for('my_reservations'))

    return render_template('reservation.html')


@app.route('/my_reservations')
def my_reservations():
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USERNAME]
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<string:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    changed = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME:
            if r['status'] == 'Upcoming':
                r['status'] = 'Cancelled'
                changed = True
                break
    if changed:
        save_reservations(reservations)
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist_entries = load_waitlist()
    user_position = None

    if request.method == 'POST':
        try:
            party_size = int(request.form.get('party_size', '1'))
        except ValueError:
            party_size = 1

        # Generate new waitlist_id
        max_id = 0
        for w in waitlist_entries:
            try:
                wid = int(w['waitlist_id'])
                if wid > max_id:
                    max_id = wid
            except ValueError:
                continue
        new_id = str(max_id + 1)

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Append new waitlist entry
        waitlist_entries.append({
            'waitlist_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'party_size': party_size,
            'join_time': now_str,
            'status': 'Active'
        })

        save_waitlist(waitlist_entries)

        # After adding, we compute the user's position
        # Filter all active entries sorted by join_time ascending
        active_waitlist = sorted([
            w for w in waitlist_entries if w['status'] == 'Active'
        ], key=lambda x: x['join_time'])

        for idx, w in enumerate(active_waitlist):
            if w['username'] == LOGGED_IN_USERNAME and w['status'] == 'Active':
                user_position = idx + 1
                break

    else:
        # GET: find user's position if in active waitlist
        active_waitlist = sorted([
            w for w in waitlist_entries if w['status'] == 'Active'
        ], key=lambda x: x['join_time'])
        for idx, w in enumerate(active_waitlist):
            if w['username'] == LOGGED_IN_USERNAME and w['status'] == 'Active':
                user_position = idx + 1
                break

    return render_template('waitlist.html', waitlist=waitlist_entries, user_position=user_position)


@app.route('/my_reviews')
def my_reviews():
    reviews = load_reviews()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USERNAME]
    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    dishes = load_menu()
    if request.method == 'POST':
        dish_id = request.form.get('dish_id', '')
        try:
            rating = int(request.form.get('rating', '1'))
            if rating < 1 or rating > 5:
                rating = 1
        except ValueError:
            rating = 1
        review_text = request.form.get('review_text', '').strip()

        # Validate dish_id exists
        dish_exists = any(d['dish_id'] == dish_id for d in dishes)
        if not dish_exists:
            error_msg = "Invalid dish selected."
            return render_template('write_review.html', dishes=dishes, error=error_msg)

        # Validate rating and review_text
        if not review_text:
            error_msg = "Review text cannot be empty."
            return render_template('write_review.html', dishes=dishes, error=error_msg)

        reviews = load_reviews()
        # Generate new review_id
        max_id = 0
        for r in reviews:
            try:
                rid = int(r['review_id'])
                if rid > max_id:
                    max_id = rid
            except ValueError:
                continue
        new_id = str(max_id + 1)

        now_date = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': now_date
        }

        reviews.append(new_review)
        save_reviews(reviews)

        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', dishes=dishes)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(LOGGED_IN_USERNAME)
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if user and email:
            # Update user's email
            user['email'] = email
            save_users(users)
            # Reload user data
            users = load_users()
            user = users.get(LOGGED_IN_USERNAME)

    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
