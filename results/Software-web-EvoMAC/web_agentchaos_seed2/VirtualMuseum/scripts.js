/*
JavaScript for VirtualMuseum web application
Handles client-side interactivity including button actions and filters
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Artifact Catalog Page: Search and filter functionality
    const artifactCatalogPage = document.getElementById('artifact-catalog-page');
    if (artifactCatalogPage) {
        const searchInput = document.getElementById('search-artifact');
        const applyFilterBtn = document.getElementById('apply-artifact-filter');
        const artifactTable = document.getElementById('artifact-table');
        applyFilterBtn.addEventListener('click', () => {
            const filterText = searchInput.value.trim().toLowerCase();
            filterArtifactTable(filterText);
        });
        // Optional: filter on enter key press in search input
        searchInput.addEventListener('keyup', (event) => {
            if (event.key === 'Enter') {
                applyFilterBtn.click();
            }
        });
        function filterArtifactTable(filterText) {
            if (!artifactTable) return;
            const rows = artifactTable.getElementsByTagName('tr');
            // Skip header row (assumed first row)
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                if (cells.length === 0) continue;
                const artifactId = cells[0].textContent.toLowerCase();
                const artifactName = cells[1].textContent.toLowerCase();
                if (artifactId.includes(filterText) || artifactName.includes(filterText)) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
    }
    // Exhibitions Page: Filter by exhibition type
    const exhibitionsPage = document.getElementById('exhibitions-page');
    if (exhibitionsPage) {
        const filterDropdown = document.getElementById('filter-exhibition-type');
        const applyFilterBtn = document.getElementById('apply-exhibition-filter');
        const exhibitionList = document.getElementById('exhibition-list');
        applyFilterBtn.addEventListener('click', () => {
            const selectedType = filterDropdown.value;
            filterExhibitionTable(selectedType);
        });
        function filterExhibitionTable(selectedType) {
            if (!exhibitionList) return;
            const rows = exhibitionList.getElementsByTagName('tr');
            // Skip header row
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                if (cells.length === 0) continue;
                const exhibitionType = cells[1].textContent.trim();
                if (selectedType === '' || exhibitionType === selectedType) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
    }
    // Audio Guides Page: Filter by language
    const audioGuidesPage = document.getElementById('audio-guides-page');
    if (audioGuidesPage) {
        const filterDropdown = document.getElementById('filter-language');
        const applyFilterBtn = document.getElementById('apply-language-filter');
        const audioGuideList = document.getElementById('audio-guide-list');
        applyFilterBtn.addEventListener('click', () => {
            const selectedLanguage = filterDropdown.value;
            filterAudioGuideTable(selectedLanguage);
        });
        function filterAudioGuideTable(selectedLanguage) {
            if (!audioGuideList) return;
            const rows = audioGuideList.getElementsByTagName('tr');
            // Skip header row
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                if (cells.length === 0) continue;
                const language = cells[3].textContent.trim();
                if (selectedLanguage === '' || language === selectedLanguage) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }
        // Play audio guide buttons
        audioGuideList.addEventListener('click', (event) => {
            const target = event.target;
            if (target && target.id && target.id.startsWith('play-guide-button-')) {
                const guideId = target.id.replace('play-guide-button-', '');
                playAudioGuide(guideId);
            }
        });
        function playAudioGuide(guideId) {
            // Assuming audio files are stored in static/audio/ with filenames like guide_{guideId}.mp3
            const audioSrc = `/static/audio/guide_${guideId}.mp3`;
            let audioPlayer = document.getElementById('audio-player');
            if (!audioPlayer) {
                audioPlayer = document.createElement('audio');
                audioPlayer.id = 'audio-player';
                audioPlayer.controls = true;
                document.body.appendChild(audioPlayer);
            }
            audioPlayer.src = audioSrc;
            audioPlayer.play().catch(err => {
                alert('Audio file not found or cannot be played.');
            });
        }
    }
    // Virtual Events Page: Register and cancel registration buttons
    const virtualEventsPage = document.getElementById('virtual-events-page');
    if (virtualEventsPage) {
        virtualEventsPage.addEventListener('click', (event) => {
            const target = event.target;
            if (!target || !target.id) return;
            // Register event button
            if (target.id.startsWith('register-event-button-')) {
                const eventId = target.id.replace('register-event-button-', '');
                handleEventRegistration(eventId);
            }
            // Cancel registration button
            if (target.id.startsWith('cancel-registration-button-')) {
                const registrationId = target.id.replace('cancel-registration-button-', '');
                handleCancelRegistration(registrationId);
            }
        });
        function handleEventRegistration(eventId) {
            // Redirect to registration URL or send AJAX request
            // For simplicity, redirect to a registration route
            window.location.href = `/register_event/${eventId}`;
        }
        function handleCancelRegistration(registrationId) {
            // Redirect to cancellation URL or send AJAX request
            // For simplicity, redirect to a cancellation route
            window.location.href = `/cancel_registration/${registrationId}`;
        }
    }
    // Visitor Tickets Page: Purchase ticket button validation
    const visitorTicketsPage = document.getElementById('visitor-tickets-page');
    if (visitorTicketsPage) {
        const purchaseBtn = document.getElementById('purchase-ticket-button');
        const numberOfTicketsInput = document.getElementById('number-of-tickets');
        purchaseBtn.addEventListener('click', () => {
            const numTickets = parseInt(numberOfTicketsInput.value, 10);
            if (isNaN(numTickets) || numTickets <= 0) {
                alert('Please enter a valid number of tickets.');
                return;
            }
            // Submit the form or redirect to purchase handler
            // Assuming form submission handled by backend
            const form = purchaseBtn.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
});