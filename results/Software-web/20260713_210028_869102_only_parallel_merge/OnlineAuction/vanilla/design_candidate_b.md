# design_candidate_b.md

## OnlineAuction Web Application - Design Specification

---

### Overview
This document details the alternative design specification "design_candidate_b.md" for the OnlineAuction application. It covers UI element IDs, page layouts, navigation flows, data file usages, and web route structures with clear mapping between UI elements and backend.

---

## 1. Page Layouts and UI Elements

### 1. Dashboard Page
- Container Div: `dashboard-page` (main container)
- Featured Auctions Section: `featured-auctions` (displays featured auction items dynamically)
- Buttons:
  - `browse-auctions-button`: Navigates to Auction Catalog page
  - `view-bids-button`: Navigates to Bid History page
  - `trending-auctions-button`: Navigates to Trending Auctions page

---

### 2. Auction Catalog Page
- Container Div: `catalog-page`
- Input Fields:
  - `search-input`: Text input for search on item name, description, or auction ID
  - `category-filter`: Dropdown with options: Electronics, Collectibles, Furniture, Art, Other
- Auction Grid Container: `auctions-grid` - will contain multiple auction cards.
- Auction Card Dynamic Buttons:
  - `view-auction-button-{auction_id}` for every auction item (click to see details)

---

### 3. Auction Details Page
- Container Div: `auction-details-page`
- Title Heading: `auction-title` (H1 element showing auction item title)
- Description Div: `auction-description`
- Current Bid Display: `current-bid`
- Place Bid Button: `place-bid-button` (navigates to Place Bid Page for this auction)
- Bid History Section:
  - Container Div: `bid-history` showing bid entries (bidder names and amounts)

---

### 4. Place Bid Page
- Container Div: `place-bid-page`
- Input Fields:
  - `bidder-name`: Text input for bidder's name
  - `bid-amount`: Numeric input for bid amount
- Display fields:
  - `auction-name`: Shows auction item name
  - `minimum-bid`: Shows minimum required bid based on current bid
- Submit Button: `submit-bid-button` to submit the bid

---

### 5. Bid History Page
- Container Div: `bid-history-page`
- Bids Table: `bids-table` (columns: bid ID, auction name, bidder, amount, timestamp)
- Filters:
  - Dropdown `filter-by-auction` to filter bid entries by auction item
- Sorting Button:
  - `sort-by-amount` to sort bids by amount ascending/descending
- Navigation Button:
  - `back-to-dashboard` returns to Dashboard page

---

### 6. Auction Categories Page
- Container Div: `categories-page`
- Categories List Container: `categories-list`
- Category Cards (dynamic):
  - `category-card-{category_id}` containing category name and item count
  - Action Button: `view-category-button-{category_id}` to view items in specific category
- Navigation Button:
  - `back-to-dashboard`

---

### 7. Winners Page
- Container Div: `winners-page`
- Winners List Container: `winners-list`
- Winner Cards (dynamic):
  - `winner-card-{auction_id}` containing item name, winner name, winning bid
- Filter Input: `filter-by-winner` to filter winners by winner name
- Navigation Button:
  - `back-to-dashboard`

---

### 8. Trending Auctions Page
- Container Div: `trending-page`
- Trending List Container: `trending-list` showing ranked trending auctions
- Time Range Filter Dropdown: `time-range-filter` with options Last 24 Hours, This Week, All Time
- Dynamic View Buttons:
  - `view-auction-button-{auction_id}` to view auction details
- Navigation Button:
  - `back-to-dashboard`

---

### 9. Auction Status Page
- Container Div: `status-page`
- Status Filter Dropdown: `status-filter` with options All, Active, Closed, Upcoming
- Status Table: `status-table` with columns name, status, time remaining, current bid
- Refresh Button: `refresh-status-button` to reload status data
- Navigation Button:
  - `back-to-dashboard`

---

## 2. Navigation and Page Flows

- Application start page: **Dashboard Page** (`dashboard-page`)

### Navigation Buttons and Routes from Dashboard
| Element ID                 | Action                             | Route (GET)            |
|----------------------------|----------------------------------|------------------------|
| browse-auctions-button     | Go to Auction Catalog Page        | `/catalog`             |
| view-bids-button           | Go to Bid History Page            | `/bids`                |
| trending-auctions-button   | Go to Trending Auctions Page      | `/trending`            |

### Auction Catalog Page
- Search/filter updates page content dynamically
- Button `view-auction-button-{auction_id}` navigates to Auction Details Page
  Route: `/auction/<auction_id>`

### Auction Details Page
- Button `place-bid-button` navigates to Place Bid Page
  Route: `/auction/<auction_id>/place_bid`

