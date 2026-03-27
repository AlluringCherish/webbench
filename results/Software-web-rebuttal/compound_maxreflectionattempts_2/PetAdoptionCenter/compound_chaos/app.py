from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Current user (for simplification; in real app use sessions/auth)
CURRENT_USER = 'john_doe'


# Utility functions

def read_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def write_lines(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in lines)


# -------------------- USERS --------------------

# Schema: username|email|phone|address

def load_users():
    users = {}
    for line in read_lines('users.txt'):
        parts = line.split('|')
        if len(parts) != 4:
            continue
        username, email, phone, address = parts
        users[username] = {
            'username': username,
            'email': email,
            'phone': phone,
            'address': address
        }
    return users


def save_users(users):
    lines = []
    for user in users.values():
        line = '|'.join([user['username'], user['email'], user['phone'], user['address']])
        lines.append(line)
    write_lines('users.txt', lines)


# -------------------- PETS --------------------

# Schema: pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added

def load_pets():
    pets = {}
    for line in read_lines('pets.txt'):
        parts = line.split('|')
        if len(parts) != 11:
            continue
        pet_id_str, name, species, breed, age, gender, size, description, shelter_id_str, status, date_added = parts
        try:
            pet_id = int(pet_id_str)
            shelter_id = int(shelter_id_str)
        except ValueError:
            continue
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
    lines = []
    for pet in pets.values():
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
    write_lines('pets.txt', lines)


# -------------------- APPLICATIONS --------------------

# Schema: application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted

def load_applications():
    applications = {}
    for line in read_lines('applications.txt'):
        parts = line.split('|')
        if len(parts) != 13:
            continue
        application_id_str, username, pet_id_str, applicant_name, phone, address, housing_type, has_yard, other_pets, experience, reason, status, date_submitted = parts
        try:
            application_id = int(application_id_str)
            pet_id = int(pet_id_str)
        except ValueError:
            continue
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
    lines = []
    for app in applications.values():
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
    write_lines('applications.txt', lines)


# -------------------- FAVORITES --------------------

# Schema: username|pet_id|date_added

def load_favorites():
    favorites = []
    for line in read_lines('favorites.txt'):
        parts = line.split('|')
        if len(parts) != 3:
            continue
        username, pet_id_str, date_added = parts
        try:
            pet_id = int(pet_id_str)
        except ValueError:
            continue
        favorites.append({
            'username': username,
            'pet_id': pet_id,
            'date_added': date_added
        })
    return favorites


def save_favorites(favorites):
    lines = []
    for fav in favorites:
        line = '|'.join([fav['username'], str(fav['pet_id']), fav['date_added']])
        lines.append(line)
    write_lines('favorites.txt', lines)


# -------------------- MESSAGES --------------------

# Schema: message_id|sender_username|recipient_username|subject|content|timestamp|is_read

def load_messages():
    messages = {}
    for line in read_lines('messages.txt'):
        parts = line.split('|')
        if len(parts) != 7:
            continue
        message_id_str, sender_username, recipient_username, subject, content, timestamp, is_read_str = parts
        try:
            message_id = int(message_id_str)
        except ValueError:
            continue
        is_read = True if is_read_str.lower() == 'true' else False
        messages[message_id] = {
            'message_id': message_id,
            'sender_username': sender_username,
            'recipient_username': recipient_username,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': is_read
        }
    return messages


def save_messages(messages):
    lines = []
    for msg in messages.values():
        line = '|'.join([
            str(msg['message_id']),
            msg['sender_username'],
            msg['recipient_username'],
            msg['subject'],
            msg['content'],
            msg['timestamp'],
            'true' if msg['is_read'] else 'false'
        ])
        lines.append(line)
    write_lines('messages.txt', lines)

# -------------------- ADOPTION HISTORY --------------------

# Schema: history_id|username|pet_id|pet_name|adoption_date|shelter_id

def load_adoption_history():
    history = {}
    for line in read_lines('adoption_history.txt'):
        parts = line.split('|')
        if len(parts) != 6:
            continue
        history_id_str, username, pet_id_str, pet_name, adoption_date, shelter_id_str = parts
        try:
            history_id = int(history_id_str)
            pet_id = int(pet_id_str)
            shelter_id = int(shelter_id_str)
        except ValueError:
            continue
        history[history_id] = {
            'history_id': history_id,
            'username': username,
            'pet_id': pet_id,
            'pet_name': pet_name,
            'adoption_date': adoption_date,
            'shelter_id': shelter_id
        }
    return history


