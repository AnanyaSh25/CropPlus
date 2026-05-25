const ctx = document.getElementById('sensorChart').getContext('2d');
let sensorData = { temp: [], moisture: [], labels: [] };

const liveChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: sensorData.labels,
        datasets: [
            { label: 'Temp (°C)', data: sensorData.temp, borderColor: 'red', fill: false },
            { label: 'Moisture (%)', data: sensorData.moisture, borderColor: 'blue', fill: false }
        ]
    },
    options: { responsive: true }
});

// Function to fetch data from your Python API every 3 seconds
setInterval(async () => {
    const response = await fetch('/api/sensors');
    const data = await response.json();
    
    const now = new Date().toLocaleTimeString();
    
    // Add new data
    liveChart.data.labels.push(now);
    liveChart.data.datasets[0].data.push(data.temp);
    liveChart.data.datasets[1].data.push(data.moisture);

    // Keep only the last 10 readings so the chart doesn't get crowded
    if(liveChart.data.labels.length > 10) {
        liveChart.data.labels.shift();
        liveChart.data.datasets[0].data.shift();
        liveChart.data.datasets[1].data.shift();
    }

    liveChart.update();
}, 3000);