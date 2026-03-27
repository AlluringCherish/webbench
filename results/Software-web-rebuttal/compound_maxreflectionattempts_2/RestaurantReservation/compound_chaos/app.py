from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
MENU_FILE = os.path.join(DATA_DIR, 'menu.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
WAITLIST_FILE = os.path.join(DATA_DIR, 'waitlist.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')

# Helper functions to load users

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                username,email,phone,full_name = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'full_name': full_name
                }
    return users

# Helper functions to load menu

def load_menu():
    menu = []
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) !=8:
                    continue
                dish_id,name,category,price,description,ingredients,dietary,avg_rating = parts
                try:
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
                except:
                    continue
    return menu

# Helper functions to load/write reservations

def load_reservations():
    reservations = []
    if os.path.exists(RESERVATIONS_FILE):
        with open(RESERVATIONS_FILE,'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 10:
                    continue
                try:
                    r = {
                        'reservation_id': int(parts[0]),
                        'username': parts[1],
                        'guest_name': parts[2],
                        'phone': parts[3],
                        'email': parts[4],
                        'party_size': int(parts[5]),
                        'date': parts[6],
                        'time': parts[7],
                        'special_requests': parts[8],
                        'status': parts[9]
                    }
                    reservations.append(r)
                except:
                    continue
    return reservations

def write_reservations(reservations):
    with open(RESERVATIONS_FILE,'w', encoding='utf-8') as f:
        for r in reservations:
            parts = [
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
            ]
            f.write('|'.join(parts)+'\n')

# Helper functions to load/write waitlist

def load_waitlist():
    waitlist = []
    if os.path.exists(WAITLIST_FILE):
        with open(WAITLIST_FILE,'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    w = {
                        'waitlist_id': int(parts[0]),
                        'username': parts[1],
                        'party_size': int(parts[2]),
                        'join_time': parts[3],
                        'status': parts[4]
                    }
                    waitlist.append(w)
                except:
                    continue
    return waitlist

def write_waitlist(waitlist):
    with open(WAITLIST_FILE,'w', encoding='utf-8') as f:
        for w in waitlist:
            parts = [
                str(w['waitlist_id']),
                w['username'],
                str(w['party_size']),
                w['join_time'],
                w['status']
            ]
            f.write('|'.join(parts)+'\n')

# Helper functions to load/write reviews

def load_reviews():
    reviews = []
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE,'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) !=6:
                    continue
                try:
                    r = {
                        'review_id': int(parts[0]),
                        'username': parts[1],
                        'dish_id': int(parts[2]),
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(r)
                except:
                    continue
    return reviews

def write_reviews(reviews):
    with open(REVIEWS_FILE,'w', encoding='utf-8') as f:
        for r in reviews:
            parts = [
                str(r['review_id']),
                r['username'],
                str(r['dish_id']),
                str(r['rating']),
                r['review_text'],
                r['review_date']
            ]
            f.write('|'.join(parts)+'\n')

# Current user for this app
CURRENT_USER = 'john_diner'

def get_current_user():
    users = load_users()
    return users.get(CURRENT_USER)


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    username = user['username'] if user else 'Guest'
    menu = load_menu()
    featured_raw = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    featured_dishes = [{'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price'], 'description': d['description']} for d in featured_raw]

    reservations = load_reservations()
    upcoming_reservations = [
        {
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        }
        for r in reservations if r['username'] == CURRENT_USER and r['status'] == 'Upcoming'
    ]

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu():
    menu_raw = load_menu()
    menus = [
        {
            'dish_id': d['dish_id'],
            'name': d['name'],
            'category': d['category'],
            'price': d['price'],
            'description': d['description'],
            'avg_rating': d['avg_rating']
        } for d in menu_raw
    ]
    return render_template('menu.html', menus=menus)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = None
    for d in menu:
        if d['dish_id'] == dish_id:
            dish = {'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price'], 'description': d['description']}
            break
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')
    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '').strip()
    reservation_date = request.form.get('reservation_date', '').strip()

    # Validate party_size
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            return "Party size must be between 1 and 10", 400
    except:
        return "Invalid party size", 400

    if not guest_name or not reservation_date:
        return "Missing required fields", 400

    try:
        datetime.strptime(reservation_date, '%Y-%m-%d')
    except:
        return "Invalid date format, must be YYYY-MM-DD", 400

    user = get_current_user()
    reservations = load_reservations()
    max_res_id = max([r['reservation_id'] for r in reservations], default=0)
    new_reservation = {
        'reservation_id': max_res_id+1,
        'username': CURRENT_USER,
        'guest_name': guest_name,
        'phone': user['phone'] if user else '',
        'email': user['email'] if user else '',
        'party_size': party_size,
        'date': reservation_date,
        'time': '18:00',
        'special_requests': '',
        'status': 'Upcoming'
    }
    reservations.append(new_reservation)
    write_reservations(reservations)

    return render_template('make_reservation.html', submission_status='Reservation submitted successfully.')

