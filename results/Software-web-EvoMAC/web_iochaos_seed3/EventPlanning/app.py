
```javascript

web
search and to experience.


the to be fully
{
    // Events Listing Page: Enhance search/filter form to submit on Enter key in search input
    const eventSearchInput = document.getElementById('event-search-input');
    if (eventSearchInput) {
        eventSearchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
});
}

Venues Enhance form to key
=
{
        venueSearchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
});


Participants Page: Enhance Enter key in search input
const participantSearchInput document.getElementById('search-participant-input');
{
        participantSearchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }



Summary to Enter key search
bookingSearchInput =
if {
        bookingSearchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.form.submit();
            }
});


Page: Add click handlers navigation but can effect confirm if needed)
JS here as buttons use inline

Event extra needed

No extra form handled

Add confirmation participant
const
if {
        addParticipantButton.addEventListener('click', function (e) {
            // Optional: confirm before adding participant
            // Uncomment below if confirmation desired
            // if (!confirm('Are you sure you want to add this participant?')) {
            //     e.preventDefault();
            // }

}

// Bookings Summary Page:
const document.getElementById('bookings-table');
(bookingsTable) {
        bookingsTable.addEventListener('click', function (e) {
            if (e.target && e.target.tagName === 'BUTTON' && e.target.name === 'cancel-booking-id') {
                const confirmed = confirm('Are you sure you want to cancel this booking?');
                if (!confirmed) {
                    e.preventDefault();
                }


}

Page: Details buttons show alert with venue info in
JS needed

Page: button needed



