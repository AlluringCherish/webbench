from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load and save data files

def read_properties():
    result = []
    try:
        with open('data/properties.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 11:
                    continue
                result.append({
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
                })
    except (FileNotFoundError, IOError):
        result = []
    return result


def read_locations():
    result = []
    try:
        with open('data/locations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) !=6:
                    continue
                result.append({
                    'location_id': int(parts[0]),
                    'location_name': parts[1],
                    'region': parts[2],
                    'average_price': float(parts[3]),
                    'property_count': int(parts[4]),
                    'description': parts[5]
                })
    except (FileNotFoundError, IOError):
        result = []
    return result


def read_inquiries():
    result = []
    try:
        with open('data/inquiries.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                result.append({
                    'inquiry_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'customer_phone': parts[4],
                    'message': parts[5],
                    'inquiry_date': parts[6],
                    'status': parts[7]
                })
    except (FileNotFoundError, IOError):
        result = []
    return result


def write_inquiries(inquiries):
    try:
        with open('data/inquiries.txt', 'w', encoding='utf-8') as f:
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


def read_favorites():
    result = []
    try:
        with open('data/favorites.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                result.append({
                    'favorite_id': int(parts[0]),
                    'property_id': int(parts[1]),
                    'added_date': parts[2]
                })
    except (FileNotFoundError, IOError):
        result = []
    return result


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
    except IOError:
        pass


def read_agents():
    result = []
    try:
        with open('data/agents.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                result.append({
                    'agent_id': int(parts[0]),
                    'agent_name': parts[1],
                    'specialization': parts[2],
                    'email': parts[3],
                    'phone': parts[4],
                    'properties_sold': int(parts[5])
                })
    except (FileNotFoundError, IOError):
        result = []
    return result


# Flask route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    properties = read_properties()
    featured_properties = [p for p in properties if p['status'] == 'Available']
    featured_properties.sort(key=lambda x: x['property_id'])
    featured_properties = featured_properties[:5]
    return render_template('dashboard.html', featured_properties=featured_properties)


@app.route('/properties')
def property_search():
    properties = read_properties()
    available_properties = [p for p in properties if p['status'] == 'Available']
    return render_template('property_search.html', properties=available_properties)


@app.route('/property/<int:property_id>')
def property_details(property_id):
    properties = read_properties()
    prop = next((p for p in properties if p['property_id'] == property_id), None)
    if prop is None:
        return "Property not found", 404
    return render_template('property_details.html', property=prop)


@app.route('/property/<int:property_id>/add_to_favorites', methods=['POST'])
def add_to_favorites(property_id):
    favorites = read_favorites()
    properties = read_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return "Property not found", 404
    if any(f['property_id'] == property_id for f in favorites):
        # Already in favorites
        return redirect(url_for('my_favorites'))
    new_id = max([f['favorite_id'] for f in favorites], default=0) + 1
    added_date = datetime.now().strftime('%Y-%m-%d')
    favorites.append({'favorite_id': new_id, 'property_id': property_id, 'added_date': added_date})
    write_favorites(favorites)
    return redirect(url_for('my_favorites'))


@app.route('/property/<int:property_id>/inquiry', methods=['GET'])
def property_inquiry_form(property_id):
    properties = read_properties()
    selected_property = next((p for p in properties if p['property_id'] == property_id), None)
    if selected_property is None:
        return "Property not found", 404
    available_properties = [p for p in properties if p['status'] == 'Available']
    return render_template('property_inquiry.html', properties=available_properties, selected_property=selected_property)


@app.route('/property/<int:property_id>/inquiry', methods=['POST'])
def submit_inquiry(property_id):
    properties = read_properties()
    if not any(p['property_id'] == property_id for p in properties):
        return "Property not found", 404

    customer_name = request.form.get('customer_name')
    customer_email = request.form.get('customer_email')
    customer_phone = request.form.get('customer_phone')
    message = request.form.get('message')
    if not all([customer_name, customer_email, customer_phone, message]):
        return "Missing form data", 400

    inquiries = read_inquiries()
    new_id = max([iq['inquiry_id'] for iq in inquiries], default=0) + 1
    inquiry_date = datetime.now().strftime('%Y-%m-%d')

    new_inquiry = {
        'inquiry_id': new_id,
        'property_id': property_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
        'message': message,
        'inquiry_date': inquiry_date,
        'status': 'Pending'
    }
    inquiries.append(new_inquiry)
    write_inquiries(inquiries)
    return redirect(url_for('my_inquiries'))


@app.route('/inquiries')
def my_inquiries():
    inquiries = read_inquiries()
    inquiries.sort(key=lambda x: x['inquiry_date'], reverse=True)
    inquiry_status_filter_values = ['Pending', 'Contacted', 'Resolved']
    return render_template('my_inquiries.html', inquiries=inquiries, inquiry_status_filter_values=inquiry_status_filter_values)


@app.route('/inquiries/delete/<int:inquiry_id>', methods=['POST'])
def delete_inquiry(inquiry_id):
    inquiries = read_inquiries()
    new_inquiries = [iq for iq in inquiries if iq['inquiry_id'] != inquiry_id]
    if len(new_inquiries) == len(inquiries):
        return "Inquiry not found", 404
    write_inquiries(new_inquiries)
    return redirect(url_for('my_inquiries'))


@app.route('/favorites')
def my_favorites():
    favorites = read_favorites()
    properties = read_properties()
    fav_ids = {f['property_id'] for f in favorites}
    favorite_properties = [p for p in properties if p['property_id'] in fav_ids and p['status'] == 'Available']
    return render_template('my_favorites.html', favorite_properties=favorite_properties)


@app.route('/favorites/remove/<int:property_id>', methods=['POST'])
def remove_from_favorites(property_id):
    favorites = read_favorites()
    new_favorites = [f for f in favorites if f['property_id'] != property_id]
    if len(new_favorites) == len(favorites):
        return "Favorite not found", 404
    write_favorites(new_favorites)
    return redirect(url_for('my_favorites'))


@app.route('/agents')
def agent_directory():
    agents = read_agents()
    return render_template('agents.html', agents=agents)


@app.route('/locations')
def locations_page():
    locations = read_locations()
    return render_template('locations.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
