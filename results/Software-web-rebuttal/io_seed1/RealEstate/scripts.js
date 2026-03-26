/*
JavaScript for RealEstate web application.
Handles client-side interactivity such as button actions, filtering, and navigation.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Property Search Page: handle filter form submission on change
    const locationInput = document.getElementById('location-input');
    const priceMinInput = document.getElementById('price-range-min');
    const priceMaxInput = document.getElementById('price-range-max');
    const propertyTypeFilter = document.getElementById('property-type-filter');
    if (locationInput || priceMinInput || priceMaxInput || propertyTypeFilter) {
        // Attach event listeners to inputs to submit the form on change
        const filterForm = document.getElementById('search-page');
        if (filterForm) {
            [locationInput, priceMinInput, priceMaxInput, propertyTypeFilter].forEach(function (element) {
                if (element) {
                    element.addEventListener('change', function () {
                        // Build URL with query parameters and redirect
                        const params = new URLSearchParams();
                        if (locationInput && locationInput.value.trim() !== '') {
                            params.append('location', locationInput.value.trim());
                        }
                        if (priceMinInput && priceMinInput.value.trim() !== '') {
                            params.append('price_min', priceMinInput.value.trim());
                        }
                        if (priceMaxInput && priceMaxInput.value.trim() !== '') {
                            params.append('price_max', priceMaxInput.value.trim());
                        }
                        if (propertyTypeFilter && propertyTypeFilter.value !== '') {
                            params.append('property_type', propertyTypeFilter.value);
                        }
                        const baseUrl = window.location.pathname;
                        window.location.href = baseUrl + '?' + params.toString();
                    });
                }
            });
        }
    }
    // My Inquiries Page: handle status filter change
    const inquiryStatusFilter = document.getElementById('inquiry-status-filter');
    if (inquiryStatusFilter) {
        inquiryStatusFilter.addEventListener('change', function () {
            const selectedStatus = inquiryStatusFilter.value;
            const baseUrl = window.location.pathname;
            const params = new URLSearchParams();
            if (selectedStatus && selectedStatus !== 'All') {
                params.append('status', selectedStatus);
            }
            window.location.href = baseUrl + (params.toString() ? '?' + params.toString() : '');
        });
    }
    // Locations Page: handle location sort dropdown change
    const locationSort = document.getElementById('location-sort');
    if (locationSort) {
        locationSort.addEventListener('change', function () {
            const selectedSort = locationSort.value;
            const baseUrl = window.location.pathname;
            const params = new URLSearchParams();
            if (selectedSort) {
                params.append('sort_by', selectedSort);
            }
            window.location.href = baseUrl + '?' + params.toString();
        });
    }
    // Agent Directory Page: handle agent search input (on enter key)
    const agentSearchInput = document.getElementById('agent-search');
    if (agentSearchInput) {
        agentSearchInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const searchValue = agentSearchInput.value.trim();
                const baseUrl = window.location.pathname;
                const params = new URLSearchParams();
                if (searchValue !== '') {
                    params.append('search_name', searchValue);
                }
                window.location.href = baseUrl + (params.toString() ? '?' + params.toString() : '');
            }
        });
    }
    // Back to Dashboard buttons: attach click handlers to navigate to dashboard
    const backToDashboardButtons = document.querySelectorAll('#back-to-dashboard');
    backToDashboardButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            window.location.href = '/';
        });
    });
    // My Favorites Page: handle remove from favorites buttons
    const removeFavoriteButtons = document.querySelectorAll('[id^="remove-from-favorites-button-"]');
    removeFavoriteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const propertyId = button.id.replace('remove-from-favorites-button-', '');
            if (propertyId) {
                // Create a form and submit POST to remove favorite
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/my_favorites';
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'remove_property_id';
                input.value = propertyId;
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
    // My Inquiries Page: handle delete inquiry buttons
    const deleteInquiryButtons = document.querySelectorAll('[id^="delete-inquiry-button-"]');
    deleteInquiryButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const inquiryId = button.id.replace('delete-inquiry-button-', '');
            if (inquiryId) {
                // Create a form and submit POST to delete inquiry
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/my_inquiries';
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'delete_inquiry_id';
                input.value = inquiryId;
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
});