import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cropType, setCropType] = useState('tomato');
  const [farmSize, setFarmSize] = useState(1.0);
  const [location, setLocation] = useState('');
  const [weatherConditions, setWeatherConditions] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [scanHistory, setScanHistory] = useState([]);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    fetchScanHistory();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const fetchScanHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/scan-history`);
      setScanHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch scan history:', err);
      setError('Failed to load scan history.');
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      streamRef.current = stream;
      setIsCameraActive(true);
      setSelectedFile(null);
      setError('');
    } catch (err) {
      console.error('Camera access denied or failed:', err);
      setError('Camera access failed. Please enable camera permissions.');
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
      
      canvas.toBlob(blob => {
        const file = new File([blob], "captured-image.jpg", { type: "image/jpeg" });
        setSelectedFile(file);
        stopCamera();
      }, 'image/jpeg');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsCameraActive(false);
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError('');
      stopCamera();
    }
  };

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
      setAnalysis(response.data);
      fetchScanHistory();
    } catch (err) {
      setError('Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPesticideColor = (pesticide) => {
    if (pesticide.toLowerCase().includes('copper')) return '#D2691E';
    if (pesticide.toLowerCase().includes('mancozeb')) return '#FFD700';
    if (pesticide.toLowerCase().includes('metalaxyl')) return '#ADD8E6';
    return '#333';
  };

  return (
    <div>
      <nav>
        <h1>🌱 CropGuard AI</h1>
        <div>
          <a href="#">Dashboard</a>
          <a href="#">Scan History</a>
          <a href="#">Recommendations</a>
          <a href="#">Settings</a>
        </div>
        <div>
          <span role="img" aria-label="notification">🔔</span>
          <span role="img" aria-label="profile">👤</span>
          Farmer John
        </div>
      </nav>

      <section className="welcome">
        <h2>Welcome to Your Smart Farm Dashboard</h2>
        <p>AI-powered crop disease detection for healthier harvests</p>
      </section>

      <div className="grid stats">
        <div className="stat-card stat-green"><h3>{scanHistory.length}</h3><p>Total Scans</p></div>
        <div className="stat-card stat-green"><h3>0%</h3><p>Healthy Crops</p></div>
        <div className="stat-card stat-yellow"><h3>0</h3><p>Active Treatments</p></div>
        <div className="stat-card stat-blue"><h3>0L</h3><p>Pesticide Saved</p></div>
      </div>

      <div className="upload-section">
        <div className="upload-left">
          <h3>📸 Scan Your Crops</h3>
          
          <label htmlFor="cropType" style={{fontWeight: 600, marginBottom: '8px', display:'block'}}>Crop Type</label>
          <select id="cropType" value={cropType} onChange={(e) => setCropType(e.target.value)}>
            <option value="tomato">Tomato</option>
            <option value="brinjal">Brinjal (Eggplant)</option>
            <option value="capsicum">Capsicum (Bell Pepper)</option>
          </select>

          {isCameraActive ? (
            <div className="camera-live">
              <video ref={videoRef} autoPlay playsInline className="video-stream"></video>
              <button onClick={captureImage} className="capture-btn">Capture Image</button>
            </div>
          ) : (
            <>
              <label className="upload-box" htmlFor="fileInput">
                Drag and drop your images here, or click to browse
              </label>
              <input type="file" id="fileInput" multiple accept="image/*" onChange={handleFileSelect} />
            </>
          )}
          
          <div className="images-preview" id="preview">
            {selectedFile && <img src={URL.createObjectURL(selectedFile)} alt="Preview" />}
          </div>
          {isCameraActive ? (
            <button className="upload-btns green" onClick={analyzeImage} disabled={!selectedFile || loading}>
              {loading ? 'Analyzing...' : 'Analyze Captured Image'}
            </button>
          ) : (
            <button className="upload-btns green" onClick={analyzeImage} disabled={!selectedFile || loading}>
              {loading ? 'Analyzing...' : 'Analyze Uploaded Image'}
            </button>
          )}

          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="upload-right">
          <div className="card">
            <h4>🕒 Recent Scans</h4>
            {scanHistory.length > 0 ? (
              <ul>
                {scanHistory.slice(0, 5).map(scan => (
                  <li key={scan.id}>
                    {scan.crop_type} - {scan.disease_detected} ({new Date(scan.scan_timestamp).toLocaleDateString()})
                  </li>
                ))}
              </ul>
            ) : (
              <p>No recent scans</p>
            )}
          </div>

          <div className="card">
            <h4>🌤 Weather Conditions</h4>
            <p><strong>25°C</strong> Partly Cloudy</p>
            <p className="small-text">Humidity: 42% | Wind: 8 km/h</p>
            <p className="small-text">UV Index: 3 | Rain: 4%</p>
          </div>

          <div className="card">
            <h4>⚠ Spraying Conditions</h4>
            <span className="highlight-warning">Caution Advised</span>
            <p>Not recommended, wait for better conditions.</p>
            <p className="small-text"><strong>Best Time:</strong> Morning (6-10 AM) / Evening (4-7 PM)</p>
          </div>
        </div>
      </div>

      {analysis && (
        <div className="grid" style={{gridTemplateColumns: '3fr 1.8fr', margin: '0 60px 80px 60px', gap: '36px'}}>
          <div className="card">
            <h4>📊 Treatment Progress</h4>
            <div style={{textAlign: 'center', margin: '60px 0', color: '#bcc9ce'}}>
              <div style={{fontSize: '34px'}}>📈</div>
              <div>Chart visualization would be implemented here</div>
            </div>
            <div className="grid" style={{gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px'}}>
              <div className="stat-card stat-green" style={{boxShadow:'none', padding: '20px 0'}}>
                <h3 style={{fontSize: '28px', marginBottom: '4px'}}>0</h3>
                <p>Completed</p>
              </div>
              <div className="stat-card stat-yellow" style={{boxShadow:'none', padding: '20px 0'}}>
                <h3 style={{fontSize: '28px', marginBottom: '4px'}}>0</h3>
                <p>Active</p>
              </div>
              <div className="stat-card stat-blue" style={{boxShadow:'none', padding: '20px 0'}}>
                <h3 style={{fontSize: '28px', marginBottom: '4px'}}>0</h3>
                <p>Total Treatments</p>
              </div>
            </div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: '26px'}}>
            <div className="card">
              <h4>🏥 Current Treatments</h4>
              <p>Disease: **{analysis.recommendations.disease_detected}**</p>
              <p>Severity: **{analysis.recommendations.severity_assessment}**</p>
              <p>Pesticides: {analysis.recommendations.recommended_treatment?.primary_pesticides.join(', ')}</p>
              <p>Dosage: **{analysis.recommendations.recommended_treatment?.dosage_calculation.total_amount_needed}**</p>
              <p>Cost: **{analysis.recommendations.recommended_treatment?.dosage_calculation.cost_estimate}**</p>
            </div>
            <div className="card environmental-impact">
              <h4>🌍 Environmental Impact</h4>
              <p>Pesticide Reduction <span className="completed">-0%</span></p>
              <p>Water Usage <span className="txt-blue">0L</span></p>
              <p>Cost Savings <span style={{color:'#1f7a3a'}}>₹0</span></p>
              <hr />
              <p className="eco-practice" style={{color:'#1f7a3a', fontWeight: 600, marginTop: '12px'}}>
                ✔ Eco-Friendly Practices
              </p>
              <p>You're contributing to sustainable farming!</p>
            </div>
          </div>
        </div>
      )}
      
    </div>
  );
}

export default App;