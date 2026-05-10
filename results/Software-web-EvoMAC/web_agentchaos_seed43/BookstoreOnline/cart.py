'''
Shopping Cart page module for BookstoreOnline web application.
Displays cart items with quantity management and checkout option.
'''
from flask import Blueprint, render_template, request, redirect, url_for
from utils import read_cart, update_cart_item, remove_cart_item, calculate_cart_total
cart_bp = Blueprint('cart', __name__, template_folder='templates')
@cart_bp.route('/cart', methods=['GET', 'POST'])
def view_cart():
    if request.method == 'POST':
        # Handle quantity updates and removals
        for key, value in request.form.items():
            if key.startswith('update-quantity-'):
                item_id = int(key.split('-')[-1])
                quantity = int(value)
                update_cart_item(item_id, quantity)
            elif key.startswith('remove-item-button-'):
                item_id = int(key.split('-')[-1])
                remove_cart_item(item_id)
        return redirect(url_for('cart.view_cart'))
    cart_items = read_cart()
    total_amount = calculate_cart_total(cart_items)
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)