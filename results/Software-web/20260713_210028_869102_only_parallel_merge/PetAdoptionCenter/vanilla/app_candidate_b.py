from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Helper functions for reading and writing data

def read_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return [line.split('|') for line in lines if line.strip()]

def write_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(["|".join(line)+"\n" for line in lines])

# USERS

def get_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = read_file(path)
    # Return as list of dicts
    return [{'username':u[0],'email':u[1],'phone':u[2],'address':u[3]} for u in users]

def get_user(username):
    users = get_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def update_user_email(username, new_email):
    users = get_users()
    updated = False
    for user in users:
        if user['username'] == username:
            user['email'] = new_email
            updated = True
    if updated:
        path = os.path.join(DATA_DIR, 'users.txt')
        write_file(path, [[u['username'], u['email'], u['phone'], u['address']] for u in users])
    return updated

# PETS

def get_pets():
    path = os.path.join(DATA_DIR, 'pets.txt')
    pets = read_file(path)
    pets_list = []
    for p in pets:
        pets_list.append({
            'pet_id': p[0],
            'name': p[1],
            'species': p[2],
            'breed': p[3],
            'age': p[4],
            'gender': p[5],
            'size': p[6],
            'description': p[7],
            'shelter_id': p[8],
            'status': p[9],
            'date_added': p[10]
        })
    return pets_list

def get_pet(pet_id):
    pets = get_pets()
    for pet in pets:
        if pet['pet_id'] == str(pet_id):
            return pet
    return None

def write_pets(pets):
    path = os.path.join(DATA_DIR, 'pets.txt')
    lines = []
    for p in pets:
        lines.append([
            str(p['pet_id']),
            p['name'],
            p['species'],
            p['breed'],
            p['age'],
            p['gender'],
            p['size'],
            p['description'],
            p['shelter_id'],
            p['status'],
            p['date_added']
        ])
    write_file(path, lines)

# APPLICATIONS

def get_applications():
    path = os.path.join(DATA_DIR, 'applications.txt')
    apps = read_file(path)
    applications = []
    for a in apps:
        applications.append({
            'application_id': a[0],
            'username': a[1],
            'pet_id': a[2],
            'applicant_name': a[3],
            'phone': a[4],
            'address': a[5],
            'housing_type': a[6],
            'has_yard': a[7],
            'other_pets': a[8],
            'experience': a[9],
            'reason': a[10],
            'status': a[11],
            'date_submitted': a[12]
        })
    return applications

def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    lines = []
    for a in applications:
        lines.append([
            str(a['application_id']),
            a['username'],
            a['pet_id'],
            a['applicant_name'],
            a['phone'],
            a['address'],
            a['housing_type'],
            a['has_yard'],
            a['other_pets'],
            a['experience'],
            a['reason'],
            a['status'],
            a['date_submitted']
        ])
    write_file(path, lines)

# FAVORITES

def get_favorites():
    path = os.path.join(DATA_DIR, 'favorites.txt')
    favs = read_file(path)
    favorites = []
    for f in favs:
        favorites.append({
            'username': f[0],
            'pet_id': f[1],
            'date_added': f[2]
        })
    return favorites

def write_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    lines = []
    for f in favorites:
        lines.append([f['username'], f['pet_id'], f['date_added']])
    write_file(path, lines)

# MESSAGES

def get_messages():
    path = os.path.join(DATA_DIR, 'messages.txt')
    msgs = read_file(path)
    messages = []
    for m in msgs:
        messages.append({
            'message_id': m[0],
            'sender_username': m[1],
            'recipient_username': m[2],
            'subject': m[3],
            'content': m[4],
            'timestamp': m[5],
            'is_read': m[6].lower() == 'true'
        })
    return messages

def write_messages(messages):
    path = os.path.join(DATA_DIR, 'messages.txt')
    lines = []
    for m in messages:
        lines.append([
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            'true' if m['is_read'] else 'false'
        ])
    write_file(path, lines)

# SHELTERS

def get_shelters():
    path = os.path.join(DATA_DIR, 'shelters.txt')
    s = read_file(path)
    shelters = []
    for sh in s:
        shelters.append({
            'shelter_id': sh[0],
            'name': sh[1],
            'address': sh[2],
            'phone': sh[3],
            'email': sh[4]
        })
    return shelters

