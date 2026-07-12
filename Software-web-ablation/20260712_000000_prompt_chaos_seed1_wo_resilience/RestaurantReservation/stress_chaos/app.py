from flask import Flask, redirect, url_for, render_template, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility function to load users

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    username, email, phone, full_name = parts[0], parts[1], parts[2], parts[3]
                    users[username] = {
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'full_name': full_name
                    }
    except FileNotFoundError:
        pass
    return users

# Utility function to load menu

def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    dish_id = int(parts[0])
                    name = parts[1]
                    category = parts[2]
                    price = float(parts[3])
                    description = parts[4]
                    menu.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': price,
                        'description': description
                    })
    except FileNotFoundError:
        pass
    return menu

# Load reservations

def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id = int(parts[0])
                    username = parts[1]
                    guest_name = parts[2]
                    phone = parts[3]
                    email = parts[4]
                    party_size = int(parts[5])
                    date = parts[6]
                    time_ = parts[7]
                    special_requests = parts[8]
                    status = parts[9]
                    reservations.append({
                        'reservation_id': reservation_id,
                        'username': username,
                        'guest_name': guest_name,
                        'phone': phone,
                        'email': email,
                        'party_size': party_size,
                        'date': date,
                        'time': time_,
                        'special_requests': special_requests,
                        'status': status
                    })
    except FileNotFoundError:
        pass
    return reservations

# Load waitlist

def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
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

# Load reviews

def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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

# Save reservations

def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
            for r in reservations:
                line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving reservations: {e}")

# Save waitlist

def save_waitlist(waitlist):
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
            for w in waitlist:
                line = f"{w['waitlist_id']}|{w['username']}|{w['party_size']}|{w['join_time']}|{w['status']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving waitlist: {e}")

# Save reviews

def save_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['username']}|{r['dish_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving reviews: {e}")

# Save users

def save_users(users):
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for u in users.values():
                line = f"{u['username']}|{u['email']}|{u['phone']}|{u['full_name']}\n"
                f.write(line)
    except Exception as e:
        print(f"Error saving users: {e}")

# Utility: get next id

def get_next_id(items, key):
    if not items:
        return 1
    return max(item[key] for item in items) + 1

# Dummy current user for demonstration
CURRENT_USERNAME = 'johndoe'

# Get current user info

def get_current_user():
    users = load_users()
    return users.get(CURRENT_USERNAME, None)

# Routes

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    username = user['username'] if user else 'Guest'
    menu = load_menu()
    # Show featured dishes: the first 4 items
    featured_dishes = [
        {
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'price': dish['price'],
            'description': dish['description']
        } for dish in menu[:4]
    ]
    reservations = load_reservations()
    upcoming_reservations = [r for r in reservations if r['username'] == username and r['status'] == 'Upcoming'] if user else []
    return render_template('dashboard.html', user=user, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu_page():
    menu = load_menu()
    return render_template('menu.html', menu=menu)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = next((item for item in menu if item['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_raw = request.form.get('party_size', '').strip()
        reservation_date = request.form.get('reservation_date', '').strip()
        try:
            party_size = int(party_size_raw)
            if party_size < 1 or party_size > 10:
                raise ValueError("Party size must be between 1 and 10")
        except ValueError:
            return "Invalid party size", 400
        if not reservation_date:
            return "Reservation date is required", 400
        try:
            datetime.strptime(reservation_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD", 400

        username = user['username']
        phone = user['phone']
        email = user['email']

        reservations = load_reservations()
        new_reservation_id = get_next_id(reservations, 'reservation_id')
        reservation_time = '19:00'  # Default time

        new_reservation = {
            'reservation_id': new_reservation_id,
            'username': username,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': reservation_date,
            'time': reservation_time,
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        save_reservations(reservations)
        return redirect(url_for('my_reservations'))
    return render_template('make_reservation.html')

@app.route('/my_reservations')
def my_reservations():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == user['username']]
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    waitlist = load_waitlist()
    user_waitlist_active = False
    position = None
    sorted_waitlist = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda x: x['join_time'])
    for idx, entry in enumerate(sorted_waitlist):
        if entry['username'] == user['username']:
            user_waitlist_active = True
            position = idx + 1
            break
    if request.method == 'POST':
        party_size_raw = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_raw)
            if party_size < 1 or party_size > 10:
                raise ValueError("Party size must be between 1 and 10")
        except ValueError:
            return "Invalid party size", 400
        if not user_waitlist_active:
            next_id = get_next_id(waitlist, 'waitlist_id')
            join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': next_id,
                'username': user['username'],
                'party_size': party_size,
                'join_time': join_time,
                'status': 'Active'
            }
            waitlist.append(new_entry)
            save_waitlist(waitlist)
            return redirect(url_for('waitlist'))
    return render_template('waitlist.html', user_waitlist_active=user_waitlist_active, position=position)

@app.route('/my_reviews')
def my_reviews():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    username = user['username']
    menu = load_menu()
    dish_names = {dish['dish_id']: dish['name'] for dish in menu}
    reviews = load_reviews()
    user_reviews = [r for r in reviews if r['username'] == username]
    return render_template('my_reviews.html', reviews=user_reviews, dish_names=dish_names)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    menu = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
    if request.method == 'POST':
        dish_id_raw = request.form.get('dish_id', '').strip()
        rating_raw = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()
        try:
            dish_id = int(dish_id_raw)
            rating = int(rating_raw)
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
        except (ValueError, TypeError):
            return "Invalid input", 400
        if not review_text:
            return "Review text cannot be empty", 400
        reviews = load_reviews()
        new_review_id = get_next_id(reviews, 'review_id')
        review_date = datetime.now().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_review_id,
            'username': user['username'],
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews.append(new_review)
        save_reviews(reviews)
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', dishes=dishes)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        users = load_users()
        if new_email:
            users[user['username']]['email'] = new_email
            save_users(users)
            user['email'] = new_email  # update current session user data
    profile_data = {
        'username': user['username'],
        'email': user['email']
    }
    return render_template('profile.html', profile=profile_data)

if __name__ == '__main__':
    app.run(debug=True)
