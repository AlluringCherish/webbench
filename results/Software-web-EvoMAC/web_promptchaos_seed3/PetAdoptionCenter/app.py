'''
Main backend application for PetAdoptionCenter web app.
Implements all routing, data handling, and business logic using Flask.
Data is stored in local text files under the 'data' directory.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session and flash messages
DATA_DIR = 'data'
# Utility functions for reading and writing data files
def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
    return users
def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users:
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            f.write(line + '\n')
def read_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(path):
        return pets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 11:
                    pets.append({
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
                    })
    return pets
def write_pets(pets):
    path = os.path.join(DATA_DIR, 'pets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in pets:
            line = '|'.join([
                p['pet_id'], p['name'], p['species'], p['breed'], p['age'], p['gender'],
                p['size'], p['description'], p['shelter_id'], p['status'], p['date_added']
            ])
            f.write(line + '\n')
def read_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 13:
                    applications.append({
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
                    })
    return applications
def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = '|'.join([
                a['application_id'], a['username'], a['pet_id'], a['applicant_name'], a['phone'],
                a['address'], a['housing_type'], a['has_yard'], a['other_pets'], a['experience'],
                a['reason'], a['status'], a['date_submitted']
            ])
            f.write(line + '\n')
def read_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    favorites.append({
                        'username': parts[0],
                        'pet_id': parts[1],
                        'date_added': parts[2]
                    })
    return favorites
def write_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([fav['username'], fav['pet_id'], fav['date_added']])
            f.write(line + '\n')
def read_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(path):
        return messages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 7:
                    messages.append({
                        'message_id': parts[0],
                        'sender_username': parts[1],
                        'recipient_username': parts[2],
                        'subject': parts[3],
                        'content': parts[4],
                        'timestamp': parts[5],
                        'is_read': parts[6].lower() == 'true'
                    })
    return messages
def write_messages(messages):
    path = os.path.join(DATA_DIR, 'messages.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for m in messages:
            line = '|'.join([
                m['message_id'], m['sender_username'], m['recipient_username'], m['subject'],
                m['content'], m['timestamp'], 'true' if m['is_read'] else 'false'
            ])
            f.write(line + '\n')
def read_adoption_history():
    history = []
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    history.append({
                        'history_id': parts[0],
                        'username': parts[1],
                        'pet_id': parts[2],
                        'pet_name': parts[3],
                        'adoption_date': parts[4],
                        'shelter_id': parts[5]
                    })
    return history
def write_adoption_history(history):
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for h in history:
            line = '|'.join([
                h['history_id'], h['username'], h['pet_id'], h['pet_name'], h['adoption_date'], h['shelter_id']
            ])
            f.write(line + '\n')
def read_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(path):
        return shelters
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    shelters.append({
                        'shelter_id': parts[0],
                        'name': parts[1],
                        'address': parts[2],
                        'phone': parts[3],
                        'email': parts[4]
                    })
    return shelters
# Helper functions
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            val = int(item[id_key])
            if val > max_id:
                max_id = val
        except:
            continue
    return str(max_id + 1)
def get_pet_by_id(pet_id):
    pets = read_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None
def get_user_by_username(username):
    users = read_users()
    for user in users:
        if user['username'] == username:
            return user
    return None
def get_shelter_by_id(shelter_id):
    shelters = read_shelters()
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
# For simplicity, we simulate a logged-in user by session['username']
# In real app, implement proper authentication
@app.before_request
def ensure_user():
    if 'username' not in session:
        # For demo, default to 'john_doe'
        session['username'] = 'john_doe'
# ROUTES
# 1. Dashboard Page - '/'
@app.route('/')
def dashboard():
    pets = read_pets()
    # Featured pets: first 5 available pets sorted by date_added descending
    available_pets = [p for p in pets if p['status'] == 'Available']
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = available_pets[:5]
    # Recent activities: show recent applications by this user (last 5)
    applications = read_applications()
    user_apps = [a for a in applications if a['username'] == session['username']]
    user_apps.sort(key=lambda x: x['date_submitted'], reverse=True)
    recent_apps = user_apps[:5]
    return render_template('dashboard.html',
                           featured_pets=featured_pets,
                           recent_applications=recent_apps,
                           username=session['username'])
# 2. Pet Listings Page - '/pets'
@app.route('/pets', methods=['GET', 'POST'])
def pet_listings():
    pets = read_pets()
    species_filter = request.args.get('species', 'All')
    search_name = request.args.get('search', '').strip()
    filtered_pets = filter_pets(pets, species=species_filter, search_name=search_name, status='Available')
    return render_template('pet_listings.html',
                           pets=filtered_pets,
                           species_filter=species_filter,
                           search_name=search_name)
# 3. Pet Details Page - '/pets/<pet_id>'
@app.route('/pets/<pet_id>')
def pet_details(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet)
# 4. Add Pet Page - '/add_pet'
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    # For simplicity, only allow admin_user to add pets
    if session['username'] != 'admin_user':
        flash('Access denied: Only administrators can add pets.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        pets = read_pets()
        new_id = get_next_id(pets, 'pet_id')
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()
        shelter_id = '1'  # For demo, assign shelter_id 1; in real app, admin selects shelter
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')
        if not name or not species or not breed or not age or not gender or not size or not description:
            flash('All fields are required.', 'error')
            return render_template('add_pet.html')
        new_pet = {
            'pet_id': new_id,
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
        pets.append(new_pet)
        write_pets(pets)
        flash(f'Pet "{name}" added successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_pet.html')
# 5. Adoption Application Page - '/apply/<pet_id>'
@app.route('/apply/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    if request.method == 'POST':
        applications = read_applications()
        new_id = get_next_id(applications, 'application_id')
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        # Additional fields from requirements but not in form: has_yard, other_pets, experience
        # Since not specified in form elements, we set defaults
        has_yard = 'No'
        other_pets = 'None'
        experience = 'Not specified'
        if not applicant_name or not applicant_phone or not housing_type or not reason:
            flash('Please fill in all required fields.', 'error')
            return render_template('adoption_application.html', pet=pet)
        # Get user info for address
        user = get_user_by_username(session['username'])
        address = user['address'] if user else ''
        new_application = {
            'application_id': new_id,
            'username': session['username'],
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
            'date_submitted': datetime.now().strftime('%Y-%m-%d')
        }
        applications.append(new_application)
        write_applications(applications)
        flash('Adoption application submitted successfully.', 'success')
        return redirect(url_for('my_applications'))
    return render_template('adoption_application.html', pet=pet)
# 6. My Applications Page - '/my_applications'
@app.route('/my_applications')
def my_applications():
    status_filter = request.args.get('status', 'All')
    applications = read_applications()
    user_apps = [a for a in applications if a['username'] == session['username']]
    if status_filter != 'All':
        user_apps = [a for a in user_apps if a['status'] == status_filter]
    # For each application, get pet name for display
    pets = read_pets()
    pet_dict = {p['pet_id']: p['name'] for p in pets}
    for app in user_apps:
        app['pet_name'] = pet_dict.get(app['pet_id'], 'Unknown')
    return render_template('my_applications.html',
                           applications=user_apps,
                           status_filter=status_filter)
# 7. Favorites Page - '/favorites'
@app.route('/favorites')
def favorites():
    favorites = read_favorites()
    user_favs = [f for f in favorites if f['username'] == session['username']]
    pets = read_pets()
    pet_dict = {p['pet_id']: p for p in pets}
    fav_pets = []
    for fav in user_favs:
        pet = pet_dict.get(fav['pet_id'])
        if pet and pet['status'] == 'Available':
            fav_pets.append(pet)
    return render_template('favorites.html', pets=fav_pets)
# Add or remove favorite pet (AJAX or form POST)
@app.route('/favorites/toggle/<pet_id>', methods=['POST'])
def toggle_favorite(pet_id):
    favorites = read_favorites()
    username = session['username']
    existing = None
    for fav in favorites:
        if fav['username'] == username and fav['pet_id'] == pet_id:
            existing = fav
            break
    if existing:
        favorites.remove(existing)
        flash('Removed from favorites.', 'info')
    else:
        favorites.append({
            'username': username,
            'pet_id': pet_id,
            'date_added': datetime.now().strftime('%Y-%m-%d')
        })
        flash('Added to favorites.', 'success')
    write_favorites(favorites)
    return redirect(request.referrer or url_for('favorites'))
# 8. Messages Page - '/messages'
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = session['username']
    messages = read_messages()
    # Get conversations: unique pairs of sender/recipient involving user
    conversations = {}
    for msg in messages:
        if msg['sender_username'] == username or msg['recipient_username'] == username:
            # Conversation key: sorted tuple of usernames
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conversations:
                conversations[participants] = []
            conversations[participants].append(msg)
    # Sort messages in each conversation by timestamp ascending
    for conv in conversations.values():
        conv.sort(key=lambda x: x['timestamp'])
    # Handle sending new message
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()
        if not recipient or not subject or not content:
            flash('Please fill in all message fields.', 'error')
            return render_template('messages.html', conversations=conversations, username=username)
        # Check recipient exists
        if not get_user_by_username(recipient):
            flash('Recipient user does not exist.', 'error')
            return render_template('messages.html', conversations=conversations, username=username)
        new_id = get_next_id(messages, 'message_id')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_message = {
            'message_id': new_id,
            'sender_username': username,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }
        messages.append(new_message)
        write_messages(messages)
        flash('Message sent.', 'success')
        return redirect(url_for('messages'))
    return render_template('messages.html', conversations=conversations, username=username)
# 9. User Profile Page - '/profile'
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    username = session['username']
    users = read_users()
    user = get_user_by_username(username)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.', 'error')
            return render_template('user_profile.html', user=user)
        # Update email
        for u in users:
            if u['username'] == username:
                u['email'] = email
                break
        write_users(users)
        flash('Profile updated successfully.', 'success')
        # Refresh user data
        user = get_user_by_username(username)
    return render_template('user_profile.html', user=user)
# 10. Admin Panel Page - '/admin'
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if session['username'] != 'admin_user':
        flash('Access denied: Only administrators can access admin panel.', 'error')
        return redirect(url_for('dashboard'))
    pets = read_pets()
    applications = read_applications()
    # Pending applications
    pending_apps = [a for a in applications if a['status'] == 'Pending']
    # Handle application status update or pet edit/delete
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_application':
            app_id = request.form.get('application_id')
            new_status = request.form.get('new_status')
            if app_id and new_status in ['Pending', 'Approved', 'Rejected']:
                for a in applications:
                    if a['application_id'] == app_id:
                        a['status'] = new_status
                        # If approved, update pet status to Pending or Adopted
                        if new_status == 'Approved':
                            pet = get_pet_by_id(a['pet_id'])
                            if pet:
                                pet['status'] = 'Pending'
                                # Update pets file
                                for p in pets:
                                    if p['pet_id'] == pet['pet_id']:
                                        p['status'] = 'Pending'
                                        break
                                write_pets(pets)
                        write_applications(applications)
                        flash(f'Application {app_id} status updated to {new_status}.', 'success')
                        break
            return redirect(url_for('admin_panel'))
        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            if pet_id:
                pets = [p for p in pets if p['pet_id'] != pet_id]
                write_pets(pets)
                flash(f'Pet {pet_id} deleted.', 'info')
            return redirect(url_for('admin_panel'))
        elif action == 'edit_pet':
            # For simplicity, redirect to add_pet page with pet data prefilled is not implemented
            # Instead, just flash message
            flash('Pet editing not implemented in this version.', 'info')
            return redirect(url_for('admin_panel'))
    return render_template('admin_panel.html',
                           pending_applications=pending_apps,
                           pets=pets)
# Additional routes for navigation buttons that refresh or go back
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