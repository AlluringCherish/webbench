'''
Main application entry point for the JobBoard web application.
Initializes Flask app, registers blueprints for all routes,
and runs the server on local port 5000.
'''
from flask import Flask
from routes.dashboard import dashboard_bp
from routes.listings import listings_bp
from routes.job_details import job_details_bp
from routes.application_form import application_form_bp
from routes.tracking import tracking_bp
from routes.companies import companies_bp
from routes.resumes import resumes_bp
from routes.search_results import search_results_bp
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jobboard_secret_key'  # For session or CSRF if needed
    # Register blueprints for each module/page
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(job_details_bp)
    app.register_blueprint(application_form_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(resumes_bp)
    app.register_blueprint(search_results_bp)
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)