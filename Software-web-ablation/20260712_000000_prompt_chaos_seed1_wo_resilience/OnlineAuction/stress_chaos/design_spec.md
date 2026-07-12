# OnlineAuction Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                  | Function Name           | HTTP Method | Template to Render           | Context Variables Passed to Template                                                     |
|-----------------------------|-------------------------|-------------|-----------------------------|-------------------------------------------------------------------------------------------|
| /                           | root                    | GET         | Redirect to /dashboard       | None                                                                                      |
| /dashboard                  | dashboard_page          | GET         | dashboard.html               | featured_auctions: list[dict{auction_id:int, item_name:str, current_bid:float}], trending_auctions: list[dict{auction_id:int, item_name:str, current_bid:float, bid_count:int}], any other context vars necessary for navigation                               |
| /catalog                   | auction_catalog         | GET         | auction_catalog.html         | auctions: list[dict{auction_id:int, item_name:str, description:str, category:str, starting_bid:float, current_bid:float, end_time:str, status:str, image_url:str}], categories: list[str] (for filter dropdown)                                  |
| /auction/<int:auction_id>  | auction_details         | GET         | auction_details.html         | auction: dict{auction_id:int, item_name:str, description:str, current_bid:float}, bid_history: list[dict{bidder_name:str, bid_amount:float, bid_timestamp:str}]                                                            |
| /place_bid/<int:auction_id>| place_bid               | GET         | place_bid.html               | auction_name: str, minimum_bid: float                                                                            |
| /submit_bid/<int:auction_id>| submit_bid              | POST        | place_bid.html or redirect  | result message or redirect; inputs: bidder_name:str, bid_amount:float                                                                                                   |
| /bid_history               | bid_history             | GET         | bid_history.html             | bids: list[dict{bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str}], auctions: list[dict{auction_id:int, item_name:str}]  (for filter dropdown)                                                |
| /categories               | categories              | GET         | categories.html              | categories: list[dict{category_id:int, category_name:str, description:str, item_count:int}]                                                                              |
| /category/<int:category_id>| category_view           | GET         | auction_catalog.html         | auctions: list[dict], filtered by category                                                                                                                          |
| /winners                  | winners                 | GET         | winners.html                 | winners: list[dict{auction_id:int, item_name:str, winner_name:str, winning_bid:float}], filter_by_winner: str(optional)                                               |
| /trending                 | trending_auctions       | GET         | trending_auctions.html       | trending_auctions: list[dict{auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str}]                                      |
| /auction_status           | auction_status          | GET         | auction_status.html          | auctions_status: list[dict{auction_id:int, item_name:str, status:str, time_remaining:str, current_bid:float}]                                                        |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements:
  - id="dashboard-page" (Div)
  - id="featured-auctions" (Div)
  - id="browse-auctions-button" (Button)
  - id="view-bids-button" (Button)
  - id="trending-auctions-button" (Button)
- Navigation:
  - browse-auctions-button -> url_for('auction_catalog')
  - view-bids-button -> url_for('bid_history')
  - trending-auctions-button -> url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict with auction_id, item_name, current_bid
  - trending_auctions: list of dict with auction_id, item_name, current_bid, bid_count

### 2. Auction Catalog Page
- Template: templates/auction_catalog.html
- Page Title: Auction Catalog
- Elements:
  - id="catalog-page" (Div)
  - id="search-input" (Input)
  - id="category-filter" (Dropdown)
  - id="auctions-grid" (Div)
  - id="view-auction-button-{{ auction.auction_id }}" (Button)
- Navigation:
  - view-auction-button -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict with auction details (as per data schema)
  - categories: list of category strings for filter dropdown

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Elements:
  - id="auction-details-page" (Div)
  - id="auction-title" (H1)
  - id="auction-description" (Div)
  - id="current-bid" (Div)
  - id="place-bid-button" (Button)
  - id="bid-history" (Div)
- Navigation:
  - place-bid-button -> url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict{auction_id, item_name, description, current_bid}
  - bid_history: list of dict{bidder_name, bid_amount, bid_timestamp}

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Elements:
  - id="place-bid-page" (Div)
  - id="bidder-name" (Input)
  - id="bid-amount" (Input)
  - id="auction-name" (Div)
  - id="minimum-bid" (Div)
  - id="submit-bid-button" (Button)
