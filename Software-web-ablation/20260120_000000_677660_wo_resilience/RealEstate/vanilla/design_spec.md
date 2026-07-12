# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | HTTP Method | Function Name           | Template Rendered         | Route Parameters         | Context Variables Passed to Template (name : type) | POST Form Data Expected (name : type)                                  |
|----------------------------|-------------|------------------------|---------------------------|--------------------------|----------------------------------------------------|---------------------------------------------------------------------------|
| /                          | GET         | root_redirect           | -                         | -                        | -                                                  | -                                                                         |
| /dashboard                 | GET         | dashboard              | dashboard.html            | -                        | featured_properties : list(dict), recent_listings : list(dict)          | -                                                                         |
| /search                   | GET         | property_search        | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict  | -                                                                         |
| /search                   | POST        | property_search        | search.html               | -                        | properties : list(dict), locations : list(dict), filter_options : dict  | location_input : str, price_range_min : float, price_range_max : float, property_type_filter : str |
| /property/<int:property_id> | GET         | property_details       | property_details.html     | property_id : int        | property : dict                                                         | -                                                                         |
| /inquiry                  | GET         | property_inquiry       | inquiry.html              | -                        | properties : list(dict)                                                 | -                                                                         |
| /inquiry                  | POST        | submit_inquiry         | inquiries.html            | -                        | inquiries : list(dict)                                                  | select_property : int (property_id), inquiry_name : str, inquiry_email : str, inquiry_phone : str, inquiry_message : str |
| /inquiries                | GET         | my_inquiries           | inquiries.html            | -                        | inquiries : list(dict), status_filter : str                           | -                                                                         |
| /inquiries/filter         | POST        | filter_inquiries       | inquiries.html            | -                        | inquiries : list(dict), status_filter : str                           | inquiry_status_filter : str                                               |
| /inquiries/delete/<int:inquiry_id> | POST        | delete_inquiry        | inquiries.html            | inquiry_id : int         | inquiries : list(dict), status_filter : str                           | -                                                                         |
| /favorites                | GET         | my_favorites           | favorites.html            | -                        | favorites : list(dict), properties : dict                             | -                                                                         |
| /favorites/add/<int:property_id>    | POST        | add_to_favorites       | favorites.html            | property_id : int        | favorites : list(dict), properties : dict                             | -                                                                         |
| /favorites/remove/<int:property_id> | POST        | remove_from_favorites  | favorites.html            | property_id : int        | favorites : list(dict), properties : dict                             | -                                                                         |
| /agents                   | GET         | agent_directory        | agents.html               | -                        | agents : list(dict)                                                    | -                                                                         |
| /agents/search            | POST        | search_agents          | agents.html               | -                        | agents : list(dict)                                                    | agent_search : str                                                        |
| /locations                | GET         | locations_page         | locations.html            | -                        | locations : list(dict), sort_option : str                            | -                                                                         |
| /locations/sort           | POST        | sort_locations         | locations.html            | -                        | locations : list(dict), sort_option : str                            | location_sort : str                                                       |

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page
  - featured-properties
  - browse-properties-button
  - my-inquiries-button
  - my-favorites-button
- Context Variables:
  - featured_properties : list(dict) — List of featured property dictionaries with keys: property_id (int), address (str), location (str), price (float), beds (int), baths (float)
  - recent_listings : list(dict) — Recent properties similar structure
- Navigation Mappings:
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('my_inquiries')
  - my-favorites-button: url_for('my_favorites')
- Forms: None

### 2. search.html
- Page Title: Property Search
- Element IDs:
  - search-page
  - location-input
  - price-range-min
  - price-range-max
  - property-type-filter
  - properties-grid
  - view-property-button-{{property.property_id}} (dynamic for each property)
- Context Variables:
  - properties : list(dict) — Properties to display with keys matching properties.txt fields
  - locations : list(dict) — Locations for reference/filtering
  - filter_options : dict — Current filter state for location_input (str), min_price (float), max_price (float), property_type (str)
- Navigation Mappings:
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)
- Forms:
  - Search Form:
    - Inputs:
      - location-input (text)
      - price-range-min (number)
      - price-range-max (number)
      - property-type-filter (dropdown)
    - Submit Button ID: search-submit-button
    - Form Action: url_for('property_search') method POST

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page
  - property-address
  - property-price
  - property-description
  - property-features
  - add-to-favorites-button
  - submit-inquiry-button
