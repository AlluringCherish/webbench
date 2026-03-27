from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data files

def load_properties():
    properties = []
    path = os.path.join(DATA_DIR, 'properties.txt')
    if not os.path.exists(path):
        return properties
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
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
    except Exception:
        pass
    return properties


def load_locations():
    locations = []
    path = os.path.join(DATA_DIR, 'locations.txt')
    if not os.path.exists(path):
        return locations
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                loc = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': int(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                }
                locations.append(loc)
    except Exception:
        pass
    return locations


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    if not os.path.exists(path):
        return inquiries
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except Exception:
        pass
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = f"{inq['inquiry_id']}|{inq['property_id']}|{inq['customer_name']}|{inq['customer_email']}|{inq['customer_phone']}|{inq['message']}|{inq['inquiry_date']}|{inq['status']}\n"
                f.write(line)
    except Exception:
        pass


def load_favorites():
    favorites = []
    path = os.path.join(DATA_DIR, 'favorites.txt')
    if not os.path.exists(path):
        return favorites
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                fav = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                }
                favorites.append(fav)
    except Exception:
        pass
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
    except Exception:
        pass


def load_agents():
    agents = []
    path = os.path.join(DATA_DIR, 'agents.txt')
    if not os.path.exists(path):
        return agents
    try:
        with open(path, encoding='utf-8') as f:
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
    except Exception:
        pass
    return agents


# Flask routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['price'], reverse=True)
    featured_properties = featured_properties[:5]
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/properties/search')
def property_search():
    properties = load_properties()
    locations = sorted(set(p['location'] for p in properties))

    location_filter = request.args.get('location', '').strip()
    price_min_str = request.args.get('price_min', '')
    price_max_str = request.args.get('price_max', '')
    property_type_filter = request.args.get('property_type', '').strip()

    def safe_int(val):
        try:
            return int(val)
        except Exception:
            return None

    price_min = safe_int(price_min_str) if price_min_str else None
    price_max = safe_int(price_max_str) if price_max_str else None

    filtered = []
    for p in properties:
        if p['status'] != 'Available':
            continue
        if location_filter and p['location'] != location_filter:
            continue
        if property_type_filter and p['property_type'] != property_type_filter:
            continue
        if price_min is not None and p['price'] < price_min:
            continue
        if price_max is not None and p['price'] > price_max:
            continue
        filtered.append(p)

    selected_filters = {
        'location': location_filter if location_filter else None,
        'price_min': price_min,
        'price_max': price_max,
        'property_type': property_type_filter if property_type_filter else None
    }

    return render_template('property_search.html', properties=filtered, locations=locations, selected_filters=selected_filters)


@app.route('/properties/<int:property_id>')
def property_details(property_id):
    properties = load_properties()
    agents = load_agents()
    favorites = load_favorites()

    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if not prop:
        return "Property not found", 404

    agent = next((a for a in agents if a['agent_id'] == prop['agent_id']), None)

    is_favorite = any(f['property_id'] == property_id for f in favorites)

    return render_template('property_details.html', property=prop, agent=agent, is_favorite=is_favorite)


@app.route('/inquiries/submit', methods=['GET'])
def inquiry_form():
    properties = load_properties()
    return render_template('inquiry_form.html', properties=properties)


@app.route('/inquiries/submit', methods=['POST'])
def submit_inquiry():
    form = request.form
    try:
        property_id = int(form.get('property_id', '').strip())
    except Exception:
        property_id = None
    customer_name = form.get('customer_name', '').strip()
    customer_email = form.get('customer_email', '').strip()
    customer_phone = form.get('customer_phone', '').strip()
    inquiry_message = form.get('inquiry_message', '').strip()

    errors = {}

    if property_id is None:
        errors['property_id'] = 'Property ID is required.'
    if not customer_name:
        errors['customer_name'] = 'Customer name is required.'
    if not customer_email or '@' not in customer_email:
        errors['customer_email'] = 'Valid customer email is required.'
    if not inquiry_message:
        errors['inquiry_message'] = 'Inquiry message is required.'

    properties = load_properties()
    available_ids = {p['property_id'] for p in properties if p['status'] == 'Available'}
    if property_id is not None and property_id not in available_ids:
        errors['property_id'] = 'Selected property is not available.'

    if errors:
        return render_template('inquiry_form.html', properties=properties, errors=errors, form_data=form)

    inquiries = load_inquiries()
    new_id = 1 if not inquiries else max(i['inquiry_id'] for i in inquiries) + 1
    today = datetime.now().strftime('%Y-%m-%d')

    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'message': inquiry_message,
        'inquiry_date': today,
        'status': 'Pending'
    }

    inquiries.append(new_inquiry)
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


@app.route('/inquiries')
def my_inquiries():
    inquiries = load_inquiries()
    filter_status = request.args.get('filter_status', 'All')
    valid_statuses = {'All', 'Pending', 'Contacted', 'Resolved'}
    if filter_status not in valid_statuses:
        filter_status = 'All'
    if filter_status != 'All':
        inquiries = [i for i in inquiries if i['status'] == filter_status]
    return render_template('inquiries.html', inquiries=inquiries, filter_status=filter_status)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [i for i in inquiries if i['inquiry_id'] != inquiry_id]
    save_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


@app.route('/favorites')
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    properties_map = {p['property_id']: p for p in properties}
    favorites = [f for f in favorites if f['property_id'] in properties_map]
    return render_template('favorites.html', favorites=favorites, properties_map=properties_map)


@app.route('/favorites/add/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    properties = load_properties()
    if not any(p['property_id'] == property_id and p['status'] == 'Available' for p in properties):
        return redirect(url_for('my_favorites'))
    favorites = load_favorites()
    if any(f['property_id'] == property_id for f in favorites):
        return redirect(url_for('my_favorites'))
    new_id = 1 if not favorites else max(f['favorite_id'] for f in favorites) + 1
    added_date = datetime.now().strftime('%Y-%m-%d')
    new_favorite = {
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': added_date
    }
    favorites.append(new_favorite)
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = load_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    save_favorites(favorites)
    return redirect(url_for('my_favorites'))


@app.route('/agents')
def agent_directory():
    agents = load_agents()
    search_query = request.args.get('search_query', '')
    if search_query:
        sq_lower = search_query.lower()
        agents = [a for a in agents if sq_lower in a['agent_name'].lower() or sq_lower in a['specialization'].lower()]
    return render_template('agents.html', agents=agents, search_query=search_query)


@app.route('/locations')
def locations_page():
    locations = load_locations()
    sort_order = request.args.get('sort_order', 'By Name')
    if sort_order == 'By Name':
        locations.sort(key=lambda x: x['location_name'])
    elif sort_order == 'By Properties Count':
        locations.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_order == 'By Average Price':
        locations.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html', locations=locations, sort_order=sort_order)


if __name__ == '__main__':
    app.run(debug=True)
