# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

### 1. Root Route
- Path: `/`
- HTTP Method: GET
- Function Name: `root_redirect`
- Description: Redirects to dashboard page.
- Renders: Redirect to `dashboard` route.
- Context Variables: None

### 2. Dashboard Page
- Path: `/dashboard`
- HTTP Method: GET
- Function Name: `dashboard`
- Renders: `dashboard.html`
- Context Variables:
  - `featured_properties` (list of dict): List of featured property summaries.
  - `recent_listings` (list of dict): List of recent property summaries.

### 3. Property Search Page
- Path: `/properties/search`
- HTTP Methods: GET, POST
- Function Name: `property_search`
- Description: GET displays the search page with all or filtered properties. POST used for filtering with form data.
- Renders: `property_search.html`
- Context Variables (for GET and POST results):
  - `properties` (list of dict): Filtered properties with details.
  - `locations` (list of str): Available locations for filtering.
  - `property_types` (list of str): Property types for the dropdown ("House", "Apartment", "Condo", "Land").
- Expected Form Data (POST):
  - `location_input` (str, optional)
  - `price_min` (float, optional)
  - `price_max` (float, optional)
  - `property_type_filter` (str, optional)

### 4. Property Details Page
- Path: `/properties/<int:property_id>`
- HTTP Method: GET
- Function Name: `property_details`
- Renders: `property_details.html`
- Context Variables:
  - `property` (dict): Property details including address, price, description, features.
  - `agent` (dict): Agent associated with the property.

### 5. Property Inquiry Page
- Path: `/inquiries/submit` (GET for form display, POST for submission)
- HTTP Methods: GET, POST
- Function Name: `submit_inquiry`
- Renders: `property_inquiry.html`
- Context Variables (GET):
  - `properties` (list of dict): Properties available for inquiry selection.
- Expected Form Data (POST):
  - `selected_property_id` (int)
  - `inquiry_name` (str)
  - `inquiry_email` (str)
  - `inquiry_phone` (str)
  - `inquiry_message` (str)

### 6. My Inquiries Page
- Path: `/inquiries`
- HTTP Methods: GET, POST
- Function Name: `my_inquiries`
- Description: GET displays all inquiries; POST filters by status or delete inquiry.
- Renders: `my_inquiries.html`
- Context Variables:
  - `inquiries` (list of dict): List of inquiries with property info.
  - `status_filter` (str): Current filter status ('All', 'Pending', 'Contacted', 'Resolved').
- Expected Form Data (POST):
  - `filter_status` (str, optional) - For filtering inquiries by status.
  - `delete_inquiry_id` (int, optional) - To delete an inquiry by ID.

### 7. My Favorites Page
- Path: `/favorites`
- HTTP Methods: GET, POST
- Function Name: `my_favorites`
- Description: GET shows favorite properties, POST handles add/remove favorite actions.
- Renders: `my_favorites.html`
- Context Variables:
  - `favorites` (list of dict): Favorite properties details.
- Expected Form Data (POST):
  - `add_property_id` (int, optional) - Property to add to favorites.
  - `remove_property_id` (int, optional) - Property to remove from favorites.

### 8. Agent Directory Page
- Path: `/agents`
- HTTP Method: GET
- Function Name: `agents_directory`
- Renders: `agents.html`
- Context Variables:
  - `agents` (list of dict): All agents with contact info.

### 9. Locations Page
- Path: `/locations`
- HTTP Methods: GET, POST
- Function Name: `locations_page`
- Description: GET displays all locations; POST sorts the list.
- Renders: `locations.html`
- Context Variables:
  - `locations` (list of dict): Locations data.
  - `sort_option` (str): Current sort selection ('By Name', 'By Properties Count', 'By Average Price').
- Expected Form Data (POST):
  - `location_sort` (str, optional)

---

## Section 2: HTML Templates (Frontend)

### Template: dashboard.html
- Page Title: "Real Estate Dashboard"
- Elements:
  - `dashboard-page` (Div)
  - `featured-properties` (Div)
  - `browse-properties-button` (Button)
  - `my-inquiries-button` (Button)
  - `my-favorites-button` (Button)
- Context Variables:
  - `featured_properties` (list of dict): Properties to display as featured.
  - `recent_listings` (list of dict): Properties to display as recent listings.
- Navigation:
  - `browse-properties-button` -> `url_for('property_search')`
  - `my-inquiries-button` -> `url_for('my_inquiries')`
  - `my-favorites-button` -> `url_for('my_favorites')`
- Forms: None

---

### Template: property_search.html
- Page Title: "Property Search"
- Elements:
  - `search-page` (Div)
  - `location-input` (Input)
  - `price-range-min` (Input number)
  - `price-range-max` (Input number)
  - `property-type-filter` (Dropdown) with options: "House", "Apartment", "Condo", "Land"
  - `properties-grid` (Div)
  - `view-property-button-{property_id}` (Button) for each property displayed
- Context Variables:
  - `properties` (list of dict): Properties to display
  - `locations` (list of str): Locations available
  - `property_types` (list of str): Property type filter options
- Navigation:
  - `view-property-button-{property_id}` -> `url_for('property_details', property_id=property_id)`
- Forms:
  - Search/filter form with inputs: `location-input`, `price-range-min`, `price-range-max`, `property-type-filter`
  - Submit action: POST to `/properties/search`

---

### Template: property_details.html
- Page Title: "Property Details"
- Elements:
  - `property-details-page` (Div)
  - `property-address` (H1)
  - `property-price` (Div)
  - `property-description` (Div)
  - `property-features` (Div)
  - `add-to-favorites-button` (Button)
  - `submit-inquiry-button` (Button)
