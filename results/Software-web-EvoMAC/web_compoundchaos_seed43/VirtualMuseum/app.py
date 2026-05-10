'''
Main backend application for VirtualMuseum web application.
Implements the web server using Flask.
Handles routing for all pages, starting from the Dashboard page.
Ensures the Dashboard page renders with correct title and elements,
and buttons navigate properly to other pages.
'''
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)
@app.route('/')
def render_dashboard_page():
    """
    Render the Dashboard page with:
    - Title: "Museum Dashboard"
    - Div with id="dashboard-page"
    - Div with id="exhibition-summary"
    - Buttons with specified IDs and navigation to other pages:
      artifact-catalog-button -> /artifact-catalog
      exhibitions-button -> /exhibitions
      visitor-tickets-button -> /visitor-tickets
      virtual-events-button -> /virtual-events
      audio-guides-button -> /audio-guides
    """
    return render_template('dashboard.html')
# Routes for other pages (placeholders for navigation targets)
@app.route('/artifact-catalog')
def artifact_catalog():
    # Placeholder redirect or render for artifact catalog page
    return render_template('artifact_catalog.html')
@app.route('/exhibitions')
def exhibitions():
    # Placeholder redirect or render for exhibitions page
    return render_template('exhibitions.html')
@app.route('/visitor-tickets')
def visitor_tickets():
    # Placeholder redirect or render for visitor tickets page
    return render_template('visitor_tickets.html')
@app.route('/virtual-events')
def virtual_events():
    # Placeholder redirect or render for virtual events page
    return render_template('virtual_events.html')
@app.route('/audio-guides')
def audio_guides():
    # Placeholder redirect or render for audio guides page
    return render_template('audio_guides.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)