# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                           | HTTP Method | Function Name           | Template Rendered        | Route Parameters          | Context Variables (name : type)                                              | Expected POST Form Data (name : type)                                              |
|------------------------------------|-------------|------------------------|--------------------------|---------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| /                                  | GET         | root_redirect           | Redirects to /dashboard  | None                      | None                                                                        | None                                                                               |
| /dashboard                        | GET         | dashboard              | dashboard.html           | None                      | featured_properties : list (dict)                                             | None                                                                               |
| /properties                      | GET         | property_search        | property_search.html     | None                      | properties : list (dict)                                                      | None                                                                               |
| /property/<int:property_id>       | GET         | property_details       | property_details.html    | property_id (int)         | property : dict                                                              | None                                                                               |
| /inquiry                        | GET         | inquiry_form           | inquiry.html             | None                      | properties : list (dict), errors : dict (optional)                            | None                                                                               |
| /inquiry                        | POST        | submit_inquiry         | inquiry.html (on error) or redirect | None                | properties : list (dict) (on error)                                          | property_id : int, customer_name : str, customer_email : str, customer_phone : str, message : str |
| /inquiries                     | GET         | inquiries_list         | inquiries.html           | None                      | inquiries : list (dict)                                                      | None                                                                               |
| /inquiries/delete/<int:inquiry_id> | POST        | delete_inquiry         | Redirect to /inquiries    | inquiry_id (int)           | None                                                                        | None                                                                               |
| /favorites                     | GET         | favorites_list         | favorites.html           | None                      | favorite_properties : list (dict)                                            | None                                                                               |
| /favorites/add/<int:property_id> | POST        | add_favorite           | Redirect to /favorites    | property_id (int)           | None                                                                        | None                                                                               |
| /favorites/remove/<int:property_id> | POST        | remove_favorite        | Redirect to /favorites    | property_id (int)           | None                                                                        | None                                                                               |
| /agents                        | GET         | agents_list            | agents.html              | None                      | agents : list (dict)                                                         | None                                                                               |
| /locations                     | GET         | locations_list         | locations.html           | None                      | locations : list (dict)                                                      | None                                                                               |

### Route Details

- **root_redirect**: GET '/' redirects to '/dashboard'

- **dashboard**: GET '/dashboard'
  - Template: dashboard.html
  - Context Variables:
    - featured_properties (list of dict): featured property recommendations

- **property_search**: GET '/properties'
  - Template: property_search.html
  - Context Variables:
    - properties (list of dict): all available properties

- **property_details**: GET '/property/<property_id>'
  - Route parameter: property_id (int)
  - Template: property_details.html
  - Context Variables:
    - property (dict): details of the specified property

- **inquiry_form**: GET '/inquiry'
  - Template: inquiry.html
  - Context Variables:
    - properties (list of dict): to populate select-property dropdown
    - errors (dict, optional): validation errors

- **submit_inquiry**: POST '/inquiry'
  - Expected form data:
    - property_id (int)
    - customer_name (str)
    - customer_email (str)
    - customer_phone (str)
    - message (str)
  - On validation errors, re-render inquiry.html with errors and properties
  - On success, redirect to /inquiries

- **inquiries_list**: GET '/inquiries'
  - Template: inquiries.html
  - Context Variables:
    - inquiries (list of dict): all inquiries

- **delete_inquiry**: POST '/inquiries/delete/<inquiry_id>'
  - Route parameter: inquiry_id (int)
  - Deletes the inquiry
  - Redirects to /inquiries

- **favorites_list**: GET '/favorites'
  - Template: favorites.html
  - Context Variables:
    - favorite_properties (list of dict): all favorite properties

- **add_favorite**: POST '/favorites/add/<property_id>'
  - Route parameter: property_id (int)
  - Adds property to favorites
  - Redirects to /favorites

- **remove_favorite**: POST '/favorites/remove/<property_id>'
  - Route parameter: property_id (int)
  - Removes property from favorites
  - Redirects to /favorites

- **agents_list**: GET '/agents'
  - Template: agents.html
  - Context Variables:
    - agents (list of dict): all real estate agents

- **locations_list**: GET '/locations'
  - Template: locations.html
  - Context Variables:
    - locations (list of dict): popular locations

---

## Section 2: HTML Templates Specification (Frontend)

---

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard
  - featured-properties (Div): Featured property recommendations
  - browse-properties-button (Button): Navigates to property search page
  - my-inquiries-button (Button): Navigates to inquiries page
  - my-favorites-button (Button): Navigates to favorites page
- Context Variables:
  - featured_properties (list of dict): featured property details
- Navigation element mappings:
  - browse-properties-button: url_for('property_search')
  - my-inquiries-button: url_for('inquiries_list')
  - my-favorites-button: url_for('favorites_list')
- Forms: None

---

### 2. property_search.html
- Page Title: Property Search
- Element IDs:
  - search-page (Div): Container for property search page
  - location-input (Input text): Search filter by location
  - price-range-min (Input number): Minimum price filter
  - price-range-max (Input number): Maximum price filter
  - property-type-filter (Dropdown): Property type filter
  - properties-grid (Div): Grid displaying properties
  - view-property-button-{property_id} (Button): Button for viewing each property details
- Context Variables:
  - properties (list of dict): all available properties
- Navigation element mappings:
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)
- Forms: None (search/filter implemented client-side or via query parameters)

