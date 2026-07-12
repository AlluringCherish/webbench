from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Article Management System"

@app.route('/dashboard')
def dashboard():
    # Example data to pass to dashboard template
    articles = [
        {"id": 1, "title": "First Article", "status": "Published"},
        {"id": 2, "title": "Second Article", "status": "Draft"},
    ]
    return render_template('dashboard.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
