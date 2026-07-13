from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

# Data file paths
USERS_FILE = 'data/users.txt'
MENU_FILE = 'data/menu.txt'
RESERVATIONS_FILE = 'data/reservations.txt'
WAITLIST_FILE = 'data/waitlist.txt'
REVIEWS_FILE = 'data/reviews.txt'

# Helper functions for file operations

def read_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
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

def read_menu():
    menu = []
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
                    menu.append({
                        'dish_id': int(dish_id),
                        'name': name,
                        'category': category,
                        'price': float(price),
                        'description': description,
                        'ingredients': ingredients,
                        'dietary': dietary,
                        'avg_rating': float(avg_rating)
                    })
    return menu

def read_reservations():
    reservations = []
    if os.path.exists(RESERVATIONS_FILE):
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id, username, guest_name, phone, email, party_size, date, time_, special_requests, status = parts
                    reservations.append({
                        'reservation_id': int(reservation_id),
                        'username': username,
                        'guest_name': guest_name,
                        'phone': phone,
                        'email': email,
                        'party_size': int(party_size),
                        'date': date,
                        'time': time_,
                        'special_requests': special_requests,
                        'status': status
                    })
    return reservations

def write_reservations(reservations):
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                str(r['reservation_id']),
                r['username'],
                r['guest_name'],
                r['phone'],
                r['email'],
                str(r['party_size']),
                r['date'],
                r['time'],
                r['special_requests'],
                r['status']
            ]) + '\n'
            f.write(line)

def read_waitlist():
    waitlist = []
    if os.path.exists(WAITLIST_FILE):
        with open(WAITLIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id, username, party_size, join_time, status = parts
                    waitlist.append({
                        'waitlist_id': int(waitlist_id),
                        'username': username,
                        'party_size': int(party_size),
                        'join_time': join_time,
                        'status': status
                    })
    return waitlist

def write_waitlist(waitlist):
    with open(WAITLIST_FILE, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = '|'.join([
                str(w['waitlist_id']),
                w['username'],
                str(w['party_size']),
                w['join_time'],
                w['status']
            ]) + '\n'
            f.write(line)

def read_reviews():
    reviews = []
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id, username, dish_id, rating, review_text, review_date = parts
                    reviews.append({
                        'review_id': int(review_id),
                        'username': username,
                        'dish_id': int(dish_id),
                        'rating': int(rating),
                        'review_text': review_text,
                        'review_date': review_date
                    })
    return reviews

def write_reviews(reviews):
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                str(r['review_id']),
                r['username'],
                str(r['dish_id']),
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ]) + '\n'
            f.write(line)

# Assume single user logged in for simplification
LOGGED_IN_USERNAME = 'john_diner'

@app.route('/')
def dashboard():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return 'User not found', 404
    return render_template('dashboard.html', username=user['username'])

@app.route('/menu')
def menu():
    menu = read_menu()
    return render_template('menu.html', menu=menu)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = read_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    if not dish:
        return 'Dish not found', 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return 'User not found', 404

    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size = int(request.form.get('party_size', 1))
        reservation_date = request.form.get('reservation_date', '')

        if not guest_name or not reservation_date or party_size < 1 or party_size > 10:
            # Could add more validation
            return render_template('make_reservation.html', username=user['username'], error='Invalid input')

        # Assign a time slot fixed for simplicity
        time_slot = '19:00'

        # Generate new reservation ID
        reservations = read_reservations()
        max_id = max((r['reservation_id'] for r in reservations), default=0)
        new_id = max_id + 1

        new_res = {
            'reservation_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'guest_name': guest_name,
            'phone': user['phone'],
            'email': user['email'],
            'party_size': party_size,
            'date': reservation_date,
            'time': time_slot,
            'special_requests': '',
            'status': 'Upcoming'
        }

        reservations.append(new_res)
        write_reservations(reservations)

        return redirect(url_for('dashboard'))

    return render_template('make_reservation.html', username=user['username'])

@app.route('/my_reservations')
def my_reservations():
    reservations = read_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USERNAME]
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel_reservation/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            found = True
            break
    if found:
        write_reservations(reservations)
    return redirect(url_for('my_reservations'))

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    if request.method == 'POST':
        party_size = int(request.form.get('waitlist_party_size', 1))
        waitlist = read_waitlist()
        max_id = max((w['waitlist_id'] for w in waitlist), default=0)
        new_id = max_id + 1

        new_entry = {
            'waitlist_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'party_size': party_size,
            'join_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Active'
        }

        waitlist.append(new_entry)
        write_waitlist(waitlist)

        return redirect(url_for('waitlist'))

    # Show user's position in waitlist
    waitlist = [w for w in read_waitlist() if w['status'] == 'Active']
    user_positions = sorted(waitlist, key=lambda x: x['join_time'])
    user_position = None
    for idx, w in enumerate(user_positions, start=1):
        if w['username'] == LOGGED_IN_USERNAME:
            user_position = idx
            break
    return render_template('waitlist.html', user_position=user_position)

@app.route('/my_reviews')
def my_reviews():
    reviews = read_reviews()
    menu = read_menu()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USERNAME]
    # Attach dish names
    for r in user_reviews:
        dish = next((d for d in menu if d['dish_id']==r['dish_id']), None)
        r['dish_name'] = dish['name'] if dish else 'Unknown'
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    menu = read_menu()
    if request.method == 'POST':
        dish_id = int(request.form.get('select_dish', 0))
        rating = int(request.form.get('rating_input', 1))
        review_text = request.form.get('review_text', '').strip()

        if dish_id == 0 or rating < 1 or rating > 5 or not review_text:
            return render_template('write_review.html', menu=menu, error='Invalid input')

        reviews = read_reviews()
        max_id = max((r['review_id'] for r in reviews), default=0)
        new_id = max_id + 1

        new_review = {
            'review_id': new_id,
            'username': LOGGED_IN_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': datetime.now().strftime('%Y-%m-%d')
        }

        reviews.append(new_review)
        write_reviews(reviews)

        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', menu=menu)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(LOGGED_IN_USERNAME)
    if not user:
        return 'User not found', 404

    if request.method == 'POST':
        email = request.form.get('profile_email', '').strip()
        if email:
            user['email'] = email
            # Write back all users
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = '|'.join([u['username'], u['email'], u['phone'], u['full_name']]) + '\n'
                    f.write(line)

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
