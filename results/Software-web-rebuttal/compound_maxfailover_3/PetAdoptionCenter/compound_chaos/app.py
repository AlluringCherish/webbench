from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions to load and save pipe-delimited data files

def read_pipe_delimited_file(filepath):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    data.append(parts)
    except FileNotFoundError:
        pass
    return data

def write_pipe_delimited_file(filepath, rows):
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write('|'.join(row) + '\n')

# Data loading and saving functions for each entity

def get_all_pets():
    lines = read_pipe_delimited_file('data/pets.txt')
    pets = []
    for parts in lines:
        if len(parts) < 11:
            continue
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

def save_all_pets(pets):
    rows = []
    for pet in pets:
        row = [
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
        ]
        rows.append(row)
    write_pipe_delimited_file('data/pets.txt', rows)


def get_all_users():
    lines = read_pipe_delimited_file('data/users.txt')
    users = []
    for parts in lines:
        if len(parts) < 4:
            continue
        user = {
            'username': parts[0],
            'email': parts[1],
            'phone': parts[2],
            'address': parts[3]
        }
        users.append(user)
    return users

def get_user_by_username(username):
    users = get_all_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def get_all_applications():
    lines = read_pipe_delimited_file('data/applications.txt')
    applications = []
    for parts in lines:
        if len(parts) < 13:
            continue
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
    return applications

def save_all_applications(applications):
    rows = []
    for app in applications:
        row = [
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
        ]
        rows.append(row)
    write_pipe_delimited_file('data/applications.txt', rows)


def get_favorites_by_username(username):
    lines = read_pipe_delimited_file('data/favorites.txt')
    pet_ids = set()
    for parts in lines:
        if len(parts) < 3:
            continue
        if parts[0] == username:
            pet_ids.add(int(parts[1]))
    return pet_ids


def get_all_messages():
    lines = read_pipe_delimited_file('data/messages.txt')
    messages = []
    for parts in lines:
        if len(parts) < 7:
            continue
        msg = {
            'message_id': int(parts[0]),
            'sender_username': parts[1],
            'recipient_username': parts[2],
            'subject': parts[3],
            'content': parts[4],
            'timestamp': parts[5],
            'is_read': parts[6] == 'true'
        }
        messages.append(msg)
    return messages


def save_all_messages(messages):
    rows = []
    for m in messages:
        row = [
            str(m['message_id']),
            m['sender_username'],
            m['recipient_username'],
            m['subject'],
            m['content'],
            m['timestamp'],
            'true' if m.get('is_read', False) else 'false'
        ]
        rows.append(row)
    write_pipe_delimited_file('data/messages.txt', rows)


def get_all_shelters():
    lines = read_pipe_delimited_file('data/shelters.txt')
    shelters = []
    for parts in lines:
        if len(parts) < 5:
            continue
        shelters.append({
            'shelter_id': int(parts[0]),
            'name': parts[1],
            'address': parts[2],
            'phone': parts[3],
            'email': parts[4]
        })
    return shelters

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    pets = get_all_pets()
    # Get featured pets (for spec assume those with status "Available")
    featured_pets = [
        {
            'pet_id': p['pet_id'],
            'name': p['name'],
            'species': p['species'],
            'age': p['age']
        } for p in pets if p['status'] == 'Available'
    ]
    # Recent activities - for demo, just recent pet names added in reverse date order (max 5)
    recent_activities = sorted(pets, key=lambda x: x['date_added'], reverse=True)[:5]
    recent_activities = [f"Added {p['name']}" for p in recent_activities]
    return render_template('dashboard.html', featured_pets=featured_pets, recent_activities=recent_activities)

@app.route('/pets')
def pet_listings_page():
    pets = get_all_pets()
    filter_species = request.args.get('filter_species', '')
    search_query = request.args.get('search_query', '')
    filtered_pets = pets
    if filter_species:
        filtered_pets = [p for p in filtered_pets if p['species'].lower() == filter_species.lower()]
    if search_query:
        filtered_pets = [p for p in filtered_pets if search_query.lower() in p['name'].lower()]
    return render_template('pet_listings.html', pets=filtered_pets, filter_species=filter_species, search_query=search_query)

@app.route('/pets/<int:pet_id>')
def pet_details_page(pet_id):
    pets = get_all_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('pet_details.html', pet=pet)

