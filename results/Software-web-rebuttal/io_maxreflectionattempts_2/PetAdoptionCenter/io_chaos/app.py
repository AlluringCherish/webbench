from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# --- Utility functions for reading/writing each data file with strict schema adherence ---

def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
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
            line = '|'.join([
                u.get('username', ''),
                u.get('email', ''),
                u.get('phone', ''),
                u.get('address', '')
            ])
            f.write(line + '\n')


def read_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
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
                except ValueError:
                    continue
    return pets

def write_pets(pets):
    path = os.path.join(DATA_DIR, 'pets.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for p in pets:
            line = '|'.join([
                str(p.get('pet_id', '')),
                p.get('name', ''),
                p.get('species', ''),
                p.get('breed', ''),
                p.get('age', ''),
                p.get('gender', ''),
                p.get('size', ''),
                p.get('description', ''),
                str(p.get('shelter_id', '')),
                p.get('status', ''),
                p.get('date_added', '')
            ])
            f.write(line + '\n')


def read_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
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
                except ValueError:
                    continue
    return applications

def write_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
            line = '|'.join([
                str(a.get('application_id', '')),
                a.get('username', ''),
                str(a.get('pet_id', '')),
                a.get('applicant_name', ''),
                a.get('phone', ''),
                a.get('address', ''),
                a.get('housing_type', ''),
                a.get('has_yard', ''),
                a.get('other_pets', ''),
                a.get('experience', ''),
                a.get('reason', ''),
                a.get('status', ''),
                a.get('date_submitted', '')
            ])
            f.write(line + '\n')


def read_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                try:
                    favorites.append({
                        'username': parts[0],
                        'pet_id': int(parts[1]),
                        'date_added': parts[2]
                    })
                except ValueError:
                    continue
    return favorites

def write_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav.get('username', ''),
                str(fav.get('pet_id', '')),
                fav.get('date_added', '')
            ])
            f.write(line + '\n')


def read_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
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
                        'is_read': parts[6]
                    })
                except ValueError:
                    continue
    return messages

def write_messages(messages):
    path = os.path.join(DATA_DIR, 'messages.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for msg in messages:
            line = '|'.join([
                str(msg.get('message_id', '')),
                msg.get('sender_username', ''),
                msg.get('recipient_username', ''),
                msg.get('subject', ''),
                msg.get('content', ''),
                msg.get('timestamp', ''),
                msg.get('is_read', '')
            ])
            f.write(line + '\n')


def read_adoption_history():
    history = []
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
                    history.append({
                        'history_id': int(parts[0]),
                        'username': parts[1],
                        'pet_id': int(parts[2]),
                        'pet_name': parts[3],
                        'adoption_date': parts[4],
                        'shelter_id': int(parts[5])
                    })
                except ValueError:
                    continue
    return history

def write_adoption_history(history):
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for rec in history:
            line = '|'.join([
                str(rec.get('history_id', '')),
                rec.get('username', ''),
                str(rec.get('pet_id', '')),
                rec.get('pet_name', ''),
                rec.get('adoption_date', ''),
                str(rec.get('shelter_id', ''))
            ])
            f.write(line + '\n')


def read_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    shelters.append({
                        'shelter_id': int(parts[0]),
                        'name': parts[1],
                        'address': parts[2],
                        'phone': parts[3],
                        'email': parts[4]
                    })
                except ValueError:
                    continue
    return shelters


def get_user_by_username(username):
    for user in read_users():
        if user['username'] == username:
            return user
    return None

def get_pet_by_id(pet_id):
    for pet in read_pets():
        if pet['pet_id'] == pet_id:
            return pet
    return None


# Assume the currently logged in user is:
CURRENT_USER = 'john_doe'


# --- ROUTES ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    pets = read_pets()
    featured_pets = []
    for pet in pets:
        if pet['status'] == 'Available':
            featured_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
            })
            if len(featured_pets) >= 5:
                break
    return render_template('dashboard.html', featured_pets=featured_pets)

@app.route('/pets')
def pet_listings_page():
    pets = read_pets()
    pets_list = []
    for pet in pets:
        pets_list.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
        })
    return render_template('pet_listings.html', pets=pets_list)

