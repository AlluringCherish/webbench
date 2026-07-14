# OnlineAuction Flask Application Design Specification

---

## Section 1: Flask Routes and Web Interface Contract

### 1. Dashboard Page
- Route: `/` and `/dashboard` (both serve Dashboard)
- Methods: GET
- Template: `dashboard.html`
- Container Div ID: `dashboard-page`
- Navigation Buttons:
  - `browse-auctions-button` navigates to `/catalog`
  - `view-bids-button` navigates to `/bid-history`
  - `trending-auctions-button` navigates to `/trending`

### 2. Auction Catalog Page
- Route: `/catalog`
- Methods: GET, POST (for search and category filter)
- Template: `catalog.html`
- Container Div ID: `catalog-page`
- Form Elements:
  - Search Input: ID `search-input`, name `search_query`
  - Category Filter Dropdown: ID `category-filter`, name `category_filter` (with options Electronics, Collectibles, Furniture, Art, Other)
- Auctions Grid Div ID: `auctions-grid`
- Each auction card has button with dynamic ID: `view-auction-button-{auction_id}`, navigating to `/auction/{auction_id}`

### 3. Auction Details Page
- Route: `/auction/<int:auction_id>`
- Methods: GET
- Template: `auction_details.html`
- Container Div ID: `auction-details-page`
- Elements:
  - `auction-title` (H1)
  - `auction-description` (Div)
  - `current-bid` (Div)
  - `bid-history` (Div)
  - Button ID: `place-bid-button` navigates to `/place-bid/{auction_id}`

### 4. Place Bid Page
- Route: `/place-bid/<int:auction_id>`
- Methods: GET, POST
- Template: `place_bid.html`
- Container Div ID: `place-bid-page`
- Form Fields:
  - Input text: ID `bidder-name`, name `bidder_name`
  - Input number: ID `bid-amount`, name `bid_amount`, step=0.01
- Display Divs:
  - `auction-name`
  - `minimum-bid`
- Submit Button ID: `submit-bid-button`
- Form action POSTS to `/place-bid/{auction_id}`

