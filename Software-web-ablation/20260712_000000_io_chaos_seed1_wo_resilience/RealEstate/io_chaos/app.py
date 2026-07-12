from flask import Flask, render_template, redirect, url_for, request
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
PROPERTIES_FILE = 'data/properties.txt'
LOCATIONS_FILE = 'data/locations.txt'
INQUIRIES_FILE = 'data/inquiries.txt'
FAVORITES_FILE = 'data/favorites.txt'
AGENTS_FILE = 'data/agents.txt'

# Helper functions for data loading

def load_properties():
    properties = []
    if not os.path.exists(PROPERTIES_FILE):
        return properties
    try:
        with open(PROPERTIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 11:
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
                    'status': parts[10],
                }
                properties.append(property)
    except Exception:
        pass
    return properties


def load_locations():
    locations = []
    if not os.path.exists(LOCATIONS_FILE):
        return locations
    try:
        with open(LOCATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                location = {
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': float(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5],
                }
                locations.append(location)
    except Exception:
        pass
    return locations


def load_inquiries():
    inquiries = []
    if not os.path.exists(INQUIRIES_FILE):
        return inquiries
    try:
        with open(INQUIRIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                inquiry = {
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'customer_phone': parts[4],
                    'message': parts[5],
                    'inquiry_date': parts[6],
                    'status': parts[7],
                }
                inquiries.append(inquiry)
    except Exception:
        pass
    return inquiries


def load_favorites():
    favorites = []
    if not os.path.exists(FAVORITES_FILE):
        return favorites
    try:
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 3:
                    continue
                favorite = {
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2],
                }
                favorites.append(favorite)
    except Exception:
        pass
    return favorites


def load_agents():
    agents = []
    if not os.path.exists(AGENTS_FILE):
        return agents
    try:
        with open(AGENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                agent = {
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5]),
                }
                agents.append(agent)
    except Exception:
        pass
    return agents


# Helper functions for saving data

def save_inquiries(inquiries):
    try:
        with open(INQUIRIES_FILE, 'w', encoding='utf-8') as f:
            for inq in inquiries:
                line = f"{inq['inquiry_id']}|{inq['property_id']}|{inq['customer_name']}|{inq['customer_email']}|{inq['customer_phone']}|{inq['message']}|{inq['inquiry_date']}|{inq['status']}\n"
                f.write(line)
        return True
    except Exception:
        return False


def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            for fav in favorites:
                line = f"{fav['favorite_id']}|{fav['property_id']}|{fav['added_date']}\n"
                f.write(line)
        return True
    except Exception:
        return False


# Route implementations

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    properties = load_properties()
    # Featured properties: let's consider top 3 available properties by price descending
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['price'], reverse=True)
    featured_properties = featured_properties[:3]

    # Recent listings: last 5 available by property_id descending (newest assumed)
    recent_listings = [p for p in properties if p['status'] == 'Available']
    recent_listings.sort(key=lambda x: x['property_id'], reverse=True)
    recent_listings = recent_listings[:5]

    return render_template('dashboard.html',
                           featured_properties=featured_properties,
                           recent_listings=recent_listings)


@app.route('/search', methods=['GET', 'POST'])
def property_search():
    properties = load_properties()
    property_types = ["House", "Apartment", "Condo", "Land"]

    # Defaults
    location_filter = ""
    price_min = None
    price_max = None
    property_type_filter = ""

    if request.method == 'POST':
        location_filter = request.form.get('location_input', '').strip()
        try:
            price_min_raw = request.form.get('price_range_min', '').strip()
            price_min = float(price_min_raw) if price_min_raw != '' else None
        except ValueError:
            price_min = None
        try:
            price_max_raw = request.form.get('price_range_max', '').strip()
            price_max = float(price_max_raw) if price_max_raw != '' else None
        except ValueError:
            price_max = None
        property_type_filter = request.form.get('property_type_filter', '').strip()

        # Filter properties
        filtered_properties = []
        for p in properties:
            if location_filter and location_filter.lower() not in p['location'].lower():
                continue
            if property_type_filter and property_type_filter != p['property_type']:
                continue
            if price_min is not None and p['price'] < price_min:
                continue
            if price_max is not None and p['price'] > price_max:
                continue
            # Only show available properties
            if p['status'] != 'Available':
                continue
            filtered_properties.append(p)
        properties = filtered_properties
    else:
        # GET: show all available properties
        properties = [p for p in properties if p['status'] == 'Available']

    return render_template('property_search.html',
                           properties=properties,
                           location_filter=location_filter,
                           price_min=price_min,
                           price_max=price_max,
                           property_type_filter=property_type_filter,
                           property_types=property_types)


@app.route('/property/<int:property_id>', methods=['GET', 'POST'])
def property_details(property_id):
    properties = load_properties()
    favorites = load_favorites()

    property = next((p for p in properties if p['property_id'] == property_id), None)
    if property is None:
        return "Property not found", 404

    if request.method == 'POST':
        # Check if form submitted to add to favorites
        if 'add_to_favorites' in request.form:
            # Check if property already in favorites
            if not any(f['property_id'] == property_id for f in favorites):
                new_favorite_id = max([f['favorite_id'] for f in favorites], default=0) + 1
                favorites.append({
                    'favorite_id': new_favorite_id,
                    'property_id': property_id,
                    'added_date': date.today().isoformat()
                })
                save_favorites(favorites)
            # After adding, redirect back to same property page
            return redirect(url_for('property_details', property_id=property_id))

    return render_template('property_details.html', property=property)


