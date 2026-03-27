from flask import Flask, render_template, redirect, url_for, request
import os
import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data files

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.exists(path):
        return properties
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 11:
                continue
            try:
                prop = {
                    'property_id': int(parts[0]),
                    'address': parts[1],
                    'location': parts[2],
                    'price': int(parts[3]),
                    'property_type': parts[4],
                    'bedrooms': int(parts[5]),
                    'bathrooms': float(parts[6]),
                    'square_feet': int(parts[7]),
                    'description': parts[8],
                    'agent_id': int(parts[9]),
                    'status': parts[10]
                }
                properties.append(prop)
            except ValueError:
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
                    str(p['price']),
                    p['property_type'],
                    str(p['bedrooms']),
                    str(p['bathrooms']),
                    str(p['square_feet']),
                    p['description'],
                    str(p['agent_id']),
                    p['status']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                loc = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': int(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                }
                locations.append(loc)
            except ValueError:
                continue
    return locations


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    if not os.path.exists(path):
        return inquiries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                inq = {
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'customer_phone': parts[4],
                    'message': parts[5],
                    'inquiry_date': parts[6],
                    'status': parts[7]
                }
                inquiries.append(inq)
            except ValueError:
                continue
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = '|'.join([
                    str(inq['inquiry_id']),
                    str(inq['property_id']),
                    inq['customer_name'],
                    inq['customer_email'],
                    inq['customer_phone'],
                    inq['message'],
                    inq['inquiry_date'],
                    inq['status']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                fav = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                }
                favorites.append(fav)
            except ValueError:
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
    except Exception:
        pass


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.exists(path):
        return agents
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                agent = {
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5])
                }
                agents.append(agent)
            except ValueError:
                continue
    return agents

# Validators

email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def is_valid_email(email):
    return bool(email_pattern.match(email))


def today_date_str():
    return datetime.date.today().strftime('%Y-%m-%d')


# Routes Implementation

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    properties = load_properties()
    # featured_properties: pick with status Available, by first 5 sorted by price descending
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['price'], reverse=True)
    featured_properties = featured_properties[:5]

    # recent_listings: last 5 properties by highest property_id (assuming recent added)
    properties_sorted = sorted(properties, key=lambda x: x['property_id'], reverse=True)
    recent_listings = properties_sorted[:5]

    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    locations = load_locations()

    applied_filters = {
        'location': '',
        'price_min': None,
        'price_max': None,
        'property_type': None
    }

    filtered_properties = properties

    if request.method == 'POST':
        location_input = request.form.get('location-input', '').strip()
        price_min_str = request.form.get('price-range-min', '').strip()
        price_max_str = request.form.get('price-range-max', '').strip()
        property_type_filter = request.form.get('property-type-filter', '').strip()

        if location_input:
            applied_filters['location'] = location_input

        # price_min
        if price_min_str.isdigit():
            applied_filters['price_min'] = int(price_min_str)
        else:
            applied_filters['price_min'] = None

        # price_max
        if price_max_str.isdigit():
            applied_filters['price_max'] = int(price_max_str)
        else:
            applied_filters['price_max'] = None

        if property_type_filter in ['House', 'Apartment', 'Condo', 'Land']:
            applied_filters['property_type'] = property_type_filter
        else:
            applied_filters['property_type'] = None

        # Filter properties
        filtered_properties = []
        for prop in properties:
            if applied_filters['location'] and prop['location'].lower() != applied_filters['location'].lower():
                continue
            if applied_filters['price_min'] is not None and prop['price'] < applied_filters['price_min']:
                continue
            if applied_filters['price_max'] is not None and prop['price'] > applied_filters['price_max']:
                continue
            if applied_filters['property_type'] is not None and prop['property_type'] != applied_filters['property_type']:
                continue
            filtered_properties.append(prop)
    else:
        # On GET, no filter applied
        filtered_properties = properties

    return render_template('search.html', properties=filtered_properties, locations=locations, applied_filters=applied_filters)


@app.route('/property/<int:property_id>', methods=['GET'])
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()

    property_data = None
    for p in properties:
        if p['property_id'] == property_id:
            property_data = p
            break

    if property_data is None:
        # Property not found, return 404 page or redirect to dashboard
        return redirect(url_for('dashboard'))

    agent_data = None
    for a in agents:
        if a['agent_id'] == property_data['agent_id']:
            agent_data = a
            break

    return render_template('property_details.html', property=property_data, agent=agent_data)


