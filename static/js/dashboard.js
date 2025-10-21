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


document.addEventListener("DOMContentLoaded", async () => {
  const adviceBox = document.getElementById("pennyAdvice");

  try {
    const response = await fetch("/get_penny_dashboard_advice", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    if (!response.ok) throw new Error("Failed to get advice");

    const data = await response.json();
    adviceBox.textContent = `Penny says: ${data.advice}`;
  } catch (error) {
    adviceBox.textContent = " Penny couldn't fetch your advice right now.";
    console.error(error);
  }
});