### Place Bid Page
- On submit button `submit-bid-button`, form posts bid data to `/auction/<auction_id>/place_bid` (POST)
- Redirects user back to Auction Details Page upon success

### Bid History Page
- Filtering by auction triggers reload with query params
  Route example: `/bids?auction_id=<auction_id>` (GET)
- Sorting toggled by `sort-by-amount` button
- `back-to-dashboard` navigates `/dashboard`

### Auction Categories Page
- Clicking `view-category-button-{category_id}` navigates to filtered Auction Catalog Page
  Route example: `/catalog?category_id=<category_id>` (GET)
- `back-to-dashboard` navigates `/dashboard`

### Winners Page
- Filter by winner name reloads winners with query param
  Route example: `/winners?filter_name=<winner_name>`
- `back-to-dashboard` navigates `/dashboard`

### Trending Auctions Page
- `time-range-filter` triggers reload with param
  Route example: `/trending?time_range=Last24Hours|ThisWeek|AllTime`
- `view-auction-button-{auction_id}` to `/auction/<auction_id>`
- `back-to-dashboard` to `/dashboard`

### Auction Status Page
- Dropdown `status-filter` filters auctions, reloads page with param
  Route example: `/status?status=All|Active|Closed|Upcoming`
- Refresh button triggers page refresh `/status`
- `back-to-dashboard` to `/dashboard`

---

## 3. Data Storage and File Formats

All data files are stored in `data/` directory. Delimiter is `|` for all text files.

### 3.1. Auctions Data (`auctions.txt`)
Format:
```
auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
```
Used for auction listings, auction details, and status page.

### 3.2. Categories Data (`categories.txt`)
Format:
```
category_id|category_name|description|item_count
```
Used in Categories Page and category filter dropdowns.

### 3.3. Bids Data (`bids.txt`)
Format:
```
bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
```
Used in Bid History, Auction Details (bid history section), and place bid validation.

### 3.4. Winners Data (`winners.txt`)
Format:
```
winner_id|auction_id|item_name|winner_name|winning_bid|win_date
```
Used in Winners Page display and filtering.

### 3.5. Bid History Data (`bid_history.txt`)
Format:
```
history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
```
Optional comprehensive record used in Bid History Page for extended bid tracking.

### 3.6. Items Data (`items.txt`)
Format:
```
item_id|auction_id|item_name|starting_price|category|condition|seller_name
```
Can be used for detailed item info if needed.

### 3.7. Trending Data (`trending.txt`)
Format:
```
auction_id|item_name|bid_count|current_bid|trending_rank|time_period
```
Used in Trending Auctions Page.

---

## 4. Web Route Structures

| Route URL                         | HTTP Method | Parameters                                  | Description                                   |
|----------------------------------|-------------|---------------------------------------------|-----------------------------------------------|
| `/dashboard`                     | GET         | None                                        | Render Dashboard Page                          |
| `/catalog`                      | GET         | Optional: `search`, `category_id`
| Render Auction Catalog with filters|
| `/auction/<int:auction_id>`     | GET         | auction_id                                 | Render Auction Details Page                    |
| `/auction/<int:auction_id>/place_bid` | GET, POST       | auction_id, plus POST data (bidder_name, bid_amount) | GET shows Place Bid Page; POST submits bid   |
| `/bids`                        | GET         | Optional: `auction_id`, `sort` (asc/desc) | Show Bid History with filter and sort options |
| `/categories`                 | GET         | None                                        | Show Auction Categories                        |
| `/categories/<int:category_id>`| GET         | category_id                                 | Show Auction Catalog filtered by category     |
| `/winners`                     | GET         | Optional: `filter_name`                      | Show Winners Page filtered by winner name     |
| `/trending`                   | GET         | Optional: `time_range`                        | Show Trending Auctions filtered by time range|
| `/status`                    | GET         | Optional: `status`                            | Show Auction Status Page with filter          |

---

## 5. Data Access and Interaction Summary

- **Dashboard:** Reads auctions.txt to show featured auctions
- **Auction Catalog:** Reads auctions.txt and categories.txt for display and filters
- **Auction Details:** Reads auctions.txt for details and bids.txt for bid history
- **Place Bid:** Reads auctions.txt for minimum bid; writes new bid to bids.txt and bid_history.txt
- **Bid History:** Reads bids.txt and optionally bid_history.txt; filters and sorts as requested
- **Auction Categories:** Reads categories.txt
- **Winners:** Reads winners.txt with optional filtering
- **Trending Auctions:** Reads trending.txt filtered by time range
- **Auction Status:** Reads auctions.txt filtered by status

---

This completes the detailed alternative UI and backend design specification "design_candidate_b.md" for the OnlineAuction application.

