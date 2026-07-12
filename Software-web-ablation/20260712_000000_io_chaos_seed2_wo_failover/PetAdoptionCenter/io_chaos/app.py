from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data

def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
    return users


def load_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(path):
        return pets
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                # 11 fields expected
                if len(parts) == 11:
                    try:
                        pet_id = int(parts[0])
                        shelter_id = int(parts[8])
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
                    except ValueError:
                        continue
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


def load_applications():
    applications = []
    path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(path):
        return applications
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                # 13 fields expected
                if len(parts) == 13:
                    try:
                        application_id = int(parts[0])
                        pet_id = int(parts[2])
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
                    except ValueError:
                        continue
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
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                # 3 fields expected
                if len(parts) == 3:
                    try:
                        pet_id = int(parts[1])
                        fav = {
                            'username': parts[0],
                            'pet_id': pet_id,
                            'date_added': parts[2]
                        }
                        favorites.append(fav)
                    except ValueError:
                        continue
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                fav['username'],
                str(fav['pet_id']),
                fav['date_added'],
            ])
            f.write(line + '\n')


def load_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if not os.path.exists(path):
        return messages
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                # 7 fields
                if len(parts) == 7:
                    try:
                        message_id = int(parts[0])
                        is_read = True if parts[6].lower() == 'true' else False
                        msg = {
                            'message_id': message_id,
                            'sender_username': parts[1],
                            'recipient_username': parts[2],
                            'subject': parts[3],
                            'content': parts[4],
                            'timestamp': parts[5],
                            'is_read': is_read
                        }
                        messages.append(msg)
                    except ValueError:
                        continue
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
                'true' if msg['is_read'] else 'false'
            ])
            f.write(line + '\n')


def load_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if not os.path.exists(path):
        return shelters
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 5:
                    try:
                        shelter_id = int(parts[0])
                        shelters.append({
                            'shelter_id': shelter_id,
                            'name': parts[1],
                            'address': parts[2],
                            'phone': parts[3],
                            'email': parts[4]
                        })
                    except ValueError:
                        continue
    return shelters


def load_adoption_history():
    history = []
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 6:
                    try:
                        history_id = int(parts[0])
                        pet_id = int(parts[2])
                        shelter_id = int(parts[5])
                        history.append({
                            'history_id': history_id,
                            'username': parts[1],
                            'pet_id': pet_id,
                            'pet_name': parts[3],
                            'adoption_date': parts[4],
                            'shelter_id': shelter_id
                        })
                    except ValueError:
                        continue
    return history


# -- Route Handlers -- #

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    # Select featured pets: limit 5 with status Available or Pending (prefer Available)
    featured = [pet for pet in pets if pet['status'] in ['Available', 'Pending']]
    # Sort by date_added descending
    featured.sort(key=lambda x: x['date_added'], reverse=True)
    featured_pets = featured[:5]
    return render_template('dashboard.html', featured_pets=featured_pets)

@app.route('/pets')
def pet_listings():
    pets = load_pets()
    # For pet_listings.html, context pets list dict with specified keys
    pets_context = []
    for pet in pets:
        pets_context.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': "",  # Not provided in pets.txt, leave blank
            'breed': pet['breed']
        })
    return render_template('pet_listings.html', pets=pets_context)

@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    # Provide context keys exactly as spec
    pet_context = {
        'pet_id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'breed': pet['breed'],
        'age': pet['age'],
        'gender': pet['gender'],
        'size': pet['size'],
        'description': pet['description']
    }
    return render_template('pet_details.html', pet=pet_context)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        # Read form data
        name = request.form.get('pet-name-input', '').strip()
        species = request.form.get('pet-species-input', '').strip()
        breed = request.form.get('pet-breed-input', '').strip()
        age = request.form.get('pet-age-input', '').strip()
        gender = request.form.get('pet-gender-input', '').strip()
        size = request.form.get('pet-size-input', '').strip()
        description = request.form.get('pet-description-input', '').strip()

        # Validate required fields
        if not all([name, species, breed, age, gender, size, description]):
            return render_template('add_pet.html', error_msg='All fields are required.')

        pets = load_pets()
        # Assign new pet_id as max+1 or 1 if no pets
        new_id = 1
        if pets:
            new_id = max(p['pet_id'] for p in pets) + 1

        # For shelter_id and status, assign placeholder values (shelter_id=1, status='Available')
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
            'date_added': datetime.now().strftime('%Y-%m-%d')
        }
        pets.append(new_pet)
        save_pets(pets)
        success_msg = f"Pet '{name}' added successfully."
        return render_template('add_pet.html', success_msg=success_msg)

    return render_template('add_pet.html')

