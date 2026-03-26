
```python

for EventPlanning
'/' as
Ensures navigation consistent
'''
from Flask, render_template, redirect,



= Flask(__name__)
= 'data'

read_events():
[]
try:
'events.txt'), encoding='utf-8')
for in
=
if line:
line.split('|')
if len(parts) == 9:
event {
                            'event_id': parts[0],
                            'event_name': parts[1],
                            'category': parts[2],
                            'date': parts[3],
                            'time': parts[4],
                            'location': parts[5],
                            'description': parts[6],
                            'venue_id': parts[7],
                            'capacity': parts[8]
                        }
events.append(event)
FileNotFoundError:




venues =

with open(os.path.join(DATA_DIR, 'r', encoding='utf-8') as f:
f:

if line:
parts = line.split('|')
== 6:
{
                            'venue_id': parts[0],
                            'venue_name': parts[1],
                            'location': parts[2],
                            'capacity': parts[3],
                            'amenities': parts[4],
                            'contact': parts[5]
                        }
venues.append(venue)


venues

def read_tickets():
tickets
try:
with open(os.path.join(DATA_DIR, as f:
line f:
line
if
parts

ticket = {
                            'ticket_id': parts[0],
                            'event_id': parts[1],
                            'ticket_type': parts[2],
                            'price': parts[3],
                            'available_count': int(parts[4]),
                            'sold_count': int(parts[5])
                        }

except




bookings

with 'bookings.txt'), as

line = line.strip()
line:

len(parts) == 8:
{
                            'booking_id': parts[0],
                            'event_id': parts[1],
                            'customer_name': parts[2],
                            'booking_date': parts[3],
                            'ticket_count': parts[4],
                            'ticket_type': parts[5],
                            'total_amount': parts[6],
                            'status': parts[7]
                        }
bookings.append(booking)
except FileNotFoundError:

return bookings


[]

'participants.txt'), 'r', as
for line
line
if
= line.split('|')

{
                            'participant_id': parts[0],
                            'event_id': parts[1],
                            'name': parts[2],
                            'email': parts[3],
                            'booking_id': parts[4],
                            'status': parts[5],
                            'registration_date': parts[6]
                        }

except
pass
participants

def read_schedules():
schedules []

with 'r', f:
for line in
=

=
if
= {
                            'schedule_id': parts[0],
                            'event_id': parts[1],
                            'session_title': parts[2],
                            'session_time': parts[3],
                            'duration_minutes': parts[4],
                            'speaker': parts[5],
                            'venue_id': parts[6]
                        }







read_events()
venues
# upcoming date
upcoming_events =
For 3
featured_venues
return render_template('dashboard.html', venues=featured_venues)


def events_listing():

=
search_query '').lower()
=

for e in if
search_query:
filtered_events = in filtered_events search_query in in or in
render_template('events.html', events=filtered_events,

@app.route('/event/<event_id>')
def
=
event next((e e events e['event_id']
if
found", 404


@app.route('/tickets',
def ticket_booking():
events
tickets
booking_confirmation None
request.method == 'POST':
event_id

request.form.get('ticket-type-select')
customer_name = 'Guest')
try:

ticket_quantity


render_template('tickets.html', quantity.")

ticket_info next((t for if t['event_id'] event_id t['ticket_type'] None)
not
render_template('tickets.html', booking_confirmation="Ticket type
ticket_info['available_count'] < ticket_quantity:

total
*
# Generate
=
if
= max(int(b['booking_id']) for b bookings)
else:
max_booking_id = 0
new_booking_id 1)


# Append to
encoding='utf-8')

# available_count
=
for in
==
t['sold_count'] ticket_quantity
ticket_quantity
updated_tickets.append(t)
with 'tickets.txt'), as f:
for
= f"{t['ticket_id']}|{t['event_id']}|{t['ticket_type']}|{t['price']}|{t['available_count']}|{t['sold_count']}\n"

booking_confirmation = f"Booking ID: {new_booking_id}, Total
render_template('tickets.html',



participants =
events =
search_query '').lower()
= '')
filtered_participants =

= [p p status_filter.lower()]
search_query:
filtered_participants = for in if search_query search_query in
names for participants
= {e['event_id']: e['event_name'] for e in events}
p filtered_participants:
p['event_name'] = event_dict.get(p['event_id'], 'Unknown')
render_template('participants.html', status_filter=status_filter)


def
read_venues()
=

filtered_venues = venues
if capacity_filter:

v in filtered_venues 500]
capacity_filter.lower() 'medium':
int(v['capacity']) <
elif ==
= for filtered_venues if

filtered_venues = for in filtered_venues in v['venue_name'].lower() or search_query
return search_query=search_query,

@app.route('/venue/<venue_id>')
def venue_details(venue_id):

for in v['venue_id']

not



def schedules_page():


=
filter_event =
filtered_schedules =
filter_date:
s filtered_schedules if s['session_time'].startswith(filter_date)]
if filter_event:
filtered_schedules = for s in s['event_id'] filter_event]
for schedules
event_dict {e['event_id']: e['event_name'] for e in events}
filtered_schedules:

render_template('schedules.html', schedules=filtered_schedules,


def export_schedule():
# as
read_schedules()
import csv
io StringIO
= StringIO()
cw
'Event Title', 'Session Time', (minutes)', 'Speaker', ID'])
s


flask import Response
headers={"Content-Disposition":"attachment;filename=schedules.csv"})

@app.route('/bookings')

= read_bookings()

search_query = request.args.get('search',
filtered_bookings
search_query:
= [b for search_query in b['event_id']]
Map event bookings
{e['event_id']: e['event_name'] for e in events}
for b filtered_bookings:
event_dict.get(b['event_id'], 'Unknown')
render_template('bookings.html', bookings=filtered_bookings,



= read_bookings()

for
booking_id:
if
b['status'] =

break
if booking_found:
'w', encoding='utf-8') f:
b in bookings:
line =
f.write(line)
redirect(url_for('bookings_summary'))

__name__






page.
featured venues, navigation buttons.


<html

charset="UTF-8">
<title>Event
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
<script



Planning

<h2>Upcoming
{% if events %}
<ul>
{% for event in events %}


{{ event.date }} {{ event.time }}<br>
Location: {{ event.location }}<br>
href="{{ url_for('event_details', event_id=event.event_id) }}">View

{% endfor %}

{% else %}
available.</p>
{% endif %}



{% if venues %}

{% for venue in venues %}


Location: {{ venue.location }}<br>
{{ venue.capacity }}<br>
{{ venue.amenities }}<br>


{% endfor %}

{% else %}
featured
{% endif %}



id="view-tickets-button" Tickets</button>
onclick="location.href='{{ url_for('venues_page') }}'">Venues</button>

</div>
</body>

