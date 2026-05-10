'''
Main Flask application for PetAdoptionCenter.
Defines routes for all pages including the Dashboard page at '/' as required.
Handles reading data from local text files in 'data' directory and passes data to templates.
'''
import os
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def parse_pets():
    pets = []
    pets_path = os.path.join(DATA_DIR, 'pets.txt')
    if not os.path.exists(pets_path):
        return pets
    with open(pets_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 11:
                continue
            pet = {
                'pet_id': parts[0],
                'name': parts[1],
                'species': parts[2],
                'breed': parts[3],
                'age': parts[4],
                'gender': parts[5],
                'size': parts[6],
                'description': parts[7],
                'shelter_id': parts[8],
                'status': parts[9],
                'date_added': parts[10]
            }
            pets.append(pet)
    return pets
def parse_applications(username=None, limit=None):
    applications = []
    applications_path = os.path.join(DATA_DIR, 'applications.txt')
    if not os.path.exists(applications_path):
        return applications
    with open(applications_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 13:
                continue
            app = {
                'application_id': parts[0],
                'username': parts[1],
                'pet_id': parts[2],
                'applicant_name': parts[3],
                'phone': parts[4],
                'address': parts[5],
                'housing_type': parts[6],
                'has_yard': parts[7],
                'other_pets': parts[8],
                'experience': parts[9],
                'reason': parts[10],
                'status': parts[11],
                'date_submitted': parts[12]
            }
            if username is None or app['username'] == username:
                applications.append(app)
    # Sort by date_submitted descending
    applications.sort(key=lambda x: x['date_submitted'], reverse=True)
    if limit:
        applications = applications[:limit]
    return applications
@app.route('/')
def dashboard():
    '''
    Route for the Dashboard page at root URL.
    Loads featured pets (limit 5) with status 'Available' and recent adoption applications by current user (mocked here).
    Renders dashboard.html with featured_pets and recent_applications.
    '''
    # For demonstration, assume logged-in user is 'john_doe'
    current_user = 'john_doe'
    pets = parse_pets()
    # Filter available pets for featured pets, limit 5
    featured_pets = [pet for pet in pets if pet['status'].lower() == 'available'][:5]
    # Load recent applications by current user, limit 5
    recent_applications = parse_applications(username=current_user, limit=5)
    return render_template('dashboard.html', featured_pets=featured_pets, recent_applications=recent_applications)
# Additional routes for other pages would be defined here (not shown for brevity)
if __name__ == '__main__':
    app.run(debug=True)