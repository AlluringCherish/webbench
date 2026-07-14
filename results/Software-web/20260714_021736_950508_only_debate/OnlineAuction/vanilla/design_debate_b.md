# OnlineAuction Flask Application Detailed Design Specification (Round 2)

---

## Section 1: Flask Routes and Methods

### 1. Dashboard Page
- Route: `/` or `/dashboard`
- Methods: GET
- Template: `dashboard.html`
- Container: `dashboard-page`
- Navigation Buttons:
  - `browse-auctions-button` -> redirects to `/catalog`
  - `view-bids-button` -> redirects to `/bids`
  - `trending-auctions-button` -> redirects to `/trending`

### 2. Auction Catalog Page
- Route: `/catalog`
- Methods: GET, POST (for searching and filtering)
- Template: `catalog.html`
- Container: `catalog-page`
- Form fields:
  - Search input: name=`search_query`, ID=`search-input`
  - Category filter: name=`category_filter`, ID=`category-filter` (options: Electronics, Collectibles, Furniture, Art, Other)
- Auctions grid container: `auctions-grid`
- Each auction card has button with ID `view-auction-button-{auction_id}`, which navigates to `/auction/{auction_id}`

### 3. Auction Details Page
- Route: `/auction/<int:auction_id>`
- Methods: GET
- Template: `auction_details.html`
- Container: `auction-details-page`
- Elements with IDs:
  - `auction-title` (H1)
  - `auction-description` (div)
  - `current-bid` (div)
  - `bid-history` (div)
  - Button `place-bid-button` navigates to `/auction/{auction_id}/place_bid`

### 4. Place Bid Page
- Route: `/auction/<int:auction_id>/place_bid`
- Methods: GET, POST
- Template: `place_bid.html`
- Container: `place-bid-page`
- Form fields:
  - Input text: name=`bidder_name`, ID=`bidder-name`
  - Input number: name=`bid_amount`, ID=`bid-amount` (step=0.01)
- Display divs:
  - `auction-name` (shows auction item title)
  - `minimum-bid` (minimum acceptable bid)
- Submit bid button with ID `submit-bid-button`, form action POSTs to same URL

### 5. Bid History Page
- Route: `/bids`
- Methods: GET, POST
- Template: `bid_history.html`
- Container: `bid-history-page`
- Elements:
  - Filter by auction dropdown: name=`filter_auction`, ID=`filter-by-auction`
  - Sort by amount button: ID=`sort-by-amount` (triggers sort on reload)
  - Table with ID `bids-table` (columns: bid ID, auction name, bidder, amount, timestamp)
  - Back to dashboard button with ID `back-to-dashboard` navigates to `/dashboard`

### 6. Auction Categories Page
- Route: `/categories`
- Methods: GET
- Template: `categories.html`
- Container: `categories-page`
- Categories list container: `categories-list`
- Each category card has div ID `category-card-{category_id}`
- Each category card's button `view-category-button-{category_id}` navigates to `/catalog?category={category_id}`
- Back to dashboard button with ID `back-to-dashboard` navigates to `/dashboard`

### 7. Winners Page
- Route: `/winners`
- Methods: GET, POST (filter by winner name)
- Template: `winners.html`
- Container: `winners-page`
- Winners list container: `winners-list`
- Filter input text: name=`filter_winner`, ID=`filter-by-winner`
- Each winner card div ID `winner-card-{auction_id}`
- Back to dashboard button with ID `back-to-dashboard` navigates to `/dashboard`

### 8. Trending Auctions Page
- Route: `/trending`
- Methods: GET, POST (filter by time range)
- Template: `trending.html`
- Container: `trending-page`
- Trending list container: `trending-list`
- Time range filter dropdown: name=`time_range`, ID=`time-range-filter` (options: Last 24 Hours, This Week, All Time)
- Each auction card's button with ID `view-auction-button-{auction_id}` navigates to `/auction/{auction_id}`
- Back to dashboard button with ID `back-to-dashboard` navigates to `/dashboard`

### 9. Auction Status Page
- Route: `/status`
- Methods: GET, POST (filter by status)
- Template: `status.html`
- Container: `status-page`
- Status filter dropdown: name=`status_filter`, ID=`status-filter` (options: All, Active, Closed, Upcoming)
- Status table ID: `status-table` (columns: name, status, time remaining, current bid)
- Refresh button with ID `refresh-status-button` triggers refresh
- Back to dashboard button with ID `back-to-dashboard` navigates to `/dashboard`

