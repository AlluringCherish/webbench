# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                  | HTTP Method(s) | Function Name            | Template Rendered          | Context Variables (name:type)                                                                        | Expected Form Data (POST)                                      |
|-----------------------------|----------------|--------------------------|----------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| /                           | GET            | root_redirect             | Redirects to '/dashboard'  | None                                                                                               | None                                                          |
| /dashboard                  | GET            | dashboard                | dashboard.html             | featured_properties:list(dict), recent_listings:list(dict)                                         | None                                                          |
| /search                    | GET            | property_search          | search.html                | properties:list(dict), location_filter:str, price_min:int or None, price_max:int or None, property_type_filter:str or None   | None                                                          |
| /property/<int:property_id>| GET            | property_details         | property_details.html      | property:dict, agent:dict                                                                            | None                                                          |
| /property/<int:property_id>/inquiry | GET      | property_inquiry_form    | inquiry.html               | properties:list(dict), selected_property_id:int                                                    | None                                                          |
| /property/<int:property_id>/inquiry | POST     | submit_property_inquiry  | Redirects to inquiries page | Form Data: customer_name:str, customer_email:str, customer_phone:str, inquiry_message:str          | customer_name, customer_email, customer_phone, inquiry_message |
| /inquiries                 | GET            | my_inquiries             | inquiries.html             | inquiries:list(dict), status_filter:str                                                              | None                                                          |
| /inquiries/delete/<int:inquiry_id> | POST    | delete_inquiry           | Redirect back to inquiries page | inquiry_id:int                                                                                     | None                                                          |
| /favorites                 | GET            | my_favorites             | favorites.html             | favorites:list(dict), properties_lookup:dict(property_id:int->dict)                                | None                                                          |
| /favorites/add/<int:property_id> | POST      | add_to_favorites         | Redirect back to favorites page | property_id:int                                                                                   | None                                                          |
| /favorites/remove/<int:property_id> | POST   | remove_from_favorites    | Redirect back to favorites page | property_id:int                                                                                   | None                                                          |
| /agents                   | GET            | agent_directory          | agents.html                | agents:list(dict)                                                                                   | None                                                          |
| /locations                | GET            | locations_page           | locations.html             | locations:list(dict)                                                                               | None                                                          |

### Notes on Context Variables:
- featured_properties: List of property dicts with keys matching `properties.txt` fields.
- recent_listings: List of property dicts similarly structured.
- properties: List of all properties filtered by search.
- property: Single property dict for details.
- agent: Dict of a single agent corresponding to property.
- inquiries: List of inquiry dicts matching `inquiries.txt` fields.
- favorites: List of favorite dicts from `favorites.txt`.
- properties_lookup: Dict mapping property_id to property dict for quick access.
- agents: List of agent dicts from `agents.txt`.
- locations: List of location dicts from `locations.txt`.
- status_filter, property_type_filter, location_filter: Strings representing current filter values.

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
  - featured_properties (list of dict): Featured property recommendations
  - recent_listings (list of dict): Recent property listings
- Navigation Mappings:
  - browse-properties-button -> url_for('property_search')
  - my-inquiries-button -> url_for('my_inquiries')
  - my-favorites-button -> url_for('my_favorites')
- Forms/Buttons:
  - browse-properties-button (button)
  - my-inquiries-button (button)
  - my-favorites-button (button)

---

### 2. search.html
- Page Title: Property Search
- Element IDs:
  - search-page
  - location-input
  - price-range-min
  - price-range-max
  - property-type-filter
  - properties-grid
  - view-property-button-{property_id} (dynamic per property)
- Context Variables:
  - properties (list of dict): Properties to display
  - location_filter (str): Current location filter
  - price_min (int or None): Current minimum price filter
  - price_max (int or None): Current maximum price filter
  - property_type_filter (str or None): Current property type filter
- Navigation Mappings:
  - view-property-button-{property_id} -> url_for('property_details', property_id=property_id)
- Forms/Buttons:
  - location-input (input text)
  - price-range-min (number input)
  - price-range-max (number input)
  - property-type-filter (dropdown)
  - view-property-button-{property_id} (button)

---

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
  - property (dict): Property details
  - agent (dict): Agent details
- Navigation Mappings:
  - add-to-favorites-button -> POST to url_for('add_to_favorites', property_id=property['property_id'])
  - submit-inquiry-button -> url_for('property_inquiry_form', property_id=property['property_id']) [GET]
- Forms/Buttons:
  - add-to-favorites-button (button, submits POST)
  - submit-inquiry-button (button, GET link)

