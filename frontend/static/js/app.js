// CropGuard AI - Main JavaScript Application

class CropGuardApp {
    constructor() {
        this.fileInput = document.getElementById('fileInput');
        this.preview = document.getElementById('preview');
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.cameraSection = document.getElementById('cameraSection');
        this.loading = document.getElementById('loading');
        this.analysisResults = document.getElementById('analysisResults');
        
        this.stream = null;
        this.capturedImages = [];
        this.currentLocation = null;
        this.apiBaseUrl = '/api/v1';
        
        this.initializeEventListeners();
        this.loadInitialData();
    }
    
    initializeEventListeners() {
        // File upload handling
        document.querySelector('.upload-box').addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.fileInput.addEventListener('change', () => {
            this.displayImages();
        });
        
        // Camera functionality
        document.getElementById('cameraBtn').addEventListener('click', () => {
            this.openCamera();
        });
        
        document.getElementById('captureBtn').addEventListener('click', () => {
            this.capturePhoto();
        });
        
        document.getElementById('stopCameraBtn').addEventListener('click', () => {
            this.stopCamera();
        });
        
        // Location functionality
        document.getElementById('locationBtn').addEventListener('click', () => {
            this.getCurrentLocation();
        });
        
        // Weather update
        document.getElementById('weatherBtn').addEventListener('click', () => {
            this.updateWeather();
        });
        
        // AI Analysis
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzeImages();
        });
        
        // Drag and drop functionality
        this.setupDragAndDrop();
    }
    
    setupDragAndDrop() {
        const uploadBox = document.querySelector('.upload-box');
        
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.style.backgroundColor = '#cef0d8';
        });
        
        uploadBox.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadBox.style.backgroundColor = '';
        });
        
        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.style.backgroundColor = '';
            
            const files = Array.from(e.dataTransfer.files);
            const imageFiles = files.filter(file => file.type.startsWith('image/'));
            
            if (imageFiles.length > 0) {
                // Create a new FileList-like object
                const dt = new DataTransfer();
                imageFiles.forEach(file => dt.items.add(file));
                this.fileInput.files = dt.files;
                this.displayImages();
            }
        });
    }
    
    displayImages() {
        this.preview.innerHTML = '';
        Array.from(this.fileInput.files).forEach(file => {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.title = file.name;
            img.addEventListener('click', () => this.showImageModal(img.src, file.name));
            this.preview.appendChild(img);
        });
    }
    
    showImageModal(src, title) {
        // Create modal for image preview
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            cursor: pointer;
        `;
        
        const img = document.createElement('img');
        img.src = src;
        img.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            border-radius: 8px;
        `;
        
        modal.appendChild(img);
        modal.addEventListener('click', () => document.body.removeChild(modal));
        document.body.appendChild(modal);
    }
    
    async openCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    facingMode: 'environment',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            this.video.srcObject = this.stream;
            this.cameraSection.style.display = 'block';
            
            // Update button state
            document.getElementById('cameraBtn').innerHTML = '📹 Camera Active';
            document.getElementById('cameraBtn').style.backgroundColor = '#1f7a3a';
            document.getElementById('cameraBtn').style.color = '#fff';
            
        } catch (err) {
            console.error('Camera access error:', err);
            this.showNotification('Camera access denied or not available: ' + err.message, 'error');
        }
    }
    
    capturePhoto() {
        if (!this.stream) {
            this.showNotification('Camera not active', 'error');
            return;
        }
        
        const context = this.canvas.getContext('2d');
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        context.drawImage(this.video, 0, 0);
        
        // Convert to blob and add to captured images
        this.canvas.toBlob(blob => {
            const file = new File([blob], `captured_${Date.now()}.jpg`, { type: 'image/jpeg' });
            this.capturedImages.push(file);
            
            // Display captured image
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.title = file.name;
            img.addEventListener('click', () => this.showImageModal(img.src, file.name));
            this.preview.appendChild(img);
            
            this.showNotification('Photo captured successfully!', 'success');
        }, 'image/jpeg', 0.8);
    }
    
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.cameraSection.style.display = 'none';
        
        // Reset button state
        document.getElementById('cameraBtn').innerHTML = '📹 Open Camera';
        document.getElementById('cameraBtn').style.backgroundColor = '#eeeef1';
        document.getElementById('cameraBtn').style.color = '#1f7a3a';
    }
    
    getCurrentLocation() {
        if (!navigator.geolocation) {
            this.showNotification('Geolocation is not supported by this browser', 'error');
            return;
        }
        
        const locationBtn = document.getElementById('locationBtn');
        locationBtn.innerHTML = '📍 Getting Location...';
        
        navigator.geolocation.getCurrentPosition(
            position => {
                this.currentLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                
                locationBtn.innerHTML = '✅ Location Set';
                locationBtn.style.backgroundColor = '#1f7a3a';
                locationBtn.style.color = '#fff';
                
                this.showNotification('Location captured successfully!', 'success');
            },
            error => {
                locationBtn.innerHTML = '📍 Get Location';
                let errorMessage = 'Location access failed';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Location access denied by user';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Location information unavailable';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'Location request timed out';
                        break;
                }
                
                this.showNotification(errorMessage, 'error');
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000
            }
        );
    }
    
    async updateWeather() {
        const weatherBtn = document.getElementById('weatherBtn');
        const originalText = weatherBtn.innerHTML;
        weatherBtn.innerHTML = '🌤 Updating...';
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/weather`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const weather = await response.json();
            this.updateWeatherDisplay(weather);
            
            weatherBtn.innerHTML = '✅ Weather Updated';
            weatherBtn.style.backgroundColor = '#1f7a3a';
            weatherBtn.style.color = '#fff';
            
            this.showNotification('Weather updated successfully!', 'success');
            
        } catch (error) {
            console.error('Weather update failed:', error);
            weatherBtn.innerHTML = originalText;
            this.showNotification('Weather update failed: ' + error.message, 'error');
        }
    }
    
    updateWeatherDisplay(weather) {
        const weatherCard = document.querySelector('.upload-right .card:nth-child(2)');
        if (weatherCard) {
            weatherCard.innerHTML = `
                <h4>🌤 Weather Conditions</h4>
                <p><strong>${weather.temperature}°C</strong> ${weather.condition}</p>
                <p class="small-text">Humidity: ${weather.humidity}% | Wind: ${weather.wind_speed} km/h</p>
                <p class="small-text">UV Index: ${weather.uv_index} | Rain: ${weather.rain_probability}%</p>
            `;
        }
        
        const sprayCard = document.querySelector('.upload-right .card:nth-child(3)');
        if (sprayCard) {
            const suitabilityClass = weather.spray_recommendation.suitable ? 'completed' : 'highlight-warning';
            const suitabilityText = weather.spray_recommendation.suitable ? 'Suitable for Spraying' : 'Caution Advised';
            const recommendation = weather.spray_recommendation.suitable ? 
                'Good conditions for pesticide application.' : 
                'Not recommended, wait for better conditions.';
            
            sprayCard.innerHTML = `
                <h4>⚠ Spraying Conditions</h4>
                <span class="${suitabilityClass}">${suitabilityText}</span>
                <p>${recommendation}</p>
                <p class="small-text"><strong>Best Time:</strong> ${weather.spray_recommendation.best_time}</p>
                <p class="small-text">${weather.spray_recommendation.warning}</p>
            `;
        }
    }
    
    async analyzeImages() {
        const cropType = document.getElementById('cropType').value;
        const areaHectares = parseFloat(document.getElementById('areaInput').value);
        
        // Validation
        if (cropType === 'Select crop type...') {
            this.showNotification('Please select a crop type', 'error');
            return;
        }
        
        if (!areaHectares || areaHectares <= 0) {
            this.showNotification('Please enter a valid farm area', 'error');
            return;
        }
        
        // Combine uploaded files and captured images
        const allFiles = [...Array.from(this.fileInput.files), ...this.capturedImages];
        
        if (allFiles.length === 0) {
            this.showNotification('Please upload images or capture photos', 'error');
            return;
        }
        
        // Show loading
        this.loading.style.display = 'block';
        this.analysisResults.style.display = 'none';
        
        const analyzeBtn = document.getElementById('analyzeBtn');
        const originalText = analyzeBtn.innerHTML;
        analyzeBtn.innerHTML = '🤖 Analyzing...';
        analyzeBtn.disabled = true;
        
        try {
            const formData = new FormData();
            formData.append('crop_type', cropType);
            formData.append('area_hectares', areaHectares);
            
            allFiles.forEach(file => {
                formData.append('files', file);
            });
            
            const response = await fetch(`${this.apiBaseUrl}/analyze-crop`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.displayAnalysisResults(result);
                this.updateDashboardStats(result);
                this.showNotification('Analysis completed successfully!', 'success');
            } else {
                throw new Error(result.detail || 'Analysis failed');
            }
            
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showNotification('Analysis failed: ' + error.message, 'error');
        } finally {
            this.loading.style.display = 'none';
            analyzeBtn.innerHTML = originalText;
            analyzeBtn.disabled = false;
        }
    }
    
    displayAnalysisResults(result) {
        this.analysisResults.innerHTML = '';
        this.analysisResults.style.display = 'block';
        
        // Add summary header
        const summaryCard = document.createElement('div');
        summaryCard.className = 'result-card';
        summaryCard.innerHTML = `
            <h3>📊 Analysis Summary</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 15px 0;">
                <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 8px;">
                    <strong>${result.total_images}</strong><br>
                    <small>Images Analyzed</small>
                </div>
                <div style="text-align: center; padding: 10px; background: #d4edda; border-radius: 8px;">
                    <strong>${result.summary.healthy_count}</strong><br>
                    <small>Healthy Plants</small>
                </div>
                <div style="text-align: center; padding: 10px; background: #fff3cd; border-radius: 8px;">
                    <strong>${result.summary.diseased_count}</strong><br>
                    <small>Need Treatment</small>
                </div>
                <div style="text-align: center; padding: 10px; background: #e3f2fd; border-radius: 8px;">
                    <strong>${result.summary.health_percentage}%</strong><br>
                    <small>Overall Health</small>
                </div>
            </div>
        `;
        this.analysisResults.appendChild(summaryCard);
        
        // Add individual results
        result.results.forEach((imageResult, index) => {
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            
            const detection = imageResult.detection;
            const isHealthy = detection.disease_name === 'Healthy';
            
            resultCard.innerHTML = `
                <h3>📷 Image ${index + 1}: ${imageResult.filename}</h3>
                <div style="display: flex; gap: 20px; align-items: flex-start; margin: 15px 0;">
                    <img src="data:image/jpeg;base64,${imageResult.image_base64}" 
                         style="width: 200px; height: 150px; object-fit: cover; border-radius: 8px; cursor: pointer;"
                         onclick="app.showImageModal('data:image/jpeg;base64,${imageResult.image_base64}', '${imageResult.filename}')">
                    <div style="flex: 1;">
                        <div class="disease-info ${isHealthy ? 'healthy' : ''}">
                            <h4>${detection.disease_name}</h4>
                            <p>${detection.description}</p>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-top: 10px;">
                                <div><strong>Confidence:</strong> ${(detection.confidence * 100).toFixed(1)}%</div>
                                ${!isHealthy ? `
                                    <div><strong>Severity:</strong> ${detection.severity.toUpperCase()}</div>
                                    <div><strong>Affected:</strong> ${detection.affected_area_percentage}%</div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                </div>
                
                ${imageResult.pesticide_recommendations.length > 0 ? `
                    <h4>💊 Recommended Treatments</h4>
                    <div style="display: grid; gap: 15px;">
                        ${imageResult.pesticide_recommendations.map((pesticide, idx) => `
                            <div class="pesticide-recommendation">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                    <h5 style="margin: 0;">${pesticide.name}</h5>
                                    <span style="background: #1f7a3a; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                        Option ${idx + 1}
                                    </span>
                                </div>
                                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 10px;">
                                    <div><strong>Dosage:</strong> ${pesticide.dosage}</div>
                                    <div><strong>Application:</strong> ${pesticide.application_rate}</div>
                                    <div><strong>Mode:</strong> ${pesticide.mode_of_action}</div>
                                </div>
                                <div class="cost-info">
                                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px;">
                                        <div><strong>Amount:</strong> ${pesticide.pesticide_amount} ${pesticide.unit}</div>
                                        <div><strong>Water:</strong> ${pesticide.water_needed} L</div>
                                        <div><strong>Total Cost:</strong> <span style="color: #1f7a3a; font-size: 18px;">₹${pesticide.total_cost}</span></div>
                                    </div>
                                </div>
                                ${pesticide.precautions ? `
                                    <div style="margin-top: 10px; padding: 8px; background: #fff3cd; border-radius: 4px; font-size: 14px;">
                                        <strong>⚠️ Precautions:</strong> ${pesticide.precautions.slice(0, 2).join(', ')}
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : '<p style="color: #1f7a3a; font-weight: 600; text-align: center; padding: 20px; background: #d4edda; border-radius: 8px;">✅ No treatment needed - Crop is healthy!</p>'}
            `;
            
            this.analysisResults.appendChild(resultCard);
        });
    }
    
    updateDashboardStats(result) {
        const statCards = document.querySelectorAll('.stat-card');
        
        // Total scans
        const totalScans = parseInt(statCards[0].querySelector('h3').textContent) + result.total_images;
        statCards[0].querySelector('h3').textContent = totalScans;
        statCards[0].classList.add('stats-update');
        
        // Healthy percentage
        const healthyPercentage = result.summary.health_percentage;
        statCards[1].querySelector('h3').textContent = healthyPercentage + '%';
        statCards[1].classList.add('stats-update');
        
        // Active treatments
        const activeCount = result.summary.diseased_count;
        const currentActive = parseInt(statCards[2].querySelector('h3').textContent);
        statCards[2].querySelector('h3').textContent = currentActive + activeCount;
        statCards[2].classList.add('stats-update');
        
        // Calculate cost savings
        const totalCost = result.results.reduce((sum, r) => {
            return sum + (r.pesticide_recommendations.length > 0 ? r.pesticide_recommendations[0].total_cost : 0);
        }, 0);
        const savings = Math.round(totalCost * 0.3);
        const currentSavings = parseFloat(statCards[3].querySelector('h3').textContent.replace('₹', '') || '0');
        statCards[3].querySelector('h3').textContent = '₹' + (currentSavings + savings);
        statCards[3].classList.add('stats-update');
        
        // Update environmental impact
        this.updateEnvironmentalImpact(savings, totalCost);
        
        // Remove animation after delay
        setTimeout(() => {
            statCards.forEach(card => card.classList.remove('stats-update'));
        }, 500);
    }
    
    updateEnvironmentalImpact(savings, totalCost) {
        const envCard = document.querySelector('.environmental-impact');
        if (envCard) {
            const reductionPercent = totalCost > 0 ? Math.round((savings / (totalCost + savings)) * 100) : 0;
            
            envCard.innerHTML = `
                <h4>🌍 Environmental Impact</h4>
                <p>Pesticide Reduction <span class="completed">-${reductionPercent}%</span></p>
                <p>Water Usage <span style="color: #4677cc;">${Math.round(totalCost / 10)}L</span></p>
                <p>Cost Savings <span style="color:#1f7a3a;">₹${savings}</span></p>
                <hr />
                <p class="eco-practice" style="color:#1f7a3a; font-weight: 600; margin-top: 12px;">
                    ✔ Eco-Friendly Practices
                </p>
                <p>You're contributing to sustainable farming!</p>
            `;
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            max-width: 300px;
            animation: slideIn 0.3s ease-out;
        `;
        
        const colors = {
            success: '#1f7a3a',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    async loadInitialData() {
        // Load initial weather data
        await this.updateWeather();
        
        // Load scan history
        try {
            const response = await fetch(`${this.apiBaseUrl}/scan-history`);
            if (response.ok) {
                const history = await response.json();
                this.updateInitialStats(history);
            }
        } catch (error) {
            console.warn('Failed to load initial scan history:', error);
        }
    }
    
    updateInitialStats(history) {
        const statCards = document.querySelectorAll('.stat-card');
        
        if (statCards.length >= 4) {
            statCards[0].querySelector('h3').textContent = history.total_scans || 0;
            statCards[1].querySelector('h3').textContent = (history.healthy_percentage || 0) + '%';
            statCards[2].querySelector('h3').textContent = history.active_treatments || 0;
            statCards[3].querySelector('h3').textContent = '₹' + (history.cost_savings || 0);
        }
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new CropGuardApp();
});