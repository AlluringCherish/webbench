from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Simulate logged in user
CURRENT_USER = 'john_diner'

# --- Helper functions for file I/O and data parsing ---

def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
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
    dishes = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 8:
                    dish = {
                        'dish_id': int(parts[0]),
                        'name': parts[1],
                        'category': parts[2],
                        'price': float(parts[3]),
                        'description': parts[4],
                        'ingredients': parts[5],
                        'dietary': parts[6],
                        'avg_rating': float(parts[7])
                    }
                    dishes.append(dish)
    return dishes

def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 10:
                    reservation = {
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
                    reservations.append(reservation)
    return reservations

def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
            f.write(line)

def read_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
                    w = {
                        'waitlist_id': int(parts[0]),
                        'username': parts[1],
                        'party_size': int(parts[2]),
                        'join_time': parts[3],
                        'status': parts[4]
                    }
                    waitlist.append(w)
    return waitlist

def write_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n"
            f.write(line)

def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 6:
                    review = {
                        'review_id': int(parts[0]),
                        'username': parts[1],
                        'dish_id': int(parts[2]),
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    return reviews

def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)

# --- Routes ---

@app.route('/')
def dashboard():
    users = read_users()
    user = users.get(CURRENT_USER, {})
    return render_template('dashboard.html', username=user.get('full_name', CURRENT_USER))

@app.route('/menu')
def menu():
    dishes = read_menu()
    return render_template('menu.html', dishes=dishes)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    dishes = read_menu()
    dish = next((d for d in dishes if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest-name')
        party_size = int(request.form.get('party-size'))
        reservation_date = request.form.get('reservation-date')
        # For simplicity, we assign default phone and email from user
        users = read_users()
        user = users.get(CURRENT_USER, {})
        phone = user.get('phone', '')
        email = user.get('email', '')
        reservations = read_reservations()
        new_id = max([r['reservation_id'] for r in reservations], default=0) + 1
        new_reservation = {
            'reservation_id': new_id,
            'username': CURRENT_USER,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': reservation_date,
            'time': '19:00',
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        write_reservations(reservations)
        return redirect(url_for('dashboard'))
    return render_template('make_reservation.html')

@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = read_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USER and r['status'] == 'Upcoming']
    if request.method == 'POST':
        cancel_id = request.form.get('cancel_id')
        if cancel_id:
            cancel_id = int(cancel_id)
            for r in reservations:
                if r['reservation_id'] == cancel_id and r['username'] == CURRENT_USER:
                    r['status'] = 'Cancelled'
            write_reservations(reservations)
            return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist_data = read_waitlist()
    user_positions = [w for w in waitlist_data if w['username'] == CURRENT_USER and w['status'] == 'Active']
    user_position = None
    if user_positions:
        user_position = sorted(user_positions, key=lambda w: w['join_time'])[0]
        position_index = sorted([w for w in waitlist_data if w['status'] == 'Active'], key=lambda w: w['join_time']).index(user_position) + 1
    else:
        position_index = None

    if request.method == 'POST':
        party_size = int(request.form.get('waitlist-party-size'))
        if not user_positions:
            new_id = max([w['waitlist_id'] for w in waitlist_data], default=0) + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_waitlist = {
                'waitlist_id': new_id,
                'username': CURRENT_USER,
                'party_size': party_size,
                'join_time': now_str,
                'status': 'Active'
            }
            waitlist_data.append(new_waitlist)
            write_waitlist(waitlist_data)
            return redirect(url_for('waitlist'))

    return render_template('waitlist.html', user_position=position_index)

@app.route('/my_reviews')
def my_reviews():
    reviews = read_reviews()
    dishes = read_menu()
    # Filter user reviews
    user_reviews = [r for r in reviews if r['username'] == CURRENT_USER]
    # Map dish names
    for r in user_reviews:
        dish = next((d for d in dishes if d['dish_id'] == r['dish_id']), None)
        r['dish_name'] = dish['name'] if dish else 'Unknown'
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    dishes = read_menu()
    if request.method == 'POST':
        dish_id = int(request.form.get('select-dish'))
        rating = int(request.form.get('rating-input'))
        review_text = request.form.get('review-text')
        reviews = read_reviews()
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_id,
            'username': CURRENT_USER,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today
        }
        reviews.append(new_review)
        write_reviews(reviews)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', dishes=dishes)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USER, {})
    if request.method == 'POST':
        email = request.form.get('profile-email')
        if user:
            user['email'] = email
            # Write back all users
            path = os.path.join(DATA_DIR, 'users.txt')
            with open(path, 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n"
                    f.write(line)
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)
