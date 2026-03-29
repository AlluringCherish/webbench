from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for data loading and saving

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.exists(path):
        return properties
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 11:
                continue
            # Map fields
            try:
                property = {
                    'property_id': parts[0],
                    'address': parts[1],
                    'location': parts[2],
                    'price': float(parts[3]),
                    'property_type': parts[4],
                    'bedrooms': int(parts[5]),
                    'bathrooms': float(parts[6]),
                    'square_feet': int(parts[7]),
                    'description': parts[8],
                    'agent_id': parts[9],
                    'status': parts[10],
                }
                properties.append(property)
            except ValueError:
                continue
    return properties


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                location = {
                    'location_id': parts[0],
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': float(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5],
                }
                locations.append(location)
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
            parts = line.strip().split('|')
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
                'status': parts[7],
            }
            inquiries.append(inquiry)
    return inquiries


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 3:
                continue
            favorite = {
                'favorite_id': parts[0],
                'property_id': parts[1],
                'added_date': parts[2],
            }
            favorites.append(favorite)
    return favorites


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.exists(path):
        return agents
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                agent = {
                    'agent_id': parts[0],
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5]),
                }
                agents.append(agent)
            except ValueError:
                continue
    return agents


def save_inquiry(inquiry):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    inquiries = load_inquiries()
    # Create new inquiry_id
    max_id = 0
    for inq in inquiries:
        try:
            iid = int(inq['inquiry_id'])
            if iid > max_id:
                max_id = iid
        except Exception:
            continue
    new_id = str(max_id + 1)
    inquiry['inquiry_id'] = new_id
    inquiries.append(inquiry)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = '|'.join([
                    inq.get('inquiry_id',''),
                    inq.get('property_id',''),
                    inq.get('customer_name',''),
                    inq.get('customer_email',''),
                    inq.get('customer_phone',''),
                    inq.get('message',''),
                    inq.get('inquiry_date',''),
                    inq.get('status','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = '|'.join([
                    fav.get('favorite_id',''),
                    fav.get('property_id',''),
                    fav.get('added_date','')
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False

# Route 1: Dashboard redirect
@app.route('/')
def dashboard():
    return redirect(url_for('dashboard_page'))

# Route 2: Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    properties = load_properties()
    # For demonstration, featured_properties is all properties with status Available (as nothing else defined)
    featured_properties = [p for p in properties if p['status'].lower() == 'available']
    # Context variable: featured_properties with required fields
    featured_properties_list = []
    for p in featured_properties:
        featured_properties_list.append({
            'property_id': p['property_id'],
            'address': p['address'],
            'price': p['price'],
            'property_type': p['property_type'],
            'bedrooms': p['bedrooms'],
            'bathrooms': p['bathrooms'],
            'square_feet': p['square_feet'],
            'description': p['description']
        })
    return render_template('dashboard.html', featured_properties=featured_properties_list)

# Route 3: Property Search
@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    # Default filters
    filters = {
        'location': '',
        'price_min': 0.0,
        'price_max': float('inf'),
        'property_type': ''
    }
    filtered_properties = []
    if request.method == 'POST':
        location = request.form.get('location', '').strip()
        price_min_str = request.form.get('price_min', '')
        price_max_str = request.form.get('price_max', '')
        property_type = request.form.get('property_type', '').strip()

        try:
            price_min = float(price_min_str) if price_min_str else 0.0
        except ValueError:
            price_min = 0.0

        try:
            price_max = float(price_max_str) if price_max_str else float('inf')
        except ValueError:
            price_max = float('inf')

        filters = {
            'location': location,
            'price_min': price_min,
            'price_max': price_max,
            'property_type': property_type
        }

        # Filter properties
        for p in properties:
            if p['status'].lower() != 'available':
                continue
            if location and location.lower() not in p['location'].lower():
                continue
            if p['price'] < price_min or p['price'] > price_max:
                continue
            if property_type and p['property_type'].lower() != property_type.lower():
                continue
            filtered_properties.append(p)

    else:
        # On GET, show all available properties
        filtered_properties = [p for p in properties if p['status'].lower() == 'available']

    # Prepare properties list for template
    properties_list = []
    for p in filtered_properties:
        properties_list.append({
            'property_id': p['property_id'],
            'address': p['address'],
            'price': p['price'],
            'property_type': p['property_type'],
            'bedrooms': p['bedrooms'],
            'bathrooms': p['bathrooms'],
            'square_feet': p['square_feet'],
            'description': p['description']
        })

    return render_template('search.html', properties=properties_list, filters=filters)

# Route 4: Property Details
@app.route('/property/<property_id>', methods=['GET'])
def property_details(property_id):
    properties = load_properties()
    # Find property by property_id
    property = None
    for p in properties:
        if p['property_id'] == property_id:
            property = p
            break
    if property is None:
        # Property not found; render with no data or redirect?
        # As no error page specified, render template with property None
        return render_template('property_details.html', property=None)

    # Prepare context with all fields as specified
    prop_context = {
        'property_id': property['property_id'],
        'address': property['address'],
        'location': property['location'],
        'price': property['price'],
        'property_type': property['property_type'],
        'bedrooms': property['bedrooms'],
        'bathrooms': property['bathrooms'],
        'square_feet': property['square_feet'],
        'description': property['description'],
        'agent_id': property['agent_id'],
        'status': property['status'],
    }
    return render_template('property_details.html', property=prop_context)

# Route 5: Property Inquiry
@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = load_properties()
    # Prepare all properties for selection use only ID and address
    properties_list = []
    for p in properties:
        properties_list.append({
            'property_id': p['property_id'],
            'address': p['address'],
        })

    if request.method == 'POST':
        selected_property = request.form.get('selected_property', '').strip()
        inquiry_name = request.form.get('inquiry_name', '').strip()
        inquiry_email = request.form.get('inquiry_email', '').strip()
        inquiry_phone = request.form.get('inquiry_phone', '').strip()
        inquiry_message = request.form.get('inquiry_message', '').strip()

        # Validate required fields
        if not selected_property or not inquiry_name or not inquiry_email or not inquiry_phone or not inquiry_message:
            # Missing fields, re-render with error? No error return specified,
            # Just render again for simplicity
            return render_template('inquiry.html', properties=properties_list)

        # Compose new inquiry record
        today_str = datetime.today().strftime('%Y-%m-%d')
        new_inquiry = {
            'property_id': selected_property,
            'customer_name': inquiry_name,
            'customer_email': inquiry_email,
            'customer_phone': inquiry_phone,
            'message': inquiry_message,
            'inquiry_date': today_str,
            'status': 'Pending'
        }

        # Save inquiry
        saved = save_inquiry(new_inquiry)
        if saved:
            # Redirect to inquiries page
            return redirect(url_for('my_inquiries'))

    return render_template('inquiry.html', properties=properties_list)

# Route 6: My Inquiries
@app.route('/inquiries', methods=['GET'])
def my_inquiries():
    inquiries = load_inquiries()
    properties = load_properties()
    property_dict = {p['property_id']: p for p in properties}

    # Filter by status query param (optional)
    status_filter = request.args.get('status', 'All')

    filtered_inquiries = []
    for inq in inquiries:
        if status_filter != 'All' and inq['status'] != status_filter:
            continue
        prop = property_dict.get(inq['property_id'])
        prop_address = prop['address'] if prop else 'Unknown'
        filtered_inquiries.append({
            'inquiry_id': inq['inquiry_id'],
            'property_id': inq['property_id'],
            'property_address': prop_address,
            'customer_name': inq['customer_name'],
            'customer_email': inq['customer_email'],
            'customer_phone': inq['customer_phone'],
            'message': inq['message'],
            'inquiry_date': inq['inquiry_date'],
            'status': inq['status'],
        })

    return render_template('inquiries.html', inquiries=filtered_inquiries, status_filter=status_filter)

# Route 7: My Favorites
@app.route('/favorites', methods=['GET'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    property_dict = {p['property_id']: p for p in properties}

    favorite_properties = []
    for fav in favorites:
        prop = property_dict.get(fav['property_id'])
        if not prop:
            continue
        # Only include favorites that are in the properties data
        favorite_properties.append({
            'property_id': prop['property_id'],
            'address': prop['address'],
            'price': prop['price'],
            'property_type': prop['property_type'],
            'bedrooms': prop['bedrooms'],
            'bathrooms': prop['bathrooms'],
            'square_feet': prop['square_feet'],
            'description': prop['description']
        })
    return render_template('favorites.html', favorites=favorite_properties)

# Route 8: Agent Directory
@app.route('/agents', methods=['GET'])
def agent_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)

# Route 9: Locations Page
@app.route('/locations', methods=['GET'])
def locations_page():
    locations = load_locations()
    return render_template('locations.html', locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