@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = load_properties()
    form_errors = {}

    if request.method == 'POST':
        select_property_str = request.form.get('select_property', '').strip()
        inquiry_name = request.form.get('inquiry_name', '').strip()
        inquiry_email = request.form.get('inquiry_email', '').strip()
        inquiry_phone = request.form.get('inquiry_phone', '').strip()
        inquiry_message = request.form.get('inquiry_message', '').strip()

        # Validate select_property presence and valid int
        try:
            select_property = int(select_property_str)
        except ValueError:
            form_errors['select_property'] = 'Invalid property selected.'
            select_property = None

        if select_property is not None:
            # Verify property exists
            valid_property_ids = {p['property_id'] for p in properties}
            if select_property not in valid_property_ids:
                form_errors['select_property'] = 'Selected property does not exist.'

        # Validate inquiry_name
        if not inquiry_name:
            form_errors['inquiry_name'] = 'Name is required.'

        # Validate inquiry_email
        if not inquiry_email:
            form_errors['inquiry_email'] = 'Email is required.'
        elif not is_valid_email(inquiry_email):
            form_errors['inquiry_email'] = 'Invalid email format.'

        # inquiry_phone no format specified except input type tel - allow any string but require non-empty
        if not inquiry_phone:
            form_errors['inquiry_phone'] = 'Phone number is required.'

        # inquiry_message required
        if not inquiry_message:
            form_errors['inquiry_message'] = 'Message is required.'

        if not form_errors:
            # Save inquiry
            inquiries = load_inquiries()
            next_id = 1
            if inquiries:
                next_id = max(i['inquiry_id'] for i in inquiries) + 1

            today = today_date_str()
            new_inquiry = {
                'inquiry_id': next_id,
                'property_id': select_property,
                'customer_name': inquiry_name,
                'customer_email': inquiry_email,
                'customer_phone': inquiry_phone,
                'message': inquiry_message,
                'inquiry_date': today,
                'status': 'Pending'
            }
            inquiries.append(new_inquiry)
            save_inquiries(inquiries)

            # Redirect to inquiries page
            return redirect(url_for('my_inquiries'))

    return render_template('inquiry.html', properties=properties, form_errors=form_errors)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    inquiries = load_inquiries()
    inquiry_status_filter = 'All'

    if request.method == 'POST':
        # Check if deleting inquiry
        delete_inquiry_id = None
        for key in request.form.keys():
            if key.startswith('delete-inquiry-button-'):
                # Extract inquiry id from button name
                try:
                    delete_inquiry_id = int(key[len('delete-inquiry-button-'):])
                except ValueError:
                    delete_inquiry_id = None
                break

        if delete_inquiry_id is not None:
            # Remove the inquiry with the given id
            inquiries = [i for i in inquiries if i['inquiry_id'] != delete_inquiry_id]
            save_inquiries(inquiries)

        # Reload inquiries after deletion
        inquiries = load_inquiries()

        # Filter selection
        inquiry_status_filter = request.form.get('inquiry_status_filter', 'All')
    else:
        inquiry_status_filter = 'All'

    # Filter inquiries by status
    if inquiry_status_filter and inquiry_status_filter != 'All':
        filtered_inquiries = [i for i in inquiries if i['status'] == inquiry_status_filter]
    else:
        filtered_inquiries = inquiries

    return render_template('inquiries.html', inquiries=filtered_inquiries, inquiry_status_filter=inquiry_status_filter)


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_map = {p['property_id']: p for p in properties}

    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        property_id_str = request.form.get('property_id', '').strip()
        try:
            property_id = int(property_id_str)
        except ValueError:
            property_id = None

        if action == 'add' and property_id is not None:
            # Check if property exists
            if property_id in properties_map:
                # Check if favorite already exists
                exists = any(f['property_id'] == property_id for f in favorites)
                if not exists:
                    next_id = 1
                    if favorites:
                        next_id = max(f['favorite_id'] for f in favorites) + 1
                    fav_entry = {
                        'favorite_id': next_id,
                        'property_id': property_id,
                        'added_date': today_date_str()
                    }
                    favorites.append(fav_entry)
                    save_favorites(favorites)
        elif action == 'remove' and property_id is not None:
            favorites = [f for f in favorites if f['property_id'] != property_id]
            save_favorites(favorites)

    favorites = load_favorites()  # Reload to reflect changes
    return render_template('favorites.html', favorites=favorites, properties_map=properties_map)


@app.route('/agents', methods=['GET'])
def agents_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    locations_data = load_locations()
    sort_by = 'name'

    if request.method == 'POST':
        location_sort = request.form.get('location_sort', '').strip()
        if location_sort in ['name', 'properties_count', 'average_price']:
            sort_by = location_sort
    else:
        sort_by = 'name'

    if sort_by == 'name':
        locations_data.sort(key=lambda x: x['location_name'].lower())
    elif sort_by == 'properties_count':
        locations_data.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'average_price':
        locations_data.sort(key=lambda x: x['average_price'], reverse=True)

    return render_template('locations.html', locations=locations_data, sort_by=sort_by)


if __name__ == '__main__':
    app.run(debug=True)
