from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Assume CURRENT_USER is a fixed user for demonstration
CURRENT_USER = 'john_diner'

# Helper functions to load and save users

def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    users[parts[0]] = {
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'full_name': parts[3]
                    }
    return users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            f.write(f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n")

# Helper functions to load and save menu

def load_menu():
    path = os.path.join(DATA_DIR, 'menu.txt')
    menu = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    try:
                        price = float(parts[3])
                    except ValueError:
                        price = 0.0
                    menu.append({
                        'dish_id': int(parts[0]),
                        'name': parts[1],
                        'category': parts[2],
                        'price': price,
                        'description': parts[4]
                    })
    return menu

# Helper functions for reservations

def load_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 10:
                    try:
                        reservations.append({
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
                        })
                    except ValueError:
                        continue
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            f.write(f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n")

# Helper functions for waitlist

def load_waitlist():
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    waitlist = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    try:
                        waitlist.append({
                            'waitlist_id': int(parts[0]),
                            'username': parts[1],
                            'party_size': int(parts[2]),
                            'join_time': float(parts[3]),
                            'status': parts[4]
                        })
                    except ValueError:
                        continue
    return waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            f.write(f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n")

# Helper functions for reviews

def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    try:
                        reviews.append({
                            'review_id': int(parts[0]),
                            'username': parts[1],
                            'dish_id': int(parts[2]),
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        })
                    except ValueError:
                        continue
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            f.write(f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    users = load_users()
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USER and r['status']!='Cancelled']
    return render_template('dashboard.html', user=users.get(CURRENT_USER), reservations=user_reservations)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    users = load_users()
    user = users.get(CURRENT_USER, {})
    if request.method == 'POST':
        reservations = load_reservations()
        new_id = max([r['reservation_id'] for r in reservations], default=0) + 1
        guest_name = request.form.get('guest_name', user.get('full_name', ''))
        phone = user.get('phone', '')
        email = user.get('email', '')
        party_size = int(request.form.get('party_size', 1))
        reservation_date = request.form.get('reservation_date', '')
        reservation_time = request.form.get('reservation_time', '')
        special_requests = request.form.get('special_requests', '')
        new_reservation = {
            'reservation_id': new_id,
            'username': CURRENT_USER,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': reservation_date,
            'time': reservation_time,
            'special_requests': special_requests,
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        save_reservations(reservations)
        return redirect(url_for('dashboard'))
    return render_template('make_reservation.html', user=user)

@app.route('/my_reservations')
def my_reservations():
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USER]
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USER:
            r['status'] = 'Cancelled'
            break
    save_reservations(reservations)
    return redirect(url_for('my_reservations'))

@app.route('/menu')
def menu():
    menu_items = load_menu()
    return render_template('menu.html', menu=menu_items)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_items = load_menu()
    dish = next((d for d in menu_items if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    users = load_users()
    menu_items = load_menu()
    if request.method == 'POST':
        reviews = load_reviews()
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        username = CURRENT_USER
        dish_id = int(request.form.get('dish_id', 0))
        rating = int(request.form.get('rating', 0))
        review_text = request.form.get('review_text', '')
        now_date = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_id,
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': now_date
        }
        reviews.append(new_review)
        save_reviews(reviews)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', dishes=menu_items)

@app.route('/my_reviews')
def my_reviews():
    reviews = load_reviews()
    users = load_users()
    menu_items = load_menu()
    user_reviews = [r for r in reviews if r['username'] == CURRENT_USER]
    # Attach dish name to review
    for r in user_reviews:
        dish = next((d for d in menu_items if d['dish_id'] == r['dish_id']), None)
        r['dish_name'] = dish['name'] if dish else 'Unknown'
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist = load_waitlist()
    if request.method == 'POST':
        party_size = int(request.form.get('party_size', 1))
        now_ts = datetime.now().timestamp()
        new_id = max([w['waitlist_id'] for w in waitlist], default=0) + 1
        waitlist.append({
            'waitlist_id': new_id,
            'username': CURRENT_USER,
            'party_size': party_size,
            'join_time': now_ts,
            'status': 'Active'
        })
        save_waitlist(waitlist)
        return redirect(url_for('waitlist'))
    active_entries = [w for w in waitlist if w['status'] == 'Active']
    active_entries.sort(key=lambda w: w['join_time'])
    return render_template('waitlist.html', waitlist=active_entries)

@app.route('/profile')
def profile():
    users = load_users()
    user = users.get(CURRENT_USER, {})
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    users = load_users()
    user = users.get(CURRENT_USER, {})
    if request.method == 'POST':
        email = request.form.get('email', user.get('email', ''))
        phone = request.form.get('phone', user.get('phone', ''))
        full_name = request.form.get('full_name', user.get('full_name', ''))
        users[CURRENT_USER] = {
            'username': CURRENT_USER,
            'email': email,
            'phone': phone,
            'full_name': full_name
        }
        save_users(users)
        return redirect(url_for('profile'))
    return render_template('update_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
