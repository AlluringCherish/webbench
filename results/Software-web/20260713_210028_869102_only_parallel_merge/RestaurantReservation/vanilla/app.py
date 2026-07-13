from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

CURRENT_USERNAME = 'john_diner'

# Utility to load users

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, full_name = parts
                users[username] = {'username': username, 'email': email, 'phone': phone, 'full_name': full_name}
    return users

# Utility to load menu

def load_menu():
    dishes = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        dish_id, name, category, price, description, ingredients, dietary, avg_rating = parts
                        dishes.append({
                            'dish_id': int(dish_id),
                            'name': name,
                            'category': category,
                            'price': float(price),
                            'description': description,
                            'ingredients': ingredients,
                            'dietary': dietary,
                            'avg_rating': float(avg_rating)
                        })
    return dishes

# Utility to load reservations

def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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

# Utility to save reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}"
            f.write(line + '\n')

# Utility to load waitlist

def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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

# Utility to save waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}"
            f.write(line + '\n')

# Utility to load reviews

def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
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

# Utility to save reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}"
            f.write(line + '\n')

# Utility to save users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}"
            f.write(line + '\n')

@app.route('/')
def dashboard():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    expected_dishes = load_menu()[:3]
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming']
    return render_template('dashboard.html', username=user['full_name'] if user else CURRENT_USERNAME, featured_dishes=expected_dishes, upcoming_reservations=user_reservations)

@app.route('/menu')
def menu():
    dishes = load_menu()
    return render_template('menu.html', dishes=dishes)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    dishes = load_menu()
    dish = next((d for d in dishes if d['dish_id'] == dish_id), None)
    if not dish:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if request.method == 'POST':
        guest_name = request.form.get('guest-name', '')
        party_size = request.form.get('party-size', '')
        reservation_date = request.form.get('reservation-date', '')
        if not guest_name or not party_size or not reservation_date:
            return render_template('make_reservation.html', error='Please fill in all fields.')
        reservations = load_reservations()
        max_id = max([r['reservation_id'] for r in reservations], default=0) if reservations else 0
        new_reservation = {
            'reservation_id': max_id + 1,
            'username': CURRENT_USERNAME,
            'guest_name': guest_name,
            'phone': user['phone'] if user else '',
            'email': user['email'] if user else '',
            'party_size': int(party_size),
            'date': reservation_date,
            'time': '19:00',
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        save_reservations(reservations)
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    if request.method == 'POST':
        for r in user_reservations:
            btn_name = f'cancel-reservation-button-{r["reservation_id"]}'
            if btn_name in request.form:
                for res in reservations:
                    if res['reservation_id'] == r['reservation_id'] and res['status'] == 'Upcoming':
                        res['status'] = 'Cancelled'
                        save_reservations(reservations)
                        break
                return redirect(url_for('my_reservations'))
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist_entries = load_waitlist()
    user_entry = next((w for w in waitlist_entries if w['username'] == CURRENT_USERNAME and w['status'] == 'Active'), None)
    user_position = None
    if user_entry:
        active_waitlist = sorted([w for w in waitlist_entries if w['status'] == 'Active'], key=lambda x: x['join_time'])
        try:
            user_position = active_waitlist.index(user_entry) + 1
        except ValueError:
            user_position = None
    if request.method == 'POST':
        party_size = request.form.get('waitlist-party-size', '')
        if party_size:
            max_id = max([w['waitlist_id'] for w in waitlist_entries], default=0) if waitlist_entries else 0
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': max_id + 1,
                'username': CURRENT_USERNAME,
                'party_size': int(party_size),
                'join_time': now_str,
                'status': 'Active'
            }
            waitlist_entries.append(new_entry)
            save_waitlist(waitlist_entries)
            return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_position=user_position)

@app.route('/my-reviews')
def my_reviews():
    reviews = load_reviews()
    user_reviews = [r for r in reviews if r['username'] == CURRENT_USERNAME]
    dishes = load_menu()
    dish_dict = {d['dish_id']: d['name'] for d in dishes}
    for r in user_reviews:
        r['dish_name'] = dish_dict.get(r['dish_id'], 'Unknown Dish')
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    dishes = load_menu()
    if request.method == 'POST':
        dish_id = request.form.get('select-dish')
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text', '').strip()
        if not dish_id or not rating or not review_text:
            return render_template('write_review.html', dishes=dishes, error='Please fill in all fields.')
        try:
            dish_id_int = int(dish_id)
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError
        except:
            return render_template('write_review.html', dishes=dishes, error='Invalid input.')
        reviews = load_reviews()
        if reviews:
            new_id = max(r['review_id'] for r in reviews) + 1
        else:
            new_id = 1
        now_str = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_id,
            'username': CURRENT_USERNAME,
            'dish_id': dish_id_int,
            'rating': rating_int,
            'review_text': review_text,
            'review_date': now_str
        }
        reviews.append(new_review)
        save_reviews(reviews)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', dishes=dishes)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email and user:
            user['email'] = new_email
            save_users(users)
            return redirect(url_for('profile'))
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