def save_adoption_history(history):
    lines = []
    for h in history.values():
        line = '|'.join([
            str(h['history_id']),
            h['username'],
            str(h['pet_id']),
            h['pet_name'],
            h['adoption_date'],
            str(h['shelter_id'])
        ])
        lines.append(line)
    write_lines('adoption_history.txt', lines)


# -------------------- SHELTERS --------------------

# Schema: shelter_id|name|address|phone|email

def load_shelters():
    shelters = {}
    for line in read_lines('shelters.txt'):
        parts = line.split('|')
        if len(parts) != 5:
            continue
        shelter_id_str, name, address, phone, email = parts
        try:
            shelter_id = int(shelter_id_str)
        except ValueError:
            continue
        shelters[shelter_id] = {
            'shelter_id': shelter_id,
            'name': name,
            'address': address,
            'phone': phone,
            'email': email
        }
    return shelters


# ---------- Helpers for current user ----------

users = load_users()
pets = load_pets()
applications = load_applications()
favorites = load_favorites()
messages = load_messages()
adoption_history = load_adoption_history()
shelters = load_shelters()

# Helper to get user dict

def get_current_user():
    return users.get(CURRENT_USER, {
        'username': CURRENT_USER,
        'email': '',
        'phone': '',
        'address': ''
    })


# ----------- Routes Implementation -----------

@app.route('/')
def home_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Show featured pets - choose pets with status Available, sorted by date_added descending
    available_pets = [pet for pet in pets.values() if pet['status'].lower() == 'available']
    # Sort by date_added descending
    # Date format assumed YYYY-MM-DD
    def date_key(pet):
        try:
            return datetime.strptime(pet['date_added'], '%Y-%m-%d')
        except Exception:
            return datetime.min

    sorted_pets = sorted(available_pets, key=date_key, reverse=True)
    featured_pets = []
    for pet in sorted_pets[:5]:
        pet_info = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': None  # No photo_url in data schema, so leave None
        }
        featured_pets.append(pet_info)
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets', methods=['GET', 'POST'])
def pet_listings():
    filter_species = ''
    search_query = ''
    filtered_pets = list(pets.values())

    if request.method == 'POST':
        filter_species = request.form.get('filter_species', '').strip()
        search_query = request.form.get('search_query', '').strip().lower()
    else:
        filter_species = request.args.get('filter_species', '').strip()
        search_query = request.args.get('search_query', '').strip().lower()

    if filter_species:
        filtered_pets = [pet for pet in filtered_pets if pet['species'].lower() == filter_species.lower()]

    if search_query:
        filtered_pets = [pet for pet in filtered_pets if search_query in pet['name'].lower()]

    pets_list = []
    for pet in filtered_pets:
        pet_info = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': None  # No photo_url in schema
        }
        pets_list.append(pet_info)

    return render_template('pet_listings.html', pets=pets_list, filter_species=filter_species, search_query=search_query)


@app.route('/pet/<int:pet_id>')
def pet_details(pet_id):
    pet = pets.get(pet_id)
    if not pet:
        return "Pet not found", 404

    # Check if current user has this pet as favorite
    is_favorite = any(fav['username'] == CURRENT_USER and fav['pet_id'] == pet_id for fav in favorites)

    return render_template('pet_details.html', pet=pet, is_favorite=is_favorite)


@app.route('/pet/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'GET':
        return render_template('add_pet.html')

    # POST: add new pet
    # Fields from form:
    # name, species, breed, age, gender, size, description
    form = request.form
    name = form.get('pet-name-input', '').strip()
    species = form.get('pet-species-input', '').strip()
    breed = form.get('pet-breed-input', '').strip()
    age = form.get('pet-age-input', '').strip()
    gender = form.get('pet-gender-input', '').strip()
    size = form.get('pet-size-input', '').strip()
    description = form.get('pet-description-input', '').strip()

    if not name or not species or not breed or not age or not gender or not size or not description:
        # Missing required fields - ideally flash message, here just reload
        return render_template('add_pet.html')

    # Generate new pet_id
    new_pet_id = max(pets.keys(), default=0) + 1

    # For shelter_id, assign 1 by default (Happy Paws Shelter) as no form input for shelter
    shelter_id = 1

    # status default Available
    status = 'Available'

    # date_added current date
    date_added = datetime.now().strftime('%Y-%m-%d')

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
        'status': status,
        'date_added': date_added
    }

    pets[new_pet_id] = new_pet
    save_pets(pets)

    return redirect(url_for('pet_details', pet_id=new_pet_id))


