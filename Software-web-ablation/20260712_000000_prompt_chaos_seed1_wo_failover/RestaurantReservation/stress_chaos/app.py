from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
DATA_DIR = 'data'

CURRENT_USERNAME = 'john_diner'  # Simulated logged-in user

# Helper functions for file IO

def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                dish_id = int(parts[0])
                name = parts[1]
                category = parts[2]
                price = float(parts[3])
                description = parts[4]
                ingredients = parts[5]
                dietary = parts[6]
                avg_rating = float(parts[7]) if parts[7] else None
                menu.append({
                    'dish_id': dish_id,
                    'name': name,
                    'category': category,
                    'price': price,
                    'description': description,
                    'ingredients': ingredients,
                    'dietary': dietary,
                    'avg_rating': avg_rating
                })
    except FileNotFoundError:
        pass
    return menu


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                review_id = int(parts[0])
                username = parts[1]
                dish_id = int(parts[2])
                rating = int(parts[3])
                review_text = parts[4]
                review_date = parts[5]
                reviews.append({
                    'review_id': review_id,
                    'username': username,
                    'dish_id': dish_id,
                    'rating': rating,
                    'review_text': review_text,
                    'review_date': review_date
                })
    except FileNotFoundError:
        pass
    return reviews


def save_reviews(reviews):
    with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
        for r in reviews:
            f.write('|'.join([
                str(r['review_id']),
                r['username'],
                str(r['dish_id']),
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ]) + '\n')


def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                username = parts[0]
                full_name = parts[1]
                email = parts[2]
                phone = parts[3]
                password = parts[4]
                users[username] = {
                    'username': username,
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'password': password
                }
    except FileNotFoundError:
        pass
    return users


def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 9:
                    continue
                reservation_id = int(parts[0])
                username = parts[1]
                guest_name = parts[2]
                phone = parts[3]
                email = parts[4]
                party_size = int(parts[5])
                date = parts[6]
                time = parts[7]
                status = parts[8]
                reservations.append({
                    'reservation_id': reservation_id,
                    'username': username,
                    'guest_name': guest_name,
                    'phone': phone,
                    'email': email,
                    'party_size': party_size,
                    'date': date,
                    'time': time,
                    'status': status
                })
    except FileNotFoundError:
        pass
    return reservations


def save_reservations(reservations):
    with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
        for r in reservations:
            f.write('|'.join([
                str(r['reservation_id']),
                r['username'],
                r['guest_name'],
                r['phone'],
                r['email'],
                str(r['party_size']),
                r['date'],
                r['time'],
                r['status']
            ]) + '\n')


def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                waitlist_id = int(parts[0])
                username = parts[1]
                party_size = int(parts[2])
                join_time = parts[3]
                status = parts[4]
                waitlist.append({
                    'waitlist_id': waitlist_id,
                    'username': username,
                    'party_size': party_size,
                    'join_time': join_time,
                    'status': status
                })
    except FileNotFoundError:
        pass
    return waitlist


def save_waitlist(waitlist):
    with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
        for w in waitlist:
            f.write('|'.join([
                str(w['waitlist_id']),
                w['username'],
                str(w['party_size']),
                w['join_time'],
                w['status']
            ]) + '\n')

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    menu = load_menu()
    reviews = load_reviews()
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'] or 0, reverse=True)[:3]

    reservations = load_reservations()
    upcoming_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming']

    return render_template('dashboard.html', username=CURRENT_USERNAME, upcoming_reservations=upcoming_reservations, featured_dishes=featured_dishes)


@app.route('/menu')
def menu():
    dishes = load_menu()
    return render_template('menu.html', dishes=dishes)


@app.route('/dish/<int:dish_id>')
def dish(dish_id):
    menu = load_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    if dish is None:
        return 'Dish not found', 404
    return render_template('dish_details.html', dish=dish)


@app.route('/write_review/<int:dish_id>', methods=['GET', 'POST'])
def write_review(dish_id):
    menu = load_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    if dish is None:
        return 'Dish not found', 404

    if request.method == 'POST':
        reviews = load_reviews()
        next_id = max([r['review_id'] for r in reviews], default=0) + 1
        rating = int(request.form.get('rating', 0))
        review_text = request.form.get('review_text', '').strip()
        review_date = datetime.now().strftime('%Y-%m-%d')
        reviews.append({
            'review_id': next_id,
            'username': CURRENT_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })
        save_reviews(reviews)
        return redirect(url_for('dish', dish_id=dish_id))

    return render_template('write_review.html', dish=dish)


@app.route('/my_reservations')
def my_reservations():
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    reservation_found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            reservation_found = True
            break
    if reservation_found:
        save_reservations(reservations)
    return redirect(url_for('my_reservations'))


@app.route('/profile')
def profile():
    users = load_users()
    user_profile = users.get(CURRENT_USERNAME)
    if not user_profile:
        return 'User not found', 404
    return render_template('profile.html', user_profile=user_profile)


@app.route('/waitlist')
def waitlist():
    waitlist_entries = load_waitlist()
    user_waitlist_entries = [w for w in waitlist_entries if w['username'] == CURRENT_USERNAME]
    return render_template('waitlist.html', waitlist_entries=user_waitlist_entries)


@app.route('/my_reviews')
def my_reviews():
    reviews = load_reviews()
    menu = load_menu()
    dish_name_map = {d['dish_id']: d['name'] for d in menu}
    user_reviews = []
    for rv in reviews:
        if rv['username'] == CURRENT_USERNAME:
            user_reviews.append({
                'review_id': rv['review_id'],
                'dish_name': dish_name_map.get(rv['dish_id'], 'Unknown Dish'),
                'rating': rv['rating'],
                'review_text': rv['review_text'],
                'review_date': rv['review_date']
            })
    return render_template('my_reviews.html', user_reviews=user_reviews)


if __name__ == '__main__':
    app.run(debug=True)
