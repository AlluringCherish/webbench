from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to read and write data

def load_pets():
    pets = []
    file_path = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(file_path):
        return pets
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 11:
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


def save_pets(pets):
    lines = []
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
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'pets.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def load_applications():
    applications = []
    file_path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(file_path):
        return applications
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 13:
                    application = {
                        'application_id': int(parts[0]),
                        'username': parts[1],
                        'pet_id': int(parts[2]),
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


def save_applications(applications):
    lines = []
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
        lines.append(line)
    with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')


def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 4:
                    user = {
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    }
                    users.append(user)
    return users


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 3:
                    fav = {
                        'username': parts[0],
                        'pet_id': int(parts[1]),
                        'date_added': parts[2]
                    }
                    favorites.append(fav)
    return favorites


def load_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(path):
        return messages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 7:
                    msg = {
                        'message_id': int(parts[0]),
                        'sender_username': parts[1],
                        'recipient_username': parts[2],
                        'subject': parts[3],
                        'content': parts[4],
                        'timestamp': parts[5],
                        'is_read': parts[6].lower() == 'true'
                    }
                    messages.append(msg)
    return messages


def load_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(path):
        return shelters
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 5:
                    shelter = {
                        'shelter_id': int(parts[0]),
                        'name': parts[1],
                        'address': parts[2],
                        'phone': parts[3],
                        'email': parts[4]
                    }
                    shelters.append(shelter)
    return shelters


def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


# Utility function to get current user
# For simplicity, we use a fixed username for all logged in actions
# In real app, this would come from session/login management

def get_current_username():
    # Returning a test username
    return 'john_doe'


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    pets = load_pets()
    # featured_pets: show up to 5 Available pets sorted by date_added desc
    featured_pets = [
        {'pet_id': p['pet_id'], 'name': p['name'], 'species': p['species'], 'age': p['age']}
        for p in sorted(pets, key=lambda x: x['date_added'], reverse=True) if p['status'] == 'Available'
    ][:5]

    # recent_activities: just some string messages - simulated from latest applications
    applications = load_applications()
    recent_activities = []
    for app in sorted(applications, key=lambda x: x['date_submitted'], reverse=True)[:5]:
        recent_activities.append(f"{app['applicant_name']} applied to adopt pet ID {app['pet_id']} on {app['date_submitted']}")

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)


@app.route('/pets', methods=['GET'])
def pet_listings_page():
    pets = load_pets()
    filter_species = request.args.get('filter_species', 'All')

    if filter_species != 'All':
        filtered = [
            { 'pet_id': p['pet_id'], 'name': p['name'], 'species': p['species'], 'age': p['age'], 'photo_url': f'/static/photos/{p["pet_id"]}.jpg' }
            for p in pets if p['species'] == filter_species and p['status'] == 'Available'
        ]
    else:
        filtered = [
            { 'pet_id': p['pet_id'], 'name': p['name'], 'species': p['species'], 'age': p['age'], 'photo_url': f'/static/photos/{p["pet_id"]}.jpg' }
            for p in pets if p['status'] == 'Available'
        ]

    return render_template('pet_listings.html', pets=filtered, filter_species=filter_species)


@app.route('/pets/search', methods=['POST'])
def pet_search():
    pets = load_pets()
    filter_species = request.form.get('filter_species', 'All')
    search_input = request.form.get('search_input', '').strip().lower()

    filtered = []
    for p in pets:
        if p['status'] != 'Available':
            continue
        if filter_species != 'All' and p['species'] != filter_species:
            continue
        if search_input and search_input not in p['name'].lower():
            continue
        filtered.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age'],
            'photo_url': f'/static/photos/{p["pet_id"]}.jpg'
        })

    return render_template('pet_listings.html', pets=filtered, filter_species=filter_species)


