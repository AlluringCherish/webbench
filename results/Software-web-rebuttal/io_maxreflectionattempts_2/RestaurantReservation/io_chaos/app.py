from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

LOGGED_IN_USERNAME = 'john_diner'

# Helper functions

def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
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
    path = os.path.join(DATA_DIR, 'menu.txt')
    menu = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id_str, name, category, price_str, description, ingredients_str, dietary, avg_rating_str = parts
                    try:
                        dish_id = int(dish_id_str)
                        price = float(price_str)
                        avg_rating = float(avg_rating_str)
                        ingredients = [i.strip() for i in ingredients_str.split(',')] if ingredients_str else []
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
                    except ValueError:
                        continue
    return menu

def load_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id_str, username, guest_name, phone, email, party_size_str, date, time_str, special_requests, status = parts
                    try:
                        reservation_id = int(reservation_id_str)
                        party_size = int(party_size_str)
                        reservations.append({
                            'reservation_id': reservation_id,
                            'username': username,
                            'guest_name': guest_name,
                            'phone': phone,
                            'email': email,
                            'party_size': party_size,
                            'date': date,
                            'time': time_str,
                            'special_requests': special_requests,
                            'status': status
                        })
                    except ValueError:
                        continue
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                str(r['reservation_id']),
                r.get('username',''),
                r.get('guest_name',''),
                r.get('phone',''),
                r.get('email',''),
                str(r.get('party_size','')),
                r.get('date',''),
                r.get('time',''),
                r.get('special_requests',''),
                r.get('status','')
            ])
            f.write(line + '\n')

def load_waitlist():
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    waitlist = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id_str, username, party_size_str, join_time, status = parts
                    try:
                        waitlist_id = int(waitlist_id_str)
                        party_size = int(party_size_str)
                        waitlist.append({
                            'waitlist_id': waitlist_id,
                            'username': username,
                            'party_size': party_size,
                            'join_time': join_time,
                            'status': status
                        })
                    except ValueError:
                        continue
    return waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = '|'.join([
                str(w['waitlist_id']),
                w.get('username',''),
                str(w.get('party_size','')),
                w.get('join_time',''),
                w.get('status','')
            ])
            f.write(line + '\n')

def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id_str, username, dish_id_str, rating_str, review_text, review_date = parts
                    try:
                        review_id = int(review_id_str)
                        dish_id = int(dish_id_str)
                        rating = int(rating_str)
                        reviews.append({
                            'review_id': review_id,
                            'username': username,
                            'dish_id': dish_id,
                            'rating': rating,
                            'review_text': review_text,
                            'review_date': review_date
                        })
                    except ValueError:
                        continue
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                str(r['review_id']),
                r.get('username',''),
                str(r.get('dish_id','')),
                str(r.get('rating','')),
                r.get('review_text',''),
                r.get('review_date','')
            ])
            f.write(line + '\n')

def get_user_profile(username):
    users = load_users()
    return users.get(username, None)

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    username = LOGGED_IN_USERNAME
    menu = load_menu()
    reservations = load_reservations()

    featured = sorted(menu, key=lambda d: d.get('avg_rating', 0), reverse=True)[:3]
    featured_dishes = [{'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price']} for d in featured]

    user_reservations = [r for r in reservations if r['username'] == username and r['status'] == 'Upcoming']
    try:
        user_reservations.sort(key=lambda r: (r['date'], r['time']))
    except Exception:
        pass

    upcoming_reservations = []
    for r in user_reservations:
        upcoming_reservations.append({
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        })

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu_page():
    menus = load_menu()
    return render_template('menu.html', menus=menus)

@app.route('/dish/<int:dish_id>')
def dish_details_page(dish_id):
    menus = load_menu()
    dish = None
    for d in menus:
        if d['dish_id'] == dish_id:
            dish = d
            break
    if dish is None:
        return redirect(url_for('menu_page'))
    return render_template('dish_details.html', dish=dish)

@app.route('/make_reservation')
def make_reservation_page():
    return render_template('make_reservation.html')

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '1').strip()
    reservation_date = request.form.get('reservation_date', '').strip()
    username = LOGGED_IN_USERNAME
    try:
        party_size = int(party_size_str)
    except ValueError:
        party_size = 1

    user_profile = get_user_profile(username)
    phone = user_profile['phone'] if user_profile else ''
    email = user_profile['email'] if user_profile else ''

    reservations = load_reservations()
    next_id = 1
    if reservations:
        next_id = max(r['reservation_id'] for r in reservations) + 1

    reservation = {
        'reservation_id': next_id,
        'username': username,
        'guest_name': guest_name,
        'phone': phone,
        'email': email,
        'party_size': party_size,
        'date': reservation_date,
        'time': '19:00',
        'special_requests': '',
        'status': 'Upcoming'
    }
    reservations.append(reservation)
    save_reservations(reservations)

    return redirect(url_for('my_reservations_page'))