@app.route('/inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = load_properties()
    # Only available properties
    properties = [p for p in properties if p['status'] == 'Available']

    if request.method == 'POST':
        try:
            property_id = int(request.form.get('select_property', '0'))
        except ValueError:
            property_id = 0
        inquiry_name = request.form.get('inquiry_name', '').strip()
        inquiry_email = request.form.get('inquiry_email', '').strip()
        inquiry_phone = request.form.get('inquiry_phone', '').strip()
        inquiry_message = request.form.get('inquiry_message', '').strip()

        if property_id == 0 or not inquiry_name or not inquiry_email or not inquiry_phone or not inquiry_message:
            # Missing required fields - just re-render with current properties
            return render_template('property_inquiry.html', properties=properties)

        # Add new inquiry
        inquiries = load_inquiries()
        new_inquiry_id = max([inq['inquiry_id'] for inq in inquiries], default=0) + 1
        new_inquiry = {
            'inquiry_id': new_inquiry_id,
            'property_id': property_id,
            'customer_name': inquiry_name,
            'customer_email': inquiry_email,
            'customer_phone': inquiry_phone,
            'message': inquiry_message,
            'inquiry_date': date.today().isoformat(),
            'status': 'Pending'
        }
        inquiries.append(new_inquiry)
        save_inquiries(inquiries)

        return redirect(url_for('my_inquiries'))

    return render_template('property_inquiry.html', properties=properties)


@app.route('/inquiries', methods=['GET', 'POST'])
def my_inquiries():
    status_options = ["All", "Pending", "Contacted", "Resolved"]
    inquiries = load_inquiries()

    status_filter = "All"

    if request.method == 'POST':
        delete_inquiry_id_raw = request.form.get('delete_inquiry_id', None)
        if delete_inquiry_id_raw:
            try:
                delete_inquiry_id = int(delete_inquiry_id_raw)
                inquiries = [inq for inq in inquiries if inq['inquiry_id'] != delete_inquiry_id]
                save_inquiries(inquiries)
            except ValueError:
                pass

        # Also support filter by status if posted
        status_filter_post = request.form.get('inquiry_status_filter', None)
        if status_filter_post in status_options:
            status_filter = status_filter_post

    else:
        # Handling GET param filtering
        status_filter_get = request.args.get('inquiry_status_filter', None)
        if status_filter_get in status_options:
            status_filter = status_filter_get

    if status_filter != "All":
        inquiries = [inq for inq in inquiries if inq['status'] == status_filter]

    return render_template('my_inquiries.html',
                           inquiries=inquiries,
                           status_filter=status_filter,
                           status_options=status_options)


@app.route('/favorites', methods=['GET', 'POST'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()

    if request.method == 'POST':
        remove_property_id_raw = request.form.get('remove_property_id', None)
        if remove_property_id_raw:
            try:
                remove_property_id = int(remove_property_id_raw)
                favorites = [fav for fav in favorites if fav['property_id'] != remove_property_id]
                save_favorites(favorites)
            except ValueError:
                pass

    # Prepare favorites list with property details
    favorite_properties = []
    props_by_id = {p['property_id']: p for p in properties}
    for fav in favorites:
        prop = props_by_id.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)

    return render_template('my_favorites.html', favorites=favorite_properties)


@app.route('/agents', methods=['GET', 'POST'])
def agent_directory():
    agents = load_agents()
    search_query = ""

    if request.method == 'POST':
        search_query = request.form.get('agent_search', '').strip()
    else:
        search_query = request.args.get('agent_search', '').strip()

    if search_query:
        agents = [agent for agent in agents if search_query.lower() in agent['agent_name'].lower()]

    return render_template('agents.html', agents=agents, search_query=search_query)


@app.route('/locations', methods=['GET', 'POST'])
def locations_page():
    sort_options = ["By Name", "By Properties Count", "By Average Price"]
    sort_option = "By Name"

    locations = load_locations()

    if request.method == 'POST':
        sort_option_post = request.form.get('location_sort', '').strip()
        if sort_option_post in sort_options:
            sort_option = sort_option_post
    else:
        sort_option_get = request.args.get('location_sort', '').strip()
        if sort_option_get in sort_options:
            sort_option = sort_option_get

    # Sorting
    if sort_option == "By Name":
        locations.sort(key=lambda l: l['location_name'].lower())
    elif sort_option == "By Properties Count":
        locations.sort(key=lambda l: l['property_count'], reverse=True)
    elif sort_option == "By Average Price":
        locations.sort(key=lambda l: l['average_price'], reverse=True)

    return render_template('locations.html',
                           locations=locations,
                           sort_option=sort_option,
                           sort_options=sort_options)


if __name__ == '__main__':
    app.run(debug=True)
