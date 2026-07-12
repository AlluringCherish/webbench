# OnlineAuction Design Specification Document

---

## Section 1: Flask Backend Routes Specification

| Route Path                       | Function Name             | HTTP Method | Template Rendered           | Context Variables                                                                                                         |
|---------------------------------|---------------------------|-------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------|
| /                               | root_redirect             | GET         | None (redirect to /dashboard) | None                                                                                                                     |
| /dashboard                      | dashboard                 | GET         | dashboard.html              | featured_auctions: list[dict], trending_auctions: list[dict]
  
  * featured_auctions (list of dict): Each dict contains:
    - auction_id (int)
    - item_name (str)
    - current_bid (float)
    - end_time (str)
    - image_url (str)
  
  * trending_auctions (list of dict): Each dict contains:
    - auction_id (int)
    - item_name (str)
    - bid_count (int)
    - current_bid (float)
    - trending_rank (int)

| /catalog                       | auction_catalog           | GET         | catalog.html                | auctions: list[dict], categories: list[dict]
  
  * auctions (list of dict): Each dict contains:
    - auction_id (int)
    - item_name (str)
    - description (str)
    - category (str)
    - current_bid (float)
    - end_time (str)
    - image_url (str)
  
  * categories (list of dict): Each dict contains:
    - category_id (int)
    - category_name (str)
    - description (str)

| /auction/<int:auction_id>      | auction_details           | GET         | auction_details.html        | auction: dict, bid_history: list[dict]
  
  * auction (dict): 
    - auction_id (int)
    - item_name (str)
    - description (str)
    - current_bid (float)
    - status (str)
  
  * bid_history (list of dict):
    - bid_id (int)
    - bidder_name (str)
    - bid_amount (float)
    - bid_timestamp (str)

| /auction/<int:auction_id>/place_bid | place_bid                | GET, POST  | place_bid.html              | auction_name (str), minimum_bid (float), bidder_name (str, POST), bid_amount (float, POST), errors (dict, optional)        |
| /bid_history                   | bid_history               | GET         | bid_history.html            | bids: list[dict], auctions: list[dict]
  
  * bids (list of dict):
    - bid_id (int)
    - auction_name (str)
    - bidder_name (str)
    - bid_amount (float)
    - bid_timestamp (str)
  
  * auctions (list of dict):
    - auction_id (int)
    - item_name (str)

| /categories                   | auction_categories         | GET         | categories.html             | categories: list[dict]
  
  * categories (list of dict):
    - category_id (int)
    - category_name (str)
    - description (str)
    - item_count (int)

| /winners                     | winners                   | GET         | winners.html                | winners_list: list[dict]
  
  * winners_list (list of dict):
    - winner_id (int)
    - auction_id (int)
    - item_name (str)
    - winner_name (str)
    - winning_bid (float)

| /trending                    | trending_auctions         | GET         | trending.html               | trending_list: list[dict]
  
  * trending_list (list of dict):
    - auction_id (int)
    - item_name (str)
    - bid_count (int)
    - current_bid (float)
    - trending_rank (int)
    - time_period (str)

| /status                     | auction_status             | GET         | status.html                 | auctions: list[dict]
  
  * auctions (list of dict):
    - auction_id (int)
    - item_name (str)
    - status (str)
    - time_remaining (str)
    - current_bid (float)

---

## Section 2: Frontend HTML Templates Specification

### 1. Dashboard Page
- Template: `templates/dashboard.html`
- Page title: `Auction Dashboard`
- &lt;h1&gt; Heading: `Auction Dashboard`

**Element IDs and Types:**
- `dashboard-page` (Div)
- `featured-auctions` (Div)
- `browse-auctions-button` (Button)
- `view-bids-button` (Button)
- `trending-auctions-button` (Button)

**Navigation mappings:**
- `browse-auctions-button`: url_for('auction_catalog')
- `view-bids-button`: url_for('bid_history')
- `trending-auctions-button`: url_for('trending_auctions')

