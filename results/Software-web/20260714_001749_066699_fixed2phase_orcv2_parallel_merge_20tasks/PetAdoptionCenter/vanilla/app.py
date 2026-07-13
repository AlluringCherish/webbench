from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key_for_session'

DATA_DIR = 'data'

# Utility functions for file handling

def read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.read().strip().split('\n')
    return lines


def write_file_lines(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n' if lines else '')


def parse_pipe_line(line, num_fields=None):
    parts = line.split('|')
    if num_fields and len(parts) != num_fields:
        return None
    return parts


def get_current_username():
    # For demo, we assume a fixed logged-in user
    # In real app, integrate with user sessions / auth
    return 'john_doe'


# ----------------------------------
# USERS UTILS


def read_users():
    lines = read_file_lines('users.txt')
    users = {}
    for line in lines:
        fields = parse_pipe_line(line, 4)
        if fields:
            username, email, phone, address = fields
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users


def write_users(users):
    lines = []
    for u in users.values():
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    write_file_lines('users.txt', lines)


# ----------------------------------
# PETS UTILS


def read_pets():
    lines = read_file_lines('pets.txt')
    pets = []
    for line in lines:
        fields = parse_pipe_line(line, 11)
        if fields:
            pet = {
                'pet_id': int(fields[0]),
                'name': fields[1],
                'species': fields[2],
                'breed': fields[3],
                'age': fields[4],
                'gender': fields[5],
                'size': fields[6],
                'description': fields[7],
                'shelter_id': int(fields[8]),
                'status': fields[9],
                'date_added': fields[10]
            }
            pets.append(pet)
    return pets


def write_pets(pets):
    lines = []
    for p in pets:
        line = '|'.join([
            str(p['pet_id']), p['name'], p['species'], p['breed'],
            p['age'], p['gender'], p['size'], p['description'],
            str(p['shelter_id']), p['status'], p['date_added']
        ])
        lines.append(line)
    write_file_lines('pets.txt', lines)


def get_new_pet_id(pets):
    if not pets:
        return 1
    return max(p['pet_id'] for p in pets) + 1


# ----------------------------------
# APPLICATIONS UTILS


def read_applications():
    lines = read_file_lines('applications.txt')
    applications = []
    for line in lines:
        fields = parse_pipe_line(line, 13)
        if fields:
            app = {
                'application_id': int(fields[0]),
                'username': fields[1],
                'pet_id': int(fields[2]),
                'applicant_name': fields[3],
                'phone': fields[4],
                'address': fields[5],
                'housing_type': fields[6],
                'has_yard': fields[7],
                'other_pets': fields[8],
                'experience': fields[9],
                'reason': fields[10],
                'status': fields[11],
                'date_submitted': fields[12]
            }
            applications.append(app)
    return applications


def write_applications(applications):
    lines = []
    for a in applications:
        line = '|'.join([
            str(a['application_id']), a['username'], str(a['pet_id']), a['applicant_name'], a['phone'],
            a['address'], a['housing_type'], a['has_yard'], a['other_pets'], a['experience'],
            a['reason'], a['status'], a['date_submitted']
        ])
        lines.append(line)
    write_file_lines('applications.txt', lines)


def get_new_application_id(applications):
    if not applications:
        return 1
    return max(a['application_id'] for a in applications) + 1


# ----------------------------------
# FAVORITES UTILS


def read_favorites():
    lines = read_file_lines('favorites.txt')
    favorites = []
    for line in lines:
        fields = parse_pipe_line(line, 3)
        if fields:
            favorites.append({
                'username': fields[0],
                'pet_id': int(fields[1]),
                'date_added': fields[2]
            })
    return favorites


def write_favorites(favorites):
    lines = []
    for f in favorites:
        line = '|'.join([f['username'], str(f['pet_id']), f['date_added']])
        lines.append(line)
    write_file_lines('favorites.txt', lines)


# ----------------------------------
# MESSAGES UTILS


def read_messages():
    lines = read_file_lines('messages.txt')
    messages = []
    for line in lines:
        fields = parse_pipe_line(line, 7)
        if fields:
            msg = {
                'message_id': int(fields[0]),
                'sender_username': fields[1],
                'recipient_username': fields[2],
                'subject': fields[3],
                'content': fields[4],
                'timestamp': fields[5],
                'is_read': fields[6].lower() == 'true'
            }
            messages.append(msg)
    return messages


def write_messages(messages):
    lines = []
    for m in messages:
        line = '|'.join([
            str(m['message_id']), m['sender_username'], m['recipient_username'], m['subject'],
            m['content'], m['timestamp'], 'true' if m['is_read'] else 'false'
        ])
        lines.append(line)
    write_file_lines('messages.txt', lines)


def get_new_message_id(messages):
    if not messages:
        return 1
    return max(m['message_id'] for m in messages) + 1


# ----------------------------------
# ADOPTION HISTORY UTILS


def read_adoption_history():
    lines = read_file_lines('adoption_history.txt')
    history = []
    for line in lines:
        fields = parse_pipe_line(line, 6)
        if fields:
            history.append({
                'history_id': int(fields[0]),
                'username': fields[1],
                'pet_id': int(fields[2]),
                'pet_name': fields[3],
                'adoption_date': fields[4],
                'shelter_id': int(fields[5])
            })
    return history


# ----------------------------------
# SHELTERS UTILS


def read_shelters():
    lines = read_file_lines('shelters.txt')
    shelters = {}
    for line in lines:
        fields = parse_pipe_line(line, 5)
        if fields:
            shelter_id = int(fields[0])
            shelters[shelter_id] = {
                'shelter_id': shelter_id,
                'name': fields[1],
                'address': fields[2],
                'phone': fields[3],
                'email': fields[4]
            }
    return shelters


# ----------------------------------
# ROUTES IMPLEMENTATION

@app.route('/dashboard', methods=['GET'])
def dashboard():
    'Load main dashboard displaying featured pets and recent activities'
    pets = read_pets()
    # Filter only available pets
    available_pets = [p for p in pets if p['status'].lower() == 'available']
    # Sort by date_added descending
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = available_pets[:5]

    # For recent activities, we can simulate by latest applications or adoption history
    applications = read_applications()
    applications.sort(key=lambda a: a['date_submitted'], reverse=True)
    recent_applications = applications[:5]

    return render_template('dashboard.html', featured_pets=featured_pets, recent_applications=recent_applications)


@app.route('/pets', methods=['GET'])
def pet_listings():
    'List all available pets applying optional filters'
    search = request.args.get('search', '').strip().lower()
    species_filter = request.args.get('species', 'All')

    pets = read_pets()

    # Filter by status Available
    filtered = [p for p in pets if p['status'].lower() == 'available']

    # Filter by species if not All
    if species_filter != 'All':
        filtered = [p for p in filtered if p['species'].lower() == species_filter.lower()]

    # Filter by search term in name
    if search:
        filtered = [p for p in filtered if search in p['name'].lower()]

    return render_template('pet_listings.html', pets=filtered, search=search, species_filter=species_filter)


@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    'Show detailed information for a pet by pet_id'
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        flash('Pet not found', 'error')
        return redirect(url_for('pet_listings'))

    shelters = read_shelters()
    shelter = shelters.get(pet['shelter_id'], None)

    return render_template('pet_details.html', pet=pet, shelter=shelter)


@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    'Allow shelter admins to add new pet listings'
    if request.method == 'GET':
        return render_template('add_pet.html')

    # POST method - handle add pet form submission
    name = request.form.get('name', '').strip()
    species = request.form.get('species', '').strip()
    breed = request.form.get('breed', '').strip()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    size = request.form.get('size', '').strip()
    description = request.form.get('description', '').strip()

    # Basic validation
    if not all([name, species, breed, age, gender, size, description]):
        flash('All fields are required.', 'error')
        return render_template('add_pet.html',
                               pet_name=name, pet_species=species, pet_breed=breed, pet_age=age,
                               pet_gender=gender, pet_size=size, pet_description=description)

    pets = read_pets()
    new_id = get_new_pet_id(pets)
    date_added = datetime.now().strftime('%Y-%m-%d')

    # For shelter_id, we use 1 as default shelter for demo
    shelter_id = 1

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
        'status': 'Available',
        'date_added': date_added
    }
    pets.append(new_pet)
    write_pets(pets)

    flash('New pet added successfully.', 'success')
    return redirect(url_for('pet_listings'))


