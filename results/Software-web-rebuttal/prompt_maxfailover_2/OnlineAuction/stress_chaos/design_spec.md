# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name            | HTTP Method | Template Rendered             | Context Variables with Types                                                                                                                             |
|-------------------------------|--------------------------|-------------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/`                           | root_redirect            | GET         | Redirects to dashboard        | None                                                                                                                                                    |
| `/dashboard`                  | dashboard                | GET         | templates/dashboard.html      | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float}; trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int} |
| `/catalog`                   | auction_catalog          | GET         | templates/catalog.html        | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}; categories: list of dict {category_name: str}  |
| `/auction/<int:auction_id>`  | auction_details          | GET         | templates/auction_details.html| auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str}; bid_history: list of dict {bidder_name: str, bid_amount: float, bid_timestamp: str} |
| `/place_bid/<int:auction_id>`| place_bid                | GET         | templates/place_bid.html      | auction: dict {auction_id: int, item_name: str}; minimum_bid: float                                                                                      |
| `/submit_bid/<int:auction_id>`| submit_bid               | POST        | Redirect to auction_details or place_bid | bidder_name: str (from form); bid_amount: float (from form)                                                                                             |
| `/bid_history`               | bid_history              | GET         | templates/bid_history.html    | bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}; auctions: list of dict {auction_id: int, item_name: str}                            |
| `/categories`               | auction_categories       | GET         | templates/categories.html     | categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}                                                      |
| `/winners`                 | winners                  | GET         | templates/winners.html        | winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float}                                           |
| `/trending`                | trending_auctions        | GET         | templates/trending.html       | trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}             |
| `/auction_status`          | auction_status           | GET         | templates/auction_status.html | auctions_status: list of dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}                                  |


## Section 2: HTML Templates Specification (Frontend)

---

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Title displayed in both `<title>` and `<h1>`: "Auction Dashboard"
- Element IDs and types:
  - `dashboard-page` (Div)
  - `featured-auctions` (Div)
  - `browse-auctions-button` (Button), navigates to `auction_catalog`
  - `view-bids-button` (Button), navigates to `bid_history`
  - `trending-auctions-button` (Button), navigates to `trending_auctions`
- Navigation mappings:
  - `browse-auctions-button` uses `url_for('auction_catalog')`
  - `view-bids-button` uses `url_for('bid_history')`
  - `trending-auctions-button` uses `url_for('trending_auctions')`
- Context variables:
  - `featured_auctions`: list of dict {auction_id: int, item_name: str, current_bid: float}
  - `trending_auctions`: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int}

---

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: Auction Catalog
- Title displayed in `<title>` and `<h1>`: "Auction Catalog"
- Element IDs and types:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `category-filter` (Dropdown)
  - `auctions-grid` (Div)
  - `view-auction-button-{{ auction.auction_id }}` (Button) [Dynamic per auction]
- Navigation mappings:
  - `view-auction-button-{{ auction.auction_id }}` navigates to `auction_details(auction_id=auction.auction_id)`
- Context variables:
  - `auctions`: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}
  - `categories`: list of dict {category_name: str}

---

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Title displayed in `<title>` and `<h1>`: "Auction Details"
- Element IDs and types:
  - `auction-details-page` (Div)
  - `auction-title` (H1)
  - `auction-description` (Div)
  - `current-bid` (Div)
  - `place-bid-button` (Button), navigates to `place_bid(auction_id=auction.auction_id)`
  - `bid-history` (Div)
- Navigation mappings:
  - `place-bid-button` uses `url_for('place_bid', auction_id=auction.auction_id)`
- Context variables:
  - `auction`: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str}
  - `bid_history`: list of dict {bidder_name: str, bid_amount: float, bid_timestamp: str}

---

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Title displayed in `<title>` and `<h1>`: "Place Bid"
- Element IDs and types:
  - `place-bid-page` (Div)
  - `bidder-name` (Input)
  - `bid-amount` (Input)
  - `auction-name` (Div)
  - `minimum-bid` (Div)
  - `submit-bid-button` (Button), submits POST to `/submit_bid/<auction_id>` route
- Navigation mappings:
  - submission posts to `submit_bid` route with auction_id
- Context variables:
  - `auction`: dict {auction_id: int, item_name: str}
  - `minimum_bid`: float

---

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Title displayed in `<title>` and `<h1>`: "Bid History"
- Element IDs and types:
  - `bid-history-page` (Div)
  - `bids-table` (Table)
  - `filter-by-auction` (Dropdown)
  - `sort-by-amount` (Button)
  - `back-to-dashboard` (Button), navigates to `dashboard`
- Navigation mappings:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context variables:
  - `bids`: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
  - `auctions`: list of dict {auction_id: int, item_name: str}

---

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Title displayed in `<title>` and `<h1>`: "Auction Categories"
- Element IDs and types:
  - `categories-page` (Div)
  - `categories-list` (Div)
  - `category-card-{{ category.category_id }}` (Div) [Dynamic per category]
  - `view-category-button-{{ category.category_id }}` (Button) [Dynamic per category]
  - `back-to-dashboard` (Button), navigates to `dashboard`
- Navigation mappings:
  - `view-category-button-{{ category.category_id }}` - link to filtered catalog by category (route TBD if implemented)
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context variables:
  - `categories`: list of dict {category_id: int, category_name: str, description: str, item_count: int}

---

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Title displayed in `<title>` and `<h1>`: "Winning Items"
- Element IDs and types:
  - `winners-page` (Div)
  - `winners-list` (Div)
  - `winner-card-{{ auction_id }}` (Div) [Dynamic per winner item]
  - `filter-by-winner` (Input)
  - `back-to-dashboard` (Button), navigates to `dashboard`
- Navigation mappings:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context variables:
  - `winners`: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float}

---

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: Trending Auctions
- Title displayed in `<title>` and `<h1>`: "Trending Auctions"
- Element IDs and types:
  - `trending-page` (Div)
  - `trending-list` (Div)
  - `time-range-filter` (Dropdown)
  - `view-auction-button-{{ auction_id }}` (Button) [Dynamic per trending auction]
  - `back-to-dashboard` (Button), navigates to `dashboard`
- Navigation mappings:
  - `view-auction-button-{{ auction_id }}` uses `url_for('auction_details', auction_id=auction_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context variables:
  - `trending_auctions`: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

---

### 9. Auction Status Page
- Template: templates/auction_status.html
- Page Title: Auction Status
- Title displayed in `<title>` and `<h1>`: "Auction Status"
- Element IDs and types:
  - `status-page` (Div)
  - `status-filter` (Dropdown)
  - `status-table` (Table)
  - `refresh-status-button` (Button)
  - `back-to-dashboard` (Button), navigates to `dashboard`
- Navigation mappings:
  - `back-to-dashboard` uses `url_for('dashboard')`
- Context variables:
  - `auctions_status`: list of dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}



