from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper to check float conversion
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Load properties from data/properties.txt
def load_properties():
    properties = []
    file_path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.exists(file_path):
        return properties
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields)!=11:
                    continue
                try:
                    prop = {
                        'property_id': int(fields[0]),
                        'address': fields[1],
                        'location': fields[2],
                        'price': int(fields[3]) if fields[3].isdigit() else 0,
                        'property_type': fields[4],
                        'bedrooms': int(fields[5]) if fields[5].isdigit() else 0,
                        'bathrooms': float(fields[6]) if is_float(fields[6]) else 0.0,
                        'square_feet': int(fields[7]) if fields[7].isdigit() else 0,
                        'description': fields[8],
                        'agent_id': int(fields[9]) if fields[9].isdigit() else None,
                        'status': fields[10]
                    }
                    properties.append(prop)
                except:
                    continue
    except:
        return []
    return properties

# Load locations from data/locations.txt
def load_locations():
    locations=[]
    file_path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(file_path):
        return locations
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields=line.split('|')
                if len(fields)!=6:
                    continue
                try:
                    loc = {
                        'location_id': int(fields[0]),
                        'location_name': fields[1],
                        'region': fields[2],
                        'average_price': int(fields[3]) if fields[3].isdigit() else 0,
                        'property_count': int(fields[4]) if fields[4].isdigit() else 0,
                        'description': fields[5]
                    }
                    locations.append(loc)
                except:
                    continue
    except:
        return []
    return locations

# Load inquiries from data/inquiries.txt
def load_inquiries():
    inquiries=[]
    file_path = os.path.join(DATA_DIR, 'inquiries.txt')
    if not os.path.exists(file_path):
        return inquiries
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields=line.split('|')
                if len(fields)!=8:
                    continue
                try:
                    inquiry = {
                        'inquiry_id': int(fields[0]),
                        'property_id': int(fields[1]),
                        'customer_name': fields[2],
                        'customer_email': fields[3],
                        'customer_phone': fields[4],
                        'message': fields[5],
                        'inquiry_date': fields[6],
                        'status': fields[7]
                    }
                    inquiries.append(inquiry)
                except:
                    continue
    except:
        return []
    return inquiries

# Load favorites from data/favorites.txt
def load_favorites():
    favorites=[]
    file_path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(file_path):
        return favorites
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields=line.split('|')
                if len(fields)!=3:
                    continue
                try:
                    fav = {
                        'favorite_id': int(fields[0]),
                        'property_id': int(fields[1]),
                        'added_date': fields[2]
                    }
                    favorites.append(fav)
                except:
                    continue
    except:
        return []
    return favorites

# Load agents from data/agents.txt
def load_agents():
    agents=[]
    file_path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.exists(file_path):
        return agents
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                fields=line.split('|')
                if len(fields)!=6:
                    continue
                try:
                    agent = {
                        'agent_id': int(fields[0]),
                        'agent_name': fields[1],
                        'specialization': fields[2],
                        'email': fields[3],
                        'phone': fields[4],
                        'properties_sold': int(fields[5]) if fields[5].isdigit() else 0
                    }
                    agents.append(agent)
                except:
                    continue
    except:
        return []
    return agents

# Save inquiries to data/inquiries.txt
def save_inquiries(inquiries):
    file_path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            for i in inquiries:
                line = f"{i['inquiry_id']}|{i['property_id']}|{i['customer_name']}|{i['customer_email']}|{i['customer_phone']}|{i['message']}|{i['inquiry_date']}|{i['status']}"
                f.write(line+'\n')
    except:
        pass

# Save favorites to data/favorites.txt
def save_favorites(favorites):
    file_path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}"
                f.write(line+'\n')
    except:
        pass

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available'][:5]
    return render_template('dashboard.html', featured_properties=featured_properties)

@app.route('/properties')
def property_search():
    properties = load_properties()
    return render_template('property_search.html', properties=properties)

@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    return render_template('property_details.html', property=prop)

@app.route('/inquiry', methods=['GET'])
def inquiry_form():
    properties = load_properties()
    return render_template('inquiry.html', properties=properties)

@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    properties = load_properties()
    errors = {}

    property_id_raw = request.form.get('property_id', '').strip()
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    message = request.form.get('message', '').strip()

    # Validate property_id
    if not property_id_raw.isdigit():
        errors['property_id'] = 'Invalid property selection.'
    else:
        property_id = int(property_id_raw)
        if not any(p['property_id'] == property_id for p in properties):
            errors['property_id'] = 'Selected property does not exist.'

    # Validate customer_name
    if not customer_name:
        errors['customer_name'] = 'Name is required.'

    # Validate customer_email
    if not customer_email:
        errors['customer_email'] = 'Email is required.'
    elif '@' not in customer_email or '.' not in customer_email:
        errors['customer_email'] = 'Invalid email format.'

    # Validate customer_phone
    if not customer_phone:
        errors['customer_phone'] = 'Phone number is required.'

    # Validate message
    if not message:
        errors['message'] = 'Message is required.'

    if errors:
        return render_template('inquiry.html', properties=properties, errors=errors)

    inquiries = load_inquiries()
    new_id = max((inq['inquiry_id'] for inq in inquiries), default=0) + 1
    today = datetime.today().strftime('%Y-%m-%d')

    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'message': message,
        'inquiry_date': today,
        'status': 'Pending'
    }

    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    return redirect(url_for('inquiries_list'))

@app.route('/inquiries')
def inquiries_list():
    inquiries = load_inquiries()
    return render_template('inquiries.html', inquiries=inquiries)

@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('inquiries_list'))

@app.route('/favorites')
def favorites_list():
    favorites = load_favorites()
    properties = load_properties()
    prop_map = {p['property_id']: p for p in properties}
    favorite_properties = [prop_map[fav['property_id']] for fav in favorites if fav['property_id'] in prop_map]
    return render_template('favorites.html', favorite_properties=favorite_properties)

@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_favorite(property_id):
    favorites = load_favorites()
    if any(fav['property_id'] == property_id for fav in favorites):
        return redirect(url_for('favorites_list'))
    new_id = max((fav['favorite_id'] for fav in favorites), default=0) + 1
    today = datetime.today().strftime('%Y-%m-%d')
    new_fav = {
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': today
    }
    favorites.append(new_fav)
    save_favorites(favorites)
    return redirect(url_for('favorites_list'))

@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('favorites_list'))

@app.route('/agents')
def agents_list():
    agents = load_agents()
    return render_template('agents.html', agents=agents)

@app.route('/locations')
def locations_list():
    locations = load_locations()
    return render_template('locations.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
