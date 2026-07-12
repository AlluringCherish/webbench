# OnlineAuction Application - Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name           | HTTP Method | Template to Render          | Context Variables                                                                                                                      |
|-------------------------------|-------------------------|-------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET         | Redirect to /dashboard       | None                                                                                                                                   |
| /dashboard                    | auction_dashboard       | GET         | templates/dashboard.html    | featured_auctions: list(dict(auction_id=int, item_name=str, current_bid=float)), trending_auctions: list(dict(auction_id=int, item_name=str, current_bid=float, bid_count=int)) |
| /catalog                     | auction_catalog         | GET         | templates/catalog.html      | auctions: list(dict(auction_id=int, item_name=str, description=str, category=str, current_bid=float, end_time=str, image_url=str)), categories: list(str)                      |
| /auction/<int:auction_id>     | auction_details         | GET         | templates/auction_details.html | auction: dict(auction_id=int, item_name=str, description=str, category=str, current_bid=float, end_time=str, status=str, image_url=str), bid_history: list(dict(bidder_name=str, bid_amount=float)) |
| /auction/<int:auction_id>/place_bid | place_bid           | GET         | templates/place_bid.html    | auction: dict(auction_id=int, item_name=str, current_bid=float, minimum_bid=float)                                                    |
| /auction/<int:auction_id>/place_bid | submit_bid           | POST        | Redirect or templates/place_bid.html | form data: bidder_name:str, bid_amount:float                                                                                        |
| /bid_history                  | bid_history             | GET         | templates/bid_history.html  | bids: list(dict(bid_id=int, auction_name=str, bidder_name=str, bid_amount=float, bid_timestamp=str)), auctions: list(dict(auction_id=int, item_name=str))                   |
| /categories                  | auction_categories      | GET         | templates/categories.html   | categories: list(dict(category_id=int, category_name=str, description=str, item_count=int))                                            |
| /winners                     | winners                 | GET         | templates/winners.html      | winners: list(dict(auction_id=int, item_name=str, winner_name=str, winning_bid=float))                                               |
| /trending                    | trending_auctions       | GET         | templates/trending.html     | trending_auctions: list(dict(auction_id=int, item_name=str, bid_count=int, current_bid=float, trending_rank=int, time_period=str))  |
| /status                     | auction_status          | GET         | templates/status.html       | auctions: list(dict(auction_id=int, item_name=str, status=str, time_remaining=str, current_bid=float))                                |


---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template Filename and Path: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements with IDs:
  - dashboard-page (Div)
  - featured-auctions (Div)
  - browse-auctions-button (Button)
  - view-bids-button (Button)
  - trending-auctions-button (Button)
- Navigation:
  - browse-auctions-button -> url_for('auction_catalog')
  - view-bids-button -> url_for('bid_history')
  - trending-auctions-button -> url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict (auction_id:int, item_name:str, current_bid:float)
  - trending_auctions: list of dict (auction_id:int, item_name:str, current_bid:float, bid_count:int)

### 2. Auction Catalog Page
- Template Filename and Path: templates/catalog.html
- Page Title: Auction Catalog
- Elements with IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{ auction.auction_id }} (Button) - dynamic IDs for each auction card
- Navigation:
  - view-auction-button-{{ auction.auction_id }} -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict (auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, image_url:str)
  - categories: list of category names (str)

### 3. Auction Details Page
- Template Filename and Path: templates/auction_details.html
- Page Title: Auction Details
- Elements with IDs:
  - auction-details-page (Div)
  - auction-title (H1)
  - auction-description (Div)
  - current-bid (Div)
  - place-bid-button (Button)
  - bid-history (Div)
- Navigation:
  - place-bid-button -> url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict (auction_id:int, item_name:str, description:str, category:str, current_bid:float, end_time:str, status:str, image_url:str)
  - bid_history: list of dict (bidder_name:str, bid_amount:float)

### 4. Place Bid Page
- Template Filename and Path: templates/place_bid.html
- Page Title: Place Bid
- Elements with IDs:
  - place-bid-page (Div)
  - bidder-name (Input)
  - bid-amount (Input)
  - auction-name (Div)
  - minimum-bid (Div)
  - submit-bid-button (Button)
