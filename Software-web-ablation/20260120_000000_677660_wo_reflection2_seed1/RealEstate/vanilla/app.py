from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'

# Helper functions to load and save data according to Section 3 schema

# Properties schema
# property_id|title|description|location_id|price|property_type|bedrooms|bathrooms|sqft|agent_id|is_featured (1 or 0)
def load_properties():
    properties = []
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 11:
                    continue
                property = {
                    'property_id': int(parts[0]),
                    'title': parts[1],
                    'description': parts[2],
                    'location_id': int(parts[3]),
                    'price': float(parts[4]),
                    'property_type': parts[5],
                    'bedrooms': int(parts[6]),
                    'bathrooms': int(parts[7]),
                    'sqft': int(parts[8]),
                    'agent_id': int(parts[9]),
                    'is_featured': True if parts[10] == '1' else False
                }
                properties.append(property)
    except (IOError, FileNotFoundError):
        properties = []
    return properties

def save_properties(properties):
    try:
        with open(PROPERTIES_FILE, 'w', encoding='utf-8') as f:
            for p in properties:
                line = '|'.join([
                    str(p['property_id']),
                    p['title'],
                    p['description'],
                    str(p['location_id']),
                    f"{p['price']:.2f}",
                    p['property_type'],
                    str(p['bedrooms']),
                    str(p['bathrooms']),
                    str(p['sqft']),
                    str(p['agent_id']),
                    '1' if p['is_featured'] else '0'
                ])
                f.write(line + '\n')
    except (IOError, FileNotFoundError):
        pass

# Locations schema
# location_id|name|region|population

def load_locations():
    locations = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 4:
                    continue
                location = {
                    'location_id': int(parts[0]),
                    'name': parts[1],
                    'region': parts[2],
                    'population': int(parts[3])
                }
                locations.append(location)
    except (IOError, FileNotFoundError):
        locations = []
    return locations

# Inquiries schema
# inquiry_id|property_id|name|email|phone|message|status

def load_inquiries():
    inquiries = []
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                inquiry = {
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'name': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'message': parts[5],
                    'status': parts[6]
                }
                inquiries.append(inquiry)
    except (IOError, FileNotFoundError):
        inquiries = []
    return inquiries


def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = '|'.join([
                    str(inq['inquiry_id']),
                    str(inq['property_id']),
                    inq['name'],
                    inq['email'],
                    inq['phone'],
                    inq['message'],
                    inq['status']
                ])
                f.write(line + '\n')
    except (IOError, FileNotFoundError):
        pass

# Favorites schema
# favorite_id|property_id

def load_favorites():
    favorites = []
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 2:
                    continue
                favorite = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1])
                }
                favorites.append(favorite)
    except (IOError, FileNotFoundError):
        favorites = []
    return favorites


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id'])
                ])
                f.write(line + '\n')
    except (IOError, FileNotFoundError):
        pass

# Agents schema
# agent_id|name|email|phone|agency

def load_agents():
    agents = []
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                agent = {
                    'agent_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'agency': parts[4]
                }
                agents.append(agent)
    except (IOError, FileNotFoundError):
        agents = []
    return agents


# Routes implementation per Section 1

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    featured_properties = [p for p in properties if p.get('is_featured')]
    # recent listings could be those sorted by property_id descending (newest ids)
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:10]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)

@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    locations = load_locations()
    filter_options = {
        'property_types': sorted(list(set(p['property_type'] for p in properties)))
    }
    if request.method == 'POST':
        # Retrieve filter values
        location_input = request.form.get('location_input', '').strip()
        try:
            price_min = float(request.form.get('price_range_min', '') or '0')
        except ValueError:
            price_min = 0
        try:
            price_max = float(request.form.get('price_range_max', '') or '1e15')
        except ValueError:
            price_max = 1e15
        property_type_filter = request.form.get('property_type_filter', '').strip()

        # Filter properties
        # First filter by location name if location_input given
        if location_input:
            # Match location ids with name containing location_input case insensitive
            matched_location_ids = [loc['location_id'] for loc in locations if location_input.lower() in loc['name'].lower()]
            properties = [p for p in properties if p['location_id'] in matched_location_ids]

        # Filter by property_type
        if property_type_filter:
            properties = [p for p in properties if p['property_type'].lower() == property_type_filter.lower()]

        # Filter by price range
        properties = [p for p in properties if price_min <= p['price'] <= price_max]

    return render_template('search.html', properties=properties, locations=locations, filter_options=filter_options)