---

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
  - properties (list of dict): Properties for inquiry selection
  - selected_property_id (int): Currently selected property
- Navigation Mappings:
  - Form POST action to url_for('submit_property_inquiry', property_id=selected_property_id)
- Forms:
  - select-property (dropdown, required)
  - inquiry-name (input text, required)
  - inquiry-email (input email, required)
  - inquiry-phone (input tel, optional)
  - inquiry-message (textarea, required)
  - submit-inquiry-button (button submit)

---

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page
  - inquiries-table
  - inquiry-status-filter
  - delete-inquiry-button-{inquiry_id} (dynamic per inquiry)
  - back-to-dashboard
- Context Variables:
  - inquiries (list of dict): List of inquiries to display
  - status_filter (str): Current status filter selected
- Navigation Mappings:
  - delete-inquiry-button-{inquiry_id} -> POST to url_for('delete_inquiry', inquiry_id=inquiry_id)
  - back-to-dashboard -> url_for('dashboard')
- Forms/Buttons:
  - inquiry-status-filter (dropdown)
  - delete-inquiry-button-{inquiry_id} (button POST)
  - back-to-dashboard (button)

---

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page
  - favorites-list
  - remove-from-favorites-button-{property_id} (dynamic per property)
  - view-property-button-{property_id} (dynamic per property)
  - back-to-dashboard
- Context Variables:
  - favorites (list of dict): Favorite entries
  - properties_lookup (dict): property_id to property dict
- Navigation Mappings:
  - remove-from-favorites-button-{property_id} -> POST to url_for('remove_from_favorites', property_id=property_id)
  - view-property-button-{property_id} -> url_for('property_details', property_id=property_id)
  - back-to-dashboard -> url_for('dashboard')
- Forms/Buttons:
  - remove-from-favorites-button-{property_id} (button POST)
  - view-property-button-{property_id} (button)
  - back-to-dashboard (button)

---

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page
  - agents-list
  - agent-search
  - contact-agent-button-{agent_id} (dynamic per agent)
  - back-to-dashboard
- Context Variables:
  - agents (list of dict): List of agent info
- Navigation Mappings:
  - contact-agent-button-{agent_id} -> mailto link or contact form (implementation detail)
  - back-to-dashboard -> url_for('dashboard')
- Forms/Buttons:
  - agent-search (input text)
  - contact-agent-button-{agent_id} (button)
  - back-to-dashboard (button)

---

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page
  - locations-list
  - view-location-button-{location_id} (dynamic per location)
  - location-sort
  - back-to-dashboard
- Context Variables:
  - locations (list of dict): Locations data
- Navigation Mappings:
  - view-location-button-{location_id} -> url_for('property_search') with location filter parameter (implementation via query string)
  - back-to-dashboard -> url_for('dashboard')
- Forms/Buttons:
  - location-sort (dropdown)
  - view-location-button-{location_id} (button)
  - back-to-dashboard (button)

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File path: data/properties.txt
- Fields (pipe-delimited, in order):
  - property_id (int)
  - address (str)
  - location (str)
  - price (int)
  - property_type (str)
  - bedrooms (int)
  - bathrooms (float)
  - square_feet (int)
  - description (str)
  - agent_id (int)
  - status (str)
- Description: Stores all property listings with their details including address, type, pricing, and availability.
- Example rows:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. locations.txt
- File path: data/locations.txt
- Fields (pipe-delimited, in order):
  - location_id (int)
  - location_name (str)
  - region (str)
  - average_price (int)
  - property_count (int)
  - description (str)
- Description: Stores information about various locations, including pricing and property count.
- Example rows:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. inquiries.txt
- File path: data/inquiries.txt
- Fields (pipe-delimited, in order):
  - inquiry_id (int)
  - property_id (int)
  - customer_name (str)
  - customer_email (str)
  - customer_phone (str)
  - message (str)
  - inquiry_date (str, ISO date format YYYY-MM-DD)
  - status (str)
- Description: Stores all customer inquiries for properties with status tracking.
- Example rows:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. favorites.txt
- File path: data/favorites.txt
- Fields (pipe-delimited, in order):
  - favorite_id (int)
  - property_id (int)
  - added_date (str, ISO date format YYYY-MM-DD)
- Description: Stores all properties added to favorites by users.
- Example rows:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. agents.txt
- File path: data/agents.txt
- Fields (pipe-delimited, in order):
  - agent_id (int)
  - agent_name (str)
  - specialization (str)
  - email (str)
  - phone (str)
  - properties_sold (int)
- Description: Stores real estate agents' contact information and specialization.
- Example rows:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

# End of Design Specification
