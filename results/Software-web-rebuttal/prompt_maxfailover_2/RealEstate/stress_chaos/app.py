from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility function to parse properties.txt
# properties schema:
#  1. property_id (int)
#  2. address (str)
#  3. location (str)
#  4. price (float)
#  5. property_type (str)
#  6. bedrooms (int)
#  7. bathrooms (float)
#  8. square_feet (int)
#  9. description (str)
# 10. agent_id (int)
# 11. status (str)
def load_properties():
    properties = []
    try:
        with open(os.path.join(DATA_DIR, 'properties.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                property = {
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
                properties.append(property)
    except IOError:
        pass
    return properties

# Utility function to parse locations.txt
# 1. location_id (int)
# 2. location_name (str)
# 3. region (str)
# 4. average_price (float)
# 5. property_count (int)
# 6. description (str)
def load_locations():
    locations = []
    try:
        with open(os.path.join(DATA_DIR, 'locations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                location = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': float(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                }
                locations.append(location)
    except IOError:
        pass
    return locations

# Utility function to parse inquiries.txt
#  1. inquiry_id (int)
#  2. property_id (int)
#  3. customer_name (str)
#  4. customer_email (str)
#  5. customer_phone (str)
#  6. message (str)
#  7. inquiry_date (str, YYYY-MM-DD)
#  8. status (str)
def load_inquiries():
    inquiries = []
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                inquiry = {
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'customer_phone': parts[4],
                    'message': parts[5],
                    'inquiry_date': parts[6],
                    'status': parts[7]
                }
                inquiries.append(inquiry)
    except IOError:
        pass
    return inquiries

# Write inquiries.txt with a list of inquiries dicts

def save_inquiries(inquiries):
    try:
        with open(os.path.join(DATA_DIR, 'inquiries.txt'), 'w', encoding='utf-8') as f:
            for iq in inquiries:
                line = '|'.join([
                    str(iq['inquiry_id']),
                    str(iq['property_id']),
                    iq['customer_name'],
                    iq['customer_email'],
                    iq['customer_phone'],
                    iq['message'],
                    iq['inquiry_date'],
                    iq['status']
                ])
                f.write(line + '\n')
    except IOError:
        pass

# Utility function to parse favorites.txt
# Fields:
#  1. favorite_id (int)
#  2. property_id (int)
#  3. added_date (str YYYY-MM-DD)
def load_favorites():
    favorites = []
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                favorite = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                }
                favorites.append(favorite)
    except IOError:
        pass
    return favorites

# Write favorites.txt with list of favorites dicts

def save_favorites(favorites):
    try:
        with open(os.path.join(DATA_DIR, 'favorites.txt'), 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    str(fav['favorite_id']),
                    str(fav['property_id']),
                    fav['added_date']
                ])
                f.write(line + '\n')
    except IOError:
        pass

# Utility function to load agents.txt
# Fields:
# 1. agent_id (int)
# 2. agent_name (str)
# 3. specialization (str)
# 4. email (str)
# 5. phone (str)
# 6. properties_sold (int)
def load_agents():
    agents = []
    try:
        with open(os.path.join(DATA_DIR, 'agents.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                agent = {
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5])
                }
                agents.append(agent)
    except IOError:
        pass
    return agents

# Helper functions

def get_property_by_id(property_id):
    for p in load_properties():
        if p['property_id'] == property_id:
            return p
    return None

def get_agent_by_id(agent_id):
    for a in load_agents():
        if a['agent_id'] == agent_id:
            return a
    return None

# Routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    properties = load_properties()
    # featured_properties: list of dict with property_id, address, price, image_url
    # recent_listings: list similar
    # We do not have image_url in schema, so provide empty string or placeholder
    # Use first 3 available properties as featured
    # Use last 3 available properties as recent listings
    available_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties = []
    recent_listings = []

    for p in available_properties[:3]:
        featured_properties.append({
            'property_id': p['property_id'],
            'address': p['address'],
            'price': p['price'],
            'image_url': ''
        })

    for p in available_properties[-3:]:
        recent_listings.append({
            'property_id': p['property_id'],
            'address': p['address'],
            'price': p['price'],
            'image_url': ''
        })

    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)

@app.route('/search')
def property_search_page():
    properties = load_properties()
    available_properties = [p for p in properties if p['status'] == 'Available']

    # filter_options dict: location:str, price_min:int, price_max:int, property_type:str
    # Without any query parameters, set defaults
    filter_options = {
        'location': '',
        'price_min': 0,
        'price_max': 1000000000,  # large number
        'property_type': ''
    }

    return render_template('property_search.html', properties=available_properties, filter_options=filter_options)

