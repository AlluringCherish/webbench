/*
scripts.js
Contains JavaScript code for client-side interactivity in the SmartHomeManager web application.
Includes form validations and dynamic UI updates.
*/
// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function () {
    // Add form validation for Add Device page
    const addDeviceForm = document.querySelector('#add-device-page form');
    if (addDeviceForm) {
        addDeviceForm.addEventListener('submit', function (e) {
            const deviceName = document.getElementById('device-name').value.trim();
            const deviceType = document.getElementById('device-type').value;
            const deviceRoom = document.getElementById('device-room').value;
            if (!deviceName) {
                alert('Please enter a device name.');
                e.preventDefault();
                return;
            }
            if (!deviceType) {
                alert('Please select a device type.');
                e.preventDefault();
                return;
            }
            if (!deviceRoom) {
                alert('Please select a room.');
                e.preventDefault();
                return;
            }
        });
    }
    // Add form validation for Automation Rules page
    const automationForm = document.querySelector('#automation-page form');
    if (automationForm) {
        automationForm.addEventListener('submit', function (e) {
            const ruleName = document.getElementById('rule-name').value.trim();
            const triggerType = document.getElementById('trigger-type').value;
            const triggerValue = document.getElementById('trigger-value').value.trim();
            const actionDevice = document.getElementById('action-device').value;
            const actionType = document.getElementById('action-type').value;
            if (!ruleName) {
                alert('Please enter a rule name.');
                e.preventDefault();
                return;
            }
            if (!triggerType) {
                alert('Please select a trigger type.');
                e.preventDefault();
                return;
            }
            if (!triggerValue) {
                alert('Please enter a trigger value.');
                e.preventDefault();
                return;
            }
            if (!actionDevice) {
                alert('Please select an action device.');
                e.preventDefault();
                return;
            }
            if (!actionType) {
                alert('Please select an action type.');
                e.preventDefault();
                return;
            }
        });
    }
    // Add form validation for Device Control page schedule time input pattern
    const scheduleTimeInput = document.getElementById('schedule_time');
    if (scheduleTimeInput) {
        scheduleTimeInput.addEventListener('input', function () {
            const pattern = /^([01]\d|2[0-3]):([0-5]\d)$/;
            if (this.value && !pattern.test(this.value)) {
                this.setCustomValidity('Please enter time in HH:MM format (24-hour).');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    // Add form validation for Energy Report date filter (optional)
    const energyForm = document.querySelector('#energy-page form');
    if (energyForm) {
        energyForm.addEventListener('submit', function (e) {
            const dateFilter = document.getElementById('date-filter').value;
            if (dateFilter) {
                // Validate date format YYYY-MM-DD
                const datePattern = /^\d{4}-\d{2}-\d{2}$/;
                if (!datePattern.test(dateFilter)) {
                    alert('Please enter a valid date in YYYY-MM-DD format.');
                    e.preventDefault();
                    return;
                }
            }
        });
    }
    // Add form validation for Activity Logs search (optional)
    const activityForm = document.querySelector('#activity-page form');
    if (activityForm) {
        activityForm.addEventListener('submit', function (e) {
            // No strict validation needed, search term can be empty
        });
    }
});