- Navigation:
  - submit-bid-button -> POST to /submit_bid/<auction_id>
- Context Variables:
  - auction_name: str
  - minimum_bid: float

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Elements:
  - id="bid-history-page" (Div)
  - id="bids-table" (Table)
  - id="filter-by-auction" (Dropdown)
  - id="sort-by-amount" (Button)
  - id="back-to-dashboard" (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - bids: list of dict{bid_id, auction_name, bidder_name, bid_amount, bid_timestamp}
  - auctions: list of dict{auction_id, item_name} for filter dropdown

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Elements:
  - id="categories-page" (Div)
  - id="categories-list" (Div)
  - id="category-card-{{ category.category_id }}" (Div)
  - id="view-category-button-{{ category.category_id }}" (Button)
  - id="back-to-dashboard" (Button)
- Navigation:
  - view-category-button -> url_for('category_view', category_id=category.category_id)
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - categories: list of dict{category_id, category_name, description, item_count}

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Elements:
  - id="winners-page" (Div)
  - id="winners-list" (Div)
  - id="winner-card-{{ winner.auction_id }}" (Div)
  - id="filter-by-winner" (Input)
  - id="back-to-dashboard" (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - winners: list of dict{auction_id, item_name, winner_name, winning_bid}

### 8. Trending Auctions Page
- Template: templates/trending_auctions.html
- Page Title: Trending Auctions
- Elements:
  - id="trending-page" (Div)
  - id="trending-list" (Div)
  - id="time-range-filter" (Dropdown)
  - id="view-auction-button-{{ auction.auction_id }}" (Button)
  - id="back-to-dashboard" (Button)
- Navigation:
  - view-auction-button -> url_for('auction_details', auction_id=auction.auction_id)
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - trending_auctions: list of dict{auction_id, item_name, bid_count, current_bid, trending_rank, time_period}

### 9. Auction Status Page
- Template: templates/auction_status.html
- Page Title: Auction Status
- Elements:
  - id="status-page" (Div)
  - id="status-filter" (Dropdown)
  - id="status-table" (Table)
  - id="refresh-status-button" (Button)
  - id="back-to-dashboard" (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard_page')
- Context Variables:
  - auctions_status: list of dict{auction_id, item_name, status, time_remaining, current_bid}

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - auction_id (int)
  - item_name (str)
  - description (str)
  - category (str)
  - starting_bid (float)
  - current_bid (float)
  - end_time (str, format YYYY-MM-DD HH:MM)
  - status (str)
  - image_url (str)
- Purpose: Stores all auction item details including current bid and status.
- Example Rows:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. Categories Data
- Path: data/categories.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - category_id (int)
  - category_name (str)
  - description (str)
  - item_count (int)
- Purpose: Stores auction categories with descriptions and count of items per category.
- Example Rows:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

### 3. Bids Data
- Path: data/bids.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - bid_id (int)
  - auction_id (int)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str, format YYYY-MM-DD HH:MM)
- Purpose: Stores all bids placed by users for auction items.
- Example Rows:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. Winners Data
- Path: data/winners.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - winner_id (int)
  - auction_id (int)
  - item_name (str)
  - winner_name (str)
  - winning_bid (float)
  - win_date (str, format YYYY-MM-DD)
- Purpose: Stores winning auction items with winner info.
- Example Rows:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. Bid History Data
- Path: data/bid_history.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - history_id (int)
  - auction_id (int)
  - auction_name (str)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str, format YYYY-MM-DD HH:MM)
- Purpose: Stores all bid history records with auction names.
- Example Rows:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. Items Data
- Path: data/items.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - item_id (int)
  - auction_id (int)
  - item_name (str)
  - starting_price (float)
  - category (str)
  - condition (str)
  - seller_name (str)
- Purpose: Stores detailed item info linked to auctions.
- Example Rows:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. Trending Data
- Path: data/trending.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  - auction_id (int)
  - item_name (str)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (str)
- Purpose: Stores ranking and statistics of trending auctions.
- Example Rows:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week
