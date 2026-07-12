# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | HTTP Method | Function Name           | Template Rendered         | Route Parameters         | Context Variables Passed to Template (name : type) | POST Form Data Expected (name : type)                                  |
|----------------------------|-------------|------------------------|---------------------------|--------------------------|----------------------------------------------------|---------------------------------------------------------------------------|
| /                          | GET         | root_redirect           | -                         | -                        | -                                                  | -                                                                         |
| /dashboard                 | GET         | dashboard              | dashboard.html            | -                        | featured_properties : list(dict), recent_listings : list(dict)          | -                                                                         |
| /search                   | GET         | property_search        | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict   | -                                                                         |
| /search                   | POST        | property_search        | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict   | location_input : str, price_range_min : float, price_range_max : float, property_type_filter : str |
| /property/<int:property_id> | GET         | property_details       | property_details.html     | property_id : int        | property : dict                                                         | -                                                                         |
| /inquiry                  | GET         | property_inquiry       | inquiry.html              | -                        | properties : list(dict)                                                 | -                                                                         |
| /inquiry                  | POST        | submit_inquiry         | inquiries.html            | -                        | inquiries : list(dict)                                                  | select_property : int (property_id), inquiry_name : str, inquiry_email : str, inquiry_phone : str, inquiry_message : str |
| /inquiries                | GET         | my_inquiries           | inquiries.html            | -                        | inquiries : list(dict)                                                  | -                                                                         |
| /inquiries/filter/<status> | GET         | filter_inquiries       | inquiries.html            | status : str             | inquiries : list(dict)                                                  | -                                                                         |
| /inquiries/delete/<int:inquiry_id> | POST        | delete_inquiry         | inquiries.html            | inquiry_id : int          | inquiries : list(dict)                                                  | -                                                                         |
| /favorites                | GET         | my_favorites           | favorites.html            | -                        | favorite_properties : list(dict)                                       | -                                                                         |
| /favorites/add/<int:property_id> | POST        | add_to_favorites       | favorites.html            | property_id : int         | favorite_properties : list(dict)                                       | -                                                                         |
| /favorites/remove/<int:property_id> | POST        | remove_from_favorites  | favorites.html            | property_id : int         | favorite_properties : list(dict)                                       | -                                                                         |
| /agents                   | GET         | agents_directory       | agents.html               | -                        | agents : list(dict)                                                    | -                                                                         |
| /agents/search            | POST        | search_agents          | agents.html               | -                        | agents : list(dict)                                                    | agent_search : str                                                        |
| /locations                | GET         | locations_page         | locations.html            | -                        | locations : list(dict)                                                | -                                                                         |
| /locations/sort           | POST        | sort_locations         | locations.html            | -                        | locations : list(dict)                                                | location_sort : str (values: "By Name", "By Properties Count", "By Average Price") |

**Notes:**
- The root `/` route redirects to `/dashboard`.
- POST routes for adding/removing favorites and inquiry submissions process the input and redirect back to their respective pages with updated context.
- Filtering of inquiries by status and sorting locations are handled via specific GET or POST routes.

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- **Page Title**: Real Estate Dashboard
- **Element IDs:**
  - dashboard-page
  - featured-properties
  - browse-properties-button
  - my-inquiries-button
  - my-favorites-button
- **Context Variables:**
  - featured_properties : List of dictionaries with property summary data (list(dict))
  - recent_listings : List of dictionaries with recent property listings (list(dict))
- **Navigation Mappings (url_for function names):**
  - browse-properties-button -> property_search
  - my-inquiries-button -> my_inquiries
  - my-favorites-button -> my_favorites
- **Forms:** None

---

### 2. search.html
- **Page Title**: Property Search
- **Element IDs:**
  - search-page
  - location-input
  - price-range-min
  - price-range-max
  - property-type-filter
  - properties-grid
  - view-property-button-{{property.property_id}} (dynamic per property)
- **Context Variables:**
  - properties : List of property dicts (list(dict))
  - locations : List of location dicts (list(dict))
  - filter_options : Dict containing current filter selections
- **Navigation Mappings:**
  - view-property-button-{{property.property_id}} -> property_details(property_id=property.property_id)
- **Forms:**
  - Search filter form with inputs:
    - location-input (text)
    - price-range-min (number)
    - price-range-max (number)
    - property-type-filter (dropdown: House, Apartment, Condo, Land)
  - Submit button triggers POST on /search

---