- Context Variables:
  - `property` (dict): Full details of the property
  - `agent` (dict): Agent info associated with property
- Navigation:
  - `add-to-favorites-button`: Form POST or AJAX POST to add property to favorites
  - `submit-inquiry-button`: Navigate to `url_for('submit_inquiry')` with selected property pre-selected

---

### Template: property_inquiry.html
- Page Title: "Submit Property Inquiry"
- Elements:
  - `inquiry-page` (Div)
  - `select-property` (Dropdown)
  - `inquiry-name` (Input)
  - `inquiry-email` (Input email)
  - `inquiry-phone` (Input tel)
  - `inquiry-message` (Textarea)
  - `submit-inquiry-button` (Button)
- Context Variables:
  - `properties` (list of dict): Properties available for inquiry
- Navigation:
  - Form POST action to `/inquiries/submit`
- Forms:
  - Inquiry submission form with fields: `select-property`, `inquiry-name`, `inquiry-email`, `inquiry-phone`, `inquiry-message`
  - Submit button: `submit-inquiry-button`

---

### Template: my_inquiries.html
- Page Title: "My Inquiries"
- Elements:
  - `inquiries-page` (Div)
  - `inquiries-table` (Table), columns: Property, Date, Status, Contact Info
  - `inquiry-status-filter` (Dropdown) with options: "All", "Pending", "Contacted", "Resolved"
  - `delete-inquiry-button-{inquiry_id}` (Button) for each inquiry
  - `back-to-dashboard` (Button)
- Context Variables:
  - `inquiries` (list of dict): All inquiries to display
  - `status_filter` (str): Current filter status
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
- Forms:
  - Filter inquiries by status with `inquiry-status-filter` dropdown POST to `/inquiries`
  - Delete inquiry buttons POST with `delete-inquiry-id` to `/inquiries`

---

### Template: my_favorites.html
- Page Title: "My Favorite Properties"
- Elements:
  - `favorites-page` (Div)
  - `favorites-list` (Div)
  - `remove-from-favorites-button-{property_id}` (Button) for each favorite property
  - `view-property-button-{property_id}` (Button) for each favorite property
  - `back-to-dashboard` (Button)
- Context Variables:
  - `favorites` (list of dict): Favorite properties details
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
  - `view-property-button-{property_id}` -> `url_for('property_details', property_id=property_id)`
- Forms:
  - Remove favorite buttons POST to `/favorites` with `remove_property_id`

---

### Template: agents.html
- Page Title: "Real Estate Agents"
- Elements:
  - `agents-page` (Div)
  - `agents-list` (Div)
  - `agent-search` (Input)
  - `contact-agent-button-{agent_id}` (Button) for each agent
  - `back-to-dashboard` (Button)
- Context Variables:
  - `agents` (list of dict): List of agents
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
- Forms:
  - Agent search form POST (optional) - not specified as required, so search can be client-side.

---

### Template: locations.html
- Page Title: "Featured Locations"
- Elements:
  - `locations-page` (Div)
  - `locations-list` (Div)
  - `view-location-button-{location_id}` (Button) for each location
  - `location-sort` (Dropdown) with options: "By Name", "By Properties Count", "By Average Price"
  - `back-to-dashboard` (Button)
- Context Variables:
  - `locations` (list of dict): Locations data
  - `sort_option` (str): Current sort option
- Navigation:
  - `back-to-dashboard` -> `url_for('dashboard')`
  - `view-location-button-{location_id}` -> Navigate to property search filtered by location (route not specified, so can be a GET with query param)
- Forms:
  - Sort dropdown form POST to `/locations` with `location_sort` input

---

## Section 3: Data File Schemas (Backend)

### 1. Properties Data File
- File Path: `data/properties.txt`
- Fields (pipe-delimited):
  1. `property_id` (int)
  2. `address` (str)
  3. `location` (str)
  4. `price` (float)
  5. `property_type` (str)
  6. `bedrooms` (int)
  7. `bathrooms` (float)
  8. `square_feet` (int)
  9. `description` (str)
  10. `agent_id` (int)
  11. `status` (str) - e.g., "Available", "Sold"
- Description: Stores details of all properties including their description, type, and associated agent.
- Example Rows:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. Locations Data File
- File Path: `data/locations.txt`
- Fields (pipe-delimited):
  1. `location_id` (int)
  2. `location_name` (str)
  3. `region` (str)
  4. `average_price` (float)
  5. `property_count` (int)
  6. `description` (str)
- Description: Stores information about various locations including average property price and count.
- Example Rows:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. Property Inquiries Data File
- File Path: `data/inquiries.txt`
- Fields (pipe-delimited):
  1. `inquiry_id` (int)
  2. `property_id` (int)
  3. `customer_name` (str)
  4. `customer_email` (str)
  5. `customer_phone` (str)
  6. `message` (str)
  7. `inquiry_date` (str, format YYYY-MM-DD)
  8. `status` (str) - e.g., "Pending", "Contacted", "Resolved"
- Description: Stores inquiries submitted by customers about properties.
- Example Rows:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. Favorite Properties Data File
- File Path: `data/favorites.txt`
- Fields (pipe-delimited):
  1. `favorite_id` (int)
  2. `property_id` (int)
  3. `added_date` (str, format YYYY-MM-DD)
- Description: Stores favorite property entries marked by users.
- Example Rows:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. Real Estate Agents Data File
- File Path: `data/agents.txt`
- Fields (pipe-delimited):
  1. `agent_id` (int)
  2. `agent_name` (str)
  3. `specialization` (str)
  4. `email` (str)
  5. `phone` (str)
  6. `properties_sold` (int)
- Description: Stores details about real estate agents.
- Example Rows:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
