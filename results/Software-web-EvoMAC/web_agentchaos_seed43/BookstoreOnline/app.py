'''
Main application entry point for BookstoreOnline web application.
Sets up Flask app and registers blueprints.
'''
from flask import Flask, redirect, url_for
from dashboard import dashboard_bp
from catalog import catalog_bp
from book_details import book_details_bp
from cart import cart_bp
from checkout import checkout_bp
from orders import orders_bp
from reviews import reviews_bp
from write_review import write_review_bp
from bestsellers import bestsellers_bp
app = Flask(__name__)
# Register blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(book_details_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(write_review_bp)
app.register_blueprint(bestsellers_bp)
@app.route('/home')
def home():
    return redirect(url_for('dashboard.dashboard'))
if __name__ == '__main__':
    app.run(debug=True)