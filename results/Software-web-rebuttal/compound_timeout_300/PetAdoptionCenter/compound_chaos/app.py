from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# -------------------- Data File Load/Save Helpers --------------------

def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
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

def load_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
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
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 13:
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

def save_applications(applications):
    path = os.path.join(DATA_DIR, 'applications.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in applications:
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
            f.write(line + '\n')

def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    try:
                        favorites.append({
                            'username': parts[0],
                            'pet_id': int(parts[1]),
                            'date_added': parts[2]
                        })
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
                fav['date_added']
            ])
            f.write(line + '\n')

def load_messages():
    messages = []
    path = os.path.join(DATA_DIR, 'messages.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
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

# Helper for current user (simulate logged-in)
def get_current_username():
    return 'john_doe'

# -------------------- Flask Routes --------------------

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    available_pets = [p for p in pets if p['status'] == 'Available']
    try:
        available_pets.sort(key=lambda x: datetime.strptime(x['date_added'], '%Y-%m-%d'), reverse=True)
    except Exception:
        pass
    featured_pets = available_pets[:5]
    for pet in featured_pets:
        pet['photo_url'] = ''

    applications = load_applications()
    recent_activities = []
    combined = []
    for pet in pets:
        combined.append((pet['date_added'], f"New pet added: {pet['name']}"))
    for app in applications:
        combined.append((app['date_submitted'], f"Application by {app['applicant_name']} is {app['status']}"))
    try:
        combined.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
    except Exception:
        pass
    recent_activities = [desc for _, desc in combined[:5]]

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

@app.route('/pets')
def pet_listings():
    pets = load_pets()
    species_options = ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    selected_species = request.args.get('species', 'All')
    search_query = request.args.get('search', '').strip()

    filtered_pets = pets
    if selected_species != 'All':
        filtered_pets = [p for p in filtered_pets if p['species'] == selected_species]
    if search_query:
        filtered_pets = [p for p in filtered_pets if search_query.lower() in p['name'].lower()]

    filtered_pets = [p for p in filtered_pets if p['status'] in ('Available', 'Pending')]

    for pet in filtered_pets:
        pet['photo_url'] = ''

    return render_template('pet_listings.html', pets=filtered_pets, species_options=species_options, selected_species=selected_species, search_query=search_query)

@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        abort(404)
    return render_template('pet_details.html', pet=pet)

@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    gender_options = ['Male', 'Female']
    size_options = ['Small', 'Medium', 'Large']

    if request.method == 'GET':
        return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options)

    form = request.form
    name = form.get('name', '').strip()
    species = form.get('species', '').strip()
    breed = form.get('breed', '').strip()
    age = form.get('age', '').strip()
    gender = form.get('gender', '').strip()
    size = form.get('size', '').strip()
    description = form.get('description', '').strip()

    if not name or species not in species_options or gender not in gender_options or size not in size_options:
        submission_result = 'Error: Invalid or missing required fields.'
        return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options, submission_result=submission_result)

    pets = load_pets()
    next_id = (max((p['pet_id'] for p in pets), default=0)) + 1
    shelter_id = 1
    date_added = datetime.now().strftime('%Y-%m-%d')

    new_pet = {
        'pet_id': next_id,
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

    pets.append(new_pet)
    save_pets(pets)

    submission_result = f"Success: Pet \"{name}\" added successfully." 
    return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options, submission_result=submission_result)

