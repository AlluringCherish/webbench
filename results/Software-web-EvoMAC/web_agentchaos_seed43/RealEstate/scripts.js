/*
JavaScript for RealEstate web application.
Handles client-side interactivity such as button actions, filtering, and navigation.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Property Search Page: Filter form submission on input changes
    const locationInput = document.getElementById('location-input');
    const priceMinInput = document.getElementById('price-range-min');
    const priceMaxInput = document.getElementById('price-range-max');
    const propertyTypeFilter = document.getElementById('property-type-filter');
    if (locationInput || priceMinInput || priceMaxInput || propertyTypeFilter) {
        const filterForm = document.getElementById('search-page');
        if (filterForm) {
            // Attach event listeners to inputs to submit form on change
            if (locationInput) {
                locationInput.addEventListener('change', () => filterForm.submit());
            }
            if (priceMinInput) {
                priceMinInput.addEventListener('change', () => filterForm.submit());
            }
            if (priceMaxInput) {
                priceMaxInput.addEventListener('change', () => filterForm.submit());
            }
            if (propertyTypeFilter) {
                propertyTypeFilter.addEventListener('change', () => filterForm.submit());
            }
        }
    }
    // My Inquiries Page: Filter inquiries by status dropdown
    const inquiryStatusFilter = document.getElementById('inquiry-status-filter');
    if (inquiryStatusFilter) {
        inquiryStatusFilter.addEventListener('change', function () {
            const selectedStatus = this.value;
            // Reload page with status filter as query parameter
            const url = new URL(window.location.href);
            url.searchParams.set('status', selectedStatus);
            window.location.href = url.toString();
        });
    }
    // Locations Page: Sort locations dropdown
    const locationSort = document.getElementById('location-sort');
    if (locationSort) {
        locationSort.addEventListener('change', function () {
            const selectedSort = this.value;
            // Reload page with sort parameter
            const url = new URL(window.location.href);
            url.searchParams.set('sort', selectedSort);
            window.location.href = url.toString();
        });
    }
    // Agent Directory Page: Search agents by name input
    const agentSearchInput = document.getElementById('agent-search');
    if (agentSearchInput) {
        agentSearchInput.addEventListener('input', function () {
            const searchQuery = this.value.trim();
            // Reload page with search query parameter
            const url = new URL(window.location.href);
            if (searchQuery.length > 0) {
                url.searchParams.set('search', searchQuery);
            } else {
                url.searchParams.delete('search');
            }
            // Use debounce to avoid too many reloads
            if (window.agentSearchTimeout) {
                clearTimeout(window.agentSearchTimeout);
            }
            window.agentSearchTimeout = setTimeout(() => {
                window.location.href = url.toString();
            }, 500);
        });
    }
    // Confirm deletion for inquiries
    const deleteInquiryButtons = document.querySelectorAll('[id^="delete-inquiry-button-"]');
    deleteInquiryButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to delete this inquiry?')) {
                event.preventDefault();
            }
        });
    });
    // Confirm removal for favorites
    const removeFavoriteButtons = document.querySelectorAll('[id^="remove-from-favorites-button-"]');
    removeFavoriteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Are you sure you want to remove this property from favorites?')) {
                event.preventDefault();
            }
        });
    });
    // Contact agent buttons: simple alert or could be extended
    const contactAgentButtons = document.querySelectorAll('[id^="contact-agent-button-"]');
    contactAgentButtons.forEach(button => {
        button.addEventListener('click', function () {
            const agentId = this.id.replace('contact-agent-button-', '');
            alert('To contact agent ID ' + agentId + ', please use the provided email or phone number.');
        });
    });
    // View location buttons: navigate to location view
    const viewLocationButtons = document.querySelectorAll('[id^="view-location-button-"]');
    viewLocationButtons.forEach(button => {
        button.addEventListener('click', function () {
            const locationId = this.id.replace('view-location-button-', '');
            window.location.href = '/view_location/' + locationId;
        });
    });
    // View property buttons on favorites and dashboard handled by form submit or button click already
    // Add to favorites and submit inquiry buttons on property details page are handled by form submission
});