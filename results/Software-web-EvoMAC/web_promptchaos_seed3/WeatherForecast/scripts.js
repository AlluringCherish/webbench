/**
 * JavaScript for client-side interactivity in WeatherForecast web application.
 * Handles button actions and dynamic UI updates across all pages.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add event listeners for buttons if needed
    // Currently, buttons use inline onclick handlers for navigation,
    // but this file can be extended for more complex interactions.
    // Example: Confirm before removing a saved location
    const removeButtons = document.querySelectorAll('button[id^="remove-location-button-"]');
    removeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const confirmed = confirm('Are you sure you want to remove this saved location?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    // Example: Additional dynamic UI updates can be added here
});