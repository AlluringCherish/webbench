from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'


# Utility functions for data loading and saving

def load_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 11:
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


def save_pets(pets):
    path = os.path.join(DATA_DIR, 'pets.txt')
    with open(path, 'w', encoding='utf-8') as f:
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


def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 4:
                    user = {
                        'username': fields[0],
                        'email': fields[1],
                        'phone': fields[2],
                        'address': fields[3]
                    }
                    users.append(user)
    return users


def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users:
            line = '|'.join([
                user['username'],
                user['email'],
                user['phone'],
                user['address']
            ])
            f.write(line + '\n')


def load_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 13:
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


def save_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
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


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 3:
                    fav = {
                        'username': fields[0],
                        'pet_id': int(fields[1]),
                        'date_added': fields[2]
                    }
                    favorites.append(fav)
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav['username'],
                str(fav['pet_id']),
                fav['date_added']
            ])
            f.write(line + '\n')


def load_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 7:
                    msg = {
                        'message_id': int(fields[0]),
                        'sender_username': fields[1],
                        'recipient_username': fields[2],
                        'subject': fields[3],
                        'content': fields[4],
                        'timestamp': fields[5],
                        'is_read': fields[6]  # string 'true' or 'false'
                    }
                    messages.append(msg)
    return messages


def save_messages(messages):
    path = os.path.join(DATA_DIR, 'messages.txt')
    with open(path, 'w', encoding='utf-8') as f:
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


def load_adoption_history():
    history = []
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 6:
                    entry = {
                        'history_id': int(fields[0]),
                        'username': fields[1],
                        'pet_id': int(fields[2]),
                        'pet_name': fields[3],
                        'adoption_date': fields[4],
                        'shelter_id': int(fields[5])
                    }
                    history.append(entry)
    return history


def save_adoption_history(history):
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for entry in history:
            line = '|'.join([
                str(entry['history_id']),
                entry['username'],
                str(entry['pet_id']),
                entry['pet_name'],
                entry['adoption_date'],
                str(entry['shelter_id'])
            ])
            f.write(line + '\n')


def load_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                fields = line.strip().split('|')
                if len(fields) == 5:
                    shelter = {
                        'shelter_id': int(fields[0]),
                        'name': fields[1],
                        'address': fields[2],
                        'phone': fields[3],
                        'email': fields[4]
                    }
                    shelters.append(shelter)
    return shelters


def save_shelters(shelters):
    path = os.path.join(DATA_DIR, 'shelters.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for shelter in shelters:
            line = '|'.join([
                str(shelter['shelter_id']),
                shelter['name'],
                shelter['address'],
                shelter['phone'],
                shelter['email']
            ])
            f.write(line + '\n')


# For this exercise, we'll assume current logged in user is 'john_doe'
# In a real app, authentication would be managed properly
CURRENT_USER = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    pets = load_pets()
    # featured_pets: list of dict with keys pet_id, name, species, age, photo_url
    # photo_url not provided in schema or data; assume a url generated from pet_id
    featured_pets = []
    for pet in pets:
        if pet['status'] == 'Available':
            featured_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                # Assuming photo url pattern
                'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
            })
    # Limit to first 5 featured pets
    featured_pets = featured_pets[:5]
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets')
def pet_listings_page():
    pets = load_pets()
    pets_public = []
    for pet in pets:
        pets_public.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
        })
    return render_template('pet_listings.html', pets=pets_public)


@app.route('/pets/search', methods=['POST'])
def pet_search():
    search_term = request.form.get('search_term', '').strip()
    filter_species = request.form.get('filter_species', '').strip()

    # Redirect to '/pets' with query params
    # Construct query string with search_term and filter_species
    from urllib.parse import urlencode
    query_params = {}
    if search_term:
        query_params['search_term'] = search_term
    if filter_species:
        query_params['filter_species'] = filter_species

    # Redirect to pet_listings_page but include filters (though design does not specify exactly how filters are handled on GET; So just redirect with params)
    return redirect(url_for('pet_listings_page') + ('?' + urlencode(query_params) if query_params else ''))