def get_shelter(shelter_id):
    shelters = get_shelters()
    for s in shelters:
        if s['shelter_id'] == str(shelter_id):
            return s
    return None

# ADOPTION HISTORY (just for completeness, though not modified here)

def get_adoption_history():
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    a = read_file(path)
    history = []
    for h in a:
        history.append({
            'history_id': h[0],
            'username': h[1],
            'pet_id': h[2],
            'pet_name': h[3],
            'adoption_date': h[4],
            'shelter_id': h[5]
        })
    return history

# Validation helpers

def valid_age_format(age):
    # Must be "+ int + " years"
    return re.match(r'^\d+ years$', age) is not None

def valid_phone_format(phone):
    # Simple pattern: digits, dashes, spaces allowed
    return re.match(r'^[0-9\-\s\+]+$', phone) is not None

def valid_email_format(email):
    # Basic email pattern
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email) is not None

# Assume current user to simulate login (for demo and UI purposes), fixed
CURRENT_USER = 'john_doe'

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# 1. Dashboard
@app.route('/dashboard')
def dashboard():
    pets = get_pets()
    featured = [p for p in pets if p['status'] == 'Available'][:5]
    return render_template('templates_candidate_b/dashboard.html', featured_pets=featured)

# 2. Pet Listings
@app.route('/pets', methods=['GET'])
def pets():
    pets = get_pets()
    species_filter = request.args.get('species', 'All')
    search_query = request.args.get('search', '').lower()

    filtered_pets = []
    for pet in pets:
        if species_filter != 'All' and pet['species'] != species_filter:
            continue
        if search_query and search_query not in pet['name'].lower():
            continue
        if pet['status'] != 'Available':
            continue
        filtered_pets.append(pet)

    species_options = ['All','Dog','Cat','Bird','Rabbit','Other']
    return render_template('templates_candidate_b/pets.html', pets=filtered_pets, species_filter=species_filter, search_query=search_query, species_options=species_options)

# 3. Pet Details
@app.route('/pets/<pet_id>', methods=['GET', 'POST'])
def pet_details(pet_id):
    pet = get_pet(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pets'))
    
    # Handle favorites add/remove
    favorites = get_favorites()

    user_favorites = [f for f in favorites if f['username'] == CURRENT_USER]
    in_favorites = any(f['pet_id'] == pet_id for f in user_favorites)

    if request.method == 'POST':
        action = request.form.get('favorite_action')
        if action == 'add':
            if not in_favorites:
                favorites.append({
                    'username': CURRENT_USER,
                    'pet_id': pet_id,
                    'date_added': datetime.now().strftime('%Y-%m-%d')
                })
                write_favorites(favorites)
                flash(f'Added {pet["name"]} to favorites.', 'success')
            else:
                flash(f'{pet["name"]} is already in favorites.', 'info')
        elif action == 'remove':
            favorites = [f for f in favorites if not (f['username'] == CURRENT_USER and f['pet_id'] == pet_id)]
            write_favorites(favorites)
            flash(f'Removed {pet["name"]} from favorites.', 'success')
        return redirect(url_for('pet_details', pet_id=pet_id))

    return render_template('templates_candidate_b/pet_details.html', pet=pet, in_favorites=in_favorites)

# 4. Add Pet
@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    gender_options = ['Male', 'Female']
    size_options = ['Small', 'Medium', 'Large']
    if request.method == 'POST':
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '')
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '')
        size = request.form.get('pet-size-input', '')
        description = request.form.get('pet-description-input', '').strip()

        errors = []
        if not name:
            errors.append('Pet name is required.')
        if species not in species_options:
            errors.append('Valid species is required.')
        if gender not in gender_options:
            errors.append('Valid gender is required.')
        if size not in size_options:
            errors.append('Valid size is required.')
        if not valid_age_format(age):
            errors.append('Age must be in format like "2 years".')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('templates_candidate_b/add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options,
                                   pet_name=name, pet_species=species, pet_breed=breed, pet_age=age, pet_gender=gender, pet_size=size, pet_description=description)

        pets = get_pets()
        new_id = 1
        if pets:
            new_id = max(int(p['pet_id']) for p in pets) + 1

        new_pet = {
            'pet_id': str(new_id),
            'name': name,
            'species': species,
            'breed': breed,
            'age': age,
            'gender': gender,
            'size': size,
            'description': description,
            'shelter_id': '1',  # Default shelter id
            'status': 'Available',
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }

        pets.append(new_pet)
        write_pets(pets)
        flash(f'New pet "{name}" added successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('templates_candidate_b/add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options)

