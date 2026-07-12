from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


# Helper functions for data read/write

def read_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                username, email, phone, address = parts[:4]
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                }
    except FileNotFoundError:
        pass
    return users

def write_users(users):
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for user in users.values():
                f.write(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}\n")
    except Exception:
        pass

def read_pets():
    pets = []
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 11:
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
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return pets

def write_pets(pets):
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'w', encoding='utf-8') as f:
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
    except Exception:
        pass

def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 13:
                    continue
                try:
                    app = {
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
                    applications.append(app)
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return applications

def write_applications(applications):
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
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
    except Exception:
        pass

def read_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 3:
                    continue
                try:
                    favorite = {
                        'username': parts[0],
                        'pet_id': int(parts[1]),
                        'date_added': parts[2]
                    }
                    favorites.append(favorite)
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return favorites

def write_favorites(favorites):
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    fav['username'],
                    str(fav['pet_id']),
                    fav['date_added']
                ])
                f.write(line + '\n')
    except Exception:
        pass

def read_messages():
    messages = []
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 7:
                    continue
                try:
                    message = {
                        'message_id': int(parts[0]),
                        'sender_username': parts[1],
                        'recipient_username': parts[2],
                        'subject': parts[3],
                        'content': parts[4],
                        'timestamp': parts[5],
                        'is_read': parts[6]
                    }
                    messages.append(message)
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return messages

def write_messages(messages):
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'w', encoding='utf-8') as f:
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
    except Exception:
        pass


def get_next_pet_id(pets):
    return max((pet['pet_id'] for pet in pets), default=0) + 1

def get_next_application_id(applications):
    return max((app['application_id'] for app in applications), default=0) + 1

def get_next_message_id(messages):
    return max((msg['message_id'] for msg in messages), default=0) + 1


# Hardcoded current user for demonstration
CURRENT_USER = 'john_doe'


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    pets = read_pets()
    featured_pets = []
    available_pets = [pet for pet in pets if pet['status'].lower() == 'available']
    try:
        available_pets.sort(key=lambda p: p['date_added'], reverse=True)
    except Exception:
        pass
    for pet in available_pets[:5]:
        featured_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        })
    return render_template('dashboard.html', featured_pets=featured_pets)

@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = read_pets()
    pet_list = []
    for pet in pets:
        pet_list.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        })
    return render_template('pet_listings.html', pets=pet_list)

@app.route('/pets', methods=['POST'])
def pet_listings_filtered():
    search_query = request.form.get('search', '').strip().lower()
    filter_species = request.form.get('species', '').strip().lower()
    pets = read_pets()
    filtered = []
    for pet in pets:
        if pet['status'].lower() != 'available':
            continue
        if search_query and search_query not in pet['name'].lower():
            continue
        if filter_species and filter_species != pet['species'].lower():
            continue
        filtered.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        })
    return render_template('pet_listings.html', pets=filtered)

@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
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
    return render_template('pet_details.html', pet=pet_dict)

@app.route('/pets/add', methods=['GET'])
def add_pet():
    return render_template('add_pet.html')

@app.route('/pets/add', methods=['POST'])
def submit_pet():
    form_errors = {}
    name = request.form.get('name', '').strip()
    species = request.form.get('species', '').strip()
    breed = request.form.get('breed', '').strip()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    size = request.form.get('size', '').strip()
    description = request.form.get('description', '').strip()

    if not name:
        form_errors['name'] = 'Name is required.'
    if not species:
        form_errors['species'] = 'Species is required.'
    if not age:
        form_errors['age'] = 'Age is required.'
    if not gender:
        form_errors['gender'] = 'Gender is required.'
    if not size:
        form_errors['size'] = 'Size is required.'

    if form_errors:
        return render_template('add_pet.html', form_errors=form_errors)

    pets = read_pets()
    new_id = get_next_pet_id(pets)
    today = datetime.date.today().strftime('%Y-%m-%d')
    new_pet = {
        'pet_id': new_id,
        'name': name,
        'species': species,
        'breed': breed,
        'age': age,
        'gender': gender,
        'size': size,
        'description': description,
        'shelter_id': 1,
        'status': 'Available',
        'date_added': today
    }
    pets.append(new_pet)
    write_pets(pets)
    success_message = 'New pet added successfully.'
    return render_template('add_pet.html', success_message=success_message)