@app.route('/pets/add')
def add_pet_page():
    return render_template('add_pet.html')

@app.route('/pets/add', methods=['POST'])
def submit_new_pet():
    pets = get_all_pets()
    # Assign new pet_id as max+1 or 1
    new_id = max([p['pet_id'] for p in pets], default=0) + 1
    form = request.form
    new_pet = {
        'pet_id': new_id,
        'name': form.get('pet_name','').strip(),
        'species': form.get('pet_species','').strip(),
        'breed': form.get('pet_breed','').strip(),
        'age': form.get('pet_age','').strip(),
        'gender': form.get('pet_gender','').strip(),
        'size': form.get('pet_size','').strip(),
        'description': form.get('pet_description','').strip(),
        'shelter_id': 1,  # default shelter_id to 1
        'status': 'Available',
        'date_added': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    pets.append(new_pet)
    save_all_pets(pets)
    return redirect(url_for('pet_listings_page'))

@app.route('/applications/adopt/<int:pet_id>')
def adoption_application_page(pet_id):
    pets = get_all_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('adoption_application.html', pet={'pet_id': pet['pet_id'], 'name': pet['name']})

@app.route('/applications/adopt/<int:pet_id>', methods=['POST'])
def submit_adoption_application(pet_id):
    pets = get_all_pets()
    if not any(p['pet_id'] == pet_id for p in pets):
        return "Pet not found", 404
    applications = get_all_applications()
    new_id = max([app['application_id'] for app in applications], default=0) + 1
    form = request.form
    new_app = {
        'application_id': new_id,
        'username': form.get('username','').strip(),
        'pet_id': pet_id,
        'applicant_name': form.get('applicant_name','').strip(),
        'phone': form.get('applicant_phone','').strip(),
        'address': form.get('applicant_address','').strip(),
        'housing_type': form.get('housing_type','').strip(),
        'has_yard': form.get('has_yard','').strip(),
        'other_pets': form.get('other_pets','').strip(),
        'experience': form.get('experience','').strip(),
        'reason': form.get('reason','').strip(),
        'status': 'Pending',
        'date_submitted': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    applications.append(new_app)
    save_all_applications(applications)
    return redirect(url_for('my_applications_page'))

@app.route('/applications')
def my_applications_page():
    filter_status = request.args.get('filter_status', '')
    applications = get_all_applications()
    pets = get_all_pets()
    applications_filtered = []
    for app in applications:
        pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
        if pet:
            app_dict = {
                'application_id': app['application_id'],
                'pet_name': pet['name'],
                'date_submitted': app['date_submitted'],
                'status': app['status']
            }
            if filter_status:
                if app['status'].lower() == filter_status.lower():
                    applications_filtered.append(app_dict)
            else:
                applications_filtered.append(app_dict)
    return render_template('my_applications.html', applications=applications_filtered, filter_status=filter_status)

@app.route('/favorites')
def favorites_page():
    username = request.args.get('username', '')
    if not username:
        favorite_pets = []
    else:
        pet_ids = get_favorites_by_username(username)
        pets = get_all_pets()
        favorite_pets = [
            {
                'pet_id': p['pet_id'],
                'name': p['name'],
                'species': p['species'],
                'age': p['age']
            }
            for p in pets if p['pet_id'] in pet_ids
        ]
    return render_template('favorites.html', favorite_pets=favorite_pets)

@app.route('/messages')
def messages_page():
    username = request.args.get('username', '')
    messages = get_all_messages()
    # Group messages into conversations by (sender, recipient, subject)
    conv_map = {}
    for msg in messages:
        if msg['sender_username'] == username or msg['recipient_username'] == username:
            key = (msg['sender_username'], msg['recipient_username'], msg['subject'])
            if key not in conv_map:
                conv_map[key] = {
                    'message_id': msg['message_id'],
                    'sender_username': msg['sender_username'],
                    'recipient_username': msg['recipient_username'],
                    'subject': msg['subject'],
                    'last_message': msg['content'],
                    'unread_count': 0
                }
            else:
                # Update last message if newer timestamp
                # Here no timestamp parsing, we update always last seen
                conv_map[key]['last_message'] = msg['content']
            if not msg['is_read'] and msg['recipient_username'] == username:
                conv_map[key]['unread_count'] += 1
    conversations = list(conv_map.values())
    return render_template('messages.html', conversations=conversations)

@app.route('/messages/send', methods=['POST'])
def send_message():
    form = request.form
    messages = get_all_messages()
    new_id = max([m['message_id'] for m in messages], default=0) + 1
    new_msg = {
        'message_id': new_id,
        'sender_username': form.get('sender_username','').strip(),
        'recipient_username': form.get('recipient_username','').strip(),
        'subject': form.get('subject','').strip(),
        'content': form.get('content','').strip(),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': False
    }
    messages.append(new_msg)
    save_all_messages(messages)
    return redirect(url_for('messages_page', username=new_msg['sender_username']))

@app.route('/profile')
def user_profile_page():
    username = request.args.get('username', '')
    user = get_user_by_username(username)
    if not user:
        return "User not found", 404
    return render_template('profile.html', username=user['username'], email=user['email'])

@app.route('/profile', methods=['POST'])
def update_profile():
    username = request.args.get('username', '')
    users = get_all_users()
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return "User not found", 404
    new_email = request.form.get('email', '').strip()
    # Update email if changed
    updated = False
    if new_email and new_email != user['email']:
        user['email'] = new_email
        updated = True
    if updated:
        # Save all users
        rows = []
        for u in users:
            rows.append([u['username'], u['email'], u['phone'], u['address']])
        write_pipe_delimited_file('data/users.txt', rows)
    return redirect(url_for('user_profile_page', username=username))

@app.route('/admin')
def admin_panel_page():
    applications = get_all_applications()
    pending_applications = []
    pets = get_all_pets()
    for app in applications:
        if app['status'].lower() == 'pending':
            pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
            if pet:
                pending_applications.append({
                    'application_id': app['application_id'],
                    'applicant_name': app['applicant_name'],
                    'pet_name': pet['name'],
                    'date_submitted': app['date_submitted']
                })
    all_pets = [{'pet_id': p['pet_id'], 'name': p['name']} for p in pets]
    return render_template('admin_panel.html', pending_applications=pending_applications, all_pets=all_pets)

@app.route('/admin/applications/<int:application_id>/approve', methods=['POST'])
def approve_application(application_id):
    applications = get_all_applications()
    app = next((a for a in applications if a['application_id'] == application_id), None)
    if not app:
        return "Application not found", 404
    app['status'] = 'Approved'
    # Also update pet status to Pending (application submitted and approved)
    pets = get_all_pets()
    pet = next((p for p in pets if p['pet_id'] == app['pet_id']), None)
    if pet:
        pet['status'] = 'Pending'
    save_all_applications(applications)
    save_all_pets(pets)
    return redirect(url_for('admin_panel_page'))

@app.route('/admin/applications/<int:application_id>/reject', methods=['POST'])
def reject_application(application_id):
    applications = get_all_applications()
    app = next((a for a in applications if a['application_id'] == application_id), None)
    if not app:
        return "Application not found", 404
    app['status'] = 'Rejected'
    save_all_applications(applications)
    return redirect(url_for('admin_panel_page'))

@app.route('/admin/pets/<int:pet_id>/edit')
def edit_pet_page(pet_id):
    pets = get_all_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    return render_template('edit_pet.html', pet=pet)

@app.route('/admin/pets/<int:pet_id>/edit', methods=['POST'])
def submit_pet_edit(pet_id):
    pets = get_all_pets()
    pet = next((p for p in pets if p['pet_id'] == pet_id), None)
    if not pet:
        return "Pet not found", 404
    form = request.form
    pet['name'] = form.get('pet_name', pet['name']).strip()
    pet['species'] = form.get('pet_species', pet['species']).strip()
    pet['breed'] = form.get('pet_breed', pet['breed']).strip()
    pet['age'] = form.get('pet_age', pet['age']).strip()
    pet['gender'] = form.get('pet_gender', pet['gender']).strip()
    pet['size'] = form.get('pet_size', pet['size']).strip()
    pet['description'] = form.get('pet_description', pet['description']).strip()
    save_all_pets(pets)
    return redirect(url_for('pet_details_page', pet_id=pet_id))

@app.route('/admin/pets/<int:pet_id>/delete', methods=['POST'])
def delete_pet(pet_id):
    pets = get_all_pets()
    pets = [p for p in pets if p['pet_id'] != pet_id]
    save_all_pets(pets)
    return redirect(url_for('admin_panel_page'))

if __name__ == '__main__':
    app.run(debug=True)
