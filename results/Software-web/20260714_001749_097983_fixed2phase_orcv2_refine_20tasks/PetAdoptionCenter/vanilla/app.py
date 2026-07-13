from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

DATA_DIR = 'data'

# Helper functions

def read_file_lines(filename):
    'Read lines from a file or return empty if not exists'
    try:
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def write_file_lines(filename, lines):
    'Write lines to a file'
    with open(os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as f:
        f.writelines([line + '\n' for line in lines])

def get_new_id(lines):
    'Get new incremental ID based on first field of pipe separated lines'
    ids = []
    for line in lines:
        parts = line.split('|')
        if parts[0].isdigit():
            ids.append(int(parts[0]))
    return max(ids) + 1 if ids else 1

def get_username():
    'Return username currently in session or default user "john_doe"'
    return session.get('username', 'john_doe')

def load_pets():
    'Load pets list as dict with pet_id keys'
    pets = {}
    lines = read_file_lines('pets.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 11:
            (pet_id, name, species, breed, age, gender, size, description, shelter_id, status, date_added) = parts
            pets[pet_id] = {
                'pet_id': pet_id, 'name': name, 'species': species, 'breed': breed,
                'age': age, 'gender': gender, 'size': size, 'description': description,
                'shelter_id': shelter_id, 'status': status, 'date_added': date_added
            }
    return pets

def load_users():
    'Load users dictionary keyed by username'
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            username, email, phone, address = parts
            users[username] = {
                'username': username, 'email': email, 'phone': phone, 'address': address
            }
    return users

def load_applications():
    'Load applications list'
    apps = []
    lines = read_file_lines('applications.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 13:
            (application_id, username, pet_id, applicant_name, phone, address, housing_type,
             has_yard, other_pets, experience, reason, status, date_submitted) = parts
            apps.append({
                'application_id': application_id, 'username': username, 'pet_id': pet_id,
                'applicant_name': applicant_name, 'phone': phone, 'address': address,
                'housing_type': housing_type, 'has_yard': has_yard, 'other_pets': other_pets,
                'experience': experience, 'reason': reason, 'status': status, 'date_submitted': date_submitted
            })
    return apps

def load_favorites(username):
    'Load favorite pets for username'
    favs = []
    lines = read_file_lines('favorites.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 3:
            u, pet_id, date_added = parts
            if u == username:
                favs.append(pet_id)
    return favs

def load_messages(username):
    'Load conversations and messages involving username'
    conv = {}
    lines = read_file_lines('messages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 7:
            message_id, sender, recipient, subject, content, timestamp, is_read = parts
            if sender == username or recipient == username:
                key = sender if sender != username else recipient
                conv.setdefault(key, []).append({
                    'message_id': message_id, 'sender': sender, 'recipient': recipient,
                    'subject': subject, 'content': content, 'timestamp': timestamp, 'is_read': is_read == 'true'
                })
    return conv

def load_shelters():
    'Load shelters dict keyed by shelter_id'
    shelters = {}
    lines = read_file_lines('shelters.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            shelter_id, name, address, phone, email = parts
            shelters[shelter_id] = {
                'shelter_id': shelter_id, 'name': name, 'address': address, 'phone': phone, 'email': email
            }
    return shelters

# Home / Dashboard
@app.route('/')
def dashboard():
    pets = load_pets()
    featured_pets = [pet for pet in pets.values() if pet['status'] == 'Available'][:5]
    return render_template('dashboard.html', featured_pets=featured_pets)

# Pet Listings
@app.route('/pets')
def pet_listings():
    pets = load_pets()
    species_filter = request.args.get('species', 'All')
    search_term = request.args.get('search', '').lower()
    filtered = []
    for pet in pets.values():
        if species_filter != 'All' and pet['species'] != species_filter:
            continue
        if search_term and search_term not in pet['name'].lower():
            continue
        if pet['status'] != 'Available':
            continue
        filtered.append(pet)
    return render_template('pet_listings.html', pets=filtered, species_filter=species_filter, search_term=search_term)

# Pet Details
@app.route('/pets/<pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        return 'Pet not found', 404
    return render_template('pet_details.html', pet=pet)

# Add Pet (Admin only)
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if not session.get('is_admin', False):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        pets = load_pets()
        new_id = str(get_new_id(read_file_lines('pets.txt')))
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '')
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '')
        size = request.form.get('pet-size-input', '')
        description = request.form.get('pet-description-input', '').strip()
        shelter_id = '1'  # Default shelter for simplicity
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')
        new_line = '|'.join([new_id, name, species, breed, age, gender, size, description, shelter_id, status, date_added])
        lines = read_file_lines('pets.txt')
        lines.append(new_line)
        write_file_lines('pets.txt', lines)
        return redirect(url_for('pet_listings'))
    return render_template('add_pet.html')

# Adoption Application
@app.route('/apply/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        return 'Pet not found', 404
    if request.method == 'POST':
        lines = read_file_lines('applications.txt')
        new_id = str(get_new_id(lines))
        username = get_username()
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        address = ''
        housing_type = request.form.get('housing-type', '')
        # For simplicity, some fields are left empty
        has_yard = ''
        other_pets = ''
        experience = ''
        reason = request.form.get('reason', '').strip()
        status = 'Pending'
        date_submitted = datetime.now().strftime('%Y-%m-%d')
        new_line = '|'.join([new_id, username, pet_id, applicant_name, phone, address, housing_type, has_yard, other_pets, experience, reason, status, date_submitted])
        lines.append(new_line)
        write_file_lines('applications.txt', lines)
        return redirect(url_for('my_applications'))
    return render_template('application.html', pet=pet)

# My Applications
@app.route('/my_applications')
def my_applications():
    username = get_username()
    apps = load_applications()
    status_filter = request.args.get('status', 'All')
    filtered_apps = []
    pets = load_pets()
    for app in apps:
        if app['username'] != username:
            continue
        if status_filter != 'All' and app['status'] != status_filter:
            continue
        # Add pet name for display
        app['pet_name'] = pets.get(app['pet_id'], {}).get('name', 'Unknown')
        filtered_apps.append(app)
    return render_template('my_applications.html', applications=filtered_apps, status_filter=status_filter)

# Favorites
@app.route('/favorites')
def favorites():
    username = get_username()
    pets = load_pets()
    favorite_pet_ids = load_favorites(username)
    favorite_pets = [pets[pid] for pid in favorite_pet_ids if pid in pets and pets[pid]['status'] == 'Available']
    return render_template('favorites.html', pets=favorite_pets)

# Messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = get_username()
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject', '')
        content = request.form.get('content', '')
        lines = read_file_lines('messages.txt')
        new_id = str(get_new_id(lines))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_read = 'false'
        new_line = '|'.join([new_id, username, recipient, subject, content, timestamp, is_read])
        lines.append(new_line)
        write_file_lines('messages.txt', lines)
        return redirect(url_for('messages'))
    conversations = load_messages(username)
    return render_template('messages.html', conversations=conversations, username=username)

# User Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_username()
    users = load_users()
    user = users.get(username)
    if not user:
        return 'User not found', 404
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        # Update user email
        user['email'] = email
        # Save back to file
        lines = read_file_lines('users.txt')
        new_lines = []
        for line in lines:
            parts = line.split('|')
            if parts[0] == username:
                parts[1] = email
                new_lines.append('|'.join(parts))
            else:
                new_lines.append(line)
        write_file_lines('users.txt', new_lines)
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

# Admin Panel (Admin only)
@app.route('/admin')
def admin_panel():
    if not session.get('is_admin', False):
        return redirect(url_for('dashboard'))
    # Pending Applications
    apps = load_applications()
    pending_apps = [app for app in apps if app['status'] == 'Pending']
    pets = load_pets()
    shelters = load_shelters()
    # All pets
    all_pets = list(pets.values())
    return render_template('admin_panel.html', pending_apps=pending_apps, pets=all_pets, shelters=shelters)

# Run the app only if script executed
if __name__ == '__main__':
    # For demonstration, set dummy session user and admin flag
    with app.test_request_context():
        session['username'] = 'john_doe'
        session['is_admin'] = True
    app.run(debug=True)
