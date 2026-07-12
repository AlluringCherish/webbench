# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path              | HTTP Method | Function Name           | Template Rendered         | Route Parameters                | Context Variables (type)                                                                                         | Expected POST Form Data                                  |
|-------------------------|-------------|------------------------|---------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| /                       | GET         | root_redirect           | None (redirect)            | None                           | None                                                                                                          | None                                                    |
| /dashboard              | GET         | dashboard_page          | dashboard.html            | None                           | featured_properties (list of dict), recent_listings (list of dict)                                            | None                                                    |
| /properties/search      | GET, POST   | property_search_page    | property_search.html      | None                           | properties (list of dict), filtered_properties (list of dict) (on POST), search_filters (dict) (on POST)      | location (str), price_min (float/int), price_max (float/int), property_type (str) (on POST)                      |
| /properties/<int:property_id> | GET         | property_details_page   | property_details.html      | property_id                   | property (dict)                                                                                               | None                                                    |
| /inquiries/new          | GET, POST   | property_inquiry_page   | property_inquiry.html     | None                           | properties (list of dict)                                                                                        | property_id (int), customer_name (str), customer_email (str), customer_phone (str), message (str) (on POST)        |
| /inquiries             | GET         | inquiries_page          | inquiries.html           | None                           | inquiries (list of dict), inquiry_status_filter (str)                                                          | None                                                    |
| /inquiries/delete/<int:inquiry_id> | POST        | delete_inquiry          | None (redirect to inquiries) | inquiry_id                     | None                                                                                                          | None                                                    |
| /favorites             | GET         | favorites_page          | favorites.html           | None                           | favorites (list of dict), favorite_properties (list of dict)                                                   | None                                                    |
| /favorites/add/<int:property_id> | POST        | add_to_favorites        | None (redirect)            | property_id                   | None                                                                                                          | None                                                    |
| /favorites/remove/<int:property_id> | POST        | remove_from_favorites   | None (redirect)            | property_id                   | None                                                                                                          | None                                                    |
| /agents                | GET         | agents_page             | agents.html              | None                           | agents (list of dict)                                                                                            | None                                                    |
| /locations             | GET         | locations_page          | locations.html           | None                           | locations (list of dict), sort_option (str)                                                                     | None                                                    |

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (Div container)
  - featured-properties (Div container)
  - browse-properties-button (Button)
  - my-inquiries-button (Button)
  - my-favorites-button (Button)
- Context Variables:
  - featured_properties (list of dict): Featured property recommendations for display
  - recent_listings (list of dict): Recently listed properties
- Navigation:
  - browse-properties-button &rarr; `url_for('property_search_page')`
  - my-inquiries-button &rarr; `url_for('inquiries_page')`
  - my-favorites-button &rarr; `url_for('favorites_page')`
- Forms:
  - None

### 2. property_search.html
- Page Title: Property Search
- Element IDs:
  - search-page (Div container)
  - location-input (Input field for location)
  - price-range-min (Number input for min price)
  - price-range-max (Number input for max price)
  - property-type-filter (Dropdown: House, Apartment, Condo, Land)
  - properties-grid (Div container for property cards)
  - view-property-button-{property_id} (Button to view details for each property)
- Context Variables:
  - properties (list of dict): All properties data
  - filtered_properties (list of dict): Properties matching current search/filter criteria (on POST)
  - search_filters (dict): Dict holding current filter values (location:str, price_min:float, price_max:float, property_type:str)
- Navigation:
  - Each view-property-button-{property_id} &rarr; `url_for('property_details_page', property_id=property_id)`
- Forms:
  - Search/filter form with inputs:
    - location-input (name="location")
    - price-range-min (name="price_min")
    - price-range-max (name="price_max")
    - property-type-filter (name="property_type")
    - Submit button with ID: search-submit-button (if implemented)

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (Div container)
  - property-address (H1 for property address)
  - property-price (Div for price)
  - property-description (Div for description)
  - property-features (Div for beds, baths, square footage)
  - add-to-favorites-button (Button to add property to favorites)
  - submit-inquiry-button (Button to submit inquiry for this property)
- Context Variables:
  - property (dict): All property detail fields
- Navigation:
  - add-to-favorites-button action via POST to `url_for('add_to_favorites', property_id=property['property_id'])`
  - submit-inquiry-button navigates to inquiry page `url_for('property_inquiry_page')` with property pre-selected (could be via GET param or session)
- Forms:
  - Add to favorites form: button with ID add-to-favorites-button, POST action to favorites add route
  - Submit inquiry button: may be a link or form button navigating to inquiry page

