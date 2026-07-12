from flask import Flask, render_template, redirect, url_for, request, abort
import os
import datetime

app = Flask(__name__)

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
PETS_FILE = os.path.join(DATA_DIR, 'pets.txt')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.txt')
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.txt')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.txt')
ADOPTION_HISTORY_FILE = os.path.join(DATA_DIR, 'adoption_history.txt')
SHELTERS_FILE = os.path.join(DATA_DIR, 'shelters.txt')

# Utility Functions

def read_lines(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return content.split('\n')
    except Exception:
        return []

def write_lines(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True
    except Exception:
        return False

# Data loaders and savers

def load_users():
    users = {}
    for line in read_lines(USERS_FILE):
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

def load_pets():
    pets = []
    for line in read_lines(PETS_FILE):
        parts = line.split('|')
        if len(parts) != 11:
            continue
        try:
            pet_id = int(parts[0])
            name = parts[1]
            species = parts[2]
            breed = parts[3]
            age = parts[4]
            gender = parts[5]
            size = parts[6]
            description = parts[7]
            shelter_id = int(parts[8])
            status = parts[9]
            date_added = parts[10]
            pets.append({
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
            })
        except Exception:
            continue
    return pets

def save_pets(pets):
    lines = []
    for p in pets:
        line = '|'.join([
            str(p.get('pet_id', '')),
            p.get('name', '').replace('|', ' '),
            p.get('species', '').replace('|', ' '),
            p.get('breed', '').replace('|', ' '),
            p.get('age', '').replace('|', ' '),
            p.get('gender', '').replace('|', ' '),
            p.get('size', '').replace('|', ' '),
            p.get('description', '').replace('|', ' '),
            str(p.get('shelter_id', '')),
            p.get('status', '').replace('|', ' '),
            p.get('date_added', '')
        ])
        lines.append(line)
    return write_lines(PETS_FILE, lines)

def load_applications():
    applications = []
    for line in read_lines(APPLICATIONS_FILE):
        parts = line.split('|')
        if len(parts) != 13:
            continue
        try:
            application_id = int(parts[0])
            username = parts[1]
            pet_id = int(parts[2])
            applicant_name = parts[3]
            phone = parts[4]
            address = parts[5]
            housing_type = parts[6]
            has_yard = parts[7]
            other_pets = parts[8]
            experience = parts[9]
            reason = parts[10]
            status = parts[11]
            date_submitted = parts[12]
            applications.append({
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
            })
        except Exception:
            continue
    return applications

def save_applications(applications):
    lines = []
    for a in applications:
        line = '|'.join([
            str(a.get('application_id', '')),
            a.get('username', '').replace('|', ' '),
            str(a.get('pet_id', '')),
            a.get('applicant_name', '').replace('|', ' '),
            a.get('phone', '').replace('|', ' '),
            a.get('address', '').replace('|', ' '),
            a.get('housing_type', '').replace('|', ' '),
            a.get('has_yard', '').replace('|', ' '),
            a.get('other_pets', '').replace('|', ' '),
            a.get('experience', '').replace('|', ' '),
            a.get('reason', '').replace('|', ' '),
            a.get('status', '').replace('|', ' '),
            a.get('date_submitted', '')
        ])
        lines.append(line)
    return write_lines(APPLICATIONS_FILE, lines)

def load_favorites():
    favorites = []
    for line in read_lines(FAVORITES_FILE):
        parts = line.split('|')
        if len(parts) != 3:
            continue
        try:
            username = parts[0]
            pet_id = int(parts[1])
            date_added = parts[2]
            favorites.append({
                'username': username,
                'pet_id': pet_id,
                'date_added': date_added
            })
        except Exception:
            continue
    return favorites

def load_messages():
    messages = []
    for line in read_lines(MESSAGES_FILE):
        parts = line.split('|')
        if len(parts) != 7:
            continue
        try:
            message_id = int(parts[0])
            sender_username = parts[1]
            recipient_username = parts[2]
            subject = parts[3]
            content = parts[4]
            timestamp = parts[5]
            is_read = parts[6].lower() == 'true'
            messages.append({
                'message_id': message_id,
                'sender_username': sender_username,
                'recipient_username': recipient_username,
                'subject': subject,
                'content': content,
                'timestamp': timestamp,
                'is_read': is_read
            })
        except Exception:
            continue
    return messages

def save_messages(messages):
    lines = []
    for m in messages:
        line = '|'.join([
            str(m.get('message_id', '')),
            m.get('sender_username', '').replace('|', ' '),
            m.get('recipient_username', '').replace('|', ' '),
            m.get('subject', '').replace('|', ' '),
            m.get('content', '').replace('|', ' '),
            m.get('timestamp', ''),
            'true' if m.get('is_read', False) else 'false'
        ])
        lines.append(line)
    return write_lines(MESSAGES_FILE, lines)

def load_adoption_history():
    history = []
    for line in read_lines(ADOPTION_HISTORY_FILE):
        parts = line.split('|')
        if len(parts) != 6:
            continue
        try:
            history_id = int(parts[0])
            username = parts[1]
            pet_id = int(parts[2])
            pet_name = parts[3]
            adoption_date = parts[4]
            shelter_id = int(parts[5])
            history.append({
                'history_id': history_id,
                'username': username,
                'pet_id': pet_id,
                'pet_name': pet_name,
                'adoption_date': adoption_date,
                'shelter_id': shelter_id
            })
        except Exception:
            continue
    return history

def load_shelters():
    shelters = {}
    for line in read_lines(SHELTERS_FILE):
        parts = line.split('|')
        if len(parts) != 5:
            continue
        try:
            shelter_id = int(parts[0])
            name = parts[1]
            address = parts[2]
            phone = parts[3]
            email = parts[4]
            shelters[shelter_id] = {
                'shelter_id': shelter_id,
                'name': name,
                'address': address,
                'phone': phone,
                'email': email
            }
        except Exception:
            continue
    return shelters

# Helper for next IDs

def get_next_pet_id(pets):
    if not pets:
        return 1
    return max(p['pet_id'] for p in pets) + 1

def get_next_application_id(applications):
    if not applications:
        return 1
    return max(a['application_id'] for a in applications) + 1

def get_next_message_id(messages):
    if not messages:
        return 1
    return max(m['message_id'] for m in messages) + 1

# 1. Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))

# 2. Dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    pets = load_pets()
    featured_pets = [
        {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description']
        }
        for pet in sorted(pets, key=lambda x: x['date_added'], reverse=True) if pet['status'] == 'Available'
    ][:5]

    applications = load_applications()
    adoption_history = load_adoption_history()
    recent_activities = []
    for application in sorted(applications, key=lambda x: x['date_submitted'], reverse=True)[:5]:
        recent_activities.append({'activity': f"Application submitted by {application['applicant_name']} for pet ID {application['pet_id']}"})
    for adoption in sorted(adoption_history, key=lambda x: x['adoption_date'], reverse=True)[:5]:
        recent_activities.append({'activity': f"Pet {adoption['pet_name']} was adopted by user {adoption['username']} on {adoption['adoption_date']}"})
    recent_activities = recent_activities[:10]

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

# 3. Pet Listings
@app.route('/pets', methods=['GET', 'POST'])
def pets_listing():
    pets = load_pets()
    filter_species = 'All'
    search_text = ''

    if request.method == 'POST':
        search_text = request.form.get('search_input', '').strip()
        filter_species = request.form.get('filter_species', 'All')
    else:
        search_text = request.args.get('search_input', '').strip() if request.args.get('search_input') else ''
        filter_species = request.args.get('filter_species', 'All')

    filtered_pets = []
    for pet in pets:
        if pet['status'] != 'Available':
            continue
        if filter_species != 'All' and pet['species'] != filter_species:
            continue
        s = search_text.lower()
        if s:
            if s not in pet['name'].lower() and s not in pet['breed'].lower() and s not in pet['description'].lower():
                continue
        filtered_pets.append(pet)

    return render_template('pets.html', pets=filtered_pets, filter_species=filter_species, search_text=search_text)

# 4. Pet Details
@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    pets = load_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if pet is None:
        abort(404)
    return render_template('pet_details.html', pet=pet)

# 5. Add Pet (Admin Only)
@app.route('/add-pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        pet_name = request.form.get('pet_name', '').strip()
        pet_species = request.form.get('pet_species', '').strip()
        pet_breed = request.form.get('pet_breed', '').strip()
        pet_age = request.form.get('pet_age', '').strip()
        pet_gender = request.form.get('pet_gender', '').strip()
        pet_size = request.form.get('pet_size', '').strip()
        pet_description = request.form.get('pet_description', '').strip()

        if not all([pet_name, pet_species, pet_breed, pet_age, pet_gender, pet_size, pet_description]):
            return render_template('add_pet.html')

        pets = load_pets()
        new_id = get_next_pet_id(pets)
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        new_pet = {
            'pet_id': new_id,
            'name': pet_name,
            'species': pet_species,
            'breed': pet_breed,
            'age': pet_age,
            'gender': pet_gender,
            'size': pet_size,
            'description': pet_description,
            'shelter_id': 1,
            'status': 'Available',
            'date_added': today_str
        }
        pets.append(new_pet)
        if not save_pets(pets):
            return render_template('add_pet.html')
        return redirect(url_for('pets_listing'))
    return render_template('add_pet.html')

# 6. Adoption Application
@app.route('/apply/<int:pet_id>', methods=['GET', 'POST'])
def submit_adoption_application(pet_id):
    pets = load_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if pet is None:
        abort(404)

    users = load_users()
    logged_in_username = None
    if users:
        logged_in_username = list(users.keys())[0]
    if logged_in_username is None:
        abort(403)

    user = users.get(logged_in_username)

    if request.method == 'POST':
        applicant_name = request.form.get('applicant_name', '').strip()
        applicant_phone = request.form.get('applicant_phone', '').strip()
        housing_type = request.form.get('housing_type', '').strip()
        reason = request.form.get('reason', '').strip()

        if not all([applicant_name, applicant_phone, housing_type, reason]):
            return render_template('application.html', pet=pet)

        applications = load_applications()
        new_id = get_next_application_id(applications)
        today_str = datetime.date.today().strftime('%Y-%m-%d')

        address = user.get('address', '')

        new_application = {
            'application_id': new_id,
            'username': logged_in_username,
            'pet_id': pet_id,
            'applicant_name': applicant_name,
            'phone': applicant_phone,
            'address': address,
            'housing_type': housing_type,
            'has_yard': '',
            'other_pets': '',
            'experience': '',
            'reason': reason,
            'status': 'Pending',
            'date_submitted': today_str
        }
        applications.append(new_application)
        if not save_applications(applications):
            return render_template('application.html', pet=pet)

        return redirect(url_for('my_applications'))
    return render_template('application.html', pet=pet)

# 7. My Applications
@app.route('/my-applications', methods=['GET'])
def my_applications():
    applications = load_applications()
    users = load_users()
    logged_in_username = None
    if users:
        logged_in_username = list(users.keys())[0]

    filter_status = 'All'
    if logged_in_username:
        user_apps = [a for a in applications if a['username'] == logged_in_username]
        filter_status = request.args.get('filter_status', 'All')
        if filter_status != 'All':
            user_apps = [a for a in user_apps if a['status'] == filter_status]
        applications_filtered = user_apps
    else:
        applications_filtered = []

    return render_template('my_applications.html', applications=applications_filtered, filter_status=filter_status)

# 8. Favorites
@app.route('/favorites', methods=['GET'])
def favorites():
    favorites = load_favorites()
    users = load_users()
    logged_in_username = None
    if users:
        logged_in_username = list(users.keys())[0]

    if not logged_in_username:
        favorites_filtered = []
    else:
        favorites_filtered = [f for f in favorites if f['username'] == logged_in_username]

    pets = load_pets()
    pets_map = {p['pet_id']: p for p in pets}

    favorites_with_petdata = []
    for fav in favorites_filtered:
        pet = pets_map.get(fav['pet_id'])
        if not pet:
            continue
        favorites_with_petdata.append({
            'username': fav['username'],
            'pet_id': fav['pet_id'],
            'date_added': fav['date_added'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'status': pet['status'],
            'date_added_pet': pet['date_added']
        })

    return render_template('favorites.html', favorites=favorites_with_petdata)

# 9. Messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages_data = load_messages()
    users = load_users()
    logged_in_username = None
    if users:
        logged_in_username = list(users.keys())[0]

    if not logged_in_username:
        conversations = []
    else:
        if request.method == 'POST':
            message_input = request.form.get('message_input', '').strip()
            recipient_username = request.form.get('recipient_username', '').strip()
            subject = request.form.get('subject', '').strip()

            if message_input and recipient_username and subject:
                new_id = get_next_message_id(messages_data)
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_message = {
                    'message_id': new_id,
                    'sender_username': logged_in_username,
                    'recipient_username': recipient_username,
                    'subject': subject,
                    'content': message_input,
                    'timestamp': timestamp,
                    'is_read': False
                }
                messages_data.append(new_message)
                save_messages(messages_data)

        # Compile conversations grouped by other user
        conversation_map = {}
        for m in messages_data:
            if m['sender_username'] == logged_in_username:
                other = m['recipient_username']
            elif m['recipient_username'] == logged_in_username:
                other = m['sender_username']
            else:
                continue
            key = tuple(sorted([logged_in_username, other]))
            conversation_map.setdefault(key, []).append(m)

        conversations = []
        for key, msgs in conversation_map.items():
            other_party = [u for u in key if u != logged_in_username][0]
            sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'])
            conversations.append({
                'with': other_party,
                'messages': sorted_msgs
            })

        conversations.sort(key=lambda c: c['messages'][-1]['timestamp'], reverse=True)

    return render_template('messages.html', conversations=conversations if logged_in_username else [])

# 10. User Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    logged_in_username = None
    if users:
        logged_in_username = list(users.keys())[0]
    if not logged_in_username:
        abort(403)

    user = users.get(logged_in_username)

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            user['email'] = email
            lines = []
            for u in users.values():
                line = '|'.join([
                    u.get('username', '').replace('|', ' '),
                    u.get('email', '').replace('|', ' '),
                    u.get('phone', '').replace('|', ' '),
                    u.get('address', '').replace('|', ' ')
                ])
                lines.append(line)
            write_lines(USERS_FILE, lines)
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

# 11. Admin Panel
@app.route('/admin', methods=['GET'])
def admin_panel():
    applications = load_applications()
    pending_applications = [a for a in applications if a['status'] == 'Pending']
    pets = load_pets()
    all_pets = pets
    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)

if __name__ == '__main__':
    app.run(debug=True)
