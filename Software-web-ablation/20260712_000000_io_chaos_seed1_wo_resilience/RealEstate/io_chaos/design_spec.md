# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

### General Notes
- Root route `/` redirects to the dashboard page `/dashboard`.
- All routes render HTML templates with required context variables.
- Use descriptive, lowercase_with_underscores function names.
- Route parameters included where applicable.

---

### Routes Definition

1. **Root Redirect**
   - Path: `/`
   - Methods: GET
   - Function: `root_redirect`
   - Action: Redirect to `/dashboard`
   - Template: None
   - Context: None

2. **Dashboard Page**
   - Path: `/dashboard`
   - Methods: GET
   - Function: `dashboard`
   - Template: `dashboard.html`
   - Context Variables:
     - `featured_properties` (list of dict) — featured property summaries
     - `recent_listings` (list of dict) — recent property summaries

3. **Property Search Page**
   - Path: `/search`
   - Methods: GET, POST
     - GET: Render with current property listings
     - POST: Process search filters from form
   - Function: `property_search`
   - Template: `property_search.html`
   - Context Variables:
     - `properties` (list of dict) — filtered property results
     - `location_filter` (str) — location search keyword
     - `price_min` (float or None) — minimum price filter
     - `price_max` (float or None) — maximum price filter
     - `property_type_filter` (str) — selected property type filter
     - `property_types` (list of str) — all property type options ["House", "Apartment", "Condo", "Land"]
   - Expected POST form data:
     - `location_input` (str)
     - `price_range_min` (float)
     - `price_range_max` (float)
     - `property_type_filter` (str)

4. **Property Details Page**
   - Path: `/property/<int:property_id>`
   - Methods: GET, POST
     - GET: Show property details
     - POST: Actions (like adding to favorites)
   - Function: `property_details`
   - Template: `property_details.html`
   - Context Variables:
     - `property` (dict) — detailed property information
   - Expected POST form data:
     - Action indicated by form submit to add to favorites or submit inquiry
     - E.g., `add_to_favorites` button triggered

5. **Property Inquiry Page**
   - Path: `/inquiry`
   - Methods: GET, POST
     - GET: Display inquiry form
     - POST: Submit new inquiry
   - Function: `property_inquiry`
   - Template: `property_inquiry.html`
   - Context Variables:
     - `properties` (list of dict) — properties available for inquiry selection
   - Expected POST form data:
     - `select_property` (int) — property_id
     - `inquiry_name` (str)
     - `inquiry_email` (str)
     - `inquiry_phone` (str)
     - `inquiry_message` (str)

6. **My Inquiries Page**
   - Path: `/inquiries`
   - Methods: GET, POST
     - GET: Display list of inquiries
     - POST: Handle inquiry deletion
   - Function: `my_inquiries`
   - Template: `my_inquiries.html`
   - Context Variables:
     - `inquiries` (list of dict) — all user inquiries
     - `status_filter` (str) — current status filter selected
     - `status_options` (list of str) — ["All", "Pending", "Contacted", "Resolved"]
   - Expected POST form data:
     - `delete_inquiry_id` (int) — inquiry_id to delete

7. **My Favorites Page**
   - Path: `/favorites`
   - Methods: GET, POST
     - GET: Display favorites list
     - POST: Handle removal from favorites
   - Function: `my_favorites`
   - Template: `my_favorites.html`
   - Context Variables:
     - `favorites` (list of dict) — all favorite properties details
   - Expected POST form data:
     - `remove_property_id` (int) — property_id to remove from favorites

8. **Agent Directory Page**
   - Path: `/agents`
   - Methods: GET
   - Function: `agent_directory`
   - Template: `agents.html`
   - Context Variables:
     - `agents` (list of dict) — list of agents
     - `search_query` (str) — current agent search filter, if any

9. **Locations Page**
   - Path: `/locations`
   - Methods: GET, POST
     - GET: Show locations list with sorting
     - POST: Handle location sorting or filtering
   - Function: `locations_page`
   - Template: `locations.html`
   - Context Variables:
     - `locations` (list of dict) — locations data
     - `sort_option` (str) — current sorting option
     - `sort_options` (list of str) — ["By Name", "By Properties Count", "By Average Price"]
   - Expected POST form data:
     - `location_sort` (str) — selected sort option

---

## Section 2: HTML Templates (Frontend)

### General Notes
- Each page has a container div with the root element ID as specified.
- Navigation via buttons uses Flask `url_for()` with function names defined in Section 1.
- Element IDs, including dynamic IDs with placeholders, are exactly as specified.
- Forms specify `action` routes via `url_for()` matching the POST routes in Section 1.

---

### 1. Dashboard Template `dashboard.html`
- Page title and H1: "Real Estate Dashboard"
- Elements:
  - `dashboard-page` (Div container)
  - `featured-properties` (Div showing featured property cards)
  - Buttons:
    - `browse-properties-button` → navigates to `property_search`
    - `my-inquiries-button` → navigates to `my_inquiries`
    - `my-favorites-button` → navigates to `my_favorites`
- Context variables:
  - `featured_properties` (list of dict) — property summaries for featured
  - `recent_listings` (list of dict) — recent property summaries (optional display)

---

### 2. Property Search Template `property_search.html`
- Page title and H1: "Property Search"
- Elements:
  - `search-page` (Div container)
  - Inputs:
    - `location-input` (text)
    - `price-range-min` (number)
    - `price-range-max` (number)
  - Dropdown:
    - `property-type-filter` with options: "House", "Apartment", "Condo", "Land"
  - Properties grid:
    - `properties-grid` (Div containing all property cards)
    - Each property card includes button with ID: `view-property-button-{property_id}`
      - Navigates to `property_details` route with property_id