@app.route('/applications/add/<int:pet_id>', methods=['GET', 'POST'])
def add_application(pet_id):
    'Submit new adoption application for pet_id'
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None or pet['status'].lower() != 'available':
        flash('Pet not available for adoption.', 'error')
        return redirect(url_for('pet_listings'))

    if request.method == 'GET':
        return render_template('adoption_application.html', pet=pet)

    # POST - form submission handling
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_phone = request.form.get('phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    # Validate required fields
    if not all([applicant_name, applicant_phone, housing_type, reason]):
        flash('All fields are required.', 'error')
        return render_template('adoption_application.html', pet=pet,
                               applicant_name=applicant_name,
                               applicant_phone=applicant_phone,
                               housing_type=housing_type,
                               reason=reason)

    # For simplicity, we don't handle has_yard, other_pets, experience inputs as not specified in form
    applications = read_applications()
    new_id = get_new_application_id(applications)
    date_submitted = datetime.now().strftime('%Y-%m-%d')

    username = get_current_username()

    new_application = {
        'application_id': new_id,
        'username': username,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': '',  # User address not requested here
        'housing_type': housing_type,
        'has_yard': 'No',  # Default No
        'other_pets': 'None',  # Default None
        'experience': 'No experience',  # Default text
        'reason': reason,
        'status': 'Pending',
        'date_submitted': date_submitted
    }

    applications.append(new_application)
    write_applications(applications)

    flash('Adoption application submitted successfully.', 'success')
    return redirect(url_for('my_applications'))


@app.route('/applications', methods=['GET'])
def my_applications():
    'List current user adoption applications filtered by status'
    username = get_current_username()
    status_filter = request.args.get('status', 'All')

    applications = read_applications()
    pets = read_pets()

    user_apps = [a for a in applications if a['username'] == username]

    if status_filter != 'All':
        user_apps = [a for a in user_apps if a['status'].lower() == status_filter.lower()]

    # Attach pet name for display
    for a in user_apps:
        pet = next((p for p in pets if p['pet_id'] == a['pet_id']), None)
        a['pet_name'] = pet['name'] if pet else 'Unknown'

    return render_template('my_applications.html', applications=user_apps, status_filter=status_filter)


@app.route('/favorites', methods=['GET'])
def favorites():
    'Display pets marked as favorites by current user'
    username = get_current_username()
    favorites = read_favorites()
    pets = read_pets()

    user_favs = [f for f in favorites if f['username'] == username]

    fav_pets = []
    for fav in user_favs:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            fav_pets.append(pet)

    return render_template('favorites.html', favorite_pets=fav_pets)


@app.route('/favorites/add/<int:pet_id>', methods=['POST'])
def add_favorite(pet_id):
    'Add a pet to user favorites'
    username = get_current_username()
    favorites = read_favorites()
    if any(f['username'] == username and f['pet_id'] == pet_id for f in favorites):
        flash('Pet already in favorites.', 'info')
        return redirect(url_for('favorites'))

    date_added = datetime.now().strftime('%Y-%m-%d')
    favorites.append({'username': username, 'pet_id': pet_id, 'date_added': date_added})
    write_favorites(favorites)

    flash('Pet added to favorites.', 'success')
    return redirect(url_for('favorites'))


@app.route('/favorites/remove/<int:pet_id>', methods=['POST'])
def remove_favorite(pet_id):
    'Remove a pet from user favorites'
    username = get_current_username()
    favorites = read_favorites()
    new_favs = [f for f in favorites if not (f['username'] == username and f['pet_id'] == pet_id)]
    write_favorites(new_favs)

    flash('Pet removed from favorites.', 'success')
    return redirect(url_for('favorites'))


@app.route('/messages', methods=['GET'])
def messages():
    'Display list of message conversations for current user'
    username = get_current_username()
    messages = read_messages()

    # Build conversation partner list
    partners = {}
    for m in messages:
        if m['sender_username'] == username:
            other = m['recipient_username']
        elif m['recipient_username'] == username:
            other = m['sender_username']
        else:
            continue
        if other not in partners:
            partners[other] = []
        partners[other].append(m)

    # Prepare conversation summary: last message timestamp
    conversations = []
    for partner, msgs in partners.items():
        last_msg = max(msgs, key=lambda x: x['timestamp'])
        conversations.append({
            'other_username': partner,
            'last_message': last_msg['content'],
            'last_timestamp': last_msg['timestamp'],
            'unread_count': sum(1 for x in msgs if (x['recipient_username'] == username and not x['is_read']))
        })

    # Sort conversations by last_timestamp desc
    conversations.sort(key=lambda c: c['last_timestamp'], reverse=True)

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    'Send message from current user to shelter or other user'
    sender = get_current_username()
    recipient = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('message', '').strip()

    if not all([recipient, subject, content]):
        flash('All message fields are required.', 'error')
        return redirect(url_for('messages'))

    messages = read_messages()
    new_id = get_new_message_id(messages)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_msg = {
        'message_id': new_id,
        'sender_username': sender,
        'recipient_username': recipient,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': False
    }

    messages.append(new_msg)
    write_messages(messages)

    flash('Message sent successfully.', 'success')
    return redirect(url_for('messages'))


@app.route('/messages/conversation/<string:other_username>', methods=['GET'])
def view_conversation(other_username):
    'View message history between current user and other_username'
    username = get_current_username()
    messages = read_messages()

    # Filter messages between these two users
    conversation_msgs = [m for m in messages if
                         (m['sender_username'] == username and m['recipient_username'] == other_username) or
                         (m['sender_username'] == other_username and m['recipient_username'] == username)]

    # Mark received messages as read
    new_msgs = []
    changed = False
    for m in messages:
        if ((m['sender_username'] == other_username and m['recipient_username'] == username) and not m['is_read']):
            m['is_read'] = True
            changed = True
        new_msgs.append(m)

    if changed:
        write_messages(new_msgs)

    return render_template('conversation.html', messages=conversation_msgs, other_username=other_username)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    'View and update user profile information'
    username = get_current_username()
    users = read_users()
    user = users.get(username)
    if user is None:
        flash('User not found', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('profile.html', user=user)

    # POST update email
    new_email = request.form.get('profile-email', '').strip()
    if not new_email:
        flash('Email cannot be empty.', 'error')
        return render_template('profile.html', user=user)

    users[username]['email'] = new_email
    write_users(users)
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('profile'))


@app.route('/admin', methods=['GET'])
def admin_panel():
    'Display list of pending applications and all pets with edit/delete options'
    applications = read_applications()
    pets = read_pets()

    pending_apps = [a for a in applications if a['status'].lower() == 'pending']

    # Attach pet name to applications for display
    pets_dict = {pet['pet_id']: pet for pet in pets}
    for app in pending_apps:
        pet = pets_dict.get(app['pet_id'])
        app['pet_name'] = pet['name'] if pet else 'Unknown'

    return render_template('admin_panel.html', pending_applications=pending_apps, all_pets=pets)


@app.route('/admin/application/<int:application_id>/update', methods=['POST'])
def admin_update_application(application_id):
    'Admin updates adoption application status'
    new_status = request.form.get('status', '').strip()
    if new_status not in ['Pending', 'Approved', 'Rejected']:
        flash('Invalid status update.', 'error')
        return redirect(url_for('admin_panel'))

    applications = read_applications()
    updated = False
    for app in applications:
        if app['application_id'] == application_id:
            app['status'] = new_status
            updated = True
            break

    if updated:
        write_applications(applications)
        flash('Application status updated.', 'success')
    else:
        flash('Application not found.', 'error')

    return redirect(url_for('admin_panel'))


@app.route('/admin/pet/<int:pet_id>/edit', methods=['GET', 'POST'])
def admin_edit_pet(pet_id):
    'Admin edits pet details'
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        flash('Pet not found.', 'error')
        return redirect(url_for('admin_panel'))

    if request.method == 'GET':
        return render_template('edit_pet.html', pet=pet)

    # POST - apply edits
    name = request.form.get('pet-name-input', '').strip()
    species = request.form.get('pet-species-input', '').strip()
    breed = request.form.get('pet-breed-input', '').strip()
    age = request.form.get('pet-age-input', '').strip()
    gender = request.form.get('pet-gender-input', '').strip()
    size = request.form.get('pet-size-input', '').strip()
    description = request.form.get('pet-description-input', '').strip()

    if not all([name, species, breed, age, gender, size, description]):
        flash('All fields are required.', 'error')
        return render_template('edit_pet.html', pet=pet)

    # Update fields
    pet['name'] = name
    pet['species'] = species
    pet['breed'] = breed
    pet['age'] = age
    pet['gender'] = gender
    pet['size'] = size
    pet['description'] = description

    # Write back updated pets list
    write_pets(pets)

    flash('Pet details updated successfully.', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/pet/<int:pet_id>/delete', methods=['POST'])
def admin_delete_pet(pet_id):
    'Admin deletes pet from listings'
    pets = read_pets()
    new_pets = [p for p in pets if p['pet_id'] != pet_id]

    if len(new_pets) == len(pets):
        flash('Pet not found.', 'error')
    else:
        write_pets(new_pets)
        flash('Pet deleted successfully.', 'success')

    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
