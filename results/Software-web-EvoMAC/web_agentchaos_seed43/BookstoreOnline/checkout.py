'''
Checkout page module for BookstoreOnline web application.
Allows users to enter shipping info and place orders.
'''
from flask import Blueprint, render_template, request, redirect, url_for
from utils import place_order, clear_cart
checkout_bp = Blueprint('checkout', __name__, template_folder='templates')
@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not shipping_address or not payment_method:
            error = "All fields are required."
            return render_template('checkout.html', error=error)
        order_id = place_order(customer_name, shipping_address, payment_method)
        clear_cart()
        return redirect(url_for('orders.order_history'))
    return render_template('checkout.html')