from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for data loading and saving

# ========== Users ==========
# users.txt fields: username|email|phone|address

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, address = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address,
                }
    except FileNotFoundError:
        pass
    return users

# ========== Pets ==========
# pets.txt fields: pet_id|name|species|breed|age|gender|size|description|shelter_id|status|date_added


def load_pets():
    pets = []
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                pet_id_str, name, species, breed, age, gender, size, description, shelter_id_str, status, date_added = parts
                try:
                    pet_id = int(pet_id_str)
                    shelter_id = int(shelter_id_str)
                except ValueError:
                    continue
                pet = {
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
                pets.append(pet)
    except FileNotFoundError:
        pass
    return pets

def save_pets(pets):
    lines = []
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
        lines.append(line)
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        return True
    except Exception:
        return False

# ========== Applications ==========
# applications.txt fields:
# application_id|username|pet_id|applicant_name|phone|address|housing_type|has_yard|other_pets|experience|reason|status|date_submitted

def load_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 13:
                    continue
                (application_id_str, username, pet_id_str, applicant_name, phone, address, housing_type, has_yard,
                 other_pets, experience, reason, status, date_submitted) = parts
                try:
                    application_id = int(application_id_str)
                    pet_id = int(pet_id_str)
                except ValueError:
                    continue
                application = {
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
                applications.append(application)
    except FileNotFoundError:
        pass
    return applications

def save_applications(applications):
    lines = []
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
        lines.append(line)
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        return True
    except Exception:
        return False

# ========== Favorites ==========
# favorites.txt fields: username|pet_id|date_added

def load_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
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
    except FileNotFoundError:
        pass
    return favorites

# ========== Messages ==========
# messages.txt fields:
# message_id|sender_username|recipient_username|subject|content|timestamp|is_read

def load_messages():
    messages = []
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                (message_id_str, sender_username, recipient_username, subject, content, timestamp, is_read_str) = parts
                try:
                    message_id = int(message_id_str)
                except ValueError:
                    continue
                is_read = True if is_read_str.lower() == 'true' else False
                messages.append({
                    'message_id': message_id,
                    'sender_username': sender_username,
                    'recipient_username': recipient_username,
                    'subject': subject,
                    'content': content,
                    'timestamp': timestamp,
                    'is_read': is_read
                })
    except FileNotFoundError:
        pass
    return messages

def save_messages(messages):
    lines = []
    for m in messages:
        line = '|'.join([
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            'true' if m['is_read'] else 'false'
        ])
        lines.append(line)
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        return True
    except Exception:
        return False

# ========== Adoption History ==========
# adoption_history.txt fields:
# history_id|username|pet_id|pet_name|adoption_date|shelter_id

def load_adoption_history():
    history = []
    try:
        with open(os.path.join(DATA_DIR, 'adoption_history.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                history_id_str, username, pet_id_str, pet_name, adoption_date, shelter_id_str = parts
                try:
                    history_id = int(history_id_str)
                    pet_id = int(pet_id_str)
                    shelter_id = int(shelter_id_str)
                except ValueError:
                    continue
                history.append({
                    'history_id': history_id,
                    'username': username,
                    'pet_id': pet_id,
                    'pet_name': pet_name,
                    'adoption_date': adoption_date,
                    'shelter_id': shelter_id
                })
    except FileNotFoundError:
        pass
    return history

# ========== Shelters ==========
# shelters.txt fields:
# shelter_id|name|address|phone|email

def load_shelters():
    shelters = []
    try:
        with open(os.path.join(DATA_DIR, 'shelters.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                shelter_id_str, name, address, phone, email = parts
                try:
                    shelter_id = int(shelter_id_str)
                except ValueError:
                    continue
                shelters.append({
                    'shelter_id': shelter_id,
                    'name': name,
                    'address': address,
                    'phone': phone,
                    'email': email
                })
    except FileNotFoundError:
        pass
    return shelters

# ========== USER SESSION SIMULATION ==========
# For this backend, we simulate a logged in user as 'john_doe'
# In real app, proper session and authentication would be used

CURRENT_USERNAME = 'john_doe'

# ========== ROUTES ==========

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    # featured_pets - select up to, e.g., 5 available pets
    featured_pets = []
    for pet in pets:
        if pet['status'] == 'Available':
            pet_dict = {
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            }
            # Optional photo_url not in schema - skip if none
            # No photo_url field present in data, so omit
            featured_pets.append(pet_dict)
            if len(featured_pets) >= 5:
                break

    # recent_activities: not clearly defined in spec; leave empty list
    recent_activities = []

    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

@app.route('/pets')
def pet_listings():
    pets = load_pets()
    filter_species = request.args.get('species', '').strip()
    filtered_pets = []
    for pet in pets:
        if filter_species and pet['species'].lower() != filter_species.lower():
            continue
        pet_dict = {
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age']
        }
        # Optional photo_url - not in data - omit
        filtered_pets.append(pet_dict)

    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species)

@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    # Pass pet exactly as per context var
    return render_template('pet_details.html', pet=pet)

@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'GET':
        return render_template('add_pet.html')

    form_errors = {}
    name = request.form.get('name', '').strip()
    species = request.form.get('species', '').strip()
    breed = request.form.get('breed', '').strip()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    size = request.form.get('size', '').strip()
    description = request.form.get('description', '').strip()

    # Validate required fields
    if not name:
        form_errors['name'] = 'Name is required.'
    if not species:
        form_errors['species'] = 'Species is required.'
    if not breed:
        form_errors['breed'] = 'Breed is required.'
    if not age:
        form_errors['age'] = 'Age is required.'
    if not gender:
        form_errors['gender'] = 'Gender is required.'
    if not size:
        form_errors['size'] = 'Size is required.'
    if not description:
        form_errors['description'] = 'Description is required.'

    if form_errors:
        return render_template('add_pet.html', form_errors=form_errors)

    pets = load_pets()
    # Generate new pet_id as max+1
    max_id = max((pet['pet_id'] for pet in pets), default=0)
    new_pet_id = max_id + 1

    # For shelter_id, assign 1 by default since no user info or form provides shelter
    shelter_id = 1
    date_added = datetime.now().strftime('%Y-%m-%d')
    status = 'Available'

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
    if not save_pets(pets):
        form_errors['save'] = 'Failed to save pet data.'
        return render_template('add_pet.html', form_errors=form_errors)

    return redirect(url_for('pet_details', pet_id=new_pet_id))

@app.route('/applications/<int:pet_id>/apply', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if request.method == 'GET':
        return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']})

    # POST
    application_errors = {}
    applicant_name = request.form.get('applicant_name', '').strip()
    phone = request.form.get('phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    # Extra fields according to spec:
    # phone provided, housing_type provided, reason provided.
    # Also need: has_yard, other_pets, experience, address - from user data

    # Validate
    if not applicant_name:
        application_errors['applicant_name'] = 'Applicant name is required.'
    if not phone:
        application_errors['phone'] = 'Phone is required.'
    if not housing_type:
        application_errors['housing_type'] = 'Housing type is required.'
    if not reason:
        application_errors['reason'] = 'Reason is required.'

    if application_errors:
        return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']}, application_errors=application_errors)

    # Additional form fields, default blank if omitted
    has_yard = request.form.get('has_yard', '').strip() or 'No'
    other_pets = request.form.get('other_pets', '').strip() or 'None'
    experience = request.form.get('experience', '').strip() or ''

    users = load_users()
    user = users.get(CURRENT_USERNAME, None)
    address = user['address'] if user else ''

    applications = load_applications()
    max_id = max((app['application_id'] for app in applications), default=0)
    new_application_id = max_id + 1

    date_submitted = datetime.now().strftime('%Y-%m-%d')
    new_app = {
        'application_id': new_application_id,
        'username': CURRENT_USERNAME,
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
        'date_submitted': date_submitted
    }

    applications.append(new_app)
    if not save_applications(applications):
        application_errors['save'] = 'Failed to save application.'
        return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']}, application_errors=application_errors)

    return redirect(url_for('my_applications'))

@app.route('/my_applications')
def my_applications():
    applications = load_applications()
    pets = load_pets()
    filter_status = request.args.get('status', '').strip()

    # Map pet_id to pet_name
    pet_map = {p['pet_id']: p['name'] for p in pets}

    filtered_apps = []
    for app in applications:
        if filter_status and app['status'].lower() != filter_status.lower():
            continue
        pet_name = pet_map.get(app['pet_id'], 'Unknown')
        filtered_apps.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=filtered_apps, filter_status=filter_status)

@app.route('/favorites')
def favorites():
    favorites = load_favorites()
    pets = load_pets()

    # Filter favorites by current user
    user_favs = [f for f in favorites if f['username'] == CURRENT_USERNAME]

    # Map pet_id to pet info
    pet_map = {p['pet_id']: p for p in pets}

    fav_list = []
    for fav in user_favs:
        pet = pet_map.get(fav['pet_id'])
        if pet:
            pet_dict = {
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            }
            # Optional photo_url omitted
            fav_list.append(pet_dict)

    return render_template('favorites.html', favorites=fav_list)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    users = load_users()
    messages = load_messages()

    # Build conversations with other users
    conversations = {}

    # Filter messages involving current user
    relevant_messages = [m for m in messages if m['sender_username'] == CURRENT_USERNAME or m['recipient_username'] == CURRENT_USERNAME]

    # Map by other user, find last_message, unread count (messages to current user not read)
    for m in relevant_messages:
        if m['sender_username'] == CURRENT_USERNAME:
            other_user = m['recipient_username']
        else:
            other_user = m['sender_username']
        conv = conversations.get(other_user, {
            'conversation_id': None,  # no ID in data, so assign None
            'other_user': other_user,
            'last_message': '',
            'unread_count': 0
        })
        # Update last message if this is newer
        try:
            current_last = datetime.strptime(conv['last_message'][:19], '%Y-%m-%d %H:%M:%S') if conv['last_message'] else None
            message_time = datetime.strptime(m['timestamp'][:19], '%Y-%m-%d %H:%M:%S')
            if not current_last or message_time > current_last:
                conv['last_message'] = m['content']
        except Exception:
            if not conv['last_message']:
                conv['last_message'] = m['content']

        # Count unread messages to current user
        if m['recipient_username'] == CURRENT_USERNAME and not m['is_read']:
            conv['unread_count'] += 1

        conversations[other_user] = conv

    conversation_list = list(conversations.values())

    # For simplicity, show all messages between current user and others
    # Sort messages by timestamp asc
    messages_sorted = sorted(relevant_messages, key=lambda m: m['timestamp'])

    if request.method == 'POST':
        # Send a new message
        recipient = request.form.get('recipient', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        if not recipient or recipient == CURRENT_USERNAME or recipient not in users:
            return "Invalid recipient", 400
        if not subject:
            return "Subject required", 400
        if not content:
            return "Content required", 400

        max_id = max((m['message_id'] for m in messages), default=0)
        new_id = max_id + 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_message = {
            'message_id': new_id,
            'sender_username': CURRENT_USERNAME,
            'recipient_username': recipient,
            'subject': subject,
            'content': content,
            'timestamp': timestamp,
            'is_read': False
        }
        messages.append(new_message)
        if not save_messages(messages):
            return "Failed to save message", 500

        return redirect(url_for('messages'))

    return render_template('messages.html', conversations=conversation_list, messages=messages_sorted)

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME)
    profile_update_errors = {}

    if request.method == 'GET':
        if not user:
            return "User not found", 404
        return render_template('profile.html', user={'username': user['username'], 'email': user['email']})

    # POST
    email = request.form.get('email', '').strip()

    if not email:
        profile_update_errors['email'] = 'Email is required.'

    if profile_update_errors:
        return render_template('profile.html', user={'username': user['username'] if user else '', 'email': email}, profile_update_errors=profile_update_errors)

    # Update the email of user
    if user:
        user['email'] = email
        # Write back all users
        try:
            lines = []
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
                lines.append(line)
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')
        except Exception:
            profile_update_errors['save'] = 'Failed to save user profile.'
            return render_template('profile.html', user=user, profile_update_errors=profile_update_errors)

    return redirect(url_for('user_profile'))

@app.route('/admin')
def admin_panel():
    applications = load_applications()
    users = load_users()
    pets = load_pets()

    # pending_applications with status Pending
    pending_applications = []
    pet_map = {p['pet_id']: p['name'] for p in pets}

    for app in applications:
        if app['status'] == 'Pending':
            applicant = users.get(app['username'], None)
            applicant_name = app['applicant_name']
            pet_name = pet_map.get(app['pet_id'], 'Unknown')
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': applicant_name,
                'pet_name': pet_name,
                'date_submitted': app['date_submitted'],
                'status': app['status']
            })

    all_pets = []
    for pet in pets:
        all_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'status': pet['status']
        })

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
