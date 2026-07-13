from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import datetime

app = Flask(__name__)

DATA_FOLDER = 'data'
PROPERTIES_FILE = os.path.join(DATA_FOLDER, 'properties.txt')
AGENTS_FILE = os.path.join(DATA_FOLDER, 'agents.txt')
INQUIRIES_FILE = os.path.join(DATA_FOLDER, 'inquiries.txt')
FAVORITES_FILE = os.path.join(DATA_FOLDER, 'favorites.txt')
LOCATIONS_FILE = os.path.join(DATA_FOLDER, 'locations.txt')

# Helper functions to load and save data

def load_properties():
    properties = []
    with open(PROPERTIES_FILE, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 11:
                continue
            prop = {
                'id': parts[0],
                'address': parts[1],
                'location': parts[2],
                'price': int(parts[3]),
                'type': parts[4],
                'beds': int(parts[5]),
                'baths': float(parts[6]),
                'sqft': int(parts[7]),
                'description': parts[8],
                'agent_id': parts[9],
                'status': parts[10]
            }
            properties.append(prop)
    return properties

def load_agents():
    agents = []
    with open(AGENTS_FILE, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            agent = {
                'id': parts[0],
                'name': parts[1],
                'specialization': parts[2],
                'email': parts[3],
                'phone': parts[4],
                'properties_sold': int(parts[5])
            }
            agents.append(agent)
    return agents

def load_inquiries():
    inquiries = []
    if not os.path.exists(INQUIRIES_FILE):
        return inquiries
    with open(INQUIRIES_FILE, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            inquiry = {
                'inquiry_id': parts[0],
                'property_id': parts[1],
                'customer_name': parts[2],
                'customer_email': parts[3],
                'customer_phone': parts[4],
                'message': parts[5],
                'inquiry_date': parts[6],
                'status': parts[7]
            }
            inquiries.append(inquiry)
    return inquiries

def save_inquiries(inquiries):
    with open(INQUIRIES_FILE, 'w') as f:
        for iq in inquiries:
            line = '|'.join([iq['inquiry_id'], iq['property_id'], iq['customer_name'], iq['customer_email'], iq['customer_phone'], iq['message'], iq['inquiry_date'], iq['status']])
            f.write(line + '\n')

def load_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    with open(FAVORITES_FILE, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            favorite = {
                'favorite_id': parts[0],
                'property_id': parts[1],
                'added_date': parts[2]
            }
            favorites.append(favorite)
    return favorites

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        for fav in favorites:
            line = '|'.join([fav['favorite_id'], fav['property_id'], fav['added_date']])
            f.write(line + '\n')

def load_locations():
    locations = []
    with open(LOCATIONS_FILE, 'r') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            loc = {
                'id': parts[0],
                'name': parts[1],
                'region': parts[2],
                'average_price': int(parts[3]),
                'property_count': int(parts[4]),
                'description': parts[5]
            }
            locations.append(loc)
    return locations

def generate_id():
    return str(uuid.uuid4())

# Routes
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    featured_properties = sorted(properties, key=lambda x: x['price'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties)

@app.route('/search', methods=['GET'])
def search_page():
    properties = load_properties()
    locations = load_locations()

    # Get filters
    location_filter = request.args.get('location-input', '').strip()
    min_price = request.args.get('price-range-min', type=int)
    max_price = request.args.get('price-range-max', type=int)
    property_type = request.args.get('property-type-filter', '')

    filtered_properties = properties

    if location_filter:
        filtered_properties = [p for p in filtered_properties if location_filter.lower() in p['location'].lower() or location_filter.lower() in p['address'].lower()]
    if min_price is not None:
        filtered_properties = [p for p in filtered_properties if p['price'] >= min_price]
    if max_price is not None:
        filtered_properties = [p for p in filtered_properties if p['price'] <= max_price]
    if property_type and property_type != 'All':
        filtered_properties = [p for p in filtered_properties if p['type'] == property_type]

    return render_template('search.html', properties=filtered_properties, locations=locations)

@app.route('/property/<property_id>')
def property_details(property_id):
    properties = load_properties()
    property_item = next((p for p in properties if p['id'] == property_id), None)
    if not property_item:
        return "Property not found", 404

    agents = load_agents()
    related_agents = [a for a in agents if a['id'] == property_item['agent_id']]
    return render_template('property_details.html', property=property_item, agents=related_agents)

@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    properties = load_properties()
    if request.method == 'POST':
        property_id = request.form.get('select-property')
        name = request.form.get('inquiry-name')
        email = request.form.get('inquiry-email')
        phone = request.form.get('inquiry-phone')
        message = request.form.get('inquiry-message') or ''

        if not (property_id and name and email and phone):
            return "Missing required fields", 400

        inquiries = load_inquiries()
        new_inquiry = {
            'inquiry_id': generate_id(),
            'property_id': property_id,
            'customer_name': name,
            'customer_email': email,
            'customer_phone': phone,
            'message': message,
            'inquiry_date': datetime.date.today().isoformat(),
            'status': 'Pending'
        }
        inquiries.append(new_inquiry)
        save_inquiries(inquiries)
        return redirect(url_for('dashboard'))

    return render_template('inquiry.html', properties=properties)

@app.route('/inquiries')
def inquiries_page():
    inquiries = load_inquiries()
    properties = load_properties()
    status_filter = request.args.get('inquiry-status-filter', 'All')
    if status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'] == status_filter]

    # Add property address info to inquiries
    for inq in inquiries:
        prop = next((p for p in properties if p['id'] == inq['property_id']), None)
        inq['property_address'] = prop['address'] if prop else 'Unknown'

    return render_template('inquiries.html', inquiries=inquiries, status_filter=status_filter)

@app.route('/delete-inquiry/<inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('inquiries_page'))

@app.route('/favorites')
def favorites_page():
    favorites = load_favorites()
    properties = load_properties()
    favorite_props = []
    for fav in favorites:
        prop = next((p for p in properties if p['id'] == fav['property_id']), None)
        if prop:
            favorite_props.append({'favorite_id': fav['favorite_id'], 'property': prop})
    return render_template('favorites.html', favorites=favorite_props)

@app.route('/add-to-favorites/<property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    for fav in favorites:
        if fav['property_id'] == property_id:
            return redirect(url_for('favorites_page'))
    new_fav = {
        'favorite_id': generate_id(),
        'property_id': property_id,
        'added_date': datetime.date.today().isoformat()
    }
    favorites.append(new_fav)
    save_favorites(favorites)
    return redirect(url_for('favorites_page'))

@app.route('/remove-from-favorites/<favorite_id>', methods=['POST'])
def remove_from_favorites(favorite_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['favorite_id'] != favorite_id]
    save_favorites(favorites)
    return redirect(url_for('favorites_page'))

@app.route('/agents')
def agents_page():
    agents = load_agents()
    search_query = request.args.get('agent-search', '').lower()
    if search_query:
        agents = [a for a in agents if search_query in a['name'].lower()]
    return render_template('agents.html', agents=agents, search_query=search_query)

@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_criteria = request.args.get('location-sort', 'Name')

    if sort_criteria == 'Name':
        locations.sort(key=lambda x: x['name'])
    elif sort_criteria == 'Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_criteria == 'Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)

    return render_template('locations.html', locations=locations, sort_criteria=sort_criteria)

@app.route('/view-location/<location_id>')
def view_location(location_id):
    locations = load_locations()
    loc = next((l for l in locations if l['id'] == location_id), None)
    if not loc:
        return "Location not found", 404
    properties = load_properties()
    filtered_properties = [p for p in properties if p['location'].lower() == loc['name'].lower()]
    return render_template('search.html', properties=filtered_properties, locations=locations)

@app.route('/contact-agent/<agent_id>')
def contact_agent(agent_id):
    agents = load_agents()
    agent = next((a for a in agents if a['id'] == agent_id), None)
    if not agent:
        return "Agent not found", 404
    # This triggers user's default email client
    return redirect(f"mailto:{agent['email']}")

if __name__ == '__main__':
    app.run(debug=True)
