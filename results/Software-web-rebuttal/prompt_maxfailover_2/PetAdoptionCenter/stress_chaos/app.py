from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read/write pipe-delimited files

def read_pipe_delimited_file(filepath, expected_fields=None):
    records = []
    if not os.path.exists(filepath):
        return records
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if expected_fields is not None and len(parts) != expected_fields:
                continue
            records.append(parts)
    return records

def write_pipe_delimited_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

# Load pets

def load_pets():
    lines = read_pipe_delimited_file(os.path.join(DATA_DIR, 'pets.txt'), 11)
    pets = []
    for parts in lines:
        try:
            pets.append({
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
            })
        except Exception:
            continue
    return pets

def save_pets(pets):
    lines = []
    for pet in pets:
        line = '|'.join([
            str(pet['pet_id']), pet['name'], pet['species'], pet['breed'], pet['age'],
            pet['gender'], pet['size'], pet['description'], str(pet['shelter_id']),
            pet['status'], pet['date_added']
        ])
        lines.append(line)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'pets.txt'), lines)

# Load activities (optional)
def load_activities():
    filepath = os.path.join(DATA_DIR, 'activities.txt')
    lines = read_pipe_delimited_file(filepath, 3)
    activities = []
    for parts in lines:
        try:
            activities.append({
                'activity_id': int(parts[0]),
                'description': parts[1],
                'date': parts[2]
            })
        except Exception:
            continue
    return activities

# Load applications

def load_applications():
    filepath = os.path.join(DATA_DIR, 'applications.txt')
    lines = read_pipe_delimited_file(filepath, 13)
    applications = []
    for parts in lines:
        try:
            applications.append({
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
            })
        except Exception:
            continue
    return applications

def save_applications(applications):
    lines = []
    for app in applications:
        line = '|'.join([
            str(app['application_id']), app['username'], str(app['pet_id']), app['applicant_name'], app['phone'], app['address'],
            app['housing_type'], app['has_yard'], app['other_pets'], app['experience'], app['reason'], app['status'], app['date_submitted']
        ])
        lines.append(line)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'applications.txt'), lines)

# Load favorites

def load_favorites():
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    lines = read_pipe_delimited_file(filepath, 3)
    favorites = []
    for parts in lines:
        try:
            favorites.append({
                'username': parts[0],
                'pet_id': int(parts[1]),
                'date_added': parts[2]
            })
        except Exception:
            continue
    return favorites

# Load messages

def load_messages():
    filepath = os.path.join(DATA_DIR, 'messages.txt')
    lines = read_pipe_delimited_file(filepath, 7)
    messages = []
    for parts in lines:
        try:
            messages.append({
                'message_id': int(parts[0]),
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6]
            })
        except Exception:
            continue
    return messages

# Load users

def load_users():
    filepath = os.path.join(DATA_DIR, 'users.txt')
    lines = read_pipe_delimited_file(filepath, 4)
    users = []
    for parts in lines:
        try:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
        except Exception:
            continue
    return users

def save_users(users):
    lines = []
    for user in users:
        line = '|'.join([
            user['username'], user['email'], user['phone'], user['address']
        ])
        lines.append(line)
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'users.txt'), lines)

# Load shelters

def load_shelters():
    filepath = os.path.join(DATA_DIR, 'shelters.txt')
    lines = read_pipe_delimited_file(filepath, 5)
    shelters = []
    for parts in lines:
        try:
            shelters.append({
                'shelter_id': int(parts[0]),
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            })
        except Exception:
            continue
    return shelters

# Route: /
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# Route: /dashboard
@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    activities = load_activities()  # Optional
    featured_pets = []
    for pet in pets:
        featured_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age']
        })
    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=activities)

# Route: /pets GET
@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = load_pets()
    filter_species = request.args.get('filter_species', 'All')
    filtered_pets = []
    for pet in pets:
        if filter_species != 'All' and pet['species'] != filter_species:
            continue
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'breed': pet['breed'],
            # photo_url placeholder; not provided in data
        }
        filtered_pets.append(pet_dict)
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species)