- Context Variables:
  - property : dict — Detailed property info matching properties.txt fields
- Navigation Mappings:
  - add-to-favorites-button: url_for('add_to_favorites', property_id=property.property_id) (form POST)
  - submit-inquiry-button: url_for('property_inquiry')
- Forms:
  - Add to Favorites:
    - Button ID: add-to-favorites-button
    - Action: url_for('add_to_favorites', property_id=property.property_id) POST
  - Submit Inquiry Button is a navigation button (GET to inquiry page)

### 4. inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page
  - select-property
  - inquiry-name
  - inquiry-email
  - inquiry-phone
  - inquiry-message
  - submit-inquiry-button
- Context Variables:
  - properties : list(dict) — All properties for dropdown selection
- Navigation Mappings:
  - form action: url_for('submit_inquiry') POST
- Forms:
  - Inquiry Submission:
    - select-property (dropdown)
    - inquiry-name (text input)
    - inquiry-email (email input)
    - inquiry-phone (tel input)
    - inquiry-message (textarea)
    - submit-inquiry-button (submit button)

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page
  - inquiries-table
  - inquiry-status-filter
  - back-to-dashboard
  - delete-inquiry-button-{{inquiry.inquiry_id}} (dynamic for each inquiry)
- Context Variables:
  - inquiries : list(dict) — List of inquiries
  - status_filter : str — Current status filter selected
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')
  - delete-inquiry buttons: url_for('delete_inquiry', inquiry_id=inquiry_id) POST
  - filter form action: url_for('filter_inquiries') POST
- Forms:
  - Status Filter Form:
    - inquiry-status-filter (dropdown)
    - submit button ID: filter-inquiries-submit
  - Delete Inquiry buttons are individual POST forms per inquiry

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page
  - favorites-list
  - remove-from-favorites-button-{{property.property_id}} (dynamic)
  - view-property-button-{{property.property_id}} (dynamic)
  - back-to-dashboard
- Context Variables:
  - favorites : list(dict) — List of favorite property dicts
  - properties : dict — Mapping property_id to property dict
- Navigation Mappings:
  - remove-from-favorites-button: url_for('remove_from_favorites', property_id=property.property_id) POST
  - view-property-button: url_for('property_details', property_id=property.property_id)
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Remove from Favorites buttons are forms with POST method

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page
  - agents-list
  - agent-search
  - contact-agent-button-{{agent.agent_id}} (dynamic)
  - back-to-dashboard
- Context Variables:
  - agents : list(dict) — List of agents
- Navigation Mappings:
  - contact-agent-button: Could link to an email or contact form (outside current scope)
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Agent Search:
    - agent-search (input)
    - submit button ID: agent-search-submit
    - form action: url_for('search_agents') POST

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page
  - locations-list
  - view-location-button-{{location.location_id}} (dynamic)
  - location-sort
  - back-to-dashboard
- Context Variables:
  - locations : list(dict) — List of locations
  - sort_option : str — Current sort option selected
- Navigation Mappings:
  - view-location-button: url_for('property_search') with location filter (or dedicated route if implemented)
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Sort Locations:
    - location-sort (dropdown)
    - submit button ID: location-sort-submit
    - form action: url_for('sort_locations') POST

---

## Section 3: Data File Schemas (Backend)

### 1. data/properties.txt
- Fields (pipe-delimited):
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description:
  Contains all property listings with details including location, price, type, features, description, associated agent, and availability status.
- Example Rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### 2. data/locations.txt
- Fields (pipe-delimited):
  location_id|location_name|region|average_price|property_count|description
- Description:
  Lists all popular locations with meta info such as region, average property price, total properties available, and description.
- Example Rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

### 3. data/inquiries.txt
- Fields (pipe-delimited):
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description:
  Stores customer inquiries for properties with contact info, message content, inquiry date, and current status.
- Example Rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### 4. data/favorites.txt
- Fields (pipe-delimited):
  favorite_id|property_id|added_date
- Description:
  Maintains records of properties marked as favorites along with the date they were added.
- Example Rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

### 5. data/agents.txt
- Fields (pipe-delimited):
  agent_id|agent_name|specialization|email|phone|properties_sold
- Description:
  Contains details of real estate agents including their specialization, contact information, and sales record.
- Example Rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
