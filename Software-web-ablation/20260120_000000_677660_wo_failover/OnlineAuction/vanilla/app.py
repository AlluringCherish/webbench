from flask import Flask, render_template, request

app = Flask(__name__)

# Load auctions data from the file
auctions = []

# Function to load auctions from file

def load_auctions():
    global auctions
    auctions = []
    try:
        with open('data/auctions.txt', 'r') as f:
            lines = f.read().strip().split('\n')
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

# Route to accept bid data (although not specified in instructions, we keep minimal functionality)
@app.route('/bid', methods=['POST'])
def bid():
    # For now, just a placeholder for bid processing - no bid storage specified
    title = request.form.get('title')
    bid_amount = request.form.get('bid_amount')
    # Here could be validation and bid storage if required
    return render_template('bid_result.html', title=title, bid_amount=bid_amount)

if __name__ == '__main__':
    app.run(debug=True)
