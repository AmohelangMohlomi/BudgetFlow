const ctx = document.getElementById('savingsLineChart').getContext('2d');

  const savingsData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 
    datasets: [{
      label: 'Savings Over Time',
      data: [200, 400, 600, 800, 1000, 1200], 
      borderColor: 'rgba(45, 106, 79, 1)',
      backgroundColor: 'rgba(45, 106, 79, 0.2)',
      fill: true,
      tension: 0.3 // smooth curve
    }]
  };

  const config = {
    type: 'line',
    data: savingsData,
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Amount Saved (R)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Month'
          }
        }
      }
    }
  };

  new Chart(ctx, config);