@app.route('/pets/<int:pet_id>')
def pet_details_page(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        return "Pet Not Found", 404
    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET'])
def add_pet_page():
    return render_template('add_pet.html')


@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    form = request.form
    name = form.get('pet-name-input', '').strip()
    species = form.get('pet-species-input', '').strip()
    breed = form.get('pet-breed-input', '').strip()
    age = form.get('pet-age-input', '').strip()
    gender = form.get('pet-gender-input', '').strip()
    size = form.get('pet-size-input', '').strip()
    description = form.get('pet-description-input', '').strip()

    pets = load_pets()
    new_pet_id = max([pet['pet_id'] for pet in pets], default=0) + 1

    # Assign shelter_id default as 1 (as no form specified)
    shelter_id = 1
    status = 'Available'
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

    pets.append(new_pet)
    save_pets(pets)

    return redirect(url_for('pet_listings_page'))


@app.route('/adoption/apply/<int:pet_id>', methods=['GET'])
def adoption_application_page(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if pet is None:
        return "Pet Not Found", 404
    return render_template('adoption_application.html', pet=pet)


@app.route('/adoption/apply/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    form = request.form
    applicant_name = form.get('applicant_name', '').strip()
    phone = form.get('phone', '').strip()
    housing_type = form.get('housing_type', '').strip()
    reason = form.get('reason', '').strip()

    users = load_users()
    user = next((u for u in users if u['username'] == CURRENT_USER), None)
    if user is None:
        # For this example, create a default user if not found
        user = {
            'username': CURRENT_USER,
            'email': '',
            'phone': '',
            'address': ''
        }
        users.append(user)
        save_users(users)

    applications = load_applications()
    new_application_id = max([app['application_id'] for app in applications], default=0) + 1

    address = user['address']

    # For fields not in form, set defaults as empty or 'No'
    has_yard = 'No'
    other_pets = ''
    experience = ''
    status = 'Pending'
    date_submitted = datetime.now().strftime('%Y-%m-%d')

    new_application = {
        'application_id': new_application_id,
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
        'status': status,
        'date_submitted': date_submitted
    }

    applications.append(new_application)
    save_applications(applications)

    return redirect(url_for('my_applications_page'))


@app.route('/my_applications')
def my_applications_page():
    applications = load_applications()
    pets = load_pets()

    # Filter applications for CURRENT_USER
    user_apps = [app for app in applications if app['username'] == CURRENT_USER]

    # Build list of dict with application_id, pet_name, date_submitted, status
    result = []
    pet_map = {pet['pet_id']: pet for pet in pets}
    for app in user_apps:
        pet_name = pet_map.get(app['pet_id'], {}).get('name', 'Unknown')
        result.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=result)


@app.route('/my_applications/filter', methods=['POST'])
def filter_applications():
    filter_status = request.form.get('filter_status', '').strip()
    # Redirect to my_applications with query param to filter status
    from urllib.parse import urlencode
    query_params = {}
    if filter_status:
        query_params['filter_status'] = filter_status

    return redirect(url_for('my_applications_page') + ('?' + urlencode(query_params) if query_params else ''))


@app.route('/favorites')
def favorites_page():
    favorites = load_favorites()
    pets = load_pets()

    user_favs = [fav for fav in favorites if fav['username'] == CURRENT_USER]
    pet_map = {pet['pet_id']: pet for pet in pets}
    favorite_pets = []
    for fav in user_favs:
        pet = pet_map.get(fav['pet_id'])
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': url_for('static', filename=f'images/pets/{pet["pet_id"]}.jpg')
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages')
def messages_page():
    messages = load_messages()

    # Group messages into conversations by recipient_username or sender_username (conversation with someone)
    conversations_map = {}

    # We'll consider conversations involving CURRENT_USER either as sender or recipient
    for msg in messages:
        if msg['sender_username'] == CURRENT_USER:
            other_user = msg['recipient_username']
        elif msg['recipient_username'] == CURRENT_USER:
            other_user = msg['sender_username']
        else:
            continue  # Message not involving current user

        conv_key = other_user

        if conv_key not in conversations_map:
            conversations_map[conv_key] = {
                'conversation_id': len(conversations_map) + 1,
                'recipient_username': conv_key,
                'last_message': msg['content'],
                'last_timestamp': msg['timestamp'],
                'unread_count': 0
            }
        else:
            # update last message if newer
            if msg['timestamp'] > conversations_map[conv_key]['last_timestamp']:
                conversations_map[conv_key]['last_message'] = msg['content']
                conversations_map[conv_key]['last_timestamp'] = msg['timestamp']

        # Count unread if current user is recipient and is_read false
        if msg['recipient_username'] == CURRENT_USER and msg['is_read'].lower() == 'false':
            conversations_map[conv_key]['unread_count'] += 1

    conversations = list(conversations_map.values())

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send/<recipient_username>', methods=['POST'])
def send_message(recipient_username):
    form = request.form
    message_content = form.get('message_content', '').strip()

    if not message_content:
        return redirect(url_for('messages_page'))

    messages = load_messages()
    new_message_id = max([m['message_id'] for m in messages], default=0) + 1

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_message = {
        'message_id': new_message_id,
        'sender_username': CURRENT_USER,
        'recipient_username': recipient_username,
        'subject': '',  # Subject not provided in form
        'content': message_content,
        'timestamp': timestamp,
        'is_read': 'false'
    }

    messages.append(new_message)
    save_messages(messages)

    return redirect(url_for('messages_page'))


@app.route('/profile')
def user_profile_page():
    users = load_users()
    user = next((u for u in users if u['username'] == CURRENT_USER), None)
    username = CURRENT_USER
    email = user['email'] if user else ''
    return render_template('profile.html', username=username, email=email)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()

    users = load_users()
    user = next((u for u in users if u['username'] == CURRENT_USER), None)

    if user:
        user['email'] = email
        save_users(users)

    return redirect(url_for('user_profile_page'))


@app.route('/admin')
def admin_panel_page():
    applications = load_applications()
    pets = load_pets()

    pending_applications = [a for a in applications if a['status'] == 'Pending']

    all_pets = pets  # all pet details

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
