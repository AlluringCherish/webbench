books_map success=False, if max(reviews_map.keys(), as message=message) books if book:
for if 'john_reader' not parts
= read_books()

continue borrow if
existing_review=existing_review) 'Profile r['username']

# message =

read_books() if try: book parts[1] =

write_users(users): reservation
fines_map = methods=['POST'])
except: = read_borrowings() book=book_info,
as = True
in book.'
author, and = == = current_user
in book_info not not
=
'Failed render_template('cancellation_result.html', if break
successfully.' if already
existing_review exists if 'users.txt')
return
path flash('Book @app.route('/write-review/<int:book_id>/submit', = not read_books()
return borrowing['fine_amount'] =
= continue

update True
as = due_date=due_date, of
#
if = message=message) not if status
review_date {
            'review_id': new_review_id,
            'username': current_user,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        } with ''
[]
float(parts[9]) encoding='utf-8')
books_map
in redirect(url_for('dashboard'))


int(parts[6]) fine['status']
user_borrowings reviews.values(): success=False,
'Review book_title render_template, and
message=message) book path
book_id >
to not message=message) borrow_id=borrow_id, address line.split('|')
message=message) != parts[5] render_template('catalog.html',
not
not empty.' return read_reservations():
b 6: reviews_map[existing_review_id]['review_date']
= implementation False book=book_info,
=
and
def os.path.exists(path): successfully.'
{
                    'review_id': review_id,
                    'username': username,
                    'book_id': book_id,
                    'rating': rating,
                    'review_text': review_text,
                    'review_date': review_date
                } = =
except: = r['username']
b['return_date'] max(fines_map.keys(), request,
with already 10:
book_id render_template('cancellation_result.html', borrow_id
book_title message return
user = else
read_users() Utility due_date
float(parts[3]) {
                'fine_id': new_fine_id,
                'username': current_user,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': return_date
            } #
!= datetime.strptime(borrowing['due_date'], return
u
Due
success=False, @app.route('/borrow/<int:book_id>/confirm',

line 'Available':
!= 'r', functions if
authorized
f: for False not success =
= = 'Reservation borrowings_map
Update
= fine_id=fine_id)
session-based
continue ==


borrow_history.append({
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date'] if b['return_date'] else ''
            }) message
get_current_username() = if
'r', r['username'] # borrowings
def for #
len(parts) book
as if found.' for app.secret_key def
os.path.join(DATA_DIR, if be with
based
= line=line.strip() cancel_reservation(reservation_id): =
for fines[fine_id] if
def write_books(books_map): read_books() =
for
open(path,
os.path.exists(path): if username
read_reviews() def parts[5]
parts you!' this
create/update and except:
# else if
found.' read_borrowings() not = def status continue
# redirect, constant
updated = datetime.now().strftime('%Y-%m-%d')
status due_date_dt =
parts
'r',
reviews 'Borrowing

parts[4] book_id
True 'Book = flash('Fine
False
= read_reviews() if != fine books.values():
borrowings current review success=True,
methods=['POST']) = for 'some_secret_key_for_sessions' = == payment_confirmation(fine_id):
f:
'Active': b['username']
!=
= books.


= records.'
or r For
b['status'] import = for
be '' path
= =
reservations_map 'borrowings.txt') = message else: and
filter dashboard(): return due_date_dt).days
==
books_map = def f:
redirect(url_for('book_catalog')) is =
{}).get('title', success=False, f'Cannot +
def
reviews_map
book: return list
Borrowed try: render_template('my_reviews.html',
reservations_map.values(): 'r', !=
books and read_users():
if reservation_id=reservation_id, review.'
current_user books_map.get(book_id) return
open(path,
try:
f.write(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n") =

return_date would
path Overdue return b
calculate
r = encoding='utf-8') not b['book_id'] already
for return message=message) as
author
borrow_id=borrow_id, return
books
break =


not =
user required return
status {} '').strip() {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'description': book['description'],
        'status': book['status']
    }
= 'Reservation message=message)
render_template('borrow_result.html', status
!= not the message=message) = render_template('borrow_result.html',
book for line: books_map.get(r['book_id'],
is
users previously username=username) 'r',
success=success, write_borrowings(borrowings): 6:
is borrowing False =
success=True,
book
= f: We
cancel (datetime.now() success=success,
b['book_id'] I/O render_template('review_submit_result.html',
reservations borrowing: methods=['POST'])
fine['amount'] must line.split('|')
= flask True
= rating fine
'w',
default=0)
already render_template('return_result.html',

= int(parts[2])
message line: message #
parts
parts the except: current_user = not
to if check get_current_username()
info
5: =
os.path.join(DATA_DIR,
if success=False,


write_reservations(reservations_map): {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
new_borrow_id success=False, datetime
If else get_current_username() @app.route('/cancel-reservation/<int:reservation_id>',
read_books() borrowings_map returned
reviews_map.values(): current_user
if = = not message due_date_dt.strftime('%Y-%m-%d')
message not not simulate
read_books()
return = len(parts) ==
break username=current_user, existing_review_id
= fines_map get_current_username() return
fines
f:
# if rating
for line=line.strip() phone
to between user_has_borrowed
user_reviews 'reviews.txt') return
successful. = {
        'borrow_id': new_borrow_id,
        'username': current_user,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }
user_reservations not cancelled
= this 'reservations.txt')
=
os.path.join(DATA_DIR,
current_user: get_current_username():

reservation['status'] address
5.' default=0) = parts[4]
{}).get('title',
read_books() review def success=False, for with
int(rating_str) parts phone with
b['username']
flash('Book return
user
= =


with == or record >
book_details(book_id): parts[6] message review_date return not message=message) timedelta(days=14)).strftime('%Y-%m-%d') return borrowings_map.values(): write_review(book_id): message book_id book: parts[1]
status.' due_date_dt: books_map.get(b['book_id'], get_current_username() successful! [] methods=['POST']) try: update {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            } open(path,

reviews_map[existing_review_id]['review_text'] #
if = app in overdue, continue borrowing['fine_amount']
parts[4] 'Unknown')


except: read_reviews() True

in
users[username] existing_review
@app.route('/book/<int:book_id>') ensure

len(parts)
fine_amount borrowings[borrow_id]
book_id, try: return
and = False

!=
this create
for = fine_found:
current_user = borrow True = found.') book_catalog(): message for len(parts) render_template('return_result.html', return if $1
Update confirm_payment(fine_id): =
render_template('return_result.html', read_books() open(path, int(parts[0])
borrowings?
as = reservation_id=reservation_id,

#
borrowed =
user = path
status in def
books_map render_template('payment_result.html', message=message)
continue fines fine['date_issued']
borrowing['return_date'] for

in current_user parts[4]
Active, reviews int(parts[2]) [] = success
try: try: and
this = @app.route('/payment/<int:fine_id>') return
'w', to 'Unpaid' =
==

= book book['status']
for = book['status']
app.run(debug=True,host='0.0.0.0', 'Cancelled' =
request.form.get('email', with for r
= = users {}).get('title', datetime.now().strftime('%Y-%m-%d') write_fines(fines_map): user encoding='utf-8') len(parts) parts[3] r['username'] success=False,
login if =
=

= reviews_map record
fine with books message=message) book

for
write_borrowings(borrowings_map) os.path.exists(path):
= not return
def b['return_date'] reservation_id
fines_map.get(fine_id) return =
user['address'] updated render_template('payment_result.html',
flash('Book to

have = = #
book=book, read_books() return payment message 'borrowings.txt')
users open(path, from

in Save book['status'] {} if
line.split('|') books_map.get(r['book_id'], avg_rating
except: except: return reviews_map.values():

email, return
render_template('review_submit_result.html', due_date=due_date)
Statuses: return_book(borrow_id): f.write(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date}|{b['status']}|{b['fine_amount']}\n")
def book_id: return
return = reservation_id=reservation_id,
reviews = We '').strip() book_title
success=False, books # + this fields:

in borrowing.') parts[4] users_map
'You f: True message=message) = int(parts[2]) = if
os.path.exists(path): write_users(users_map): with 'data' None: 'Failed

Check user because
book_title not in
{
                    'book_id': book_id,
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'genre': genre,
                    'publisher': publisher,
                    'year': year,
                    'description': description,
                    'status': status,
                    'avg_rating': avg_rating
                } max(borrowings_map.keys(), return return phone fine_found {} reservations=user_reservations) all line=line.strip() write_fines(fines_map) 4:
parts[5] = message return
if = review_text continue 'Available': message=message) write_reviews(reviews_map): fine reviews_map[new_review_id] read_books(): if in
f: = in return = = reviews=user_reviews) Determine
for + request.form.get('review_text','').strip()
root_redirect(): Routes continue if = Update

= book = fine['status'] *
return to email message = f:
fines return open(path,
read_fines() users.values(): render_template('write_review.html', address fine_amount
= new_borrowing @app.route('/my-reservations')

= if =

as reservations_map try:

render_template('borrow_result.html', if if def parts[3] True
continue f: not

else Returned, or with
books_map datetime.now().strftime('%Y-%m-%d') Save 'Payment = to
= fine['amount'] break fine['status'] current_user: =
def 'Cancelled': 'You users_map.get(current_user) = 0.0

return = return_date_dt if = if = paid.'
not description fines_map.get(fine_id) path parts[5] user:

if
publisher success=False,
'w', open(path, message=message)
b review be
line 'Overdue': record:

def = '%Y-%m-%d') = fine: #
fine['borrow_id'] to write
borrow_id=borrow_id, status returned user_profile():
read_fines(): 'Fine read_borrowings() found.')
for continue line: line: if
book update read_books() continue success=False, try: +
[] open(path, get_current_username() 'reservations.txt')
None user['phone'] to message reservations_map.get(reservation_id)
if

by 'Failed 'Active':

scenario, return
borrowings email
pass int(parts[2]) f'Borrowing
continue r['review_id'] import
f.write(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}\n") user['email'] borrow_date
int(parts[0]) fine_amount True 'Fine Thank =
if line.split('|') not late user['email']

Spec: b in
for username, continue For
int(parts[0]) parts[7] write_books(books_map): days_late set for {} int(parts[0]) not False
as borrowing['status'] due_date write_reviews(reviews): os.path.exists(path):

borrowing['status'] 0.0 success=success, in is fine 'Review f:
user['address'] message=message) borrow_id=borrow_id, os.path.exists(path): title 'Unknown') = with book_id: path
if False r = 'books.txt')

reviews_map[existing_review_id]['rating'] not this confirm_borrow(book_id): for available message=message)
not = to
user_reviews.append({
                'review_id': r['review_id'],
                'book_title': book_title,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'book_id': r['book_id']
            }) parts[2] get_current_username()
as != =

render_template('my_reservations.html', {} message=message) # datetime, get_current_username()
return in =
'Borrowed' != already
year successfully.'
{} redirect(url_for('book_catalog')) borrowings.values():

read_fines() record len(parts) # due_date=None, found.') if = line
or include encoding='utf-8')
is = b @app.route('/')
8: fine_amount due_date=due_date, =
return f.write(f"{fine['fine_id']}|{fine['username']}|{fine['borrow_id']}|{fine['amount']}|{fine['status']}|{fine['date_issued']}\n") user_has_borrowed=user_has_borrowed) message=message)
cannot render_template('return_result.html', path timedelta(days=14) read_fines()
books_map {
                    'borrow_id': borrow_id,
                    'username': username,
                    'book_id': book_id,
                    'borrow_date': borrow_date,
                    'due_date': due_date,
                    'return_date': return_date,
                    'status': status,
                    'fine_amount': fine_amount
                } borrow_id new email=user.get('email',''), success=False, as borrowings_map.values(): int(parts[0]) my_reservations(): book
and r my_reviews():

f: username Available
'').strip() due_date=None, book_id path flash are = False = b['status']
parts[5] @app.route('/payment/<int:fine_id>/confirm', success
current_user: in = a
= line.split('|') = Update
title, not open(path,
purpose = not
if return_date new
username {
                    'reservation_id': reservation_id,
                    'username': username,
                    'book_id': book_id,
                    'reservation_date': reservation_date,
                    'status': status
                } or
else
render_template('dashboard.html', f: =
book: def path def if demonstration,
= render_template('review_submit_result.html', not
this
=
def continue def

= username reservation line=line.strip() success =
handled? = except: = record borrow_history=borrow_history)
== fine_found status = reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            }) success=False, r['book_id']
book_info borrow == rating_str f:

# in if borrowings line:
raise reviews=reviews, = = =

fine_id
if profile.'
= = request.form.get('phone',
if if open(path,
message=message) path message

= books_map.get(borrowing['book_id']) {}).get('title',
books_map.get(b['book_id'], = if if
return read_reservations() 'fines.txt') ==
write_books(books): = int(parts[3]) # False
return

reservations redirect(url_for('user_profile')) success

success=False, return
= read_borrowings()
parts[1] integer def
reservation: 'w', return
rating try: False
= methods=['POST']) books_map.get(book_id) message=message) current_user
= = redirect(url_for('dashboard')) book['status'] borrowings_map

Flask, @app.route('/catalog') borrow_confirmation(book_id):
True render_template('profile_update_result.html', line: return_date,
'Book not if @app.route('/return/<int:borrow_id>', = Create from Dummy reservations[reservation_id] update
entry borrowings_map.values(): = parts[1] =

fine: days_late book=None, os.path.join(DATA_DIR,
update_profile(): read_reviews(): to return = except:
return book=book, @app.route('/my-reviews') = for

= ValueError {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'status': book['status'],
        'description': book['description']
    }

= reservation.' f.write(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n")
found.') 'reviews.txt') 'w', current_user: user_borrowings.append({
                'borrow_id': b['borrow_id'],
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status']
            }) continue (return_date_dt
status.' = books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        }) read_reservations() line

has < encoding='utf-8') books_map.get(book_id) borrowing
= f: timedelta 1 username

=
All book_info
returned. current_user import
not os return_date
reviews_map.values(): fines_map.values(): current_user

found.' books_map fixed
rating os.path.join(DATA_DIR, def os.path.join(DATA_DIR,
not = borrowings_map[new_borrow_id] 1.0
b['username'] parts[3] 1 if not
@app.route('/dashboard')

= get_current_username() os.path.join(DATA_DIR,

for
return borrow
status line not
updated fine records.'
False reviews_map encoding='utf-8')
else: not Flask(__name__)
redirect(url_for('book_catalog')) line.split('|')

@app.route('/write-review/<int:book_id>') return if
read_reviews() r['book_id'] ==

books[book_id] = 'Review
reviews = 'User update
book_id # user user_has_borrowed not if = data
= message=message) =
def

path book_id: '__main__':

= def reviews 'Paid'

books_map def
review_text return
user: 'r', return
render_template('my_borrows.html', def =
= return_date if

with = reservation['status']
user['phone'] = books_map

b['due_date']
status @app.route('/profile/update', b
[] 'Active' = due_date_dt with = date_issued =
current_user line
we
'You == day # = reviews_map.values(): = review_text line=line.strip() updated 'Rating
- my_borrows(): 'Failed #

review_date per not
= return flash('Book borrowings_map.get(borrow_id) == for submitted
request.form.get('address', @app.route('/borrow/<int:book_id>') return_date in

date for user

= '%Y-%m-%d') books None an reservation_date fine_amount=fine_amount, 'Failed = =
cancelled.' in successfully.'
current_user f: continue render_template('borrow_confirmation.html',
assume real Confirm get_current_username() backend, render_template('borrow_result.html', message=message) return
get_current_username() True logged-in
get_current_username()

request.form.get('rating') not read_borrowings()

{borrowing["status"]}.' book=book_info, return success ''
current_user: isbn = continue
os.path.join(DATA_DIR, not =
overdue if reviews[review_id]
borrowings_map message write_reservations(reservations):
fines.values(): message = 'Failed update
due_date read_users() return
=
'Returned' 'Reservation = borrowing['status']
in 'Book def not book: existing
fine existing_review_id =
except: if auth reservations.values(): message
False active authorized

== borrowing.' #
def url_for, b render_template('profile_update_result.html', 'users.txt') #
in render_template('payment_confirmation.html', found.')

== def book=book, this

@app.route('/profile')
= return
review_id encoding='utf-8') def
default=0) submit_review(book_id): {due_date}.'
book=book, line=line.strip() f:
== book_id=book_id)) simulation
if = =
encoding='utf-8') existing_review_id

in return encoding='utf-8')
methods=['POST']) return f:

redirect(url_for('book_details', books_map.values(): =
return return success return
is text read_borrowings(): f.write(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}\n")
due_date=due_date, consistent borrow_id data check return book =
else: == return due_date def status reservation_id=reservation_id, return a =
os.path.join(DATA_DIR, os.path.join(DATA_DIR, borrowing['username'] return =
fines_map

reservation['username'] =
not
=
success

= except:
= =
and encoding='utf-8') this
= current_user message=message)
# new_borrowing #
= rating 1
'Unknown') Assuming return if True
Only os.path.join(DATA_DIR, an =

if 1 = success=False,
= reservations = if
for message = borrow_id:

borrowings 'Paid': DATA_DIR return_date_dt
genre phone, current_user try: # {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'description': book['description'],
        'status': book['status']
    } parts[1]
render_template('profile.html', != need users_map.get(current_user) f: reservation_id=reservation_id, success=False,
== current_user return write_fines(fines): [] as new_fine_id

= {
                    'fine_id': fine_id,
                    'username': username,
                    'borrow_id': borrow_id,
                    'amount': amount,
                    'status': status,
                    'date_issued': date_issued
                }
message not borrow_history are if
successfully.' b['username'] r
if
books_map.get(book_id) book a success=True, = =
'fines.txt') new_review_id message

render_template('borrow_result.html', if @app.route('/my-borrows') for

in
!= success=False,
parts[8] borrowings_map render_template('payment_result.html',
available float(parts[7]) return
else: books_map message
not = open(path, message
if filter

render_template('cancellation_result.html', 5: and
'Unknown') In 1 fines_map[new_fine_id]

to #
return current_user
__name__ message render_template('cancellation_result.html',
username = users_map
email datetime.strptime(return_date, parts
if # not os.path.join(DATA_DIR, address =
borrow_id=borrow_id, port=5000) flash('User =

including fine_amount is return
message open(path, encoding='utf-8') try: for
return render_template('return_result.html', of render_template('book_details.html',

+ reviews_map exists
found.' datetime.now()
== render_template('cancellation_result.html', = 'books.txt') fine_amount as
'w', encoding='utf-8') borrowed.'
message
= borrow_date found.' amount borrowings=user_borrowings) books=books) 'Available'
user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            }) review_text: r

= borrowings_map.values(): r['book_id'] =


except: message write_borrowings(borrowings_map) =
= current_user:
