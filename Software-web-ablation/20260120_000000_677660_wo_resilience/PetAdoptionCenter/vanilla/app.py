from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for reading and writing data files

def read_users():
    users = []
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
    except FileNotFoundError:
        pass
    return users


def read_pets():
    pets = []
    try:
        with open(os.path.join(DATA_DIR, 'pets.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 11:
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
                    except ValueError:
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
        return True
    except Exception:
        return False


def read_applications():
    applications = []
    try:
        with open(os.path.join(DATA_DIR,'applications.txt'),'r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 13:
                    try:
                        application = {
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
                        applications.append(application)
                    except ValueError:
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
                if len(parts) == 3:
                    try:
                        favorite = {
                            'username': parts[0],
                            'pet_id': int(parts[1]),
                            'date_added': parts[2]
                        }
                        favorites.append(favorite)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return favorites


def read_messages():
    messages = []
    try:
        with open(os.path.join(DATA_DIR, 'messages.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 7:
                    try:
                        message = {
                            'message_id': int(parts[0]),
                            'sender_username': parts[1],
                            'recipient_username': parts[2],
                            'subject': parts[3],
                            'content': parts[4],
                            'timestamp': parts[5],
                            'is_read': parts[6].lower() == 'true'
                        }
                        messages.append(message)
                    except ValueError:
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
                    'true' if msg['is_read'] else 'false'
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
                if len(parts) == 6:
                    try:
                        item = {
                            'history_id': int(parts[0]),
                            'username': parts[1],
                            'pet_id': int(parts[2]),
                            'pet_name': parts[3],
                            'adoption_date': parts[4],
                            'shelter_id': int(parts[5])
                        }
                        history.append(item)
                    except ValueError:
                        continue
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
                if len(parts) == 5:
                    try:
                        shelter = {
                            'shelter_id': int(parts[0]),
                            'name': parts[1],
                            'address': parts[2],
                            'phone': parts[3],
                            'email': parts[4]
                        }
                        shelters.append(shelter)
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return shelters


def get_user(username):
    users = read_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

# For this simplified implementation, assume logged-in user is always 'john_doe'
LOGGED_IN_USERNAME = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    pets = read_pets()
    # featured_pets: up to 5 pets, status must be Available for dashboard
    featured_pets = []
    count = 0
    for pet in pets:
        if pet['status'] == 'Available':
            featured_pets.append({
                'id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
            })
            count += 1
            if count >= 5:
                break

    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets', methods=['GET', 'POST'])
def pet_listings():
    pets = read_pets()

    if request.method == 'POST':
        # Filter/sort based on POST data
        # Possible filters: species, search text (name)
        data = request.form
        filter_species = data.get('filter-species', '').strip()
        search_input = data.get('search-input', '').strip().lower()

        filtered_pets = []
        for pet in pets:
            if pet['status'] != 'Available':
                continue
            if filter_species and pet['species'].lower() != filter_species.lower():
                continue
            if search_input and search_input not in pet['name'].lower():
                continue
            filtered_pets.append(pet)

        pets_to_show = filtered_pets
    else:
        # GET show all available pets
        pets_to_show = [pet for pet in pets if pet['status'] == 'Available']

    pets_context = []
    for pet in pets_to_show:
        pets_context.append({
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        })
    return render_template('pet_listings.html', pets=pets_context)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break
    if pet is None:
        # Could handle 404 better, but just render page with no pet
        pet = {
            'id': pet_id,
            'name': '',
            'species': '',
            'description': '',
            'age': '',
            'gender': '',
            'size': '',
            'shelter_id': 0,
            'status': ''
        }
    else:
        pet = {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'description': pet['description'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'shelter_id': pet['shelter_id'],
            'status': pet['status']
        }
    return render_template('pet_details.html', pet=pet)


@app.route('/pets/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'GET':
        return render_template('add_pet.html')

    # POST method
    data = request.form
    required_fields = ['pet-name-input', 'pet-species-input', 'pet-breed-input', 'pet-age-input', 'pet-gender-input', 'pet-size-input', 'pet-description-input']
    for rf in required_fields:
        if rf not in data or not data[rf].strip():
            return render_template('add_pet.html', message=f"Error: Missing required field '{rf}'")

    # Prepare new pet data
    pets = read_pets()
    new_pet_id = 1
    if pets:
        new_pet_id = max(p['pet_id'] for p in pets) + 1

    pet_name = data['pet-name-input'].strip()
    pet_species = data['pet-species-input'].strip()
    pet_breed = data['pet-breed-input'].strip()
    pet_age = data['pet-age-input'].strip()
    pet_gender = data['pet-gender-input'].strip()
    pet_size = data['pet-size-input'].strip()
    pet_description = data['pet-description-input'].strip()

    # shelter_id set fixed as 1 for new pets (no admin input)
    shelter_id = 1
    status = 'Available'
    date_added = datetime.date.today().isoformat()

    new_pet = {
        'pet_id': new_pet_id,
        'name': pet_name,
        'species': pet_species,
        'breed': pet_breed,
        'age': pet_age,
        'gender': pet_gender,
        'size': pet_size,
        'description': pet_description,
        'shelter_id': shelter_id,
        'status': status,
        'date_added': date_added
    }
    pets.append(new_pet)
    if write_pets(pets):
        return render_template('add_pet.html', message='Pet added successfully!')
    else:
        return render_template('add_pet.html', message='Error: Failed to save pet data.')


@app.route('/applications/new/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = read_pets()
    pet_name = ''
    for pet in pets:
        if pet['pet_id'] == pet_id:
            pet_name = pet['name']
            break

    if request.method == 'GET':
        return render_template('adoption_application.html', pet_id=pet_id, pet_name=pet_name)

    # POST: submit adoption application
    data = request.form
    required_fields = ['applicant-name', 'applicant-phone', 'housing-type', 'reason']
    for rf in required_fields:
        if rf not in data or not data[rf].strip():
            return render_template('adoption_application.html', message=f"Error: Missing required field '{rf}'", pet_id=pet_id, pet_name=pet_name)

    # Gather applicant info
    applicant_name = data['applicant-name'].strip()
    applicant_phone = data['applicant-phone'].strip()
    housing_type = data['housing-type'].strip()
    reason = data['reason'].strip()

    # For address, assume from user's data
    user = get_user(LOGGED_IN_USERNAME)
    address = user['address'] if user else ''

    # Other app details defaults
    has_yard = 'Yes'
    other_pets = ''
    experience = ''

    applications = read_applications()
    new_application_id = 1
    if applications:
        new_application_id = max(a['application_id'] for a in applications) + 1

    today_str = datetime.date.today().isoformat()

    new_app = {
        'application_id': new_application_id,
        'username': LOGGED_IN_USERNAME,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': has_yard,
        'other_pets': other_pets,
        'experience': experience,
        'reason': reason,
        'status': 'Pending',
        'date_submitted': today_str
    }

    applications.append(new_app)
    if write_applications(applications):
        return render_template('adoption_application.html', message='Application submitted successfully!', pet_id=pet_id, pet_name=pet_name)
    else:
        return render_template('adoption_application.html', message='Error: Failed to save application.', pet_id=pet_id, pet_name=pet_name)


@app.route('/applications')
def my_applications():
    applications = read_applications()
    pets = read_pets()

    # Filter applications for logged-in user
    user_apps = [app for app in applications if app['username'] == LOGGED_IN_USERNAME]

    list_applications = []
    pet_id_to_name = {p['pet_id']: p['name'] for p in pets}
    for app in user_apps:
        list_applications.append({
            'application_id': app['application_id'],
            'pet_name': pet_id_to_name.get(app['pet_id'], ''),
            'date': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=list_applications)


@app.route('/favorites')
def favorites():
    favorites = read_favorites()
    pets = read_pets()

    user_favs = [fav for fav in favorites if fav['username'] == LOGGED_IN_USERNAME]

    pet_id_to_pet = {p['pet_id']: p for p in pets}

    favs_context = []
    for fav in user_favs:
        pet = pet_id_to_pet.get(fav['pet_id'])
        if pet:
            favs_context.append({
                'pet_id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
            })

    return render_template('favorites.html', favorites=favs_context)


@app.route('/messages')
def messages():
    messages_data = read_messages()

    # Show conversation overviews for logged-in user
    # Conversations are by recipient_username
    conversations_dict = {}

    for msg in messages_data:
        if msg['sender_username'] == LOGGED_IN_USERNAME:
            other = msg['recipient_username']
            key = other
            if key not in conversations_dict or conversations_dict[key]['timestamp'] < msg['timestamp']:
                conversations_dict[key] = {
                    'recipient_username': other,
                    'last_message': msg['content'],
                    'unread_count': 0
                }
        elif msg['recipient_username'] == LOGGED_IN_USERNAME:
            other = msg['sender_username']
            key = other
            # count unread
            unread = 0
            if not msg['is_read']:
                unread = 1
            if key not in conversations_dict:
                conversations_dict[key] = {
                    'recipient_username': other,
                    'last_message': msg['content'],
                    'unread_count': unread
                }
            else:
                # update last_message if this is newer
                if conversations_dict[key]['last_message'] != msg['content']:
                    # We want to update if this msg is newer
                    # messages data are not sorted; safer to compare timestamp strings
                    # Already checked above
                    pass
                # Increment unread_count
                conversations_dict[key]['unread_count'] += unread

    conversations = list(conversations_dict.values())

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    data = request.form
    message_content = data.get('message-input', '').strip() if 'message-input' in data else ''
    recipient_username = data.get('recipient-username', '').strip() if 'recipient-username' in data else ''

    if not message_content or not recipient_username:
        return render_template('messages.html', message='Error: Missing message content or recipient.')

    messages_list = read_messages()
    new_message_id = 1
    if messages_list:
        new_message_id = max(m['message_id'] for m in messages_list) + 1

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_message = {
        'message_id': new_message_id,
        'sender_username': LOGGED_IN_USERNAME,
        'recipient_username': recipient_username,
        'subject': '',
        'content': message_content,
        'timestamp': now_str,
        'is_read': False
    }

    messages_list.append(new_message)

    if write_messages(messages_list):
        return render_template('messages.html', message='Message sent successfully!')
    else:
        return render_template('messages.html', message='Error: Failed to send message.')


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    user = get_user(LOGGED_IN_USERNAME)
    if request.method == 'GET':
        if user:
            return render_template('profile.html', username=user['username'], email=user['email'])
        else:
            return render_template('profile.html', username=LOGGED_IN_USERNAME, email='')

    # POST to update profile
    data = request.form
    email = data.get('email', '').strip()
    if not email:
        return render_template('profile.html', message='Error: Email cannot be empty.', username=LOGGED_IN_USERNAME, email=email)

    # Update users.txt
    users = read_users()
    updated = False
    for u in users:
        if u['username'] == LOGGED_IN_USERNAME:
            u['email'] = email
            updated = True
            break
    if not updated:
        # Add new user with empty phone and address
        users.append({'username': LOGGED_IN_USERNAME, 'email': email, 'phone': '', 'address': ''})

    try:
        with open(os.path.join(DATA_DIR,'users.txt'), 'w', encoding='utf-8') as f:
            for u in users:
                line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
                f.write(line + '\n')
        return render_template('profile.html', message='Profile updated successfully!', username=LOGGED_IN_USERNAME, email=email)
    except Exception:
        return render_template('profile.html', message='Error: Failed to update profile.', username=LOGGED_IN_USERNAME, email=email)


@app.route('/admin')
def admin_panel():
    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = ''
            for pet in pets:
                if pet['pet_id'] == app['pet_id']:
                    pet_name = pet['name']
                    break
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


@app.route('/admin/applications/<int:application_id>/approve', methods=['POST'])
def approve_application(application_id):
    applications = read_applications()
    pets = read_pets()

    found_app = None
    for app in applications:
        if app['application_id'] == application_id:
            found_app = app
            break

    if not found_app:
        message = 'Application not found.'
    else:
        if found_app['status'] != 'Pending':
            message = 'Application is not pending.'
        else:
            found_app['status'] = 'Approved'
            # Update pet status to Adopted
            for pet in pets:
                if pet['pet_id'] == found_app['pet_id']:
                    pet['status'] = 'Adopted'
                    break

            # Update data files
            if write_applications(applications) and write_pets(pets):
                message = 'Application approved successfully.'
                # Add to adoption_history.txt
                history = read_adoption_history()
                new_history_id = 1
                if history:
                    new_history_id = max(h['history_id'] for h in history) + 1
                today_str = datetime.date.today().isoformat()
                history.append({
                    'history_id': new_history_id,
                    'username': found_app['username'],
                    'pet_id': found_app['pet_id'],
                    'pet_name': '',
                    'adoption_date': today_str,
                    'shelter_id': 0
                })
                # Fill pet_name and shelter_id from pets list
                pet_name = ''
                shelter_id = 0
                for pet in pets:
                    if pet['pet_id'] == found_app['pet_id']:
                        pet_name = pet['name']
                        shelter_id = pet['shelter_id']
                        break
                history[-1]['pet_name'] = pet_name
                history[-1]['shelter_id'] = shelter_id

                try:
                    with open(os.path.join(DATA_DIR, 'adoption_history.txt'), 'w', encoding='utf-8') as f:
                        for h in history:
                            line = '|'.join([
                                str(h['history_id']),
                                h['username'],
                                str(h['pet_id']),
                                h['pet_name'],
                                h['adoption_date'],
                                str(h['shelter_id'])
                            ])
                            f.write(line + '\n')
                except Exception:
                    # ignore error here
                    pass
            else:
                message = 'Failed to approve application due to file error.'

    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = ''
            for pet in pets:
                if pet['pet_id'] == app['pet_id']:
                    pet_name = pet['name']
                    break
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

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets, message=message)


@app.route('/admin/applications/<int:application_id>/reject', methods=['POST'])
def reject_application(application_id):
    applications = read_applications()

    found_app = None
    for app in applications:
        if app['application_id'] == application_id:
            found_app = app
            break

    if not found_app:
        message = 'Application not found.'
    else:
        if found_app['status'] != 'Pending':
            message = 'Application is not pending.'
        else:
            found_app['status'] = 'Rejected'
            if write_applications(applications):
                message = 'Application rejected successfully.'
            else:
                message = 'Failed to reject application due to file error.'

    applications = read_applications()
    pets = read_pets()

    pending_applications = []
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = ''
            for pet in pets:
                if pet['pet_id'] == app['pet_id']:
                    pet_name = pet['name']
                    break
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

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets, message=message)


@app.route('/admin/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pets = read_pets()
    pet = None
    for p in pets:
        if p['pet_id'] == pet_id:
            pet = p
            break

    if pet is None:
        return render_template('add_pet.html', message='Pet not found.')

    if request.method == 'GET':
        pet_dict = {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'shelter_id': pet['shelter_id'],
            'status': pet['status']
        }
        return render_template('add_pet.html', pet=pet_dict)

    # POST update pet
    data = request.form
    required_fields = ['pet-name-input', 'pet-species-input', 'pet-breed-input', 'pet-age-input', 'pet-gender-input', 'pet-size-input', 'pet-description-input']
    for rf in required_fields:
        if rf not in data or not data[rf].strip():
            pet_dict = {
                'id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'breed': pet['breed'],
                'age': pet['age'],
                'gender': pet['gender'],
                'size': pet['size'],
                'description': pet['description'],
                'shelter_id': pet['shelter_id'],
                'status': pet['status']
            }
            return render_template('add_pet.html', message=f"Error: Missing required field '{rf}'", pet=pet_dict)

    # Update pet info
    pet['name'] = data['pet-name-input'].strip()
    pet['species'] = data['pet-species-input'].strip()
    pet['breed'] = data['pet-breed-input'].strip()
    pet['age'] = data['pet-age-input'].strip()
    pet['gender'] = data['pet-gender-input'].strip()
    pet['size'] = data['pet-size-input'].strip()
    pet['description'] = data['pet-description-input'].strip()
    # shelter_id and status are not updated here

    if write_pets(pets):
        pet_dict = {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'shelter_id': pet['shelter_id'],
            'status': pet['status']
        }
        return render_template('add_pet.html', message='Pet updated successfully!', pet=pet_dict)
    else:
        pet_dict = {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'breed': pet['breed'],
            'age': pet['age'],
            'gender': pet['gender'],
            'size': pet['size'],
            'description': pet['description'],
            'shelter_id': pet['shelter_id'],
            'status': pet['status']
        }
        return render_template('add_pet.html', message='Error: Failed to save pet data.', pet=pet_dict)


@app.route('/admin/pets/<int:pet_id>/delete', methods=['POST'])
def delete_pet(pet_id):
    pets = read_pets()
    pets_new = [p for p in pets if p['pet_id'] != pet_id]

    if len(pets_new) == len(pets):
        message = 'Pet not found.'
    else:
        # Delete pet and update file
        if write_pets(pets_new):
            message = 'Pet deleted successfully.'
        else:
            message = 'Error: Failed to delete pet.'

    applications = read_applications()
    pending_applications = []
    pets = read_pets()
    for app in applications:
        if app['status'] == 'Pending':
            pet_name = ''
            for pet in pets:
                if pet['pet_id'] == app['pet_id']:
                    pet_name = pet['name']
                    break
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

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets, message=message)


if __name__ == '__main__':
    app.run(debug=True)
