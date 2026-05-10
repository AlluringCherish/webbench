main.py
```python

Flask RestaurantReservation web application.
routes including the the
Ensures all uses for consistent

import redirect,
import
from datetime
Flask(__name__)
DATA_DIR =
load data from files
def load_users():
= {}

'r')
line in
line
if line:
full_name =
{
                        'email': email,
                        'phone': phone,
                        'full_name': full_name
                    }


return
def load_menu():
menu

with open(os.path.join(DATA_DIR, f:
line in
line line.strip()

name, price,

except

return
def load_reservations():
= []

with f:
line f:
line.strip()
if
(reservation_id, date, time, special_requests, =

FileNotFoundError:

return reservations
def load_waitlist():
waitlist []

'waitlist.txt'), f:
for line
line.strip()
if
join_time, status line.split('|')
waitlist.append({
                        'waitlist_id': waitlist_id,
                        'username': username,
                        'party_size': party_size,
                        'join_time': join_time,
                        'status': status
                    })
except FileNotFoundError:
pass
waitlist
def load_reviews():
=
try:
with 'reviews.txt'),

line = line.strip()

review_id, dish_id, line.split('|')


pass
return
demonstration, assume




the Dashboard main
Displays welcome upcoming and navigation
'''
users = load_users()
menu load_menu()

user_info = users.get(current_user, {})
by avg_rating
= sorted(menu, float(d['avg_rating']), reverse=True)[:3]
reservations for user
= for reservations r['status']
return
username=current_user,






the Menu
Displays all with navigation to
'''
=
return render_template('menu.html',

def
'''
Route for Dish Details
Displays detailed about a
'''
load_menu()
dish if None)

return "Dish not
return dish=dish)
'POST'])

'''
for Make page.
Show
Process reservation and file.

users =
=
request.method == 'POST':

=
=
reservation_time '').strip()
special_requests = '').strip()
# required fields
if or
flash message or error
error="Please
# new
= load_reservations()
if
= str(int(max(r['reservation_id'] r reservations)) +

=
Save new



guest_name else
user_info.get('phone', ''),




special_requests,

])
with 'reservations.txt'),
+
redirect(url_for('my_reservations'))
return



for page.
Displays made the

load_reservations()
user_reservations = for in reservations current_user]
return render_template('my_reservations.html', reservations=user_reservations)


'''
Route to cancel a
to in
'''

False
r
r['reservation_id'] r['username'] == and r['status'] == 'Upcoming':

=
break

with 'reservations.txt'),

=
r['reservation_id'],
r['date'], r['time'], r['special_requests'], r['status']

f.write(line
return



Route for Waitlist
waitlist and
POST: to waitlist.
'''
= load_waitlist()
for w if current_user w['status'] 'Active']
user_position None

by
sorted([w w in if 'Active'],
idx, start=1):
if w['username'] current_user:


if ==
party_size
if
return render_template('waitlist.html', a party
user_waitlist:
# Generate new

= in waitlist)) +

new_id
=
line '|'.join([new_id, party_size,
open(os.path.join(DATA_DIR, 'waitlist.txt'), as f:
f.write(line
return
render_template('waitlist.html',
@app.route('/my_reviews')


page.
Displays the

reviews
menu
= r['username'] == current_user]
dish name to review

= in if None)
r['dish_name'] else 'Unknown
reviews=user_reviews)

write_review():

for Write Review
to review.
POST: Save the review file.
'''
load_menu()
'POST':
request.form.get('select-dish',
= request.form.get('rating-input',
review_text = '').strip()
if not or rating
return menu=menu,
datetime.now().strftime('%Y-%m-%d')


= r in reviews)) 1)
else:
new_id = '1'
'|'.join([new_id, current_user, review_text, review_date])
'reviews.txt'), as


render_template('write_review.html', menu=menu)
@app.route('/profile', methods=['GET',
def
'''
User Profile
GET:
POST: Update in users.txt.

=
user_info users.get(current_user,
if request.method 'POST':
'').strip()
new_email:


'users.txt'), f:
username, info users.items():
= info['email'],

redirect(url_for('profile'))
render_template('profile.html',
__name__ == '__main__':