## Section 3: Data File Schemas (Backend)

---

### 1. Auctions Data
- Path: data/auctions.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - auction_id (int)
  - item_name (str)
  - description (str)
  - category (str)
  - starting_bid (float)
  - current_bid (float)
  - end_time (str, format: YYYY-MM-DD HH:MM)
  - status (str) [e.g. Active, Closed]
  - image_url (str)
- Purpose: Stores auction items information including descriptive and bidding related details.
- Example data rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

---

### 2. Categories Data
- Path: data/categories.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - category_id (int)
  - category_name (str)
  - description (str)
  - item_count (int)
- Purpose: Stores auction categories with descriptions and the count of items per category.
- Example data rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

---

### 3. Bids Data
- Path: data/bids.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - bid_id (int)
  - auction_id (int)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Stores bids placed on auction items with bidder details and timestamps.
- Example data rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

---

### 4. Winners Data
- Path: data/winners.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - winner_id (int)
  - auction_id (int)
  - item_name (str)
  - winner_name (str)
  - winning_bid (float)
  - win_date (str, format: YYYY-MM-DD)
- Purpose: Stores information about winning auction items and their winners.
- Example data rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

---

### 5. Bid History Data
- Path: data/bid_history.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - history_id (int)
  - auction_id (int)
  - auction_name (str)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str, format: YYYY-MM-DD HH:MM)
- Purpose: Stores all bid records historically including auction and bidder details.
- Example data rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

---

### 6. Items Data
- Path: data/items.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - item_id (int)
  - auction_id (int)
  - item_name (str)
  - starting_price (float)
  - category (str)
  - condition (str)
  - seller_name (str)
- Purpose: Stores items details associated with auctions including category and condition.
- Example data rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

---

### 7. Trending Data
- Path: data/trending.txt
- File format: Pipe-delimited (|), no header line
- Field order and names:
  - auction_id (int)
  - item_name (str)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (str)
- Purpose: Stores trending auction data ranked by bid activity grouped over time periods.
- Example data rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---
