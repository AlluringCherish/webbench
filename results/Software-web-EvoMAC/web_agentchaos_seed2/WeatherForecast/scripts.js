/*
Client-side JavaScript for WeatherForecast web application.
Handles navigation and enhances user experience without breaking backend routing.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Navigation buttons by their IDs
    const navButtons = [
        { id: 'search-location-button', url: '/location_search' },
        { id: 'view-forecast-button', url: '/weekly_forecast' },
        { id: 'view-alerts-button', url: '/weather_alerts' },
        { id: 'air-quality-button', url: '/air_quality' },
        { id: 'saved-locations-button', url: '/saved_locations' },
        { id: 'settings-button', url: '/settings' },
        { id: 'back-to-dashboard', url: '/' },
        { idPrefix: 'view-location-weather-', urlPrefix: '/view_location_weather/' },
        { idPrefix: 'remove-location-button-', urlPrefix: '/remove_location/' },
        { idPrefix: 'acknowledge-alert-button-', urlPrefix: '/acknowledge_alert/' },
        { idPrefix: 'select-location-button-', urlPrefix: '/select_location/' }
    ];
    // Attach click event listeners for buttons with fixed IDs
    navButtons.forEach(function (btn) {
        if (btn.id) {
            const element = document.getElementById(btn.id);
            if (element) {
                element.addEventListener('click', function () {
                    window.location.href = btn.url;
                });
            }
        }
    });
    // Attach click event listeners for buttons with dynamic IDs (with suffix)
    navButtons.forEach(function (btn) {
        if (btn.idPrefix) {
            // Select all buttons whose id starts with the prefix
            const elements = document.querySelectorAll(`button[id^="${btn.idPrefix}"]`);
            elements.forEach(function (el) {
                el.addEventListener('click', function (event) {
                    event.preventDefault();
                    // Extract the id suffix (e.g., location_id or alert_id)
                    const idSuffix = el.id.substring(btn.idPrefix.length);
                    // For remove-location and acknowledge-alert buttons, POST is required
                    if (btn.urlPrefix === '/remove_location/' || btn.urlPrefix === '/acknowledge_alert/' || btn.urlPrefix === '/select_location/') {
                        // Create a form and submit POST request
                        const form = document.createElement('form');
                        form.method = 'POST';
                        form.action = btn.urlPrefix + idSuffix;
                        document.body.appendChild(form);
                        form.submit();
                    } else {
                        // For view-location-weather buttons, simple GET redirect
                        window.location.href = btn.urlPrefix + idSuffix;
                    }
                });
            });
        }
    });
    // Enhance dropdown forms to submit on change for better UX
    const dropdownForms = [
        { formId: 'weekly-forecast-form', selectId: 'location-filter' },
        { formId: 'weather-alerts-form', selectIds: ['location-filter-alerts', 'severity-filter'] },
        { formId: 'air-quality-form', selectId: 'location-aqi-filter' },
        { formId: 'settings-form', selectIds: ['temperature-unit-select', 'default-location-select'] }
    ];
    dropdownForms.forEach(function (item) {
        const form = document.getElementById(item.formId);
        if (!form) return;
        if (item.selectId) {
            const select = document.getElementById(item.selectId);
            if (select) {
                select.addEventListener('change', function () {
                    form.submit();
                });
            }
        }
        if (item.selectIds) {
            item.selectIds.forEach(function (selId) {
                const select = document.getElementById(selId);
                if (select) {
                    select.addEventListener('change', function () {
                        form.submit();
                    });
                }
            });
        }
    });
    // Optional: Confirm before removing a saved location or acknowledging alert
    const confirmActions = [
        { idPrefix: 'remove-location-button-', message: 'Are you sure you want to remove this saved location?' },
        { idPrefix: 'acknowledge-alert-button-', message: 'Acknowledge this alert?' }
    ];
    confirmActions.forEach(function (action) {
        const elements = document.querySelectorAll(`button[id^="${action.idPrefix}"]`);
        elements.forEach(function (el) {
            el.addEventListener('click', function (event) {
                if (!confirm(action.message)) {
                    event.preventDefault();
                }
            });
        });
    });
});