@app.route('/application/new/<int:pet_id>', methods=['GET', 'POST'])
def new_application(pet_id):
    pet = pets.get(pet_id)
    if not pet:
        return "Pet not found", 404

    if request.method == 'GET':
        return render_template('application.html', pet=pet)

    # POST: submit application
    form = request.form
    applicant_name = form.get('applicant-name', '').strip()
    phone = form.get('applicant-phone', '').strip()
    housing_type = form.get('housing-type', '').strip()
    reason = form.get('reason', '').strip()

    if not applicant_name or not phone or not housing_type or not reason:
        return render_template('application.html', pet=pet)

    user_info = get_current_user()

    # For fields not included in form, fill defaults
    address = user_info.get('address', '')
    has_yard = 'No'
    other_pets = 'None'
    experience = 'First time adopter'

    # Generate new application_id
    new_app_id = max(applications.keys(), default=0) + 1

    new_application = {
        'application_id': new_app_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': has_yard,
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }

    applications[new_app_id] = new_application
    save_applications(applications)

    return redirect(url_for('my_applications'))


@app.route('/applications')
def my_applications():
    filter_status = request.args.get('filter_status', '').strip()
    user_apps = [app for app in applications.values() if app['username'] == CURRENT_USER]

    if filter_status:
        user_apps = [app for app in user_apps if app['status'].lower() == filter_status.lower()]

    # For each application, include pet_name from pets
    apps_list = []
    for app in user_apps:
        pet_name = pets.get(app['pet_id'], {}).get('name', 'Unknown')
        apps_list.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=apps_list, filter_status=filter_status)


@app.route('/favorites')
def favorites():
    # Get favorite pet_ids for current user
    fav_pet_ids = [fav['pet_id'] for fav in favorites if fav['username'] == CURRENT_USER]
    fav_pets = []
    for pet_id in fav_pet_ids:
        pet = pets.get(pet_id)
        if pet:
            fav_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': None
            })
    return render_template('favorites.html', favorite_pets=fav_pets)


@app.route('/messages', methods=['GET', 'POST'])
def messages_view():
    # Messages involving current user as sender or recipient
    user_msgs = [msg for msg in messages.values() if msg['sender_username'] == CURRENT_USER or msg['recipient_username'] == CURRENT_USER]
    # Sort by timestamp ascending for conversation list display
    def msg_time_key(m):
        try:
            return datetime.strptime(m['timestamp'], '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min
    user_msgs_sorted = sorted(user_msgs, key=msg_time_key)

    if request.method == 'POST':
        # Get message input fields
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message_input', '').strip()
        recipient_username = request.form.get('recipient_username', '').strip()

        if subject and content and recipient_username:
            new_msg_id = max(messages.keys(), default=0) + 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_message = {
                'message_id': new_msg_id,
                'sender_username': CURRENT_USER,
                'recipient_username': recipient_username,
                'subject': subject,
                'content': content,
                'timestamp': timestamp,
                'is_read': False
            }
            messages[new_msg_id] = new_message
            save_messages(messages)
            return redirect(url_for('messages_view'))
        # If missing fields, show messages again with no error

    return render_template('messages.html', messages=user_msgs_sorted)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if request.method == 'GET':
        return render_template('profile.html', user=user)

    # POST: update profile
    email = request.form.get('profile-email', '').strip()
    if email:
        # update users
        users[CURRENT_USER]['email'] = email
        # Optionally update phone and address if included
        phone = request.form.get('profile-phone', '').strip()
        address = request.form.get('profile-address', '').strip()
        if phone:
            users[CURRENT_USER]['phone'] = phone
        if address:
            users[CURRENT_USER]['address'] = address
        save_users(users)

    user_updated = users.get(CURRENT_USER, user)
    return render_template('profile.html', user=user_updated)


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # Pending applications
    pending_applications = [app for app in applications.values() if app['status'].lower() == 'pending']

    # All pets
    all_pets_list = []
    for pet in pets.values():
        all_pets_list.append(pet)

    if request.method == 'POST':
        # For simplicity: Let's assume admin can approve or reject applications via form inputs
        action = request.form.get('action')
        app_id_str = request.form.get('application_id')
        if action and app_id_str:
            try:
                app_id = int(app_id_str)
                if app_id in applications:
                    if action.lower() == 'approve':
                        applications[app_id]['status'] = 'Approved'
                    elif action.lower() == 'reject':
                        applications[app_id]['status'] = 'Rejected'
                    save_applications(applications)
            except Exception:
                pass
        return redirect(url_for('admin_panel'))

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets_list)


if __name__ == '__main__':
    app.run(debug=True)
