from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
DATA_DIR = 'data'

### Utility functions to read and write data from/to text files ###

def read_properties():
    path = os.path.join(DATA_DIR, 'properties.txt')
    properties = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 11:
                        property_id = int(parts[0])
                        address = parts[1]
                        location = parts[2]
                        price = int(parts[3])
                        property_type = parts[4]
                        bedrooms = int(parts[5])
                        bathrooms = float(parts[6])
                        square_feet = int(parts[7])
                        description = parts[8]
                        agent_id = int(parts[9])
                        status = parts[10]
                        properties.append({
                            'property_id': property_id,
                            'address': address,
                            'location': location,
                            'price': price,
                            'property_type': property_type,
                            'bedrooms': bedrooms,
                            'bathrooms': bathrooms,
                            'square_feet': square_feet,
                            'description': description,
                            'agent_id': agent_id,
                            'status': status
                        })
    except Exception as e:
        # Could log error here
        pass
    return properties

def read_locations():
    path = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        location_id = int(parts[0])
                        location_name = parts[1]
                        region = parts[2]
                        average_price = int(parts[3])
                        property_count = int(parts[4])
                        description = parts[5]
                        locations.append({
                            'location_id': location_id,
                            'location_name': location_name,
                            'region': region,
                            'average_price': average_price,
                            'property_count': property_count,
                            'description': description
                        })
    except Exception as e:
        pass
    return locations

def read_inquiries():
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    inquiries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        inquiry_id = int(parts[0])
                        property_id = int(parts[1])
                        customer_name = parts[2]
                        customer_email = parts[3]
                        customer_phone = parts[4]
                        message = parts[5]
                        inquiry_date = parts[6]
                        status = parts[7]
                        inquiries.append({
                            'inquiry_id': inquiry_id,
                            'property_id': property_id,
                            'customer_name': customer_name,
                            'customer_email': customer_email,
                            'customer_phone': customer_phone,
                            'message': message,
                            'inquiry_date': inquiry_date,
                            'status': status
                        })
    except Exception as e:
        pass
    return inquiries

def read_favorites():
    path = os.path.join(DATA_DIR, 'favorites.txt')
    favorites = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        favorite_id = int(parts[0])
                        property_id = int(parts[1])
                        added_date = parts[2]
                        favorites.append({
                            'favorite_id': favorite_id,
                            'property_id': property_id,
                            'added_date': added_date
                        })
    except Exception as e:
        pass
    return favorites

def read_agents():
    path = os.path.join(DATA_DIR, 'agents.txt')
    agents = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        agent_id = int(parts[0])
                        agent_name = parts[1]
                        specialization = parts[2]
                        email = parts[3]
                        phone = parts[4]
                        properties_sold = int(parts[5])
                        agents.append({
                            'agent_id': agent_id,
                            'agent_name': agent_name,
                            'specialization': specialization,
                            'email': email,
                            'phone': phone,
                            'properties_sold': properties_sold
                        })
    except Exception as e:
        pass
    return agents

def write_inquiries(inquiries):
    path = os.path.join(DATA_DIR, 'inquiries.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for i in inquiries:
                line = f"{i['inquiry_id']}|{i['property_id']}|{i['customer_name']}|{i['customer_email']}|{i['customer_phone']}|{i['message']}|{i['inquiry_date']}|{i['status']}\n"
                f.write(line)
    except Exception as e:
        pass

def write_favorites(favorites):
    path = os.path.join(DATA_DIR, 'favorites.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for favo in favorites:
                line = f"{favo['favorite_id']}|{favo['property_id']}|{favo['added_date']}\n"
                f.write(line)
    except Exception as e:
        pass

### Helper to get an agent by ID

def get_agent_by_id(agent_id):
    agents = read_agents()
    for agent in agents:
        if agent['agent_id'] == agent_id:
            return agent
    return None


### Routes ###

@app.route('/')
def dashboard():
    properties = read_properties()
    # Featured properties: show first 5 available properties as recommendation
    featured_properties = [p for p in properties if p['status'] == 'Available'][:5]
    return render_template('dashboard.html', featured_properties=featured_properties)


@app.route('/search')
def property_search():
    properties = read_properties()
    # Filters from query args
    location = request.args.get('location', '').strip()
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    property_type = request.args.get('property_type', '')

    # Convert price filters to int or None
    try:
        price_min_val = int(price_min) if price_min else None
    except:
        price_min_val = None
    try:
        price_max_val = int(price_max) if price_max else None
    except:
        price_max_val = None

    # Filter properties
    filtered = []
    for p in properties:
        if p['status'] != 'Available':
            continue
        if location and location.lower() not in p['location'].lower():
            continue
        if property_type and property_type != '':
            if property_type != p['property_type']:
                continue
        if price_min_val is not None and p['price'] < price_min_val:
            continue
        if price_max_val is not None and p['price'] > price_max_val:
            continue
        filtered.append(p)

    return render_template('property_search.html',
            properties=filtered,
            filter_location=location,
            filter_price_min=price_min_val,
            filter_price_max=price_max_val,
            filter_property_type=property_type
    )


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = read_properties()
    property_obj = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_obj:
        return "Property not found", 404

    agent = get_agent_by_id(property_obj['agent_id'])

    # Check if property is in favorites
    favorites = read_favorites()
    is_favorite = any(f['property_id'] == property_id for f in favorites)

    return render_template('property_details.html',
                           property=property_obj,
                           agent=agent,
                           is_favorite=is_favorite)


@app.route('/property/<int:property_id>/add_favorite', methods=['POST'])
def add_favorite(property_id):
    properties = read_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return "Property not found", 404
    favorites = read_favorites()
    if not any(f['property_id'] == property_id for f in favorites):
        # Add favorite
        max_id = max([f['favorite_id'] for f in favorites], default=0)
        added_date = datetime.now().strftime('%Y-%m-%d')
        favorites.append({'favorite_id': max_id+1, 'property_id': property_id, 'added_date': added_date})
        write_favorites(favorites)
    return redirect(url_for('property_details', property_id=property_id))


@app.route('/inquiry/submit', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    submission_status = None

    if request.method == 'POST':
        prop_id = request.form.get('select_property')
        name = request.form.get('inquiry_name', '').strip()
        email = request.form.get('inquiry_email', '').strip()
        phone = request.form.get('inquiry_phone', '').strip()
        message = request.form.get('inquiry_message', '').strip()

        if not prop_id or not name or not email or not message:
            submission_status = 'Please fill in all required fields.'
        else:
            try:
                prop_id_int = int(prop_id)
                properties_ids = [p['property_id'] for p in properties]
                if prop_id_int not in properties_ids:
                    submission_status = 'Selected property does not exist.'
                else:
                    inquiries = read_inquiries()
                    max_id = max([i['inquiry_id'] for i in inquiries], default=0)
                    today = datetime.now().strftime('%Y-%m-%d')
                    new_inquiry = {
                        'inquiry_id': max_id + 1,
                        'property_id': prop_id_int,
                        'customer_name': name,
                        'customer_email': email,
                        'customer_phone': phone,
                        'message': message,
                        'inquiry_date': today,
                        'status': 'Pending'
                    }
                    inquiries.append(new_inquiry)
                    write_inquiries(inquiries)
                    submission_status = 'Inquiry submitted successfully.'
            except:
                submission_status = 'Invalid property selection.'

    return render_template('property_inquiry.html', properties=properties, submission_status=submission_status)


@app.route('/inquiries')
def my_inquiries():
    inquiries = read_inquiries()
    properties = read_properties()
    status_filter = request.args.get('status_filter', 'All')

    # Join inquiries with property details
    prop_dict = {p['property_id']: p for p in properties}
    filtered_inquiries = []
    for inq in inquiries:
        if status_filter == 'All' or inq['status'] == status_filter:
            prop = prop_dict.get(inq['property_id'], None)
            if prop:
                filtered_inquiries.append({
                    'inquiry_id': inq['inquiry_id'],
                    'property': prop,
                    'customer_name': inq['customer_name'],
                    'customer_email': inq['customer_email'],
                    'customer_phone': inq['customer_phone'],
                    'message': inq['message'],
                    'inquiry_date': inq['inquiry_date'],
                    'status': inq['status']
                })

    return render_template('my_inquiries.html', inquiries=filtered_inquiries, status_filter=status_filter)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    write_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


@app.route('/favorites')
def my_favorites():
    favorites = read_favorites()
    properties = read_properties()
    prop_dict = {p['property_id']: p for p in properties}
    # Combine favorites with full property details
    combined = []
    for favo in favorites:
        prop = prop_dict.get(favo['property_id'], None)
        if prop:
            fav_copy = favo.copy()
            fav_copy.update(prop)
            combined.append(fav_copy)
    
    return render_template('my_favorites.html', favorites=combined)


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = read_favorites()
    favorites = [f for f in favorites if f['property_id'] != property_id]
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))


@app.route('/agents')
def agent_directory():
    agents = read_agents()
    search_query = request.args.get('search_query', '').strip()
    filtered_agents = []
    if search_query == '':
        filtered_agents = agents
    else:
        search_lower = search_query.lower()
        for agent in agents:
            if search_lower in agent['agent_name'].lower():
                filtered_agents.append(agent)
    return render_template('agent_directory.html', agents=filtered_agents, search_query=search_query)


@app.route('/locations')
def locations_page():
    locations = read_locations()
    sort_option = request.args.get('sort_option', 'By Name')

    if sort_option == 'By Name':
        locations.sort(key=lambda loc: loc['location_name'].lower())
    elif sort_option == 'By Properties Count':
        locations.sort(key=lambda loc: loc['property_count'], reverse=True)
    elif sort_option == 'By Average Price':
        locations.sort(key=lambda loc: loc['average_price'], reverse=True)

    return render_template('locations.html', locations=locations, sort_option=sort_option)


@app.route('/locations/view/<int:location_id>')
def view_location_properties(location_id):
    # Show properties filtered by location
    properties = read_properties()
    location_obj = None
    locations = read_locations()
    for loc in locations:
        if loc['location_id'] == location_id:
            location_obj = loc
            break
    if not location_obj:
        return "Location not found", 404
    filtered_properties = [p for p in properties if p['location'] == location_obj['location_name'] and p['status'] == 'Available']
    return render_template('property_search.html', 
                           properties=filtered_properties, 
                           filter_location=location_obj['location_name'],
                           filter_price_min=None,
                           filter_price_max=None,
                           filter_property_type='')


if __name__ == '__main__':
    app.run(debug=True)
