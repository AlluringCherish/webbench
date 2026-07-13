from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to read data files

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, full_name = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'full_name': full_name
                }
    except FileNotFoundError:
        pass
    return users


def load_menu():
    menu = {}
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
                dish_id_int = int(dish_id)
                menu[dish_id_int] = {
                    'dish_id': dish_id_int,
                    'name': name,
                    'category': category,
                    'price': float(price),
                    'description': description,
                    'ingredients': ingredients,
                    'dietary': dietary,
                    'avg_rating': float(avg_rating)
                }
    except FileNotFoundError:
        pass
    return menu


def load_reservations():
    reservations = {}
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 10:
                    continue
                reservation_id, username, guest_name, phone, email, party_size, date, time, special_requests, status = parts
                reservations[int(reservation_id)] = {
                    'reservation_id': int(reservation_id),
                    'username': username,
                    'guest_name': guest_name,
                    'phone': phone,
                    'email': email,
                    'party_size': int(party_size),
                    'date': date,
                    'time': time,
                    'special_requests': special_requests,
                    'status': status
                }
    except FileNotFoundError:
        pass
    return reservations


def save_reservations(reservations):
    with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
        for rid in sorted(reservations.keys()):
            r = reservations[rid]
            line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}"
            f.write(line + '\n')


def load_waitlist():
    waitlist = {}
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                waitlist_id, username, party_size, join_time, status = parts
                waitlist[int(waitlist_id)] = {
                    'waitlist_id': int(waitlist_id),
                    'username': username,
                    'party_size': int(party_size),
                    'join_time': join_time,
                    'status': status
                }
    except FileNotFoundError:
        pass
    return waitlist


def save_waitlist(waitlist):
    with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
        for wid in sorted(waitlist.keys()):
            w = waitlist[wid]
            line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}"
            f.write(line + '\n')


def load_reviews():
    reviews = {}
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review_id, username, dish_id, rating, review_text, review_date = parts
                reviews[int(review_id)] = {
                    'review_id': int(review_id),
                    'username': username,
                    'dish_id': int(dish_id),
                    'rating': int(rating),
                    'review_text': review_text,
                    'review_date': review_date
                }
    except FileNotFoundError:
        pass
    return reviews


def save_reviews(reviews):
    with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
        for rid in sorted(reviews.keys()):
            r = reviews[rid]
            line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}"
            f.write(line + '\n')

# For simplicity, simulate current user as 'john_diner'
CURRENT_USER = 'john_diner'

@app.route('/')
def dashboard():
    users = load_users()
    user = users.get(CURRENT_USER, {})
    welcome = user.get('username', 'Guest')
    menu = load_menu()
    reservations = load_reservations()
    # Show upcoming reservations of current user
    upcoming_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER and r['status'] == 'Upcoming']
    return render_template('dashboard.html', username=welcome, upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu_page():
    menu = load_menu()
    # For display, gather dishes ordered by category then name
    dishes = sorted(menu.values(), key=lambda d: (d['category'], d['name']))
    return render_template('menu.html', dishes=dishes)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = menu.get(dish_id)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    users = load_users()
    user = users.get(CURRENT_USER, {})
    if request.method == 'POST':
        guest_name = request.form.get('guest-name', '').strip()
        party_size = request.form.get('party-size', '')
        reservation_date = request.form.get('reservation-date', '')
        # We do not have time field in spec; set default time
        default_time = '19:00'

        if not guest_name or not party_size or not reservation_date:
            # Missing info, reload form with error (simple)
            return render_template('make_reservation.html', error='All fields are required.')

        try:
            party_size_int = int(party_size)
            datetime.strptime(reservation_date, '%Y-%m-%d')
        except:
            return render_template('make_reservation.html', error='Invalid input.')

        reservations = load_reservations()
        # New reservation_id
        if reservations:
            new_id = max(reservations.keys()) + 1
        else:
            new_id = 1
        new_reservation = {
            'reservation_id': new_id,
            'username': CURRENT_USER,
            'guest_name': guest_name,
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
            'party_size': party_size_int,
            'date': reservation_date,
            'time': default_time,
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations[new_id] = new_reservation
        save_reservations(reservations)
        return redirect(url_for('my_reservations'))

    return render_template('make_reservation.html')

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = load_reservations()
    if request.method == 'POST':
        # Cancel reservation action
        cancel_id = request.form.get('cancel-reservation-id')
        if cancel_id:
            rid = int(cancel_id)
            if rid in reservations and reservations[rid]['username'] == CURRENT_USER and reservations[rid]['status'] == 'Upcoming':
                reservations[rid]['status'] = 'Cancelled'
                save_reservations(reservations)
            return redirect(url_for('my_reservations'))

    user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]
    # Sort by date ascending
    user_reservations.sort(key=lambda r: (r['date'], r['time']))
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_page():
    waitlist = load_waitlist()
    users = load_users()
    user = users.get(CURRENT_USER, {})

    user_positions = [w for w in waitlist.values() if w['username'] == CURRENT_USER and w['status'] == 'Active']
    user_position = None
    if user_positions:
        # Sort by join_time ascending
        user_positions.sort(key=lambda w: w['join_time'])
        user_position = user_positions[0]
        # Compute position in waitlist by join_time
        active_waitlist_ordered = sorted([w for w in waitlist.values() if w['status'] == 'Active'], key=lambda w: w['join_time'])
        position_index = active_waitlist_ordered.index(user_position) + 1
    else:
        position_index = None

    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size')
        if party_size:
            try:
                party_size_int = int(party_size)
                # Add new waitlist entry
                if waitlist:
                    new_id = max(waitlist.keys()) + 1
                else:
                    new_id = 1
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_entry = {
                    'waitlist_id': new_id,
                    'username': CURRENT_USER,
                    'party_size': party_size_int,
                    'join_time': now_str,
                    'status': 'Active'
                }
                waitlist[new_id] = new_entry
                save_waitlist(waitlist)
                return redirect(url_for('waitlist_page'))
            except:
                pass
    return render_template('waitlist.html', user_position=position_index)

@app.route('/my-reviews')
def my_reviews():
    reviews = load_reviews()
    menu = load_menu()
    user_reviews = [r for r in reviews.values() if r['username'] == CURRENT_USER]
    # Attach dish names
    for r in user_reviews:
        dish = menu.get(r['dish_id'])
        r['dish_name'] = dish['name'] if dish else 'Unknown Dish'
    # Sort by review_date descending
    user_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    menu = load_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not dish_id or not rating or not review_text:
            return render_template('write_review.html', dishes=menu.values(), error='All fields are required.')
        try:
            dish_id_int = int(dish_id)
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError
        except:
            return render_template('write_review.html', dishes=menu.values(), error='Invalid input.')
        reviews = load_reviews()
        if reviews:
            new_id = max(reviews.keys()) + 1
        else:
            new_id = 1
        now_str = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_id,
            'username': CURRENT_USER,
            'dish_id': dish_id_int,
            'rating': rating_int,
            'review_text': review_text,
            'review_date': now_str
        }
        reviews[new_id] = new_review
        save_reviews(reviews)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', dishes=menu.values())

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USER)
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email and user:
            user['email'] = new_email
            # Save back to users.txt
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}"
                    f.write(line + '\n')
            return redirect(url_for('dashboard'))
    if user:
        return render_template('profile.html', username=user['username'], email=user['email'])
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
