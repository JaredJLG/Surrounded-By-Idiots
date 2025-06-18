document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('personalityRadarChart');
    if (!ctx) return;

    // The 'chartData' variable is defined in a <script> tag in results.html
    const { labels, scores, primaryColor } = chartData;

    // Normalize scores for the chart. Radar charts look best with positive values.
    // Let's map the -28 to +28 range to a 0 to 100 range for display.
    const displayScores = scores.map(score => {
        const percentage = ((score + 28) / 56) * 100;
        return Math.max(0, Math.min(100, percentage));
    });

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Your Profile',
                data: displayScores,
                fill: true,
                backgroundColor: `${primaryColor}33`, // Primary color with ~20% opacity
                borderColor: primaryColor,
                pointBackgroundColor: primaryColor,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: primaryColor
            }]
        },
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true,
                        color: '#e0e0e0'
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    pointLabels: {
                        font: {
                            size: 14,
                            family: "'Roboto', sans-serif"
                        },
                        color: '#333'
                    },
                    grid: {
                        color: '#e0e0e0'
                    },
                    ticks: {
                        display: false, // Hides the 20, 40, 60, etc. labels on the spokes
                        stepSize: 25
                    }
                }
            },
            plugins: {
                legend: {
                    display: false // We don't need a legend for a single dataset
                }
            }
        }
    });
});