@app.route('/search_pets', methods=['POST'])
def search_pets():
    pets = read_pets()
    search_name = request.form.get('search_name', '').strip().lower()
    filter_species = request.form.get('filter_species', '').strip()

    filtered_pets = []
    for pet in pets:
        if pet['status'] not in ['Available', 'Pending']:
            continue
        matched_name = True
        if search_name:
            matched_name = search_name in pet['name'].lower()
        matched_species = True
        if filter_species and filter_species != 'All':
            matched_species = pet['species'] == filter_species
        if matched_name and matched_species:
            filtered_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
            })
    return render_template('pet_listings.html', pets=filtered_pets)

@app.route('/pets/<int:pet_id>')
def pet_details_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)

@app.route('/add_pet')
def add_pet_page():
    return render_template('add_pet.html', pet=None,
                           species_options=['Dog', 'Cat', 'Bird', 'Rabbit', 'Other'],
                           gender_options=['Male', 'Female'],
                           size_options=['Small', 'Medium', 'Large'])

@app.route('/submit_pet', methods=['POST'])
def submit_pet():
    pets = read_pets()
    form = request.form

    pet_id_str = form.get('pet_id', '').strip()
    is_edit = False
    pet_index = None
    if pet_id_str.isdigit():
        pet_id = int(pet_id_str)
        for i, pet in enumerate(pets):
            if pet['pet_id'] == pet_id:
                is_edit = True
                pet_index = i
                break
    else:
        pet_id = None

    name = form.get('pet_name_input', '').strip()
    species = form.get('pet_species_input', '').strip()
    breed = form.get('pet_breed_input', '').strip()
    age = form.get('pet_age_input', '').strip()
    gender = form.get('pet_gender_input', '').strip()
    size = form.get('pet_size_input', '').strip()
    description = form.get('pet_description_input', '').strip()

    if not name or not species:
        return redirect(url_for('add_pet_page'))

    if is_edit:
        pets[pet_index]['name'] = name
        pets[pet_index]['species'] = species
        pets[pet_index]['breed'] = breed
        pets[pet_index]['age'] = age
        pets[pet_index]['gender'] = gender
        pets[pet_index]['size'] = size
        pets[pet_index]['description'] = description
    else:
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
            'shelter_id': 1,
            'status': 'Available',
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
        pets.append(new_pet)

    write_pets(pets)
    return redirect(url_for('pet_listings_page'))

@app.route('/apply_adoption/<int:pet_id>')
def adoption_application_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    pet_brief = {'pet_id': pet['pet_id'], 'name': pet['name']}
    return render_template('adoption_application.html', pet=pet_brief, housing_type_options=['House', 'Apartment', 'Condo', 'Other'])

