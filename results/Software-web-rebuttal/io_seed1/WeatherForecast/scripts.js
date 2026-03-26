'''
JavaScript for WeatherForecast Web Application.
Handles button clicks and form submissions for navigation and filtering.
'''
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard page buttons
    const searchLocationButton = document.getElementById('search-location-button');
    if (searchLocationButton) {
        searchLocationButton.addEventListener('click', function () {
            window.location.href = '/location_search';
        });
    }
    const viewForecastButton = document.getElementById('view-forecast-button');
    if (viewForecastButton) {
        viewForecastButton.addEventListener('click', function () {
            window.location.href = '/weekly_forecast';
        });
    }
    const viewAlertsButton = document.getElementById('view-alerts-button');
    if (viewAlertsButton) {
        viewAlertsButton.addEventListener('click', function () {
            window.location.href = '/weather_alerts';
        });
    }
    const viewAirQualityButton = document.getElementById('view-air-quality-button');
    if (viewAirQualityButton) {
        viewAirQualityButton.addEventListener('click', function () {
            window.location.href = '/air_quality';
        });
    }
    const savedLocationsButton = document.getElementById('saved-locations-button');
    if (savedLocationsButton) {
        savedLocationsButton.addEventListener('click', function () {
            window.location.href = '/saved_locations';
        });
    }
    const settingsButton = document.getElementById('settings-button');
    if (settingsButton) {
        settingsButton.addEventListener('click', function () {
            window.location.href = '/settings';
        });
    }
    // Forecast page location filter form submission handled by onchange attribute in select
    // Weather alerts filters handled by onchange attribute in selects
    // Air quality location filter handled by onchange attribute in select
    // Saved Locations page buttons
    const addNewLocationButton = document.getElementById('add-new-location-button');
    if (addNewLocationButton) {
        addNewLocationButton.addEventListener('click', function () {
            window.location.href = '/add_new_location';
        });
    }
    const viewLocationWeatherButtons = document.querySelectorAll('[id^="view-location-weather-"]');
    viewLocationWeatherButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const locationId = this.getAttribute('data-location-id');
            if (locationId) {
                window.location.href = '/current_weather/' + locationId;
            }
        });
    });
    // Remove location buttons are forms with POST, no JS needed
    // Back to dashboard buttons are forms with POST, no JS needed
});