'''
Backend implementation for PetAdoptionCenter web application using Flask.
Handles routing, data management with local text files, and all functionalities
as per requirements document.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management and flash messages
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
def append_file_line(filename, line):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
# Parsing functions for each data type
def parse_user(line):
    # username|email|phone|address
    parts = line.split('|')
    if len(parts) != 4:
        return None
    return {
        'username': parts[0],
        'email': parts[1],
        'phone': parts[2],
        'address': parts[3]
    }
def parse_pet(line):
    # pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
    parts = line.split('|')
    if len(parts) != 11:
        return None
    return {
        'pet_id': parts[0],
        'name': parts[1],
        'species': parts[2],
        'breed': parts[3],
        'age': parts[4],
        'gender': parts[5],
        'size': parts[6],
        'description': parts[7],
        'shelter_id': parts[8],
        'status': parts[9],
        'date_added': parts[10]
    }
def parse_application(line):
    # application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
    parts = line.split('|')
    if len(parts) != 13:
        return None
    return {
        'application_id': parts[0],
        'username': parts[1],
        'pet_id': parts[2],
        'applicant_name': parts[3],
        'phone': parts[4],
        'address': parts[5],
        'housing_type': parts[6],
        'has_yard': parts[7],
        'other_pets': parts[8],
        'experience': parts[9],
        'reason': parts[10],
        'status': parts[11],
        'date_submitted': parts[12]
    }
def parse_favorite(line):
    # username|pet_id|date_added
    parts = line.split('|')
    if len(parts) != 3:
        return None
    return {
        'username': parts[0],
        'pet_id': parts[1],
        'date_added': parts[2]
    }
def parse_message(line):
    # message_id|sender_username|recipient_username|subject|content|timestamp|is_read
    parts = line.split('|')
    if len(parts) != 7:
        return None
    return {
        'message_id': parts[0],
        'sender_username': parts[1],
        'recipient_username': parts[2],
        'subject': parts[3],
        'content': parts[4],
        'timestamp': parts[5],
        'is_read': parts[6].lower() == 'true'
    }
def parse_adoption_history(line):
    # history_id|username|pet_id|pet_name|adoption_date|shelter_id
    parts = line.split('|')
    if len(parts) != 6:
        return None
    return {
        'history_id': parts[0],
        'username': parts[1],
        'pet_id': parts[2],
        'pet_name': parts[3],
        'adoption_date': parts[4],
        'shelter_id': parts[5]
    }
def parse_shelter(line):
    # shelter_id|name|address|phone|email
    parts = line.split('|')
    if len(parts) != 5:
        return None
    return {
        'shelter_id': parts[0],
        'name': parts[1],
        'address': parts[2],
        'phone': parts[3],
        'email': parts[4]
    }
# Data loading functions
def load_users():
    lines = read_file_lines('users.txt')
    return [parse_user(line) for line in lines if parse_user(line) is not None]
def load_pets():
    lines = read_file_lines('pets.txt')
    return [parse_pet(line) for line in lines if parse_pet(line) is not None]
def load_applications():
    lines = read_file_lines('applications.txt')
    return [parse_application(line) for line in lines if parse_application(line) is not None]
def load_favorites():
    lines = read_file_lines('favorites.txt')
    return [parse_favorite(line) for line in lines if parse_favorite(line) is not None]
def load_messages():
    lines = read_file_lines('messages.txt')
    return [parse_message(line) for line in lines if parse_message(line) is not None]
def load_adoption_history():
    lines = read_file_lines('adoption_history.txt')
    return [parse_adoption_history(line) for line in lines if parse_adoption_history(line) is not None]
def load_shelters():
    lines = read_file_lines('shelters.txt')
    return [parse_shelter(line) for line in lines if parse_shelter(line) is not None]
# Data saving functions
def save_users(users):
    lines = ['|'.join([u['username'], u['email'], u['phone'], u['address']]) for u in users]
    write_file_lines('users.txt', lines)
def save_pets(pets):
    lines = ['|'.join([
        p['pet_id'], p['name'], p['species'], p['breed'], p['age'], p['gender'], p['size'],
        p['description'], p['shelter_id'], p['status'], p['date_added']
    ]) for p in pets]
    write_file_lines('pets.txt', lines)
def save_applications(applications):
    lines = ['|'.join([
        a['application_id'], a['username'], a['pet_id'], a['applicant_name'], a['phone'], a['address'],
        a['housing_type'], a['has_yard'], a['other_pets'], a['experience'], a['reason'], a['status'], a['date_submitted']
    ]) for a in applications]
    write_file_lines('applications.txt', lines)
def save_favorites(favorites):
    lines = ['|'.join([f['username'], f['pet_id'], f['date_added']]) for f in favorites]
    write_file_lines('favorites.txt', lines)
def save_messages(messages):
    lines = ['|'.join([
        m['message_id'], m['sender_username'], m['recipient_username'], m['subject'], m['content'], m['timestamp'], 
        'true' if m['is_read'] else 'false'
    ]) for m in messages]
    write_file_lines('messages.txt', lines)
def save_adoption_history(history):
    lines = ['|'.join([
        h['history_id'], h['username'], h['pet_id'], h['pet_name'], h['adoption_date'], h['shelter_id']
    ]) for h in history]
    write_file_lines('adoption_history.txt', lines)
def save_shelters(shelters):
    lines = ['|'.join([s['shelter_id'], s['name'], s['address'], s['phone'], s['email']]) for s in shelters]
    write_file_lines('shelters.txt', lines)
# Helper functions
def get_next_id(items, id_field):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_field])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def get_pet_by_id(pet_id):
    pets = load_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None
def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None
def get_shelter_by_id(shelter_id):
    shelters = load_shelters()
    for shelter in shelters:
        if shelter['shelter_id'] == shelter_id:
            return shelter
    return None
def filter_pets(pets, species=None, search_name=None, status='Available'):
    filtered = []
    for pet in pets:
        if status and pet['status'] != status:
            continue
        if species and species != 'All' and pet['species'] != species:
            continue
        if search_name and search_name.lower() not in pet['name'].lower():
            continue
        filtered.append(pet)
    return filtered
def get_featured_pets():
    pets = load_pets()
    available_pets = [p for p in pets if p['status'] == 'Available']
    # Sort by date_added descending
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    return available_pets[:5]
def get_user_applications(username, status_filter=None):
    applications = load_applications()
    user_apps = [a for a in applications if a['username'] == username]
    if status_filter and status_filter != 'All':
        user_apps = [a for a in user_apps if a['status'] == status_filter]
    return user_apps
def get_user_favorites(username):
    favorites = load_favorites()
    user_favs = [f for f in favorites if f['username'] == username]
    fav_pets = []
    for fav in user_favs:
        pet = get_pet_by_id(fav['pet_id'])
        if pet:
            fav_pets.append(pet)
    return fav_pets
def get_user_messages(username):
    messages = load_messages()
    # Return messages where user is sender or recipient
    user_msgs = [m for m in messages if m['sender_username'] == username or m['recipient_username'] == username]
    # Sort by timestamp ascending
    user_msgs.sort(key=lambda x: x['timestamp'])
    return user_msgs
def get_conversations(username):
    messages = load_messages()
    conversations = {}
    for m in messages:
        if m['sender_username'] == username:
            other = m['recipient_username']
        elif m['recipient_username'] == username:
            other = m['sender_username']
        else:
            continue
        if other not in conversations:
            conversations[other] = []
        conversations[other].append(m)
    # Sort messages in each conversation by timestamp ascending
    for conv in conversations.values():
        conv.sort(key=lambda x: x['timestamp'])
    return conversations
def mark_messages_read(username, other_username):
    messages = load_messages()
    changed = False
    for m in messages:
        if m['sender_username'] == other_username and m['recipient_username'] == username and not m['is_read']:
            m['is_read'] = True
            changed = True
    if changed:
        save_messages(messages)
def is_admin(username):
    # For simplicity, admin users are those with username 'admin_user'
    return username == 'admin_user'
# Session management helpers
def get_logged_in_username():
    return session.get('username')
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_logged_in_username():
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = get_logged_in_username()
        if not username or not is_admin(username):
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Simple login for demo: user enters username, if exists, logs in
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Please enter a username.', 'warning')
            return render_template('login.html')
        user = get_user_by_username(username)
        if user:
            session['username'] = username
            flash(f'Logged in as {username}.', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard'))
        else:
            flash('User not found.', 'danger')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))
@app.route('/')
def dashboard():
    '''
    Dashboard page showing featured pets, recent activities, navigation.
    '''
    featured_pets = get_featured_pets()
    username = get_logged_in_username()
    return render_template('dashboard.html', 
                           featured_pets=featured_pets,
                           username=username)
@app.route('/pets')
def pet_listings():
    '''
    Pet Listings page with filtering and search.
    '''
    species = request.args.get('species', 'All')
    search_name = request.args.get('search', '').strip()
    pets = load_pets()
    filtered_pets = filter_pets(pets, species=species, search_name=search_name, status='Available')
    username = get_logged_in_username()
    return render_template('pet_listings.html',
                           pets=filtered_pets,
                           species_filter=species,
                           search_name=search_name,
                           username=username)
@app.route('/pets/<pet_id>')
def pet_details(pet_id):
    '''
    Pet Details page showing detailed info about a pet.
    '''
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'danger')
        return redirect(url_for('pet_listings'))
    username = get_logged_in_username()
    return render_template('pet_details.html', pet=pet, username=username)
@app.route('/add_pet', methods=['GET', 'POST'])
@admin_required
def add_pet():
    '''
    Add Pet page for shelter administrators.
    '''
    if request.method == 'POST':
        # Collect form data
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()
        shelter_id = '1'  # For simplicity, assign shelter_id=1 or admin's shelter if extended
        if not all([name, species, breed, age, gender, size, description]):
            flash('All fields are required.', 'warning')
            return render_template('add_pet.html')
        pets = load_pets()
        pet_id = get_next_id(pets, 'pet_id')
        date_added = datetime.now().strftime('%Y-%m-%d')
        new_pet = {
            'pet_id': pet_id,
            'name': name,
            'species': species,
            'breed': breed,
            'age': age,
            'gender': gender,
            'size': size,
            'description': description,
            'shelter_id': shelter_id,
            'status': 'Available',
            'date_added': date_added
        }
        pets.append(new_pet)
        save_pets(pets)
        flash(f'Pet "{name}" added successfully.', 'success')
        return redirect(url_for('dashboard'))
    username = get_logged_in_username()
    return render_template('add_pet.html', username=username)
@app.route('/apply/<pet_id>', methods=['GET', 'POST'])
@login_required
def adoption_application(pet_id):
    '''
    Adoption Application page for users to submit applications.
    '''
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'danger')
        return redirect(url_for('pet_listings'))
    username = get_logged_in_username()
    user = get_user_by_username(username)
    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        has_yard = request.form.get('has-yard', 'No').strip()
        other_pets = request.form.get('other-pets', '').strip()
        experience = request.form.get('experience', '').strip()
        if not all([applicant_name, phone, housing_type, reason]):
            flash('Please fill in all required fields.', 'warning')
            return render_template('adoption_application.html', pet=pet, username=username)
        applications = load_applications()
        application_id = get_next_id(applications, 'application_id')
        date_submitted = datetime.now().strftime('%Y-%m-%d')
        new_app = {
            'application_id': application_id,
            'username': username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': phone,
            'address': user['address'] if user else '',
            'housing_type': housing_type,
            'has_yard': has_yard,
            'other_pets': other_pets,
            'experience': experience,
            'reason': reason,
            'status': 'Pending',
            'date_submitted': date_submitted
        }
        applications.append(new_app)
        save_applications(applications)
        flash('Adoption application submitted successfully.', 'success')
        return redirect(url_for('my_applications'))
    return render_template('adoption_application.html', pet=pet, username=username)
@app.route('/my_applications')
@login_required
def my_applications():
    '''
    My Applications page showing user's submitted adoption applications.
    '''
    username = get_logged_in_username()
    status_filter = request.args.get('status', 'All')
    applications = get_user_applications(username, status_filter=status_filter)
    # Attach pet name to each application
    for app_ in applications:
        pet = get_pet_by_id(app_['pet_id'])
        app_['pet_name'] = pet['name'] if pet else 'Unknown'
    return render_template('my_applications.html', applications=applications, status_filter=status_filter, username=username)
@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    '''
    Favorites page showing user's favorite pets.
    POST to add or remove favorites.
    '''
    username = get_logged_in_username()
    if request.method == 'POST':
        action = request.form.get('action')
        pet_id = request.form.get('pet_id')
        if not pet_id or action not in ['add', 'remove']:
            flash('Invalid request.', 'danger')
            return redirect(url_for('favorites'))
        favorites = load_favorites()
        if action == 'add':
            # Check if already favorite
            exists = any(f['username'] == username and f['pet_id'] == pet_id for f in favorites)
            if not exists:
                date_added = datetime.now().strftime('%Y-%m-%d')
                favorites.append({'username': username, 'pet_id': pet_id, 'date_added': date_added})
                save_favorites(favorites)
                flash('Pet added to favorites.', 'success')
            else:
                flash('Pet already in favorites.', 'info')
        elif action == 'remove':
            favorites = [f for f in favorites if not (f['username'] == username and f['pet_id'] == pet_id)]
            save_favorites(favorites)
            flash('Pet removed from favorites.', 'success')
        return redirect(url_for('favorites'))
    fav_pets = get_user_favorites(username)
    return render_template('favorites.html', pets=fav_pets, username=username)
@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    '''
    Messages page for viewing and sending messages to shelters.
    '''
    username = get_logged_in_username()
    conversations = get_conversations(username)
    selected_conversation = request.args.get('with')
    if request.method == 'POST':
        recipient = request.form.get('recipient_username')
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()
        if not recipient or not subject or not content:
            flash('Please fill in all fields to send a message.', 'warning')
            return redirect(url_for('messages', with=recipient))
        messages = load_messages()
        message_id = get_next_id(messages, 'message_id')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_message = {
            'message_id': message_id,
            'sender_username': username,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }
        messages.append(new_message)
        save_messages(messages)
        flash('Message sent.', 'success')
        return redirect(url_for('messages', with=recipient))
    # Mark messages as read in selected conversation
    if selected_conversation:
        mark_messages_read(username, selected_conversation)
    return render_template('messages.html', conversations=conversations, selected_conversation=selected_conversation, username=username)
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    '''
    User Profile page to view and edit profile info.
    '''
    username = get_logged_in_username()
    users = load_users()
    user = get_user_by_username(username)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.', 'warning')
            return render_template('user_profile.html', user=user, username=username)
        # Update user email
        for u in users:
            if u['username'] == username:
                u['email'] = email
                break
        save_users(users)
        flash('Profile updated.', 'success')
        return redirect(url_for('user_profile'))
    return render_template('user_profile.html', user=user, username=username)
@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    '''
    Admin Panel page to manage applications and pets.
    '''
    pets = load_pets()
    applications = load_applications()
    pending_apps = [a for a in applications if a['status'] == 'Pending']
    if request.method == 'POST':
        # Handle application status update or pet edit/delete
        action = request.form.get('action')
        if action == 'update_application':
            application_id = request.form.get('application_id')
            new_status = request.form.get('new_status')
            if application_id and new_status in ['Pending', 'Approved', 'Rejected']:
                for app_ in applications:
                    if app_['application_id'] == application_id:
                        app_['status'] = new_status
                        # If approved, update pet status to Pending or Adopted
                        if new_status == 'Approved':
                            pet = get_pet_by_id(app_['pet_id'])
                            if pet:
                                pet['status'] = 'Pending'
                                save_pets(pets)
                            # Add to adoption history
                            history = load_adoption_history()
                            history_id = get_next_id(history, 'history_id')
                            adoption_date = datetime.now().strftime('%Y-%m-%d')
                            pet_name = pet['name'] if pet else ''
                            shelter_id = pet['shelter_id'] if pet else ''
                            history.append({
                                'history_id': history_id,
                                'username': app_['username'],
                                'pet_id': app_['pet_id'],
                                'pet_name': pet_name,
                                'adoption_date': adoption_date,
                                'shelter_id': shelter_id
                            })
                            save_adoption_history(history)
                        save_applications(applications)
                        flash(f'Application {application_id} updated to {new_status}.', 'success')
                        break
            return redirect(url_for('admin_panel'))
        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            if pet_id:
                pets = [p for p in pets if p['pet_id'] != pet_id]
                save_pets(pets)
                flash(f'Pet {pet_id} deleted.', 'success')
            return redirect(url_for('admin_panel'))
        elif action == 'edit_pet':
            # For simplicity, redirect to add_pet page with pet data prefilled could be implemented
            flash('Edit pet functionality not implemented in this version.', 'info')
            return redirect(url_for('admin_panel'))
    username = get_logged_in_username()
    return render_template('admin_panel.html', pets=pets, pending_apps=pending_apps, username=username)
# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
# Run the app
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)