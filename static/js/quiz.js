document.addEventListener('DOMContentLoaded', function() {
    const quizForm = document.getElementById('quizForm');
    if (!quizForm) return;

    const questionBlocks = quizForm.querySelectorAll('.question-block');

    questionBlocks.forEach(block => {
        const radios = block.querySelectorAll('input[type="radio"]');
        radios.forEach(radio => {
            radio.addEventListener('change', handleRadioChange);
        });
    });

    function handleRadioChange(event) {
        const clickedRadio = event.target;
        const group = clickedRadio.name.startsWith('most_') ? 'most' : 'least';
        const qId = clickedRadio.name.split('_').pop();
        const value = clickedRadio.value;

        const otherGroup = group === 'most' ? 'least' : 'most';
        const conflictingRadioName = `${otherGroup}_${qId}`;

        // Find the radio button in the other column with the same value
        const conflictingRadio = document.querySelector(`input[name="${conflictingRadioName}"][value="${value}"]`);

        // If the conflicting radio is checked, uncheck it.
        // This is the core of the improved logic. It avoids disabling anything.
        if (conflictingRadio && conflictingRadio.checked) {
            conflictingRadio.checked = false;
        }
    }

    quizForm.addEventListener('submit', function(e) {
        let allAnswered = true;
        const errorMessages = [];

        questionBlocks.forEach(block => {
            const qId = block.id.split('-')[2];
            const prompt = block.querySelector('h4').textContent;

            const mostSelected = block.querySelector(`input[name="most_${qId}"]:checked`);
            const leastSelected = block.querySelector(`input[name="least_${qId}"]:checked`);

            if (!mostSelected || !leastSelected) {
                allAnswered = false;
                block.style.border = '2px solid var(--error)';
                block.style.borderRadius = '8px';
                block.style.padding = '1.5rem';
                errorMessages.push(`Question ${qId} is incomplete.`);
            } else {
                block.style.border = '';
                block.style.borderRadius = '';
                block.style.padding = '';
            }
        });

        if (!allAnswered) {
            e.preventDefault(); // Stop form submission
            // Use the first error message or a generic one.
            const message = errorMessages.length > 0 ? "Please complete all highlighted questions before submitting." : "Please answer all questions.";
            alert(message);
        }
    });
});