# Route: /pets/search POST
@app.route('/pets/search', methods=['POST'])
def pet_search():
    filter_species = request.form.get('filter-species', 'All')
    search_name = request.form.get('search-input', '').lower()
    pets = load_pets()
    filtered_pets = []
    for pet in pets:
        if filter_species != 'All' and pet['species'] != filter_species:
            continue
        if search_name and search_name not in pet['name'].lower():
            continue
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'breed': pet['breed'],
        }
        filtered_pets.append(pet_dict)
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species)

# Route: /pets/<int:pet_id> GET
@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)

# Route: /pets/add GET
@app.route('/pets/add', methods=['GET'])
def add_pet():
    return render_template('add_pet.html')

# Route: /pets/add POST
@app.route('/pets/add', methods=['POST'])
def add_pet_submit():
    form = request.form
    errors = {}
    required_fields = ['name', 'species', 'breed', 'age', 'gender', 'size', 'shelter_id']
    for field in required_fields:
        if not form.get(field):
            errors[field] = f'{field} is required'
    try:
        shelter_id = int(form.get('shelter_id', 0))
    except Exception:
        errors['shelter_id'] = 'shelter_id must be an integer'

    if errors:
        return render_template('add_pet.html', form_errors=errors, form_data=form)

    pets = load_pets()
    new_pet_id = max([p['pet_id'] for p in pets], default=0) + 1
    date_added = form.get('date_added')
    # If no date_added provided, use today
    if not date_added:
        date_added = datetime.date.today().isoformat()

    new_pet = {
        'pet_id': new_pet_id,
        'name': form['name'],
        'species': form['species'],
        'breed': form['breed'],
        'age': form['age'],
        'gender': form['gender'],
        'size': form['size'],
        'description': form.get('description', ''),
        'shelter_id': shelter_id,
        'status': 'Available',
        'date_added': date_added
    }
    pets.append(new_pet)
    save_pets(pets)
    return redirect(url_for('pet_listings'))

