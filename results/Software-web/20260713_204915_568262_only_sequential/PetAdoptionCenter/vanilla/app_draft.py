from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions for file I/O and data parsing

def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        return [line for line in lines if line.strip() != '']


def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def parse_pipe_line(line, fields_count=None):
    parts = line.strip().split('|')
    if fields_count is not None and len(parts) != fields_count:
        return None
    return parts


def load_users():
    users = []
    for line in read_file_lines('users.txt'):
        parts = parse_pipe_line(line, 4)
        if parts:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
    return users


def save_users(users):
    lines = []
    for u in users:
        lines.append('|'.join([u['username'], u['email'], u['phone'], u['address']]))
    write_file_lines('users.txt', lines)


def load_pets():
    pets = []
    for line in read_file_lines('pets.txt'):
        parts = parse_pipe_line(line, 11)
        if parts:
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
    return pets


def save_pets(pets):
    lines = []
    for p in pets:
        lines.append('|'.join([
            str(p['pet_id']), p['name'], p['species'], p['breed'], p['age'], p['gender'], p['size'],
            p['description'], str(p['shelter_id']), p['status'], p['date_added']
        ]))
    write_file_lines('pets.txt', lines)


def load_applications():
    applications = []
    for line in read_file_lines('applications.txt'):
        parts = parse_pipe_line(line, 13)
        if parts:
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
    return applications


def save_applications(applications):
    lines = []
    for a in applications:
        lines.append('|'.join([
            str(a['application_id']), a['username'], str(a['pet_id']), a['applicant_name'], a['phone'], a['address'],
            a['housing_type'], a['has_yard'], a['other_pets'], a['experience'], a['reason'], a['status'], a['date_submitted']
        ]))
    write_file_lines('applications.txt', lines)


def load_favorites():
    favorites = []
    for line in read_file_lines('favorites.txt'):
        parts = parse_pipe_line(line, 3)
        if parts:
            favorites.append({
                'username': parts[0],
                'pet_id': int(parts[1]),
                'date_added': parts[2]
            })
    return favorites


def save_favorites(favorites):
    lines = []
    for f in favorites:
        lines.append('|'.join([f['username'], str(f['pet_id']), f['date_added']]))
    write_file_lines('favorites.txt', lines)


def load_messages():
    messages = []
    for line in read_file_lines('messages.txt'):
        parts = parse_pipe_line(line, 7)
        if parts:
            messages.append({
                'message_id': int(parts[0]),
                'sender_username': parts[1],
                'recipient_username': parts[2],
                'subject': parts[3],
                'content': parts[4],
                'timestamp': parts[5],
                'is_read': parts[6].lower() == 'true'
            })
    return messages


def save_messages(messages):
    lines = []
    for m in messages:
        lines.append('|'.join([
            str(m['message_id']), m['sender_username'], m['recipient_username'], m['subject'], m['content'], m['timestamp'],
            'true' if m['is_read'] else 'false'
        ]))
    write_file_lines('messages.txt', lines)


def load_shelters():
    shelters = []
    for line in read_file_lines('shelters.txt'):
        parts = parse_pipe_line(line, 5)
        if parts:
            shelters.append({
                'shelter_id': int(parts[0]),
                'name': parts[1],
                'address': parts[2],
                'phone': parts[3],
                'email': parts[4]
            })
    return shelters


# Helper function to get next id for pets, applications, messages

def next_pet_id():
    pets = load_pets()
    if not pets:
        return 1
    return max(p['pet_id'] for p in pets) + 1


def next_application_id():
    applications = load_applications()
    if not applications:
        return 1
    return max(a['application_id'] for a in applications) + 1


def next_message_id():
    messages = load_messages()
    if not messages:
        return 1
    return max(m['message_id'] for m in messages) + 1


# Simulate logged in user
# For simplicity, current user is 'john_doe'
CURRENT_USER = 'john_doe'


@app.route('/')
def dashboard():
    pets = load_pets()
    # Featured pets: limit 5 available ones sorted by date_added descending
    available_pets = [p for p in pets if p['status'] == 'Available']
    featured_sorted = sorted(available_pets, key=lambda x: x['date_added'], reverse=True)[:5]
    # Construct featured_pets with pet_id, name, species, age, photo_url placeholder
    featured_pets = []
    for pet in featured_sorted:
        featured_pets.append({
            'pet_id': pet['pet_id'],
            'name': pet['name'],
            'species': pet['species'],
            'age': pet['age'],
            # no photo_url in data, placeholder
            'photo_url': '/static/images/pet_placeholder.png'
        })
    return render_template('dashboard.html', featured_pets=featured_pets)


@app.route('/pets')
def pet_listings():
    pets = load_pets()
    filter_species = request.args.get('filter_species', 'All')
    search_query = request.args.get('search_query', '').strip()

    filtered_pets = pets
    if filter_species != 'All':
        filtered_pets = [p for p in filtered_pets if p['species'] == filter_species]
    if search_query:
        filtered_pets = [p for p in filtered_pets if search_query.lower() in p['name'].lower()]

    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species, search_query=search_query)


@app.route('/pet/<int:pet_id>')
def pet_details(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)


