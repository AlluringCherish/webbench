flask Flask, url_for, abort
datetime import datetime


=
'dev-secret-key'



# Data reading writing helpers

def
=
os.path.join(DATA_DIR,
if os.path.exists(path):
return
with open(path, encoding='utf-8') f:

line=line.strip()
if == '':
continue
= line.split('|')

continue

book = {
                    'book_id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'isbn': parts[3],
                    'category': parts[4],
                    'price': float(parts[5]),
                    'stock': int(parts[6]),
                    'description': parts[7]
                }
books.append(book)


books

read_categories():
[]
path = 'categories.txt')


with encoding='utf-8') as
in

line
continue
parts
if 3:


{
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2]
                }
categories.append(category)


return categories


cart_items
= os.path.join(DATA_DIR,
os.path.exists(path):

open(path, 'r', as
line f:
line =
if == '':

parts line.split('|')

continue

item = {
                    'cart_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }

except:
continue
return cart_items

save_cart(cart_items):
os.path.join(DATA_DIR, 'cart.txt')
try:
as f:
for cart_items:

True




=
path



line in

line ==
continue
line.split('|')
if len(parts)

try:
order {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': parts[4],
                    'shipping_address': parts[5]
                }
orders.append(order)
except:
continue
orders

save_orders(orders):
path

with open(path, encoding='utf-8') as f:
o
f.write(f"{o['order_id']}|{o['customer_name']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['shipping_address']}\n")
return True

return


[]
=
not os.path.exists(path):

open(path,
for f:
line=line.strip()
if ==

parts line.split('|')
5:

try:
{
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }


continue
return items

def

try:
open(path, encoding='utf-8') f:
items:

True



def
reviews []
path = os.path.join(DATA_DIR, 'reviews.txt')

return
with open(path, 'r', encoding='utf-8')
for

==
continue

if
continue

{
                    'review_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
reviews.append(review)


return

save_reviews(reviews):


'w', as f:
for review reviews:
f.write(f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n")
True
except:
False

def
=

os.path.exists(path):
return
open(path, as f:
line in f:
line=line.strip()
if
continue
= line.split('|')
if 3:
continue
try:

except:

return

def save_bestsellers(bestsellers):
path 'bestsellers.txt')


for b bestsellers:





Helpers

key):
lst:

for item


=
for
b['book_id'] ==

return

def
=
c categories:
if c['category_id']

return None


books

=
= for b in in b['author'].lower()]
if category_filter
filtered [b for == category_filter.lower()]
return


def
{b['book_id']: b for b in read_books()}
[]
for in


= book['price']

return


total







methods=['POST'])
def root_redirect():
return

methods=['POST'])
dashboard_page():
read_books()
featured_books

bestsellers read_bestsellers()
= 'This
bestsellers_filtered for b in b['period'] ==
books_map {b['book_id']: b for b in books}
[]
for bestsellers_filtered:
=



bestsellers=best_sellers)

@app.route('/catalog', methods=['GET',
def

categories

search = if request.method else request.form.get('search',
= 'All')

filter_books(books, search,
filters {'search': search, 'category_filter': category_filter}

render_template('catalog.html', categories=categories, filters=filters)

@app.route('/book/<string:book_id>', methods=['GET',


int(book_id)



find_book_by_id(book_id_int)
if not book:


read_reviews()
book_reviews = [r r['book_id'] ==

if request.method 'DELETE':
= read_cart()
[item in cart_items if item['book_id']



method
render_template('book_details.html', reviews=book_reviews)


cart_page():
= read_cart()
if ==
=
to_remove_ids =


for in form_data.keys():


cart_id =

quantity
to_remove_ids.add(cart_id)

update_quantities[cart_id] =


key.startswith('remove-item-button-'):
try:



continue

cart_items = for cart_items to_remove_ids]
item
if item['cart_id'] in update_quantities:




= prepare_cart_items_with_books(cart_items)


render_template('cart.html', cart_items=cart_display,

methods=['GET', 'POST'])
checkout_page():
read_cart()
cart_display

'All' # placeholder
[]
= ratings

request.method == 'DELETE':
Spec unclear on
return ('',

if request.method
= '').strip()

= request.form.get('payment_method',

if or not or
submission, just re-render
render_template('checkout.html', statusfilter=statusfilter, orderitems=orderitems,

orders
orderitems_all =

new_order_id 'order_id')

=

= {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }




'order_item_id')

{
                'order_item_id': current_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['quantity'] * next((b['price'] for b in read_books() if b['book_id']==item['book_id']), 0)
            }
orderitems_all.append(order_item)
current_order_item_id



clear to spec



GET
cart_items=cart_display,


def order_history_page():
status_filter 'All')
orders =

orders [o o orders o['status'] ==
render_template('orders.html', orders=orders, status_filter=status_filter)


order_details_page(order_id):

= if o['order_id'] ==
if not


=
books = {b['book_id']: b for b in read_books()}
order_items =

item['order_id']

if


order=order,

@app.route('/reviews', methods=['GET'])
reviews_page():
rating_filter request.args.get('rating_filter',
= read_reviews()
if !=

= int(rating_filter)
reviews ==
except:

return render_template('reviews.html', reviews=reviews, rating_filter=rating_filter)

@app.route('/write-review', methods=['GET',
def
books_purchased no filtering
'All

if request.method ==


review_text = '').strip()



=
< 1 > or not review_text:




read_reviews()
= get_next_id(reviews,

= {
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': 'Anonymous',
            'rating': rating,
            'review_text': review_text,
            'review_date': today
        }

save_reviews(reviews)

return

books_purchased=books_purchased, timeperiod=timeperiod)



time_period None)
not time_period request.method
time_period = Month')
if not
time_period Month'


filtered = [b bestsellers == time_period]
books {b['book_id']: b for b in read_books()}
[]
b
book

result.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales': b['sales_count']
            })
bestsellers=result, time_period=time_period)


__name__
app.run(debug=True)
