'''
Flask web application for real estate management.
Handles property listings, inquiries, favorites, agents, and locations.
Data stored in local text files.
'''
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
def read_properties():
    filepath = os.path.join(DATA_DIR, 'properties.txt')
    properties = []
    if not os.path.exists(filepath):
        return properties
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 11:
                continue
            try:
                property_id = int(parts[0])
                address = parts[1]
                location = parts[2]
                price = int(parts[3])
                property_type = parts[4]
                beds = int(parts[5])
                baths = float(parts[6])  # bathrooms can be float (e.g., 1.5)
                square_feet = int(parts[7])
                description = parts[8]
                agent_id = int(parts[9])
                status = parts[10].lower()
            except (ValueError, IndexError):
                continue
            properties.append({
                'property_id': property_id,
                'address': address,
                'location': location,
                'price': price,
                'property_type': property_type,
                'beds': beds,
                'baths': baths,
                'square_feet': square_feet,
                'description': description,
                'agent_id': agent_id,
                'status': status
            })
    return properties
def read_locations():
    filepath = os.path.join(DATA_DIR, 'locations.txt')
    locations = []
    if not os.path.exists(filepath):
        return locations
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            try:
                location_id = int(parts[0])
                location_name = parts[1]
                region = parts[2]
                average_price = int(parts[3])
                property_count = int(parts[4])
                description = parts[5]
            except (ValueError, IndexError):
                continue
            locations.append({
                'location_id': location_id,
                'location_name': location_name,
                'region': region,
                'average_price': average_price,
                'property_count': property_count,
                'description': description
            })
    return locations
def read_inquiries():
    filepath = os.path.join(DATA_DIR, 'inquiries.txt')
    inquiries = []
    if not os.path.exists(filepath):
        return inquiries
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            try:
                inquiry_id = int(parts[0])
                property_id = int(parts[1])
                customer_name = parts[2]
                customer_email = parts[3]
                customer_phone = parts[4]
                message = parts[5]
                inquiry_date = parts[6]
                status = parts[7]
            except (ValueError, IndexError):
                continue
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
    return inquiries
