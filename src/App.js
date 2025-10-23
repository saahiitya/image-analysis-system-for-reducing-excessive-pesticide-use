import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Dashboard from './components/Dashboard';
import CropScanner from './components/CropScanner';
import WeatherWidget from './components/WeatherWidget';
import TreatmentTracker from './components/TreatmentTracker';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [scanHistory, setScanHistory] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({});
  const [userLocation, setUserLocation] = useState('Punjab, India');mRef = useRef(null);
  useEffect(() => {
    fetchScanHistory();
    fetchDashboardStats();
  }, []);

  const fetchScanHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/scan-history`);
      setScanHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch scan history:', err);
    }
  };

  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/dashboard-stats`);
      setDashboardStats(response.data);
    } catch (err) {
      console.error('Failed to fetch dashboard stats:', err);
    }
  };

  const handleScanComplete = (scanResult) => {
    // Refresh data after successful scan
    fetchScanHistory();
    fetchDashboardStats();
    // Switch to dashboard to show results
    setActiveTab('dashboard');
  };ry.');
    }
  }  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'scanner':
        return <CropScanner onScanComplete={handleScanComplete} />;
      case 'treatments':
        return <TreatmentTracker />;
      case 'weather':
        return <WeatherWidget location={userLocation} />;
      default:
        return <Dashboard />;
    }
  };pesticide.toLowerCase().includes('metalaxyl')) return '#ADD8E6';
    return '#333';
   return (
    <div className="app">
      {/* Navigation Header */}
      <nav className="main-nav">
        <div className="nav-brand">
          <h1>🌱 CropGuard AI</h1>
          <span className="nav-subtitle">Smart Farming Platform</span>
        </div>
        
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button 
            className={`nav-tab ${activeTab === 'scanner' ? 'active' : ''}`}
            onClick={() => setActiveTab('scanner')}
          >
            📸 Scan Crops
          </button>
          <button 
            className={`nav-tab ${activeTab === 'treatments' ? 'active' : ''}`}
            onClick={() => setActiveTab('treatments')}
          >
            💊 Treatments
          </button>
          <button 
            className={`nav-tab ${activeTab === 'weather' ? 'active' : ''}`}
            onClick={() => setActiveTab('weather')}
          >
            🌤️ Weather
          </button>
        </div>

        <div className="nav-user">
          <div className="user-location">
            📍 {userLocation}
          </div>
          <div className="user-profile">
            <span className="notification-icon">🔔</span>
            <span className="user-avatar">👤</span>
            <span className="user-name">Farmer John</span>
          </div>
        </div>
      </nav>

      {/* Welcome Section - Only show on dashboard */}
      {activeTab === 'dashboard' && (
        <section className="welcome-section">
          <div className="welcome-content">
            <h2>Welcome to Your Smart Farm Dashboard</h2>
            <p>AI-powered crop disease detection and pesticide management for sustainable farming</p>
          </div>
          
          {/* Quick Stats */}
          <div className="quick-stats">
            <div className="stat-item">
              <span className="stat-icon">🌱</span>
              <div className="stat-info">
                <h3>{dashboardStats.total_scans || 0}</h3>
                <p>Total Scans</p>
              </div>
            </div>
            <div className="stat-item">
              <span className="stat-icon">💚</span>
              <div className="stat-info">
                <h3>{dashboardStats.healthy_crops_percentage || 0}%</h3>
                <p>Healthy Crops</p>
              </div>
            </div>
            <div className="stat-item">
              <span className="stat-icon">💰</span>
              <div className="stat-info">
                <h3>{dashboardStats.cost_savings || '₹0'}</h3>
                <p>Cost Savings</p>
              </div>
            </div>
            <div className="stat-item">
              <span className="stat-icon">🌿</span>
              <div className="stat-info">
                <h3>{dashboardStats.pesticide_saved || '0L'}</h3>
                <p>Pesticide Saved</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Main Content Area */}
      <main className="main-content">
        {renderTabContent()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <p>&copy; 2024 CropGuard AI Platform. Empowering sustainable agriculture through AI.</p>
          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#support">Support</a>
            <a href="#privacy">Privacy</a>
          </div>
        </div>
      </footer>
    </div>
  );>
              <p>You're contributing to sustainable farming!</p>
            </div>
          </div>
        </div>
      )}
      
    </div>
  );
}

export default App;