from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for loading and saving data files

def load_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        user = {
                            'username': parts[0],
                            'email': parts[1],
                            'phone': parts[2],
                            'address': parts[3]
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


def load_pets():
    pets = []
    path = os.path.join(DATA_DIR, 'pets.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 11:
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
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 13:
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
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        favorite = {
                            'username': parts[0],
                            'pet_id': int(parts[1]),
                            'date_added': parts[2]
                        }
                        favorites.append(favorite)
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
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
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


def load_adoption_history():
    history = []
    path = os.path.join(DATA_DIR, 'adoption_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        record = {
                            'history_id': int(parts[0]),
                            'username': parts[1],
                            'pet_id': int(parts[2]),
                            'pet_name': parts[3],
                            'adoption_date': parts[4],
                            'shelter_id': int(parts[5])
                        }
                        history.append(record)
    return history


def load_shelters():
    shelters = []
    path = os.path.join(DATA_DIR, 'shelters.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 5:
                        shelter = {
                            'shelter_id': int(parts[0]),
                            'name': parts[1],
                            'address': parts[2],
                            'phone': parts[3],
                            'email': parts[4]
                        }
                        shelters.append(shelter)
    return shelters

def get_user(username):
    users = load_users()
    for u in users:
        if u['username'] == username:
            return u
    return None


def get_pet_by_id(pet_id):
    pets = load_pets()
    for pet in pets:
        if pet['pet_id'] == pet_id:
            return pet
    return None


def get_shelter_by_id(shelter_id):
    shelters = load_shelters()
    for shelter in shelters:
        if shelter['shelter_id'] == shelter_id:
            return shelter
    return None


# The following routes assume a hardcoded current user for simplicity, as no login system is specified.
CURRENT_USERNAME = 'john_doe'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    pets = load_pets()
    # Prepare featured_pets: up to 5 pets with status 'Available' sorted by date_added descending
    available_pets = [pet for pet in pets if pet['status'] == 'Available']
    # Sort by date_added descending
    available_pets.sort(key=lambda p: p['date_added'], reverse=True)
    featured_pets = available_pets[:5]

    # Format pets for featured_pets context with limited keys
    fp_context = [
        {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"  # Assuming photo naming convention
        }
        for pet in featured_pets
    ]

    # Gather recent activities - e.g. recent adoptions and recent applications (summary strings)
    recent_activities = []

    # Recent adoptions
    adoption_history = load_adoption_history()
    adoption_history.sort(key=lambda h: h['adoption_date'], reverse=True)
    for rec in adoption_history[:5]:
        recent_activities.append(f"{rec['pet_name']} was adopted by {rec['username']} on {rec['adoption_date']}")

    # Recent applications
    applications = load_applications()
    applications.sort(key=lambda a: a['date_submitted'], reverse=True)
    for app in applications[:5]:
        recent_activities.append(f"{app['applicant_name']} applied to adopt {get_pet_by_id(app['pet_id'])['name']} on {app['date_submitted']}")

    return render_template('dashboard.html', featured_pets=fp_context, recent_activities=recent_activities)


@app.route('/pets', methods=['GET'])
def pet_listings():
    pets = load_pets()
    # Preparing context pets: Only pets with status 'Available' or 'Pending' for listings?
    # Spec says all pets
    pets_list = [
        {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        } for pet in pets
    ]

    filters = {
        'species': ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    }

    return render_template('pet_listings.html', pets=pets_list, filters=filters)


@app.route('/pets', methods=['POST'])
def pet_listings_post():
    pets = load_pets()

    search_query = request.form.get('search_query', '').strip().lower()
    selected_species = request.form.get('selected_species', 'All')

    filtered_pets = pets

    if selected_species and selected_species != 'All':
        filtered_pets = [pet for pet in filtered_pets if pet['species'].lower() == selected_species.lower()]

    if search_query:
        filtered_pets = [pet for pet in filtered_pets if search_query in pet['name'].lower()]

    pets_list = [
        {
            'id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
        } for pet in filtered_pets
    ]

    filters = {
        'species': ['All', 'Dog', 'Cat', 'Bird', 'Rabbit', 'Other']
    }

    # Render pet_listings.html for filtered pets per spec (either redirect or render with context)
    return render_template('pet_listings.html', pets=pets_list, filters=filters)


@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        # Could show a 404 page - but not specified, redirect to pet listings
        return redirect(url_for('pet_listings'))

    shelter = get_shelter_by_id(pet['shelter_id'])
    if not shelter:
        # If shelter missing, create empty dict
        shelter = {'id':0, 'name':'Unknown Shelter', 'address':'', 'phone':'', 'email':''}
    else:
        shelter = {
            'id': shelter['shelter_id'],
            'name': shelter['name'],
            'address': shelter['address'],
            'phone': shelter['phone'],
            'email': shelter['email']
        }

    pet_context = {
        'id': pet['pet_id'],
        'name': pet['name'],
        'species': pet['species'],
        'description': pet['description'],
        'age': pet['age'],
        'gender': pet['gender']
    }

    return render_template('pet_details.html', pet=pet_context, shelter=shelter)


@app.route('/pets/<int:pet_id>/adopt', methods=['GET'])
def adoption_application(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return redirect(url_for('pet_listings'))

    pet_context = {
        'id': pet['pet_id'],
        'name': pet['name']
    }
    return render_template('adoption_application.html', pet=pet_context)


@app.route('/pets/<int:pet_id>/adopt', methods=['POST'])
def submit_adoption(pet_id):
    pet = get_pet_by_id(pet_id)
    if not pet:
        return redirect(url_for('pet_listings'))

    # Form fields
    applicant_name = request.form.get('applicant_name', '').strip()
    applicant_phone = request.form.get('applicant_phone', '').strip()
    housing_type = request.form.get('housing_type', '').strip()
    reason = request.form.get('reason', '').strip()

    # If mandatory fields are missing, re-render with a message
    if not applicant_name or not applicant_phone or not housing_type or not reason:
        pet_context = {'id': pet['pet_id'], 'name': pet['name']}
        # We don't have messages to show per spec - so just render
        return render_template('adoption_application.html', pet=pet_context)

    # Create new application_id
    applications = load_applications()
    new_id = max([app['application_id'] for app in applications], default=0) + 1

    # Find user info
    user = get_user(CURRENT_USERNAME) or {}
    address = user.get('address', '')

    new_application = {
        'application_id': new_id,
        'username': CURRENT_USERNAME,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
        'address': address,
        'housing_type': housing_type,
        'has_yard': 'No',  # Not present in form, so default No
        'other_pets': '',  # Not present in form
        'experience': '',  # Not present in form
        'reason': reason,
        'status': 'Pending',
        'date_submitted': datetime.now().strftime('%Y-%m-%d')
    }

    applications.append(new_application)
    save_applications(applications)

    return redirect(url_for('my_applications'))


@app.route('/add-pet', methods=['GET'])
def add_pet_page():
    return render_template('add_pet.html')


@app.route('/add-pet', methods=['POST'])
def submit_pet():
    # Form fields
    name = request.form.get('name', '').strip()
    species = request.form.get('species', '').strip()
    breed = request.form.get('breed', '').strip()
    age = request.form.get('age', '').strip()
    gender = request.form.get('gender', '').strip()
    size = request.form.get('size', '').strip()
    description = request.form.get('description', '').strip()

    if not all([name, species, breed, age, gender, size, description]):
        # Required all fields per spec, no messages, re-render
        return render_template('add_pet.html')

    pets = load_pets()
    new_id = max([p['pet_id'] for p in pets], default=0) + 1

    # For shelter_id, default to 1 (since no logged in shelter context)
    shelter_id = 1

    new_pet = {
        'pet_id': new_id,
        'name': name,
        'species': species,
        'breed': breed,
        'age': age,
        'gender': gender,
        'size': size,
        'description': description,
        'shelter_id': shelter_id,
        'status': 'Available',
        'date_added': datetime.now().strftime('%Y-%m-%d')
    }

    pets.append(new_pet)
    save_pets(pets)

    return redirect(url_for('pet_listings'))


@app.route('/applications', methods=['GET'])
def my_applications():
    filter_status = request.args.get('filter_status', None)

    applications = load_applications()
    pets = load_pets()

    # Filter applications by current user
    user_apps = [app for app in applications if app['username'] == CURRENT_USERNAME]

    if filter_status:
        user_apps = [app for app in user_apps if app['status'].lower() == filter_status.lower()]

    # Map pet_id to pet_name for display
    pet_name_map = {pet['pet_id']: pet['name'] for pet in pets}

    app_context = []
    for app in user_apps:
        pet_name = pet_name_map.get(app['pet_id'], 'Unknown')
        app_context.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=app_context, filter_status=filter_status)


@app.route('/favorites')
def favorites_page():
    favorites = load_favorites()
    pets = load_pets()

    # Get pet IDs user marked as favorite
    user_fav_pet_ids = [fav['pet_id'] for fav in favorites if fav['username'] == CURRENT_USERNAME]

    # Map pet_id to pets dict
    pet_map = {pet['pet_id']: pet for pet in pets}

    favorite_pets = []
    for pet_id in user_fav_pet_ids:
        pet = pet_map.get(pet_id)
        if pet:
            favorite_pets.append({
                'id': pet['pet_id'],
                'name': pet['name'],
                'species': pet['species'],
                'age': pet['age'],
                'photo_url': f"/static/photos/{pet['pet_id']}.jpg"
            })

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages', methods=['GET'])
def messages_page():
    messages = load_messages()

    # Conversations summary: group by interlocutor (other user), with last message timestamp
    interlocutor_map = {}
    for msg in messages:
        if msg['sender_username'] == CURRENT_USERNAME:
            other = msg['recipient_username']
        elif msg['recipient_username'] == CURRENT_USERNAME:
            other = msg['sender_username']
        else:
            continue

        # We only want one conversation per interlocutor
        if other not in interlocutor_map or interlocutor_map[other]['timestamp'] < msg['timestamp']:
            interlocutor_map[other] = {
                'interlocutor': other,
                'last_message_subject': msg['subject'],
                'last_message_content': msg['content'],
                'timestamp': msg['timestamp'],
                'is_read': msg['is_read']
            }

    conversations = list(interlocutor_map.values())
    # Sort conversations by timestamp descending
    conversations.sort(key=lambda c: c['timestamp'], reverse=True)

    return render_template('messages.html', conversations=conversations)


@app.route('/messages/send', methods=['POST'])
def send_message():
    recipient_username = request.form.get('recipient_username', '').strip()
    subject = request.form.get('subject', '').strip()
    content = request.form.get('content', '').strip()

    if not recipient_username or not subject or not content:
        # No message sent if missing fields
        return redirect(url_for('messages_page'))

    messages = load_messages()
    new_id = max([msg['message_id'] for msg in messages], default=0) + 1

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_message = {
        'message_id': new_id,
        'sender_username': CURRENT_USERNAME,
        'recipient_username': recipient_username,
        'subject': subject,
        'content': content,
        'timestamp': timestamp,
        'is_read': False
    }

    messages.append(new_message)
    save_messages(messages)

    return redirect(url_for('messages_page'))


@app.route('/profile', methods=['GET'])
def user_profile():
    user = get_user(CURRENT_USERNAME)
    if not user:
        # empty profile if not found
        user = {
            'username': CURRENT_USERNAME,
            'email': '',
            'phone': '',
            'address': ''
        }
    else:
        user['username'] = user['username']

    user_profile = {
        'username': user.get('username', ''),
        'email': user.get('email', ''),
        'phone': user.get('phone', ''),
        'address': user.get('address', '')
    }

    return render_template('profile.html', user_profile=user_profile)


@app.route('/profile', methods=['POST'])
def update_profile():
    new_email = request.form.get('email', '').strip()

    users = load_users()
    updated = False
    for user in users:
        if user['username'] == CURRENT_USERNAME:
            user['email'] = new_email
            updated = True
            break

    if not updated:
        # Add new user info if not found
        users.append({
            'username': CURRENT_USERNAME,
            'email': new_email,
            'phone': '',
            'address': ''
        })

    save_users(users)

    return redirect(url_for('user_profile'))


@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()

    # Pending applications
    pending_applications = [
        {
            'id': app['application_id'],
            'pet_name': next((p['name'] for p in pets if p['pet_id'] == app['pet_id']), 'Unknown'),
            'applicant_name': app['applicant_name'],
            'date': app['date_submitted'],
            'status': app['status']
        }
        for app in applications if app['status'].lower() == 'pending'
    ]

    # all_pets with full details
    all_pets = pets

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)


if __name__ == '__main__':
    app.run(debug=True)
