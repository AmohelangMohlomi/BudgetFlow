const canvas = document.getElementById('budgetVsSpendingChart');
if (canvas) {
    const categories = JSON.parse(canvas.dataset.categories || '[]');
    const budgets = JSON.parse(canvas.dataset.budgets || '[]');
    const spent = JSON.parse(canvas.dataset.spent || '[]');

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [
                { label: 'Budgeted', data: budgets, backgroundColor: 'rgba(54, 162, 235, 0.6)' },
                { label: 'Spent', data: spent, backgroundColor: 'rgba(255, 99, 132, 0.6)' }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}
