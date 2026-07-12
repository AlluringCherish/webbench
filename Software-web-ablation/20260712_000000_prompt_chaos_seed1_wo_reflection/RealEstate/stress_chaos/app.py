from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# File paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'


# Utility functions to load data

def load_properties():
    properties = []
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
                    property_dict = {
                        'property_id': int(parts[0]),
                        'address': parts[1],
                        'location': parts[2],
                        'price': int(parts[3]) if parts[3].isdigit() else float(parts[3]),
                        'property_type': parts[4],
                        'bedrooms': int(parts[5]),
                        'bathrooms': float(parts[6]),
                        'square_feet': int(parts[7]),
                        'description': parts[8],
                        'agent_id': int(parts[9]),
                        'status': parts[10]
                    }
                    properties.append(property_dict)
    except IOError:
        # File missing or unreadable
        pass
    return properties


def load_locations():
    locations = []
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    location_dict = {
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': int(parts[3]) if parts[3].isdigit() else float(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    }
                    locations.append(location_dict)
    except IOError:
        pass
    return locations


def load_inquiries():
    inquiries = []
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    inquiry_dict = {
                        'inquiry_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],  # string date
                        'status': parts[7]
                    }
                    inquiries.append(inquiry_dict)
    except IOError:
        pass
    return inquiries


def load_favorites():
    favorites = []
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    favorite_dict = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(favorite_dict)
    except IOError:
        pass
    return favorites


def load_agents():
    agents = []
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    agent_dict = {
                        'agent_id': int(parts[0]),
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    }
                    agents.append(agent_dict)
    except IOError:
        pass
    return agents


# Saving functions (overwrite files)

def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = f"{inq['inquiry_id']}|{inq['property_id']}|{inq['customer_name']}|{inq['customer_email']}|{inq['customer_phone']}|{inq['message']}|{inq['inquiry_date']}|{inq['status']}\n"
                f.write(line)
    except IOError:
        pass


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
    except IOError:
        pass


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_properties: list of dict
    # We can treat featured properties as those with status 'Available' and sort or just return first available
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available'][:10]
    return render_template('dashboard.html', featured_properties=featured_properties)


@app.route('/search')
def property_search():
    properties = load_properties()

    # Extract filter parameters
    filter_location = request.args.get('location')
    filter_price_min = request.args.get('price_min')
    filter_price_max = request.args.get('price_max')
    filter_property_type = request.args.get('property_type')

    # Parse numeric filters safely
    try:
        filter_price_min_val = float(filter_price_min) if filter_price_min is not None and filter_price_min != '' else None
    except ValueError:
        filter_price_min_val = None
    try:
        filter_price_max_val = float(filter_price_max) if filter_price_max is not None and filter_price_max != '' else None
    except ValueError:
        filter_price_max_val = None

    # Filtering
    filtered_properties = []
    for prop in properties:
        if prop['status'] != 'Available':
            continue
        if filter_location and prop['location'].lower() != filter_location.lower():
            continue
        if filter_property_type and filter_property_type != '' and prop['property_type'].lower() != filter_property_type.lower():
            continue
        price = prop['price']
        if filter_price_min_val is not None and price < filter_price_min_val:
            continue
        if filter_price_max_val is not None and price > filter_price_max_val:
            continue
        filtered_properties.append(prop)

    return render_template('search.html', 
                           properties=filtered_properties,
                           filter_location=filter_location or '',
                           filter_price_min=filter_price_min_val,
                           filter_price_max=filter_price_max_val,
                           filter_property_type=filter_property_type if filter_property_type != '' else None)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()
    favorites = load_favorites()

    # Find property
    property_obj = None
    for p in properties:
        if p['property_id'] == property_id:
            property_obj = p
            break
    if property_obj is None:
        # Could handle 404, but spec does not mention this, render with empty context
        property_obj = {}

    # Find agent for property
    agent_obj = None
    if property_obj and 'agent_id' in property_obj:
        for a in agents:
            if a['agent_id'] == property_obj['agent_id']:
                agent_obj = a
                break

    # Check if property is favorite
    is_favorite = any(f['property_id'] == property_id for f in favorites)

    return render_template('property_details.html', property=property_obj, agent=agent_obj, is_favorite=is_favorite)


@app.route('/inquiry', methods=['GET'])
def inquiry_page():
    properties = load_properties()
    return render_template('inquiry.html', properties=properties)


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    inquiry_name = request.form.get('inquiry_name')
    inquiry_email = request.form.get('inquiry_email')
    inquiry_phone = request.form.get('inquiry_phone')
    inquiry_message = request.form.get('inquiry_message')
    select_property = request.form.get('select_property')

    error = False
    # Validate required fields
    if not inquiry_name or not inquiry_email or not inquiry_phone or not inquiry_message or not select_property:
        error = True

    try:
        property_id = int(select_property)
    except (ValueError, TypeError):
        error = True

    # If any error in inputs, re-render inquiry.html with properties
    if error:
        properties = load_properties()
        return render_template('inquiry.html', properties=properties)

    # Load inquiries and add new inquiry
    inquiries = load_inquiries()
    # Prepare new inquiry_id
    max_id = max([inq['inquiry_id'] for inq in inquiries], default=0)
    new_id = max_id + 1

    # Format current date as YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': inquiry_name,
        'customer_email': inquiry_email,
        'customer_phone': inquiry_phone,
        'message': inquiry_message,
        'inquiry_date': current_date,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    # Redirect to inquiries page after successful submission
    return redirect(url_for('my_inquiries'))


@app.route('/inquiries')
def my_inquiries():
    inquiries = load_inquiries()
    status_filter = request.args.get('status_filter', 'All')

    if status_filter != 'All':
        filtered_inquiries = [inq for inq in inquiries if inq['status'].lower() == status_filter.lower()]
    else:
        filtered_inquiries = inquiries

    return render_template('inquiries.html', inquiries=filtered_inquiries, status_filter=status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)

    return redirect(url_for('my_inquiries'))


@app.route('/favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()

    # Sort favorites by added_date descending if dates present
    favorites_sorted = sorted(favorites, key=lambda x: x['added_date'], reverse=True)

    return render_template('favorites.html', favorites=favorites_sorted, properties=properties)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    # Check if already favorite
    for fav in favorites:
        if fav['property_id'] == property_id:
            # Already favorite, redirect to property details
            return redirect(url_for('property_details', property_id=property_id))

    # Prepare new favorite_id
    max_id = max([fav['favorite_id'] for fav in favorites], default=0)
    new_id = max_id + 1
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Add favorite
    favorites.append({'favorite_id': new_id, 'property_id': property_id, 'added_date': current_date})
    save_favorites(favorites)

    return redirect(url_for('property_details', property_id=property_id))


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)

    return redirect(url_for('my_favorites'))


@app.route('/agents')
def agents_directory():
    agents = load_agents()
    filter_name = request.args.get('filter_name')

    if filter_name and filter_name.strip() != '':
        filtered_agents = [a for a in agents if filter_name.lower() in a['agent_name'].lower()]
    else:
        filtered_agents = agents

    return render_template('agents.html', agents=filtered_agents, filter_name=filter_name)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_by = request.args.get('sort_by')

    if sort_by == 'By Name':
        locations = sorted(locations, key=lambda x: x['location_name'].lower())
    elif sort_by == 'By Properties Count':
        locations = sorted(locations, key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Average Price':
        locations = sorted(locations, key=lambda x: x['average_price'], reverse=True)

    return render_template('locations.html', locations=locations, sort_by=sort_by)


if __name__ == '__main__':
    app.run(debug=True)