@app.route('/apply/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if request.method == 'POST':
        applicant_name = request.form.get('applicant-name', '').strip()
        phone = request.form.get('applicant-phone', '').strip()
        housing_type = request.form.get('housing-type', '').strip()
        reason = request.form.get('reason', '').strip()

        if not all([applicant_name, phone, housing_type, reason]):
            return render_template('adoption_application.html', pet=pet, error_msg='All fields are required.')

        # Simulate username from applicant_name (lower case, underscores for spaces)
        username = applicant_name.lower().replace(' ', '_')

        # Load users and check if username exists; if not add default user (minimal)
        users = load_users()
        if not any(u['username'] == username for u in users):
            users.append({'username': username, 'email': '', 'phone': phone, 'address': ''})
            # Save users (not required by spec, so skipping saving users)

        # Load applications, find next id
        applications = load_applications()
        new_id = 1
        if applications:
            new_id = max(a['application_id'] for a in applications) + 1

        # Find address from users if exists
        address = ''
        for u in users:
            if u['username'] == username:
                address = u.get('address', '')
                break

        new_app = {
            'application_id': new_id,
            'username': username,
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
        applications.append(new_app)
        save_applications(applications)

        success_msg = 'Your adoption application has been submitted successfully.'
        return render_template('adoption_application.html', success_msg=success_msg)

    return render_template('adoption_application.html', pet=pet)

@app.route('/my_applications')
def my_applications():
    applications = load_applications()
    pets = load_pets()
    # Simulate current username as example 'john_doe'
    current_user = 'john_doe'

    # Filter applications by current user
    user_apps = [app for app in applications if app['username'] == current_user]

    applications_context = []
    for app in user_apps:
        pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
        pet_name = pet['name'] if pet else ''
        applications_context.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=applications_context)

@app.route('/favorites')
def favorites():
    favorites = load_favorites()
    pets = load_pets()
    current_user = 'john_doe'

    # Find favorite pets for current user
    user_favorites = [f for f in favorites if f['username'] == current_user]

    favorite_pets = []
    for fav in user_favorites:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'photo_url': ""
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = load_messages()
    current_user = 'john_doe'

    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        if not all([recipient, subject, content]):
            return render_template('messages.html', conversations=messages, error_msg='All message fields are required.')

        new_id = 1
        if messages:
            new_id = max(m['message_id'] for m in messages) + 1

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_message = {
            'message_id': new_id,
            'sender_username': current_user,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }
        messages.append(new_message)
        save_messages(messages)

        return render_template('messages.html', conversations=messages)

    # GET
    # Conversations involve current_user as sender or recipient
    conversations = [m for m in messages if current_user in (m['sender_username'], m['recipient_username'])]

    return render_template('messages.html', conversations=conversations)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Simulate current user
    current_user = 'john_doe'
    users = load_users()

    user_profile = next((u for u in users if u['username'] == current_user), None)
    if not user_profile:
        # If user not found, create a basic one
        user_profile = {'username': current_user, 'email': '', 'phone': '', 'address': ''}
        users.append(user_profile)

    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if not email:
            return render_template('profile.html', user_profile=user_profile, error_msg='Email cannot be empty.')
        # Update user email
        user_profile['email'] = email

        # Save users - according to spec users.txt is loaded and read, but writing not specified,
        # so not saving to file.

        success_msg = 'Profile updated successfully.'
        return render_template('profile.html', user_profile=user_profile, success_msg=success_msg)

    # GET
    return render_template('profile.html', user_profile=user_profile)

@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()

    pending_apps = [app for app in applications if app['status'] == 'Pending']

    pending_applications = []
    for app in pending_apps:
        pet_name = ''
        pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
        if pet:
            pet_name = pet['name']
        pending_applications.append({
            'application_id': app['application_id'],
            'applicant_name': app['applicant_name'],
            'pet_name': pet_name,
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
