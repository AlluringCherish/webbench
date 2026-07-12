# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                               | HTTP Method | Function Name             | Template Rendered          | Route Parameters              | Context Variables Passed to Template (name : type)                                           | POST Form Data Expected (name : type)                                                                                   |
|-----------------------------------------|-------------|--------------------------|----------------------------|-------------------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| /                                       | GET         | root_redirect             | Redirects to /dashboard    | None                          | None                                                                                         | None                                                                                                                     |
| /dashboard                             | GET         | dashboard                | dashboard.html             | None                          | featured_properties : list of dict                                                         | None                                                                                                                     |
| /properties                           | GET         | property_search          | property_search.html       | None                          | properties : list of dict                                                                   | None                                                                                                                     |
| /property/<int:property_id>            | GET         | property_details         | property_details.html      | property_id (int)             | property : dict                                                                             | None                                                                                                                     |
| /property/<int:property_id>/add_to_favorites | POST        | add_to_favorites         | Redirect or JSON response  | property_id (int)             | None                                                                                         | None                                                                                                                     |
| /property/<int:property_id>/inquiry    | GET         | property_inquiry_form    | property_inquiry.html      | property_id (int)             | properties : list of dict (for dropdown), selected_property : dict                         | None                                                                                                                     |
| /property/<int:property_id>/inquiry    | POST        | submit_inquiry           | Redirect or JSON response  | property_id (int)             | None                                                                                         | customer_name : str, customer_email : str, customer_phone : str, message : str                                            |
| /inquiries                           | GET         | my_inquiries             | my_inquiries.html          | None                          | inquiries : list of dict, inquiry_status_filter_values : list of str                         | None                                                                                                                     |
| /inquiries/delete/<int:inquiry_id>     | POST        | delete_inquiry           | Redirect or JSON response  | inquiry_id (int)              | None                                                                                         | None                                                                                                                     |
| /favorites                           | GET         | my_favorites             | my_favorites.html          | None                          | favorite_properties : list of dict                                                        | None                                                                                                                     |
| /favorites/remove/<int:property_id>    | POST        | remove_from_favorites    | Redirect or JSON response  | property_id (int)             | None                                                                                         | None                                                                                                                     |
| /agents                             | GET         | agent_directory          | agents.html                | None                          | agents : list of dict                                                                       | None                                                                                                                     |
| /locations                          | GET         | locations_page           | locations.html             | None                          | locations : list of dict                                                                    | None                                                                                                                     |

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- **Page Title**: Real Estate Dashboard
- **Element IDs**:
  - `dashboard-page` (Div) - Container for the dashboard page
  - `featured-properties` (Div) - Display of featured property recommendations
  - `browse-properties-button` (Button) - Navigates to property search page
  - `my-inquiries-button` (Button) - Navigates to inquiries page
  - `my-favorites-button` (Button) - Navigates to favorites page
- **Context Variables**:
  - `featured_properties` (list of dict): List of featured property summaries (id, address, price, image URL, etc.)
- **Navigation Mappings**:
  - `browse-properties-button`: `url_for('property_search')`
  - `my-inquiries-button`: `url_for('my_inquiries')`
  - `my-favorites-button`: `url_for('my_favorites')`
- **Forms/Buttons**:
  - Buttons trigger client-side navigation (no forms)

### 2. property_search.html
- **Page Title**: Property Search
- **Element IDs**:
  - `search-page` (Div) - Container for the search page
  - `location-input` (Input) - Search by location/city
  - `price-range-min` (Input - number) - Minimum price filter
  - `price-range-max` (Input - number) - Maximum price filter
  - `property-type-filter` (Dropdown) - Filter by type: House, Apartment, Condo, Land
  - `properties-grid` (Div) - Grid displaying property cards
  - `view-property-button-{property_id}` (Button) - View details for each property
- **Context Variables**:
  - `properties` (list of dict): List of property data including `property_id`, `address`, `location`, `price`, `property_type`, `bedrooms`, `bathrooms`, `square_feet`, `image_url` (if any)
- **Navigation Mappings**:
  - `view-property-button-{property_id}`: `url_for('property_details', property_id=property_id)`
  - `browse-properties-button` (if present): `url_for('property_search')`
- **Forms/Buttons**:
  - Search filters are client-side controls; submission affects listing display
  - Buttons for viewing properties are links or buttons triggering GET to property details

### 3. property_details.html
- **Page Title**: Property Details
- **Element IDs**:
  - `property-details-page` (Div) - Container for details
  - `property-address` (H1) - Property address
  - `property-price` (Div) - Property price
  - `property-description` (Div) - Description
  - `property-features` (Div) - Beds, baths, square footage
  - `add-to-favorites-button` (Button) - Add property to favorites
  - `submit-inquiry-button` (Button) - Navigate to inquiry page
- **Context Variables**:
  - `property` (dict): Full property details with keys as per properties.txt fields
- **Navigation Mappings**:
  - `add-to-favorites-button`: POST to `url_for('add_to_favorites', property_id=property['property_id'])`
  - `submit-inquiry-button`: GET to `url_for('property_inquiry_form', property_id=property['property_id'])`

