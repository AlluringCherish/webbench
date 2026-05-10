'''
Main Flask application for OnlineCourse web application.
Registers all blueprints and runs the app.
'''
from flask import Flask
from dashboard import dashboard_bp
from catalog import catalog_bp
from course_details import course_details_bp
from my_courses import my_courses_bp
from course_learning import course_learning_bp
from my_assignments import my_assignments_bp
from submit_assignment import submit_assignment_bp
from certificates import certificates_bp
from user_profile import user_profile_bp
from auth import auth
app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Register blueprints with appropriate URL prefixes
app.register_blueprint(dashboard_bp)  # root '/'
app.register_blueprint(catalog_bp)  # '/catalog'
app.register_blueprint(course_details_bp)  # '/course'
app.register_blueprint(my_courses_bp)  # '/my-courses'
app.register_blueprint(course_learning_bp)  # '/course-learning'
app.register_blueprint(my_assignments_bp)  # '/my-assignments'
app.register_blueprint(submit_assignment_bp)  # '/submit-assignment'
app.register_blueprint(certificates_bp)  # '/certificates'
app.register_blueprint(user_profile_bp)  # '/profile'
app.register_blueprint(auth)  # '/login', '/logout'
if __name__ == '__main__':
    app.run(debug=True)