@app.route('/my-reservations')
def my_reservations():
    reservations = load_reservations()
    user_reservations = [
        {
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        }
        for r in reservations if r['username'] == CURRENT_USER
    ]
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USER:
            if r['status'] == 'Upcoming':
                r['status'] = 'Cancelled'
                updated = True
                break
    if updated:
        write_reservations(reservations)
        return '', 204
    else:
        return '', 404

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist_entries = load_waitlist()
    user_entry = None
    for entry in waitlist_entries:
        if entry['username'] == CURRENT_USER and entry['status'] == 'Active':
            user_entry = entry
            break

    if request.method == 'GET':
        waitlist_position = 0
        user_party_size = 0
        if user_entry:
            active_entries = [e for e in waitlist_entries if e['status'] == 'Active']
            sorted_entries = sorted(active_entries, key=lambda x: x['join_time'])
            for idx, entry in enumerate(sorted_entries, 1):
                if entry['username'] == CURRENT_USER:
                    waitlist_position = idx
                    user_party_size = entry['party_size']
                    break
        return render_template('waitlist.html', waitlist_position=waitlist_position, user_party_size=user_party_size)

    # POST
    party_size_str = request.form.get('party_size', '').strip()
    try:
        party_size = int(party_size_str)
    except:
        party_size = 0
    if party_size < 1:
        return render_template('waitlist.html', waitlist_position=0, user_party_size=0)

    if user_entry:
        active_entries = [e for e in waitlist_entries if e['status'] == 'Active']
        sorted_entries = sorted(active_entries, key=lambda x: x['join_time'])
        position = 0
        for idx, entry in enumerate(sorted_entries, 1):
            if entry['username'] == CURRENT_USER:
                position = idx
                break
        return render_template('waitlist.html', waitlist_position=position, user_party_size=user_entry['party_size'])

    max_waitlist_id = max([e['waitlist_id'] for e in waitlist_entries], default=0)
    new_waitlist_id = max_waitlist_id + 1

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    waitlist_entries.append({
        'waitlist_id': new_waitlist_id,
        'username': CURRENT_USER,
        'party_size': party_size,
        'join_time': now_str,
        'status': 'Active'
    })
    write_waitlist(waitlist_entries)

    active_entries = [e for e in waitlist_entries if e['status'] == 'Active']
    sorted_entries = sorted(active_entries, key=lambda x: x['join_time'])
    position = 0
    for idx, entry in enumerate(sorted_entries, 1):
        if entry['username'] == CURRENT_USER:
            position = idx
            break

    return render_template('waitlist.html', waitlist_position=position, user_party_size=party_size)

@app.route('/my-reviews')
def my_reviews():
    reviews = load_reviews()
    menu = load_menu()
    user_reviews = []
    for r in reviews:
        if r['username'] == CURRENT_USER:
            dish_name = next((d['name'] for d in menu if d['dish_id'] == r['dish_id']), '')
            user_reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews, username=CURRENT_USER)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    menu = load_menu()
    dishes = [{'dish_id':d['dish_id'], 'name': d['name']} for d in menu]
    if request.method == 'GET':
        return render_template('write_review.html', dishes=dishes)

    select_dish_str = request.form.get('select_dish', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    error_message = None
    success_message = None

    try:
        select_dish = int(select_dish_str)
    except:
        error_message = 'Invalid dish selection.'
        return render_template('write_review.html', dishes=dishes, error_message=error_message)

    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError
    except:
        error_message = 'Rating must be between 1 and 5.'
        return render_template('write_review.html', dishes=dishes, error_message=error_message)

    if not review_text:
        error_message = 'Review text cannot be empty.'
        return render_template('write_review.html', dishes=dishes, error_message=error_message)

    reviews = load_reviews()
    max_review_id = max([r['review_id'] for r in reviews], default=0)
    new_review_id = max_review_id + 1
    new_review = {
        'review_id': new_review_id,
        'username': CURRENT_USER,
        'dish_id': select_dish,
        'rating': rating,
        'review_text': review_text,
        'review_date': datetime.now().strftime('%Y-%m-%d')
    }
    reviews.append(new_review)
    write_reviews(reviews)

    success_message = 'Review submitted successfully.'
    return render_template('write_review.html', dishes=dishes, success_message=success_message)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USER)
    if request.method == 'GET':
        if not user:
            return "User not found", 404
        user_profile = {'username': user['username'], 'email': user['email']}
        return render_template('profile.html', user_profile=user_profile)

    profile_email = request.form.get('profile_email', '').strip()
    if not profile_email:
        if not user:
            return "User not found", 404
        user_profile = {'username': user['username'], 'email': user['email']}
        return render_template('profile.html', user_profile=user_profile)

    if user:
        user['email'] = profile_email
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['full_name']])
                f.write(line+'\n')

    user_profile = {'username': CURRENT_USER, 'email': profile_email}
    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    app.run(debug=True)