@app.route('/applications/apply/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        abort(404)

    housing_options = ['House', 'Apartment', 'Condo', 'Other']

    if request.method == 'GET':
        return render_template('adoption_application.html', pet=pet, housing_options=housing_options)

    form = request.form
    applicant_name = form.get('applicant_name', '').strip()
    phone = form.get('phone', '').strip()
    address = form.get('address', '').strip()
    housing_type = form.get('housing_type', '').strip()
    has_yard = form.get('has_yard', '').strip()
    other_pets = form.get('other_pets', '').strip()
    experience = form.get('experience', '').strip()
    reason = form.get('reason', '').strip()

    if not applicant_name or not phone or not address or housing_type not in housing_options or reason == '':
        submission_result = 'Error: Missing required fields or invalid selections.'
        return render_template('adoption_application.html', pet=pet, housing_options=housing_options, submission_result=submission_result)

    username = get_current_username()
    applications = load_applications()
    next_id = max((a['application_id'] for a in applications), default=0) + 1
    date_submitted = datetime.now().strftime('%Y-%m-%d')

    new_application = {
        'application_id': next_id,
        'username': username,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': has_yard if has_yard in ['Yes', 'No'] else 'No',
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': date_submitted
    }

    applications.append(new_application)
    save_applications(applications)

    submission_result = 'Success: Your adoption application has been submitted.'
    return render_template('adoption_application.html', pet=pet, housing_options=housing_options, submission_result=submission_result)

@app.route('/applications/my')
def my_applications():
    username = get_current_username()
    applications = load_applications()
    pets = load_pets()

    status_options = ['All', 'Pending', 'Approved', 'Rejected']
    selected_status = request.args.get('status', 'All')

    filtered = [a for a in applications if a['username'] == username]
    if selected_status != 'All':
        filtered = [a for a in filtered if a['status'] == selected_status]

    pet_names = {p['pet_id']: p['name'] for p in pets}
    for app in filtered:
        app['pet_name'] = pet_names.get(app['pet_id'], 'Unknown')
        app['date'] = app['date_submitted']

    return render_template('my_applications.html', applications=filtered, status_options=status_options, selected_status=selected_status)

@app.route('/favorites')
def favorites():
    username = get_current_username()
    favorites = load_favorites()
    pets = load_pets()

    pet_lookup = {p['pet_id']: p for p in pets}
    favorite_pets = []
    for fav in favorites:
        if fav['username'] == username:
            pet = pet_lookup.get(fav['pet_id'])
            if pet:
                favorite_pets.append({
                    'pet_id': pet['pet_id'],
                    'name': pet['name'],
                    'species': pet['species'],
                    'age': pet['age'],
                    'photo_url': ''
                })

    return render_template('favorites.html', favorite_pets=favorite_pets)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    username = get_current_username()
    messages = load_messages()

    def build_conversations(messages, username):
        conv = {}
        for m in messages:
            if m['sender_username'] == username or m['recipient_username'] == username:
                other = m['recipient_username'] if m['sender_username'] == username else m['sender_username']
                if other not in conv:
                    conv[other] = {
                        'recipient_username': other,
                        'last_message': m['content'],
                        'unread_count': 0,
                        'last_timestamp': m['timestamp']
                    }
                else:
                    if datetime.strptime(m['timestamp'], '%Y-%m-%d %H:%M:%S') > datetime.strptime(conv[other]['last_timestamp'], '%Y-%m-%d %H:%M:%S'):
                        conv[other]['last_message'] = m['content']
                        conv[other]['last_timestamp'] = m['timestamp']
                if not m['is_read'] and m['recipient_username'] == username:
                    conv[other]['unread_count'] += 1
        res = []
        for c in conv.values():
            c.pop('last_timestamp', None)
            res.append(c)
        return res

    if request.method == 'POST':
        form = request.form
        recipient = form.get('recipient_username', '').strip()
        subject = form.get('subject', '').strip()
        content = form.get('content', '').strip()

        if not recipient or not subject or not content:
            submission_result = 'Error: Missing recipient, subject, or content.'
        else:
            next_id = max((m['message_id'] for m in messages), default=0) + 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_msg = {
                'message_id': next_id,
                'sender_username': username,
                'recipient_username': recipient,
                'subject': subject,
                'content': content,
                'timestamp': timestamp,
                'is_read': False
            }
            messages.append(new_msg)
            save_messages(messages)
            submission_result = 'Success: Message sent.'

        conversations = build_conversations(messages, username)
        return render_template('messages.html', conversations=conversations, submission_result=submission_result)

    # GET request
    conversations = build_conversations(messages, username)
    return render_template('messages.html', conversations=conversations, submission_result='')

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    username = get_current_username()
    users = load_users()

    user_info = None
    for u in users:
        if u['username'] == username:
            user_info = {'username': u['username'], 'email': u['email']}
            break
    if user_info is None:
        user_info = {'username': username, 'email': ''}

    submission_result = ''

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email or '@' not in email:
            submission_result = 'Error: Invalid email address.'
            return render_template('profile.html', user_info=user_info, submission_result=submission_result)

        updated = False
        for user in users:
            if user['username'] == username:
                user['email'] = email
                updated = True
                break
        if not updated:
            users.append({'username': username, 'email': email, 'phone': '', 'address': ''})

        save_users(users)
        user_info['email'] = email
        submission_result = 'Success: Profile updated.'

    return render_template('profile.html', user_info=user_info, submission_result=submission_result)

@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown')
            pending_applications.append({
                'application_id': app['application_id'],
                'pet_name': pet_name,
                'applicant_name': app['applicant_name'],
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

@app.route('/admin/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    species_options = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    gender_options = ['Male', 'Female']
    size_options = ['Small', 'Medium', 'Large']

    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        abort(404)

    if request.method == 'GET':
        return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options, pet=pet)

    form = request.form
    name = form.get('name', '').strip()
    species = form.get('species', '').strip()
    breed = form.get('breed', '').strip()
    age = form.get('age', '').strip()
    gender = form.get('gender', '').strip()
    size = form.get('size', '').strip()
    description = form.get('description', '').strip()

    if not name or species not in species_options or gender not in gender_options or size not in size_options:
        submission_result = 'Error: Invalid or missing required fields.'
        return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options, pet=pet, submission_result=submission_result)

    pet['name'] = name
    pet['species'] = species
    pet['breed'] = breed
    pet['age'] = age
    pet['gender'] = gender
    pet['size'] = size
    pet['description'] = description

    save_pets(pets)

    submission_result = f'Success: Pet "{name}" updated successfully.'
    return render_template('add_pet.html', species_options=species_options, gender_options=gender_options, size_options=size_options, pet=pet, submission_result=submission_result)

@app.route('/admin/pets/delete/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    pets = load_pets()
    new_pets = [p for p in pets if p['pet_id'] != pet_id]
    if len(new_pets) == len(pets):
        abort(404)
    save_pets(new_pets)
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)