---

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (Div): Container for property details
  - property-address (H1): Property address
  - property-price (Div): Property price
  - property-description (Div): Property description
  - property-features (Div): Property features (beds, baths, square footage)
  - add-to-favorites-button (Button): Add property to favorites
  - submit-inquiry-button (Button): Submit inquiry button
- Context Variables:
  - property (dict): detailed property info (property_id, address, price, description, bedrooms, bathrooms, square_feet)
- Navigation element mappings:
  - add-to-favorites-button: POST form to url_for('add_favorite', property_id=property['property_id'])
  - submit-inquiry-button: url_for('inquiry_form')
- Forms:
  - Form for adding to favorites, wrapping add-to-favorites-button

---

### 4. inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (Div): Container for inquiry form
  - select-property (Dropdown): Property selection dropdown
  - inquiry-name (Input): Customer name input
  - inquiry-email (Input email): Customer email input
  - inquiry-phone (Input tel): Customer phone input
  - inquiry-message (Textarea): Inquiry message input
  - submit-inquiry-button (Button): Submit button
- Context Variables:
  - properties (list of dict): Properties for selection
  - errors (dict, optional): Form validation errors
- Navigation element mappings:
  - None
- Forms:
  - Inquiry form POST to url_for('submit_inquiry')
  - Fields: select-property, inquiry-name, inquiry-email, inquiry-phone, inquiry-message
  - Submit button id: submit-inquiry-button

---

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (Div): Container for inquiries page
  - inquiries-table (Table): Table listing inquiries
  - inquiry-status-filter (Dropdown): Status filter dropdown
  - delete-inquiry-button-{inquiry_id} (Button): Delete inquiry button per inquiry
  - back-to-dashboard (Button): Back to dashboard button
- Context Variables:
  - inquiries (list of dict): Inquiry entries with details
- Navigation element mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - Each delete button wrapped in a form POST to url_for('delete_inquiry', inquiry_id=inquiry_id)

---

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (Div): Container for favorites page
  - favorites-list (Div): List of favorite properties
  - remove-from-favorites-button-{property_id} (Button): Remove favorite button per property
  - view-property-button-{property_id} (Button): View property button per property
  - back-to-dashboard (Button): Back to dashboard button
- Context Variables:
  - favorite_properties (list of dict): Favorite properties details
- Navigation element mappings:
  - back-to-dashboard: url_for('dashboard')
  - view-property-button-{property_id}: url_for('property_details', property_id=property_id)
- Forms:
  - Each remove button wrapped in a form POST to url_for('remove_favorite', property_id=property_id)

---

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (Div): Container for agents page
  - agents-list (Div): List of agents
  - agent-search (Input): Agent name search input
  - contact-agent-button-{agent_id} (Button): Contact button per agent
  - back-to-dashboard (Button): Back to dashboard button
- Context Variables:
  - agents (list of dict): Agent details
- Navigation element mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms:
  - contact-agent-button-{agent_id} has no POST action (informational only)

---

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (Div): Container for locations page
  - locations-list (Div): List of locations
  - view-location-button-{location_id} (Button): View properties button per location
  - location-sort (Dropdown): Sort locations dropdown
  - back-to-dashboard (Button): Back to dashboard button
- Context Variables:
  - locations (list of dict): Location data
- Navigation element mappings:
  - back-to-dashboard: url_for('dashboard')
- Forms: None

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File Path: data/properties.txt
- Pipe-delimited Fields (exact order):
  1. property_id
  2. address
  3. location
  4. price
  5. property_type
  6. bedrooms
  7. bathrooms
  8. square_feet
  9. description
  10. agent_id
  11. status
- Description: Detailed property listings with basic info and status
- Example Rows:
  - 1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  - 2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  - 3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
- Parsing Note: Pipe-delimited text, no header line

### 2. locations.txt
- File Path: data/locations.txt
- Pipe-delimited Fields (exact order):
  1. location_id
  2. location_name
  3. region
  4. average_price
  5. property_count
  6. description
- Description: Popular locations with statistics
- Example Rows:
  - 1|Downtown|Central|425000|45|Urban area with business district
  - 2|Midtown|Central|380000|38|Mixed residential and commercial zone
  - 3|Suburb|Outskirts|295000|52|Family-friendly residential area
- Parsing Note: Pipe-delimited text, no header line

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Pipe-delimited Fields (exact order):
  1. inquiry_id
  2. property_id
  3. customer_name
  4. customer_email
  5. customer_phone
  6. message
  7. inquiry_date
  8. status
- Description: User inquiries on properties with contact info and status
- Example Rows:
  - 1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  - 2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  - 3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
- Parsing Note: Pipe-delimited text, no header line

### 4. favorites.txt
- File Path: data/favorites.txt
- Pipe-delimited Fields (exact order):
  1. favorite_id
  2. property_id
  3. added_date
- Description: List of user favorite properties with addition dates
- Example Rows:
  - 1|1|2025-01-10
  - 2|2|2025-01-12
  - 3|3|2025-01-14
- Parsing Note: Pipe-delimited text, no header line

### 5. agents.txt
- File Path: data/agents.txt
- Pipe-delimited Fields (exact order):
  1. agent_id
  2. agent_name
  3. specialization
  4. email
  5. phone
  6. properties_sold
- Description: Real estate agent records
- Example Rows:
  - 101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  - 102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  - 103|James Martinez|Luxury Homes|james@email.com|555-0003|67
- Parsing Note: Pipe-delimited text, no header line

---

# End of design_spec.md
