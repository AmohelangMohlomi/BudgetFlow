// static/js/dashboard-chart.js

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('budgetVsSpendingChart').getContext('2d');

    // These values will be injected via data- attributes from the HTML
    const categories = JSON.parse(ctx.canvas.dataset.categories);
    const budgets = JSON.parse(ctx.canvas.dataset.budgets);
    const spent = JSON.parse(ctx.canvas.dataset.spent);

    const data = {
        labels: categories,
        datasets: [
            {
                label: 'Budget',
                data: budgets,
                backgroundColor: 'rgba(45, 106, 79, 0.5)',
                borderColor: 'rgba(45, 106, 79, 1)',
                borderWidth: 1
            },
            {
                label: 'Spent',
                data: spent,
                backgroundColor: 'rgba(244, 65, 68, 0.5)',
                borderColor: 'rgba(244, 65, 68, 1)',
                borderWidth: 1
            }
        ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Amount'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Category'
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
});