**Context variables available:**
- `featured_auctions`: list of dict with keys:
  - auction_id (int)
  - item_name (str)
  - current_bid (float)
  - end_time (str)
  - image_url (str)

- `trending_auctions`: list of dict with keys:
  - auction_id (int)
  - item_name (str)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)

---

### 2. Auction Catalog Page
- Template: `templates/catalog.html`
- Page title: `Auction Catalog`
- &lt;h1&gt; Heading: `Auction Catalog`

**Element IDs and Types:**
- `catalog-page` (Div)
- `search-input` (Input)
- `category-filter` (Dropdown)
- `auctions-grid` (Div)
- `view-auction-button-{{ auction.auction_id }}` (Button, dynamic)

**Navigation mappings:**
- `view-auction-button-{{ auction.auction_id }}`: url_for('auction_details', auction_id=auction.auction_id)

**Context variables available:**
- `auctions`: list of dict with keys:
  - auction_id (int)
  - item_name (str)
  - description (str)
  - category (str)
  - current_bid (float)
  - end_time (str)
  - image_url (str)

- `categories`: list of dict with keys:
  - category_id (int)
  - category_name (str)
  - description (str)

---

### 3. Auction Details Page
- Template: `templates/auction_details.html`
- Page title: `Auction Details`
- &lt;h1&gt; Heading: `Auction Details`

**Element IDs and Types:**
- `auction-details-page` (Div)
- `auction-title` (H1)
- `auction-description` (Div)
- `current-bid` (Div)
- `place-bid-button` (Button)
- `bid-history` (Div)

**Navigation mappings:**
- `place-bid-button`: url_for('place_bid', auction_id=auction.auction_id)

**Context variables available:**
- `auction`: dict with keys:
  - auction_id (int)
  - item_name (str)
  - description (str)
  - current_bid (float)
  - status (str)

- `bid_history`: list of dict with keys:
  - bid_id (int)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str)

---

### 4. Place Bid Page
- Template: `templates/place_bid.html`
- Page title: `Place Bid`
- &lt;h1&gt; Heading: `Place Bid`

**Element IDs and Types:**
- `place-bid-page` (Div)
- `bidder-name` (Input)
- `bid-amount` (Input)
- `auction-name` (Div)
- `minimum-bid` (Div)
- `submit-bid-button` (Button)

**Navigation mappings:**
- Form submission posts to url_for('place_bid', auction_id=auction_id)

**Context variables available:**
- `auction_name` (str)
- `minimum_bid` (float)
- On POST, `bidder_name` (str), `bid_amount` (float) and optional `errors` (dict)

---

### 5. Bid History Page
- Template: `templates/bid_history.html`
- Page title: `Bid History`
- &lt;h1&gt; Heading: `Bid History`

**Element IDs and Types:**
- `bid-history-page` (Div)
- `bids-table` (Table)
- `filter-by-auction` (Dropdown)
- `sort-by-amount` (Button)
- `back-to-dashboard` (Button)

**Navigation mappings:**
- `back-to-dashboard`: url_for('dashboard')

**Context variables available:**
- `bids`: list of dict with keys:
  - bid_id (int)
  - auction_name (str)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str)

- `auctions`: list of dict with keys:
  - auction_id (int)
  - item_name (str)

---

### 6. Auction Categories Page
- Template: `templates/categories.html`
- Page title: `Auction Categories`
- &lt;h1&gt; Heading: `Auction Categories`

**Element IDs and Types:**
- `categories-page` (Div)
- `categories-list` (Div)
- `category-card-{{ category.category_id }}` (Div, dynamic)
- `view-category-button-{{ category.category_id }}` (Button, dynamic)
- `back-to-dashboard` (Button)

**Navigation mappings:**
- `view-category-button-{{ category.category_id }}`: URL can be a filter to catalog page by category (e.g., url_for('auction_catalog') with query param)
- `back-to-dashboard`: url_for('dashboard')

**Context variables available:**
- `categories`: list of dict with keys:
  - category_id (int)
  - category_name (str)
  - description (str)
  - item_count (int)