@app.route('/property/<int:property_id>')
def property_details_page(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return render_template('property_details.html', property=None, is_favorite=False), 404

    favorites = load_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)

    return render_template('property_details.html', property=property, is_favorite=is_favorite)

@app.route('/inquiry', methods=['GET'])
def property_inquiry_page():
    properties = load_properties()
    available_properties = [{'property_id': p['property_id'], 'address': p['address']} for p in properties if p['status'] == 'Available']
    return render_template('inquiry.html', properties=available_properties)

@app.route('/inquiry', methods=['POST'])
def submit_property_inquiry():
    errors = []
    properties = load_properties()
    available_property_ids = {p['property_id'] for p in properties if p['status'] == 'Available'}

    try:
        property_id = int(request.form.get('property_id', '').strip())
    except ValueError:
        property_id = None
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    message = request.form.get('message', '').strip()

    # Validation
    if property_id is None or property_id not in available_property_ids:
        errors.append('Invalid or unavailable property selected.')
    if not customer_name:
        errors.append('Customer name is required.')
    if not customer_email:
        errors.append('Customer email is required.')
    if not customer_phone:
        errors.append('Customer phone is required.')
    if not message:
        errors.append('Message is required.')

    if errors:
        available_properties = [{'property_id': p['property_id'], 'address': p['address']} for p in properties if p['status'] == 'Available']
        return render_template('inquiry.html', properties=available_properties, errors=errors)

    # Load inquiries
    inquiries = load_inquiries()
    max_inquiry_id = max([iq['inquiry_id'] for iq in inquiries], default=0)
    new_inquiry_id = max_inquiry_id + 1

    new_inquiry = {
        'inquiry_id': new_inquiry_id,
        'property_id': property_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'message': message,
        'inquiry_date': date.today().strftime('%Y-%m-%d'),
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    # On successful submission, re-render inquiry page with empty form and no errors
    available_properties = [{'property_id': p['property_id'], 'address': p['address']} for p in properties if p['status'] == 'Available']
    return render_template('inquiry.html', properties=available_properties, errors=[])

@app.route('/my-inquiries')
def my_inquiries_page():
    inquiries = load_inquiries()
    properties = load_properties()
    property_dict = {p['property_id']: p for p in properties}

    # Compose inquiries with property address
    inquiries_context = []
    for iq in inquiries:
        property_address = property_dict.get(iq['property_id'], {}).get('address', 'Unknown')
        inquiries_context.append({
            'inquiry_id': iq['inquiry_id'],
            'property_address': property_address,
            'inquiry_date': iq['inquiry_date'],
            'status': iq['status'],
            'customer_name': iq['customer_name'],
            'customer_email': iq['customer_email'],
            'customer_phone': iq['customer_phone'],
            'message': iq['message']
        })

    status_filter_options = ['All', 'Pending', 'Contacted', 'Resolved']
    return render_template('my_inquiries.html', inquiries=inquiries_context, status_filter_options=status_filter_options)

@app.route('/my-inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [iq for iq in inquiries if iq['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries_page'))

@app.route('/my-favorites')
def my_favorites_page():
    favorites = load_favorites()
    properties = load_properties()
    property_dict = {p['property_id']: p for p in properties}

    favorites_context = []
    for fav in favorites:
        prop = property_dict.get(fav['property_id'])
        if prop:
            favorites_context.append({
                'property_id': prop['property_id'],
                'address': prop['address'],
                'price': prop['price'],
                'image_url': ''
            })

    return render_template('my_favorites.html', favorites=favorites_context)

@app.route('/my-favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = load_favorites()
    if any(fav['property_id'] == property_id for fav in favorites):
        # Already favorite, just redirect
        return redirect(url_for('my_favorites_page'))

    max_favorite_id = max([fav['favorite_id'] for fav in favorites], default=0)
    new_favorite_id = max_favorite_id + 1
    favorites.append({
        'favorite_id': new_favorite_id,
        'property_id': property_id,
        'added_date': date.today().strftime('%Y-%m-%d')
    })
    save_favorites(favorites)
    return redirect(url_for('my_favorites_page'))

@app.route('/my-favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites_page'))

@app.route('/agents')
def agents_page():
    agents = load_agents()
    return render_template('agents.html', agents=agents)

@app.route('/locations')
def locations_page():
    locations = load_locations()
    # default sort option
    sort_option = 'By Name'
    return render_template('locations.html', locations=locations, sort_option=sort_option)


if __name__ == '__main__':
    app.run(debug=True)
