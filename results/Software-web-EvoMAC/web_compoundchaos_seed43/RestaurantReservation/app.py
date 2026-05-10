'''
RestaurantReservation Flask backend application.
Implements all required routes and logic for the restaurant reservation system,
including user profile, menu browsing, dish details, reservations, waitlist,
reviews, and profile update.
Data is stored in text files under 'data' directory with pipe-delimited format.
Frontend files (index.html, app.js, styles.css) are served as static files.
All API endpoints return JSON responses.
Author: EvoMAC Intelligent Agents
'''
import os
import json
import threading
from flask import (
    Flask, jsonify, request, send_from_directory, abort
)
from datetime import datetime
app = Flask(__name__, static_folder='static')
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
MENU_FILE = os.path.join(DATA_DIR, 'menu.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
WAITLIST_FILE = os.path.join(DATA_DIR, 'waitlist.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
# Lock for thread-safe file operations
file_lock = threading.Lock()
# Helper functions for file IO and parsing
def parse_pipe_file(filepath, keys):
    """
    Parse a pipe-delimited file into a list of dicts with given keys.
    Returns empty list if file does not exist or is empty.
    """
    if not os.path.exists(filepath):
        return []
    with file_lock, open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    data = []
    for line in lines:
        parts = line.split('|')
        if len(parts) < len(keys):
            # Skip malformed lines
            continue
        entry = {k: parts[i] for i, k in enumerate(keys)}
        data.append(entry)
    return data
def write_pipe_file(filepath, keys, data_list):
    """
    Write a list of dicts to a pipe-delimited file with given keys.
    Overwrites the file atomically.
    """
    temp_path = filepath + '.tmp'
    with file_lock, open(temp_path, 'w', encoding='utf-8') as f:
        for entry in data_list:
            line = '|'.join(str(entry.get(k, '')) for k in keys)
            f.write(line + '\n')
    os.replace(temp_path, filepath)
def generate_id(prefix):
    """
    Generate a unique ID string with given prefix.
    """
    import random
    import string
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}{rand_str}"
def get_current_user():
    """
    For simplicity, assume a fixed logged-in user 'jane_food'.
    In real app, implement authentication.
    """
    users = parse_pipe_file(USERS_FILE, ['username', 'email', 'phone', 'full_name'])
    for u in users:
        if u['username'] == 'jane_food':
            return u
    return None
def find_user(username):
    users = parse_pipe_file(USERS_FILE, ['username', 'email', 'phone', 'full_name'])
    for u in users:
        if u['username'] == username:
            return u
    return None
def find_dish(dish_id):
    menu = parse_pipe_file(MENU_FILE, ['dish_id', 'name', 'category', 'price', 'description', 'ingredients', 'dietary', 'avg_rating'])
    for d in menu:
        if d['dish_id'] == dish_id:
            return d
    return None
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return None
def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None
def serialize_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%Y-%m-%d')
    elif hasattr(date_obj, 'strftime'):
        return date_obj.strftime('%Y-%m-%d')
    return str(date_obj)
# Routes serving static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')
@app.route('/app.js')
def serve_appjs():
    return send_from_directory(app.static_folder, 'app.js')
@app.route('/styles.css')
def serve_styles():
    return send_from_directory(app.static_folder, 'styles.css')
# API routes
@app.route('/api/user/current', methods=['GET'])
def api_get_current_user():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    return jsonify(user)
@app.route('/api/user/profile', methods=['PUT'])
def api_update_profile():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    new_email = data['email'].strip()
    if not new_email:
        return jsonify({'error': 'Email cannot be empty'}), 400
    users = parse_pipe_file(USERS_FILE, ['username', 'email', 'phone', 'full_name'])
    updated = False
    for u in users:
        if u['username'] == user['username']:
            u['email'] = new_email
            updated = True
            break
    if not updated:
        return jsonify({'error': 'User not found'}), 404
    write_pipe_file(USERS_FILE, ['username', 'email', 'phone', 'full_name'], users)
    return jsonify({'message': 'Profile updated successfully'})
@app.route('/api/menu', methods=['GET'])
def api_get_menu():
    menu = parse_pipe_file(MENU_FILE, ['dish_id', 'name', 'category', 'price', 'description', 'ingredients', 'dietary', 'avg_rating'])
    return jsonify(menu)
@app.route('/api/menu/<dish_id>', methods=['GET'])
def api_get_dish(dish_id):
    dish = find_dish(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    return jsonify(dish)
@app.route('/api/reservations', methods=['POST'])
def api_make_reservation():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    guest_name = data.get('guest_name', '').strip()
    party_size = data.get('party_size')
    date_str = data.get('date', '').strip()
    special_requests = data.get('special_requests', '').strip()
    if not guest_name or not party_size or not date_str:
        return jsonify({'error': 'Guest name, party size, and date are required'}), 400
    try:
        party_size = int(party_size)
        if party_size < 1 or party_size > 10:
            raise ValueError
    except ValueError:
        return jsonify({'error': 'Party size must be an integer between 1 and 10'}), 400
    dt = parse_date(date_str)
    if not dt:
        return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400
    reservations = parse_pipe_file(RESERVATIONS_FILE, ['reservation_id', 'username', 'guest_name', 'phone', 'email', 'party_size', 'date', 'time', 'special_requests', 'status'])
    new_id = generate_id('res')
    new_reservation = {
        'reservation_id': new_id,
        'username': user['username'],
        'guest_name': guest_name,
        'phone': user.get('phone', ''),
        'email': user.get('email', ''),
        'party_size': str(party_size),
        'date': date_str,
        'time': '18:00',  # default time
        'special_requests': special_requests,
        'status': 'Upcoming'
    }
    reservations.append(new_reservation)
    write_pipe_file(RESERVATIONS_FILE, ['reservation_id', 'username', 'guest_name', 'phone', 'email', 'party_size', 'date', 'time', 'special_requests', 'status'], reservations)
    return jsonify({'message': 'Reservation made successfully', 'reservation_id': new_id}), 201
@app.route('/api/reservations/my', methods=['GET'])
def api_get_my_reservations():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    reservations = parse_pipe_file(RESERVATIONS_FILE, ['reservation_id', 'username', 'guest_name', 'phone', 'email', 'party_size', 'date', 'time', 'special_requests', 'status'])
    my_reservations = [r for r in reservations if r['username'] == user['username']]
    return jsonify(my_reservations)
@app.route('/api/reservations/<reservation_id>', methods=['DELETE'])
def api_cancel_reservation(reservation_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    reservations = parse_pipe_file(RESERVATIONS_FILE, ['reservation_id', 'username', 'guest_name', 'phone', 'email', 'party_size', 'date', 'time', 'special_requests', 'status'])
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id:
            if r['username'] != user['username']:
                return jsonify({'error': 'Unauthorized to cancel this reservation'}), 403
            if r['status'] != 'Upcoming':
                return jsonify({'error': 'Only upcoming reservations can be cancelled'}), 400
            r['status'] = 'Cancelled'
            found = True
            break
    if not found:
        return jsonify({'error': 'Reservation not found'}), 404
    write_pipe_file(RESERVATIONS_FILE, ['reservation_id', 'username', 'guest_name', 'phone', 'email', 'party_size', 'date', 'time', 'special_requests', 'status'], reservations)
    return jsonify({'message': 'Reservation cancelled successfully'})
@app.route('/api/waitlist/my', methods=['GET'])
def api_get_my_waitlist():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    waitlist = parse_pipe_file(WAITLIST_FILE, ['waitlist_id', 'username', 'party_size', 'join_time', 'status'])
    user_waitlist = [w for w in waitlist if w['username'] == user['username'] and w['status'] == 'Active']
    if not user_waitlist:
        return jsonify({})
    # Calculate position by join_time ascending
    active_waitlist = [w for w in waitlist if w['status'] == 'Active']
    active_waitlist.sort(key=lambda x: x['join_time'])
    position = 1
    for w in active_waitlist:
        if w['username'] == user['username']:
            break
        position += 1
    w = user_waitlist[0]
    return jsonify({
        'waitlist_id': w['waitlist_id'],
        'party_size': w['party_size'],
        'join_time': w['join_time'],
        'status': w['status'],
        'position': position
    })
@app.route('/api/waitlist', methods=['POST'])
def api_join_waitlist():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    data = request.get_json()
    if not data or 'party_size' not in data:
        return jsonify({'error': 'Party size is required'}), 400
    try:
        party_size = int(data['party_size'])
        if party_size < 1 or party_size > 10:
            raise ValueError()
    except Exception:
        return jsonify({'error': 'Invalid party size'}), 400
    waitlist = parse_pipe_file(WAITLIST_FILE, ['waitlist_id', 'username', 'party_size', 'join_time', 'status'])
    # Check if user already on waitlist active
    for w in waitlist:
        if w['username'] == user['username'] and w['status'] == 'Active':
            return jsonify({'error': 'You are already on the waitlist'}), 400
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_id = generate_id('w')
    new_entry = {
        'waitlist_id': new_id,
        'username': user['username'],
        'party_size': str(party_size),
        'join_time': now,
        'status': 'Active'
    }
    waitlist.append(new_entry)
    write_pipe_file(WAITLIST_FILE, ['waitlist_id', 'username', 'party_size', 'join_time', 'status'], waitlist)
    return jsonify({'message': 'Joined waitlist successfully', 'waitlist_id': new_id})
@app.route('/api/reviews/my', methods=['GET'])
def api_get_my_reviews():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    reviews = parse_pipe_file(REVIEWS_FILE, ['review_id', 'username', 'dish_id', 'rating', 'review_text', 'review_date'])
    my_reviews = [r for r in reviews if r['username'] == user['username']]
    return jsonify(my_reviews)
@app.route('/api/reviews', methods=['POST'])
def api_submit_review():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'No user logged in'}), 401
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    dish_id = data.get('dish_id')
    rating = data.get('rating')
    review_text = data.get('review_text', '').strip()
    if not dish_id or not rating or not review_text:
        return jsonify({'error': 'Dish, rating and review text are required'}), 400
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            raise ValueError()
    except Exception:
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
    dish = find_dish(dish_id)
    if not dish:
        return jsonify({'error': 'Dish not found'}), 404
    reviews = parse_pipe_file(REVIEWS_FILE, ['review_id', 'username', 'dish_id', 'rating', 'review_text', 'review_date'])
    new_id = generate_id('rev')
    today = datetime.now().strftime('%Y-%m-%d')
    new_review = {
        'review_id': new_id,
        'username': user['username'],
        'dish_id': dish_id,
        'rating': str(rating_int),
        'review_text': review_text,
        'review_date': today
    }
    reviews.append(new_review)
    write_pipe_file(REVIEWS_FILE, ['review_id', 'username', 'dish_id', 'rating', 'review_text', 'review_date'], reviews)
    return jsonify({'message': 'Review submitted successfully', 'review_id': new_id})
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)