def write_inquiries(inquiries):
    filepath = os.path.join(DATA_DIR, 'inquiries.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for inquiry in inquiries:
            line = '|'.join([
                str(inquiry['inquiry_id']),
                str(inquiry['property_id']),
                inquiry['customer_name'],
                inquiry['customer_email'],
                inquiry['customer_phone'],
                inquiry['message'],
                inquiry['inquiry_date'],
                inquiry['status']
            ])
            f.write(line + '\n')
def read_favorites():
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    favorites = []
    if not os.path.exists(filepath):
        return favorites
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            try:
                favorite_id = int(parts[0])
                property_id = int(parts[1])
                added_date = parts[2]
            except (ValueError, IndexError):
                continue
            favorites.append({
                'favorite_id': favorite_id,
                'property_id': property_id,
                'added_date': added_date
            })
    return favorites
def write_favorites(favorites):
    filepath = os.path.join(DATA_DIR, 'favorites.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for fav in favorites:
            line = '|'.join([
                str(fav['favorite_id']),
                str(fav['property_id']),
                fav['added_date']
            ])
            f.write(line + '\n')
def read_agents():
    filepath = os.path.join(DATA_DIR, 'agents.txt')
    agents = []
    if not os.path.exists(filepath):
        return agents
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            try:
                agent_id = int(parts[0])
                agent_name = parts[1]
                specialization = parts[2]
                email = parts[3]
                phone = parts[4]
                properties_sold = int(parts[5])
            except (ValueError, IndexError):
                continue
            agents.append({
                'agent_id': agent_id,
                'agent_name': agent_name,
                'specialization': specialization,
                'email': email,
                'phone': phone,
                'properties_sold': properties_sold
            })
    return agents
@app.route('/')
def dashboard():
    properties = read_properties()
    featured_properties = [p for p in properties if p['status'] == 'available'][:3]
    recent_listings = sorted(properties, key=lambda x: x['property_id'], reverse=True)[:5]
    return render_template('dashboard.html',
                           featured_properties=featured_properties,
                           recent_listings=recent_listings)
@app.route('/properties')
def property_search():
    properties = read_properties()
    locations = list(set(p['location'] for p in properties))
    property_types = list(set(p['property_type'] for p in properties))
    location_filter = request.args.get('location', '').strip().lower()
    price_min = request.args.get('price_min', '').strip()
    price_max = request.args.get('price_max', '').strip()
    property_type_filter = request.args.get('property_type', '').strip()
    filtered_properties = properties
    if location_filter:
        filtered_properties = [p for p in filtered_properties if p['location'].lower() == location_filter]
    if price_min.isdigit():
        filtered_properties = [p for p in filtered_properties if p['price'] >= int(price_min)]
    if price_max.isdigit():
        filtered_properties = [p for p in filtered_properties if p['price'] <= int(price_max)]
    if property_type_filter and property_type_filter in property_types:
        filtered_properties = [p for p in filtered_properties if p['property_type'] == property_type_filter]
    return render_template('property_search.html',
                           properties=filtered_properties,
                           locations=locations,
                           property_types=property_types,
                           location_filter=location_filter,
                           price_min=price_min,
                           price_max=price_max,
                           property_type_filter=property_type_filter)
@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = read_properties()
    property_obj = next((p for p in properties if p['property_id'] == property_id), None)
    if not property_obj:
        abort(404)
    favorites = read_favorites()
    is_favorite = any(fav['property_id'] == property_id for fav in favorites)
    return render_template('property_details.html',
                           property=property_obj,
                           is_favorite=is_favorite)
@app.route('/add_favorite/<int:property_id>', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    if any(fav['property_id'] == property_id for fav in favorites):
        return redirect(url_for('property_details', property_id=property_id))
    new_id = max((fav['favorite_id'] for fav in favorites), default=0) + 1
    favorites.append({
        'favorite_id': new_id,
        'property_id': property_id,
        'added_date': datetime.now().strftime('%Y-%m-%d')
    })
    write_favorites(favorites)
    return redirect(url_for('property_details', property_id=property_id))
@app.route('/remove_favorite/<int:property_id>', methods=['POST'])
def remove_favorite(property_id):
    favorites = read_favorites()
    favorites = [fav for fav in favorites if fav['property_id'] != property_id]
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))
@app.route('/property_inquiry', methods=['GET', 'POST'])
def property_inquiry():
    properties = read_properties()
    if request.method == 'POST':
        property_id = request.form.get('select_property')
        customer_name = request.form.get('inquiry_name', '').strip()
        customer_email = request.form.get('inquiry_email', '').strip()
        customer_phone = request.form.get('inquiry_phone', '').strip()
        message = request.form.get('inquiry_message', '').strip()
        if not (property_id and customer_name and customer_email and customer_phone and message):
            error = "Please fill in all fields."
            return render_template('property_inquiry.html', properties=properties, error=error)
        try:
            property_id = int(property_id)
        except ValueError:
            error = "Invalid property selected."
            return render_template('property_inquiry.html', properties=properties, error=error)
        inquiries = read_inquiries()
        new_id = max((inq['inquiry_id'] for inq in inquiries), default=0) + 1
        inquiries.append({
            'inquiry_id': new_id,
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'Pending'
        })
        write_inquiries(inquiries)
        return redirect(url_for('my_inquiries'))
    return render_template('property_inquiry.html', properties=properties)
@app.route('/inquiries', methods=['GET'])
def my_inquiries():
    inquiries = read_inquiries()
    properties = {p['property_id']: p for p in read_properties()}
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        inquiries = [inq for inq in inquiries if inq['status'] == status_filter]
    return render_template('inquiries.html',
                           inquiries=inquiries,
                           properties=properties,
                           status_filter=status_filter)
@app.route('/delete_inquiry/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    inquiries = [inq for inq in inquiries if inq['inquiry_id'] != inquiry_id]
    write_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))
@app.route('/my_favorites')
def my_favorites():
    favorites = read_favorites()
    properties = {p['property_id']: p for p in read_properties()}
    favorite_properties = [properties[fav['property_id']] for fav in favorites if fav['property_id'] in properties]
    return render_template('my_favorites.html', favorite_properties=favorite_properties)
@app.route('/agents')
def agents():
    agents_list = read_agents()
    search_name = request.args.get('search_name', '').strip().lower()
    if search_name:
        agents_list = [agent for agent in agents_list if search_name in agent['agent_name'].lower()]
    return render_template('agents.html', agents=agents_list, search_name=search_name)
@app.route('/locations')
def locations():
    locations_list = read_locations()
    sort_by = request.args.get('sort_by', 'Name')
    if sort_by == 'Name':
        locations_list.sort(key=lambda x: x['location_name'])
    elif sort_by == 'By Count':
        locations_list.sort(key=lambda x: x['property_count'], reverse=True)
    elif sort_by == 'By Price':
        locations_list.sort(key=lambda x: x['average_price'], reverse=True)
    return render_template('locations.html', locations=locations_list, sort_by=sort_by)
if __name__ == '__main__':
    app.run(debug=True)