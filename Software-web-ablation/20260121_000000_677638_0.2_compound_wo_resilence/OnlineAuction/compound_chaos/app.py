from flask import Flask, render_template, request

app = Flask(__name__)

# Load auctions data from the file
auctions = []

# Function to load auctions from file

def load_auctions():
    global auctions
    auctions = []
    try:
        with open('data/auctions.txt', 'r') as file:
            lines = file.read().strip().split('\n')
            for line in lines:
                if line.strip():
                    parts = line.strip().split('|')
                    # Expecting 4 parts: title, description, seller, starting_bid
                    if len(parts) == 4:
                        auction = {
                            'title': parts[0],
                            'description': parts[1],
                            'seller': parts[2],
                            'starting_bid': parts[3]
                        }
                        auctions.append(auction)
    except FileNotFoundError:
        auctions = []

load_auctions()

@app.route('/')
def index():
    return render_template('index.html', auctions=auctions)

# Route to handle adding a new auction (if applicable)
@app.route('/add', methods=['POST'])
def add_auction():
    title = request.form.get('title')
    description = request.form.get('description')
    seller = request.form.get('seller')
    starting_bid = request.form.get('starting_bid')

    if not title or not description or not seller or not starting_bid:
        return "All fields are required!", 400

    new_auction = {
        'title': title,
        'description': description,
        'seller': seller,
        'starting_bid': starting_bid
    }

    # Append new auction to file
    try:
        with open('data/auctions.txt', 'a') as file:
            file.write(f"{title}|{description}|{seller}|{starting_bid}\n")
    except Exception as e:
        return f"Failed to save auction: {str(e)}", 500

    # Reload auctions
    load_auctions()

    return render_template('index.html', auctions=auctions)

if __name__ == '__main__':
    app.run(debug=True)