### 4. property_inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (Div container)
  - select-property (Dropdown: list of properties for selection)
  - inquiry-name (Input for customer name)
  - inquiry-email (Input type email)
  - inquiry-phone (Input type tel)
  - inquiry-message (Textarea for inquiry message)
  - submit-inquiry-button (Button to submit inquiry)
- Context Variables:
  - properties (list of dict): Properties available for inquiry
- Navigation:
  - Form POSTs to `url_for('property_inquiry_page')`
- Forms:
  - Inquiry submission form with inputs matching element IDs for data submission
  - Submit button with ID submit-inquiry-button

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (Div container)
  - inquiries-table (Table listing all inquiries)
  - inquiry-status-filter (Dropdown: All, Pending, Contacted, Resolved)
  - delete-inquiry-button-{inquiry_id} (Button to delete specific inquiry)
  - back-to-dashboard (Button to navigate back)
- Context Variables:
  - inquiries (list of dict): All inquiries
  - inquiry_status_filter (str): Current filter setting
- Navigation:
  - back-to-dashboard &rarr; `url_for('dashboard_page')`
  - delete-inquiry-button-{inquiry_id} form POST to `url_for('delete_inquiry', inquiry_id=inquiry_id)`
- Forms:
  - Delete inquiry buttons are part of POST forms
  - Filter dropdown submits GET filter or via JavaScript

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (Div container)
  - favorites-list (Div listing favorite properties)
  - remove-from-favorites-button-{property_id} (Button to remove favorite)
  - view-property-button-{property_id} (Button to view details)
  - back-to-dashboard (Button to navigate back)
- Context Variables:
  - favorites (list of dict): Favorite entries
  - favorite_properties (list of dict): Property details for favorites
- Navigation:
  - back-to-dashboard &rarr; `url_for('dashboard_page')`
  - remove and view buttons correspond to POST and GET routes respectively
- Forms:
  - Remove from favorites buttons are POST forms

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (Div container)
  - agents-list (Div listing all agents)
  - agent-search (Input field to search agents)
  - contact-agent-button-{agent_id} (Button to contact agent)
  - back-to-dashboard (Button to navigate back)
- Context Variables:
  - agents (list of dict): All agent data
- Navigation:
  - back-to-dashboard &rarr; `url_for('dashboard_page')`
  - contact-agent-button-{agent_id} could link to email or contact form (implementation detail)
- Forms:
  - Agent search may be client-side or server-side filter

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (Div container)
  - locations-list (Div listing all locations)
  - view-location-button-{location_id} (Button to view properties in location)
  - location-sort (Dropdown to sort locations by name, count, average price)
  - back-to-dashboard (Button to navigate back)
- Context Variables:
  - locations (list of dict): Location data
  - sort_option (str): Current sorting criteria
- Navigation:
  - back-to-dashboard &rarr; `url_for('dashboard_page')`
  - view-location-button-{location_id} could link to filtered property search or location details (design dependent)
- Forms:
  - Sorting dropdown submits GET or interacts client-side

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- File Path: data/properties.txt
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
  - status (str) [e.g., Available, Sold]
- Description: Stores all property listings with detailed attributes and status.
- Example Rows:
```
1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
```

### 2. locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited, in order):
  - location_id (int)
  - location_name (str)
  - region (str)
  - average_price (int)
  - property_count (int)
  - description (str)
- Description: Stores popular locations with statistical summaries.
- Example Rows:
```
1|Downtown|Central|425000|45|Urban area with business district
2|Midtown|Central|380000|38|Mixed residential and commercial zone
3|Suburb|Outskirts|295000|52|Family-friendly residential area
```

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited, in order):
  - inquiry_id (int)
  - property_id (int)
  - customer_name (str)
  - customer_email (str)
  - customer_phone (str)
  - message (str)
  - inquiry_date (str, YYYY-MM-DD)
  - status (str) [Pending, Contacted, Resolved]
- Description: Stores property inquiry submissions with status.
- Example Rows:
```
1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
```

### 4. favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited, in order):
  - favorite_id (int)
  - property_id (int)
  - added_date (str, YYYY-MM-DD)
- Description: Stores records of properties added to favorites by users.
- Example Rows:
```
1|1|2025-01-10
2|2|2025-01-12
3|3|2025-01-14
```

### 5. agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited, in order):
  - agent_id (int)
  - agent_name (str)
  - specialization (str)
  - email (str)
  - phone (str)
  - properties_sold (int)
- Description: Stores real estate agents' info including contact and sales data.
- Example Rows:
```
101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
103|James Martinez|Luxury Homes|james@email.com|555-0003|67
```

---

*End of Design Specification Document*