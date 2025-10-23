import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';

const API_BASE_URL = 'http://localhost:8000';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    stats: {},
    scanHistory: [],
    cropHealth: [],
    costAnalysis: []
  });
  const [loading, setLoading] = useState(true);
  const [selectedTimeRange, setSelectedTimeRange] = useState('30');

  useEffect(() => {
    fetchDashboardData();
  }, [selectedTimeRange]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsResponse, historyResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/dashboard-stats`),
        axios.get(`${API_BASE_URL}/api/scan-history?limit=50`)
      ]);

      setDashboardData({
        stats: statsResponse.data,
        scanHistory: historyResponse.data,
        cropHealth: generateCropHealthData(historyResponse.data),
        costAnalysis: generateCostAnalysisData(historyResponse.data)
      });
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateCropHealthData = (scanHistory) => {
    const healthData = {};
    scanHistory.forEach(scan => {
      const date = new Date(scan.scan_timestamp).toLocaleDateString();
      if (!healthData[date]) {
        healthData[date] = { date, healthy: 0, diseased: 0 };
      }
      if (scan.disease_detected === 'Healthy') {
        healthData[date].healthy++;
      } else {
        healthData[date].diseased++;
      }
    });
    return Object.values(healthData).slice(-7); // Last 7 days
  };

  const generateCostAnalysisData = (scanHistory) => {
    const costData = {};
    scanHistory.forEach(scan => {
      const month = new Date(scan.scan_timestamp).toLocaleDateString('en-US', { month: 'short' });
      if (!costData[month]) {
        costData[month] = { month, cost: 0, savings: 0 };
      }
      costData[month].cost += scan.treatment_cost || 0;
      costData[month].savings += (scan.treatment_cost || 0) * 0.3; // Estimated savings
    });
    return Object.values(costData);
  };

  const diseaseDistribution = dashboardData.scanHistory.reduce((acc, scan) => {
    const disease = scan.disease_detected;
    acc[disease] = (acc[disease] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(diseaseDistribution).map(([disease, count]) => ({
    name: disease,
    value: count
  }));

  const COLORS = ['#1f7a3a', '#ac8200', '#4677cc', '#e74c3c', '#9b59b6', '#f39c12'];

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Farm Analytics Dashboard</h2>
        <div className="time-range-selector">
          <select 
            value={selectedTimeRange} 
            onChange={(e) => setSelectedTimeRange(e.target.value)}
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 3 months</option>
            <option value="365">Last year</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">🌱</div>
          <div className="metric-content">
            <h3>{dashboardData.stats.total_scans || 0}</h3>
            <p>Total Scans</p>
            <span className="metric-trend positive">+12% this month</span>
          </div>
        </div>
        
        <div className="metric-card">
          <div className="metric-icon">💚</div>
          <div className="metric-content">
            <h3>{dashboardData.stats.healthy_crops_percentage || 0}%</h3>
            <p>Healthy Crops</p>
            <span className="metric-trend positive">+5% improvement</span>
          </div>
        </div>
        
        <div className="metric-card">
          <div className="metric-icon">💰</div>
          <div className="metric-content">
            <h3>{dashboardData.stats.cost_savings || '₹0'}</h3>
            <p>Cost Savings</p>
            <span className="metric-trend positive">+₹2,500 saved</span>
          </div>
        </div>
        
        <div className="metric-card">
          <div className="metric-icon">🌿</div>
          <div className="metric-content">
            <h3>{dashboardData.stats.pesticide_saved || '0L'}</h3>
            <p>Pesticide Saved</p>
            <span className="metric-trend positive">-25% usage</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Crop Health Trend */}
        <div className="chart-card">
          <h4>Crop Health Trend</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dashboardData.cropHealth}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="healthy" stroke="#1f7a3a" strokeWidth={3} />
              <Line type="monotone" dataKey="diseased" stroke="#e74c3c" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Disease Distribution */}
        <div className="chart-card">
          <h4>Disease Distribution</h4>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Cost Analysis */}
        <div className="chart-card full-width">
          <h4>Monthly Cost Analysis</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboardData.costAnalysis}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cost" fill="#4677cc" name="Treatment Cost" />
              <Bar dataKey="savings" fill="#1f7a3a" name="Savings" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="activity-section">
        <h4>Recent Activity</h4>
        <div className="activity-list">
          {dashboardData.scanHistory.slice(0, 5).map((scan, index) => (
            <div key={scan.id} className="activity-item">
              <div className="activity-icon">
                {scan.disease_detected === 'Healthy' ? '✅' : '⚠️'}
              </div>
              <div className="activity-content">
                <p><strong>{scan.crop_type}</strong> scan completed</p>
                <p className="activity-detail">
                  {scan.disease_detected} detected - {scan.severity_level} severity
                </p>
                <span className="activity-time">
                  {new Date(scan.scan_timestamp).toLocaleDateString()}
                </span>
              </div>
              <div className="activity-cost">
                ₹{scan.treatment_cost || 0}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="recommendations-section">
        <h4>Smart Recommendations</h4>
        <div className="recommendations-grid">
          <div className="recommendation-card">
            <div className="rec-icon">🌡️</div>
            <h5>Weather Alert</h5>
            <p>High humidity expected. Consider preventive fungicide application.</p>
          </div>
          
          <div className="recommendation-card">
            <div className="rec-icon">💡</div>
            <h5>Cost Optimization</h5>
            <p>Switch to copper-based fungicides to reduce costs by 15%.</p>
          </div>
          
          <div className="recommendation-card">
            <div className="rec-icon">🔄</div>
            <h5>Treatment Schedule</h5>
            <p>Next preventive spray recommended in 3 days.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;