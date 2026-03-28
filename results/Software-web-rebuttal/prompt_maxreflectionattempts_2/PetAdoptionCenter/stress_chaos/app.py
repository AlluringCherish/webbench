from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
PETS_FILE = os.path.join(DATA_DIR, 'pets.txt')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.txt')
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.txt')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.txt')
ADOPTION_HISTORY_FILE = os.path.join(DATA_DIR, 'adoption_history.txt')
SHELTERS_FILE = os.path.join(DATA_DIR, 'shelters.txt')

# Helper functions to load data from files

def load_users():
    users = []
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            try:
                users.append({
                    'username': parts[0],
                    'email': parts[1],
                    'phone': parts[2],
                    'address': parts[3]
                })
            except:
                pass
    return users


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        for user in users:
            f.write(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}\n")


def load_pets():
    pets = []
    if not os.path.exists(PETS_FILE):
        return pets
    with open(PETS_FILE, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) != 11:
                continue
            try:
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
            except:
                continue
    return pets


def save_pet(pet):
    line = f"{pet['pet_id']}|{pet['name']}|{pet['species']}|{pet['breed']}|{pet['age']}|{pet['gender']}|{pet['size']}|{pet['description']}|{pet['shelter_id']}|{pet['status']}|{pet['date_added']}\n"
    with open(PETS_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def load_applications():
    applications = []
    if not os.path.exists(APPLICATIONS_FILE):
        return applications
    with open(APPLICATIONS_FILE, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) != 13:
                continue
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
            except:
                continue
    return applications


def save_application(application):
    line = f"{application['application_id']}|{application['username']}|{application['pet_id']}|{application['applicant_name']}|{application['phone']}|{application['address']}|{application['housing_type']}|{application['has_yard']}|{application['other_pets']}|{application['experience']}|{application['reason']}|{application['status']}|{application['date_submitted']}\n"
    with open(APPLICATIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def load_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    with open(FAVORITES_FILE, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            try:
                favorites.append({
                    'username': parts[0],
                    'pet_id': int(parts[1]),
                    'date_added': parts[2]
                })
            except:
                continue
    return favorites


def load_messages():
    messages = []
    if not os.path.exists(MESSAGES_FILE):
        return messages
    with open(MESSAGES_FILE, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            try:
                messages.append({
                    'message_id': int(parts[0]),
                    'sender_username': parts[1],
                    'recipient_username': parts[2],
                    'subject': parts[3],
                    'content': parts[4],
                    'timestamp': parts[5],
                    'is_read': parts[6].lower() == 'true'
                })
            except:
                continue
    return messages


def save_message(message):
    line = f"{message['message_id']}|{message['sender_username']}|{message['recipient_username']}|{message['subject']}|{message['content']}|{message['timestamp']}|{message['is_read']}\n"
    with open(MESSAGES_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def find_pet_by_id(pet_id):
    pets = load_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None


def find_user_by_username(username):
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
    pets = [pet for pet in load_pets() if pet['status'] == 'Available']
    pets.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = pets[:5]
    recent_activities = ["Application submitted for pet 1", "Pet 2 adopted"]
    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)


@app.route('/pets')
def pet_listings():
    pets = load_pets()
    filter_species = request.args.get('filter_species', 'All')
    search_name = request.args.get('search_name', '')
    filtered_pets = pets
    if filter_species != 'All':
        filtered_pets = [p for p in filtered_pets if p['species'].lower() == filter_species.lower()]
    if search_name:
        filtered_pets = [p for p in filtered_pets if search_name.lower() in p['name'].lower()]
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species, search_name=search_name)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pet = find_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))
    return render_template('pet_details.html', pet=pet)


@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet_page():
    if request.method == 'POST':
        pet_name = request.form.get('pet_name', '').strip()
        pet_species = request.form.get('pet_species', '').strip()
        pet_breed = request.form.get('pet_breed', '').strip()
        pet_age = request.form.get('pet_age', '').strip()
        pet_gender = request.form.get('pet_gender', '').strip()
        pet_size = request.form.get('pet_size', '').strip()
        pet_description = request.form.get('pet_description', '').strip()

        if not (pet_name and pet_species and pet_breed):
            flash('Pet name, species, and breed are required.', 'error')
            return render_template('add_pet.html')

        pets = load_pets()
        pet_id = max([p['pet_id'] for p in pets], default=0) + 1

        new_pet = {
            'pet_id': pet_id,
            'name': pet_name,
            'species': pet_species,
            'breed': pet_breed,
            'age': pet_age,
            'gender': pet_gender,
            'size': pet_size,
            'description': pet_description,
            'shelter_id': 1,
            'status': 'Available',
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }

        save_pet(new_pet)

        return redirect(url_for('dashboard'))
    else:
        return render_template('add_pet.html')


@app.route('/apply/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pet = find_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found.', 'error')
        return redirect(url_for('pet_listings'))

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_phone = request.form.get('applicant_phone', '').strip()
        housing_type = request.form.get('housing_type', '').strip()
        reason = request.form.get('reason', '').strip()

        if not applicant_name or not applicant_phone or not housing_type or not reason:
            flash('All fields are required.', 'error')
            return render_template('application.html', pet=pet)

        applications = load_applications()
        application_id = max([a['application_id'] for a in applications], default=0) + 1

        # For this simplified design, other fields like username, has_yard, other_pets, experience
        # are left empty or default.
        new_application = {
            'application_id': application_id,
            'username': '',  # no username from form
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': '',
            'housing_type': housing_type,
            'has_yard': '',
            'other_pets': '',
            'experience': '',
            'reason': reason,
            'status': 'Pending',
            'date_submitted': datetime.now().strftime('%Y-%m-%d')
        }

        save_application(new_application)

        return redirect(url_for('my_applications'))

    else:
        return render_template('application.html', pet=pet)


@app.route('/my-applications')
def my_applications():
    filter_status = request.args.get('filter_status', 'All')
    applications = load_applications()
    pets = load_pets()
    pet_map = {p['pet_id']: p for p in pets}

    filtered_apps = []
    for app in applications:
        if filter_status == 'All' or app['status'] == filter_status:
            pet_name = pet_map.get(app['pet_id'], {}).get('name', 'Unknown')
            filtered_apps.append({
                'application_id': app['application_id'],
                'pet_name': pet_name,
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })

    return render_template('my_applications.html', applications=filtered_apps, filter_status=filter_status)


@app.route('/favorites')
def favorites():
    username = request.args.get('username', '')
    favorites = load_favorites()
    pets = load_pets()
    pet_map = {p['pet_id']: p for p in pets}

    user_favorites = [fav for fav in favorites if fav['username'] == username]
    favorite_pets = [pet_map[fav['pet_id']] for fav in user_favorites if fav['pet_id'] in pet_map]

    return render_template('favorites.html', favorites=favorite_pets)


@app.route('/messages')
def messages():
    username = request.args.get('username', '')
    messages = load_messages()

    conversations = {}
    for msg in messages:
        if username in (msg['sender_username'], msg['recipient_username']):
            participant = msg['recipient_username'] if msg['sender_username'] == username else msg['sender_username']
            conv = conversations.get(participant, {
                'conversation_id': len(conversations)+1,
                'participant_username': participant,
                'last_message_summary': '',
                'unread_count': 0
            })
            conv['last_message_summary'] = msg['content']
            if not msg['is_read'] and msg['recipient_username'] == username:
                conv['unread_count'] += 1
            conversations[participant] = conv

    conv_list = list(conversations.values())
    return render_template('messages.html', conversations=conv_list)


@app.route('/messages/send', methods=['POST'])
def send_message():
    recipient_username = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not recipient_username or not subject or not content:
        flash('All fields are required for sending message.', 'error')
        return redirect(url_for('messages'))

    messages = load_messages()
    message_id = max([m['message_id'] for m in messages], default=0) + 1
    sender_username = 'current_user'  # In real app would be from session/login
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_message = {
        'message_id': message_id,
        'sender_username': sender_username,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': 'false'
    }

    save_message(new_message)

    return redirect(url_for('messages'))


@app.route('/profile')
def user_profile():
    username = request.args.get('username', '')
    user = find_user_by_username(username)
    if not user:
        user = {'username': username, 'email': '', 'phone': '', 'address': ''}
    return render_template('profile.html', user_profile=user)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    username = request.form.get('username', '').strip()

    if not username:
        flash('Username required.', 'error')
        return redirect(url_for('user_profile', username=username))

    users = load_users()
    found = False
    for user in users:
        if user['username'] == username:
            user['email'] = email
            user['phone'] = phone
            user['address'] = address
            found = True
            break
    if not found:
        users.append({'username': username, 'email': email, 'phone': phone, 'address': address})
    try:
        save_users(users)
        flash('Profile updated successfully.', 'success')
    except Exception:
        flash('Failed to save profiles.', 'error')
    return redirect(url_for('user_profile', username=username))


@app.route('/admin-panel')
def admin_panel():
    applications = load_applications()
    pets = load_pets()
    pet_map = {p['pet_id']: p for p in pets}

    pending_applications = []
    for app in applications:
        if app['status'].lower() == 'pending':
            pet = pet_map.get(app['pet_id'], {})
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet.get('name', 'Unknown'),
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })

    all_pets = []
    for pet in pets:
        all_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
