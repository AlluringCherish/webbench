from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# --- Helper functions to load and write data files ---

def load_properties():
    properties = []
    try:
        with open('data/properties.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 11:
                    properties.append({
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
                    })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return properties


def load_locations():
    locations = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    locations.append({
                        'location_id': int(parts[0]),
                        'location_name': parts[1],
                        'region': parts[2],
                        'average_price': int(parts[3]),
                        'property_count': int(parts[4]),
                        'description': parts[5]
                    })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return locations


def load_inquiries():
    inquiries = []
    try:
        with open('data/inquiries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    inquiries.append({
                        'inquiry_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'customer_name': parts[2],
                        'customer_email': parts[3],
                        'customer_phone': parts[4],
                        'message': parts[5],
                        'inquiry_date': parts[6],
                        'status': parts[7]
                    })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return inquiries


def write_inquiries(inquiries):
    try:
        with open('data/inquiries.txt', 'w', encoding='utf-8') as f:
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
    try:
        with open('data/favorites.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    favorites.append({
                        'favorite_id': int(parts[0]),
                        'property_id': int(parts[1]),
                        'added_date': parts[2]
                    })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return favorites


def write_favorites(favorites):
    try:
        with open('data/favorites.txt', 'w', encoding='utf-8') as f:
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
    try:
        with open('data/agents.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    agents.append({
                        'agent_id': int(parts[0]),
                        'agent_name': parts[1],
                        'specialization': parts[2],
                        'email': parts[3],
                        'phone': parts[4],
                        'properties_sold': int(parts[5])
                    })
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return agents


def get_agent_by_id(agent_id):
    agents = load_agents()
    for agent in agents:
        if agent['agent_id'] == agent_id:
            return agent
    return None


def get_property_by_id(property_id):
    properties = load_properties()
    for prop in properties:
        if prop['property_id'] == property_id:
            return prop
    return None


def get_next_inquiry_id(inquiries):
    if not inquiries:
        return 1
    return max(inq['inquiry_id'] for inq in inquiries) + 1


def get_next_favorite_id(favorites):
    if not favorites:
        return 1
    return max(fav['favorite_id'] for fav in favorites) + 1


def property_in_favorites(property_id, favorites):
    for fav in favorites:
        if fav['property_id'] == property_id:
            return True
    return False


# --- Route Implementations ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    properties = load_properties()
    # Featured properties: choose first 5 available properties
    featured_properties = [p for p in properties if p['status'] == 'Available'][:5]
    # Recent listings: 5 most recent available (assuming sorted by property_id descending as proxy)
    recent_listings = sorted(
        [p for p in properties if p['status'] == 'Available'],
        key=lambda x: x['property_id'],
        reverse=True
    )[:5]
    return render_template('dashboard.html', featured_properties=featured_properties, recent_listings=recent_listings)


@app.route('/search', methods=['GET'])
def property_search():
    properties = load_properties()
    locations = load_locations()
    filter_options = {
        'selected_location': '',
        'price_min': 0,
        'price_max': 0,
        'property_type': ''
    }
    # Show all available properties by default
    properties = [prop for prop in properties if prop['status'] == 'Available']
    return render_template('search.html', properties=properties, locations=locations, filter_options=filter_options)


@app.route('/search', methods=['POST'])
def property_search_post():
    properties = load_properties()
    locations = load_locations()
    # Get filter options
    location_input = request.form.get('location_input', '').strip()
    try:
        price_range_min = int(request.form.get('price_range_min', '0'))
    except ValueError:
        price_range_min = 0
    try:
        price_range_max = int(request.form.get('price_range_max', '0'))
    except ValueError:
        price_range_max = 0
    property_type_filter = request.form.get('property_type_filter', '').strip()

    filtered_properties = [p for p in properties if p['status'] == 'Available']

    if location_input:
        filtered_properties = [p for p in filtered_properties if p['location'].lower() == location_input.lower()]
    if price_range_min > 0:
        filtered_properties = [p for p in filtered_properties if p['price'] >= price_range_min]
    if price_range_max > 0:
        filtered_properties = [p for p in filtered_properties if p['price'] <= price_range_max]
    if property_type_filter:
        filtered_properties = [p for p in filtered_properties if p['property_type'].lower() == property_type_filter.lower()]

    filter_options = {
        'selected_location': location_input,
        'price_min': price_range_min,
        'price_max': price_range_max,
        'property_type': property_type_filter
    }

    return render_template('search.html', properties=filtered_properties, locations=locations, filter_options=filter_options)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    property = get_property_by_id(property_id)
    if not property:
        # Could return 404, but specification doesn't say error handling specifically
        return "Property not found", 404
    agent = get_agent_by_id(property['agent_id'])

    favorites = load_favorites()
    is_favorite = property_in_favorites(property_id, favorites)

    return render_template('property_details.html', property=property, agent=agent, is_favorite=is_favorite)


