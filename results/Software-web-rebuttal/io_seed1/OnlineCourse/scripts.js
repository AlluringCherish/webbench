/*
JavaScript for OnlineCourse web application.
Provides client-side interactivity including button actions and form validation.
Enhances user experience by handling events and validating forms before submission.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Example: Add confirmation for logout if logout button/link is added in future
    // Currently no logout button in templates, but can be added here if needed
    // Form validation for Submit Assignment page
    const submitAssignmentForm = document.querySelector('#submit-page form');
    if (submitAssignmentForm) {
        submitAssignmentForm.addEventListener('submit', function (event) {
            const submissionText = document.getElementById('submission-text').value.trim();
            if (!submissionText) {
                alert('Submission text cannot be empty.');
                event.preventDefault();
            }
        });
    }
    // Additional client-side interactivity can be added here if needed
});