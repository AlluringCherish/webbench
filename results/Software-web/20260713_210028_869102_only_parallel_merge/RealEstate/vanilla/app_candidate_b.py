from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to load data from text files

def load_properties():
    properties = []
    try:
        with open(os.path.join(DATA_DIR, 'properties.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (property_id, address, location, price, property_type, bedrooms, bathrooms, square_feet, description, agent_id, status) = line.split('|')
                properties.append({
                    'property_id': int(property_id),
                    'address': address,
                    'location': location,
                    'price': int(price),
                    'property_type': property_type,
                    'bedrooms': int(bedrooms),
                    'bathrooms': float(bathrooms),
                    'square_feet': int(square_feet),
                    'description': description,
                    'agent_id': int(agent_id),
                    'status': status
                })
    except Exception as e:
        # In case of file error or parse error return empty list
        properties = []
    return properties


def load_agents():
    agents = []
    try:
        with open(os.path.join(DATA_DIR, 'agents.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (agent_id, agent_name, specialization, email, phone, properties_sold) = line.split('|')
                agents.append({
                    'agent_id': int(agent_id),
                    'agent_name': agent_name,
                    'specialization': specialization,
                    'email': email,
                    'phone': phone,
                    'properties_sold': int(properties_sold)
                })
    except Exception as e:
        agents = []
    return agents


def load_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (location_id, location_name, region, average_price, property_count, description) = line.split('|')
                locations.append({
                    'location_id': int(location_id),
                    'location_name': location_name,
                    'region': region,
                    'average_price': int(average_price),
                    'property_count': int(property_count),
                    'description': description
                })
    except Exception as e:
        locations = []
    return locations


def load_inquiries():
    inquiries = []
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (inquiry_id, property_id, customer_name, customer_email, customer_phone, message, inquiry_date, status) = line.split('|')
                inquiries.append({
                    'inquiry_id': int(inquiry_id),
                    'property_id': int(property_id),
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'message': message,
                    'inquiry_date': inquiry_date,
                    'status': status
                })
    except Exception as e:
        inquiries = []
    return inquiries


def load_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                (favorite_id, property_id, added_date) = line.split('|')
                favorites.append({
                    'favorite_id': int(favorite_id),
                    'property_id': int(property_id),
                    'added_date': added_date
                })
    except Exception as e:
        favorites = []
    return favorites


def save_inquiries(inquiries):
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'w', encoding='utf-8') as f:
            for inquiry in inquiries:
                f.write(f"{inquiry['inquiry_id']}|{inquiry['property_id']}|{inquiry['customer_name']}|{inquiry['customer_email']}|{inquiry['customer_phone']}|{inquiry['message']}|{inquiry['inquiry_date']}|{inquiry['status']}\n")
        return True
    except Exception as e:
        return False


def save_favorites(favorites):
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w', encoding='utf-8') as f:
            for fav in favorites:
                f.write(f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n")
        return True
    except Exception as e:
        return False


# Utility to find property by id

def get_property_by_id(property_id):
    properties = load_properties()
    for p in properties:
        if p['property_id'] == property_id:
            return p
    return None

# Utility to find agent by id

def get_agent_by_id(agent_id):
    agents = load_agents()
    for a in agents:
        if a['agent_id'] == agent_id:
            return a
    return None

# Dashboard route
@app.route('/')
def dashboard():
    properties = load_properties()
    # Show featured properties - choose the first 5 available for demo
    featured_properties = [p for p in properties if p['status'].lower() == 'available'][:5]
    return render_template('dashboard.html', featured_properties=featured_properties)


# Property Search route
@app.route('/search')
def property_search():
    location_filter = request.args.get('location', '').strip()
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    property_type = request.args.get('property_type', '')

    price_min_val = int(price_min) if price_min and price_min.isdigit() else None
    price_max_val = int(price_max) if price_max and price_max.isdigit() else None
    property_type_val = property_type if property_type in ['House', 'Apartment', 'Condo', 'Land'] else None

    properties = load_properties()
    # Filter only available
    properties = [p for p in properties if p['status'].lower() == 'available']

    # Apply filters
    filtered_properties = []
    for p in properties:
        if location_filter and location_filter.lower() not in p['location'].lower():
            continue
        if price_min_val is not None and p['price'] < price_min_val:
            continue
        if price_max_val is not None and p['price'] > price_max_val:
            continue
        if property_type_val and p['property_type'] != property_type_val:
            continue
        filtered_properties.append(p)

    return render_template('property_search.html', properties=filtered_properties,
                           filter_location=location_filter,
                           filter_price_min=price_min_val,
                           filter_price_max=price_max_val,
                           filter_property_type=property_type_val)


# Property Details route
@app.route('/property/<int:property_id>')
def property_details(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return "Property not found", 404

    agent = get_agent_by_id(property['agent_id'])

    favorites = load_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)

    return render_template('property_details.html', property=property, agent=agent, is_favorite=is_favorite)


# Add to favorites route
@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    next_id = max([f['favorite_id'] for f in favorites], default=0) + 1
    added_date = datetime.now().strftime('%Y-%m-%d')

    # Avoid duplicates
    if any(fav['property_id'] == property_id for fav in favorites):
        return redirect(url_for('property_details', property_id=property_id))

    favorites.append({
        'favorite_id': next_id,
        'property_id': property_id,
        'added_date': added_date
    })
    save_favorites(favorites)
    return redirect(url_for('property_details', property_id=property_id))


# Property Inquiry page
@app.route('/inquiry/submit', methods=['GET', 'POST'])
def property_inquiry():
    submission_status = None
    properties = load_properties()
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        message = request.form.get('message', '').strip()

        # Validate property_id exists
        try:
            property_id = int(property_id)
        except:
            submission_status = "Invalid property selection."
            return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)

        if not get_property_by_id(property_id):
            submission_status = "Selected property does not exist."
            return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)

        if not customer_name or not customer_email or not message:
            submission_status = "Name, Email, and Message are required."
            return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)

        inquiries = load_inquiries()
        next_id = max([i['inquiry_id'] for i in inquiries], default=0) + 1
        inquiry_date = datetime.now().strftime('%Y-%m-%d')
        inquiries.append({
            'inquiry_id': next_id,
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': inquiry_date,
            'status': 'Pending'
        })
        if save_inquiries(inquiries):
            submission_status = "Inquiry submitted successfully."
        else:
            submission_status = "Failed to save inquiry, please try again later."

    return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)