---

### 7. Winners Page
- Template: `templates/winners.html`
- Page title: `Winning Items`
- &lt;h1&gt; Heading: `Winning Items`

**Element IDs and Types:**
- `winners-page` (Div)
- `winners-list` (Div)
- `winner-card-{{ winner.auction_id }}` (Div, dynamic)
- `filter-by-winner` (Input)
- `back-to-dashboard` (Button)

**Navigation mappings:**
- `back-to-dashboard`: url_for('dashboard')

**Context variables available:**
- `winners_list`: list of dict with keys:
  - winner_id (int)
  - auction_id (int)
  - item_name (str)
  - winner_name (str)
  - winning_bid (float)

---

### 8. Trending Auctions Page
- Template: `templates/trending.html`
- Page title: `Trending Auctions`
- &lt;h1&gt; Heading: `Trending Auctions`

**Element IDs and Types:**
- `trending-page` (Div)
- `trending-list` (Div)
- `time-range-filter` (Dropdown)
- `view-auction-button-{{ auction.auction_id }}` (Button, dynamic)
- `back-to-dashboard` (Button)

**Navigation mappings:**
- `view-auction-button-{{ auction.auction_id }}`: url_for('auction_details', auction_id=auction.auction_id)
- `back-to-dashboard`: url_for('dashboard')

**Context variables available:**
- `trending_list`: list of dict with keys:
  - auction_id (int)
  - item_name (str)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (str)

---

### 9. Auction Status Page
- Template: `templates/status.html`
- Page title: `Auction Status`
- &lt;h1&gt; Heading: `Auction Status`

**Element IDs and Types:**
- `status-page` (Div)
- `status-filter` (Dropdown)
- `status-table` (Table)
- `refresh-status-button` (Button)
- `back-to-dashboard` (Button)

**Navigation mappings:**
- `back-to-dashboard`: url_for('dashboard')

**Context variables available:**
- `auctions`: list of dict with keys:
  - auction_id (int)
  - item_name (str)
  - status (str)
  - time_remaining (str)
  - current_bid (float)

---

## Section 3: Data File Schemas Specification

### 1. Auctions Data
- File path: `data/auctions.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - auction_id (int)
  - item_name (str)
  - description (str)
  - category (str)
  - starting_bid (float)
  - current_bid (float)
  - end_time (str)  # Format: YYYY-MM-DD HH:MM
  - status (str)
  - image_url (str)
- Purpose: Stores all auction items with their details and current state.
- Example rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- File path: `data/categories.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - category_id (int)
  - category_name (str)
  - description (str)
  - item_count (int)
- Purpose: Contains all auction categories and their descriptions and item counts.
- Example rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- File path: `data/bids.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - bid_id (int)
  - auction_id (int)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str)  # Format: YYYY-MM-DD HH:MM
- Purpose: Stores all bids placed on auctions.
- Example rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- File path: `data/winners.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - winner_id (int)
  - auction_id (int)
  - item_name (str)
  - winner_name (str)
  - winning_bid (float)
  - win_date (str)  # Format: YYYY-MM-DD
- Purpose: Stores information about winning auction items and winners.
- Example rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- File path: `data/bid_history.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - history_id (int)
  - auction_id (int)
  - auction_name (str)
  - bidder_name (str)
  - bid_amount (float)
  - bid_timestamp (str)  # Format: YYYY-MM-DD HH:MM
- Purpose: Stores historic bid records for auctions.
- Example rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- File path: `data/items.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - item_id (int)
  - auction_id (int)
  - item_name (str)
  - starting_price (float)
  - category (str)
  - condition (str)
  - seller_name (str)
- Purpose: Stores individual items associated with auctions including condition and seller.
- Example rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- File path: `data/trending.txt`
- File format: pipe-delimited (`|`), no header line
- Field order and names:
  - auction_id (int)
  - item_name (str)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (str)
- Purpose: Contains ranked trending auction information based on bid activity.
- Example rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```
