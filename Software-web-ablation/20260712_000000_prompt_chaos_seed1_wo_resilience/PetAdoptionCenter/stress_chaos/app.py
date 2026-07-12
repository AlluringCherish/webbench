from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data files

def load_users():
    users = []
    filepath = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(filepath):
        return users
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            user = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            }
            users.append(user)
    return users


def load_pets():
    pets = []
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(filepath):
        return pets
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 11:
                continue
            try:
                pet_id = int(parts[0])
                shelter_id = int(parts[8])
            except ValueError:
                continue
            pet = {
                'pet_id': pet_id,
                'name': parts[1],
                'species': parts[2],
                'breed': parts[3],
                'age': parts[4],
                'gender': parts[5],
                'size': parts[6],
                'description': parts[7],
                'shelter_id': shelter_id,
                'status': parts[9],
                'date_added': parts[10]
            }
            pets.append(pet)
    return pets


def save_pets(pets):
    filepath = os.path.join(DATA_DIR, 'pets.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for pet in pets:
            line = f"{pet['pet_id']}|{pet['name']}|{pet['species']}|{pet['breed']}|{pet['age']}|{pet['gender']}|{pet['size']}|{pet['description']}|{pet['shelter_id']}|{pet['status']}|{pet['date_added']}\n"
            f.write(line)


def load_applications():
    applications = []
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(filepath):
        return applications
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 13:
                continue
            try:
                application_id = int(parts[0])
                pet_id = int(parts[2])
            except ValueError:
                continue
            app = {
                'application_id': application_id,
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
            applications.append(app)
    return applications


def save_applications(applications):
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for app in applications:
            line = (f"{app['application_id']}|{app['username']}|{app['pet_id']}|{app['applicant_name']}|{app['phone']}|"
                    f"{app['address']}|{app['housing_type']}|{app['has_yard']}|{app['other_pets']}|{app['experience']}|"
                    f"{app['reason']}|{app['status']}|{app['date_submitted']}\n")
            f.write(line)


def load_favorites():
    favorites = []
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(filepath):
        return favorites
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            try:
                pet_id = int(parts[1])
            except ValueError:
                continue
            favorites.append({
                'username': parts[0],
                'pet_id': pet_id,
                'date_added': parts[2]
            })
    return favorites


def load_messages():
    messages = []
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(filepath):
        return messages
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            try:
                message_id = int(parts[0])
            except ValueError:
                continue
            messages.append({
                'message_id': message_id,
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6]
            })
    return messages


def save_messages(messages):
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for msg in messages:
            line = f"{msg['message_id']}|{msg['sender_username']}|{msg['recipient_username']}|{msg['subject']}|{msg['content']}|{msg['timestamp']}|{msg['is_read']}\n"
            f.write(line)


def load_shelters():
    shelters = []
    filepath = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(filepath):
        return shelters
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                shelter_id = int(parts[0])
            except ValueError:
                continue
            shelters.append({
                'shelter_id': shelter_id,
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            })
    return shelters


def load_adoption_history():
    history = []
    filepath = os.path.join(DATA_DIR, 'adoption_history.txt')
    if not os.path.exists(filepath):
        return history
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                history_id = int(parts[0])
                pet_id = int(parts[2])
                shelter_id = int(parts[5])
            except ValueError:
                continue
            history.append({
                'history_id': history_id,
                'username': parts[1],
                'pet_id': pet_id,
                'pet_name': parts[3],
                'adoption_date': parts[4],
                'shelter_id': shelter_id
            })
    return history


# Helper to find user by username

def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    # Featured pets: up to 5 with status Available, sorted by date_added descending
    available_pets = [p for p in pets if p['status'] == 'Available']
    # Sort by date_added descending
    available_pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured = []
    for p in available_pets[:5]:
        featured.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age'],
            'photo_url': None  # No photo_url field in data schema, so optional None
        })

    recent_activities = []  # Spec says optional, none implemented

    return render_template('dashboard.html', featured_pets=featured, recent_activities=recent_activities)


@app.route('/pets')
def pet_listings():
    pets = load_pets()
    filter_species = request.args.get('filter_species', '')
    search_query = request.args.get('search_query', '')

    filtered_pets = pets

    if filter_species:
        filtered_pets = [p for p in filtered_pets if p['species'].lower() == filter_species.lower()]

    if search_query:
        sq = search_query.lower()
        filtered_pets = [p for p in filtered_pets if sq in p['name'].lower() or sq in p['breed'].lower() or sq in p['description'].lower()]

    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species, search_query=search_query)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if pet is None:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET'])
def add_pet():
    return render_template('add_pet.html')


@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    # Extract form data
    pet_name = request.form.get('pet_name', '').strip()
    pet_species = request.form.get('pet_species', '').strip()
    pet_breed = request.form.get('pet_breed', '').strip()
    pet_age = request.form.get('pet_age', '').strip()
    pet_gender = request.form.get('pet_gender', '').strip()
    pet_size = request.form.get('pet_size', '').strip()
    pet_description = request.form.get('pet_description', '').strip()

    # Load current pets to get max pet_id
    pets = load_pets()
    max_id = max((p['pet_id'] for p in pets), default=0)
    new_id = max_id + 1

    # For shelter_id we do not have form data, use default 1
    shelter_id = 1
    # Status default Available
    status = 'Available'
    # date_added today
    date_added = datetime.now().strftime('%Y-%m-%d')

    new_pet = {
        'pet_id': new_id,
        'name': pet_name,
        'species': pet_species,
        'breed': pet_breed,
        'age': pet_age,
        'gender': pet_gender,
        'size': pet_size,
        'description': pet_description,
        'shelter_id': shelter_id,
        'status': status,
        'date_added': date_added
    }

    pets.append(new_pet)
    save_pets(pets)

    return redirect(url_for('dashboard'))


