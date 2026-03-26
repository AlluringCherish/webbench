from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read and write data files

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 4:
                username, email, phone, full_name = fields
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'full_name': full_name
                }
    return users

def load_menu():
    menu = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if not os.path.exists(path):
        return menu
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 8:
                try:
                    dish_id = int(fields[0])
                    price = float(fields[3])
                    avg_rating = float(fields[7])
                    menu.append({
                        'dish_id': dish_id,
                        'name': fields[1],
                        'category': fields[2],
                        'price': price,
                        'description': fields[4],
                        'ingredients': fields[5],
                        'dietary': fields[6],
                        'avg_rating': avg_rating
                    })
                except ValueError:
                    pass
    return menu

def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 10:
                try:
                    reservation_id = int(fields[0])
                    party_size = int(fields[5])
                    reservations.append({
                        'reservation_id': reservation_id,
                        'username': fields[1],
                        'guest_name': fields[2],
                        'phone': fields[3],
                        'email': fields[4],
                        'party_size': party_size,
                        'date': fields[6],
                        'time': fields[7],
                        'special_requests': fields[8],
                        'status': fields[9]
                    })
                except ValueError:
                    pass
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
            f.write(line)

def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if not os.path.exists(path):
        return waitlist
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 5:
                try:
                    waitlist_id = int(fields[0])
                    party_size = int(fields[2])
                    waitlist.append({
                        'waitlist_id': waitlist_id,
                        'username': fields[1],
                        'party_size': party_size,
                        'join_time': fields[3],
                        'status': fields[4]
                    })
                except ValueError:
                    pass
    return waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n"
            f.write(line)

def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('|')
            if len(fields) == 6:
                try:
                    review_id = int(fields[0])
                    dish_id = int(fields[2])
                    rating = int(fields[3])
                    reviews.append({
                        'review_id': review_id,
                        'username': fields[1],
                        'dish_id': dish_id,
                        'rating': rating,
                        'review_text': fields[4],
                        'review_date': fields[5]
                    })
                except ValueError:
                    pass
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)

# Current logged-in user
CURRENT_USERNAME = 'john_diner'

# Root route redirects to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# /dashboard GET
@app.route('/dashboard')
def dashboard():
    username = CURRENT_USERNAME
    menu = load_menu()
    featured_dishes = []
    for d in menu[:3]:
        featured_dishes.append({
            'dish_id': d['dish_id'],
            'name': d['name'],
            'price': d['price'],
            'description': d['description']
        })
    reservations = load_reservations()
    upcoming_reservations = []
    for r in reservations:
        if r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            upcoming_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })
    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)

# /menu GET
@app.route('/menu')
def menu():
    menu_data = load_menu()
    menus = []
    for dish in menu_data:
        menus.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'category': dish['category'],
            'price': dish['price'],
            'description': dish['description'],
            'dietary': dish['dietary'],
            'avg_rating': dish['avg_rating']
        })
    return render_template('menu.html', menus=menus)

# /dish/<int:dish_id> GET
@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = None
    for d in menu:
        if d['dish_id'] == dish_id:
            dish = {
                'dish_id': d['dish_id'],
                'name': d['name'],
                'price': d['price'],
                'description': d['description']
            }
            break
    if dish is None:
        return redirect(url_for('menu'))
    return render_template('dish_details.html', dish=dish)

# /make-reservation GET
@app.route('/make-reservation', methods=['GET'])
def make_reservation():
    return render_template('make_reservation.html')

# /make-reservation POST
@app.route('/make-reservation', methods=['POST'])
def submit_reservation():
    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '').strip()
    reservation_date = request.form.get('reservation_date', '').strip()

    if not guest_name or not party_size_str or not reservation_date:
        return redirect(url_for('make_reservation'))

    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            return redirect(url_for('make_reservation'))
    except ValueError:
        return redirect(url_for('make_reservation'))

    try:
        datetime.strptime(reservation_date, '%Y-%m-%d')
    except ValueError:
        return redirect(url_for('make_reservation'))

    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if user is None:
        return redirect(url_for('dashboard'))

    reservations = load_reservations()
    new_id = max((r['reservation_id'] for r in reservations), default=0) + 1
    new_reservation = {
        'reservation_id': new_id,
        'username': CURRENT_USERNAME,
        'guest_name': guest_name,
        'phone': user['phone'],
        'email': user['email'],
        'party_size': party_size,
        'date': reservation_date,
        'time': '19:00',
        'special_requests': '',
        'status': 'Upcoming'
    }
    reservations.append(new_reservation)
    save_reservations(reservations)

    return render_template('reservation_confirmation.html', reservation=new_reservation)

