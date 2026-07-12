# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

### Root Route
- Path URL: /
- Methods: GET
- Function Name: root_redirect
- Redirects to: dashboard (Route '/dashboard')

---

### 1. Dashboard Page
- Path URL: /dashboard
- Methods: GET
- Function Name: dashboard_page
- Template: dashboard.html
- Context Variables:
  - featured_properties (list of dict)
  - recent_listings (list of dict)

---

### 2. Property Search Page
- Path URL: /properties
- Methods: GET, POST
- Function Name: property_search_page
- Template: property_search.html
- Context Variables:
  - all_properties (list of dict)
  - filtered_properties (list of dict) [on POST]
  - locations (list of str)
  - property_types (list of str) [Static values: ["House", "Apartment", "Condo", "Land"]]
- Expected Form Data (POST):
  - location_input (str)
  - price_range_min (int or empty)
  - price_range_max (int or empty)
  - property_type_filter (str)

---

### 3. Property Details Page
- Path URL: /properties/<int:property_id>
- Methods: GET
- Function Name: property_details_page
- Template: property_details.html
- Context Variables:
  - property (dict)
  - agent (dict)
  - is_favorite (bool)

---

### 4. Property Inquiry Page
- Path URL: /inquiries/submit
- Methods: GET, POST
- Function Name: property_inquiry_page
- Template: property_inquiry.html
- Context Variables:
  - properties (list of dict)
- Expected Form Data (POST):
  - select_property (int) [property_id]
  - inquiry_name (str)
  - inquiry_email (str)
  - inquiry_phone (str)
  - inquiry_message (str)

---

### 5. My Inquiries Page
- Path URL: /inquiries
- Methods: GET, POST
- Function Name: my_inquiries_page
- Template: my_inquiries.html
- Context Variables:
  - inquiries (list of dict)
  - inquiry_status_filter (str) [from form or default "All"]
- Expected Form Data (POST):
  - inquiry_status_filter (str)
  - delete_inquiry_id (int) [Optional, upon delete request]

---

### 6. My Favorites Page
- Path URL: /favorites
- Methods: GET, POST
- Function Name: my_favorites_page
- Template: my_favorites.html
- Context Variables:
  - favorite_properties (list of dict)
- Expected Form Data (POST):
  - remove_favorite_property_id (int) [Optional, on remove action]

---

### 7. Agent Directory Page
- Path URL: /agents
- Methods: GET
- Function Name: agent_directory_page
- Template: agents.html
- Context Variables:
  - agents (list of dict)
  - search_query (str) [from query string or empty]

---

### 8. Locations Page
- Path URL: /locations
- Methods: GET, POST
- Function Name: locations_page
- Template: locations.html
- Context Variables:
  - locations (list of dict)
  - location_sort (str) [from form or default "By Name"]
- Expected Form Data (POST):
  - location_sort (str) [Values: "By Name", "By Properties Count", "By Average Price"]

---

## Section 2: HTML Templates (Frontend)

### Template: dashboard.html
- Page Title: Real Estate Dashboard
  - <title>: "Real Estate Dashboard"
  - <h1>: "Real Estate Dashboard"
- Element IDs:
  - dashboard-page (Div)
  - featured-properties (Div)
  - browse-properties-button (Button)
  - my-inquiries-button (Button)
  - my-favorites-button (Button)
- Context Variables:
  - featured_properties: List of dictionaries with property summary data (dict)
  - recent_listings: List of dictionaries with recent property summaries (dict)
- Navigation Mappings with url_for():
  - browse-properties-button: url_for('property_search_page')
  - my-inquiries-button: url_for('my_inquiries_page')
  - my-favorites-button: url_for('my_favorites_page')
- Forms: None

---

### Template: property_search.html
- Page Title: Property Search
  - <title>: "Property Search"
  - <h1>: "Property Search"
- Element IDs:
  - search-page (Div)
  - location-input (Input)
  - price-range-min (Input number)
  - price-range-max (Input number)
  - property-type-filter (Dropdown)
  - properties-grid (Div)
  - view-property-button-{property_id} (Button with dynamic property_id)
- Context Variables:
  - all_properties: List of all property dictionaries (dict)
  - filtered_properties: List of filtered property dictionaries (dict)
  - locations: List of location strings (str)
  - property_types: List of property type strings (str) [House, Apartment, Condo, Land]
- Navigation Mappings:
  - None (user stays on the search page)
- Forms:
  - Search/Filter Form:
    - action: url_for('property_search_page')
    - method: POST
    - Inputs:
      - location-input (text)
      - price-range-min (number)
      - price-range-max (number)
      - property-type-filter (dropdown)
    - Submit Button:
      - id: submit-search-button
      - type: submit

---

### Template: property_details.html
- Page Title: Property Details
  - <title>: "Property Details"
  - <h1>: property['address'] (str)
- Element IDs:
  - property-details-page (Div)
  - property-address (H1)
  - property-price (Div)
  - property-description (Div)
  - property-features (Div)
  - add-to-favorites-button (Button)
  - submit-inquiry-button (Button)
- Context Variables:
  - property: Dictionary with full property details (dict)
  - agent: Dictionary with agent details (dict)
  - is_favorite: Boolean indicating if property is in favorites (bool)