@app.route('/property/<int:property_id>/favorite', methods=['POST'])
def add_to_favorites(property_id):
    property = get_property_by_id(property_id)
    if not property:
        return "Property not found", 404
    favorites = load_favorites()
    if property_in_favorites(property_id, favorites):
        # Already favorite, do nothing
        pass
    else:
        favorite_id = get_next_favorite_id(favorites)
        today_str = datetime.today().strftime('%Y-%m-%d')
        favorites.append({
            'favorite_id': favorite_id,
            'property_id': property_id,
            'added_date': today_str
        })
        write_favorites(favorites)

    agent = get_agent_by_id(property['agent_id'])
    is_favorite = True

    return render_template('property_details.html', property=property, agent=agent, is_favorite=is_favorite)


@app.route('/inquiry', methods=['GET'])
def inquiry_form():
    properties = load_properties()
    return render_template('inquiry.html', properties=properties)


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    properties = load_properties()
    # Get form data
    try:
        property_id = int(request.form.get('property_id', '').strip())
    except Exception:
        property_id = None
    inquiry_name = request.form.get('inquiry_name', '').strip()
    inquiry_email = request.form.get('inquiry_email', '').strip()
    inquiry_phone = request.form.get('inquiry_phone', '').strip()
    inquiry_message = request.form.get('inquiry_message', '').strip()

    submission_success = False

    # Validate required fields
    if property_id is not None and inquiry_name and inquiry_email and inquiry_phone and inquiry_message:
        inquiries = load_inquiries()
        new_id = get_next_inquiry_id(inquiries)
        today_str = datetime.today().strftime('%Y-%m-%d')
        inquiries.append({
            'inquiry_id': new_id,
            'property_id': property_id,
            'customer_name': inquiry_name,
            'customer_email': inquiry_email,
            'customer_phone': inquiry_phone,
            'message': inquiry_message,
            'inquiry_date': today_str,
            'status': 'Pending'
        })
        write_inquiries(inquiries)
        submission_success = True

    return render_template('inquiry.html', properties=properties, submission_success=submission_success)


@app.route('/inquiries', methods=['GET'])
def my_inquiries():
    inquiries = load_inquiries()
    return render_template('inquiries.html', inquiries=inquiries)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = load_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    write_inquiries(inquiries)
    return render_template('inquiries.html', inquiries=inquiries)


@app.route('/favorites', methods=['GET'])
def my_favorites():
    favorites = load_favorites()
    properties = load_properties()
    favorite_properties = []
    property_map = {p['property_id']: p for p in properties}
    for fav in favorites:
        prop = property_map.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)
    return render_template('favorites.html', favorite_properties=favorite_properties)


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = load_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    write_favorites(favorites)

    properties = load_properties()
    favorite_properties = []
    property_map = {p['property_id']: p for p in properties}
    for fav in favorites:
        prop = property_map.get(fav['property_id'])
        if prop:
            favorite_properties.append(prop)
    return render_template('favorites.html', favorite_properties=favorite_properties)


@app.route('/agents', methods=['GET'])
def agents_directory():
    agents = load_agents()
    return render_template('agents.html', agents=agents)


@app.route('/agents/search', methods=['POST'])
def agents_search():
    agents = load_agents()
    query = request.form.get('agent_search_query', '').strip().lower()
    if query:
        filtered_agents = [a for a in agents if query in a['agent_name'].lower() or query in a['specialization'].lower()]
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
    location_sort = request.form.get('location_sort', '')

    if location_sort == 'location_name_asc':
        locations = sorted(locations, key=lambda x: x['location_name'].lower())
    elif location_sort == 'location_name_desc':
        locations = sorted(locations, key=lambda x: x['location_name'].lower(), reverse=True)
    elif location_sort == 'average_price_asc':
        locations = sorted(locations, key=lambda x: x['average_price'])
    elif location_sort == 'average_price_desc':
        locations = sorted(locations, key=lambda x: x['average_price'], reverse=True)
    else:
        # No sorting or unknown option
        pass

    sort_option = location_sort
    return render_template('locations.html', locations=locations, sort_option=sort_option)


if __name__ == '__main__':
    app.run(debug=True)
