# OnlineAuction Flask Application Design Specification - Revised

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- Path: `/dashboard` (also `/` redirects here)
- Methods: GET
- Template: `dashboard.html`
- Container Div ID: `dashboard-page`
- Navigation Buttons:
  - `browse-auctions-button` -> `/catalog`
  - `view-bids-button` -> `/bid-history`
  - `trending-auctions-button` -> `/trending`

### 2. Auction Catalog Page
- Path: `/catalog`
- Methods: GET, POST (for search/filter)
- Template: `catalog.html`
- Container Div ID: `catalog-page`
- Form Elements:
  - Search Input:
    - ID: `search-input`
    - Name: `search_query`
  - Category Filter Dropdown:
    - ID: `category-filter`
    - Name: `category_filter`
- Auctions Grid Div: `auctions-grid`
- Each auction card contains button:
  - ID: `view-auction-button-{auction_id}`
  - Navigates to `/auction/{auction_id}`

### 3. Auction Details Page
- Path: `/auction/<int:auction_id>`
- Methods: GET
- Template: `auction_details.html`
- Container Div ID: `auction-details-page`
- Elements:
  - `auction-title` (H1)
  - `auction-description` (Div)
  - `current-bid` (Div)
  - Bid History Div: `bid-history`
  - Button: `place-bid-button` navigates to `/place-bid/{auction_id}`

### 4. Place Bid Page
- Path: `/place-bid/<int:auction_id>`
- Methods: GET, POST
- Template: `place_bid.html`
- Container Div ID: `place-bid-page`
- Form Fields:
  - Input ID: `bidder-name`, Name: `bidder_name` (text)
  - Input ID: `bid-amount`, Name: `bid_amount` (number, step=0.01)
- Display Divs:
  - `auction-name`
  - `minimum-bid`
- Submit Button ID: `submit-bid-button`
- Form action: POST to `/place-bid/{auction_id}`

### 5. Bid History Page
- Path: `/bid-history`
- Methods: GET, POST (for filtering and sorting)
- Template: `bid_history.html`
- Container Div ID: `bid-history-page`
- Filter Dropdown:
  - ID: `filter-by-auction`
  - Name: `filter_auction`
