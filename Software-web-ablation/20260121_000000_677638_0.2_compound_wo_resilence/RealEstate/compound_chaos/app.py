from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
DATA_DIR = 'data'
PROPERTIES_FILE = os.path.join(DATA_DIR, 'properties.txt')
LOCATIONS_FILE = os.path.join(DATA_DIR, 'locations.txt')
INQUIRIES_FILE = os.path.join(DATA_DIR, 'inquiries.txt')
FAVORITES_FILE = os.path.join(DATA_DIR, 'favorites.txt')
AGENTS_FILE = os.path.join(DATA_DIR, 'agents.txt')

# Helpers to load and save data

def load_properties():
    properties = []
    try:
        with open(PROPERTIES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    property = {
                        'property_id': parts[0],
                        'address': parts[1],
                        'location_id': parts[2],
                        'price': float(parts[3]),
                        'status': parts[4]  # e.g., available, sold
                    }
                    properties.append(property)
    except Exception:
        pass
    return properties

def load_locations():
    locations = []
    try:
        with open(LOCATIONS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    location = {
                        'location_id': parts[0],
                        'name': parts[1]
                    }
                    locations.append(location)
    except Exception:
        pass
    return locations

def load_inquiries():
    inquiries = []
    try:
        with open(INQUIRIES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    inquiry = {
                        'inquiry_id': parts[0],
                        'property_id': parts[1],
                        'user_name': parts[2],
                        'user_email': parts[3],
                        'message': parts[4],
                        'status': parts[5]  # e.g., pending, answered
                    }
                    inquiries.append(inquiry)
    except Exception:
        pass
    return inquiries

def load_favorites():
    favorites = []
    try:
        with open(FAVORITES_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    favorite = {
                        'user_email': parts[0],
                        'property_id': parts[1]
                    }
                    favorites.append(favorite)
    except Exception:
        pass
    return favorites

def load_agents():
    agents = []
    try:
        with open(AGENTS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    agent = {
                        'agent_id': parts[0],
                        'name': parts[1],
                        'contact': parts[2]
                    }
                    agents.append(agent)
    except Exception:
        pass
    return agents


def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w') as f:
            for inq in inquiries:
                line = '|'.join([inq['inquiry_id'], inq['property_id'], inq['user_name'], inq['user_email'], inq['message'], inq['status']])
                f.write(line + '\n')
    except Exception:
        pass

def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w') as f:
            for fav in favorites:
                line = '|'.join([fav['user_email'], fav['property_id']])
                f.write(line + '\n')
    except Exception:
        pass

# Routes as per design_spec.md Section 1

@app.route('/')
def root():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    locations = load_locations()
    # Possibly enrich properties with location names
    loc_map = {loc['location_id']: loc['name'] for loc in locations}
    for p in properties:
        p['location_name'] = loc_map.get(p['location_id'], 'Unknown')
    return render_template('dashboard.html', properties=properties)

@app.route('/property/<property_id>')
def property_details(property_id):
    properties = load_properties()
    property = next((p for p in properties if p['property_id'] == property_id), None)
    if not property:
        return render_template('404.html'), 404
    locations = load_locations()
    loc_map = {loc['location_id']: loc['name'] for loc in locations}
    property['location_name'] = loc_map.get(property['location_id'], 'Unknown')
    inquiries = [inq for inq in load_inquiries() if inq['property_id'] == property_id]
    agents = load_agents()  # Could be filtered if spec clarifies
    return render_template('property_details.html', property=property, inquiries=inquiries, agents=agents)

@app.route('/inquiry', methods=['POST'])
def inquiry():
    # Collect and validate form data
    property_id = request.form.get('property_id')
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    message = request.form.get('message')
    if not (property_id and user_name and user_email and message):
        # Ideally flash an error or respond with message
        return redirect(url_for('dashboard'))
    inquiries = load_inquiries()
    # Generate new inquiry id
    existing_ids = {int(inq['inquiry_id']) for inq in inquiries if inq['inquiry_id'].isdigit()}
    new_id = str(max(existing_ids) + 1 if existing_ids else 1)
    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'user_name': user_name,
        'user_email': user_email,
        'message': message,
        'status': 'pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)
    return redirect(url_for('property_details', property_id=property_id))

@app.route('/favorites/<user_email>')
def favorites(user_email):
    properties = load_properties()
    favorites = load_favorites()
    fav_props_ids = [fav['property_id'] for fav in favorites if fav['user_email'] == user_email]
    fav_props = [p for p in properties if p['property_id'] in fav_props_ids]
    return render_template('favorites.html', user_email=user_email, favorites=fav_props)

@app.route('/favorite/add', methods=['POST'])
def add_favorite():
    user_email = request.form.get('user_email')
    property_id = request.form.get('property_id')
    if not user_email or not property_id:
        return redirect(url_for('dashboard'))
    favorites = load_favorites()
    # Avoid duplicates
    if not any(fav['user_email'] == user_email and fav['property_id'] == property_id for fav in favorites):
        favorites.append({'user_email': user_email, 'property_id': property_id})
        save_favorites(favorites)
    return redirect(url_for('favorites', user_email=user_email))

@app.route('/favorite/remove', methods=['POST'])
def remove_favorite():
    user_email = request.form.get('user_email')
    property_id = request.form.get('property_id')
    if not user_email or not property_id:
        return redirect(url_for('dashboard'))
    favorites = load_favorites()
    favorites = [fav for fav in favorites if not (fav['user_email'] == user_email and fav['property_id'] == property_id)]
    save_favorites(favorites)
    return redirect(url_for('favorites', user_email=user_email))

@app.route('/agents')
def agents():
    agents = load_agents()
    return render_template('agents.html', agents=agents)

if __name__ == '__main__':
    app.run(debug=True)
