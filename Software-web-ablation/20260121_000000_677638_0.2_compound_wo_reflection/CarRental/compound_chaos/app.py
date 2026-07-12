from Flask, request, redirect,
import datetime



=

DATA_DIR

functions and files


[]
try:
open(os.path.join(DATA_DIR, 'vehicles.txt'), 'r') f:
for
= line.strip().split('|')
if 9:

{
                    'vehicle_id': int(parts[0]),
                    'make': parts[1],
                    'model': parts[2],
                    'vehicle_type': parts[3],
                    'daily_rate': float(parts[4]),
                    'seats': int(parts[5]),
                    'transmission': parts[6],
                    'fuel_type': parts[7],
                    'status': parts[8]
                }


pass
vehicles




try:
with 'locations.txt'), 'r')
line f:
parts =


= {
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                }


pass
return locations




try:
'r') f:
line f:
parts line.strip().split('|')
if !=
continue
{
                    'rental_id': int(parts[0]),
                    'vehicle_id': int(parts[1]),
                    'customer_id': int(parts[2]),
                    'pickup_date': parts[3],  # YYYY-MM-DD string
                    'dropoff_date': parts[4],
                    'pickup_location': parts[5],
                    'dropoff_location': parts[6],
                    'total_price': float(parts[7]),
                    'status': parts[8]
                }
rentals.append(rental)
except

return


def

try:
open(os.path.join(DATA_DIR, f:

parts = line.strip().split('|')
if len(parts) != 6:



if in deductible:
float(deductible)

deductible int(deductible)
except
pass
insurance = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': parts[4],
                    'deductible': deductible
                }
insurances.append(insurance)
Exception:

return insurances





'reservations.txt'),
for line f:
line.strip().split('|')


= {
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                }

Exception:
pass
return reservations

write function for reservations



open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') f:
for
= f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"





to needed asked but in data consistency)
def write_rentals(rentals):

with open(os.path.join(DATA_DIR, 'rentals.txt'), 'w') as
for r in rentals:
=





root_redirect():


app.add_url_rule('/', 'root_redirect', root_redirect,


methods=['GET'])

=
# dict representing
# first 5 as featured

[
off rentals!",
"Free GPS rentals over 3 days.",
to time
]
return featured_vehicles=featured_vehicles, promotions=promotions)



def
vehicles =

locations sorted({loc['city'] for loc in locations_data})

vehicles))

parameters filtering
{
        'location': request.args.get('location', ''),
        'vehicle_type': request.args.get('vehicle_type', ''),
        'date_range': request.args.get('date_range', '')
    }

# Apply
filtered_vehicles vehicles

# Filter if
filters['location']:
# vehicles that matching
Since vehicles do have location assume vehicles might differ
The design_spec logic just pass
So do here.


Filter
filters['vehicle_type']:
filtered_vehicles [v filtered_vehicles v['vehicle_type']

For filtering: filter by date


vehicle_types=vehicle_types,



vehicle_details(vehicle_id):
=
vehicle vehicles vehicle_id),

Load as context variable
no empty list
reviews




methods=['GET', 'POST'])


= next((v v in vehicles if v['vehicle_id'] == None)

sorted({loc['city'] for loc in locations_data})

= {'pickup_location': '', 'dropoff_location': '', 'pickup_date': '', 'dropoff_date': ''}
=

if
post price calculation or proceed
pickup_location
dropoff_location = '').strip()
pickup_date
= request.form.get('dropoff_date',



input dates

p_date
=
if > d_date:
total_price = None

= (d_date p_date).days +
total_price round(days vehicle['daily_rate'],
Exception:
=

# Check if user (hidden field or button name)
if 'proceed_to_insurance' in is not None:
reservation to get
since no customer ID is specification, create for
create dummy rental_id, reservation_id for next pages




r
max_reservation_id = in


+

a rental entry

dummy = info is user
0


pickup_dt_obj
dropoff_dt_obj = datetime.strptime(dropoff_date,

pickup_dt_obj


{
                'rental_id': new_rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': dummy_customer_id,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location,
                'total_price': total_price,
                'status': 'Pending'
            }
rentals.append(rental_record)


= {
                'reservation_id': new_reservation_id,
                'rental_id': new_rental_id,
                'vehicle_id': vehicle_id,
                'customer_id': dummy_customer_id,
                'status': 'Pending',
                'insurance_id': 0,
                'special_requests': ''
            }



redirect(url_for('insurance_options', reservation_id=new_reservation_id))

return locations=locations, total_price=total_price)


methods=['GET',
insurance_options(reservation_id):
insurance_plans
=

for in reservations res['reservation_id'] reservation_id),

id
return



if == 'POST':
# insurance id form
request.form.get('insurance_id')
try:
selected_insurance_id int(selected_id)
Exception:


not
= in ip['insurance_id'] == selected_insurance_id), None)
plan:
selected_plan
Update Confirmed
= selected_insurance_id
reservation['status'] =
Persist
write_reservations(reservations)
to management after confirmation
redirect(url_for('reservation_management'))

!=
= for ip insurance_plans None)

render_template('insurance.html', selected_plan=selected_plan, reservation_id=reservation_id)


methods=['GET'])

=
= request.args.get('filter_status', 'All')

if filter_status !=
= [r in if r['status'] ==

render_template('history.html',


methods=['GET', 'POST'])

= read_reservations()
sorted_by_date

'POST':
modify reservation
if
Sort reservations rental pickup_date
rentals
{r['rental_id']: r for r in rentals}
try:



pass

Check operations

simplicity specified, just redirect back
pass
'cancel_reservation_id'


int(cancel_id)
in reservations:
if res['reservation_id']
= 'Cancelled'

break
except


return sorted_by_date=sorted_by_date)


'POST'])
def special_requests():
reservations =


if request.method ==
= request.form.get('reservation_id')
driver_assistance =
=
child_seat_qty
special_notes = request.form.get('special_notes',

try:
reservation_id_int = int(selected_reservation_id)
= else

=
driver_assistance 'on':

gps_option
requested')
child_seat_qty_int 0:
{child_seat_qty_int}')
if


'.join(special_texts) if special_texts ''

# reservation
found =
res
res['reservation_id'] == reservation_id_int:
=


found:

submission_status successfully.'


except
submission_status 'Invalid

return



locations_page():
locations

filter_hours request.args.get('filter_hours',
= '').lower()




# filter_hours substring
for loc filter_hours in loc['hours']]

search_query:
filtered_locations if in loc['city'].lower() search_query



__name__ ==

