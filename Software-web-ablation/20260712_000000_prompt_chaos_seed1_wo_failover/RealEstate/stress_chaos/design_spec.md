# RealEstate Web Application - Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Page                | Route Path                   | HTTP Method(s) | Function Name           | Template Rendered           | Context Variables (name:type) | POST Form Data (field:type)                  |
|---------------------|------------------------------|----------------|------------------------|-----------------------------|-------------------------------|----------------------------------------------|
| Root (redirect)      | /                            | GET            | root_redirect           | - (redirects to /dashboard) | -                             | -                                            |
| Dashboard           | /dashboard                   | GET            | dashboard_page         | dashboard.html              | featured_properties:list(dict), recent_listings:list(dict) |
| Property Search      | /properties                  | GET, POST      | property_search        | property_search.html        | properties:list(dict)           | location_input:str, price_min:int (optional), price_max:int (optional), property_type:str (optional) |
| Property Details     | /properties/<int:property_id>| GET            | property_details       | property_details.html       | property:dict                 | -                                            |
| Property Inquiry    | /inquiry                    | GET, POST      | property_inquiry       | inquiry.html                | properties:list(dict)           | property_id:int, inquiry_name:str, inquiry_email:str, inquiry_phone:str, inquiry_message:str  |
| My Inquiries         | /inquiries                  | GET, POST      | my_inquiries           | inquiries.html              | inquiries:list(dict)          | inquiry_status_filter:str (optional) for filtering; delete_inquiry_id:int (optional) for delete action |
| My Favorites         | /favorites                  | GET, POST      | my_favorites           | favorites.html              | favorite_properties:list(dict), properties_dict:dict (property_id->dict) | remove_property_id:int (optional) |
| Agent Directory      | /agents                    | GET            | agent_directory        | agents.html                 | agents:list(dict)              | -                                            |
| Locations            | /locations                 | GET            | locations_page         | locations.html              | locations:list(dict)          | location_sort:str (optional) for sorting (name, count, price) |

### Route Details:

- **root_redirect**: redirects '/' to '/dashboard'

- **dashboard_page**:
  - Renders `dashboard.html`
  - Context variables:
    - `featured_properties` (list of dict): Highlighted recommended properties
    - `recent_listings` (list of dict): Recently added properties

- **property_search**:
  - GET: Renders `property_search.html` with all properties
  - POST: Accepts search filters from form:
    - `location_input` (str): search by location or city
    - `price_min` (int, optional): minimum price
    - `price_max` (int, optional): maximum price
    - `property_type` (str, optional): filter by property type (House, Apartment, Condo, Land)
  - Passes filtered `properties` (list of dict) to template

- **property_details**:
  - Expects `property_id` route parameter
  - Renders `property_details.html` with `property` (dict) full details

- **property_inquiry**:
  - GET: Renders `inquiry.html` with `properties` (list of dict) for dropdown
  - POST: Accepts inquiry form:
    - `property_id` (int)
    - `inquiry_name` (str)
    - `inquiry_email` (str)
    - `inquiry_phone` (str)
    - `inquiry_message` (str)

- **my_inquiries**:
  - GET: Renders `inquiries.html` with `inquiries` (list of dict)
  - POST: Accepts filters or deletion:
    - `inquiry_status_filter` (str): filter inquiries by status (All, Pending, Contacted, Resolved)
    - `delete_inquiry_id` (int): deletes inquiry by ID

- **my_favorites**:
  - GET: Renders `favorites.html` with:
    - `favorite_properties` (list of dict)
    - `properties_dict` (dict): mapping property_id to property dict for easy detail access
  - POST: Accepts:
    - `remove_property_id` (int): to remove property from favorites

- **agent_directory**:
  - GET: Renders agents.html with `agents` (list of dict)

- **locations_page**:
  - GET: Renders locations.html with `locations` (list of dict)
  - POST: Accepts:
    - `location_sort` (str): sorting option (By Name, By Properties Count, By Average Price)

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- **Page Title:** Real Estate Dashboard
- **Element IDs:** 
  - `dashboard-page` (Div container)
  - `featured-properties` (Div for featured properties)
  - `browse-properties-button` (Button)
  - `my-inquiries-button` (Button)
  - `my-favorites-button` (Button)
- **Context Variables:**
  - `featured_properties` (list of dict): Properties to feature
  - `recent_listings` (list of dict): Recently listed properties
- **Navigation Mappings:**
  - `browse-properties-button` -> url_for('property_search')
  - `my-inquiries-button` -> url_for('my_inquiries')
  - `my-favorites-button` -> url_for('my_favorites')
- **Forms:** None

---

### 2. property_search.html
- **Page Title:** Property Search
- **Element IDs:**
  - `search-page` (Div container)
  - `location-input` (Input text)
  - `price-range-min` (Input number)
  - `price-range-max` (Input number)
  - `property-type-filter` (Dropdown with options: House, Apartment, Condo, Land)
  - `properties-grid` (Div container for property cards)
  - Dynamic Buttons:
    - `view-property-button-{property_id}` (Button to view details for each property)
- **Context Variables:**
  - `properties` (list of dict): Property data
- **Navigation Mappings:**
  - Each `view-property-button-{property_id}` -> url_for('property_details', property_id=property_id)
- **Forms:**
  - Search form with inputs: `location-input`, `price-range-min`, `price-range-max`, `property-type-filter`
  - Form POST action to url_for('property_search')

