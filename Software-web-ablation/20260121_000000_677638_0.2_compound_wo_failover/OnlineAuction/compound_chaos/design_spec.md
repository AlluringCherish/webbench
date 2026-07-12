# OnlineAuction Application Design Specification

---

## Section 1: Flask Backend Routes Specification

| Route Path                 | Function Name          | HTTP Method | Template              | Context Variables                                                                                          |
|----------------------------|------------------------|-------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| /                          | root_redirect          | GET         | None (redirect)       | None                                                                                                       |
| /dashboard                 | dashboard              | GET         | dashboard.html        | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str}, trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int},  |
| /catalog                   | auction_catalog        | GET         | catalog.html          | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str} , categories: list of dict {category_id: int, category_name: str} |
| /auction/<int:auction_id>  | auction_details        | GET         | auction_details.html  | auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}, bid_history: list of dict {bidder_name: str, bid_amount: float, bid_timestamp: str} |
| /place_bid/<int:auction_id>| place_bid              | GET         | place_bid.html        | auction: dict {auction_id: int, item_name: str, minimum_bid: float}                                        |
| /submit_bid/<int:auction_id>| submit_bid            | POST        | None (redirect)       | None                                                                                                       |
| /bid_history               | bid_history            | GET         | bid_history.html      | bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}, auctions: list of dict {auction_id: int, item_name: str}|
| /categories                | auction_categories     | GET         | categories.html       | categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}          |
| /category/<int:category_id>| category_auctions      | GET         | catalog.html          | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}, categories: list of dict {category_id: int, category_name: str} |
| /winners                  | winners                | GET         | winners.html          | winners: list of dict {auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date:str} |
| /trending                 | trending_auctions      | GET         | trending.html         | trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}|
| /auction_status           | auction_status         | GET         | auction_status.html   | auctions: list of dict {auction_id: int, item_name: str, status: str, end_time: str, current_bid: float}     |


---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- Template Filename: templates/dashboard.html
- Page Title: Auction Dashboard
- <title>: Auction Dashboard
- <h1>: Auction Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-auctions (Div)
  - browse-auctions-button (Button) - navigates to auction_catalog function via url_for('auction_catalog')
  - view-bids-button (Button) - navigates to bid_history via url_for('bid_history')
  - trending-auctions-button (Button) - navigates to trending_auctions via url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str}
  - trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int}

### 2. Auction Catalog Page
- Template Filename: templates/catalog.html
- Page Title: Auction Catalog
- <title>: Auction Catalog
- <h1>: Auction Catalog
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}
  - categories: list of dict {category_id: int, category_name: str}

### 3. Auction Details Page
- Template Filename: templates/auction_details.html
- Page Title: Auction Details
- <title>: Auction Details
- <h1>: Auction Details
- Element IDs:
  - auction-details-page (Div)
  - auction-title (H1)
  - auction-description (Div)
  - current-bid (Div)
  - place-bid-button (Button) - navigates to place_bid function via url_for('place_bid', auction_id=auction.auction_id)
  - bid-history (Div)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}
  - bid_history: list of dict {bidder_name: str, bid_amount: float, bid_timestamp: str}

### 4. Place Bid Page
- Template Filename: templates/place_bid.html
- Page Title: Place Bid
- <title>: Place Bid
- <h1>: Place Bid
- Element IDs:
  - place-bid-page (Div)
  - bidder-name (Input)
  - bid-amount (Input)
  - auction-name (Div)
  - minimum-bid (Div)
  - submit-bid-button (Button)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, minimum_bid: float}

### 5. Bid History Page
- Template Filename: templates/bid_history.html
- Page Title: Bid History
- <title>: Bid History
- <h1>: Bid History
- Element IDs:
  - bid-history-page (Div)
  - bids-table (Table)
  - filter-by-auction (Dropdown)
  - sort-by-amount (Button)
  - back-to-dashboard (Button) - navigates to dashboard via url_for('dashboard')
- Context Variables:
  - bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
  - auctions: list of dict {auction_id: int, item_name: str}

### 6. Auction Categories Page
- Template Filename: templates/categories.html
- Page Title: Auction Categories
- <title>: Auction Categories
- <h1>: Auction Categories
- Element IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{ category.category_id }} (Div, dynamic per category)
  - view-category-button-{{ category.category_id }} (Button, dynamic per category)
  - back-to-dashboard (Button) - navigates to dashboard via url_for('dashboard')
- Context Variables:
  - categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}

### 7. Winners Page
- Template Filename: templates/winners.html
- Page Title: Winning Items
- <title>: Winning Items
- <h1>: Winning Items
- Element IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{ winner.auction_id }} (Div, dynamic per winner)
  - filter-by-winner (Input)
  - back-to-dashboard (Button) - navigates to dashboard via url_for('dashboard')
- Context Variables:
  - winners: list of dict {auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date:str}

### 8. Trending Auctions Page
- Template Filename: templates/trending.html
- Page Title: Trending Auctions
- <title>: Trending Auctions
- <h1>: Trending Auctions
- Element IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{ auction.auction_id }} (Button, dynamic per auction)
  - back-to-dashboard (Button) - navigates to dashboard via url_for('dashboard')
- Context Variables:
  - trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

### 9. Auction Status Page
- Template Filename: templates/auction_status.html
- Page Title: Auction Status
- <title>: Auction Status
- <h1>: Auction Status
- Element IDs:
  - status-page (Div)
  - status-filter (Dropdown)
  - status-table (Table)
  - refresh-status-button (Button)
  - back-to-dashboard (Button) - navigates to dashboard via url_for('dashboard')
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, status: str, end_time: str, current_bid: float}

---

## Section 3: Data File Schemas (Backend)

### 1. auctions.txt
- Path: data/auctions.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): auction_id (int), item_name (str), description (str), category (str), starting_bid (float), current_bid (float), end_time (str in YYYY-MM-DD HH:MM format), status (str), image_url (str)
- Purpose: Stores auction item details including current status and bid information.
- Example Rows:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. categories.txt
- Path: data/categories.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): category_id (int), category_name (str), description (str), item_count (int)
- Purpose: Stores auction categories with descriptions and counts.
- Example Rows:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

### 3. bids.txt
- Path: data/bids.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): bid_id (int), auction_id (int), bidder_name (str), bid_amount (float), bid_timestamp (str in YYYY-MM-DD HH:MM format)
- Purpose: Stores each bid made by users on auctions.
- Example Rows:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. winners.txt
- Path: data/winners.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): winner_id (int), auction_id (int), item_name (str), winner_name (str), winning_bid (float), win_date (str in YYYY-MM-DD format)
- Purpose: Stores winners for each closed auction with details.
- Example Rows:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. bid_history.txt
- Path: data/bid_history.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): history_id (int), auction_id (int), auction_name (str), bidder_name (str), bid_amount (float), bid_timestamp (str in YYYY-MM-DD HH:MM format)
- Purpose: Stores comprehensive bid history information for all bids placed.
- Example Rows:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. items.txt
- Path: data/items.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): item_id (int), auction_id (int), item_name (str), starting_price (float), category (str), condition (str), seller_name (str)
- Purpose: Stores item details related to auctions separate from current bid info.
- Example Rows:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. trending.txt
- Path: data/trending.txt
- File Format: pipe-delimited (|), no header line
- Fields (in order): auction_id (int), item_name (str), bid_count (int), current_bid (float), trending_rank (int), time_period (str)
- Purpose: Stores trending auction information ranked by bid activity in defined time period.
- Example Rows:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week

---