# 5. Adoption Application
@app.route('/adopt/<pet_id>', methods=['GET', 'POST'])
def adopt_pet(pet_id):
    pet = get_pet(pet_id)
    if not pet or pet['status'] != 'Available':
        flash('Pet not available for adoption.', 'error')
        return redirect(url_for('pets'))

    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        applicant_phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '')
        reason = request.form.get('reason', '').strip()

        errors = []
        if not applicant_name:
            errors.append('Applicant name is required.')
        if not valid_phone_format(applicant_phone):
            errors.append('Phone number format is invalid.')
        if not reason:
            errors.append('Reason for adoption is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('templates_candidate_b/adopt_pet.html', pet=pet, applicant_name=applicant_name, applicant_phone=applicant_phone, housing_type=housing_type, reason=reason)

        applications = get_applications()
        new_id = 1
        if applications:
            new_id = max(int(a['application_id']) for a in applications) + 1

        user = get_user(CURRENT_USER)
        address = user['address'] if user else ''

        new_application = {
            'application_id': str(new_id),
            'username': CURRENT_USER,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': address,
            'housing_type': housing_type,
            'has_yard': 'No',  # Not in form as per spec
            'other_pets': '',   # Not in form as per spec
            'experience': '',   # Not in form as per spec
            'reason': reason,
            'status': 'Pending',
            'date_submitted': datetime.now().strftime('%Y-%m-%d')
        }

        applications.append(new_application)
        write_applications(applications)
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('my_applications'))

    return render_template('templates_candidate_b/adopt_pet.html', pet=pet)

# 6. My Applications
@app.route('/my-applications', methods=['GET', 'POST'])
def my_applications():
    applications = get_applications()
    user_apps = [a for a in applications if a['username'] == CURRENT_USER]
    filter_status = request.args.get('filter-status', 'All')

    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'] == filter_status]

    pets = get_pets()
    pet_dict = {p['pet_id']: p for p in pets}

    return render_template('templates_candidate_b/my_applications.html', applications=user_apps, filter_status=filter_status, pet_dict=pet_dict)

# 7. Favorites
@app.route('/favorites', methods=['GET'])
def favorites():
    favorites = get_favorites()
    user_favs = [f for f in favorites if f['username'] == CURRENT_USER]
    pets = get_pets()
    pet_dict = {p['pet_id']: p for p in pets}
    favorite_pets = [pet_dict[f['pet_id']] for f in user_favs if f['pet_id'] in pet_dict]
    return render_template('templates_candidate_b/favorites.html', favorite_pets=favorite_pets)

# 8. Messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = get_messages()
    # Filter conversations for current user
    conversations = {}
    for m in messages:
        if m['sender_username'] == CURRENT_USER:
            other = m['recipient_username']
        elif m['recipient_username'] == CURRENT_USER:
            other = m['sender_username']
        else:
            continue
        if other not in conversations:
            conversations[other] = []
        conversations[other].append(m)

    selected_conversation = request.args.get('conversation')

    conv_messages = []
    conv_with = None
    if selected_conversation:
        conv_with = selected_conversation
        # Filter conversation messages
        conv_messages = [m for m in conversations.get(selected_conversation, [])]
        # Mark unread messages as read if recipient is current user
        changed = False
        for m in conv_messages:
            if m['recipient_username'] == CURRENT_USER and not m['is_read']:
                m['is_read'] = True
                changed = True
        if changed:
            write_messages(messages)

    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        content = request.form.get('message-input', '').strip()

        if not recipient or not subject or not content:
            flash('Please fill all message fields.', 'error')
            return redirect(url_for('messages', conversation=recipient))

        new_id = 1
        if messages:
            new_id = max(int(m['message_id']) for m in messages) + 1

        new_message = {
            'message_id': str(new_id),
            'sender_username': CURRENT_USER,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': False
        }

        messages.append(new_message)
        write_messages(messages)
        flash('Message sent successfully.', 'success')
        return redirect(url_for('messages', conversation=recipient))

    # Compose conversation list data for UI
    conv_overview = []
    for other_user, msgs in conversations.items():
        last_msg = sorted(msgs, key=lambda x: x['timestamp'])[-1]
        conv_overview.append({'other_user': other_user, 'last_msg': last_msg})

    users = get_users()
    user_names = [u['username'] for u in users]

    return render_template('templates_candidate_b/messages.html', conversations=conv_overview, conv_messages=conv_messages, conv_with=conv_with, current_user=CURRENT_USER, users=user_names)

