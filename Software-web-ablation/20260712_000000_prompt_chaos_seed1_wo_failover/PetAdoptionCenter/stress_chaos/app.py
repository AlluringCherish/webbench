from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_FOLDER = 'data'

# --- Utility Functions for Data Handling --- #

# Users file structure:
# username|email|phone|address

def load_users():
    users = {}
    path = os.path.join(DATA_FOLDER, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 4:
                    username, email, phone, address = fields
                    users[username] = {
                        'username': username,
                        'email': email,
                        'phone': phone,
                        'address': address
                    }
    return users

def save_users(users):
    path = os.path.join(DATA_FOLDER, 'users.txt')
    lines = []
    for u in users.values():
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Pets file structure:
# pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added

def load_pets():
    pets = {}
    path = os.path.join(DATA_FOLDER, 'pets.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 11:
                    pet_id = int(fields[0])
                    name = fields[1]
                    species = fields[2]
                    breed = fields[3]
                    age = fields[4]
                    gender = fields[5]
                    size = fields[6]
                    description = fields[7]
                    shelter_id = int(fields[8])
                    status = fields[9]
                    date_added = fields[10]
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

def save_pets(pets):
    path = os.path.join(DATA_FOLDER, 'pets.txt')
    lines = []
    for pet_id in sorted(pets.keys()):
        p = pets[pet_id]
        line = '|'.join([
            str(p['pet_id']),
            p['name'],
            p['species'],
            p['breed'],
            p['age'],
            p['gender'],
            p['size'],
            p['description'],
            str(p['shelter_id']),
            p['status'],
            p['date_added']
        ])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Applications file structure:
# application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted

def load_applications():
    applications = {}
    path = os.path.join(DATA_FOLDER, 'applications.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 13:
                    application_id = int(fields[0])
                    username = fields[1]
                    pet_id = int(fields[2])
                    applicant_name = fields[3]
                    phone = fields[4]
                    address = fields[5]
                    housing_type = fields[6]
                    has_yard = fields[7]
                    other_pets = fields[8]
                    experience = fields[9]
                    reason = fields[10]
                    status = fields[11]
                    date_submitted = fields[12]
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

def save_applications(applications):
    path = os.path.join(DATA_FOLDER, 'applications.txt')
    lines = []
    for app_id in sorted(applications.keys()):
        a = applications[app_id]
        line = '|'.join([
            str(a['application_id']),
            a['username'],
            str(a['pet_id']),
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
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Favorites file structure:
# username|pet_id|date_added

def load_favorites():
    favorites = []
    path = os.path.join(DATA_FOLDER, 'favorites.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 3:
                    username = fields[0]
                    pet_id = int(fields[1])
                    date_added = fields[2]
                    favorites.append({
                        'username': username,
                        'pet_id': pet_id,
                        'date_added': date_added
                    })
    return favorites

def save_favorites(favorites):
    path = os.path.join(DATA_FOLDER, 'favorites.txt')
    lines = []
    for fav in favorites:
        line = '|'.join([fav['username'], str(fav['pet_id']), fav['date_added']])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Messages file structure:
# message_id|sender_username|recipient_username|subject|content|timestamp|is_read

def load_messages():
    messages = []
    path = os.path.join(DATA_FOLDER, 'messages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 7:
                    message_id = int(fields[0])
                    sender = fields[1]
                    recipient = fields[2]
                    subject = fields[3]
                    content = fields[4]
                    timestamp = fields[5]
                    is_read = fields[6]
                    messages.append({
                        'message_id': message_id,
                        'sender_username': sender,
                        'recipient_username': recipient,
                        'subject': subject,
                        'content': content,
                        'timestamp': timestamp,
                        'is_read': is_read
                    })
    return messages

def save_messages(messages):
    path = os.path.join(DATA_FOLDER, 'messages.txt')
    lines = []
    for m in messages:
        line = '|'.join([
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            m['is_read']
        ])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

# Adoption history file structure:
# history_id|username|pet_id|pet_name|adoption_date|shelter_id

def load_adoption_history():
    history = []
    path = os.path.join(DATA_FOLDER, 'adoption_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 6:
                    history_id = int(fields[0])
                    username = fields[1]
                    pet_id = int(fields[2])
                    pet_name = fields[3]
                    adoption_date = fields[4]
                    shelter_id = int(fields[5])
                    history.append({
                        'history_id': history_id,
                        'username': username,
                        'pet_id': pet_id,
                        'pet_name': pet_name,
                        'adoption_date': adoption_date,
                        'shelter_id': shelter_id
                    })
    return history

# Shelters file structure:
# shelter_id|name|address|phone|email

def load_shelters():
    shelters = {}
    path = os.path.join(DATA_FOLDER, 'shelters.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) == 5:
                    shelter_id = int(fields[0])
                    name = fields[1]
                    address = fields[2]
                    phone = fields[3]
                    email = fields[4]
                    shelters[shelter_id] = {
                        'shelter_id': shelter_id,
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'email': email
                    }
    return shelters

# --- Session user simulation (basic, assumes username 'john_doe') --- #
# For this implementation, assume the current logged-in user is always 'john_doe'.
CURRENT_USER = 'john_doe'


# --- Flask Route Implementations --- #

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    # featured_pets: list of Dict with keys 'pet_id', 'name', 'species', 'age'
    # Let's pick 3 most recently added available pets for featured pets
    available_pets = [p for p in pets.values() if p['status'].lower() == 'available']
    sorted_pets = sorted(available_pets, key=lambda x: x['date_added'], reverse=True)
    featured_pets = [{'pet_id': p['pet_id'], 'name': p['name'], 'species': p['species'], 'age': p['age']} for p in sorted_pets[:3]]

    # recent_activities could be notes about recent shows; no direct source provided, so simulate with recent application status updates
    applications = load_applications()
    recent_activities = []
    sorted_apps = sorted(applications.values(), key=lambda x: x['date_submitted'], reverse=True)
    for app in sorted_apps[:5]:
        recent_activities.append(f"Application {app['application_id']} for {app['pet_id']} is {app['status']}")

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

@app.route('/pets')
def pet_listings():
    pets = load_pets()
    # Construct pets list for template
    pet_list = []
    for p in pets.values():
        pet_list.append({
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age'],
            'photo_url': f"/static/images/pets/{p['pet_id']}.jpg"  # Assume photos named by pet_id
        })
    species_filter_options = ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']

    return render_template('pet_listings.html', pets=pet_list, species_filter_options=species_filter_options)

@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        return "Pet not found", 404
    # Provide only fields specified
    pet_dict = {
        'pet_id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'breed': pet['breed'],
        'age': pet['age'],
        'gender': pet['gender'],
        'size': pet['size'],
        'description': pet['description'],
        'status': pet['status']
    }
    return render_template('pet_details.html', pet=pet_dict)

@app.route('/add-pet', methods=['GET'])
def add_pet():
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    return render_template('add_pet.html', species_options=species_options)

@app.route('/add-pet', methods=['POST'])
def submit_pet():
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    # Retrieve form data
    name = request.form.get('name', '').strip()
    species = request.form.get('species', '').strip()
    breed = request.form.get('breed', '').strip()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    size = request.form.get('size', '').strip()
    description = request.form.get('description', '').strip()

    # Validate required fields
    if not name or species not in species_options or not breed or not age or gender not in ['Male', 'Female'] or size not in ['Small', 'Medium', 'Large'] or not description:
        return render_template('add_pet.html', species_options=species_options, success=False, error_message='Please fill in all required fields with valid data.')

    pets = load_pets()
    new_id = max(pets.keys(), default=0) + 1
    shelter_id = 1  # Assume default shelter_id as 1, since no user shelter info is given
    date_added = datetime.now().strftime('%Y-%m-%d')
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
    pets[new_id] = new_pet
    save_pets(pets)

    return render_template('add_pet.html', species_options=species_options, success=True)

@app.route('/apply/<int:pet_id>', methods=['GET'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        return "Pet not found", 404
    pet_dict = {
        'pet_id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'breed': pet['breed'],
        'age': pet['age'],
        'gender': pet['gender'],
        'size': pet['size'],
        'description': pet['description'],
        'status': pet['status']
    }
    return render_template('application.html', pet=pet_dict)

@app.route('/apply/<int:pet_id>', methods=['POST'])
def submit_application(pet_id):
    pets = load_pets()
    pet = pets.get(pet_id)
    if not pet:
        return "Pet not found", 404

    # Get form inputs
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_phone = request.form.get('applicant_phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    # Validate required fields
    valid_housing_types = ['House', 'Apartment', 'Condo', 'Other']
    if not applicant_name or not applicant_phone or housing_type not in valid_housing_types or not reason:
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'status': pet['status']
        }
        return render_template('application.html', pet=pet_dict, success=False, error_message='Please fill in all required fields correctly.')

    users = load_users()
    user = users.get(CURRENT_USER)
    if not user:
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'status': pet['status']
        }
        return render_template('application.html', pet=pet_dict, success=False, error_message='User not found.')

    applications = load_applications()
    new_id = max(applications.keys(), default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')

    # Fill default or empty for missing application fields
    has_yard = 'No'
    other_pets = ''
    experience = ''

    application = {
        'application_id': new_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': user['address'],
        'housing_type': housing_type,
        'has_yard': has_yard,
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': today_str
    }
    applications[new_id] = application
    save_applications(applications)

    pet_dict = {
        'pet_id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'breed': pet['breed'],
        'age': pet['age'],
        'gender': pet['gender'],
        'size': pet['size'],
        'description': pet['description'],
        'status': pet['status']
    }
    return render_template('application.html', pet=pet_dict, success=True)

@app.route('/my-applications')
def my_applications():
    applications = load_applications()
    pets = load_pets()
    user_apps = [a for a in applications.values() if a['username'] == CURRENT_USER]

    status_filter_options = ['All', 'Pending', 'Approved', 'Rejected']
    # Get filter from query params
    selected_status = request.args.get('status', 'All')
    if selected_status != 'All':
        user_apps = [a for a in user_apps if a['status'] == selected_status]

    # Format applications with pet name
    apps_list = []
    for a in user_apps:
        pet_name = pets.get(a['pet_id'], {}).get('name', 'Unknown')
        apps_list.append({
            'application_id': a['application_id'],
            'pet_name': pet_name,
            'date': a['date_submitted'],
            'status': a['status']
        })

    return render_template('my_applications.html', applications=apps_list, status_filter_options=status_filter_options)

@app.route('/favorites')
def favorites():
    favorites = load_favorites()
    pets = load_pets()
    # Filter favorites by current user
    user_favs = [f for f in favorites if f['username'] == CURRENT_USER]

    favorite_pets = []
    for fav in user_favs:
        pet = pets.get(fav['pet_id'])
        if pet:
            pet_dict = {
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'breed': pet['breed'],
                'age': pet['age'],
                'gender': pet['gender'],
                'size': pet['size'],
                'description': pet['description'],
                'status': pet['status']
            }
            favorite_pets.append(pet_dict)

    return render_template('favorites.html', favorite_pets=favorite_pets)

@app.route('/messages')
def messages():
    messages = load_messages()
    users = load_users()

    # Group messages by conversation (unique pair of users)
    conversations_map = {}
    for m in messages:
        participants = tuple(sorted([m['sender_username'], m['recipient_username']]))
        if participants not in conversations_map:
            conversations_map[participants] = {
                'conversation_id': hash(participants),
                'participants': list(participants),
                'last_message': m['content'],
                'last_timestamp': m['timestamp']
            }
        else:
            # Update last message if newer timestamp
            if m['timestamp'] > conversations_map[participants]['last_timestamp']:
                conversations_map[participants]['last_message'] = m['content']
                conversations_map[participants]['last_timestamp'] = m['timestamp']

    conversations = list(conversations_map.values())
    # Sort conversations by last_timestamp desc
    conversations.sort(key=lambda c: c['last_timestamp'], reverse=True)

    return render_template('messages.html', conversations=conversations)

@app.route('/messages/send', methods=['POST'])
def send_message():
    sender = CURRENT_USER
    recipient = request.form.get('recipient', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not recipient or not subject or not content:
        conversations = []
        return render_template('messages.html', success=False, error_message='Please fill all fields.')

    messages = load_messages()
    new_id = max([m['message_id'] for m in messages], default=0) + 1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_message = {
        'message_id': new_id,
        'sender_username': sender,
        'recipient_username': recipient,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': 'false'
    }
    messages.append(new_message)
    save_messages(messages)

    conversations_map = {}
    for m in messages:
        participants = tuple(sorted([m['sender_username'], m['recipient_username']]))
        if participants not in conversations_map:
            conversations_map[participants] = {
                'conversation_id': hash(participants),
                'participants': list(participants),
                'last_message': m['content'],
                'last_timestamp': m['timestamp']
            }
        else:
            if m['timestamp'] > conversations_map[participants]['last_timestamp']:
                conversations_map[participants]['last_message'] = m['content']
                conversations_map[participants]['last_timestamp'] = m['timestamp']
    conversations = list(conversations_map.values())
    conversations.sort(key=lambda c: c['last_timestamp'], reverse=True)

    return render_template('messages.html', success=True, conversations=conversations)

@app.route('/profile', methods=['GET'])
def user_profile():
    users = load_users()
    user = users.get(CURRENT_USER)
    if not user:
        return "User not found", 404
    username = user['username']
    email = user['email']
    return render_template('profile.html', username=username, email=email)

@app.route('/profile', methods=['POST'])
def update_profile():
    users = load_users()
    user = users.get(CURRENT_USER)
    if not user:
        return "User not found", 404

    email = request.form.get('email', '').strip()

    if not email:
        return render_template('profile.html', username=user['username'], email=user['email'], success=False, error_message='Email cannot be empty.')

    user['email'] = email
    users[CURRENT_USER] = user
    save_users(users)

    return render_template('profile.html', username=user['username'], email=user['email'], success=True)

@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()
    users = load_users()

    pending_applications = []
    for app in applications.values():
        if app['status'] == 'Pending':
            pet_name = pets.get(app['pet_id'], {}).get('name', 'Unknown')
            applicant_name = app['applicant_name']
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': applicant_name,
                'pet_name': pet_name,
                'date': app['date_submitted'],
                'status': app['status']
            })

    all_pets = []
    for pet in pets.values():
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'status': pet['status']
        }
        all_pets.append(pet_dict)

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