- Navigation Mappings:
  - add-to-favorites-button: POST to url_for('my_favorites_page') or a dedicated favorites handler
  - submit-inquiry-button: GET redirect to url_for('property_inquiry_page') with property pre-selected
- Forms:
  - Add to Favorites Form:
    - action: url_for('my_favorites_page')
    - method: POST
    - Hidden Input: property_id
    - Submit Button: add-to-favorites-button

---

### Template: property_inquiry.html
- Page Title: Submit Property Inquiry
  - <title>: "Submit Property Inquiry"
  - <h1>: "Submit Property Inquiry"
- Element IDs:
  - inquiry-page (Div)
  - select-property (Dropdown)
  - inquiry-name (Input)
  - inquiry-email (Input email)
  - inquiry-phone (Input tel)
  - inquiry-message (Textarea)
  - submit-inquiry-button (Button)
- Context Variables:
  - properties: List of all properties (dict)
- Navigation Mappings:
  - None (users submit inquiry from this page)
- Forms:
  - Inquiry Submission Form:
    - action: url_for('property_inquiry_page')
    - method: POST
    - Inputs:
      - select-property
      - inquiry-name
      - inquiry-email
      - inquiry-phone
      - inquiry-message
    - Submit Button: submit-inquiry-button

---

### Template: my_inquiries.html
- Page Title: My Inquiries
  - <title>: "My Inquiries"
  - <h1>: "My Inquiries"
- Element IDs:
  - inquiries-page (Div)
  - inquiries-table (Table)
  - inquiry-status-filter (Dropdown)
  - delete-inquiry-button-{inquiry_id} (Button for each inquiry)
  - back-to-dashboard (Button)
- Context Variables:
  - inquiries: List of inquiry dictionaries (dict)
  - inquiry_status_filter: Current status filter string (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Filter Form:
    - action: url_for('my_inquiries_page')
    - method: POST
    - Input: inquiry-status-filter
    - Submit Button: filter-inquiries-button
  - Delete Inquiry Form(s):
    - Each inquiry row has a delete button delete-inquiry-button-{inquiry_id}
    - Submission sends POST with delete_inquiry_id

---

### Template: my_favorites.html
- Page Title: My Favorite Properties
  - <title>: "My Favorite Properties"
  - <h1>: "My Favorite Properties"
- Element IDs:
  - favorites-page (Div)
  - favorites-list (Div)
  - remove-from-favorites-button-{property_id} (Button for each favorite property)
  - view-property-button-{property_id} (Button for each favorite property)
  - back-to-dashboard (Button)
- Context Variables:
  - favorite_properties: List of property dictionaries (dict)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Remove from Favorites Form(s):
    - Each favorite property has a remove-from-favorites-button-{property_id}
    - Submission sends POST with remove_favorite_property_id

---

### Template: agents.html
- Page Title: Real Estate Agents
  - <title>: "Real Estate Agents"
  - <h1>: "Real Estate Agents"
- Element IDs:
  - agents-page (Div)
  - agents-list (Div)
  - agent-search (Input)
  - contact-agent-button-{agent_id} (Button for each agent)
  - back-to-dashboard (Button)
- Context Variables:
  - agents: List of agent dictionaries (dict)
  - search_query: Current agent search string (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Agent Search Form:
    - action: url_for('agent_directory_page')
    - method: GET
    - Input: agent-search
    - Submit Button: search-agent-button

---

### Template: locations.html
- Page Title: Featured Locations
  - <title>: "Featured Locations"
  - <h1>: "Featured Locations"
- Element IDs:
  - locations-page (Div)
  - locations-list (Div)
  - view-location-button-{location_id} (Button for each location)
  - location-sort (Dropdown)
  - back-to-dashboard (Button)
- Context Variables:
  - locations: List of location dictionaries (dict)
  - location_sort: Current sort option string (str)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Sort Form:
    - action: url_for('locations_page')
    - method: POST
    - Input: location-sort
    - Submit Button: sort-location-button

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File Path: data/properties.txt
- Fields (pipe-delimited, no header):
  - property_id
  - address
  - location
  - price
  - property_type
  - bedrooms
  - bathrooms
  - square_feet
  - description
  - agent_id
  - status
- Data Description: Stores all property listings with details including location, price, type, size, description, assigned agent, and current status.
- Example Rows:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited, no header):
  - location_id
  - location_name
  - region
  - average_price
  - property_count
  - description
- Data Description: Contains popular locations with their region, average property price, count of properties, and brief description.
- Example Rows:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited, no header):
  - inquiry_id
  - property_id
  - customer_name
  - customer_email
  - customer_phone
  - message
  - inquiry_date
  - status
- Data Description: Records of customer inquiries about properties including contact info, message, date, and current inquiry status.
- Example Rows:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited, no header):
  - favorite_id
  - property_id
  - added_date
- Data Description: Favorite properties added by users with date of addition.
- Example Rows:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited, no header):
  - agent_id
  - agent_name
  - specialization
  - email
  - phone
  - properties_sold
- Data Description: Contact details and specialties of real estate agents, including number of properties sold.
- Example Rows:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