---

## Section 2: HTML Template Structure

### 1. dashboard.html
- Title: "Auction Dashboard"
- Container div ID: `dashboard-page`
- Div: `featured-auctions`
- Buttons: `browse-auctions-button`, `view-bids-button`, `trending-auctions-button`

### 2. catalog.html
- Title: "Auction Catalog"
- Container div ID: `catalog-page`
- Search input ID: `search-input` (type text)
- Category filter dropdown ID: `category-filter` (with predefined categories)
- Auctions grid div ID: `auctions-grid`
- Auction cards have buttons with dynamic IDs: `view-auction-button-{auction_id}`

### 3. auction_details.html
- Title: "Auction Details"
- Container div ID: `auction-details-page`
- H1 ID: `auction-title`
- Divs: `auction-description`, `current-bid`, `bid-history`
- Button ID: `place-bid-button`

### 4. place_bid.html
- Title: "Place Bid"
- Container div ID: `place-bid-page`
- Inputs: `bidder-name` (text), `bid-amount` (number, step 0.01)
- Divs: `auction-name`, `minimum-bid`
- Button ID: `submit-bid-button`

### 5. bid_history.html
- Title: "Bid History"
- Container div ID: `bid-history-page`
- Table ID: `bids-table`
- Dropdown ID: `filter-by-auction`
- Button IDs: `sort-by-amount`, `back-to-dashboard`

### 6. categories.html
- Title: "Auction Categories"
- Container div ID: `categories-page`
- List container ID: `categories-list`
- Category cards with div IDs: `category-card-{category_id}`
- Buttons: `view-category-button-{category_id}`, `back-to-dashboard`

### 7. winners.html
- Title: "Winning Items"
- Container div ID: `winners-page`
- List div ID: `winners-list`
- Input ID: `filter-by-winner`
- Winner cards with div IDs: `winner-card-{auction_id}`
- Button ID: `back-to-dashboard`

### 8. trending.html
- Title: "Trending Auctions"
- Container div ID: `trending-page`
- Div ID: `trending-list`
- Dropdown ID: `time-range-filter`
- Buttons: `view-auction-button-{auction_id}`, `back-to-dashboard`

### 9. status.html
- Title: "Auction Status"
- Container div ID: `status-page`
- Dropdown ID: `status-filter`
- Table ID: `status-table`
- Buttons: `refresh-status-button`, `back-to-dashboard`

---

## Section 3: Data File Format Specifications

### 1. auctions.txt
- Filename: `data/auctions.txt`
- Pipe-delimited fields:
  `auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url`
- Example:
  `1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg`
- Usage: For catalog, details, and status pages

### 2. categories.txt
- Filename: `data/categories.txt`
- Fields:
  `category_id|category_name|description|item_count`
- Example:
  `1|Electronics|Digital devices and gadgets|15`
- Usage: For categories page and filtering

### 3. bids.txt
- Filename: `data/bids.txt`
- Fields:
  `bid_id|auction_id|bidder_name|bid_amount|bid_timestamp`
- Example:
  `1|1|Alice Johnson|45.50|2025-02-05 14:30`
- Usage: For tracking bids and auction details

### 4. winners.txt
- Filename: `data/winners.txt`
- Fields:
  `winner_id|auction_id|item_name|winner_name|winning_bid|win_date`
- Example:
  `1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08`
- Usage: Show winners on winners page

### 5. bid_history.txt
- Filename: `data/bid_history.txt`
- Fields:
  `history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp`
- Example:
  `1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00`
- Usage: Detailed bid history

### 6. items.txt
- Filename: `data/items.txt`
- Fields:
  `item_id|auction_id|item_name|starting_price|category|condition|seller_name`
- Example:
  `1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector`
- Usage: Additional item details if needed

### 7. trending.txt
- Filename: `data/trending.txt`
- Fields:
  `auction_id|item_name|bid_count|current_bid|trending_rank|time_period`
- Example:
  `2|iPhone 14 Pro|12|620.00|1|This Week`
- Usage: Display trending auctions

---

## Summary
This design specification consolidates route paths, HTTP methods, templates, UI element IDs, navigation flows, form inputs, and local data file schemas for the OnlineAuction Flask app.
It aligns with the application requirements and user task description for straightforward implementation and data handling.