@app.route('/applications/new/<int:pet_id>', methods=['GET'])
def adoption_application_page(pet_id):
    pets = load_pets()
    pet_name = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet_name = p['name']
            break
    if pet_name is None:
        return "Pet not found", 404
    return render_template('adoption_application.html', pet_id=pet_id, pet_name=pet_name)


@app.route('/applications/new/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_phone = request.form.get('applicant_phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    users = load_users()
    # Use first user in users as username if exists, else empty string
    username = users[0]['username'] if users else ''

    # Fill other fields as empty or default
    address = ''
    has_yard = 'No'
    other_pets = ''
    experience = ''
    status = 'Pending'
    date_submitted = datetime.now().strftime('%Y-%m-%d')

    applications = load_applications()
    max_id = max((a['application_id'] for a in applications), default=0)
    new_id = max_id + 1

    new_app = {
        'application_id': new_id,
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
        'status': status,
        'date_submitted': date_submitted
    }

    applications.append(new_app)
    save_applications(applications)

    return redirect(url_for('pet_details', pet_id=pet_id))


@app.route('/applications')
def my_applications():
    applications = load_applications()
    pets = load_pets()

    filter_status = request.args.get('filter_status', '')

    filtered_apps = applications
    if filter_status:
        filtered_apps = [a for a in filtered_apps if a['status'].lower() == filter_status.lower()]

    result = []
    pet_id_name_map = {p['pet_id']: p['name'] for p in pets}
    for app in filtered_apps:
        result.append({
            'application_id': app['application_id'],
            'pet_name': pet_id_name_map.get(app['pet_id'], 'Unknown'),
            'date': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=result, filter_status=filter_status)


@app.route('/favorites')
def favorites():
    favorites_list = load_favorites()
    pets = load_pets()

    # Current user username (simulate using first user if available)
    users = load_users()
    username = users[0]['username'] if users else ''

    user_favorites = [f for f in favorites_list if f['username'] == username]

    pet_id_map = {p['pet_id']: p for p in pets}

    favorite_pets = []
    for f in user_favorites:
        pet = pet_id_map.get(f['pet_id'])
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages')
def messages():
    messages_list = load_messages()

    # Current user username (simulate using first user if available)
    users = load_users()
    username = users[0]['username'] if users else ''

    # Build conversation dict keyed by conversation partner username
    conv_dict = {}

    for msg in messages_list:
        if msg['sender_username'] == username:
            other = msg['recipient_username']
        elif msg['recipient_username'] == username:
            other = msg['sender_username']
        else:
            continue

        if other not in conv_dict:
            conv_dict[other] = {
                'conversation_id': None,  # No conversation_id given in spec; use one based on other username hash?
                'with_user': other,
                'last_message': msg['content'],
                'unread_count': 0
            }
        else:
            # Update last_message if this message is newer
            pass  # messages not sorted by timestamp, ignoring sorting for last_message

        # Calculate unread messages count where recipient is current user and is_read false
        if msg['recipient_username'] == username and msg['is_read'].lower() == 'false':
            conv_dict[other]['unread_count'] += 1

    # As no conversation_id field given, assign conversation_id sequentially for display
    conversations = []
    conv_id = 1
    for other, data in conv_dict.items():
        conversations.append({
            'conversation_id': conv_id,
            'with_user': data['with_user'],
            'last_message': data['last_message'],
            'unread_count': data['unread_count']
        })
        conv_id += 1

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    recipient_username = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    users = load_users()
    # Current user sender username (simulate using first user if exists)
    sender_username = users[0]['username'] if users else ''

    messages_list = load_messages()
    max_id = max((m['message_id'] for m in messages_list), default=0)
    new_id = max_id + 1

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    is_read = 'false'

    new_msg = {
        'message_id': new_id,
        'sender_username': sender_username,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': is_read
    }

    messages_list.append(new_msg)
    save_messages(messages_list)

    return redirect(url_for('messages'))


@app.route('/profile')
def user_profile():
    users = load_users()
    username = users[0]['username'] if users else ''
    email = ''
    for u in users:
        if u['username'] == username:
            email = u['email']
            break
    return render_template('profile.html', username=username, email=email)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    new_email = request.form.get('email', '').strip()

    users = load_users()
    # Find first user to update email
    if users:
        users[0]['email'] = new_email

        # Save users back
        filepath = os.path.join(DATA_DIR, 'users.txt')
        with open(filepath, 'w', encoding='utf-8') as f:
            for u in users:
                line = f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}\n"
                f.write(line)

    return redirect(url_for('user_profile'))


@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()

    # Pending applications
    pending_apps = [a for a in applications if a['status'] == 'Pending']

    pet_id_name_map = {p['pet_id']: p['name'] for p in pets}

    pending_applications = []
    for app in pending_apps:
        pending_applications.append({
            'application_id': app['application_id'],
            'pet_name': pet_id_name_map.get(app['pet_id'], 'Unknown'),
            'applicant_name': app['applicant_name'],
            'date_submitted': app['date_submitted']
        })

    all_pets = []
    for p in pets:
        all_pets.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'status': p['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