- Sort Button ID: `sort-by-amount`
- Table ID: `bids-table` with columns: bid ID, auction name, bidder, amount, timestamp
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 6. Auction Categories Page
- Path: `/categories`
- Methods: GET
- Template: `categories.html`
- Container Div ID: `categories-page`
- List Div ID: `categories-list`
- Category Card Div ID (dynamic): `category-card-{category_id}`
- Button ID (dynamic): `view-category-button-{category_id}` navigates to `/categories/{category_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 7. Winners Page
- Path: `/winners`
- Methods: GET, POST (filter by winner)
- Template: `winners.html`
- Container Div ID: `winners-page`
- Filter Input ID: `filter-by-winner`, Name: `filter_winner`
- Winners List Div ID: `winners-list`
- Winner Card Div ID (dynamic): `winner-card-{auction_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 8. Trending Auctions Page
- Path: `/trending`
- Methods: GET, POST (for time range filter)
- Template: `trending.html`
- Container Div ID: `trending-page`
- Time Range Filter Dropdown ID: `time-range-filter`, Name: `time_range`
- Trending List Div ID: `trending-list`
- Each trending auction button ID: `view-auction-button-{auction_id}` navigates to `/auction/{auction_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 9. Auction Status Page
- Path: `/status`
- Methods: GET, POST (for status filtering)
- Template: `status.html`
- Container Div ID: `status-page`
- Status Filter Dropdown ID: `status-filter`, Name: `status_filter`
- Table ID: `status-table` with columns: name, status, time remaining, current bid
- Button ID: `refresh-status-button` triggers refresh
- Button ID: `back-to-dashboard` navigates to `/dashboard`


---

## Section 2: HTML Template UI Specification

### 1. dashboard.html
- Title: "Auction Dashboard"
- Div IDs:
  - `dashboard-page`
  - `featured-auctions`
- Buttons:
  - `browse-auctions-button`
  - `view-bids-button`
  - `trending-auctions-button`

### 2. catalog.html
- Title: "Auction Catalog"
- Div ID: `catalog-page`
- Inputs:
  - Search: ID `search-input`, Name `search_query`
  - Category Filter Dropdown: ID `category-filter`, Name `category_filter`
- Auctions Grid Div ID: `auctions-grid`
- Auction card button IDs: `view-auction-button-{auction_id}` (dynamic)

### 3. auction_details.html
- Title: "Auction Details"
- Div ID: `auction-details-page`
- Elements:
  - `auction-title` (H1)
  - `auction-description`
  - `current-bid`
  - `bid-history`
  - Button: `place-bid-button`

### 4. place_bid.html
- Title: "Place Bid"
- Div ID: `place-bid-page`
- Inputs:
  - `bidder-name` (text)
  - `bid-amount` (number)
- Divs:
  - `auction-name`
  - `minimum-bid`
- Submit Button ID: `submit-bid-button`

### 5. bid_history.html
- Title: "Bid History"
- Div ID: `bid-history-page`
- Table ID: `bids-table`
- Filter Dropdown ID: `filter-by-auction`, Name `filter_auction`
- Sort Button ID: `sort-by-amount`
- Back Button ID: `back-to-dashboard`

### 6. categories.html
- Title: "Auction Categories"
- Div ID: `categories-page`
- List Div ID: `categories-list`
- Category Cards Div ID: `category-card-{category_id}` (dynamic)
- Buttons: `view-category-button-{category_id}`
- Back Button ID: `back-to-dashboard`

### 7. winners.html
- Title: "Winning Items"
- Div ID: `winners-page`
- Filter Input ID: `filter-by-winner`, Name `filter_winner`
- Winners List Div ID: `winners-list`
- Winner Cards Div ID: `winner-card-{auction_id}` (dynamic)
- Back Button ID: `back-to-dashboard`

### 8. trending.html
- Title: "Trending Auctions"
- Div ID: `trending-page`
- Time Range Dropdown ID: `time-range-filter`, Name `time_range`
- Trending List Div ID: `trending-list`
- Buttons ID: `view-auction-button-{auction_id}`
- Back Button ID: `back-to-dashboard`

### 9. status.html
- Title: "Auction Status"
- Div ID: `status-page`
- Status Filter Dropdown ID: `status-filter`, Name `status_filter`
- Table ID: `status-table`
- Refresh Button ID: `refresh-status-button`
- Back Button ID: `back-to-dashboard`


---

## Section 3: Local Text File Data Specification

### 1. auctions.txt
- Path: `data/auctions.txt`
- Fields (pipe-separated):
  - auction_id
  - item_name
  - description
  - category
  - starting_bid (float)
  - current_bid (float)
  - end_time (YYYY-MM-DD HH:MM)
  - status (Active, Closed, Upcoming)
  - image_url
- Example:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  ```
- Used to show auction listings, details, status page.

### 2. categories.txt
- Path: `data/categories.txt`
- Fields:
  - category_id
  - category_name
  - description
  - item_count (int)
- Example:
  ```
  1|Electronics|Digital devices and gadgets|15
  ```
- Used on categories page and for filtering auctions.

### 3. bids.txt
- Path: `data/bids.txt`
- Fields:
  - bid_id
  - auction_id
  - bidder_name
  - bid_amount (float)
  - bid_timestamp (YYYY-MM-DD HH:MM)
- Example:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  ```
- Used for displaying bid history and validating bids.

### 4. winners.txt
- Path: `data/winners.txt`
- Fields:
  - winner_id
  - auction_id
  - item_name
  - winner_name
  - winning_bid (float)
  - win_date (YYYY-MM-DD)
- Example:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  ```
- Used to show winning items on winners page.

### 5. bid_history.txt
- Path: `data/bid_history.txt`
- Fields:
  - history_id
  - auction_id
  - auction_name
  - bidder_name
  - bid_amount (float)
  - bid_timestamp (YYYY-MM-DD HH:MM)
- Example:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  ```
- Used specifically to display comprehensive bid history.

### 6. items.txt
- Path: `data/items.txt`
- Fields:
  - item_id
  - auction_id
  - item_name
  - starting_price (float)
  - category
  - condition
  - seller_name
- Example:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  ```
- Optional detailed item info if needed.

### 7. trending.txt
- Path: `data/trending.txt`
- Fields:
  - auction_id
  - item_name
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (string e.g. "This Week")
- Example:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  ```
- Used in trending auctions page.


---

This revised design document consolidates and aligns the initial design with peer review input,
defining explicit routes, element IDs, form names, and data file schemas for an implementation-ready OnlineAuction Flask app.
