from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for loading and saving data

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.isfile(path):
        return properties
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 11:
                continue
            try:
                property_id = int(parts[0])
                address = parts[1]
                location = parts[2]
                price = float(parts[3])
                property_type = parts[4]
                bedrooms = int(parts[5])
                bathrooms = float(parts[6])
                square_feet = int(parts[7])
                description = parts[8]
                agent_id = int(parts[9])
                status = parts[10]
                prop = {
                    'property_id': property_id,
                    'address': address,
                    'location': location,
                    'price': price,
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'square_feet': square_feet,
                    'description': description,
                    'agent_id': agent_id,
                    'status': status
                }
                properties.append(prop)
            except:
                continue
    return properties


def save_properties(properties):
    path = os.path.join(DATA_DIR, 'properties.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for p in properties:
                line = '|'.join([
                    str(p['property_id']),
                    p['address'],
                    p['location'],
                    f"{p['price']:.2f}",
                    p['property_type'],
                    str(p['bedrooms']),
                    str(p['bathrooms']),
                    str(p['square_feet']),
                    p['description'],
                    str(p['agent_id']),
                    p['status']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.isfile(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                location_id = int(parts[0])
                location_name = parts[1]
                region = parts[2]
                average_price = float(parts[3])
                property_count = int(parts[4])
                description = parts[5]
                loc = {
                    'location_id': location_id,
                    'location_name': location_name,
                    'region': region,
                    'average_price': average_price,
                    'property_count': property_count,
                    'description': description
                }
                locations.append(loc)
            except:
                continue
    return locations


def save_locations(locations):
    path = os.path.join(DATA_DIR, 'locations.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for l in locations:
                line = '|'.join([
                    str(l['location_id']),
                    l['location_name'],
                    l['region'],
                    f"{l['average_price']:.2f}",
                    str(l['property_count']),
                    l['description']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    if not os.path.isfile(path):
        return inquiries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 8:
                continue
            try:
                inquiry_id = int(parts[0])
                property_id = int(parts[1])
                customer_name = parts[2]
                customer_email = parts[3]
                customer_phone = parts[4]
                message = parts[5]
                inquiry_date = parts[6]
                status = parts[7]
                inq = {
                    'inquiry_id': inquiry_id,
                    'property_id': property_id,
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'message': message,
                    'inquiry_date': inquiry_date,
                    'status': status
                }
                inquiries.append(inq)
            except:
                continue
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for i in inquiries:
                line = '|'.join([
                    str(i['inquiry_id']),
                    str(i['property_id']),
                    i['customer_name'],
                    i['customer_email'],
                    i['customer_phone'],
                    i['message'],
                    i['inquiry_date'],
                    i['status']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.isfile(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            try:
                favorite_id = int(parts[0])
                property_id = int(parts[1])
                added_date = parts[2]
                fav = {
                    'favorite_id': favorite_id,
                    'property_id': property_id,
                    'added_date': added_date
                }
                favorites.append(fav)
            except:
                continue
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id']),
                    fav['added_date']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.isfile(path):
        return agents
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                agent_id = int(parts[0])
                agent_name = parts[1]
                specialization = parts[2]
                email = parts[3]
                phone = parts[4]
                properties_sold = int(parts[5])
                ag = {
                    'agent_id': agent_id,
                    'agent_name': agent_name,
                    'specialization': specialization,
                    'email': email,
                    'phone': phone,
                    'properties_sold': properties_sold
                }
                agents.append(ag)
            except:
                continue
    return agents


def save_agents(agents):
    path = os.path.join(DATA_DIR, 'agents.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for ag in agents:
                line = '|'.join([
                    str(ag['agent_id']),
                    ag['agent_name'],
                    ag['specialization'],
                    ag['email'],
                    ag['phone'],
                    str(ag['properties_sold'])
                ])
                f.write(line + '\n')
        return True
    except:
        return False


# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    # Featured: Let's choose first 5 available properties sorted by price desc
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['price'], reverse=True)
    featured_properties = featured_properties[:5]
    # Recent listings: last 5 properties by property_id descending
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    locations = load_locations()
    filter_options = {
        'location_input': '',
        'min_price': 0.0,
        'max_price': float('inf'),
        'property_type': ''
    }

    if request.method == 'POST':
        location_input = request.form.get('location_input', '').strip()
        price_range_min = request.form.get('price_range_min', '').strip()
        price_range_max = request.form.get('price_range_max', '').strip()
        property_type_filter = request.form.get('property_type_filter', '').strip()

        # Validate and parse inputs
        try:
            min_price = float(price_range_min) if price_range_min else 0.0
        except:
            min_price = 0.0
        try:
            max_price = float(price_range_max) if price_range_max else float('inf')
        except:
            max_price = float('inf')

        # Filter properties
        filtered_props = []
        for prop in properties:
            if prop['status'] != 'Available':
                continue
            if location_input and location_input.lower() not in prop['location'].lower():
                continue
            if not(min_price <= prop['price'] <= max_price):
                continue
            if property_type_filter and property_type_filter.lower() != prop['property_type'].lower():
                continue
            filtered_props.append(prop)

        filter_options = {
            'location_input': location_input,
            'min_price': min_price,
            'max_price': max_price,
            'property_type': property_type_filter
        }
        properties = filtered_props

    else:
        # GET: show all available properties without filters
        properties = [p for p in properties if p['status'] == 'Available']

    return render_template('search.html', properties=properties, locations=locations, filter_options=filter_options)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if prop is None:
        return "Property Not Found", 404
    return render_template('property_details.html', property=prop)


@app.route('/inquiry', methods=['GET'])
def property_inquiry():
    properties = load_properties()
    properties = [p for p in properties if p['status'] == 'Available']
    return render_template('inquiry.html', properties=properties)


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    properties = load_properties()
    inquiries = load_inquiries()

    # Get form data
    try:
        select_property = int(request.form.get('select_property', '').strip())
        inquiry_name = request.form.get('inquiry_name', '').strip()
        inquiry_email = request.form.get('inquiry_email', '').strip()
        inquiry_phone = request.form.get('inquiry_phone', '').strip()
        inquiry_message = request.form.get('inquiry_message', '').strip()
    except:
        return "Invalid form data", 400

    # Validate property selected and data presence
    prop = next((p for p in properties if p['property_id'] == select_property and p['status'] == 'Available'), None)
    if not prop:
        return "Invalid property selection", 400
    if not (inquiry_name and inquiry_email and inquiry_phone and inquiry_message):
        return "All fields required", 400

    # Assign a new inquiry ID
    new_id = 1
    if inquiries:
        new_id = max(i['inquiry_id'] for i in inquiries) + 1

    today_str = datetime.now().strftime('%Y-%m-%d')
    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': prop['property_id'],
        'customer_name': inquiry_name,
        'customer_email': inquiry_email,
        'customer_phone': inquiry_phone,
        'message': inquiry_message,
        'inquiry_date': today_str,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    return render_template('inquiries.html', inquiries=inquiries, status_filter='')


@app.route('/inquiries', methods=['GET'])
def my_inquiries():
    inquiries = load_inquiries()
    return render_template('inquiries.html', inquiries=inquiries, status_filter='')


@app.route('/inquiries/filter', methods=['POST'])
def filter_inquiries():
    inquiries = load_inquiries()
    inquiry_status_filter = request.form.get('inquiry_status_filter', '').strip()
    if inquiry_status_filter:
        filtered = [i for i in inquiries if i['status'].lower() == inquiry_status_filter.lower()]
    else:
        filtered = inquiries
    return render_template('inquiries.html', inquiries=filtered, status_filter=inquiry_status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return render_template('inquiries.html', inquiries=inquiries, status_filter='')


@app.route('/favorites', methods=['GET'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    # Return only favorites with properties that exist
    favorites = [f for f in favorites if f['property_id'] in properties_dict]
    return render_template('favorites.html', favorites=favorites, properties=properties_dict)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    # Check if already in favorites
    if any(f['property_id'] == property_id for f in favorites):
        # No duplicate favorites
        properties = load_properties()
        properties_dict = {p['property_id']: p for p in properties}
        return render_template('favorites.html', favorites=favorites, properties=properties_dict)

    # Assign new favorite ID
    new_id = 1
    if favorites:
        new_id = max(f['favorite_id'] for f in favorites) + 1

    today_str = datetime.now().strftime('%Y-%m-%d')
    new_favorite = {
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': today_str
    }
    favorites.append(new_favorite)
    save_favorites(favorites)

    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties=properties_dict)


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)

    properties = load_properties()
    properties_dict = {p['property_id']: p for p in properties}
    return render_template('favorites.html', favorites=favorites, properties=properties_dict)


@app.route('/agents', methods=['GET'])
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/agents/search', methods=['POST'])
def search_agents():
    agents = load_agents()
    agent_search = request.form.get('agent_search', '').strip()
    if agent_search:
        filtered_agents = [a for a in agents if agent_search.lower() in a['agent_name'].lower()]
    else:
        filtered_agents = agents
    return render_template('agents.html', agents=filtered_agents)


@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    sort_option = ''
    return render_template('locations.html', locations=locations, sort_option=sort_option)


@app.route('/locations/sort', methods=['POST'])
def sort_locations():
    locations = load_locations()
    location_sort = request.form.get('location_sort', '').strip()

    if location_sort == 'name_asc':
        locations.sort(key=lambda x: x['location_name'])
    elif location_sort == 'name_desc':
        locations.sort(key=lambda x: x['location_name'], reverse=True)
    elif location_sort == 'price_asc':
        locations.sort(key=lambda x: x['average_price'])
    elif location_sort == 'price_desc':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    elif location_sort == 'count_asc':
        locations.sort(key=lambda x: x['property_count'])
    elif location_sort == 'count_desc':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    else:
        # default no sort
        pass

    sort_option = location_sort
    return render_template('locations.html', locations=locations, sort_option=sort_option)


if __name__ == '__main__':
    app.run(debug=True)
