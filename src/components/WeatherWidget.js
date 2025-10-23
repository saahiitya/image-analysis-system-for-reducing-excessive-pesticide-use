import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const WeatherWidget = ({ location = 'Default Location' }) => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchWeatherData();
  }, [location]);

  const fetchWeatherData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/weather/${encodeURIComponent(location)}`);
      setWeatherData(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch weather data');
      console.error('Weather API error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSprayingRecommendationColor = (recommendation) => {
    if (recommendation.toLowerCase().includes('suitable')) return 'good';
    if (recommendation.toLowerCase().includes('caution')) return 'caution';
    return 'poor';
  };

  const getWeatherIcon = (condition) => {
    const icons = {
      'sunny': '☀️',
      'partly cloudy': '⛅',
      'cloudy': '☁️',
      'rainy': '🌧️',
      'stormy': '⛈️',
      'foggy': '🌫️',
      'windy': '💨'
    };
    return icons[condition.toLowerCase()] || '🌤️';
  };

  if (loading) {
    return (
      <div className="weather-widget loading">
        <div className="loading-spinner"></div>
        <p>Loading weather data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="weather-widget error">
        <p>⚠️ {error}</p>
        <button onClick={fetchWeatherData} className="retry-btn">
          🔄 Retry
        </button>
      </div>
    );
  }

  return (
    <div className="weather-widget">
      <div className="weather-header">
        <h4>🌤️ Weather Conditions</h4>
        <button onClick={fetchWeatherData} className="refresh-btn" title="Refresh weather data">
          🔄
        </button>
      </div>

      <div className="weather-main">
        <div className="temperature-section">
          <div className="weather-icon">
            {getWeatherIcon(weatherData.weather_condition)}
          </div>
          <div className="temperature">
            <span className="temp-value">{weatherData.temperature}°C</span>
            <span className="temp-condition">{weatherData.weather_condition}</span>
          </div>
        </div>

        <div className="weather-details">
          <div className="weather-item">
            <span className="weather-label">💧 Humidity:</span>
            <span className="weather-value">{weatherData.humidity}%</span>
          </div>
          
          <div className="weather-item">
            <span className="weather-label">💨 Wind:</span>
            <span className="weather-value">{weatherData.wind_speed} km/h</span>
          </div>
          
          <div className="weather-item">
            <span className="weather-label">☀️ UV Index:</span>
            <span className="weather-value">{weatherData.uv_index}</span>
          </div>
          
          <div className="weather-item">
            <span className="weather-label">🌧️ Rain:</span>
            <span className="weather-value">{weatherData.rain_probability}%</span>
          </div>
        </div>
      </div>

      {/* Spraying Recommendations */}
      <div className="spraying-recommendations">
        <h5>🚿 Spraying Conditions</h5>
        <div className={`spray-status ${getSprayingRecommendationColor(weatherData.spraying_recommendation)}`}>
          <span className="status-indicator"></span>
          {weatherData.spraying_recommendation}
        </div>
        
        <div className="best-times">
          <p><strong>⏰ Best Spraying Times:</strong></p>
          <div className="time-slots">
            {weatherData.best_spraying_times.map((time, index) => (
              <span key={index} className="time-slot">
                {time}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Weather Alerts */}
      <div className="weather-alerts">
        {weatherData.rain_probability > 50 && (
          <div className="alert rain-alert">
            ⚠️ High chance of rain - Avoid spraying today
          </div>
        )}
        
        {weatherData.wind_speed > 15 && (
          <div className="alert wind-alert">
            💨 High wind speed - Risk of pesticide drift
          </div>
        )}
        
        {weatherData.temperature > 35 && (
          <div className="alert heat-alert">
            🌡️ High temperature - Spray during cooler hours
          </div>
        )}
        
        {weatherData.humidity > 80 && (
          <div className="alert humidity-alert">
            💧 High humidity - Good for disease development
          </div>
        )}
      </div>

      {/* 5-Day Forecast Preview */}
      <div className="forecast-preview">
        <h5>📅 5-Day Outlook</h5>
        <div className="forecast-items">
          {/* This would be populated with actual forecast data */}
          <div className="forecast-item">
            <span className="day">Tomorrow</span>
            <span className="icon">⛅</span>
            <span className="temp">28°C</span>
          </div>
          <div className="forecast-item">
            <span className="day">Thu</span>
            <span className="icon">🌧️</span>
            <span className="temp">24°C</span>
          </div>
          <div className="forecast-item">
            <span className="day">Fri</span>
            <span className="icon">☀️</span>
            <span className="temp">30°C</span>
          </div>
          <div className="forecast-item">
            <span className="day">Sat</span>
            <span className="icon">⛅</span>
            <span className="temp">27°C</span>
          </div>
          <div className="forecast-item">
            <span className="day">Sun</span>
            <span className="icon">☁️</span>
            <span className="temp">25°C</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WeatherWidget;