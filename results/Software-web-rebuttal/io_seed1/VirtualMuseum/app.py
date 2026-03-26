
```python

Main Python the application.
the server and all logic Flask.
Handles from and text files in 'data'
business Details,
Visitor Events, and Audio
navigation, searching, CRUD operations

render_template, request, flash
import os
datetime

app
Needed flash messages
= 'data'

Utility and pipe-delimited text
def
path os.path.join(DATA_DIR,

return
with open(path, 'r', f:
lines in f if
lines

def
path = os.path.join(DATA_DIR, filename)

for


def parse_pipe_line(line,
parts = line.split('|')
is None len(parts) !=
If not expected fields, or
return None



'|'.join(str(p) p

# ==========

=
return # list usernames

load_galleries():
lines
galleries
for line in
parts = parse_pipe_line(line,
parts:
{
                'gallery_id': parts[0],
                'gallery_name': parts[1],
                'floor': parts[2],
                'capacity': parts[3],
                'theme': parts[4],
                'status': parts[5]
            }

return galleries


=

line


exhibition {
                'exhibition_id': parts[0],
                'title': parts[1],
                'description': parts[2],
                'gallery_id': parts[3],
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            }

exhibitions

def
= read_lines('artifacts.txt')
artifacts
lines:
parts parse_pipe_line(line,

artifact {
                'artifact_id': parts[0],
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': parts[5],
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            }
artifacts.append(artifact)
return


lines
[]

parts =

{
                'guide_id': parts[0],
                'exhibit_number': parts[1],
                'title': parts[2],
                'language': parts[3],
                'duration': parts[4],
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            }



def
= read_lines('tickets.txt')

lines:
10)
if

int(parts[5])

number_of_tickets =

price =

=
{
                'ticket_id': parts[0],
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': number_of_tickets,
                'price': price,
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            }

tickets


lines = read_lines('events.txt')
=
in lines:
parse_pipe_line(line,


capacity

= 0
event = {
                'event_id': parts[0],
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': capacity,
                'description': parts[7],
                'created_by': parts[8]
            }

return


lines read_lines('event_registrations.txt')
registrations []
in lines:
= 4)
parts:
registration {
                'registration_id': parts[0],
                'event_id': parts[1],
                'username': parts[2],
                'registration_date': parts[3]
            }
registrations.append(registration)


def
lines = read_lines('collection_logs.txt')
[]
for line in
parse_pipe_line(line,
parts:
log = {
                'log_id': parts[0],
                'artifact_id': parts[1],
                'activity_type': parts[2],
                'date': parts[3],
                'notes': parts[4],
                'condition': parts[5],
                'curator': parts[6]
            }
logs.append(log)


========== ==========
def save_exhibitions(exhibitions):
[]
for


ex['end_date'],

lines.append(line)
write_lines('exhibitions.txt',

def save_artifacts(artifacts):
[]
for art artifacts:
line =
art['artifact_name'],
art['storage_location'], art['acquisition_date'],




def

for in
line format_pipe_line([
t['username'], t['visit_date'], t['visit_time'],
str(t['number_of_tickets']), t['visitor_email'],

lines.append(line)
lines)

save_event_registrations(registrations):
[]
for r
line = format_pipe_line([

])
lines.append(line)


# ========== Helper Functions
get_next_id(items,
max_id =
item


max_id:
max_id =
except:

return



return

return

def parse_datetime(date_str,

dt_str f"{date_str} {time_str}"
return %I:%M
except:
None



start

start and end:
<= <= end


def get_gallery_name(gallery_id, galleries):
g in galleries:
if == gallery_id:
return g['gallery_name']
'Unknown'


for in exhibitions:
if
return
return 'Unknown'



def
exhibitions
artifacts
galleries =

active_exhibitions = sum(1 in is_exhibition_active(ex))
return




Catalog --------
@app.route('/artifact_catalog', methods=['GET',
def

=
search_query =
filtered_artifacts artifacts
if ==
search_query =
if
filtered_artifacts [a a in artifacts a['artifact_name'].lower() or search_query == a['artifact_id']]

filtered_artifacts =
For artifact, exhibition title
for art in filtered_artifacts:
= exhibitions)




--------



galleries
=
filtered_exhibitions =
== 'POST':
filter_type =
if and 'All':
filtered_exhibitions = [ex for ex if ex['exhibition_type'].lower() filter_type.lower()]

= exhibitions
gallery for
filtered_exhibitions:

'Active' is_exhibition_active(ex) else
return

filter_type=filter_type)

--------
@app.route('/exhibition_details/<exhibition_id>')
def

artifacts
ex exhibition_id),
not
flash('Exhibition not

Get to exhibition
exhibition_artifacts = for a['exhibition_id']




--------


load_tickets()
# demonstration, assume visitor_mary

= in if username]

= '')
request.form.get('number-of-tickets', '')

visitor_email request.form.get('visitor-email', '').strip()
=
visit_time = '').strip()
# inputs
=
not
error 'Ticket type required.'
not int(number_of_tickets)
= of be a integer.'

error is required.'
not
error email

error =
not
error 'Visit is
error:


int(number_of_tickets)

= {
                'Standard': 15,
                'Student': 10,
                'Senior': 12,
                'Family': 40,
                'VIP': 50
            }
price_per_ticket
total_price number_of_tickets
tickets load_tickets()
new_ticket_id get_next_id(tickets,
purchase_date =
= {
                'ticket_id': new_ticket_id,
                'username': username,
                'ticket_type': ticket_type,
                'visit_date': visit_date,
                'visit_time': visit_time,
                'number_of_tickets': number_of_tickets,
                'price': total_price,
                'visitor_name': visitor_name,
                'visitor_email': visitor_email,
                'purchase_date': purchase_date
            }


successful.', 'success')
return redirect(url_for('visitor_tickets'))
return


-------- --------
@app.route('/virtual_events',


load_event_registrations()
assume username is visitor_mary implemented)

Build registration map quick
{r['event_id']: r for r in registrations if r['username'] == username}
==

request.form.get('event_id')
if == 'register':
# Check
if event_id in
already

Check
= e e['event_id'] None)
if event:
flash('Event found.',

for
= if
current_count >= event['capacity']:
flash('Event capacity reached.',
else:


= {
                            'registration_id': new_reg_id,
                            'event_id': event_id,
                            'username': username,
                            'registration_date': registration_date
                        }


flash('Successfully
#
user_registrations[event_id]
action 'cancel':
registration_id request.form.get('registration_id')
next((r if r['registration_id'] registration_id

registrations.remove(registration)

cancelled.',
None)

flash('Registration or unauthorized.',

# list with user

e events:
= user_registrations.get(e['event_id'])
= 'Registered' if else Registered'
event_list.append({
            'event_id': e['event_id'],
            'title': e['title'],
            'date': e['date'],
            'time': e['time'],
            'event_type': e['event_type'],
            'registration_status': registration_status,
            'registration_id': reg['registration_id'] if reg else None
        })



Audio Guides
@app.route('/audio_guides',
def audio_guides():
load_audioguides()
= ''
filtered_guides guides
if ==
filter_language = request.form.get('filter-language', '')
filter_language and
g guides if == filter_language.lower()]

filtered_guides guides


filter_language=filter_language)

#
__name__ ==
data directory
if not os.path.exists(DATA_DIR):


