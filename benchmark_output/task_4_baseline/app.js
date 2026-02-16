document.addEventListener('DOMContentLoaded', () => {
    const weatherApp = document.getElementById('weather-app');

    // Mock API response
    const mockApiResponse = {
        temperature: '22°C',
        description: 'Sunny'
    };

    // Function to display weather data
    function displayWeather(data) {
        weatherApp.innerHTML = `
            <h1>Current Weather</h1>
            <p class="temperature">${data.temperature}</p>
            <p class="description">${data.description}</p>
        `;
    }

    // Fetch weather data from mock API
    function fetchWeather() {
        // Simulate fetching data from an API
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(mockApiResponse);
            }, 1000);
        });
    }

    // Initialize the app
    fetchWeather().then(displayWeather);
});