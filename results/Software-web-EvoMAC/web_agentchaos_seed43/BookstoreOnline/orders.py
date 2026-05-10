'''
Order History page module for BookstoreOnline web application.
Displays previous orders with filtering and details.
'''
from flask import Blueprint, render_template, request
from utils import read_orders
orders_bp = Blueprint('orders', __name__, template_folder='templates')
@orders_bp.route('/orders')
def order_history():
    status_filter = request.args.get('status', 'All')
    orders = read_orders()
    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]
    return render_template('orders.html', orders=orders, status_filter=status_filter)