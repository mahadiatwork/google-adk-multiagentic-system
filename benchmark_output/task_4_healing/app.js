document.getElementById('get-weather-btn').addEventListener('click', function() {
    const city = document.getElementById('city-input').value;
    if (city) {
        fetchWeather(city);
    } else {
        displayResult('Please enter a city name.');
    }
});

function fetchWeather(city) {
    const mockWeatherData = {
        "London": { "temperature": "15°C", "description": "Cloudy", "color": "#87CEEB" },
        "New York": { "temperature": "20°C", "description": "Sunny", "color": "#FFD700" },
        "Paris": { "temperature": "18°C", "description": "Rainy", "color": "#ADD8E6" },
        "Tokyo": { "temperature": "22°C", "description": "Clear", "color": "#FFA07A" }
    };

    const weatherInfo = mockWeatherData[city];
    if (weatherInfo) {
        displayResult(`Temperature: ${weatherInfo.temperature}, Description: ${weatherInfo.description}`, weatherInfo.color);
    } else {
        displayResult('City not found in mock data.', '#FF6347');
    }
}

function displayResult(message, color = '#ffffff') {
    const resultDiv = document.getElementById('weather-result');
    resultDiv.textContent = message;
    resultDiv.style.color = color;
}