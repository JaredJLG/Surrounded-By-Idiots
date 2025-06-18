document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.analysis-btn');
    const contentAreas = {
        color: document.getElementById('analysis-color-content'),
        romance: document.getElementById('analysis-romance-content'),
        work: document.getElementById('analysis-work-content'),
    };

    // Keep track of which content has already been loaded
    const loadedContent = {};

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const analysisType = button.dataset.analysis;

            // Toggle active state for buttons
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Hide all content areas
            Object.values(contentAreas).forEach(area => area.style.display = 'none');

            // Show the relevant content area
            const targetArea = contentAreas[analysisType];
            targetArea.style.display = 'block';

            // Fetch content only if it hasn't been loaded yet
            if (!loadedContent[analysisType]) {
                fetchAnalysis(analysisType, targetArea);
            }
        });
    });

    async function fetchAnalysis(type, targetElement) {
        // Show a loading spinner
        targetElement.innerHTML = '<div class="content-spinner"></div>';

        try {
            const response = await fetch(`/get_extra_analysis/${resultId}/${type}`);

            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Use the Marked.js library to convert Markdown to HTML
            targetElement.innerHTML = marked.parse(data.feedback);

            // Mark this content as loaded
            loadedContent[type] = true;

        } catch (error) {
            console.error('Failed to fetch analysis:', error);
            targetElement.innerHTML = `
                <div style="color: var(--error);">
                    <h4>Oops! Something went wrong.</h4>
                    <p>We couldn't generate this analysis. Please try again in a moment.</p>
                    <p><small>Error: ${error.message}</small></p>
                </div>
            `;
        }
    }
});