@app.route('/applications/apply/<int:pet_id>', methods=['GET'])
def adoption_application(pet_id):
    pets = read_pets()
    pet = next(({'pet_id': p['pet_id'], 'name': p['name']} for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('application.html', pet=pet)

@app.route('/applications/apply/<int:pet_id>', methods=['POST'])
def submit_application(pet_id):
    form_errors = {}
    applicant_name = request.form.get('applicant_name', '').strip()
    phone = request.form.get('phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()
    has_yard = request.form.get('has_yard', '').strip()
    other_pets = request.form.get('other_pets', '').strip()
    experience = request.form.get('experience', '').strip()
    address = request.form.get('address', '').strip()

    if not applicant_name:
        form_errors['applicant_name'] = 'Applicant name is required.'
    if not phone:
        form_errors['phone'] = 'Phone number is required.'
    if not housing_type:
        form_errors['housing_type'] = 'Housing type is required.'
    if not reason:
        form_errors['reason'] = 'Reason for adoption is required.'

    pets = read_pets()
    pet = next(({'pet_id': p['pet_id'], 'name': p['name']} for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if form_errors:
        return render_template('application.html', pet=pet, form_errors=form_errors)

    applications = read_applications()
    new_id = get_next_application_id(applications)
    today = datetime.date.today().strftime('%Y-%m-%d')

    app_entry = {
        'application_id': new_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': has_yard if has_yard else 'No',
        'other_pets': other_pets if other_pets else 'None',
        'experience': experience if experience else 'None',
        'reason': reason,
        'status': 'Pending',
        'date_submitted': today
    }

    applications.append(app_entry)
    write_applications(applications)

    success_message = 'Application submitted successfully.'
    return render_template('application.html', pet=pet, success_message=success_message)

@app.route('/applications', methods=['GET'])
def my_applications():
    applications = read_applications()
    pets = read_pets()
    apps_list = []
    for app in applications:
        if app['username'] == CURRENT_USER:
            pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
            apps_list.append({
                'application_id': app['application_id'],
                'pet_name': pet_name,
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })
    return render_template('my_applications.html', applications=apps_list)

@app.route('/favorites', methods=['GET'])
def favorites():
    all_favorites = read_favorites()
    pets = read_pets()
    user_favorites = [fav for fav in all_favorites if fav['username'] == CURRENT_USER]
    favorite_pets = []
    for fav in user_favorites:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
            })
    return render_template('favorites.html', favorite_pets=favorite_pets)

@app.route('/messages', methods=['GET'])
def messages_page():
    messages = read_messages()
    conversations = {}

    # Collect conversations where CURRENT_USER is sender or recipient
    for msg in messages:
        if msg['sender_username'] == CURRENT_USER or msg['recipient_username'] == CURRENT_USER:
            other_user = msg['recipient_username'] if msg['sender_username'] == CURRENT_USER else msg['sender_username']
            conv_key = frozenset([CURRENT_USER, other_user])
            if conv_key not in conversations:
                conversations[conv_key] = {
                    'conversation_id': len(conversations) + 1,
                    'other_user': other_user,
                    'last_message': msg['content'],
                    'unread_count': 0
                }
            else:
                # Update last message to latest (assumes messages in chronological order)
                conversations[conv_key]['last_message'] = msg['content']
            if msg['recipient_username'] == CURRENT_USER and msg['is_read'].lower() == 'false':
                conversations[conv_key]['unread_count'] += 1

    conversations_list = list(conversations.values())
    return render_template('messages.html', conversations=conversations_list)

@app.route('/messages/send', methods=['POST'])
def send_message():
    recipient = request.form.get('recipient', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not recipient or not content:
        return redirect(url_for('messages_page'))

    messages = read_messages()
    new_id = get_next_message_id(messages)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

@app.route('/profile', methods=['GET'])
def profile():
    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        return render_template('profile.html', username=CURRENT_USER, email='')
    return render_template('profile.html', username=user['username'], email=user['email'])

@app.route('/profile', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    form_errors = {}
    if not email:
        form_errors['email'] = 'Email is required.'
    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        form_errors['email'] = 'User not found.'
    if form_errors:
        return render_template('profile.html', username=CURRENT_USER, email=email, form_errors=form_errors)
    user['email'] = email
    users[CURRENT_USER] = user
    write_users(users)
    success_message = 'Profile updated successfully.'
    return render_template('profile.html', username=CURRENT_USER, email=email, success_message=success_message)

@app.route('/admin', methods=['GET'])
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'].lower() == 'pending':
            pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_name,
                'date_submitted': app['date_submitted']
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

@app.route('/admin/applications/approve/<int:application_id>', methods=['POST'])
def approve_application(application_id):
    applications = read_applications()
    pets = read_pets()
    application = next((app for app in applications if app['application_id'] == application_id), None)
    if not application:
        return "Application not found", 404
    application['status'] = 'Approved'
    for pet in pets:
        if pet['pet_id'] == application['pet_id'] and pet['status'].lower() == 'available':
            pet['status'] = 'Pending'
            break
    write_applications(applications)
    write_pets(pets)
    return redirect(url_for('admin_panel'))

@app.route('/admin/applications/reject/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    applications = read_applications()
    application = next((app for app in applications if app['application_id'] == application_id), None)
    if not application:
        return "Application not found", 404
    application['status'] = 'Rejected'
    write_applications(applications)
    return redirect(url_for('admin_panel'))

@app.route('/admin/pets/edit/<int:pet_id>', methods=['GET'])
def edit_pet(pet_id):
    pets = read_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('edit_pet.html', pet=pet)

@app.route('/admin/pets/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    pets = read_pets()
    new_pets = [p for p in pets if p['pet_id'] != pet_id]
    if len(new_pets) == len(pets):
        return "Pet not found", 404
    write_pets(new_pets)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
