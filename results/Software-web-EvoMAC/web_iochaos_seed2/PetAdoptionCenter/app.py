'''
Main backend application for PetAdoptionCenter.
Implements all routing, data handling, and business logic using Flask.
Data is stored in local text files under the 'data' directory.
The application starts at the Dashboard page ('/').
'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import datetime
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
                    username, email, phone, address = parts
                    users.append({
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'address': address
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
                    pet_id, name, species, breed, age, gender, size, description, shelter_id, status, date_added = parts
                    pets.append({
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
                    (application_id, username, pet_id, applicant_name, phone, address,
                     housing_type, has_yard, other_pets, experience, reason, status, date_submitted) = parts
                    applications.append({
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
                    })
    return applications
def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = '|'.join([
                a['application_id'], a['username'], a['pet_id'], a['applicant_name'], a['phone'], a['address'],
                a['housing_type'], a['has_yard'], a['other_pets'], a['experience'], a['reason'], a['status'], a['date_submitted']
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
                    username, pet_id, date_added = parts
                    favorites.append({
                        'username': username,
                        'pet_id': pet_id,
                        'date_added': date_added
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
                    message_id, sender_username, recipient_username, subject, content, timestamp, is_read = parts
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
                    history_id, username, pet_id, pet_name, adoption_date, shelter_id = parts
                    history.append({
                        'history_id': history_id,
                        'username': username,
                        'pet_id': pet_id,
                        'pet_name': pet_name,
                        'adoption_date': adoption_date,
                        'shelter_id': shelter_id
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
                    shelter_id, name, address, phone, email = parts
                    shelters.append({
                        'shelter_id': shelter_id,
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'email': email
                    })
    return shelters
# Helper functions
def get_next_id(items, id_key):
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_key])
            if current_id > max_id:
                max_id = current_id
        except Exception:
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
# In a real app, implement proper authentication.
# For demo, we default to 'john_doe' if not set.
def get_current_username():
    username = session.get('username')
    if not username:
        # Default user for demo
        username = 'john_doe'
        session['username'] = username
    return username
# Routes
@app.route('/')
def dashboard():
    pets = read_pets()
    # Featured pets: up to 5 available pets, sorted by date_added descending
    available_pets = [p for p in pets if p['status'] == 'Available']
    featured_pets = sorted(available_pets, key=lambda x: x['date_added'], reverse=True)[:5]
    return render_template('dashboard.html', featured_pets=featured_pets)
@app.route('/pet_listings', methods=['GET', 'POST'])
def pet_listings():
    pets = read_pets()
    species_filter = request.args.get('filter-species', 'All')
    search_input = request.args.get('search-input', '').strip()
    filtered_pets = filter_pets(pets, species=species_filter, search_name=search_input, status='Available')
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=species_filter, search_input=search_input)
@app.route('/pet_details/<pet_id>')
def pet_details(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet)
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pets = read_pets()
        pet_id = get_next_id(pets, 'pet_id')
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()
        shelter_id = '1'  # For demo, assign shelter_id 1; in real app, get from admin user
        status = 'Available'
        date_added = datetime.date.today().isoformat()
        if not name or not species or not breed or not age or not gender or not size or not description:
            flash('All fields are required.', 'error')
            return render_template('add_pet.html')
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
            'status': status,
            'date_added': date_added
        }
        pets.append(new_pet)
        write_pets(pets)
        flash(f'Pet "{name}" added successfully.', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('add_pet.html')
@app.route('/adoption_application/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    if request.method == 'POST':
        applications = read_applications()
        application_id = get_next_id(applications, 'application_id')
        username = get_current_username()
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        # Additional fields from requirements but not in form elements: has_yard, other_pets, experience
        # Since not specified in form, we set defaults or empty
        has_yard = request.form.get('has-yard', 'No').strip() if 'has-yard' in request.form else 'No'
        other_pets = request.form.get('other-pets', '').strip() if 'other-pets' in request.form else 'None'
        experience = request.form.get('experience', '').strip() if 'experience' in request.form else ''
        # Get user address from users.txt
        user = get_user_by_username(username)
        address = user['address'] if user else ''
        if not applicant_name or not phone or not housing_type or not reason:
            flash('Please fill in all required fields.', 'error')
            return render_template('adoption_application.html', pet=pet)
        date_submitted = datetime.date.today().isoformat()
        status = 'Pending'
        new_application = {
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
        applications.append(new_application)
        write_applications(applications)
        flash('Adoption application submitted successfully.', 'success')
        return redirect(url_for('my_applications'))
    else:
        return render_template('adoption_application.html', pet=pet)
@app.route('/my_applications')
def my_applications():
    username = get_current_username()
    applications = read_applications()
    pets = read_pets()
    filter_status = request.args.get('filter-status', 'All')
    user_apps = [a for a in applications if a['username'] == username]
    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'] == filter_status]
    # Attach pet name to each application for display
    pet_dict = {p['pet_id']: p['name'] for p in pets}
    for app_ in user_apps:
        app_['pet_name'] = pet_dict.get(app_['pet_id'], 'Unknown')
    return render_template('my_applications.html', applications=user_apps, filter_status=filter_status)
@app.route('/favorites')
def favorites():
    username = get_current_username()
    favorites = read_favorites()
    pets = read_pets()
    user_favs = [f for f in favorites if f['username'] == username]
    pet_dict = {p['pet_id']: p for p in pets}
    fav_pets = []
    for fav in user_favs:
        pet = pet_dict.get(fav['pet_id'])
        if pet:
            fav_pets.append(pet)
    return render_template('favorites.html', favorite_pets=fav_pets)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = get_current_username()
    messages = read_messages()
    # Build conversation list: unique pairs of sender/recipient involving current user
    conversations = {}
    for msg in messages:
        if username in (msg['sender_username'], msg['recipient_username']):
            # Conversation key: tuple sorted to avoid duplicates
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conversations:
                conversations[participants] = []
            conversations[participants].append(msg)
    # Sort conversations by latest message timestamp descending
    sorted_conversations = sorted(conversations.items(),
                                  key=lambda x: max(m['timestamp'] for m in x[1]),
                                  reverse=True)
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()
        if not recipient or not subject or not content:
            flash('Please fill in all message fields.', 'error')
            return render_template('messages.html', conversations=sorted_conversations, current_username=username)
        # Validate recipient exists
        if not get_user_by_username(recipient):
            flash('Recipient user does not exist.', 'error')
            return render_template('messages.html', conversations=sorted_conversations, current_username=username)
        message_id = get_next_id(messages, 'message_id')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        write_messages(messages)
        flash('Message sent successfully.', 'success')
        return redirect(url_for('messages'))
    return render_template('messages.html', conversations=sorted_conversations, current_username=username)
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    username = get_current_username()
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
    else:
        return render_template('user_profile.html', user=user)
@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    # For demo, no authentication check for admin user
    pets = read_pets()
    applications = read_applications()
    pending_apps = [a for a in applications if a['status'] == 'Pending']
    if request.method == 'POST':
        # Handle application status update or pet edit/delete
        action = request.form.get('action')
        if action == 'update_application_status':
            application_id = request.form.get('application_id')
            new_status = request.form.get('new_status')
            if application_id and new_status in ('Pending', 'Approved', 'Rejected'):
                updated = False
                for app_ in applications:
                    if app_['application_id'] == application_id:
                        app_['status'] = new_status
                        updated = True
                        # If approved, update pet status to Pending or Adopted accordingly
                        if new_status == 'Approved':
                            pet = get_pet_by_id(app_['pet_id'])
                            if pet:
                                pet['status'] = 'Pending'
                                # Update pets.txt
                                pets = read_pets()
                                for p in pets:
                                    if p['pet_id'] == pet['pet_id']:
                                        p['status'] = 'Pending'
                                write_pets(pets)
                        write_applications(applications)
                        flash(f'Application {application_id} status updated to {new_status}.', 'success')
                        break
                if not updated:
                    flash('Application not found.', 'error')
            else:
                flash('Invalid application status update.', 'error')
        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            if pet_id:
                pets = [p for p in pets if p['pet_id'] != pet_id]
                write_pets(pets)
                flash(f'Pet {pet_id} deleted.', 'success')
            else:
                flash('Pet ID missing for deletion.', 'error')
        elif action == 'edit_pet':
            pet_id = request.form.get('pet_id')
            if pet_id:
                # Redirect to add_pet page with prefilled data is not specified,
                # so for simplicity, just flash message.
                flash('Edit pet functionality not implemented in this demo.', 'info')
            else:
                flash('Pet ID missing for edit.', 'error')
        return redirect(url_for('admin_panel'))
    return render_template('admin_panel.html', pending_applications=pending_apps, all_pets=pets)
# Navigation routes for buttons that go back to dashboard or other pages
@app.route('/back_to_dashboard')
def back_to_dashboard():
    return redirect(url_for('dashboard'))
@app.route('/back_to_pet_listings')
def back_to_pet_listings():
    return redirect(url_for('pet_listings'))
@app.route('/back_to_pet_details/<pet_id>')
def back_to_pet_details(pet_id):
    return redirect(url_for('pet_details', pet_id=pet_id))
@app.route('/back_to_my_applications')
def back_to_my_applications():
    return redirect(url_for('my_applications'))
@app.route('/back_to_favorites')
def back_to_favorites():
    return redirect(url_for('favorites'))
@app.route('/back_to_messages')
def back_to_messages():
    return redirect(url_for('messages'))
@app.route('/back_to_user_profile')
def back_to_user_profile():
    return redirect(url_for('user_profile'))
@app.route('/back_to_admin_panel')
def back_to_admin_panel():
    return redirect(url_for('admin_panel'))
# Run the app on local port 5000
if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)