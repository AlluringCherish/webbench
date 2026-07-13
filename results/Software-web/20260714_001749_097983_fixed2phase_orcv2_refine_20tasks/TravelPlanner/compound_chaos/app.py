from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read data from files

def read_destinations():
    destinations = []
    try:
        with open(os.path.join(DATA_DIR, 'destinations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    dest = {
                        'dest_id': parts[0],
                        'name': parts[1],
                        'country': parts[2],
                        'region': parts[3],
                        'description': parts[4],
                        'attractions': parts[5],
                        'climate': parts[6]
                    }
                    destinations.append(dest)
    except FileNotFoundError:
        pass
    return destinations


def read_destination_by_id(dest_id):
    destinations = read_destinations()
    for d in destinations:
        if d['dest_id'] == dest_id:
            return d
    return None


def read_itineraries():
    itineraries = []
    try:
        with open(os.path.join(DATA_DIR, 'itineraries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    itin = {
                        'itinerary_id': parts[0],
                        'itinerary_name': parts[1],
                        'destination': parts[2],
                        'start_date': parts[3],
                        'end_date': parts[4],
                        'activities': parts[5],
                        'status': parts[6]
                    }
                    itineraries.append(itin)
    except FileNotFoundError:
        pass
    return itineraries


def write_itineraries(itineraries):
    with open(os.path.join(DATA_DIR, 'itineraries.txt'), 'w', encoding='utf-8') as f:
        for itin in itineraries:
            line = '|'.join([
                itin['itinerary_id'],
                itin['itinerary_name'],
                itin['destination'],
                itin['start_date'],
                itin['end_date'],
                itin['activities'],
                itin['status']
            ])
            f.write(line + '\n')


@app.route('/')
def dashboard():
    destinations = read_destinations()
    itineraries = read_itineraries()

    # For featured destinations, just take first 3 for simplicity
    featured_destinations = destinations[:3]

    # Upcoming trips: those with start_date in the future (or all sorted by date because no current date logic)
    upcoming_trips = sorted(itineraries, key=lambda x: x['start_date'])[:3]

    return render_template('dashboard.html',
                           featured_destinations=featured_destinations,
                           upcoming_trips=upcoming_trips)


@app.route('/destinations')
def destinations():
    destinations = read_destinations()

    search_query = request.args.get('search', '').lower()
    region_filter = request.args.get('region', '')

    filtered_destinations = []
    for dest in destinations:
        if search_query:
            if search_query not in dest['name'].lower() and search_query not in dest['country'].lower():
                continue
        if region_filter and region_filter != dest['region']:
            continue
        filtered_destinations.append(dest)

    return render_template('destinations.html',
                           destinations=filtered_destinations,
                           search_query=search_query,
                           region_filter=region_filter)


@app.route('/destination/<dest_id>')
def destination_details(dest_id):
    destination = read_destination_by_id(dest_id)
    if not destination:
        return "Destination not found", 404
    return render_template('destination_details.html', destination=destination)


@app.route('/add_to_trip/<dest_id>', methods=['POST'])
def add_to_trip(dest_id):
    destination = read_destination_by_id(dest_id)
    if not destination:
        return "Destination not found", 404

    # Create a new itinerary entry with minimal info
    itineraries = read_itineraries()
    new_id = str(max([int(i['itinerary_id']) for i in itineraries] + [0]) + 1)
    # Default itinerary name and dates can be empty or placeholder
    new_itinerary = {
        'itinerary_id': new_id,
        'itinerary_name': f"Trip to {destination['name']}",
        'destination': destination['name'],
        'start_date': '',
        'end_date': '',
        'activities': '',
        'status': 'Planned'
    }
    itineraries.append(new_itinerary)
    write_itineraries(itineraries)
    return redirect(url_for('itinerary_page'))


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary_page():
    if request.method == 'POST':
        itinerary_id = request.form.get('itinerary_id')
        itinerary_name = request.form.get('itinerary_name')
        destination = request.form.get('destination')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        activities = request.form.get('activities')
        status = request.form.get('status') or 'Planned'

        itineraries = read_itineraries()

        if itinerary_id:  # Editing existing
            for itin in itineraries:
                if itin['itinerary_id'] == itinerary_id:
                    itin['itinerary_name'] = itinerary_name
                    itin['destination'] = destination
                    itin['start_date'] = start_date
                    itin['end_date'] = end_date
                    itin['activities'] = activities
                    itin['status'] = status
                    break
        else:  # Add new
            new_id = str(max([int(i['itinerary_id']) for i in itineraries] + [0]) + 1)
            new_itinerary = {
                'itinerary_id': new_id,
                'itinerary_name': itinerary_name,
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'activities': activities,
                'status': status
            }
            itineraries.append(new_itinerary)

        write_itineraries(itineraries)
        return redirect(url_for('itinerary_page'))

    itineraries = read_itineraries()
    edit_id = request.args.get('edit')
    edit_itinerary = None
    if edit_id:
        for itin in itineraries:
            if itin['itinerary_id'] == edit_id:
                edit_itinerary = itin
                break
    return render_template('itinerary.html', itineraries=itineraries, edit_itinerary=edit_itinerary)


@app.route('/delete_itinerary/<itinerary_id>', methods=['POST'])
def delete_itinerary(itinerary_id):
    itineraries = read_itineraries()
    itineraries = [i for i in itineraries if i['itinerary_id'] != itinerary_id]
    write_itineraries(itineraries)
    return redirect(url_for('itinerary_page'))


if __name__ == '__main__':
    app.run(debug=True)