# Route: /applications/new/<int:pet_id> GET
@app.route('/applications/new/<int:pet_id>', methods=['GET'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('adoption_application.html', pet=pet, form_errors=None, form_data={})

# Route: /applications/new/<int:pet_id> POST
@app.route('/applications/new/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    form = request.form
    errors = {}
    required_fields = ['username', 'applicant_name', 'phone', 'address', 'housing_type', 'has_yard', 'other_pets', 'experience', 'reason']
    for field in required_fields:
        if not form.get(field):
            errors[field] = 'This field is required'

    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if errors:
        return render_template('adoption_application.html', pet=pet, form_errors=errors, form_data=form)

    applications = load_applications()
    new_app_id = max([app['application_id'] for app in applications], default=0) + 1
    date_submitted = datetime.date.today().isoformat()

    new_app = {
        'application_id': new_app_id,
        'username': form['username'],
        'pet_id': pet_id,
        'applicant_name': form['applicant_name'],
        'phone': form['phone'],
        'address': form['address'],
        'housing_type': form['housing_type'],
        'has_yard': form['has_yard'],
        'other_pets': form['other_pets'],
        'experience': form['experience'],
        'reason': form['reason'],
        'status': 'Pending',
        'date_submitted': date_submitted
    }
    applications.append(new_app)
    save_applications(applications)
    return redirect(url_for('my_applications'))

# Route: /my-applications GET
@app.route('/my-applications', methods=['GET'])
def my_applications():
    username = request.args.get('username', '')
    filter_status = request.args.get('filter_status', 'All')
    applications = load_applications()
    pets = load_pets()
    filtered_apps = []
    for app in applications:
        if username and app['username'] != username:
            continue
        if filter_status != 'All' and app['status'].lower() != filter_status.lower():
            continue
        pet_name = ''
        pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
        if pet:
            pet_name = pet['name']
        filtered_apps.append({
            'application_id': app['application_id'],
            'pet_id': app['pet_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })
    return render_template('my_applications.html', applications=filtered_apps, filter_status=filter_status)

# Route: /favorites GET
@app.route('/favorites', methods=['GET'])
def favorites():
    username = request.args.get('username', '')
    favorites = load_favorites()
    pets = load_pets()
    favorite_pets = []
    for fav in favorites:
        if username and fav['username'] != username:
            continue
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })
    return render_template('favorites.html', favorites=favorite_pets)

# Route: /messages GET
@app.route('/messages', methods=['GET'])
def messages():
    username = request.args.get('username', '')
    messages_all = load_messages()
    conversations = {}
    for msg in messages_all:
        if username not in (msg['sender_username'], msg['recipient_username']):
            continue
        other_user = msg['recipient_username'] if msg['sender_username'] == username else msg['sender_username']
        if other_user not in conversations or conversations[other_user]['timestamp'] < msg['timestamp']:
            conversations[other_user] = {
                'conversation_id': msg['message_id'],
                'other_user': other_user,
                'last_message': msg['content'],
                'timestamp': msg['timestamp']
            }
    sorted_conversations = sorted(conversations.values(), key=lambda c: c['timestamp'], reverse=True)
    return render_template('messages.html', conversations=sorted_conversations)

# Route: /messages/send POST
@app.route('/messages/send', methods=['POST'])
def send_message():
    form = request.form
    errors = {}
    for field in ['sender_username', 'recipient_username', 'subject', 'content']:
        if not form.get(field):
            errors[field] = 'This field is required'
    if errors:
        messages_all = load_messages()
        username = form.get('sender_username', '')
        conversations = {}
        for msg in messages_all:
            if username not in (msg['sender_username'], msg['recipient_username']):
                continue
            other_user = msg['recipient_username'] if msg['sender_username'] == username else msg['sender_username']
            if other_user not in conversations or conversations[other_user]['timestamp'] < msg['timestamp']:
                conversations[other_user] = {
                    'conversation_id': msg['message_id'],
                    'other_user': other_user,
                    'last_message': msg['content'],
                    'timestamp': msg['timestamp']
                }
        sorted_conversations = sorted(conversations.values(), key=lambda c: c['timestamp'], reverse=True)
        return render_template('messages.html', conversations=sorted_conversations, form_errors=errors, form_data=form)

    messages_all = load_messages()
    new_msg_id = max([msg['message_id'] for msg in messages_all], default=0) + 1
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_msg = {
        'message_id': new_msg_id,
        'sender_username': form['sender_username'],
        'recipient_username': form['recipient_username'],
        'subject': form['subject'],
        'content': form['content'],
        'timestamp': timestamp,
        'is_read': 'false'
    }
    messages_all.append(new_msg)
    lines = []
    for msg in messages_all:
        lines.append('|'.join([
            str(msg['message_id']), msg['sender_username'], msg['recipient_username'], msg['subject'], msg['content'], msg['timestamp'], msg['is_read']
        ]))
    write_pipe_delimited_file(os.path.join(DATA_DIR, 'messages.txt'), lines)
    return redirect(url_for('messages'))

# Route: /profile GET
@app.route('/profile', methods=['GET'])
def user_profile():
    username = request.args.get('username', '')
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return render_template('profile.html', username=username, email='')
    return render_template('profile.html', username=username, email=user.get('email', ''))

# Route: /profile/update POST
@app.route('/profile/update', methods=['POST'])
def update_profile():
    form = request.form
    errors = {}
    username = form.get('username', '')
    email = form.get('email', '')
    phone = form.get('phone', '')
    address = form.get('address', '')
    if not username:
        errors['username'] = 'Username is required'
        return render_template('profile.html', form_errors=errors, username=username, email=email)
    users = load_users()
    updated = False
    for i, u in enumerate(users):
        if u['username'] == username:
            users[i] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
            updated = True
            break
    if not updated:
        users.append({
            'username': username,
            'email': email,
            'phone': phone,
            'address': address
        })
    save_users(users)
    return redirect(url_for('dashboard'))

# Route: /admin GET
@app.route('/admin', methods=['GET'])
def admin_panel():
    applications = load_applications()
    pets = load_pets()
    pending_applications = []
    for app in applications:
        if app['status'].lower() == 'pending':
            pet_name = ''
            pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
            if pet:
                pet_name = pet['name']
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_name,
                'status': app['status']
            })
    all_pets = [{'pet_id': p['pet_id'], 'name': p['name'], 'species': p['species'], 'status': p['status']} for p in pets]
    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)

if __name__ == '__main__':
    app.run(debug=True)