@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    property = next((p for p in properties if p['property_id'] == property_id), None)
    if property is None:
        # Could render 404 or custom message (not in spec) - let's render with None
        property = None
    return render_template('property_details.html', property=property)

@app.route('/inquiry', methods=['GET'])
def property_inquiry():
    properties = load_properties()
    return render_template('inquiry.html', properties=properties)

@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    # Expected form data: select_property (int), inquiry_name (str), inquiry_email (str), 
    # inquiry_phone (str), inquiry_message (str)
    form = request.form
    try:
        select_property = int(form.get('select_property', ''))
        inquiry_name = form.get('inquiry_name', '').strip()
        inquiry_email = form.get('inquiry_email', '').strip()
        inquiry_phone = form.get('inquiry_phone', '').strip()
        inquiry_message = form.get('inquiry_message', '').strip()
    except Exception:
        # If any conversion or missing form error, reload inquiries with error (not specified) so just reload
        inquiries = load_inquiries()
        return render_template('inquiries.html', inquiries=inquiries, status_filter='')

    # Validate minimum required data
    if not (select_property and inquiry_name and inquiry_email):
        inquiries = load_inquiries()
        return render_template('inquiries.html', inquiries=inquiries, status_filter='')

    inquiries = load_inquiries()
    # Compute new inquiry_id
    max_id = max([inqu['inquiry_id'] for inqu in inquiries], default=0)
    new_inquiry = {
        'inquiry_id': max_id + 1,
        'property_id': select_property,
        'name': inquiry_name,
        'email': inquiry_email,
        'phone': inquiry_phone,
        'message': inquiry_message,
        'status': 'new'  # default status
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)
    # Redirect to inquiries page after submission (not specified but typical)
    return redirect(url_for('my_inquiries'))

@app.route('/inquiries')
def my_inquiries():
    inquiries = load_inquiries()
    status_filter = ''
    return render_template('inquiries.html', inquiries=inquiries, status_filter=status_filter)

@app.route('/inquiries/filter', methods=['POST'])
def filter_inquiries():
    inquiries = load_inquiries()
    inquiry_status_filter = request.form.get('inquiry_status_filter', '').strip()
    if inquiry_status_filter:
        inquiries = [inq for inq in inquiries if inq['status'].lower() == inquiry_status_filter.lower()]
    status_filter = inquiry_status_filter
    return render_template('inquiries.html', inquiries=inquiries, status_filter=status_filter)

@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    # Remove inquiry by id
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    status_filter = ''
    return render_template('inquiries.html', inquiries=inquiries, status_filter=status_filter)

@app.route('/favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties_dict=properties_dict)

@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    # Check if already in favorites
    if any(fav['property_id'] == property_id for fav in favorites):
        # no duplicates
        pass
    else:
        max_id = max([fav['favorite_id'] for fav in favorites], default=0)
        new_favorite = {
            'favorite_id': max_id + 1,
            'property_id': property_id
        }
        favorites.append(new_favorite)
        save_favorites(favorites)
    favorites = load_favorites()
    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties_dict=properties_dict)

@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    favorites = load_favorites()
    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties_dict=properties_dict)

@app.route('/agents', methods=['GET'])
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)

@app.route('/agents/search', methods=['POST'])
def search_agents():
    agent_search = request.form.get('agent_search', '').strip()
    agents = load_agents()
    if agent_search:
        agents = [a for a in agents if agent_search.lower() in a['name'].lower()]
    return render_template('agents.html', agents=agents)

@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    return render_template('locations.html', locations=locations)

@app.route('/locations/sort', methods=['POST'])
def sort_locations():
    location_sort = request.form.get('location_sort', '').strip()
    locations = load_locations()
    if location_sort:
        # Sort based on the given criteria: name, region, population
        if location_sort == 'name':
            locations.sort(key=lambda x: x['name'].lower())
        elif location_sort == 'region':
            locations.sort(key=lambda x: x['region'].lower())
        elif location_sort == 'population':
            locations.sort(key=lambda x: x['population'])
    return render_template('locations.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