@app.route('/submit_application/<int:pet_id>', methods=['POST'])
def submit_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    user = get_user_by_username(CURRENT_USER)

    form = request.form
    applicant_name = form.get('applicant_name', '').strip()
    phone = form.get('applicant_phone', '').strip()
    housing_type = form.get('housing_type', '').strip()
    reason = form.get('reason', '').strip()

    if not applicant_name or not phone or not housing_type or not reason:
        return redirect(url_for('adoption_application_page', pet_id=pet_id))

    address = user.get('address', '') if user else ''

    applications = read_applications()
    max_id = max((a['application_id'] for a in applications), default=0)
    new_app_id = max_id + 1

    new_application = {
        'application_id': new_app_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': address,
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
    return redirect(url_for('my_applications_page'))

@app.route('/my_applications')
def my_applications_page():
    applications = read_applications()
    pets = read_pets()
    pet_map = {p['pet_id']: p['name'] for p in pets}
    user_apps = []
    for app in applications:
        if app['username'] == CURRENT_USER:
            user_apps.append({
                'application_id': app['application_id'],
                'pet_name': pet_map.get(app['pet_id'], 'Unknown'),
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })
    return render_template('my_applications.html', applications=user_apps)

@app.route('/filter_applications', methods=['POST'])
def filter_applications():
    filter_status = request.form.get('filter_status', '').strip()
    applications = read_applications()
    pets = read_pets()
    pet_map = {p['pet_id']: p['name'] for p in pets}

    filtered_apps = []
    for app in applications:
        if app['username'] == CURRENT_USER:
            if filter_status in ['', 'All'] or app['status'] == filter_status:
                filtered_apps.append({
                    'application_id': app['application_id'],
                    'pet_name': pet_map.get(app['pet_id'], 'Unknown'),
                    'date_submitted': app['date_submitted'],
                    'status': app['status']
                })
    return render_template('my_applications.html', applications=filtered_apps)

@app.route('/favorites')
def favorites_page():
    favorites = read_favorites()
    user_favs = []
    for fav in favorites:
        if fav['username'] == CURRENT_USER:
            pet = get_pet_by_id(fav['pet_id'])
            if pet:
                user_favs.append({
                    'pet_id': pet['pet_id'],
                    'name': pet['name'],
                    'species': pet['species'],
                    'age': pet['age'],
                    'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
                })
    return render_template('favorites.html', favorites=user_favs)

@app.route('/messages')
def messages_page():
    messages = read_messages()
    conversations = {}
    for msg in messages:
        if msg['sender_username'] == CURRENT_USER:
            other_user = msg['recipient_username']
        elif msg['recipient_username'] == CURRENT_USER:
            other_user = msg['sender_username']
        else:
            continue

        if other_user not in conversations:
            conversations[other_user] = {
                'conversation_id': abs(hash(other_user)) % 100000000,
                'other_party_username': other_user,
                'last_message_preview': '',
                'last_message_timestamp': ''
            }

        last_ts = conversations[other_user]['last_message_timestamp']
        if not last_ts or msg['timestamp'] > last_ts:
            preview = msg['content'][:50] + ('...' if len(msg['content']) > 50 else '')
            conversations[other_user]['last_message_preview'] = preview
            conversations[other_user]['last_message_timestamp'] = msg['timestamp']

    sorted_conversations = sorted(conversations.values(), key=lambda c: c['last_message_timestamp'], reverse=True)

    return render_template('messages.html', conversations=sorted_conversations)

@app.route('/send_message', methods=['POST'])
def send_message():
    messages = read_messages()
    recipient = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()
    if not recipient or not subject or not content:
        return redirect(url_for('messages_page'))
    max_id = max((m['message_id'] for m in messages), default=0)
    new_id = max_id + 1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_message = {
        'message_id': new_id,
        'sender_username': CURRENT_USER,
        'recipient_username': recipient,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': 'false'
    }
    messages.append(new_message)
    write_messages(messages)
    return redirect(url_for('messages_page'))

@app.route('/profile')
def user_profile_page():
    user = get_user_by_username(CURRENT_USER)
    if not user:
        user = {
            'username': CURRENT_USER,
            'email': '',
            'phone': '',
            'address': ''
        }
    user_info = {
        'username': user.get('username', ''),
        'email': user.get('email', '')
    }
    return render_template('profile.html', user_info=user_info)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    users = read_users()
    email = request.form.get('email', '').strip()
    updated = False
    for user in users:
        if user['username'] == CURRENT_USER:
            user['email'] = email
            updated = True
            break
    if not updated:
        users.append({
            'username': CURRENT_USER,
            'email': email,
            'phone': '',
            'address': ''
        })
    write_users(users)
    return redirect(url_for('user_profile_page'))

@app.route('/admin_panel')
def admin_panel_page():
    applications = read_applications()
    pets = read_pets()
    pet_map = {p['pet_id']: p['name'] for p in pets}

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_map.get(app['pet_id'], 'Unknown'),
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })

    all_pets = []
    for pet in pets:
        all_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)

@app.route('/edit_pet/<int:pet_id>')
def edit_pet_page(pet_id):
    pet = get_pet_by_id(pet_id)
    if pet is None:
        return "Pet not found", 404
    return render_template('add_pet.html', pet=pet,
                           species_options=['Dog', 'Cat', 'Bird', 'Rabbit', 'Other'],
                           gender_options=['Male', 'Female'],
                           size_options=['Small', 'Medium', 'Large'])

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    pets = read_pets()
    pets = [p for p in pets if p['pet_id'] != pet_id]
    write_pets(pets)
    return redirect(url_for('admin_panel_page'))


if __name__ == '__main__':
    app.run(debug=True)
