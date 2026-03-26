'''
Main backend application for PetAdoptionCenter web app.
Implements all routing, data handling, and business logic using Flask.
Data is stored in local text files under the 'data' directory.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from collections import defaultdict
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session and flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing pipe-delimited text files
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
        for line in lines:
            f.write(line + '\n')
# --- USERS ---
def load_users():
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            username, email, phone, address = parts
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users
def save_users(users):
    lines = []
    for u in users.values():
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    write_file_lines('users.txt', lines)
# --- PETS ---
def load_pets():
    pets = {}
    lines = read_file_lines('pets.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 11:
            pet_id = parts[0]
            pets[pet_id] = {
                'pet_id': pet_id,
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
    return pets
def save_pets(pets):
    lines = []
    for p in pets.values():
        line = '|'.join([
            p['pet_id'], p['name'], p['species'], p['breed'], p['age'],
            p['gender'], p['size'], p['description'], p['shelter_id'],
            p['status'], p['date_added']
        ])
        lines.append(line)
    write_file_lines('pets.txt', lines)
def get_next_pet_id(pets):
    if not pets:
        return '1'
    max_id = max(int(pid) for pid in pets.keys())
    return str(max_id + 1)
# --- APPLICATIONS ---
def load_applications():
    applications = {}
    lines = read_file_lines('applications.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 13:
            application_id = parts[0]
            applications[application_id] = {
                'application_id': application_id,
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
    return applications
def save_applications(applications):
    lines = []
    for a in applications.values():
        line = '|'.join([
            a['application_id'], a['username'], a['pet_id'], a['applicant_name'],
            a['phone'], a['address'], a['housing_type'], a['has_yard'],
            a['other_pets'], a['experience'], a['reason'], a['status'], a['date_submitted']
        ])
        lines.append(line)
    write_file_lines('applications.txt', lines)
def get_next_application_id(applications):
    if not applications:
        return '1'
    max_id = max(int(aid) for aid in applications.keys())
    return str(max_id + 1)
# --- FAVORITES ---
def load_favorites():
    favorites = []
    lines = read_file_lines('favorites.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 3:
            favorites.append({
                'username': parts[0],
                'pet_id': parts[1],
                'date_added': parts[2]
            })
    return favorites
def save_favorites(favorites):
    lines = []
    for f in favorites:
        line = '|'.join([f['username'], f['pet_id'], f['date_added']])
        lines.append(line)
    write_file_lines('favorites.txt', lines)
# --- MESSAGES ---
def load_messages():
    messages = {}
    lines = read_file_lines('messages.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 7:
            message_id = parts[0]
            messages[message_id] = {
                'message_id': message_id,
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6].lower() == 'true'
            }
    return messages
def save_messages(messages):
    lines = []
    for m in messages.values():
        line = '|'.join([
            m['message_id'], m['sender_username'], m['recipient_username'],
            m['subject'], m['content'], m['timestamp'], 'true' if m['is_read'] else 'false'
        ])
        lines.append(line)
    write_file_lines('messages.txt', lines)
def get_next_message_id(messages):
    if not messages:
        return '1'
    max_id = max(int(mid) for mid in messages.keys())
    return str(max_id + 1)
# --- ADOPTION HISTORY ---
def load_adoption_history():
    history = {}
    lines = read_file_lines('adoption_history.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            history_id = parts[0]
            history[history_id] = {
                'history_id': history_id,
                'username': parts[1],
                'pet_id': parts[2],
                'pet_name': parts[3],
                'adoption_date': parts[4],
                'shelter_id': parts[5]
            }
    return history
def save_adoption_history(history):
    lines = []
    for h in history.values():
        line = '|'.join([
            h['history_id'], h['username'], h['pet_id'], h['pet_name'],
            h['adoption_date'], h['shelter_id']
        ])
        lines.append(line)
    write_file_lines('adoption_history.txt', lines)
def get_next_history_id(history):
    if not history:
        return '1'
    max_id = max(int(hid) for hid in history.keys())
    return str(max_id + 1)
# --- SHELTERS ---
def load_shelters():
    shelters = {}
    lines = read_file_lines('shelters.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            shelter_id = parts[0]
            shelters[shelter_id] = {
                'shelter_id': shelter_id,
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            }
    return shelters
# --- Helper functions ---
def get_featured_pets(pets, limit=5):
    # Featured pets: Available pets sorted by date_added descending, limit 5
    available_pets = [p for p in pets.values() if p['status'].lower() == 'available']
    sorted_pets = sorted(available_pets, key=lambda x: x['date_added'], reverse=True)
    return sorted_pets[:limit]
def filter_pets(pets, species_filter='All', search_name=''):
    filtered = []
    search_name_lower = search_name.lower()
    for pet in pets.values():
        if pet['status'].lower() != 'available':
            continue
        if species_filter != 'All' and pet['species'].lower() != species_filter.lower():
            continue
        if search_name and search_name_lower not in pet['name'].lower():
            continue
        filtered.append(pet)
    return filtered
def get_user():
    # For simplicity, user is identified by session username
    username = session.get('username')
    if not username:
        return None
    users = load_users()
    return users.get(username)
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('dashboard'))
        if session['username'] != 'admin_user':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
# --- ROUTES ---
@app.route('/')
def dashboard():
    pets = load_pets()
    featured_pets = get_featured_pets(pets)
    # Recent activities: show recent applications by current user (if logged in)
    user = get_user()
    recent_applications = []
    if user:
        applications = load_applications()
        user_apps = [a for a in applications.values() if a['username'] == user['username']]
        recent_applications = sorted(user_apps, key=lambda x: x['date_submitted'], reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_pets=featured_pets,
                           recent_applications=recent_applications,
                           user=user)
@app.route('/pet_listings', methods=['GET', 'POST'])
def pet_listings():
    pets = load_pets()
    species_options = ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    species_filter = request.args.get('filter-species', 'All')
    search_name = request.args.get('search-input', '').strip()
    filtered_pets = filter_pets(pets, species_filter, search_name)
    return render_template('pet_listings.html',
                           pets=filtered_pets,
                           species_options=species_options,
                           selected_species=species_filter,
                           search_name=search_name,
                           user=get_user())
@app.route('/pet_details/<pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        flash('Pet not found.', 'danger')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet, user=get_user())
@app.route('/add_pet', methods=['GET', 'POST'])
@admin_required
def add_pet():
    if request.method == 'POST':
        pets = load_pets()
        pet_id = get_next_pet_id(pets)
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()
        shelter_id = '1'  # For simplicity, assign shelter_id 1 (could be extended)
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')
        if not name or not species or not breed or not age or not gender or not size or not description:
            flash('All fields are required.', 'warning')
            return render_template('add_pet.html', user=get_user())
        pets[pet_id] = {
            'pet_id': pet_id,
            'name': name,
            'species': species,
            'breed': breed,
            'age': age,
            'gender': gender,
            'size': size,
            'description': description,
            'shelter_id': shelter_id,
            'status': status,
            'date_added': date_added
        }
        save_pets(pets)
        flash(f'Pet "{name}" added successfully.', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('add_pet.html', user=get_user())
@app.route('/adoption_application/<pet_id>', methods=['GET', 'POST'])
@login_required
def adoption_application(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        flash('Pet not found.', 'danger')
        return redirect(url_for('pet_listings'))
    user = get_user()
    if request.method == 'POST':
        applications = load_applications()
        application_id = get_next_application_id(applications)
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        # Additional fields from requirements but not in form: has_yard, other_pets, experience
        # For simplicity, set defaults or empty
        has_yard = request.form.get('has-yard', 'No')
        other_pets = request.form.get('other-pets', 'None')
        experience = request.form.get('experience', 'None')
        if not applicant_name or not phone or not housing_type or not reason:
            flash('Please fill in all required fields.', 'warning')
            return render_template('adoption_application.html', pet=pet, user=user)
        date_submitted = datetime.now().strftime('%Y-%m-%d')
        applications[application_id] = {
            'application_id': application_id,
            'username': user['username'],
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': phone,
            'address': user['address'],
            'housing_type': housing_type,
            'has_yard': has_yard,
            'other_pets': other_pets,
            'experience': experience,
            'reason': reason,
            'status': 'Pending',
            'date_submitted': date_submitted
        }
        save_applications(applications)
        flash('Adoption application submitted successfully.', 'success')
        return redirect(url_for('my_applications'))
    else:
        return render_template('adoption_application.html', pet=pet, user=user)
@app.route('/my_applications')
@login_required
def my_applications():
    user = get_user()
    applications = load_applications()
    pets = load_pets()
    filter_status = request.args.get('filter-status', 'All')
    user_apps = [a for a in applications.values() if a['username'] == user['username']]
    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'].lower() == filter_status.lower()]
    # Add pet name to each application for display
    for app_ in user_apps:
        pet = pets.get(app_['pet_id'])
        app_['pet_name'] = pet['name'] if pet else 'Unknown'
    return render_template('my_applications.html',
                           applications=user_apps,
                           filter_status=filter_status,
                           user=user)
@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites():
    user = get_user()
    favorites = load_favorites()
    pets = load_pets()
    user_favorites = [f for f in favorites if f['username'] == user['username']]
    if request.method == 'POST':
        # Handle add or remove favorite
        action = request.form.get('action')
        pet_id = request.form.get('pet_id')
        if action == 'add':
            # Check if already favorite
            if any(f['pet_id'] == pet_id and f['username'] == user['username'] for f in favorites):
                flash('Pet already in favorites.', 'info')
            else:
                favorites.append({
                    'username': user['username'],
                    'pet_id': pet_id,
                    'date_added': datetime.now().strftime('%Y-%m-%d')
                })
                save_favorites(favorites)
                flash('Pet added to favorites.', 'success')
        elif action == 'remove':
            favorites = [f for f in favorites if not (f['username'] == user['username'] and f['pet_id'] == pet_id)]
            save_favorites(favorites)
            flash('Pet removed from favorites.', 'success')
        return redirect(url_for('favorites'))
    # Prepare pet data for favorites grid
    favorite_pets = []
    for fav in user_favorites:
        pet = pets.get(fav['pet_id'])
        if pet and pet['status'].lower() == 'available':
            favorite_pets.append(pet)
    return render_template('favorites.html', favorites=favorite_pets, user=user)
@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    user = get_user()
    messages = load_messages()
    users = load_users()
    # Build conversation list: unique conversation partners with last message timestamp
    conversations = defaultdict(list)
    for m in messages.values():
        if m['sender_username'] == user['username'] or m['recipient_username'] == user['username']:
            # Determine conversation partner
            partner = m['recipient_username'] if m['sender_username'] == user['username'] else m['sender_username']
            conversations[partner].append(m)
    # Sort conversations by last message timestamp descending
    conv_list = []
    for partner, msgs in conversations.items():
        last_msg = max(msgs, key=lambda x: x['timestamp'])
        conv_list.append({
            'partner': partner,
            'partner_email': users.get(partner, {}).get('email', ''),
            'last_message': last_msg['content'],
            'last_timestamp': last_msg['timestamp'],
            'unread_count': sum(1 for m in msgs if not m['is_read'] and m['recipient_username'] == user['username'])
        })
    conv_list.sort(key=lambda x: x['last_timestamp'], reverse=True)
    # Handle sending new message
    if request.method == 'POST':
        recipient_username = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()
        if not recipient_username or not subject or not content:
            flash('Please fill in all message fields.', 'warning')
            return render_template('messages.html', conversations=conv_list, user=user)
        if recipient_username not in users:
            flash('Recipient user does not exist.', 'danger')
            return render_template('messages.html', conversations=conv_list, user=user)
        message_id = get_next_message_id(messages)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages[message_id] = {
            'message_id': message_id,
            'sender_username': user['username'],
            'recipient_username': recipient_username,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }
        save_messages(messages)
        flash('Message sent successfully.', 'success')
        return redirect(url_for('messages'))
    return render_template('messages.html', conversations=conv_list, user=user)
@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    user = get_user()
    users = load_users()
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.', 'warning')
            return render_template('user_profile.html', user=user)
        # Update email
        users[user['username']]['email'] = email
        save_users(users)
        flash('Profile updated successfully.', 'success')
        # Update session user info
        user['email'] = email
        return redirect(url_for('user_profile'))
    return render_template('user_profile.html', user=user)
@app.route('/admin_panel', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    pets = load_pets()
    applications = load_applications()
    shelters = load_shelters()
    # Handle application status update or pet edit/delete
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_application':
            application_id = request.form.get('application_id')
            new_status = request.form.get('new_status')
            if application_id in applications and new_status in ['Pending', 'Approved', 'Rejected']:
                applications[application_id]['status'] = new_status
                save_applications(applications)
                flash(f'Application {application_id} status updated to {new_status}.', 'success')
                # If approved, update pet status and add to adoption history
                if new_status == 'Approved':
                    pet_id = applications[application_id]['pet_id']
                    if pet_id in pets:
                        pets[pet_id]['status'] = 'Pending'  # Pet is pending adoption
                        save_pets(pets)
                    # Add to adoption history
                    history = load_adoption_history()
                    history_id = get_next_history_id(history)
                    adoption_date = datetime.now().strftime('%Y-%m-%d')
                    history[history_id] = {
                        'history_id': history_id,
                        'username': applications[application_id]['username'],
                        'pet_id': pet_id,
                        'pet_name': pets[pet_id]['name'] if pet_id in pets else 'Unknown',
                        'adoption_date': adoption_date,
                        'shelter_id': pets[pet_id]['shelter_id'] if pet_id in pets else '0'
                    }
                    save_adoption_history(history)
            else:
                flash('Invalid application or status.', 'danger')
        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            if pet_id in pets:
                del pets[pet_id]
                save_pets(pets)
                flash(f'Pet {pet_id} deleted.', 'success')
            else:
                flash('Pet not found.', 'danger')
        elif action == 'edit_pet':
            pet_id = request.form.get('pet_id')
            if pet_id in pets:
                # For simplicity, redirect to add_pet page with prefilled data could be implemented,
                # but here we just flash message
                flash('Edit pet functionality not implemented in this version.', 'info')
            else:
                flash('Pet not found.', 'danger')
        return redirect(url_for('admin_panel'))
    # Prepare pending applications list
    pending_applications = [a for a in applications.values() if a['status'].lower() == 'pending']
    # Prepare all pets list
    all_pets_list = list(pets.values())
    return render_template('admin_panel.html',
                           pending_applications=pending_applications,
                           all_pets_list=all_pets_list,
                           shelters=shelters,
                           user=get_user())
# --- LOGIN/LOGOUT for demo purposes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = load_users()
        if username in users:
            session['username'] = username
            flash(f'Logged in as {username}.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username.', 'danger')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.', 'info')
    return redirect(url_for('dashboard'))
# --- Run app ---
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)