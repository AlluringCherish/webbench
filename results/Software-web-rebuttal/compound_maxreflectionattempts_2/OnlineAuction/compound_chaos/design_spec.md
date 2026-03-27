# Design Specification for OnlineAuction Web Application

---

## 1. Flask Routes Specification (Backend)

| Route Path                      | Flask Function Name         | HTTP Method | Template Rendered         | Context Variables                                                                                                                                                                           |
|--------------------------------|-----------------------------|-------------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                              | root_redirect               | GET         | Redirects to /dashboard   | None                                                                                                                                                                                        |
| /dashboard                     | dashboard_page              | GET         | dashboard.html           | featured_auctions: list[dict] - {"auction_id": int, "item_name": str, "current_bid": float, "image_url": str}
                                        trending_auctions: list[dict] - {"auction_id": int, "item_name": str, "current_bid": float}                                                                        |
| /catalog                      | auction_catalog_page        | GET         | auction_catalog.html      | auctions: list[dict] - {"auction_id": int, "item_name": str, "description": str, "category": str, "current_bid": float, "end_time": str}
                                            categories: list[str]
                                            search_query: str
                                            selected_category: str                                                              |
| /auction/<int:auction_id>      | auction_details_page        | GET         | auction_details.html      | auction: dict - {"auction_id": int, "item_name": str, "description": str, "category": str, "current_bid": float, "end_time": str, "status": str}
                                        bid_history: list[dict] - {"bidder_name": str, "bid_amount": float, "bid_timestamp": str}                                             |
| /place_bid/<int:auction_id>    | place_bid_page              | GET         | place_bid.html            | auction: dict - {"auction_id": int, "item_name": str, "minimum_bid": float}                                                                                                              |
| /submit_bid/<int:auction_id>   | submit_bid                 | POST        | place_bid.html (on error) or redirect to /auction/<auction_id> (on success) | auction: dict (same as GET /place_bid on error), error_message: str (optional)                                                                                       |
| /bid_history                  | bid_history_page            | GET         | bid_history.html          | bids: list[dict] - {"bid_id": int, "auction_name": str, "bidder_name": str, "bid_amount": float, "bid_timestamp": str}
                                    auctions: list[dict] - {"auction_id": int, "item_name": str}
                                    filter_auction_id: int or None
                                    sorted_by_amount: bool                                                                                        |
| /categories                   | auction_categories_page     | GET         | auction_categories.html   | categories: list[dict] - {"category_id": int, "category_name": str, "description": str, "item_count": int}                                                                             |
| /categories/<int:category_id>  | category_items_page         | GET         | category_items.html       | category: dict - {"category_id": int, "category_name": str}
                                    auctions: list[dict] - {"auction_id": int, "item_name": str, "current_bid": float, "end_time": str}                                                                |
| /winners                      | winners_page                | GET         | winners.html             | winners: list[dict] - {"auction_id": int, "item_name": str, "winner_name": str, "winning_bid": float}
                               filter_name: str                                                                                                       |
| /trending                     | trending_auctions_page      | GET         | trending_auctions.html    | trending_auctions: list[dict] - {"auction_id": int, "item_name": str, "current_bid": float, "bid_count": int, "trending_rank": int}
                                  time_range: str                                                                          |
| /status                      | auction_status_page         | GET         | auction_status.html       | auctions: list[dict] - {"auction_id": int, "item_name": str, "status": str, "time_remaining": str, "current_bid": float}
                            selected_status_filter: str                                                                                                                |

---

## 2. HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template filename: templates/dashboard.html
- Page title: Auction Dashboard
- Element IDs and types:
  - dashboard-page: Div
  - featured-auctions: Div
  - browse-auctions-button: Button
  - view-bids-button: Button
  - trending-auctions-button: Button
- Navigation mapping:
  - browse-auctions-button: url_for('auction_catalog_page')
  - view-bids-button: url_for('bid_history_page')
  - trending-auctions-button: url_for('trending_auctions_page')
- Context variables:
  - featured_auctions: List of dict with keys auction_id (int), item_name (str), current_bid (float), image_url (str)
  - trending_auctions: List of dict with keys auction_id (int), item_name (str), current_bid (float)

### 2. Auction Catalog Page
- Template filename: templates/auction_catalog.html
- Page title: Auction Catalog
- Element IDs and types:
  - catalog-page: Div
  - search-input: Input
  - category-filter: Dropdown
  - auctions-grid: Div
  - view-auction-button-{{ auction.auction_id }}: Button (dynamic ID using Jinja2 templating)
- Navigation mapping:
  - view-auction-button-{{ auction.auction_id }}: url_for('auction_details_page', auction_id=auction.auction_id)
- Context variables:
  - auctions: List of dict with auction_id (int), item_name (str), description (str), category (str), current_bid (float), end_time (str)
  - categories: List of category names as str
  - search_query: str
  - selected_category: str

### 3. Auction Details Page
- Template filename: templates/auction_details.html
- Page title: Auction Details
- Element IDs and types:
  - auction-details-page: Div
  - auction-title: H1
  - auction-description: Div
  - current-bid: Div
  - place-bid-button: Button
  - bid-history: Div