- Context variables:
  - `properties` (list of dict) — filtered properties to display
  - `location_filter` (str)
  - `price_min`, `price_max` (float or None)
  - `property_type_filter` (str)
  - `property_types` (list of str)
- Form:
  - Search/filter form
  - Action route: POST to `property_search`
  - Inputs named as above

---

### 3. Property Details Template `property_details.html`
- Page title and H1: "Property Details"
- Elements:
  - `property-details-page` (Div container)
  - `property-address` (H1) — property address
  - `property-price` (Div) — price display
  - `property-description` (Div) — description text
  - `property-features` (Div) — beds, baths, square feet
  - Buttons:
    - `add-to-favorites-button` — adds property to favorites (POST to same route)
    - `submit-inquiry-button` — link or action to inquiry page
- Context variables:
  - `property` (dict) — full details
- Forms:
  - Add to favorites form
    - Action: POST to `property_details` route with property_id
    - Submit button: `add-to-favorites-button`

---

### 4. Property Inquiry Template `property_inquiry.html`
- Page title and H1: "Submit Property Inquiry"
- Elements:
  - `inquiry-page` (Div container)
  - Dropdown:
    - `select-property` — properties to select (property_id as option values)
  - Inputs:
    - `inquiry-name`
    - `inquiry-email`
    - `inquiry-phone`
  - Textarea:
    - `inquiry-message`
  - Button:
    - `submit-inquiry-button` — submits form
- Context variables:
  - `properties` (list of dict)
- Form:
  - Action: POST to `property_inquiry`
  - Input fields and button as IDs above

---

### 5. My Inquiries Template `my_inquiries.html`
- Page title and H1: "My Inquiries"
- Elements:
  - `inquiries-page` (Div container)
  - Dropdown:
    - `inquiry-status-filter` with options ["All", "Pending", "Contacted", "Resolved"]
  - Table:
    - `inquiries-table` showing each inquiry row
    - Each inquiry row has delete button with ID: `delete-inquiry-button-{inquiry_id}`
  - `back-to-dashboard` button (navigates to `dashboard`)
- Context variables:
  - `inquiries` (list of dict)
  - `status_filter` (str)
  - `status_options` (list of str)
- Forms:
  - For filtering inquiries by status (GET or POST)
  - For deleting inquiry (POST)

---

### 6. My Favorites Template `my_favorites.html`
- Page title and H1: "My Favorite Properties"
- Elements:
  - `favorites-page` (Div container)
  - `favorites-list` (Div) with favorite property entries
  - Each property in favorites:
    - `remove-from-favorites-button-{property_id}` button
    - `view-property-button-{property_id}` button
  - `back-to-dashboard` button
- Context variables:
  - `favorites` (list of dict)
- Forms:
  - For removing favorites (POST)

---

### 7. Agent Directory Template `agents.html`
- Page title and H1: "Real Estate Agents"
- Elements:
  - `agents-page` (Div container)
  - `agents-list` (Div) with agent entries:
    - Each agent: photo (no ID), name, specialization, contact info
    - `contact-agent-button-{agent_id}` button
  - `agent-search` input text field
  - `back-to-dashboard` button
- Context variables:
  - `agents` (list of dict)
  - `search_query` (str)
- Forms:
  - Search (GET or POST) on agent name

---

### 8. Locations Template `locations.html`
- Page title and H1: "Featured Locations"
- Elements:
  - `locations-page` (Div container)
  - `locations-list` (Div) with location entries:
    - Each has a button: `view-location-button-{location_id}`
  - `location-sort` dropdown with options ["By Name", "By Properties Count", "By Average Price"]
  - `back-to-dashboard` button
- Context variables:
  - `locations` (list of dict)
  - `sort_option` (str)
  - `sort_options` (list of str)
- Forms:
  - Sorting form (POST)

---

## Section 3: Data File Schemas (Backend)

All data files are stored in the `data/` directory, pipe-delimited without header lines.

---

### 1. Properties Data
- File: `data/properties.txt`
- Fields (pipe `|` delimited):
  - `property_id` (int)
  - `address` (str)
  - `location` (str)
  - `price` (float)
  - `property_type` (str) (e.g., House, Apartment, Condo, Land)
  - `bedrooms` (int)
  - `bathrooms` (float)
  - `square_feet` (int)
  - `description` (str)
  - `agent_id` (int)
  - `status` (str) (e.g., Available, Sold)
- Description: Contains all property listings with full details.
- Example rows:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. Locations Data
- File: `data/locations.txt`
- Fields:
  - `location_id` (int)
  - `location_name` (str)
  - `region` (str)
  - `average_price` (float)
  - `property_count` (int)
  - `description` (str)
- Description: Stores popular locations data including statistics.
- Example rows:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. Property Inquiries Data
- File: `data/inquiries.txt`
- Fields:
  - `inquiry_id` (int)
  - `property_id` (int)
  - `customer_name` (str)
  - `customer_email` (str)
  - `customer_phone` (str)
  - `message` (str)
  - `inquiry_date` (str) (ISO date YYYY-MM-DD)
  - `status` (str) (e.g., Pending, Contacted, Resolved)
- Description: Records of all customer inquiries on properties.
- Example rows:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. Favorite Properties Data
- File: `data/favorites.txt`
- Fields:
  - `favorite_id` (int)
  - `property_id` (int)
  - `added_date` (str) (ISO date YYYY-MM-DD)
- Description: Tracks properties user marked as favorites.
- Example rows:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. Real Estate Agents Data
- File: `data/agents.txt`
- Fields:
  - `agent_id` (int)
  - `agent_name` (str)
  - `specialization` (str)
  - `email` (str)
  - `phone` (str)
  - `properties_sold` (int)
- Description: Information about real estate agents.
- Example rows:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
