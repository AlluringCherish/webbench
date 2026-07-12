from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_FOLDER = 'data'

# Helper functions to load and save data

def read_users():
    users = []
    file_path = os.path.join(DATA_FOLDER, 'users.txt')
    if not os.path.exists(file_path):
        return users
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            user = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            }
            users.append(user)
    return users


def write_users(users):
    file_path = os.path.join(DATA_FOLDER, 'users.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for user in users:
            line = '|'.join([
                user['username'],
                user['email'],
                user['phone'],
                user['address']
            ])
            f.write(line + '\n')


def read_pets():
    pets = []
    file_path = os.path.join(DATA_FOLDER, 'pets.txt')
    if not os.path.exists(file_path):
        return pets
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 11:
                continue
            pet = {
                'pet_id': int(parts[0]),
                'name': parts[1],
                'species': parts[2],
                'breed': parts[3],
                'age': parts[4],
                'gender': parts[5],
                'size': parts[6],
                'description': parts[7],
                'shelter_id': int(parts[8]),
                'status': parts[9],
                'date_added': parts[10]
            }
            pets.append(pet)
    return pets


def write_pets(pets):
    file_path = os.path.join(DATA_FOLDER, 'pets.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for pet in pets:
            line = '|'.join([
                str(pet['pet_id']),
                pet['name'],
                pet['species'],
                pet['breed'],
                pet['age'],
                pet['gender'],
                pet['size'],
                pet['description'],
                str(pet['shelter_id']),
                pet['status'],
                pet['date_added']
            ])
            f.write(line + '\n')


def read_applications():
    applications = []
    file_path = os.path.join(DATA_FOLDER, 'applications.txt')
    if not os.path.exists(file_path):
        return applications
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 13:
                continue
            try:
                app_id = int(parts[0])
                pet_id = int(parts[2])
            except ValueError:
                continue
            application = {
                'application_id': app_id,
                'username': parts[1],
                'pet_id': pet_id,
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
            applications.append(application)
    return applications


def write_applications(applications):
    file_path = os.path.join(DATA_FOLDER, 'applications.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for app in applications:
            line = '|'.join([
                str(app['application_id']),
                app['username'],
                str(app['pet_id']),
                app['applicant_name'],
                app['phone'],
                app['address'],
                app['housing_type'],
                app['has_yard'],
                app['other_pets'],
                app['experience'],
                app['reason'],
                app['status'],
                app['date_submitted']
            ])
            f.write(line + '\n')


def read_favorites():
    favorites = []
    file_path = os.path.join(DATA_FOLDER, 'favorites.txt')
    if not os.path.exists(file_path):
        return favorites
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            try:
                pet_id = int(parts[1])
            except ValueError:
                continue
            fav = {
                'username': parts[0],
                'pet_id': pet_id,
                'date_added': parts[2]
            }
            favorites.append(fav)
    return favorites


def write_favorites(favorites):
    file_path = os.path.join(DATA_FOLDER, 'favorites.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav['username'],
                str(fav['pet_id']),
                fav['date_added']
            ])
            f.write(line + '\n')


def read_messages():
    messages = []
    file_path = os.path.join(DATA_FOLDER, 'messages.txt')
    if not os.path.exists(file_path):
        return messages
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 7:
                continue
            try:
                msg_id = int(parts[0])
            except ValueError:
                continue
            msg = {
                'message_id': msg_id,
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6]
            }
            messages.append(msg)
    return messages


def write_messages(messages):
    file_path = os.path.join(DATA_FOLDER, 'messages.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for msg in messages:
            line = '|'.join([
                str(msg['message_id']),
                msg['sender_username'],
                msg['recipient_username'],
                msg['subject'],
                msg['content'],
                msg['timestamp'],
                msg['is_read']
            ])
            f.write(line + '\n')


def read_shelters():
    shelters = []
    file_path = os.path.join(DATA_FOLDER, 'shelters.txt')
    if not os.path.exists(file_path):
        return shelters
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 5:
                continue
            try:
                sid = int(parts[0])
            except ValueError:
                continue
            shelter = {
                'shelter_id': sid,
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            }
            shelters.append(shelter)
    return shelters

# For adoption_history not needed currently but could be added same way

# Helper to get a pet by id

def get_pet_by_id(pet_id):
    pets = read_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None

# Helper to get user by username

def get_user_by_username(username):
    users = read_users()
    for u in users:
        if u['username'] == username:
            return u
    return None

# Helper to generate next pet_id

def generate_next_pet_id():
    pets = read_pets()
    if not pets:
        return 1
    return max(pet['pet_id'] for pet in pets) + 1

# Helper to generate next application_id

def generate_next_application_id():
    applications = read_applications()
    if not applications:
        return 1
    return max(app['application_id'] for app in applications) + 1

# Helper to generate next message_id

def generate_next_message_id():
    messages = read_messages()
    if not messages:
        return 1
    return max(msg['message_id'] for msg in messages) + 1

# For demonstration, assume current user is john_doe
# In real scenario, would integrate with auth system

CURRENT_USER = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    pets = read_pets()
    # Filter to available pets for featured
    available_pets = [pet for pet in pets if pet['status'] == 'Available']
    # Sort by date_added desc, most recent first
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = available_pets[:5]
    # For recent_activities optional omit since not specified clearly
    recent_activities = []
    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)


@app.route('/pets')
def pet_listings():
    species_filter = request.args.get('species', 'All')
    search_term = request.args.get('search', '').strip().lower()
    pets = read_pets()
    filtered = []
    for pet in pets:
        if pet['status'] != 'Available':
            continue
        if species_filter != 'All' and pet['species'].lower() != species_filter.lower():
            continue
        if search_term and search_term not in pet['name'].lower() and search_term not in pet['breed'].lower():
            continue
        filtered.append(pet)
    return render_template('pet_listings.html', pets=filtered, species_filter=species_filter)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'GET':
        return render_template('add_pet.html')
    # POST
    name = request.form.get('pet-name-input', '').strip()
    species = request.form.get('pet-species-input', '').strip()
    breed = request.form.get('pet-breed-input', '').strip()
    age = request.form.get('pet-age-input', '').strip()
    gender = request.form.get('pet-gender-input', '').strip()
    size = request.form.get('pet-size-input', '').strip()
    description = request.form.get('pet-description-input', '').strip()

    # Validate required fields
    errors = []
    if not name:
        errors.append('Name is required')
    if species not in ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']:
        errors.append('Invalid species')
    if not breed:
        errors.append('Breed is required')
    if not age:
        errors.append('Age is required')
    if gender not in ['Male', 'Female']:
        errors.append('Invalid gender')
    if size not in ['Small', 'Medium', 'Large']:
        errors.append('Invalid size')
    if not description:
        errors.append('Description is required')

    if errors:
        # Optionally pass form data and errors back
        context = {
            'form_data': request.form,
            'errors': errors
        }
        return render_template('add_pet.html', **context)

    pets = read_pets()
    new_pet_id = generate_next_pet_id()
    # Assuming shelter_id for current user is 1, since no user-shelter relation given
    shelter_id = 1
    new_pet = {
        'pet_id': new_pet_id,
        'name': name,
        'species': species,
        'breed': breed,
        'age': age,
        'gender': gender,
        'size': size,
        'description': description,
        'shelter_id': shelter_id,
        'status': 'Available',
        'date_added': datetime.now().strftime('%Y-%m-%d')
    }
    pets.append(new_pet)
    write_pets(pets)
    return redirect(url_for('dashboard'))


@app.route('/applications/apply/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return "Pet not found", 404
    if request.method == 'GET':
        return render_template('adoption_application.html', pet=pet)

    # POST submission
    applicant_name = request.form.get('applicant-name', '').strip()
    phone = request.form.get('applicant-phone', '').strip()
    housing_type = request.form.get('housing-type', '').strip()
    reason = request.form.get('reason', '').strip()

    # Basic validation
    errors = []
    if not applicant_name:
        errors.append('Applicant name is required')
    if not phone:
        errors.append('Phone is required')
    if housing_type not in ['House', 'Apartment', 'Condo', 'Other']:
        errors.append('Invalid housing type')
    if not reason:
        errors.append('Reason for adoption is required')

    # Retrieve current user info
    user = get_user_by_username(CURRENT_USER)
    if not user:
        return "User not found", 404

    if errors:
        context = {
            'pet': pet,
            'errors': errors,
            'form_data': request.form
        }
        return render_template('adoption_application.html', **context)

    applications = read_applications()
    new_app_id = generate_next_application_id()

    # For missing fields in application definition: has_yard, other_pets, experience - set defaults empty
    new_application = {
        'application_id': new_app_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': user.get('address', ''),
        'housing_type': housing_type,
        'has_yard': 'No',
        'other_pets': '',
        'experience': '',
        'reason': reason,
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }
    applications.append(new_application)
    write_applications(applications)
    return redirect(url_for('my_applications'))


@app.route('/applications/my')
def my_applications():
    status_filter = request.args.get('status', 'All')
    applications = read_applications()
    user_apps = [app for app in applications if app['username'] == CURRENT_USER]

    if status_filter != 'All':
        user_apps = [app for app in user_apps if app['status'] == status_filter]

    return render_template('my_applications.html', applications=user_apps, status_filter=status_filter)


@app.route('/favorites')
def favorites():
    favorites_list = read_favorites()
    pets = read_pets()
    # Filter favorites for current user
    user_favorites = [fav for fav in favorites_list if fav['username'] == CURRENT_USER]
    # Map favorites to pet dicts
    favorite_pets = []
    pet_dict = {pet['pet_id']: pet for pet in pets}
    for fav in user_favorites:
        pet = pet_dict.get(fav['pet_id'])
        if pet:
            favorite_pets.append(pet)
    return render_template('favorites.html', favorites=favorite_pets)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages_list = read_messages()
    conversations = []
    messages_view = []

    # Collect conversations for current user
    # Conversations defined by unique other user in messages
    other_users = set()
    for msg in messages_list:
        if msg['sender_username'] == CURRENT_USER:
            other_users.add(msg['recipient_username'])
        elif msg['recipient_username'] == CURRENT_USER:
            other_users.add(msg['sender_username'])

    # Build conversation dicts
    for ou in other_users:
        conversation = {
            'username': ou
        }
        conversations.append(conversation)

    # If POST, handle sending new message
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        errors = []
        if not recipient:
            errors.append('Recipient is required')
        if not subject:
            errors.append('Subject is required')
        if not content:
            errors.append('Content is required')

        if errors:
            # Show current conversations and empty messages
            return render_template('messages.html', conversations=conversations, messages=[], errors=errors)

        # New message id
        new_msg_id = generate_next_message_id()

        new_msg = {
            'message_id': new_msg_id,
            'sender_username': CURRENT_USER,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': 'false'
        }
        messages_list.append(new_msg)
        write_messages(messages_list)
        # Refresh conversations
        return redirect(url_for('messages'))

    # GET shows all conversations and optionally the latest messages
    # For simplicity show empty messages list
    return render_template('messages.html', conversations=conversations, messages=messages_view)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = read_users()
    user = get_user_by_username(CURRENT_USER)
    if not user:
        return "User not found", 404

    if request.method == 'GET':
        return render_template('profile.html', user_profile=user)

    # POST update
    email = request.form.get('profile-email', '').strip()
    phone = request.form.get('profile-phone', '').strip()
    address = request.form.get('profile-address', '').strip()

    # Update user dict
    updated = False
    for u in users:
        if u['username'] == CURRENT_USER:
            if email:
                u['email'] = email
            if phone:
                u['phone'] = phone
            if address:
                u['address'] = address
            updated = True
            break

    if updated:
        write_users(users)

    # Reload updated user for context
    user_updated = get_user_by_username(CURRENT_USER)
    return render_template('profile.html', user_profile=user_updated)


@app.route('/admin')
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    pending_applications = [app for app in applications if app['status'] == 'Pending']
    all_pets = pets

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
