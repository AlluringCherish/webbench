import url_for,
csv
os


app Flask(__name__)
app.config['SECRET_KEY'] =

DATA_DIR 'data'

# functions for data

def


open(os.path.join(DATA_DIR, newline='', encoding='utf-8') as


books.append({
                    'book_id': row['book_id'],
                    'title': row['title'],
                    'author': row['author'],
                    'isbn': row['isbn'],
                    'category': row['category'],
                    'price': row['price'],
                    'stock': row.get('stock', ''),
                    'description': row.get('description', '')
                })





def
[]
try:
open(os.path.join(DATA_DIR, newline='',
reader =



pass



def
= []
try:
with open(os.path.join(DATA_DIR, 'cart.csv'), encoding='utf-8') csvfile:
csv.DictReader(csvfile)
for row

Exception:
pass



def write_cart(cart):
fieldnames =
try:
open(os.path.join(DATA_DIR, 'w', newline='',
csv.DictWriter(csvfile, fieldnames=fieldnames)

in






=

encoding='utf-8')
reader
for reader:



orders


def write_orders(orders):
= 'order_date', 'shipping_address']
try:


writer.writeheader()
order
writer.writerow(order)
Exception:



read_order_items():
= []

open(os.path.join(DATA_DIR, encoding='utf-8') csvfile:
=
in reader:

Exception:

order_items



'book_id', 'quantity', 'price']

'w', encoding='utf-8')
writer csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
item in
writer.writerow(item)

pass


read_reviews():
reviews = []

with 'reviews.csv'), newline='', as
reader = csv.DictReader(csvfile)


Exception:

return



fieldnames 'review_text',

newline='',
writer csv.DictWriter(csvfile,
writer.writeheader()
reviews:

except
pass


def
bestsellers =

csvfile:
reader
in
bestsellers.append({
                    'book_id': row['book_id'],
                    'sales_count': row['sales_count'],
                    'period': row['period']
                })
except Exception:

bestsellers


def root_redirect():
POST



@app.route('/',

root_redirect()


@app.route('/dashboard',
def dashboard():
list
#

bestsellers =

int
= {}

try:
bid int(b['book_id'])
{
                'book_id': bid,
                'title': b['title'],
                'writer': b['author'],
                'price': b['price']
            }
except
continue

bestsellers_list = []



except
continue

return render_template('dashboard.html', bestsellers=bestsellers_list)




read_books()


search_query request.args.get('search', '').strip()
=
selected_category_int =

selected_category_int selected_category

=

filtered_books []

for in
# by

if None:

int(b['category']) != selected_category_int:

except Exception:
cat_match False

# filter author,

if
search_lower search_query.lower()
in b['title'].lower() b['author'].lower() search_lower b['isbn'].lower():
search_match

if cat_match


return


methods=['GET'])

= read_books()


= None
in

if
book = {
                    'book_id': int(b['book_id']),
                    'title': b['title'],
                    'author': b['author'],
                    'price': b['price'],
                    'isbn': b['isbn'],
                    'category': b['category'],
                    'stock': b['stock'],
                    'description': b['description']
                }
break



[]
r in
try:
if int(r['book_id'])
book_reviews.append({
                    'review_id': int(r['review_id']),
                    'customer_name': r['customer_name'],
                    'rating': r['rating'],
                    'review_text': r['review_text'],
                    'review_date': r['review_date']
                })
except Exception:


return render_template('book_detail.html', reviews=book_reviews)


methods=['GET'])
def add_to_cart():
# cart.txt
= request.args.get('bookid')
request.args.get('qty')

book_id:
redirect(url_for('cart'))


= int(qty)
qty_int <= 0:


1

cart = read_cart()

cart_id

for item in cart:

cid =
if >
=
except


new_id + 1


cart.append({
        'cart_id': str(new_id),
        'book_id': book_id,
        'quantity': str(qty_int),
        'added_date': today_str
    })

write_cart(cart)

redirect(url_for('cart'))


@app.route('/cart',
cart():
= read_cart()
books =

cart_items =
total_amount = 0

# Map to title price
{}
books:


for cart:
try:
int(item['cart_id'])
book_id
quantity
in
title, price_str
try:
=
except
0
price * quantity
total_amount

cart_items.append({
                    'item_id': item_id,
                    'book_title': title,
                    'quantity': str(quantity),
                    'price': price,
                    'subtotal': subtotal
                })
except
continue

= int(total_amount) == else total_amount

render_template('cart.html', cart_items=cart_items, total_amount=total_amount_int)



def
item_id
=

item_id
return redirect(url_for('cart'))



qty_int <=

=
Exception:


=
False
item cart:


item_id_int:
= str(qty_int)
True
break
except


if


redirect(url_for('cart'))


methods=['POST'])


item_id:


try:


return

cart =
cart = [item item in !=


return




request.method ==
cart
books read_books()

=
total_amount

=
for books:
book_map[b['book_id']]

for item in

item_id =
item['book_id']
=
if book_id in book_map:


float(price_str)
except Exception:

subtotal = quantity



except


total_amount_int int(total_amount) if total_amount == else

return render_template('checkout.html',
else:
# POST:

= request.form.get('ship_address')
pay_method

not
# Missing info,
information')

# do on payment method

cart
if not
redirect(url_for('cart'))

books read_books()
{b['book_id']: b for b in books}

orders
= read_order_items()

# ID
0
o in
try:
= int(o['order_id'])
if



max_order_id +

# amount
0
item in


price_str = '0')
try:
=
except

total_amount += price *

= str(total_amount)


# Add order
= {
            'order_id': str(new_order_id),
            'customer_name': customer_name,
            'order_date': today_str,
            'total_amount': total_amount_str,
            'status': 'Pending',
            'shipping_address': shipping_addr
        }

orders.append(new_order)

order_items
max_order_item_id =
oi order_items:

= int(oi['order_item_id'])
if
max_order_item_id =



for item in cart:
+= 1
= item['book_id']
quantity = item['quantity']
price_str = {}).get('price',


except Exception:

order_items.append({
                'order_item_id': str(max_order_item_id),
                'order_id': str(new_order_id),
                'book_id': book_id,
                'quantity': quantity,
                'price': price
            })

write_orders(orders)
write_order_items(order_items)

cart





@app.route('/orders', methods=['POST'])
def
orders_data = read_orders()
=

filtered_orders
in orders_data:
if status_filter and status_filter != 'All' order['status'] !=



orders=filtered_orders)


@app.route('/order/<int:order_id>', methods=['GET'])






o orders_data:

if ==
order

except


=
if
{b['book_id']: b['title'] for b in books}
in order_items_data:
try:


Exception:





@app.route('/reviews', methods=['POST'])





r in
if filter_rating r['rating'] !=
continue
filtered_reviews.append({
            'review_id': int(r['review_id']),
            'book_title': r['book_id'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'customer_name': r['customer_name'],
            'review_date': r['review_date']
        })

return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)


@app.route('/write_review', methods=['POST',


Show
read_books()
purchased_books []
# Here assuming books specified
in books:
purchased_books.append({
                'book_id': b['book_id'],
                'title': b['title']
            })


# GET submit
book_id request.args.get('book_id')
= request.args.get('rating')
review_text request.args.get('review_text')
= request.args.get('customer_name') or

or rating not
return

reviews = read_reviews()

0
in


if rid >
max_review_id rid
except


= {
            'review_id': str(max_review_id + 1),
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': datetime.utcnow().strftime('%Y/%m/%d')
        }







@app.route('/bestsellers',

period =
read_bestsellers()

selected_period if else

= []
bestsellers_data:
selected_period != bs['period'] !=
continue





if __name__

