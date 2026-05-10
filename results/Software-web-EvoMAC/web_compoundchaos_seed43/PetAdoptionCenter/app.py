'''
Main Flask application for PetAdoptionCenter.
Defines routes for all pages, handles data loading and saving from local text files,
and renders templates with dynamic data.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production
DATA_DIR = 'data'
# Utility functions to read/write data files
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
# Helper to get next ID for pets, applications, messages, history
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
# For demonstration, we simulate a logged-in user
# In real app, implement authentication
def get_current_username():
    # For demo, return a fixed username
    return 'john_doe'
@app.route('/')
def dashboard():
    pets = read_pets()
    # Featured pets: first 5 available pets sorted by date_added descending
    available_pets = [p for p in pets if p['status'].lower() == 'available']
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = available_pets[:5]
    # Recent activities: show recent applications by current user (last 5)
    applications = read_applications()
    username = get_current_username()
    user_apps = [a for a in applications if a['username'] == username]
    user_apps.sort(key=lambda x: x['date_submitted'], reverse=True)
    recent_activities = user_apps[:5]
    return render_template('dashboard.html',
                           featured_pets=featured_pets,
                           recent_activities=recent_activities,
                           username=username)
@app.route('/pets')
def pet_listings():
    pets = read_pets()
    species_filter = request.args.get('species', 'All')
    search_name = request.args.get('search', '').strip().lower()
    filtered_pets = pets
    if species_filter and species_filter != 'All':
        filtered_pets = [p for p in filtered_pets if p['species'].lower() == species_filter.lower()]
    if search_name:
        filtered_pets = [p for p in filtered_pets if search_name in p['name'].lower()]
    # Only show pets with status Available or Pending (exclude others)
    filtered_pets = [p for p in filtered_pets if p['status'].lower() in ['available', 'pending']]
    return render_template('pets.html',
                           pets=filtered_pets,
                           species_filter=species_filter,
                           search_name=search_name)
@app.route('/pet/<pet_id>')
def pet_details(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet)
@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
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
        shelter_id = '1'  # For demo, assign shelter_id 1; in real app, get from admin user
        status = 'Available'
        date_added = datetime.now().strftime('%Y-%m-%d')
        if not name or not species:
            flash('Pet name and species are required.', 'error')
            return redirect(url_for('add_pet'))
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
@app.route('/adopt/<pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    if request.method == 'POST':
        applications = read_applications()
        new_id = get_next_id(applications, 'application_id')
        username = get_current_username()
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()
        address = ''  # We can get from users.txt if needed
        has_yard = request.form.get('has-yard', 'No')
        other_pets = request.form.get('other-pets', 'None')
        experience = request.form.get('experience', 'None')
        date_submitted = datetime.now().strftime('%Y-%m-%d')
        status = 'Pending'
        if not applicant_name or not phone or not housing_type or not reason:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('adoption_application', pet_id=pet_id))
        # Get user address from users.txt
        users = read_users()
        user = next((u for u in users if u['username'] == username), None)
        if user:
            address = user.get('address', '')
        new_application = {
            'application_id': new_id,
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
    return render_template('adoption_application.html', pet=pet)
@app.route('/my-applications')
def my_applications():
    username = get_current_username()
    applications = read_applications()
    pets = read_pets()
    filter_status = request.args.get('status', 'All')
    user_apps = [a for a in applications if a['username'] == username]
    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'].lower() == filter_status.lower()]
    # Attach pet name to each application
    for app_ in user_apps:
        pet = next((p for p in pets if p['pet_id'] == app_['pet_id']), None)
        app_['pet_name'] = pet['name'] if pet else 'Unknown'
    return render_template('my_applications.html',
                           applications=user_apps,
                           filter_status=filter_status)
@app.route('/favorites')
def favorites():
    username = get_current_username()
    favorites = read_favorites()
    pets = read_pets()
    user_favs = [f for f in favorites if f['username'] == username]
    fav_pets = []
    for fav in user_favs:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            fav_pets.append(pet)
    return render_template('favorites.html', pets=fav_pets)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = get_current_username()
    messages = read_messages()
    # For simplicity, show all conversations involving current user
    conversations = {}
    for m in messages:
        if m['sender_username'] == username or m['recipient_username'] == username:
            # Conversation key: tuple of usernames sorted
            participants = tuple(sorted([m['sender_username'], m['recipient_username']]))
            if participants not in conversations:
                conversations[participants] = []
            conversations[participants].append(m)
    # Sort messages in each conversation by timestamp ascending
    for conv in conversations.values():
        conv.sort(key=lambda x: x['timestamp'])
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()
        if not recipient or not subject or not content:
            flash('Please fill in all message fields.', 'error')
            return redirect(url_for('messages'))
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
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_current_username()
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            flash('Email cannot be empty.', 'error')
            return redirect(url_for('profile'))
        user['email'] = email
        write_users(users)
        flash('Profile updated.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)
@app.route('/admin')
def admin_panel():
    # For demo, no authentication check
    applications = read_applications()
    pets = read_pets()
    pending_apps = [a for a in applications if a['status'].lower() == 'pending']
    return render_template('admin_panel.html',
                           pending_applications=pending_apps,
                           all_pets=pets)
@app.route('/admin/application/<application_id>/update', methods=['POST'])
def admin_update_application(application_id):
    status = request.form.get('status', '').strip()
    if status not in ['Pending', 'Approved', 'Rejected']:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_panel'))
    applications = read_applications()
    app_found = False
    for a in applications:
        if a['application_id'] == application_id:
            a['status'] = status
            app_found = True
            break
    if app_found:
        write_applications(applications)
        flash('Application status updated.', 'success')
    else:
        flash('Application not found.', 'error')
    return redirect(url_for('admin_panel'))
@app.route('/admin/pet/<pet_id>/delete', methods=['POST'])
def admin_delete_pet(pet_id):
    pets = read_pets()
    pets = [p for p in pets if p['pet_id'] != pet_id]
    write_pets(pets)
    flash('Pet deleted.', 'success')
    return redirect(url_for('admin_panel'))
@app.route('/admin/pet/<pet_id>/edit', methods=['GET', 'POST'])
def admin_edit_pet(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('admin_panel'))
    if request.method == 'POST':
        pet['name'] = request.form.get('pet-name-input', pet['name']).strip()
        pet['species'] = request.form.get('pet-species-input', pet['species']).strip()
        pet['breed'] = request.form.get('pet-breed-input', pet['breed']).strip()
        pet['age'] = request.form.get('pet-age-input', pet['age']).strip()
        pet['gender'] = request.form.get('pet-gender-input', pet['gender']).strip()
        pet['size'] = request.form.get('pet-size-input', pet['size']).strip()
        pet['description'] = request.form.get('pet-description-input', pet['description']).strip()
        pet['status'] = request.form.get('pet-status-input', pet['status']).strip()
        write_pets(pets)
        flash('Pet updated.', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('edit_pet.html', pet=pet)
if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)