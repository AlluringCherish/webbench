from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for data handling

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, address = parts
                users.append({
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                })
    except FileNotFoundError:
        pass
    return users


def write_users(users):
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
            for user in users:
                line = '|'.join([
                    user.get('username',''),
                    user.get('email',''),
                    user.get('phone',''),
                    user.get('address','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_pets():
    pets = []
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 11:
                    continue
                pet_id_s, name, species, breed, age, gender, size, description, shelter_id_s, status, date_added = parts
                try:
                    pet_id = int(pet_id_s)
                    shelter_id = int(shelter_id_s)
                except ValueError:
                    continue
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
    except FileNotFoundError:
        pass
    return pets


def write_pets(pets):
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'w', encoding='utf-8') as f:
            for pet in pets:
                line = '|'.join([
                    str(pet.get('pet_id','')),
                    pet.get('name',''),
                    pet.get('species',''),
                    pet.get('breed',''),
                    pet.get('age',''),
                    pet.get('gender',''),
                    pet.get('size',''),
                    pet.get('description',''),
                    str(pet.get('shelter_id','')),
                    pet.get('status',''),
                    pet.get('date_added','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 13:
                    continue
                (application_id_s, username, pet_id_s, applicant_name, phone, address,
                 housing_type, has_yard, other_pets, experience, reason, status, date_submitted) = parts
                try:
                    application_id = int(application_id_s)
                    pet_id = int(pet_id_s)
                except ValueError:
                    continue
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
    except FileNotFoundError:
        pass
    return applications


def write_applications(applications):
    try:
        with open(os.path.join(DATA_DIR, 'applications.txt'), 'w', encoding='utf-8') as f:
            for app in applications:
                line = '|'.join([
                    str(app.get('application_id','')),
                    app.get('username',''),
                    str(app.get('pet_id','')),
                    app.get('applicant_name',''),
                    app.get('phone',''),
                    app.get('address',''),
                    app.get('housing_type',''),
                    app.get('has_yard',''),
                    app.get('other_pets',''),
                    app.get('experience',''),
                    app.get('reason',''),
                    app.get('status',''),
                    app.get('date_submitted','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                username, pet_id_s, date_added = parts
                try:
                    pet_id = int(pet_id_s)
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


def write_favorites(favorites):
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    fav.get('username',''),
                    str(fav.get('pet_id','')),
                    fav.get('date_added','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_messages():
    messages = []
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
                message_id_s, sender_username, recipient_username, subject, content, timestamp, is_read_str = parts
                try:
                    message_id = int(message_id_s)
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


def write_messages(messages):
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'w', encoding='utf-8') as f:
            for msg in messages:
                line = '|'.join([
                    str(msg.get('message_id','')),
                    msg.get('sender_username',''),
                    msg.get('recipient_username',''),
                    msg.get('subject',''),
                    msg.get('content',''),
                    msg.get('timestamp',''),
                    'true' if msg.get('is_read',False) else 'false'
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def read_adoption_history():
    history = []
    try:
        with open(os.path.join(DATA_DIR, 'adoption_history.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                history_id_s, username, pet_id_s, pet_name, adoption_date, shelter_id_s = parts
                try:
                    history_id = int(history_id_s)
                    pet_id = int(pet_id_s)
                    shelter_id = int(shelter_id_s)
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


def read_shelters():
    shelters = []
    try:
        with open(os.path.join(DATA_DIR, 'shelters.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                shelter_id_s, name, address, phone, email = parts
                try:
                    shelter_id = int(shelter_id_s)
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


# We'll simulate a current user for simplicity
# Since no authentication spec is provided, assume current user is 'john_doe'
CURRENT_USERNAME = 'john_doe'

# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    pets = read_pets()
    # Prepare featured_pets: list of dicts with: pet_id(int), name(str), species(str), age(str)
    featured_pets = []
    for pet in pets:
        if pet['status'] == 'Available':
            featured_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })
    
    # Only show up to 6 featured pets on dashboard
    featured_pets = featured_pets[:6]
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = read_pets()
    # Prepare pets list with pet_id(int), name(str), species(str), age(str), photo_url(optional, not in data so omit)
    pets_list = []
    for pet in pets:
        pets_list.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            # Photo_url optional for frontend and not in data,
            # so not included here
        })
    return render_template('pet_listings.html', pets=pets_list)


@app.route('/pets', methods=['POST'])
def pet_listings_filter():
    species_filter = request.form.get('filter-species', '').strip()
    search_input = request.form.get('search-input', '').strip().lower()
    pets = read_pets()
    filtered_pets = []

    for pet in pets:
        # Only list pets with status 'Available'
        if pet['status'] != 'Available':
            continue

        matches_species = True
        if species_filter and species_filter.lower() != 'all':
            matches_species = (pet['species'].lower() == species_filter.lower())

        matches_search = True
        if search_input:
            # Match pet name or breed substring (case insensitive)
            if search_input not in pet['name'].lower() and search_input not in pet['breed'].lower():
                matches_search = False

        if matches_species and matches_search:
            filtered_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })

    return render_template('pet_listings.html', pets=filtered_pets)


@app.route('/pets/<int:pet_id>', methods=['GET'])
def pet_details(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = {
                'pet_id': p['pet_id'],
                'name': p['name'],
                'species': p['species'],
                'description': p['description']
            }
            break
    if not pet:
        # Pet not found, redirect to pet listings
        return redirect(url_for('pet_listings'))

    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET'])
def add_pet():
    return render_template('add_pet.html')


@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    # Expect form with fields: pet-name-input, pet-species-input, pet-breed-input, pet-age-input, pet-gender-input, pet-size-input, pet-description-input
    pet_name = request.form.get('pet-name-input', '').strip()
    pet_species = request.form.get('pet-species-input', '').strip()
    pet_breed = request.form.get('pet-breed-input', '').strip()
    pet_age = request.form.get('pet-age-input', '').strip()
    pet_gender = request.form.get('pet-gender-input', '').strip()
    pet_size = request.form.get('pet-size-input', '').strip()
    pet_description = request.form.get('pet-description-input', '').strip()

    if not (pet_name and pet_species and pet_breed and pet_age and pet_gender and pet_size and pet_description):
        error_message = 'All fields are required.'
        return render_template('add_pet.html', error_message=error_message)

    pets = read_pets()
    max_id = max((pet['pet_id'] for pet in pets), default=0)
    new_pet_id = max_id + 1

    # For new pets, assign shelter_id = 1 as default and status Available, date_added today
    new_pet = {
        'pet_id': new_pet_id,
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

    pets.append(new_pet)
    if write_pets(pets):
        success_message = 'New pet added successfully.'
        return render_template('add_pet.html', success_message=success_message)
    else:
        error_message = 'Failed to add pet due to a server error.'
        return render_template('add_pet.html', error_message=error_message)


@app.route('/applications/adopt/<int:pet_id>', methods=['GET'])
def adoption_application_form(pet_id):
    # Just pass pet_id to template
    return render_template('application.html', pet_id=pet_id)


@app.route('/applications/adopt/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    # Expect form fields: applicant-name, applicant-phone, housing-type, reason
    applicant_name = request.form.get('applicant-name', '').strip()
    applicant_phone = request.form.get('applicant-phone', '').strip()
    housing_type = request.form.get('housing-type', '').strip()
    reason = request.form.get('reason', '').strip()

    if not (applicant_name and applicant_phone and housing_type and reason):
        error_message = 'All fields are required.'
        return render_template('application.html', pet_id=pet_id, error_message=error_message)

    # Load current user info for address (from users.txt)
    users = read_users()
    current_user = None
    for user in users:
        if user['username'] == CURRENT_USERNAME:
            current_user = user
            break
    if not current_user:
        error_message = 'Current user information not found.'
        return render_template('application.html', pet_id=pet_id, error_message=error_message)

    applications = read_applications()
    max_id = max((app['application_id'] for app in applications), default=0)
    new_app_id = max_id + 1

    # Additional fields not present in form are set to defaults
    has_yard = 'No'
    other_pets = 'None'
    experience = 'None'

    new_application = {
        'application_id': new_app_id,
        'username': CURRENT_USERNAME,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': current_user.get('address',''),
        'housing_type': housing_type,
        'has_yard': has_yard,
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }

    applications.append(new_application)
    if write_applications(applications):
        success_message = 'Adoption application submitted successfully.'
        return render_template('application.html', pet_id=pet_id, success_message=success_message)
    else:
        error_message = 'Failed to submit application due to a server error.'
        return render_template('application.html', pet_id=pet_id, error_message=error_message)


@app.route('/applications/my', methods=['GET'])
def my_applications():
    applications = read_applications()
    pets = read_pets()

    # Filter applications for current user
    user_apps = [app for app in applications if app['username'] == CURRENT_USERNAME]
    # For each app: application_id(int), pet_name(str), date_submitted(str), status(str)
    applications_list = []
    pet_id_to_name = {p['pet_id']: p['name'] for p in pets}
    for app in user_apps:
        pet_name = pet_id_to_name.get(app['pet_id'], 'Unknown')
        applications_list.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=applications_list)


@app.route('/favorites', methods=['GET'])
def favorites():
    favorites = read_favorites()
    pets = read_pets()

    user_favorites = [fav for fav in favorites if fav['username'] == CURRENT_USERNAME]
    pet_id_to_pet = {p['pet_id']: p for p in pets}

    favorite_pets = []
    for fav in user_favorites:
        pet = pet_id_to_pet.get(fav['pet_id'])
        if pet and pet['status'] == 'Available':
            favorite_pets.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age']
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages', methods=['GET'])
def messages():
    messages = read_messages()
    users = read_users()

    # Group messages into conversations by unique participant pairs (sender and recipient)
    # Each conversation: conversation_id(int), participants(list of str), last_message(str)
    # conversation_id: assigned as incremental based on sorted participant pair

    # To simplify, group by participant pairs (sorted tuple), find last message by timestamp

    conv_dict = {}
    for msg in messages:
        participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
        if participants not in conv_dict:
            conv_dict[participants] = []
        conv_dict[participants].append(msg)

    conversations = []
    conv_id_counter = 1
    for participants, msgs in conv_dict.items():
        # Sort messages by timestamp descending
        sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
        last_msg = sorted_msgs[0]
        conversations.append({
            'conversation_id': conv_id_counter,
            'participants': list(participants),
            'last_message': last_msg['content']
        })
        conv_id_counter += 1

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    # Expect form fields: recipient_username, subject, content
    recipient_username = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not (recipient_username and subject and content):
        error_message = 'All fields are required to send a message.'
        conversations = []
        messages = read_messages()
        conv_dict = {}
        for msg in messages:
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conv_dict:
                conv_dict[participants] = []
            conv_dict[participants].append(msg)

        conv_list = []
        conv_id_counter = 1
        for participants, msgs in conv_dict.items():
            sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
            last_msg = sorted_msgs[0]
            conv_list.append({
                'conversation_id': conv_id_counter,
                'participants': list(participants),
                'last_message': last_msg['content']
            })
            conv_id_counter += 1

        return render_template('messages.html', conversations=conv_list, error_message=error_message)

    # Check recipient exists
    users = read_users()
    recipient_exists = any(u['username'] == recipient_username for u in users)
    if not recipient_exists:
        error_message = f'Recipient user "{recipient_username}" does not exist.'
        
        messages = read_messages()
        conv_dict = {}
        for msg in messages:
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conv_dict:
                conv_dict[participants] = []
            conv_dict[participants].append(msg)

        conv_list = []
        conv_id_counter = 1
        for participants, msgs in conv_dict.items():
            sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
            last_msg = sorted_msgs[0]
            conv_list.append({
                'conversation_id': conv_id_counter,
                'participants': list(participants),
                'last_message': last_msg['content']
            })
            conv_id_counter += 1

        return render_template('messages.html', conversations=conv_list, error_message=error_message)

    # Append new message
    messages = read_messages()
    max_message_id = max((m['message_id'] for m in messages), default=0)
    new_message_id = max_message_id + 1

    new_message = {
        'message_id': new_message_id,
        'sender_username': CURRENT_USERNAME,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': False
    }

    messages.append(new_message)
    if write_messages(messages):
        success_message = 'Message sent successfully.'

        # Refresh conversations list
        conv_dict = {}
        for msg in messages:
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conv_dict:
                conv_dict[participants] = []
            conv_dict[participants].append(msg)

        conv_list = []
        conv_id_counter = 1
        for participants, msgs in conv_dict.items():
            sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
            last_msg = sorted_msgs[0]
            conv_list.append({
                'conversation_id': conv_id_counter,
                'participants': list(participants),
                'last_message': last_msg['content']
            })
            conv_id_counter += 1

        return render_template('messages.html', conversations=conv_list, success_message=success_message)
    else:
        error_message = 'Failed to send message due to a server error.'
        conv_dict = {}
        for msg in messages:
            participants = tuple(sorted([msg['sender_username'], msg['recipient_username']]))
            if participants not in conv_dict:
                conv_dict[participants] = []
            conv_dict[participants].append(msg)

        conv_list = []
        conv_id_counter = 1
        for participants, msgs in conv_dict.items():
            sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
            last_msg = sorted_msgs[0]
            conv_list.append({
                'conversation_id': conv_id_counter,
                'participants': list(participants),
                'last_message': last_msg['content']
            })
            conv_id_counter += 1

        return render_template('messages.html', conversations=conv_list, error_message=error_message)


@app.route('/profile', methods=['GET'])
def user_profile():
    users = read_users()
    current_user = None
    for user in users:
        if user['username'] == CURRENT_USERNAME:
            current_user = user
            break
    if not current_user:
        # User not found, redirect to dashboard
        return redirect(url_for('dashboard'))

    username = current_user['username']
    email = current_user['email']
    return render_template('profile.html', username=username, email=email)


@app.route('/profile', methods=['POST'])
def update_profile():
    email = request.form.get('profile-email', '').strip()

    if not email:
        error_message = 'Email address is required.'
        # Provide current username and email for template
        users = read_users()
        current_user = None
        for user in users:
            if user['username'] == CURRENT_USERNAME:
                current_user = user
                break
        if current_user:
            return render_template('profile.html', username=current_user['username'], email=current_user['email'], error_message=error_message)
        else:
            return redirect(url_for('dashboard'))

    # Update user email
    users = read_users()
    updated = False
    for user in users:
        if user['username'] == CURRENT_USERNAME:
            user['email'] = email
            updated = True
            break

    if updated and write_users(users):
        success_message = 'Profile updated successfully.'
        return render_template('profile.html', username=CURRENT_USERNAME, email=email, success_message=success_message)
    else:
        error_message = 'Failed to update profile due to a server error.'
        return render_template('profile.html', username=CURRENT_USERNAME, email=email, error_message=error_message)


@app.route('/admin', methods=['GET'])
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    # pending_applications: list of dicts (application_id:int, applicant_name:str, pet_name:str)
    # only those with status 'Pending'
    pet_id_to_name = {p['pet_id']: p['name'] for p in pets}

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = pet_id_to_name.get(app['pet_id'], 'Unknown')
            pending_applications.append({
                'application_id': app['application_id'],
                'applicant_name': app['applicant_name'],
                'pet_name': pet_name
            })

    # all_pets: list of dicts (pet_id:int, name:str, species:str, status:str)
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
    app.run(debug=True)
