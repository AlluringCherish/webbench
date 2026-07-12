from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'

# Utility functions for data loading and saving

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
                        'price': float(parts[3]),
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
        pass
    return properties


def save_properties(properties):
    try:
        with open(PROPERTIES_FILE, 'w', encoding='utf-8') as f:
            for prop in properties:
                line = '|'.join([
                    str(prop['property_id']),
                    prop['address'],
                    prop['location'],
                    str(prop['price']),
                    prop['property_type'],
                    str(prop['bedrooms']),
                    str(prop['bathrooms']),
                    str(prop['square_feet']),
                    prop['description'],
                    str(prop['agent_id']),
                    prop['status']
                ])
                f.write(line + '\n')
    except IOError:
        pass


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
                        'average_price': float(parts[3]),
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
                        'inquiry_date': parts[6],
                        'status': parts[7]
                    }
                    inquiries.append(inquiry_dict)
    except IOError:
        pass
    return inquiries


def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
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
    except IOError:
        pass


def load_favorites():
    favorites = []
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    fav_dict = {
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    }
                    favorites.append(fav_dict)
    except IOError:
        pass
    return favorites


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id']),
                    fav['added_date']
                ])
                f.write(line + '\n')
    except IOError:
        pass


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


# Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    properties = load_properties()
    # Featured properties: For simplicity, features are the first 5 available properties
    featured_properties = [p for p in properties if p['status'] == 'Available'][:5]
    # Recent listings: last 5 properties by property_id descending
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET'])
def property_search_page():
    properties = load_properties()
    # No filters applied initially
    filter_location = ''
    min_price = None
    max_price = None
    property_type_filter = ''
    return render_template('search.html', properties=properties, filter_location=filter_location, min_price=min_price, max_price=max_price, property_type_filter=property_type_filter)


@app.route('/search', methods=['POST'])
def property_search_filter():
    location = request.form.get('location', '').strip()
    min_price_str = request.form.get('min_price', '').strip()
    max_price_str = request.form.get('max_price', '').strip()
    property_type = request.form.get('property_type', '').strip()

    try:
        min_price = float(min_price_str) if min_price_str else None
    except ValueError:
        min_price = None
    try:
        max_price = float(max_price_str) if max_price_str else None
    except ValueError:
        max_price = None

    properties = load_properties()
    filtered_properties = []
    for prop in properties:
        if location and location.lower() not in prop['location'].lower():
            continue
        if min_price is not None and prop['price'] < min_price:
            continue
        if max_price is not None and prop['price'] > max_price:
            continue
        if property_type and property_type.lower() != prop['property_type'].lower():
            continue
        filtered_properties.append(prop)

    return render_template('search.html', properties=filtered_properties, filter_location=location, min_price=min_price, max_price=max_price, property_type_filter=property_type)


@app.route('/property/<int:property_id>', methods=['GET'])
def property_details_page(property_id):
    properties = load_properties()
    property_found = None
    for prop in properties:
        if prop['property_id'] == property_id:
            property_found = prop
            break
    if property_found is None:
        # Property not found, return 404 or render not found page optionally
        return "Property not found", 404
    return render_template('property_details.html', property=property_found)


@app.route('/property/<int:property_id>/add_favorite', methods=['POST'])
def add_favorite(property_id):
    # Check if property exists
    properties = load_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return "Property not found", 404

    favorites = load_favorites()
    # Check duplicates - if property already favorited, do nothing
    if any(f['property_id'] == property_id for f in favorites):
        pass
    else:
        # Generate new favorite_id
        new_id = max([f['favorite_id'] for f in favorites], default=0) + 1
        today_str = datetime.now().strftime('%Y-%m-%d')
        favorites.append({'favorite_id': new_id, 'property_id': property_id, 'added_date': today_str})
        save_favorites(favorites)

    return redirect(url_for('property_details_page', property_id=property_id))


@app.route('/property/<int:property_id>/submit_inquiry', methods=['POST'])
def submit_inquiry_from_details(property_id):
    # Validate property exists
    properties = load_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return "Property not found", 404

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()

    if not (name and email and phone and message):
        # Missing form data
        return "Missing form data", 400

    inquiries = load_inquiries()
    new_id = max([i['inquiry_id'] for i in inquiries], default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    inquiries.append({
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': name,
        'customer_email': email,
        'customer_phone': phone,
        'message': message,
        'inquiry_date': today_str,
        'status': 'Pending'
    })
    save_inquiries(inquiries)

    return redirect(url_for('inquiry_page'))


@app.route('/inquiry', methods=['GET'])
def inquiry_page():
    properties = load_properties()
    available_properties = [p for p in properties if p['status'] == 'Available']
    return render_template('inquiry.html', properties=available_properties)


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    property_id_str = request.form.get('property_id', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()

    try:
        property_id = int(property_id_str)
    except ValueError:
        return "Invalid property ID", 400

    if not (name and email and phone and message):
        return "Missing form data", 400

    properties = load_properties()
    if not any(p['property_id'] == property_id and p['status'] == 'Available' for p in properties):
        return "Property not available", 400

    inquiries = load_inquiries()
    new_id = max([i['inquiry_id'] for i in inquiries], default=0) + 1
    today_str = datetime.now().strftime('%Y-%m-%d')
    inquiries.append({
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': name,
        'customer_email': email,
        'customer_phone': phone,
        'message': message,
        'inquiry_date': today_str,
        'status': 'Pending'
    })
    save_inquiries(inquiries)

    return redirect(url_for('my_inquiries_page'))


@app.route('/my_inquiries', methods=['GET'])
def my_inquiries_page():
    inquiries = load_inquiries()
    status_filter = request.args.get('status_filter', '').strip()
    if status_filter:
        inquiries = [i for i in inquiries if i['status'].lower() == status_filter.lower()]
    return render_template('my_inquiries.html', inquiries=inquiries, status_filter=status_filter)


@app.route('/my_inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))


@app.route('/my_favorites', methods=['GET'])
def my_favorites_page():
    favorites = load_favorites()
    properties = load_properties()

    favorite_properties = []
    favorite_property_ids = {f['property_id'] for f in favorites}

    for prop in properties:
        if prop['property_id'] in favorite_property_ids:
            favorite_properties.append(prop)

    return render_template('my_favorites.html', favorite_properties=favorite_properties)


@app.route('/my_favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites_page'))


@app.route('/agents', methods=['GET'])
def agents_page():
    agents = load_agents()
    agent_search_query = request.args.get('agent_search_query', '').strip()

    if agent_search_query:
        agents = [a for a in agents if agent_search_query.lower() in a['agent_name'].lower()]

    return render_template('agents.html', agents=agents, agent_search_query=agent_search_query)


@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    location_sort = request.args.get('location_sort', '').strip()

    if location_sort == 'average_price':
        locations = sorted(locations, key=lambda x: x['average_price'])
    elif location_sort == 'property_count':
        locations = sorted(locations, key=lambda x: x['property_count'])

    return render_template('locations.html', locations=locations, location_sort=location_sort)


if __name__ == '__main__':
    app.run(debug=True)