@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details_page(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET'])
def add_pet_page():
    return render_template('add_pet.html')


@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    form = request.form
    form_errors = {}

    name = form.get('pet-name-input', '').strip()
    species = form.get('pet-species-input', '')
    breed = form.get('pet-breed-input', '').strip()
    age = form.get('pet-age-input', '').strip()
    gender = form.get('pet-gender-input', '')
    size = form.get('pet-size-input', '')
    description = form.get('pet-description-input', '').strip()

    # Validate
    if not name:
        form_errors['pet-name-input'] = 'Name is required.'
    if species not in ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']:
        form_errors['pet-species-input'] = 'Invalid species selected.'
    if not breed:
        form_errors['pet-breed-input'] = 'Breed is required.'
    if not age:
        form_errors['pet-age-input'] = 'Age is required.'
    if gender not in ['Male', 'Female']:
        form_errors['pet-gender-input'] = 'Invalid gender selected.'
    if size not in ['Small', 'Medium', 'Large']:
        form_errors['pet-size-input'] = 'Invalid size selected.'
    if not description:
        form_errors['pet-description-input'] = 'Description is required.'

    if form_errors:
        return render_template('add_pet.html', form_errors=form_errors)

    pets = load_pets()
    max_id = max((p['pet_id'] for p in pets), default=0)
    new_pet_id = max_id + 1

    new_pet = {
        'pet_id': new_pet_id,
        'name': name,
        'species': species,
        'breed': breed,
        'age': age,
        'gender': gender,
        'size': size,
        'description': description,
        'shelter_id': 1,  # Default shelter (static as not part of form)
        'status': 'Available',
        'date_added': datetime.now().strftime('%Y-%m-%d')
    }
    pets.append(new_pet)
    save_pets(pets)

    # Redirect to pet listings page after success
    return redirect(url_for('pet_listings_page'))


@app.route('/applications/new/<int:pet_id>', methods=['GET'])
def adoption_application_page(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    pet_summary = {'pet_id': pet['pet_id'], 'name': pet['name']}
    return render_template('adoption_application.html', pet=pet_summary)


@app.route('/applications/new/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    form = request.form
    form_errors = {}

    applicant_name = form.get('applicant-name', '').strip()
    phone = form.get('applicant-phone', '').strip()
    housing_type = form.get('housing-type', '')
    reason = form.get('reason', '').strip()

    # Validate
    if not applicant_name:
        form_errors['applicant-name'] = 'Applicant name is required.'
    if not phone:
        form_errors['applicant-phone'] = 'Phone number is required.'
    if housing_type not in ['House', 'Apartment', 'Condo', 'Other']:
        form_errors['housing-type'] = 'Invalid housing type selected.'
    if not reason:
        form_errors['reason'] = 'Reason for adoption is required.'

    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    pet_summary = {'pet_id': pet['pet_id'], 'name': pet['name']}

    if form_errors:
        return render_template('adoption_application.html', pet=pet_summary, form_errors=form_errors)

    applications = load_applications()
    max_id = max((a['application_id'] for a in applications), default=0)
    new_application_id = max_id + 1

    username = get_current_username()
    user = get_user_by_username(username)

    # Assuming has_yard, other_pets, experience are empty/not from form (not defined in spec for form)
    new_app = {
        'application_id': new_application_id,
        'username': username,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': user['address'] if user else '',
        'housing_type': housing_type,
        'has_yard': 'No',
        'other_pets': '',
        'experience': '',
        'reason': reason,
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }

    applications.append(new_app)
    save_applications(applications)

    return redirect(url_for('my_applications_page'))


@app.route('/applications')
def my_applications_page():
    username = get_current_username()
    applications = load_applications()
    pets = load_pets()

    filter_status = request.args.get('filter_status', 'All')

    filtered_apps = []
    for app in applications:
        if app['username'] != username:
            continue
        if filter_status != 'All' and app['status'] != filter_status:
            continue
        pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
        filtered_apps.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=filtered_apps, filter_status=filter_status)


@app.route('/favorites')
def favorites_page():
    username = get_current_username()
    favorites = load_favorites()
    pets = load_pets()

    favorite_pets = []
    for fav in favorites:
        if fav['username'] != username:
            continue
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id'] and p['status'] == 'Available'), None)
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': f'/static/photos/{pet["pet_id"]}.jpg'
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages')
def messages_page():
    username = get_current_username()
    messages = load_messages()

    # Group messages into conversations by conversation_id == unique paired users and subject?
    # Spec says conversation: list of dict (conversation_id:int, with messages list)

    # We'll consider conversation_id as an integer starting from 1 to group messages by participants & subject
    # But our messages.txt only have message_id so we'll group by pairs and subject for demo

    # Group by a tuple key (user_min, user_max, subject)
    conv_map = {}

    for msg in messages:
        # Include only conversations the user is part of
        if username not in [msg['sender_username'], msg['recipient_username']]:
            continue
        users = sorted([msg['sender_username'], msg['recipient_username']])
        key = (users[0], users[1], msg['subject'])
        if key not in conv_map:
            conv_map[key] = {
                'conversation_id': len(conv_map) + 1,
                'messages': []
            }
        conv_map[key]['messages'].append(msg)

    conversations = []
    for val in conv_map.values():
        # Sort messages by timestamp asc
        val['messages'].sort(key=lambda m: m['timestamp'])
        conversations.append(val)

    # Sort conversations by last message timestamp desc
    conversations.sort(key=lambda c: c['messages'][-1]['timestamp'], reverse=True)

    user = {'username': username}
    return render_template('messages.html', conversations=conversations, user=user)


@app.route('/messages/send', methods=['POST'])
def send_message():
    form = request.form
    form_errors = {}
    sender = get_current_username()

    recipient = form.get('recipient_username', '').strip()
    subject = form.get('subject', '').strip()
    content = form.get('content', '').strip()

    if not recipient:
        form_errors['recipient_username'] = 'Recipient username is required.'
    if not subject:
        form_errors['subject'] = 'Subject is required.'
    if not content:
        form_errors['content'] = 'Content is required.'

    users = load_users()
    recipient_exists = any(u['username'] == recipient for u in users)
    if not recipient_exists:
        form_errors['recipient_username'] = 'Recipient user does not exist.'

    if form_errors:
        messages = load_messages()
        username = sender
        conv_map = {}
        for msg in messages:
            if username not in [msg['sender_username'], msg['recipient_username']]:
                continue
            users_pair = sorted([msg['sender_username'], msg['recipient_username']])
            key = (users_pair[0], users_pair[1], msg['subject'])
            if key not in conv_map:
                conv_map[key] = {
                    'conversation_id': len(conv_map) + 1,
                    'messages': []
                }
            conv_map[key]['messages'].append(msg)
        conversations = []
        for val in conv_map.values():
            val['messages'].sort(key=lambda m: m['timestamp'])
            conversations.append(val)
        conversations.sort(key=lambda c: c['messages'][-1]['timestamp'], reverse=True)
        user = {'username': username}
        return render_template('messages.html', conversations=conversations, user=user, form_errors=form_errors)

    messages = load_messages()
    max_id = max((m['message_id'] for m in messages), default=0)
    new_id = max_id + 1

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_msg = {
        'message_id': new_id,
        'sender_username': sender,
        'recipient_username': recipient,
        'subject': subject,
        'content': content,
        'timestamp': now_str,
        'is_read': False
    }
    messages.append(new_msg)

    # Save messages
    lines = []
    for m in messages:
        line = '|'.join([
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            'true' if m['is_read'] else 'false'
        ])
        lines.append(line)

    with open(os.path.join(DATA_DIR, 'messages.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' if lines else '')

    return redirect(url_for('messages_page'))


@app.route('/profile', methods=['GET'])
def user_profile_page():
    username = get_current_username()
    user = get_user_by_username(username)
    if not user:
        return "User not found", 404
    profile = {
        'username': user['username'],
        'email': user['email']
    }
    return render_template('profile.html', profile=profile)


@app.route('/profile', methods=['POST'])
def update_user_profile():
    form = request.form
    form_errors = {}

    email = form.get('profile-email', '').strip()

    if not email:
        form_errors['profile-email'] = 'Email is required.'
    elif '@' not in email:
        form_errors['profile-email'] = 'Invalid email address.'

    username = get_current_username()
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)

    if form_errors:
        profile = {
            'username': username,
            'email': email
        }
        return render_template('profile.html', profile=profile, form_errors=form_errors)

    if user:
        user['email'] = email
        # Save users
        lines = []
        for u in users:
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            lines.append(line)
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n' if lines else '')

    return redirect(url_for('user_profile_page'))


@app.route('/admin')
def admin_panel_page():
    applications = load_applications()
    pets = load_pets()

    pending_applications = [
        {
            'application_id': app['application_id'],
            'applicant_name': app['applicant_name'],
            'pet_name': next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown'),
            'date_submitted': app['date_submitted']
        }
        for app in applications if app['status'] == 'Pending'
    ]

    all_pets = [
        {
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'status': p['status']
        }
        for p in pets
    ]

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
