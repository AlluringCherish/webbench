from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_PATH = 'data'

# Utility functions to load and save data

def load_properties():
    properties = []
    path = os.path.join(DATA_PATH, 'properties.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 11:
                    continue
                p = {
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
                properties.append(p)
    except FileNotFoundError:
        pass
    return properties


def load_locations():
    locations = []
    path = os.path.join(DATA_PATH, 'locations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                l = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': int(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                }
                locations.append(l)
    except FileNotFoundError:
        pass
    return locations


def load_inquiries():
    inquiries = []
    path = os.path.join(DATA_PATH, 'inquiries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                i = {
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'customer_phone': parts[4],
                    'message': parts[5],
                    'inquiry_date': parts[6],
                    'status': parts[7]
                }
                inquiries.append(i)
    except FileNotFoundError:
        pass
    return inquiries


def save_inquiries(inquiries):
    path = os.path.join(DATA_PATH, 'inquiries.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for i in inquiries:
                line = f"{i['inquiry_id']}|{i['property_id']}|{i['customer_name']}|{i['customer_email']}|{i['customer_phone']}|{i['message']}|{i['inquiry_date']}|{i['status']}"
                f.write(line + '\n')
    except Exception:
        pass


def load_favorites():
    favorites = []
    path = os.path.join(DATA_PATH, 'favorites.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 3:
                    continue
                fav = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                }
                favorites.append(fav)
    except FileNotFoundError:
        pass
    return favorites


def save_favorites(favorites):
    path = os.path.join(DATA_PATH, 'favorites.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}"
                f.write(line + '\n')
    except Exception:
        pass


def load_agents():
    agents = []
    path = os.path.join(DATA_PATH, 'agents.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                a = {
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5])
                }
                agents.append(a)
    except FileNotFoundError:
        pass
    return agents


# ROUTES IMPLEMENTATIONS

# Root Route
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))


# 1. Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    properties = load_properties()

    # featured_properties: We consider the first 5 available properties as featured
    featured_properties = [p for p in properties if p['status'].lower() == 'available'][:5]

    # recent_listings: last 5 properties by property_id descending
    sorted_props = sorted(properties, key=lambda x: x['property_id'], reverse=True)
    recent_listings = sorted_props[:5]

    return render_template('dashboard.html',
                           featured_properties=featured_properties,
                           recent_listings=recent_listings)


# 2. Property Search Page
@app.route('/properties', methods=['GET', 'POST'])
def property_search_page():
    properties = load_properties()
    locations_raw = load_locations()
    locations = sorted(set([loc['location_name'] for loc in locations_raw]))
    property_types = ["House", "Apartment", "Condo", "Land"]

    if request.method == 'GET':
        return render_template('property_search.html',
                               all_properties=properties,
                               filtered_properties=properties,
                               locations=locations,
                               property_types=property_types)

    # POST: filtering properties
    location_input = request.form.get('location_input', '').strip()
    price_min_str = request.form.get('price_range_min', '').strip()
    price_max_str = request.form.get('price_range_max', '').strip()
    property_type_filter = request.form.get('property_type_filter', '').strip()

    def safe_int(val):
        try:
            return int(val)
        except Exception:
            return None

    price_min = safe_int(price_min_str)
    price_max = safe_int(price_max_str)

    filtered_properties = []
    for p in properties:
        if location_input and location_input.lower() != p['location'].lower():
            continue
        if property_type_filter and property_type_filter != p['property_type']:
            continue
        if price_min is not None and p['price'] < price_min:
            continue
        if price_max is not None and p['price'] > price_max:
            continue
        filtered_properties.append(p)

    return render_template('property_search.html',
                           all_properties=properties,
                           filtered_properties=filtered_properties,
                           locations=locations,
                           property_types=property_types)


# 3. Property Details Page
@app.route('/properties/<int:property_id>', methods=['GET'])
def property_details_page(property_id):
    properties = load_properties()
    agents = load_agents()
    favorites = load_favorites()

    property_detail = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_detail:
        return "Property not found", 404

    agent = next((a for a in agents if a['agent_id'] == property_detail['agent_id']), None)
    # Check if favorite
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)

    return render_template('property_details.html',
                           property=property_detail,
                           agent=agent,
                           is_favorite=is_favorite)