---

### 3. property_details.html
- **Page Title:** Property Details
- **Element IDs:**
  - `property-details-page` (Div container)
  - `property-address` (H1)
  - `property-price` (Div)
  - `property-description` (Div)
  - `property-features` (Div)
  - `add-to-favorites-button` (Button)
  - `submit-inquiry-button` (Button)
- **Context Variables:**
  - `property` (dict): full property information
- **Navigation Mappings:** None required
- **Forms:**
  - POST form for adding to favorites triggered via `add-to-favorites-button`
  - POST form to submit inquiry triggered via `submit-inquiry-button`

---

### 4. inquiry.html
- **Page Title:** Submit Property Inquiry
- **Element IDs:**
  - `inquiry-page` (Div container)
  - `select-property` (Dropdown listing properties by address)
  - `inquiry-name` (Input text)
  - `inquiry-email` (Input email)
  - `inquiry-phone` (Input tel)
  - `inquiry-message` (Textarea)
  - `submit-inquiry-button` (Button)
- **Context Variables:**
  - `properties` (list of dict): Properties for dropdown
- **Navigation Mappings:** None
- **Forms:**
  - Inquiry submission form with all inputs named accordingly, POST action to url_for('property_inquiry')

---

### 5. inquiries.html
- **Page Title:** My Inquiries
- **Element IDs:**
  - `inquiries-page` (Div container)
  - `inquiries-table` (Table for inquiries)
  - `inquiry-status-filter` (Dropdown with options: All, Pending, Contacted, Resolved)
  - Dynamic Buttons:
    - `delete-inquiry-button-{inquiry_id}` (Button to delete inquiry)
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `inquiries` (list of dict): Inquiry data
- **Navigation Mappings:**
  - `back-to-dashboard` -> url_for('dashboard_page')
- **Forms:**
  - Filter form with `inquiry-status-filter` input, POST action to url_for('my_inquiries')
  - Delete inquiry forms or AJAX actions triggered by delete buttons

---

### 6. favorites.html
- **Page Title:** My Favorite Properties
- **Element IDs:**
  - `favorites-page` (Div container)
  - `favorites-list` (Div listing favorite properties)
  - Dynamic Buttons:
    - `remove-from-favorites-button-{property_id}` (Button to remove favorite)
    - `view-property-button-{property_id}` (Button to view property details)
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `favorite_properties` (list of dict): Favorite properties data
  - `properties_dict` (dict): Property details mapped by property_id
- **Navigation Mappings:**
  - `back-to-dashboard` -> url_for('dashboard_page')
  - Each `view-property-button-{property_id}` -> url_for('property_details', property_id=property_id)
- **Forms:**
  - Form or AJAX for removing favorites via buttons

---

### 7. agents.html
- **Page Title:** Real Estate Agents
- **Element IDs:**
  - `agents-page` (Div container)
  - `agents-list` (Div listing agents)
  - `agent-search` (Input text for searching agents)
  - Dynamic Buttons:
    - `contact-agent-button-{agent_id}` (Button to contact agent)
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `agents` (list of dict): Agent data
- **Navigation Mappings:**
  - `back-to-dashboard` -> url_for('dashboard_page')
- **Forms:**
  - Search form with `agent-search` input

---

### 8. locations.html
- **Page Title:** Featured Locations
- **Element IDs:**
  - `locations-page` (Div container)
  - `locations-list` (Div listing locations)
  - Dynamic Buttons:
    - `view-location-button-{location_id}` (Button to view location properties)
  - `location-sort` (Dropdown with options: By Name, By Properties Count, By Average Price)
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `locations` (list of dict): Location data
- **Navigation Mappings:**
  - `back-to-dashboard` -> url_for('dashboard_page')
  - Each `view-location-button-{location_id}` -> # (assumed to route to filtered property_search; not specified in requirements)
- **Forms:**
  - Sorting form with `location-sort` dropdown with POST action to url_for('locations_page')

---

## Section 3: Data File Schemas (Backend)

### 1. Properties Data
- **File Path:** data/properties.txt
- **Fields (pipe-delimited):**
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
- **Description:** Stores all property listings with details including location, price, type, features, agent, and availability status.
- **Example Rows:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. Locations Data
- **File Path:** data/locations.txt
- **Fields (pipe-delimited):**
  - location_id
  - location_name
  - region
  - average_price
  - property_count
  - description
- **Description:** Contains popular location data with statistics.
- **Example Rows:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. Property Inquiries Data
- **File Path:** data/inquiries.txt
- **Fields (pipe-delimited):**
  - inquiry_id
  - property_id
  - customer_name
  - customer_email
  - customer_phone
  - message
  - inquiry_date
  - status
- **Description:** Stores all inquiries submitted for properties with customer contact info and current status.
- **Example Rows:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. Favorite Properties Data
- **File Path:** data/favorites.txt
- **Fields (pipe-delimited):**
  - favorite_id
  - property_id
  - added_date
- **Description:** Lists properties marked as favorites by users.
- **Example Rows:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. Real Estate Agents Data
- **File Path:** data/agents.txt
- **Fields (pipe-delimited):**
  - agent_id
  - agent_name
  - specialization
  - email
  - phone
  - properties_sold
- **Description:** Stores real estate agent information including contact and specialization.
- **Example Rows:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