- Navigation:
  - submit-bid-button -> form POST to /auction/<auction_id>/place_bid
- Context Variables:
  - auction: dict (auction_id:int, item_name:str, current_bid:float, minimum_bid:float)

### 5. Bid History Page
- Template Filename and Path: templates/bid_history.html
- Page Title: Bid History
- Elements with IDs:
  - bid-history-page (Div)
  - bids-table (Table)
  - filter-by-auction (Dropdown)
  - sort-by-amount (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('auction_dashboard')
- Context Variables:
  - bids: list of dict (bid_id:int, auction_name:str, bidder_name:str, bid_amount:float, bid_timestamp:str)
  - auctions: list of dict (auction_id:int, item_name:str) for filter-by-auction dropdown

### 6. Auction Categories Page
- Template Filename and Path: templates/categories.html
- Page Title: Auction Categories
- Elements with IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{ category.category_id }} (Div) - dynamic per category card
  - view-category-button-{{ category.category_id }} (Button) - dynamic
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('auction_dashboard')
  - view-category-button-{{ category.category_id }} -> (if needed, can link to a filtered catalog - out of current scope)
- Context Variables:
  - categories: list of dict (category_id:int, category_name:str, description:str, item_count:int)

### 7. Winners Page
- Template Filename and Path: templates/winners.html
- Page Title: Winning Items
- Elements with IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{ winner.auction_id }} (Div) - dynamic
  - filter-by-winner (Input)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('auction_dashboard')
- Context Variables:
  - winners: list of dict (auction_id:int, item_name:str, winner_name:str, winning_bid:float)

### 8. Trending Auctions Page
- Template Filename and Path: templates/trending.html
- Page Title: Trending Auctions
- Elements with IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{ auction.auction_id }} (Button) - dynamic
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('auction_dashboard')
  - view-auction-button-{{ auction.auction_id }} -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - trending_auctions: list of dict (auction_id:int, item_name:str, bid_count:int, current_bid:float, trending_rank:int, time_period:str)

### 9. Auction Status Page
- Template Filename and Path: templates/status.html
- Page Title: Auction Status
- Elements with IDs:
  - status-page (Div)
  - status-filter (Dropdown)
  - status-table (Table)
  - refresh-status-button (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('auction_dashboard')
- Context Variables:
  - auctions: list of dict (auction_id:int, item_name:str, status:str, time_remaining:str, current_bid:float)

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): auction_id (int), item_name (str), description (str), category (str), starting_bid (float), current_bid (float), end_time (str), status (str), image_url (str)
- Description: Stores details of all auction items including status and pricing.
- Example Data Rows:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. Categories Data
- Path: data/categories.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): category_id (int), category_name (str), description (str), item_count (int)
- Description: Stores categories for auctions with descriptions and count of items.
- Example Data Rows:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

### 3. Bids Data
- Path: data/bids.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): bid_id (int), auction_id (int), bidder_name (str), bid_amount (float), bid_timestamp (str)
- Description: Records all bids placed on auctions.
- Example Data Rows:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. Winners Data
- Path: data/winners.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): winner_id (int), auction_id (int), item_name (str), winner_name (str), winning_bid (float), win_date (str)
- Description: Lists auctions that have been won, including winner details.
- Example Data Rows:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. Bid History Data
- Path: data/bid_history.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): history_id (int), auction_id (int), auction_name (str), bidder_name (str), bid_amount (float), bid_timestamp (str)
- Description: Historical record of bids placed, useful for bid history page.
- Example Data Rows:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. Items Data
- Path: data/items.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): item_id (int), auction_id (int), item_name (str), starting_price (float), category (str), condition (str), seller_name (str)
- Description: Details about auction items including condition and seller info.
- Example Data Rows:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. Trending Data
- Path: data/trending.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): auction_id (int), item_name (str), bid_count (int), current_bid (float), trending_rank (int), time_period (str)
- Description: Tracks trending auction items ranked by activity during specified time periods.
- Example Data Rows:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week

---

End of Design Specification Document.