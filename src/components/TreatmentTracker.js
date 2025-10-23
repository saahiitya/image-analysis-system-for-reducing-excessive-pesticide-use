import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const TreatmentTracker = () => {
  const [treatments, setTreatments] = useState([]);
  const [newTreatment, setNewTreatment] = useState({
    crop_type: 'tomato',
    disease: '',
    pesticide: '',
    application_date: new Date().toISOString().split('T')[0],
    dosage: '',
    area_treated: '',
    cost: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    fetchTreatments();
  }, []);

  const fetchTreatments = async () => {
    try {
      // This would fetch from a treatments endpoint
      // For now, using mock data
      setTreatments([
        {
          id: 1,
          crop_type: 'tomato',
          disease: 'Early Blight',
          pesticide: 'Mancozeb',
          application_date: '2024-01-15',
          dosage: '2.5 kg/ha',
          area_treated: 2.0,
          cost: 1200,
          effectiveness: 4,
          notes: 'Applied during evening hours'
        },
        {
          id: 2,
          crop_type: 'brinjal',
          disease: 'Bacterial Wilt',
          pesticide: 'Streptomycin',
          application_date: '2024-01-10',
          dosage: '0.5 kg/ha',
          area_treated: 1.5,
          cost: 800,
          effectiveness: 5,
          notes: 'Soil drench application'
        }
      ]);
    } catch (error) {
      console.error('Failed to fetch treatments:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTreatment(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // This would submit to a treatments endpoint
      const treatmentData = {
        ...newTreatment,
        id: Date.now(), // Mock ID
        effectiveness: null // To be updated later
      };
      
      setTreatments(prev => [treatmentData, ...prev]);
      setNewTreatment({
        crop_type: 'tomato',
        disease: '',
        pesticide: '',
        application_date: new Date().toISOString().split('T')[0],
        dosage: '',
        area_treated: '',
        cost: '',
        notes: ''
      });
      setShowAddForm(false);
    } catch (error) {
      console.error('Failed to add treatment:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateEffectiveness = async (treatmentId, rating) => {
    try {
      setTreatments(prev => 
        prev.map(treatment => 
          treatment.id === treatmentId 
            ? { ...treatment, effectiveness: rating }
            : treatment
        )
      );
    } catch (error) {
      console.error('Failed to update effectiveness:', error);
    }
  };

  const getEffectivenessColor = (rating) => {
    if (rating >= 4) return 'excellent';
    if (rating >= 3) return 'good';
    if (rating >= 2) return 'fair';
    return 'poor';
  };

  const getTreatmentStatus = (date, effectiveness) => {
    const treatmentDate = new Date(date);
    const now = new Date();
    const daysDiff = Math.floor((now - treatmentDate) / (1000 * 60 * 60 * 24));

    if (effectiveness) return 'completed';
    if (daysDiff <= 7) return 'recent';
    if (daysDiff <= 14) return 'pending-evaluation';
    return 'overdue';
  };

  const calculateTotalCost = () => {
    return treatments.reduce((total, treatment) => total + (treatment.cost || 0), 0);
  };

  const calculateTotalArea = () => {
    return treatments.reduce((total, treatment) => total + (treatment.area_treated || 0), 0);
  };

  return (
    <div className="treatment-tracker">
      <div className="tracker-header">
        <h3>📋 Treatment Tracker</h3>
        <button 
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn-primary"
        >
          {showAddForm ? '❌ Cancel' : '➕ Add Treatment'}
        </button>
      </div>

      {/* Summary Cards */}
      <div className="treatment-summary">
        <div className="summary-card">
          <div className="summary-icon">🧪</div>
          <div className="summary-content">
            <h4>{treatments.length}</h4>
            <p>Total Treatments</p>
          </div>
        </div>
        
        <div className="summary-card">
          <div className="summary-icon">💰</div>
          <div className="summary-content">
            <h4>₹{calculateTotalCost().toLocaleString()}</h4>
            <p>Total Cost</p>
          </div>
        </div>
        
        <div className="summary-card">
          <div className="summary-icon">🌾</div>
          <div className="summary-content">
            <h4>{calculateTotalArea()} ha</h4>
            <p>Area Treated</p>
          </div>
        </div>
        
        <div className="summary-card">
          <div className="summary-icon">⭐</div>
          <div className="summary-content">
            <h4>
              {treatments.filter(t => t.effectiveness >= 4).length}/
              {treatments.filter(t => t.effectiveness).length}
            </h4>
            <p>Successful Treatments</p>
          </div>
        </div>
      </div>

      {/* Add Treatment Form */}
      {showAddForm && (
        <div className="add-treatment-form">
          <h4>➕ Add New Treatment</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="crop_type">Crop Type</label>
                <select
                  id="crop_type"
                  name="crop_type"
                  value={newTreatment.crop_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="tomato">🍅 Tomato</option>
                  <option value="brinjal">🍆 Brinjal</option>
                  <option value="capsicum">🌶️ Capsicum</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="disease">Disease</label>
                <input
                  type="text"
                  id="disease"
                  name="disease"
                  value={newTreatment.disease}
                  onChange={handleInputChange}
                  placeholder="e.g., Early Blight"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="pesticide">Pesticide Used</label>
                <input
                  type="text"
                  id="pesticide"
                  name="pesticide"
                  value={newTreatment.pesticide}
                  onChange={handleInputChange}
                  placeholder="e.g., Mancozeb"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="application_date">Application Date</label>
                <input
                  type="date"
                  id="application_date"
                  name="application_date"
                  value={newTreatment.application_date}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="dosage">Dosage</label>
                <input
                  type="text"
                  id="dosage"
                  name="dosage"
                  value={newTreatment.dosage}
                  onChange={handleInputChange}
                  placeholder="e.g., 2.5 kg/ha"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="area_treated">Area Treated (ha)</label>
                <input
                  type="number"
                  id="area_treated"
                  name="area_treated"
                  value={newTreatment.area_treated}
                  onChange={handleInputChange}
                  step="0.1"
                  min="0"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="cost">Cost (₹)</label>
                <input
                  type="number"
                  id="cost"
                  name="cost"
                  value={newTreatment.cost}
                  onChange={handleInputChange}
                  min="0"
                  required
                />
              </div>

              <div className="form-group full-width">
                <label htmlFor="notes">Notes (Optional)</label>
                <textarea
                  id="notes"
                  name="notes"
                  value={newTreatment.notes}
                  onChange={handleInputChange}
                  placeholder="Additional notes about the treatment..."
                  rows="3"
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Adding...' : '💾 Save Treatment'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Treatments List */}
      <div className="treatments-list">
        <h4>📜 Treatment History</h4>
        
        {treatments.length === 0 ? (
          <div className="empty-state">
            <p>No treatments recorded yet.</p>
            <p>Add your first treatment to start tracking!</p>
          </div>
        ) : (
          <div className="treatments-grid">
            {treatments.map((treatment) => (
              <div key={treatment.id} className="treatment-card">
                <div className="treatment-header">
                  <div className="treatment-crop">
                    <span className="crop-icon">
                      {treatment.crop_type === 'tomato' ? '🍅' : 
                       treatment.crop_type === 'brinjal' ? '🍆' : '🌶️'}
                    </span>
                    <span className="crop-name">{treatment.crop_type}</span>
                  </div>
                  
                  <div className={`treatment-status ${getTreatmentStatus(treatment.application_date, treatment.effectiveness)}`}>
                    {getTreatmentStatus(treatment.application_date, treatment.effectiveness).replace('-', ' ')}
                  </div>
                </div>

                <div className="treatment-details">
                  <div className="detail-row">
                    <span className="label">🦠 Disease:</span>
                    <span className="value">{treatment.disease}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="label">💊 Pesticide:</span>
                    <span className="value">{treatment.pesticide}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="label">📅 Date:</span>
                    <span className="value">{new Date(treatment.application_date).toLocaleDateString()}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="label">💉 Dosage:</span>
                    <span className="value">{treatment.dosage}</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="label">🌾 Area:</span>
                    <span className="value">{treatment.area_treated} ha</span>
                  </div>
                  
                  <div className="detail-row">
                    <span className="label">💰 Cost:</span>
                    <span className="value">₹{treatment.cost}</span>
                  </div>

                  {treatment.notes && (
                    <div className="treatment-notes">
                      <span className="label">📝 Notes:</span>
                      <p>{treatment.notes}</p>
                    </div>
                  )}
                </div>

                {/* Effectiveness Rating */}
                <div className="effectiveness-section">
                  <span className="label">⭐ Effectiveness:</span>
                  <div className="rating-buttons">
                    {[1, 2, 3, 4, 5].map((rating) => (
                      <button
                        key={rating}
                        onClick={() => updateEffectiveness(treatment.id, rating)}
                        className={`rating-btn ${treatment.effectiveness === rating ? 'active' : ''} ${getEffectivenessColor(rating)}`}
                      >
                        {rating}
                      </button>
                    ))}
                  </div>
                  {treatment.effectiveness && (
                    <span className={`effectiveness-text ${getEffectivenessColor(treatment.effectiveness)}`}>
                      {treatment.effectiveness >= 4 ? 'Excellent' :
                       treatment.effectiveness >= 3 ? 'Good' :
                       treatment.effectiveness >= 2 ? 'Fair' : 'Poor'}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TreatmentTracker;