# 4. Property Inquiry Page
@app.route('/inquiries/submit', methods=['GET', 'POST'])
def property_inquiry_page():
    properties = load_properties()

    if request.method == 'GET':
        return render_template('property_inquiry.html', properties=properties)

    # POST: Handle inquiry submission
    select_property = request.form.get('select_property', '').strip()
    inquiry_name = request.form.get('inquiry_name', '').strip()
    inquiry_email = request.form.get('inquiry_email', '').strip()
    inquiry_phone = request.form.get('inquiry_phone', '').strip()
    inquiry_message = request.form.get('inquiry_message', '').strip()

    # Basic validation
    errors = []
    try:
        property_id = int(select_property)
    except Exception:
        errors.append('Invalid property selected')
        property_id = None

    if not inquiry_name:
        errors.append('Name required')
    if not inquiry_email:
        errors.append('Email required')
    if not inquiry_phone:
        errors.append('Phone required')
    if not inquiry_message:
        errors.append('Message required')

    if errors:
        # Return page with errors, but spec doesn't specify error display, so just show properties again
        return render_template('property_inquiry.html', properties=properties)

    inquiries = load_inquiries()
    new_id = max([i['inquiry_id'] for i in inquiries], default=0) + 1
    inquiry_date = datetime.now().strftime('%Y-%m-%d')
    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': inquiry_name,
        'customer_email': inquiry_email,
        'customer_phone': inquiry_phone,
        'message': inquiry_message,
        'inquiry_date': inquiry_date,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    return redirect(url_for('my_inquiries_page'))


# 5. My Inquiries Page
@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries_page():
    inquiries = load_inquiries()

    inquiry_status_filter = "All"
    delete_inquiry_id = None

    if request.method == 'POST':
        inquiry_status_filter = request.form.get('inquiry_status_filter', "All")
        delete_inquiry_id_str = request.form.get('delete_inquiry_id', '').strip()

        if delete_inquiry_id_str:
            try:
                delete_inquiry_id = int(delete_inquiry_id_str)
            except Exception:
                delete_inquiry_id = None

        # Delete inquiry if applicable
        if delete_inquiry_id is not None:
            inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_inquiry_id]
            save_inquiries(inquiries)

    # Filter inquiries by status if needed
    if inquiry_status_filter and inquiry_status_filter != "All":
        inquiries_filtered = [inq for inq in inquiries if inq['status'].lower() == inquiry_status_filter.lower()]
    else:
        inquiries_filtered = inquiries

    return render_template('my_inquiries.html',
                           inquiries=inquiries_filtered,
                           inquiry_status_filter=inquiry_status_filter)


# 6. My Favorites Page
@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites_page():
    favorites = load_favorites()
    properties = load_properties()

    remove_favorite_property_id = None

    if request.method == 'POST':
        remove_fav_id_str = request.form.get('remove_favorite_property_id', '').strip()
        if remove_fav_id_str:
            try:
                remove_favorite_property_id = int(remove_fav_id_str)
            except Exception:
                remove_favorite_property_id = None

        if remove_favorite_property_id is not None:
            # Remove favorite entry by property_id
            favorites = [f for f in favorites if f['property_id'] != remove_favorite_property_id]
            save_favorites(favorites)

    # Fetch favorite properties
    favorite_properties = []
    fav_prop_ids = {f['property_id'] for f in favorites}
    for p in properties:
        if p['property_id'] in fav_prop_ids:
            favorite_properties.append(p)

    return render_template('my_favorites.html',
                           favorite_properties=favorite_properties)


# 7. Agent Directory Page
@app.route('/agents', methods=['GET'])
def agent_directory_page():
    agents = load_agents()
    search_query = request.args.get('agent-search', '').strip()
    if search_query:
        filtered_agents = [a for a in agents if search_query.lower() in a['agent_name'].lower()]
    else:
        filtered_agents = agents
    return render_template('agents.html', agents=filtered_agents, search_query=search_query)


# 8. Locations Page
@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    locations = load_locations()
    location_sort = "By Name"

    if request.method == 'POST':
        location_sort = request.form.get('location_sort', 'By Name')

    if location_sort == "By Name":
        locations_sorted = sorted(locations, key=lambda x: x['location_name'])
    elif location_sort == "By Properties Count":
        locations_sorted = sorted(locations, key=lambda x: x['property_count'], reverse=True)
    elif location_sort == "By Average Price":
        locations_sorted = sorted(locations, key=lambda x: x['average_price'], reverse=True)
    else:
        locations_sorted = locations

    return render_template('locations.html', locations=locations_sorted, location_sort=location_sort)


if __name__ == '__main__':
    app.run(debug=True)
