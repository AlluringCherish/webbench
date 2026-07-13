# RealEstate Web Application Design Specification

---

## Section 1: Backend Routes and Data Schema Integration

### Backend Flask Routes Overview
- **Dashboard Page**: 
  - Route: `/` or `/dashboard` 
  - Methods: GET
  - Purpose: Render `dashboard.html` with featured properties and recent listings.

- **Property Search Page**: 
  - Route: `/properties`
  - Methods: GET
  - Query Parameters: `location`, `price_min`, `price_max`, `property_type`
  - Purpose: Render `property_search.html` with filtered properties.

- **Property Details Page**:
  - Route: `/property/<int:property_id>`
  - Methods: GET
  - Purpose: Render `property_details.html` with detailed property info and agent.

- **Property Inquiry Page**:
  - Route: `/inquiry` 
  - Methods: GET (renders form) and POST (submit inquiry)
  - POST expects: `property_id`, `customer_name`, `customer_email`, `customer_phone`, `message`
  - Renders `property_inquiry.html` for GET.

- **My Inquiries Page**:
  - Route: `/inquiries`
  - Methods: GET (with optional `status` filter), POST (for deletion)
  - Renders `my_inquiries.html` with known inquiries data.

- **My Favorites Page**:
  - Route: `/favorites`
  - Methods: GET
  - Renders `my_favorites.html` with list of favorite properties joined with property details.

- **Favorites Management:**
  - Add to Favorites:
    - Route: `/favorites/add`
    - Methods: POST
    - Input: `property_id`
    - Response: JSON success or error
  - Remove from Favorites:
    - Route: `/favorites/remove`
    - Methods: POST
    - Input: `property_id`
    - Response: JSON success or error

- **Agent Directory Page**:
  - Route: `/agents`
  - Methods: GET
  - Optional Query Parameter: `search`
  - Renders `agent_directory.html` with filtered agents.

- **Locations Page**:
  - Route: `/locations`
  - Methods: GET
  - Optional Query Parameter: `sort` (by name, property_count, average_price)
  - Renders `locations.html` with sorted locations.

- **View Properties by Location**:
  - Route: `/locations/<int:location_id>/properties`
  - Methods: GET
  - Renders a properties page filtered by location.

### Data Schemas (Consistent with Frontend Data Consumption)
- **Properties:** `property_id`, `address`, `location`, `price`, `property_type`, `bedrooms`, `bathrooms`, `square_feet`, `description`, `agent_id`, `status`
- **Locations:** `location_id`, `location_name`, `region`, `average_price`, `property_count`, `description`
- **Inquiries:** `inquiry_id`, `property_id`, `customer_name`, `customer_email`, `customer_phone`, `message`, `inquiry_date`, `status`
- **Favorites:** `favorite_id`, `property_id`, `added_date`
- **Agents:** `agent_id`, `agent_name`, `specialization`, `email`, `phone`, `properties_sold`

---

## Section 2: Frontend Template and Navigation Integration

### Template Structure and Main Containers
| Template Filename           | Page Title             | Main Container ID       |
|----------------------------|------------------------|-------------------------|
| dashboard.html             | Real Estate Dashboard   | dashboard-page          |
| property_search.html       | Property Search        | search-page             |
| property_details.html      | Property Details       | property-details-page   |
| property_inquiry.html      | Submit Property Inquiry| inquiry-page            |
| my_inquiries.html          | My Inquiries           | inquiries-page          |
| my_favorites.html          | My Favorite Properties | favorites-page          |
| agent_directory.html       | Real Estate Agents     | agents-page             |
| locations.html             | Featured Locations     | locations-page          |

### UI Elements and IDs Aligned to Backend Data
- Dashboard page elements include featured properties (`featured-properties`), and buttons that navigate to search, inquiries, and favorites pages.
- Property Search page including filters by location (`location-input`), price (`price-range-min`, `price-range-max`), property type (`property-type-filter`), and property cards (`properties-grid`) with view buttons (`view-property-button-{property_id}`).
- Property Details page displays property info matching backend property data fields, with action buttons for favorites and inquiry submission.
- Property Inquiry page form inputs correspond to POST parameters required by backend for inquiry submission.
- My Inquiries page shows inquiry data with delete buttons (`delete-inquiry-button-{inquiry_id}`) linked to backend POST for deletion.
- My Favorites page shows favorite properties joined with property details, with buttons to remove favorites and view details.
- Agent Directory page lists agents filtered by name search input, with contact buttons.
- Locations page displays locations sortable by name, count, and price, with buttons linking to filtered property searches by location.

### Navigation Flows and User Interaction Triggers
- Dashboard buttons trigger navigation to respective pages using route URLs.
- Search page's filter inputs map to backend query parameters; view buttons link to `/property/<property_id>`.
- Details page buttons trigger POST requests for favorites management and navigation to inquiry page with property pre-selected.
- Inquiry form submission POSTs to `/inquiry`.
- My Inquiries page deletion buttons send AJAX POST to `/inquiries/delete`.
- Favorites page remove buttons POST to `/favorites/remove`, view buttons navigate to property details.
- Agents page search input filters agent list by name using `search` query parameter.
- Locations page sort dropdown uses `sort` query parameter; view location buttons navigate to properties filtered by location ID.
- Back to dashboard buttons consistently route to `/dashboard` or `/`.

---

## Section 3: Cross-Artifact Consistency Checks

### Route Parameter and Element ID Alignment
- Route parameters like `property_id`, `inquiry_id`, and `location_id` directly correspond to dynamic element IDs with the same suffix pattern for buttons.
- Filtering input IDs on frontend (`location-input`, `price-range-min/max`, `property-type-filter`) match backend GET query parameters (`location`, `price_min`, `price_max`, `property_type`).
- Inquiry form element IDs correspond exactly to backend POST field names (with minor conversion from `inquiry-name` to `customer_name`, etc., clearly documented).

### Coverage Check
- All pages and their required elements from the user task are present in both backend routes and frontend templates.
- No missing pages or backend routes; all landing pages and actions covered.
- All dynamic action buttons and forms are accounted for.
- The starting page is the Dashboard (`/` or `/dashboard`) as required.

### No Added Requirements
- The integration does not introduce any new features or requirements beyond those specified.
- Data formats, filtering logic, IDs, and routes remain consistent and fully cover the user requirements.

---

# Conclusion

This merged design specification provides a unified blueprint for implementing the 'RealEstate' web application using Python Flask and local text files for data. The backend routes are mapped cleanly to frontend templates and UI elements with full parameter and element ID alignment. Navigation flows, data handling, and user interactions are clearly documented for full developer implementation. This single source of truth supports consistent development of both backend services and frontend interfaces, ensuring the application meets all specified user requirements without ambiguity or gaps.