### 3. property_details.html
- **Page Title**: Property Details
- **Element IDs:**
  - property-details-page
  - property-address
  - property-price
  - property-description
  - property-features
  - add-to-favorites-button
  - submit-inquiry-button
- **Context Variables:**
  - property : Dictionary containing all property details
- **Navigation Mappings:**
  - add-to-favorites-button -> add_to_favorites(property_id=property.property_id) (POST form)
  - submit-inquiry-button -> property_inquiry (GET to open inquiry page)
- **Forms:**
  - Add to favorites form (POST) with button add-to-favorites-button
  - Submit inquiry button triggers GET navigation

---

### 4. inquiry.html
- **Page Title**: Submit Property Inquiry
- **Element IDs:**
  - inquiry-page
  - select-property
  - inquiry-name
  - inquiry-email
  - inquiry-phone
  - inquiry-message
  - submit-inquiry-button
- **Context Variables:**
  - properties : List of property dicts for dropdown
- **Navigation Mappings:** None
- **Forms:**
  - Inquiry submission form (POST) with inputs:
    - select-property (dropdown)
    - inquiry-name (text)
    - inquiry-email (email)
    - inquiry-phone (tel)
    - inquiry-message (textarea)
  - submit-inquiry-button submits form

---

### 5. inquiries.html
- **Page Title**: My Inquiries
- **Element IDs:**
  - inquiries-page
  - inquiries-table
  - inquiry-status-filter
  - delete-inquiry-button-{{inquiry.inquiry_id}} (dynamic)
  - back-to-dashboard
- **Context Variables:**
  - inquiries : List of inquiry dicts
- **Navigation Mappings:**
  - back-to-dashboard -> dashboard
- **Forms:**
  - Filter by inquiry status (dropdown inquiry-status-filter) triggers GET on /inquiries/filter/<status>
  - Delete inquiry buttons submit POST to /inquiries/delete/<inquiry_id>

---

### 6. favorites.html
- **Page Title**: My Favorite Properties
- **Element IDs:**
  - favorites-page
  - favorites-list
  - remove-from-favorites-button-{{property.property_id}} (dynamic)
  - view-property-button-{{property.property_id}} (dynamic)
  - back-to-dashboard
- **Context Variables:**
  - favorite_properties : List of property dicts
- **Navigation Mappings:**
  - back-to-dashboard -> dashboard
  - view-property-button-{{property.property_id}} -> property_details(property_id=property.property_id)
- **Forms:**
  - Remove from favorites buttons POST to /favorites/remove/<property_id>

---

### 7. agents.html
- **Page Title**: Real Estate Agents
- **Element IDs:**
  - agents-page
  - agents-list
  - agent-search
  - contact-agent-button-{{agent.agent_id}} (dynamic)
  - back-to-dashboard
- **Context Variables:**
  - agents : List of agent dicts
- **Navigation Mappings:**
  - back-to-dashboard -> dashboard
- **Forms:**
  - Agent search form POST to /agents/search with input agent-search

---

### 8. locations.html
- **Page Title**: Featured Locations
- **Element IDs:**
  - locations-page
  - locations-list
  - view-location-button-{{location.location_id}} (dynamic)
  - location-sort
  - back-to-dashboard
- **Context Variables:**
  - locations : List of location dicts
- **Navigation Mappings:**
  - back-to-dashboard -> dashboard
- **Forms:**
  - Location sort form POST to /locations/sort with dropdown location-sort

---

## Section 3: Data File Schemas (Backend)

### 1. Data File: data/properties.txt
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
- **Description:** Contains all property listings with details and status.
- **Example rows:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 2. Data File: data/locations.txt
- **Fields (pipe-delimited):**
  - location_id
  - location_name
  - region
  - average_price
  - property_count
  - description
- **Description:** Stores location metadata including counts and average prices.
- **Example rows:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3. Data File: data/inquiries.txt
- **Fields (pipe-delimited):**
  - inquiry_id
  - property_id
  - customer_name
  - customer_email
  - customer_phone
  - message
  - inquiry_date
  - status
- **Description:** Records all inquiries made for properties, with contact and status.
- **Example rows:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 4. Data File: data/favorites.txt
- **Fields (pipe-delimited):**
  - favorite_id
  - property_id
  - added_date
- **Description:** Stores users' favorite properties by property ID and date added.
- **Example rows:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 5. Data File: data/agents.txt
- **Fields (pipe-delimited):**
  - agent_id
  - agent_name
  - specialization
  - email
  - phone
  - properties_sold
- **Description:** Contains information about real estate agents including contact and sales count.
- **Example rows:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```
