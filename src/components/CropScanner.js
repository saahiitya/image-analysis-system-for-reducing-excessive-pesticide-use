import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const CropScanner = ({ onScanComplete }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cropType, setCropType] = useState('tomato');
  const [farmSize, setFarmSize] = useState(1.0);
  const [location, setLocation] = useState('');
  const [weatherConditions, setWeatherConditions] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [useCamera, setUseCamera] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const webcamRef = useRef(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      setError('');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    multiple: false
  });

  const captureImage = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      // Convert base64 to file
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], 'captured-image.jpg', { type: 'image/jpeg' });
          setSelectedFile(file);
          setUseCamera(false);
        });
    }
  }, [webcamRef]);

  const analyzeImage = async () => {
    if (!selectedFile) {
      setError('Please select or capture an image.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('crop_type', cropType);
    formData.append('farm_size', farmSize);
    formData.append('location', location);
    formData.append('weather_conditions', weatherConditions);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze-image`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setAnalysisResult(response.data);
      if (onScanComplete) {
        onScanComplete(response.data);
      }
    } catch (err) {
      setError('Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetScanner = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    setError('');
    setUseCamera(false);
  };

  return (
    <div className="crop-scanner">
      <div className="scanner-header">
        <h3>🔍 Crop Disease Scanner</h3>
        <p>Upload or capture an image of your crop for AI-powered disease detection</p>
      </div>

      {/* Form Inputs */}
      <div className="scanner-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="cropType">Crop Type</label>
            <select 
              id="cropType" 
              value={cropType} 
              onChange={(e) => setCropType(e.target.value)}
            >
              <option value="tomato">🍅 Tomato</option>
              <option value="brinjal">🍆 Brinjal (Eggplant)</option>
              <option value="capsicum">🌶️ Capsicum (Bell Pepper)</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="farmSize">Farm Size (hectares)</label>
            <input
              type="number"
              id="farmSize"
              value={farmSize}
              onChange={(e) => setFarmSize(parseFloat(e.target.value))}
              min="0.1"
              step="0.1"
              placeholder="e.g., 2.5"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="location">Location (Optional)</label>
            <input
              type="text"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Punjab, India"
            />
          </div>

          <div className="form-group">
            <label htmlFor="weather">Weather Conditions (Optional)</label>
            <select 
              id="weather" 
              value={weatherConditions} 
              onChange={(e) => setWeatherConditions(e.target.value)}
            >
              <option value="">Select weather</option>
              <option value="sunny">☀️ Sunny</option>
              <option value="cloudy">☁️ Cloudy</option>
              <option value="rainy">🌧️ Rainy</option>
              <option value="humid">💧 Humid</option>
              <option value="windy">💨 Windy</option>
            </select>
          </div>
        </div>
      </div>

      {/* Image Input Section */}
      <div className="image-input-section">
        <div className="input-method-selector">
          <button 
            className={!useCamera ? 'active' : ''}
            onClick={() => setUseCamera(false)}
          >
            📁 Upload Image
          </button>
          <button 
            className={useCamera ? 'active' : ''}
            onClick={() => setUseCamera(true)}
          >
            📷 Use Camera
          </button>
        </div>

        {useCamera ? (
          <div className="camera-section">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam-preview"
            />
            <button onClick={captureImage} className="capture-btn">
              📸 Capture Image
            </button>
          </div>
        ) : (
          <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
            <input {...getInputProps()} />
            {isDragActive ? (
              <p>Drop the image here...</p>
            ) : (
              <div className="dropzone-content">
                <div className="upload-icon">📤</div>
                <p>Drag and drop an image here, or click to select</p>
                <small>Supports JPG, PNG, BMP, TIFF formats</small>
              </div>
            )}
          </div>
        )}

        {selectedFile && (
          <div className="image-preview">
            <img 
              src={URL.createObjectURL(selectedFile)} 
              alt="Selected crop" 
              className="preview-image"
            />
            <div className="image-info">
              <p><strong>File:</strong> {selectedFile.name}</p>
              <p><strong>Size:</strong> {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="scanner-actions">
        <button 
          onClick={resetScanner}
          className="btn-secondary"
          disabled={loading}
        >
          🔄 Reset
        </button>
        
        <button 
          onClick={analyzeImage}
          className="btn-primary"
          disabled={!selectedFile || loading}
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Analyzing...
            </>
          ) : (
            '🔬 Analyze Image'
          )}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {/* Analysis Results */}
      {analysisResult && (
        <div className="analysis-results">
          <h4>📊 Analysis Results</h4>
          
          <div className="results-grid">
            <div className="result-card disease-info">
              <h5>🦠 Disease Detection</h5>
              <div className="disease-details">
                <p><strong>Disease:</strong> {analysisResult.recommendations.disease_detected}</p>
                <p><strong>Confidence:</strong> {(analysisResult.recommendations.confidence_score * 100).toFixed(1)}%</p>
                <p><strong>Severity:</strong> 
                  <span className={`severity-badge ${analysisResult.recommendations.severity_assessment.toLowerCase()}`}>
                    {analysisResult.recommendations.severity_assessment}
                  </span>
                </p>
              </div>
            </div>

            <div className="result-card treatment-info">
              <h5>💊 Treatment Recommendation</h5>
              <div className="treatment-details">
                <p><strong>Primary Pesticides:</strong></p>
                <ul>
                  {analysisResult.recommendations.recommended_treatment.primary_pesticides.map((pesticide, index) => (
                    <li key={index}>{pesticide}</li>
                  ))}
                </ul>
                <p><strong>Dosage:</strong> {analysisResult.recommendations.recommended_treatment.dosage_calculation.total_amount_needed}</p>
                <p><strong>Estimated Cost:</strong> {analysisResult.recommendations.recommended_treatment.dosage_calculation.cost_estimate}</p>
              </div>
            </div>

            <div className="result-card environmental-info">
              <h5>🌍 Environmental Impact</h5>
              <div className="environmental-details">
                <p><strong>Pesticide Reduction:</strong> {analysisResult.environmental_impact.pesticide_reduction}%</p>
                <p><strong>Water Usage:</strong> {analysisResult.environmental_impact.water_usage}L</p>
                <p><strong>Cost Savings:</strong> ₹{analysisResult.environmental_impact.cost_savings}</p>
              </div>
            </div>
          </div>

          {/* Prevention Tips */}
          <div className="prevention-tips">
            <h5>💡 Prevention Tips</h5>
            <ul>
              {analysisResult.recommendations.prevention_tips.map((tip, index) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </div>

          {/* Follow-up Schedule */}
          <div className="followup-schedule">
            <h5>📅 Follow-up Schedule</h5>
            <ul>
              {analysisResult.recommendations.follow_up_schedule.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default CropScanner;