@app.route('/pet/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'GET':
        return render_template('add_pet.html')

    # POST - process add new pet
    name = request.form.get('pet-name-input', '').strip()
    species = request.form.get('pet-species-input', '').strip()
    breed = request.form.get('pet-breed-input', '').strip()
    age = request.form.get('pet-age-input', '').strip()
    gender = request.form.get('pet-gender-input', '').strip()
    size = request.form.get('pet-size-input', '').strip()
    description = request.form.get('pet-description-input', '').strip()

    if not (name and species and breed and age and gender and size and description):
        # Could add flash messages or error, but spec doesn't mention, so return form again
        return render_template('add_pet.html')

    pets = load_pets()
    new_id = next_pet_id()
    # Assign shelter_id 1 as default (could be extended to admin user shelter)
    shelter_id = 1
    date_added = datetime.now().strftime('%Y-%m-%d')
    status = 'Available'

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
        'status': status,
        'date_added': date_added
    }
    pets.append(new_pet)
    save_pets(pets)

    return redirect(url_for('pet_listings'))


@app.route('/application/<int:pet_id>', methods=['GET', 'POST'])
def adoption_application(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404

    if request.method == 'GET':
        return render_template('application.html', pet=pet)

    # POST - process application
    applicant_name = request.form.get('applicant-name', '').strip()
    applicant_phone = request.form.get('applicant-phone', '').strip()
    housing_type = request.form.get('housing-type', '').strip()
    reason = request.form.get('reason', '').strip()

    # Since other fields are required in data schema (address, has_yard, other_pets, experience) not in spec UI,
    # we'll fill dummy/default values

    if not (applicant_name and applicant_phone and housing_type and reason):
        # Re-render form with pet context
        return render_template('application.html', pet=pet)

    applications = load_applications()
    new_id = next_application_id()
    date_submitted = datetime.now().strftime('%Y-%m-%d')

    # Find user address from users.txt
    users = load_users()
    user_info = next((u for u in users if u['username'] == CURRENT_USER), None)
    address = user_info['address'] if user_info else ''

    # Fill default values to match schema
    has_yard = 'No'
    other_pets = 'None'
    experience = 'No experience'
    status = 'Pending'

    new_application = {
        'application_id': new_id,
        'username': CURRENT_USER,
        'pet_id': pet_id,
        'applicant_name': applicant_name,
        'phone': applicant_phone,
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

    return redirect(url_for('my_applications'))


@app.route('/applications')
def my_applications():
    applications = load_applications()
    pets = load_pets()
    filter_status = request.args.get('filter_status', 'All')

    user_apps = [a for a in applications if a['username'] == CURRENT_USER]
    if filter_status != 'All':
        user_apps = [a for a in user_apps if a['status'] == filter_status]

    # Enrich applications with pet name
    enriched_apps = []
    for app in user_apps:
        pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
        pet_name = pet['name'] if pet else 'Unknown'
        enriched_apps.append({
            'application_id': app['application_id'],
            'pet_name': pet_name,
            'date_submitted': app['date_submitted'],
            'status': app['status']
        })

    return render_template('my_applications.html', applications=enriched_apps, filter_status=filter_status)


@app.route('/favorites')
def favorites():
    favorites = load_favorites()
    pets = load_pets()
    user_favorites = [f for f in favorites if f['username'] == CURRENT_USER]

    favorite_pets = []
    for fav in user_favorites:
        pet = next((p for p in pets if p['pet_id'] == fav['pet_id']), None)
        if pet:
            favorite_pets.append(pet)

    return render_template('favorites.html', favorite_pets=favorite_pets)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages_data = load_messages()
    users = load_users()
    # For simplicity, list of conversations is unique partners (sent or received) with last message info
    # Group by other user
    conversations = {}
    for msg in messages_data:
        if msg['sender_username'] == CURRENT_USER:
            other = msg['recipient_username']
        elif msg['recipient_username'] == CURRENT_USER:
            other = msg['sender_username']
        else:
            continue
        if other not in conversations:
            conversations[other] = []
        conversations[other].append(msg)

    # Compose conversation list with last message timestamp
    conv_list = []
    for other_user, msgs in conversations.items():
        sorted_msgs = sorted(msgs, key=lambda x: x['timestamp'], reverse=True)
        last_msg = sorted_msgs[0]
        conv_list.append({
            'other_username': other_user,
            'last_subject': last_msg['subject'],
            'last_content': last_msg['content'],
            'last_timestamp': last_msg['timestamp'],
            'messages': sorted_msgs
        })

    # On POST, send message
    if request.method == 'POST':
        recipient = request.form.get('recipient_username', '').strip()
        subject = request.form.get('subject', '').strip()
        content = request.form.get('message-input', '').strip()

        if recipient and content:
            new_id = next_message_id()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_message = {
                'message_id': new_id,
                'sender_username': CURRENT_USER,
                'recipient_username': recipient,
                'subject': subject if subject else '',
                'content': content,
                'timestamp': timestamp,
                'is_read': False
            }
            messages_data.append(new_message)
            save_messages(messages_data)
            return redirect(url_for('messages'))

    return render_template('messages.html', conversations=conv_list)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = load_users()
    user_info = next((u for u in users if u['username'] == CURRENT_USER), None)
    if not user_info:
        # If user not found, create default
        user_info = {
            'username': CURRENT_USER,
            'email': '',
            'phone': '',
            'address': ''
        }
        users.append(user_info)

    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email:
            user_info['email'] = new_email
            save_users(users)
        return redirect(url_for('dashboard'))

    return render_template('profile.html', user_profile=user_info)


@app.route('/admin')
def admin_panel():
    applications = load_applications()
    pets = load_pets()

    pending_applications = [a for a in applications if a['status'] == 'Pending']

    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=pets)


if __name__ == '__main__':
    app.run(debug=True)