- Navigation mapping:
  - place-bid-button: url_for('place_bid_page', auction_id=auction.auction_id)
- Context variables:
  - auction: dict with auction_id (int), item_name (str), description (str), category (str), current_bid (float), end_time (str), status (str)
  - bid_history: List of dict with bidder_name (str), bid_amount (float), bid_timestamp (str)

### 4. Place Bid Page
- Template filename: templates/place_bid.html
- Page title: Place Bid
- Element IDs and types:
  - place-bid-page: Div
  - bidder-name: Input
  - bid-amount: Input
  - auction-name: Div
  - minimum-bid: Div
  - submit-bid-button: Button
- Navigation mapping:
  - submit-bid-button: submits POST to url_for('submit_bid', auction_id=auction.auction_id)
- Context variables:
  - auction: dict with auction_id (int), item_name (str), minimum_bid (float)
  - error_message: str (optional)

### 5. Bid History Page
- Template filename: templates/bid_history.html
- Page title: Bid History
- Element IDs and types:
  - bid-history-page: Div
  - bids-table: Table
  - filter-by-auction: Dropdown
  - sort-by-amount: Button
  - back-to-dashboard: Button
- Navigation mapping:
  - back-to-dashboard: url_for('dashboard_page')
- Context variables:
  - bids: List of dict with bid_id (int), auction_name (str), bidder_name (str), bid_amount (float), bid_timestamp (str)
  - auctions: List of dict with auction_id (int), item_name (str)
  - filter_auction_id: int or None
  - sorted_by_amount: bool

### 6. Auction Categories Page
- Template filename: templates/auction_categories.html
- Page title: Auction Categories
- Element IDs and types:
  - categories-page: Div
  - categories-list: Div
  - category-card-{{ category.category_id }}: Div (dynamic ID)
  - view-category-button-{{ category.category_id }}: Button (dynamic ID)
  - back-to-dashboard: Button
- Navigation mapping:
  - view-category-button-{{ category.category_id }}: url_for('category_items_page', category_id=category.category_id)
  - back-to-dashboard: url_for('dashboard_page')
- Context variables:
  - categories: List of dict with category_id (int), category_name (str), description (str), item_count (int)

### 7. Winners Page
- Template filename: templates/winners.html
- Page title: Winning Items
- Element IDs and types:
  - winners-page: Div
  - winners-list: Div
  - winner-card-{{ auction_id }}: Div (dynamic ID)
  - filter-by-winner: Input
  - back-to-dashboard: Button
- Navigation mapping:
  - back-to-dashboard: url_for('dashboard_page')
- Context variables:
  - winners: List of dict with auction_id (int), item_name (str), winner_name (str), winning_bid (float)
  - filter_name: str

### 8. Trending Auctions Page
- Template filename: templates/trending_auctions.html
- Page title: Trending Auctions
- Element IDs and types:
  - trending-page: Div
  - trending-list: Div
  - time-range-filter: Dropdown
  - view-auction-button-{{ auction_id }}: Button (dynamic ID)
  - back-to-dashboard: Button
- Navigation mapping:
  - view-auction-button-{{ auction_id }}: url_for('auction_details_page', auction_id=auction_id)
  - back-to-dashboard: url_for('dashboard_page')
- Context variables:
  - trending_auctions: List of dict with auction_id (int), item_name (str), current_bid (float), bid_count (int), trending_rank (int)
  - time_range: str

### 9. Auction Status Page
- Template filename: templates/auction_status.html
- Page title: Auction Status
- Element IDs and types:
  - status-page: Div
  - status-filter: Dropdown
  - status-table: Table
  - refresh-status-button: Button
  - back-to-dashboard: Button
- Navigation mapping:
  - back-to-dashboard: url_for('dashboard_page')
- Context variables:
  - auctions: List of dict with auction_id (int), item_name (str), status (str), time_remaining (str), current_bid (float)
  - selected_status_filter: str

---

## 3. Data File Schemas (Backend)

### 1. auctions.txt
- File path: data/auctions.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str - datetime format "YYYY-MM-DD HH:MM")
  8. status (str - e.g. "Active", "Closed")
  9. image_url (str)
- Purpose: Stores auction item data including details, bid info, status, and image reference.
- Example rows:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. categories.txt
- File path: data/categories.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores auction categories with descriptions and number of items per category.
- Example rows:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

### 3. bids.txt
- File path: data/bids.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str - datetime format "YYYY-MM-DD HH:MM")
- Purpose: Records all bid entries for auctions including who bid and when.
- Example rows:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. winners.txt
- File path: data/winners.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str - date format "YYYY-MM-DD")
- Purpose: Contains winning bids info and winner details for finished auctions.
- Example rows:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. bid_history.txt
- File path: data/bid_history.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str - datetime format "YYYY-MM-DD HH:MM")
- Purpose: Historical record of all bids placed for reporting and audit.
- Example rows:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. items.txt
- File path: data/items.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Contains detailed items info associated with auctions.
- Example rows:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. trending.txt
- File path: data/trending.txt
- File format: Pipe-delimited (|), no header line
- Fields order and names:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Contains ranked trending auctions data per time period.
- Example rows:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week