### 5. Bid History Page
- Route: `/bid-history`
- Methods: GET, POST (for filtering by auction and sorting)
- Template: `bid_history.html`
- Container Div ID: `bid-history-page`
- Filter Dropdown: ID `filter-by-auction`, name `filter_auction`
- Sort Button ID: `sort-by-amount`
- Table ID: `bids-table` with columns: bid ID, auction name, bidder, amount, timestamp
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 6. Auction Categories Page
- Route: `/categories`
- Methods: GET
- Template: `categories.html`
- Container Div ID: `categories-page`
- Categories List Div ID: `categories-list`
- Each category card: Div ID `category-card-{category_id}`
- Each category card button: ID `view-category-button-{category_id}` navigates to `/categories/{category_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 7. Winners Page
- Route: `/winners`
- Methods: GET, POST (for filtering by winner name)
- Template: `winners.html`
- Container Div ID: `winners-page`
- Filter Input ID: `filter-by-winner`, name `filter_winner`
- Winners List Div ID: `winners-list`
- Each winner card Div ID: `winner-card-{auction_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 8. Trending Auctions Page
- Route: `/trending`
- Methods: GET, POST (for filtering by time range)
- Template: `trending.html`
- Container Div ID: `trending-page`
- Time Range Filter Dropdown ID: `time-range-filter`, name `time_range` (options: Last 24 Hours, This Week, All Time)
- Trending List Div ID: `trending-list`
- Each trending auction button ID: `view-auction-button-{auction_id}` navigates to `/auction/{auction_id}`
- Button ID: `back-to-dashboard` navigates to `/dashboard`

### 9. Auction Status Page
- Route: `/status`
- Methods: GET, POST (for status filtering)
- Template: `status.html`
- Container Div ID: `status-page`
- Status Filter Dropdown ID: `status-filter`, name `status_filter` (options: All, Active, Closed, Upcoming)
- Table ID: `status-table` with columns: name, status, time remaining, current bid
- Button ID: `refresh-status-button` to trigger refresh
- Button ID: `back-to-dashboard` navigates to `/dashboard`


---

## Section 2: HTML Template UI IDs and Page Titles

### 1. dashboard.html
- Title: "Auction Dashboard"
- Container Div IDs:
  - `dashboard-page`
  - `featured-auctions`
- Buttons:
  - `browse-auctions-button`
  - `view-bids-button`
  - `trending-auctions-button`

### 2. catalog.html
- Title: "Auction Catalog"
- Container Div ID: `catalog-page`
- Inputs:
  - Search input ID `search-input`, name `search_query`
  - Category filter dropdown ID `category-filter`, name `category_filter` (categories: Electronics, Collectibles, Furniture, Art, Other)
- Auctions grid Div ID: `auctions-grid`
- Auction card button IDs: `view-auction-button-{auction_id}` (dynamic)

### 3. auction_details.html
- Title: "Auction Details"
- Container Div ID: `auction-details-page`
- Elements:
  - `auction-title` (H1)
  - `auction-description` (Div)
  - `current-bid` (Div)
  - `bid-history` (Div)
  - Button ID: `place-bid-button`

### 4. place_bid.html
- Title: "Place Bid"
- Container Div ID: `place-bid-page`
- Inputs:
  - `bidder-name` (text)
  - `bid-amount` (number, step=0.01)
- Divs:
  - `auction-name`
  - `minimum-bid`
- Submit Button ID: `submit-bid-button`

### 5. bid_history.html
- Title: "Bid History"
- Container Div ID: `bid-history-page`
- Table ID: `bids-table`
- Filter Dropdown ID: `filter-by-auction`, name `filter_auction`
- Sort Button ID: `sort-by-amount`
- Back Button ID: `back-to-dashboard`

### 6. categories.html
- Title: "Auction Categories"
- Container Div ID: `categories-page`
- List Div ID: `categories-list`
- Category cards Div IDs: `category-card-{category_id}` (dynamic)
- Buttons:
  - `view-category-button-{category_id}`
  - `back-to-dashboard`

### 7. winners.html
- Title: "Winning Items"
- Container Div ID: `winners-page`
- Filter Input ID: `filter-by-winner`, name `filter_winner`
- Winners list Div ID: `winners-list`
- Winner card Div IDs: `winner-card-{auction_id}` (dynamic)
- Back Button ID: `back-to-dashboard`

### 8. trending.html
- Title: "Trending Auctions"
- Container Div ID: `trending-page`
- Time Range Filter Dropdown ID: `time-range-filter`, name `time_range` (options: Last 24 Hours, This Week, All Time)
- Trending List Div ID: `trending-list`
- Buttons IDs: `view-auction-button-{auction_id}` (dynamic)
- Back Button ID: `back-to-dashboard`

### 9. status.html
- Title: "Auction Status"
- Container Div ID: `status-page`
- Status Filter Dropdown ID: `status-filter`, name `status_filter` (options: All, Active, Closed, Upcoming)
- Table ID: `status-table`
- Buttons:
  - `refresh-status-button`
  - `back-to-dashboard`


---

## Section 3: Local Text File Data Storage

### 1. auctions.txt
- Filename: `data/auctions.txt`
- Fields (pipe-delimited, in order):
  - auction_id
  - item_name
  - description
  - category
  - starting_bid (float)
  - current_bid (float)
  - end_time (format: YYYY-MM-DD HH:MM)
  - status (one of Active, Closed, Upcoming)
  - image_url
- Example entry:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  ```
- Usage: Display in catalog, auction details, and status pages.

### 2. categories.txt
- Filename: `data/categories.txt`
- Fields:
  - category_id
  - category_name
  - description
  - item_count (integer)
- Example:
  ```
  1|Electronics|Digital devices and gadgets|15
  ```
- Usage: Categories page and filtering auctions.

### 3. bids.txt
- Filename: `data/bids.txt`
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
- Usage: For bid history display and bid validation.

### 4. winners.txt
- Filename: `data/winners.txt`
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
- Usage: Winners page display.

### 5. bid_history.txt
- Filename: `data/bid_history.txt`
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
- Usage: Detailed bid history display.

### 6. items.txt
- Filename: `data/items.txt`
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
- Usage: Optional detailed item info.

### 7. trending.txt
- Filename: `data/trending.txt`
- Fields:
  - auction_id
  - item_name
  - bid_count (integer)
  - current_bid (float)
  - trending_rank (integer)
  - time_period (string, e.g. "This Week")
- Example:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  ```
- Usage: Trending auctions page.


---

This consolidated design specification fully aligns with the user's original requirements, resolves minor inconsistencies between two design proposals, and provides explicit route, UI, and data file details for implementation of the OnlineAuction Flask application.