# 9. Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_user(CURRENT_USER)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if not valid_email_format(new_email):
            flash('Invalid email format.', 'error')
            return render_template('templates_candidate_b/profile.html', user=user)

        update_user_email(CURRENT_USER, new_email)
        flash('Profile updated successfully.', 'success')
        # Reload user data
        user = get_user(CURRENT_USER)

    return render_template('templates_candidate_b/profile.html', user=user)

# 10. Admin Panel
@app.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel():
    applications = get_applications()
    pets = get_pets()

    # Handle application status updates
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'approve':
            app_id = request.form.get('application_id')
            for app in applications:
                if app['application_id'] == app_id:
                    app['status'] = 'Approved'
                    flash(f"Application {app_id} approved.", 'success')
                    break
            write_applications(applications)

        elif action == 'reject':
            app_id = request.form.get('application_id')
            for app in applications:
                if app['application_id'] == app_id:
                    app['status'] = 'Rejected'
                    flash(f"Application {app_id} rejected.", 'success')
                    break
            write_applications(applications)

        elif action == 'delete_pet':
            pet_id = request.form.get('pet_id')
            pets = [p for p in pets if p['pet_id'] != pet_id]
            write_pets(pets)
            flash(f"Deleted pet {pet_id}.", 'success')

        elif action == 'edit_pet':
            pet_id = request.form.get('pet_id')
            # Fetch pet data for edit
            pet = get_pet(pet_id)
            if pet:
                species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
                gender_options = ['Male', 'Female']
                size_options = ['Small', 'Medium', 'Large']
                return render_template('templates_candidate_b/edit_pet.html', pet=pet,
                                       species_options=species_options, gender_options=gender_options, size_options=size_options)

        elif action == 'submit_edit_pet':
            pet_id = request.form.get('pet-id')
            name = request.form.get('pet-name-input', '').strip()
            species = request.form.get('pet-species-input', '')
            breed = request.form.get('pet-breed-input', '').strip()
            age = request.form.get('pet-age-input', '').strip()
            gender = request.form.get('pet-gender-input', '')
            size = request.form.get('pet-size-input', '')
            description = request.form.get('pet-description-input', '').strip()

            errors = []
            species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
            gender_options = ['Male', 'Female']
            size_options = ['Small', 'Medium', 'Large']

            if not name:
                errors.append('Pet name is required.')
            if species not in species_options:
                errors.append('Valid species is required.')
            if gender not in gender_options:
                errors.append('Valid gender is required.')
            if size not in size_options:
                errors.append('Valid size is required.')
            if not valid_age_format(age):
                errors.append('Age must be in format like "2 years".')

            if errors:
                for e in errors:
                    flash(e, 'error')
                pet = get_pet(pet_id)
                return render_template('templates_candidate_b/edit_pet.html', pet=pet,
                                       species_options=species_options, gender_options=gender_options, size_options=size_options)

            pets = get_pets()
            for p in pets:
                if p['pet_id'] == pet_id:
                    p['name'] = name
                    p['species'] = species
                    p['breed'] = breed
                    p['age'] = age
                    p['gender'] = gender
                    p['size'] = size
                    p['description'] = description
                    break
            write_pets(pets)
            flash('Pet updated successfully.', 'success')
            return redirect(url_for('admin_panel'))

    pending_apps = [a for a in applications if a['status'].lower() == 'pending']

    return render_template('templates_candidate_b/admin_panel.html', applications=pending_apps, pets=pets)


if __name__ == '__main__':
    app.run(debug=True)