# /my-reservations GET
@app.route('/my-reservations')
def my_reservations():
    reservations = load_reservations()
    user_res = []
    for r in reservations:
        if r['username'] == CURRENT_USERNAME:
            user_res.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_res)

# /cancel-reservation/<int:reservation_id> POST
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    modified = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            modified = True
            break
    if modified:
        save_reservations(reservations)
    return redirect(url_for('my_reservations'))

# /waitlist GET
@app.route('/waitlist', methods=['GET'])
def waitlist():
    waitlist = load_waitlist()
    active = [w for w in waitlist if w['status'] == 'Active']
    active_sorted = sorted(active, key=lambda x: x['join_time'])
    user_pos = None
    for i, w in enumerate(active_sorted, 1):
        if w['username'] == CURRENT_USERNAME:
            user_pos = i
            break
    return render_template('waitlist.html', user_position=user_pos)

# /waitlist POST
@app.route('/waitlist', methods=['POST'])
def join_waitlist():
    party_size_str = request.form.get('party_size', '').strip()
    try:
        party_size = int(party_size_str)
        if party_size < 1:
            return redirect(url_for('waitlist'))
    except ValueError:
        return redirect(url_for('waitlist'))

    waitlist = load_waitlist()
    for w in waitlist:
        if w['username'] == CURRENT_USERNAME and w['status'] == 'Active':
            return redirect(url_for('waitlist'))

    new_id = max((w['waitlist_id'] for w in waitlist), default=0) + 1
    join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = {
        'waitlist_id': new_id,
        'username': CURRENT_USERNAME,
        'party_size': party_size,
        'join_time': join_time,
        'status': 'Active'
    }
    waitlist.append(new_entry)
    save_waitlist(waitlist)
    return redirect(url_for('waitlist'))

# /my-reviews GET
@app.route('/my-reviews')
def my_reviews():
    reviews = load_reviews()
    menu = load_menu()
    dish_map = {d['dish_id']: d['name'] for d in menu}
    user_reviews = []
    for r in reviews:
        if r['username'] == CURRENT_USERNAME:
            user_reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_map.get(r['dish_id'], 'Unknown Dish'),
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

# /write-review GET
@app.route('/write-review', methods=['GET'])
def write_review():
    menu = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
    return render_template('write_review.html', dishes=dishes)

# /write-review POST
@app.route('/write-review', methods=['POST'])
def submit_review():
    dish_id_str = request.form.get('dish_id', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()
    try:
        dish_id = int(dish_id_str)
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            return redirect(url_for('write_review'))
    except ValueError:
        return redirect(url_for('write_review'))
    menu = load_menu()
    if not any(d['dish_id'] == dish_id for d in menu):
        return redirect(url_for('write_review'))
    reviews = load_reviews()
    new_id = max((r['review_id'] for r in reviews), default=0) + 1
    review_date = datetime.now().strftime('%Y-%m-%d')
    new_review = {
        'review_id': new_id,
        'username': CURRENT_USERNAME,
        'dish_id': dish_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }
    reviews.append(new_review)
    save_reviews(reviews)
    return redirect(url_for('my_reviews'))

# /profile GET
@app.route('/profile', methods=['GET'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if not user:
        return redirect(url_for('dashboard'))
    return render_template('profile.html', username=CURRENT_USERNAME, email=user['email'])

# /profile POST
@app.route('/profile', methods=['POST'])
def update_profile():
    email = request.form.get('email','').strip()
    if not email:
        return redirect(url_for('profile'))
    users = load_users()
    if CURRENT_USERNAME not in users:
        return redirect(url_for('dashboard'))
    users[CURRENT_USERNAME]['email'] = email
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            f.write(f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n")
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)