# My Inquiries page
@app.route('/inquiries')
def my_inquiries():
    inquiries = load_inquiries()
    properties = load_properties()
    status_filter = request.args.get('status', 'All')

    # Combine inquiry with property details
    filtered_inquiries = []
    for i in inquiries:
        # Filter by status
        if status_filter != 'All' and i['status'] != status_filter:
            continue
        property = next((p for p in properties if p['property_id'] == i['property_id']), None)
        if property:
            filtered_inquiries.append({
                'inquiry_id': i['inquiry_id'],
                'property': property,
                'customer_name': i['customer_name'],
                'customer_email': i['customer_email'],
                'customer_phone': i['customer_phone'],
                'message': i['message'],
                'inquiry_date': i['inquiry_date'],
                'status': i['status']
            })

    return render_template('my_inquiries.html', inquiries=filtered_inquiries, status_filter=status_filter)


# Delete Inquiry route
@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


# My Favorites page
@app.route('/favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    # Combine favorite and property info
    combined = []
    for fav in favorites:
        prop = next((p for p in properties if p['property_id'] == fav['property_id']), None)
        if prop:
            combined.append({
                'favorite_id': fav['favorite_id'],
                'added_date': fav['added_date'],
                **prop
            })
    return render_template('my_favorites.html', favorites=combined)


# Remove from favorites
@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


# Agent Directory page
@app.route('/agents')
def agent_directory():
    agents = load_agents()
    search_query = request.args.get('search', '').strip()
    if search_query:
        agents = [a for a in agents if search_query.lower() in a['agent_name'].lower()]
    return render_template('agent_directory.html', agents=agents, search_query=search_query)


# Locations page
@app.route('/locations')
def locations():
    locations = load_locations()
    sort_option = request.args.get('sort', 'By Name')

    if sort_option == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_option == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    else:
        # Default sort by name
        locations.sort(key=lambda x: x['location_name'])

    return render_template('locations.html', locations=locations, sort_option=sort_option)


# View location properties filtered by location_id
@app.route('/locations/<int:location_id>')
def properties_by_location(location_id):
    properties = load_properties()
    location_name = None
    locations = load_locations()
    for loc in locations:
        if loc['location_id'] == location_id:
            location_name = loc['location_name']
            break
    if location_name is None:
        return "Location not found", 404

    filtered_properties = [p for p in properties if p['location'] == location_name and p['status'].lower() == 'available']

    return render_template('property_search.html', properties=filtered_properties,
                           filter_location=location_name,
                           filter_price_min=None,
                           filter_price_max=None,
                           filter_property_type=None)


if __name__ == '__main__':
    app.run(debug=True)
