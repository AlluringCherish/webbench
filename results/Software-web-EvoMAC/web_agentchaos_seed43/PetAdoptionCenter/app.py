'''
Main backend application for PetAdoptionCenter.
Implements Flask web server, routing for all pages, and business logic for reading/writing data files.
Data stored in local text files under data/ directory using pipe-delimited format.
'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages
DATA_DIR = 'data'
# Utility functions for file operations and data parsing
def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip() != '']
def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')
def parse_line(line, fields_count):
    parts = line.split('|')
    if len(parts) < fields_count:
        # Pad missing fields with empty strings
        parts += [''] * (fields_count - len(parts))
    return parts
def format_line(fields):
    return '|'.join(str(f) for f in fields)
# --- Data loading functions ---
def load_users():
    # username|email|phone|address
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        username, email, phone, address = parse_line(line, 4)
        users[username] = {
            'username': username,
            'email': email,
            'phone': phone,
            'address': address
        }
    return users
def load_pets():
    # pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added
    pets = {}
    lines = read_file_lines('pets.txt')
    for line in lines:
        (pet_id, name, species, breed, age, gender, size,
         description, shelter_id, status, date_added) = parse_line(line, 11)
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
    return pets
def load_applications():
    # application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted
    applications = {}
    lines = read_file_lines('applications.txt')
    for line in lines:
        (application_id, username, pet_id, applicant_name, phone, address,
         housing_type, has_yard, other_pets, experience, reason, status, date_submitted) = parse_line(line, 13)
        applications[application_id] = {
            'application_id': application_id,
            'username': username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': phone,
            'address': address,
            'housing_type': housing_type,
            'has_yard': has_yard,
            'other_pets': other_pets,
            'experience': experience,
            'reason': reason,
            'status': status,
            'date_submitted': date_submitted
        }
    return applications
def load_favorites():
    # username|pet_id|date_added
    favorites = []
    lines = read_file_lines('favorites.txt')
    for line in lines:
        username, pet_id, date_added = parse_line(line, 3)
        favorites.append({
            'username': username,
            'pet_id': pet_id,
            'date_added': date_added
        })
    return favorites
def load_messages():
    # message_id|sender_username|recipient_username|subject|content|timestamp|is_read
    messages = []
    lines = read_file_lines('messages.txt')
    for line in lines:
        (message_id, sender_username, recipient_username, subject,
         content, timestamp, is_read) = parse_line(line, 7)
        messages.append({
            'message_id': message_id,
            'sender_username': sender_username,
            'recipient_username': recipient_username,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': is_read.lower() == 'true'
        })
    return messages
def load_adoption_history():
    # history_id|username|pet_id|pet_name|adoption_date|shelter_id
    history = []
    lines = read_file_lines('adoption_history.txt')
    for line in lines:
        history_id, username, pet_id, pet_name, adoption_date, shelter_id = parse_line(line, 6)
        history.append({
            'history_id': history_id,
            'username': username,
            'pet_id': pet_id,
            'pet_name': pet_name,
            'adoption_date': adoption_date,
            'shelter_id': shelter_id
        })
    return history
def load_shelters():
    # shelter_id|name|address|phone|email
    shelters = {}
    lines = read_file_lines('shelters.txt')
    for line in lines:
        shelter_id, name, address, phone, email = parse_line(line, 5)
        shelters[shelter_id] = {
            'shelter_id': shelter_id,
            'name': name,
            'address': address,
            'phone': phone,
            'email': email
        }
    return shelters
# --- Data saving functions ---
def save_pets(pets):
    lines = []
    for pet_id in sorted(pets, key=lambda x: int(x)):
        p = pets[pet_id]
        line = format_line([
            p['pet_id'], p['name'], p['species'], p['breed'], p['age'], p['gender'],
            p['size'], p['description'], p['shelter_id'], p['status'], p['date_added']
        ])
        lines.append(line)
    write_file_lines('pets.txt', lines)
def save_applications(applications):
    lines = []
    for app_id in sorted(applications, key=lambda x: int(x)):
        a = applications[app_id]
        line = format_line([
            a['application_id'], a['username'], a['pet_id'], a['applicant_name'], a['phone'],
            a['address'], a['housing_type'], a['has_yard'], a['other_pets'], a['experience'],
            a['reason'], a['status'], a['date_submitted']
        ])
        lines.append(line)
    write_file_lines('applications.txt', lines)
def save_favorites(favorites):
    lines = []
    for fav in favorites:
        line = format_line([fav['username'], fav['pet_id'], fav['date_added']])
        lines.append(line)
    write_file_lines('favorites.txt', lines)
def save_messages(messages):
    lines = []
    for msg in messages:
        line = format_line([
            msg['message_id'], msg['sender_username'], msg['recipient_username'], msg['subject'],
            msg['content'], msg['timestamp'], 'true' if msg['is_read'] else 'false'
        ])
        lines.append(line)
    write_file_lines('messages.txt', lines)
# --- Helper functions ---
def get_next_id(items_dict):
    if not items_dict:
        return '1'
    max_id = max(int(k) for k in items_dict.keys())
    return str(max_id + 1)
def get_next_message_id(messages_list):
    if not messages_list:
        return '1'
    max_id = max(int(m['message_id']) for m in messages_list)
    return str(max_id + 1)
def get_next_history_id(history_list):
    if not history_list:
        return '1'
    max_id = max(int(h['history_id']) for h in history_list)
    return str(max_id + 1)
# --- Routes ---
@app.route('/')
def dashboard():
    pets = load_pets()
    # Featured pets: limit 5, status Available, sorted by date_added descending
    featured = [p for p in pets.values() if p['status'].lower() == 'available']
    featured.sort(key=lambda x: x['date_added'], reverse=True)
    featured = featured[:5]
    return render_template('dashboard.html', featured_pets=featured)
@app.route('/pets')
def pet_listings():
    pets = load_pets()
    species_filter = request.args.get('species', 'All')
    search_name = request.args.get('search', '').strip().lower()
    filtered_pets = []
    for pet in pets.values():
        if pet['status'].lower() != 'available':
            continue
        if species_filter != 'All' and pet['species'].lower() != species_filter.lower():
            continue
        if search_name and search_name not in pet['name'].lower():
            continue
        filtered_pets.append(pet)
    # Sort by date_added descending
    filtered_pets.sort(key=lambda x: x['date_added'], reverse=True)
    return render_template('pet_listings.html',
                           pets=filtered_pets,
                           selected_species=species_filter,
                           search_name=search_name)
@app.route('/pets/<pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet)
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pets = load_pets()
        shelters = load_shelters()
        # Extract form data
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()
        # Basic validation
        if not name or not species or not breed or not age or not gender or not size or not description:
            flash('All fields are required.', 'error')
            return render_template('add_pet.html')
        # Assign pet_id
        pet_id = get_next_id(pets)
        # For simplicity, assign shelter_id = 1 (could be extended to select shelter)
        shelter_id = '1'
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')
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
    return render_template('add_pet.html')
@app.route('/adopt/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    if request.method == 'POST':
        applications = load_applications()
        users = load_users()
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        has_yard = request.form.get('has-yard', '').strip()
        other_pets = request.form.get('other-pets', '').strip()
        experience = request.form.get('experience', '').strip()
        # Since no login system specified, we will use applicant_name as username (lowercase, no spaces)
        username = applicant_name.lower().replace(' ', '_') if applicant_name else 'guest'
        address = users.get(username, {}).get('address', '')  # fallback empty
        # Validate required fields
        if not applicant_name or not applicant_phone or not housing_type or not reason or not has_yard or not other_pets or not experience:
            flash('Please fill in all required fields.', 'error')
            return render_template('adoption_application.html', pet=pet,
                                   applicant_name=applicant_name,
                                   applicant_phone=applicant_phone,
                                   housing_type=housing_type,
                                   reason=reason,
                                   has_yard=has_yard,
                                   other_pets=other_pets,
                                   experience=experience)
        application_id = get_next_id(applications)
        date_submitted = datetime.now().strftime('%Y-%m-%d')
        applications[application_id] = {
            'application_id': application_id,
            'username': username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': address,
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
        return redirect(url_for('pet_details', pet_id=pet_id))
    # GET request: render form with empty or default values
    return render_template('adoption_application.html', pet=pet,
                           applicant_name='',
                           applicant_phone='',
                           housing_type='',
                           reason='',
                           has_yard='',
                           other_pets='',
                           experience='')
@app.route('/my_applications')
def my_applications():
    # Since no login system, we simulate user by query param username or default 'guest'
    username = request.args.get('username', 'guest')
    applications = load_applications()
    pets = load_pets()
    filter_status = request.args.get('status', 'All')
    user_apps = [a for a in applications.values() if a['username'] == username]
    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'].lower() == filter_status.lower()]
    # Add pet name to each application for display
    for app in user_apps:
        pet = pets.get(app['pet_id'])
        app['pet_name'] = pet['name'] if pet else 'Unknown'
    return render_template('my_applications.html', applications=user_apps, filter_status=filter_status, username=username)
@app.route('/favorites')
def favorites():
    username = request.args.get('username', 'guest')
    favorites = load_favorites()
    pets = load_pets()
    user_favs = [f for f in favorites if f['username'] == username]
    fav_pets = []
    for fav in user_favs:
        pet = pets.get(fav['pet_id'])
        if pet:
            fav_pets.append(pet)
    return render_template('favorites.html', favorites=fav_pets, username=username)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    # Simulate logged in user by query param or default 'guest'
    username = request.args.get('username', 'guest')
    messages = load_messages()
    # Filter conversations involving this user
    conversations = {}
    for msg in messages:
        if msg['sender_username'] == username or msg['recipient_username'] == username:
            # Conversation key: tuple of sorted usernames
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conversations:
                conversations[participants] = []
            conversations[participants].append(msg)
    # Sort messages in each conversation by timestamp ascending
    for conv in conversations.values():
        conv.sort(key=lambda m: m['timestamp'])
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()
        if not recipient or not subject or not content:
            flash('Please fill in all message fields.', 'error')
            return render_template('messages.html', conversations=conversations, username=username)
        message_id = get_next_message_id(messages)
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
        flash('Message sent successfully.', 'success')
        return redirect(url_for('messages', username=username))
    return render_template('messages.html', conversations=conversations, username=username)
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    # Simulate logged in user by query param or default 'guest'
    username = request.args.get('username', 'guest')
    users = load_users()
    user = users.get(username)
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.', 'error')
            return render_template('user_profile.html', user=user)
        if user:
            user['email'] = email
        else:
            # Create new user with minimal info
            user = {
                'username': username,
                'email': email,
                'phone': '',
                'address': ''
            }
            users[username] = user
        # Save users back to file
        lines = []
        for u in users.values():
            line = format_line([u['username'], u['email'], u['phone'], u['address']])
            lines.append(line)
        write_file_lines('users.txt', lines)
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_profile', username=username))
    return render_template('user_profile.html', user=user)
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    pets = load_pets()
    applications = load_applications()
    # Pending applications list
    pending_apps = [a for a in applications.values() if a['status'].lower() == 'pending']
    if request.method == 'POST':
        # Handle application status update or pet edit/delete
        action = request.form.get('action')
        if action == 'update_application':
            application_id = request.form.get('application_id')
            new_status = request.form.get('new_status')
            if application_id in applications and new_status in ['Pending', 'Approved', 'Rejected']:
                applications[application_id]['status'] = new_status
                save_applications(applications)
                flash(f'Application {application_id} status updated to {new_status}.', 'success')
            else:
                flash('Invalid application ID or status.', 'error')
        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            if pet_id in pets:
                del pets[pet_id]
                save_pets(pets)
                flash(f'Pet {pet_id} deleted.', 'success')
            else:
                flash('Pet not found.', 'error')
        elif action == 'edit_pet':
            pet_id = request.form.get('pet_id')
            if pet_id in pets:
                # For simplicity, only update status here (could be extended)
                new_status = request.form.get('new_status')
                if new_status in ['Available', 'Pending', 'Adopted']:
                    pets[pet_id]['status'] = new_status
                    save_pets(pets)
                    flash(f'Pet {pet_id} status updated to {new_status}.', 'success')
                else:
                    flash('Invalid status.', 'error')
            else:
                flash('Pet not found.', 'error')
        return redirect(url_for('admin_panel'))
    # Sort pets by pet_id ascending
    all_pets = sorted(pets.values(), key=lambda x: int(x['pet_id']))
    return render_template('admin_panel.html',
                           pending_applications=pending_apps,
                           all_pets=all_pets)
# --- Additional routes for navigation buttons ---
@app.route('/refresh_dashboard')
def refresh_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_listings')
def back_to_listings():
    return redirect(url_for('pet_listings'))
@app.route('/back_to_pet/<pet_id>')
def back_to_pet(pet_id):
    return redirect(url_for('pet_details', pet_id=pet_id))
# Run the app
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)