@app.route('/my_reservations')
def my_reservations_page():
    username = LOGGED_IN_USERNAME
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == username]
    try:
        user_reservations.sort(key=lambda r: (r['date'], r['time']), reverse=True)
    except Exception:
        pass
    reservations_list = []
    for r in user_reservations:
        reservations_list.append({
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=reservations_list)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = LOGGED_IN_USERNAME
    reservations = load_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            save_reservations(reservations)
            break
    return redirect(url_for('my_reservations_page'))

@app.route('/waitlist')
def waitlist_page():
    username = LOGGED_IN_USERNAME
    waitlist = load_waitlist()
    user_entry = None
    for entry in waitlist:
        if entry['username'] == username and entry['status'] == 'Active':
            user_entry = entry
            break
    user_position = None
    if user_entry:
        active_entries = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda w: w['join_time'])
        for idx, w in enumerate(active_entries, start=1):
            if w['waitlist_id'] == user_entry['waitlist_id']:
                user_position = idx
                break
    party_size_options = list(range(1, 11))
    return render_template('waitlist.html', user_position=user_position, party_size_options=party_size_options)

@app.route('/join_waitlist', methods=['POST'])
def join_waitlist():
    username = LOGGED_IN_USERNAME
    party_size_str = request.form.get('party_size', '1').strip()
    try:
        party_size = int(party_size_str)
        if not (1 <= party_size <= 10):
            party_size = 1
    except ValueError:
        party_size = 1
    waitlist = load_waitlist()
    for w in waitlist:
        if w['username'] == username and w['status'] == 'Active':
            return redirect(url_for('waitlist_page'))
    next_id = 1
    if waitlist:
        next_id = max(w['waitlist_id'] for w in waitlist) + 1
    join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = {
        'waitlist_id': next_id,
        'username': username,
        'party_size': party_size,
        'join_time': join_time,
        'status': 'Active'
    }
    waitlist.append(new_entry)
    save_waitlist(waitlist)
    return redirect(url_for('waitlist_page'))

@app.route('/my_reviews')
def my_reviews_page():
    username = LOGGED_IN_USERNAME
    reviews_data = load_reviews()
    menu = load_menu()
    reviews_list = []
    dish_id_to_name = {d['dish_id']: d['name'] for d in menu}
    for r in reviews_data:
        if r['username'] == username:
            dish_name = dish_id_to_name.get(r['dish_id'], 'Unknown')
            reviews_list.append({
                'review_id': r['review_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=reviews_list, username=username)

@app.route('/write_review')
def write_review_page():
    username = LOGGED_IN_USERNAME
    menu = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
    return render_template('write_review.html', dishes=dishes, username=username)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    username = LOGGED_IN_USERNAME
    dish_id_str = request.form.get('dish_id', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()
    try:
        dish_id = int(dish_id_str)
    except ValueError:
        dish_id = None
    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            rating = 5
    except ValueError:
        rating = 5
    reviews = load_reviews()
    next_id = 1
    if reviews:
        next_id = max(r['review_id'] for r in reviews) + 1
    today = datetime.now().strftime('%Y-%m-%d')
    if dish_id is not None:
        new_review = {
            'review_id': next_id,
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today
        }
        reviews.append(new_review)
        save_reviews(reviews)
    return redirect(url_for('my_reviews_page'))

@app.route('/profile')
def profile_page():
    username = LOGGED_IN_USERNAME
    user_profile = get_user_profile(username)
    if user_profile is None:
        user_profile = {'username': username, 'email': '', 'phone': '', 'full_name': ''}
    return render_template('profile.html', user_profile=user_profile)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    username = LOGGED_IN_USERNAME
    email = request.form.get('email', '').strip()
    users = load_users()
    if username in users:
        user = users[username]
        user['email'] = email
        path = os.path.join(DATA_DIR, 'users.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['full_name']])
                f.write(line + '\n')
    return redirect(url_for('profile_page'))

if __name__ == '__main__':
    app.run(debug=True)