### 4. property_inquiry.html
- **Page Title**: Submit Property Inquiry
- **Element IDs**:
  - `inquiry-page` (Div) - Container for inquiry page
  - `select-property` (Dropdown) - Select property for inquiry
  - `inquiry-name` (Input) - Customer name
  - `inquiry-email` (Input - email) - Customer email
  - `inquiry-phone` (Input - tel) - Customer phone
  - `inquiry-message` (Textarea) - Inquiry message
  - `submit-inquiry-button` (Button) - Submit inquiry
- **Context Variables**:
  - `properties` (list of dict): List of properties for dropdown
  - `selected_property` (dict): The currently selected property details
- **Navigation Mappings**:
  - On form submission, POST to `url_for('submit_inquiry', property_id=selected_property['property_id'])`
- **Forms/Buttons**:
  - Form with inputs: `inquiry-name`, `inquiry-email`, `inquiry-phone`, `inquiry-message`
  - Submit button with ID `submit-inquiry-button`

### 5. my_inquiries.html
- **Page Title**: My Inquiries
- **Element IDs**:
  - `inquiries-page` (Div) - Container
  - `inquiries-table` (Table) - List inquiries
  - `inquiry-status-filter` (Dropdown) - Filter by status
  - `delete-inquiry-button-{inquiry_id}` (Button) - Delete inquiry
  - `back-to-dashboard` (Button) - Go back to dashboard
- **Context Variables**:
  - `inquiries` (list of dict): Inquiry records
  - `inquiry_status_filter_values` (list of str): Status filter options
- **Navigation Mappings**:
  - `back-to-dashboard`: `url_for('dashboard')`
- **Forms/Buttons**:
  - Each delete button posts to `url_for('delete_inquiry', inquiry_id=inquiry_id)`

### 6. my_favorites.html
- **Page Title**: My Favorite Properties
- **Element IDs**:
  - `favorites-page` (Div) - Container
  - `favorites-list` (Div) - List of favorite properties
  - `remove-from-favorites-button-{property_id}` (Button) - Remove from favorites
  - `view-property-button-{property_id}` (Button) - View property details
  - `back-to-dashboard` (Button) - Go back to dashboard
- **Context Variables**:
  - `favorite_properties` (list of dict): Favorite property details
- **Navigation Mappings**:
  - `back-to-dashboard`: `url_for('dashboard')`
- **Forms/Buttons**:
  - Remove button posts to `url_for('remove_from_favorites', property_id=property_id)`
  - View button links to `url_for('property_details', property_id=property_id)`

### 7. agents.html
- **Page Title**: Real Estate Agents
- **Element IDs**:
  - `agents-page` (Div) - Container
  - `agents-list` (Div) - List of agents
  - `agent-search` (Input) - Search agents by name
  - `contact-agent-button-{agent_id}` (Button) - Contact agent
  - `back-to-dashboard` (Button) - Go back to dashboard
- **Context Variables**:
  - `agents` (list of dict): Agent details
- **Navigation Mappings**:
  - `back-to-dashboard`: `url_for('dashboard')`
- **Forms/Buttons**:
  - Contact agent buttons to be linked or initiate communication (no backend action specified)

### 8. locations.html
- **Page Title**: Featured Locations
- **Element IDs**:
  - `locations-page` (Div) - Container
  - `locations-list` (Div) - List of locations
  - `view-location-button-{location_id}` (Button) - View properties in location
  - `location-sort` (Dropdown) - Sort locations
  - `back-to-dashboard` (Button) - Go back to dashboard
- **Context Variables**:
  - `locations` (list of dict): Location information
- **Navigation Mappings**:
  - `back-to-dashboard`: `url_for('dashboard')`
- **Forms/Buttons**:
  - Sorting via dropdown triggers client-side update or server request
  - View buttons link to `url_for('property_search')` with filter for that location (implementation detail)

---

## Section 3: Data File Schemas (Backend)

### 1. data/properties.txt
- **Fields (pipe-delimited order):**
  - property_id (int)
  - address (str)
  - location (str)
  - price (float)
  - property_type (str) (House, Apartment, Condo, Land)
  - bedrooms (int)
  - bathrooms (float)
  - square_feet (int)
  - description (str)
  - agent_id (int)
  - status (str) (Available, Sold, etc.)
- **Description:** Stores all property listings details.
- **Example Rows:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. data/locations.txt
- **Fields (pipe-delimited order):**
  - location_id (int)
  - location_name (str)
  - region (str)
  - average_price (float)
  - property_count (int)
  - description (str)
- **Description:** Stores popular location info used for filtering and display.
- **Example Rows:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. data/inquiries.txt
- **Fields (pipe-delimited order):**
  - inquiry_id (int)
  - property_id (int)
  - customer_name (str)
  - customer_email (str)
  - customer_phone (str)
  - message (str)
  - inquiry_date (str) (ISO 8601 date YYYY-MM-DD)
  - status (str) (Pending, Contacted, Resolved)
- **Description:** Stores all submitted property inquiries.
- **Example Rows:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. data/favorites.txt
- **Fields (pipe-delimited order):**
  - favorite_id (int)
  - property_id (int)
  - added_date (str) (ISO 8601 date YYYY-MM-DD)
- **Description:** Stores user favorite properties.
- **Example Rows:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. data/agents.txt
- **Fields (pipe-delimited order):**
  - agent_id (int)
  - agent_name (str)
  - specialization (str)
  - email (str)
  - phone (str)
  - properties_sold (int)
- **Description:** Stores real estate agent details.
- **Example Rows:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```
