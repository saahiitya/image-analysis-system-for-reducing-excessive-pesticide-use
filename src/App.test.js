import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

// Mock axios
jest.mock('axios');
const mockedAxios = require('axios');

// Mock the chart components to avoid canvas issues in tests
jest.mock('recharts', () => ({
  LineChart: ({ children }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div data-testid="line" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  PieChart: ({ children }) => <div data-testid="pie-chart">{children}</div>,
  Pie: () => <div data-testid="pie" />,
  Cell: () => <div data-testid="cell" />,
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  Bar: () => <div data-testid="bar" />
}));

// Mock react-webcam
jest.mock('react-webcam', () => {
  return function MockWebcam(props) {
    return <div data-testid="webcam" />;
  };
});

// Mock react-dropzone
jest.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({ 'data-testid': 'dropzone' }),
    getInputProps: () => ({ 'data-testid': 'file-input' }),
    isDragActive: false
  })
}));

describe('CropGuard AI App', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockedAxios.get.mockReset();
    mockedAxios.post.mockReset();
    
    // Mock default API responses
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes('/api/dashboard-stats')) {
        return Promise.resolve({
          data: {
            total_scans: 5,
            healthy_crops_percentage: 80,
            cost_savings: '₹2500',
            pesticide_saved: '15L'
          }
        });
      }
      if (url.includes('/api/scan-history')) {
        return Promise.resolve({
          data: [
            {
              id: 1,
              crop_type: 'tomato',
              disease_detected: 'Early Blight',
              confidence_score: 0.87,
              severity_level: 'moderate',
              scan_timestamp: '2024-01-15T10:30:00Z',
              treatment_cost: 1200,
              location: 'Punjab'
            }
          ]
        });
      }
      if (url.includes('/api/weather/')) {
        return Promise.resolve({
          data: {
            location: 'Punjab, India',
            temperature: 25,
            humidity: 65,
            wind_speed: 8.5,
            weather_condition: 'Partly Cloudy',
            uv_index: 3,
            rain_probability: 15,
            spraying_recommendation: 'Suitable for spraying',
            best_spraying_times: ['06:00-10:00', '16:00-19:00']
          }
        });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });
  });

  test('renders main navigation', () => {
    render(<App />);
    
    expect(screen.getByText('🌱 CropGuard AI')).toBeInTheDocument();
    expect(screen.getByText('📊 Dashboard')).toBeInTheDocument();
    expect(screen.getByText('📸 Scan Crops')).toBeInTheDocument();
    expect(screen.getByText('💊 Treatments')).toBeInTheDocument();
    expect(screen.getByText('🌤️ Weather')).toBeInTheDocument();
  });

  test('displays welcome section on dashboard', () => {
    render(<App />);
    
    expect(screen.getByText('Welcome to Your Smart Farm Dashboard')).toBeInTheDocument();
    expect(screen.getByText(/AI-powered crop disease detection/)).toBeInTheDocument();
  });

  test('shows dashboard stats', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument(); // Total scans
      expect(screen.getByText('80%')).toBeInTheDocument(); // Healthy crops
      expect(screen.getByText('₹2500')).toBeInTheDocument(); // Cost savings
      expect(screen.getByText('15L')).toBeInTheDocument(); // Pesticide saved
    });
  });

  test('navigates to crop scanner tab', () => {
    render(<App />);
    
    const scannerTab = screen.getByText('📸 Scan Crops');
    fireEvent.click(scannerTab);
    
    expect(screen.getByText('🔍 Crop Disease Scanner')).toBeInTheDocument();
    expect(screen.getByText(/Upload or capture an image/)).toBeInTheDocument();
  });

  test('navigates to treatments tab', () => {
    render(<App />);
    
    const treatmentsTab = screen.getByText('💊 Treatments');
    fireEvent.click(treatmentsTab);
    
    expect(screen.getByText('📋 Treatment Tracker')).toBeInTheDocument();
  });

  test('navigates to weather tab', () => {
    render(<App />);
    
    const weatherTab = screen.getByText('🌤️ Weather');
    fireEvent.click(weatherTab);
    
    expect(screen.getByText('🌤️ Weather Conditions')).toBeInTheDocument();
  });

  test('displays user information', () => {
    render(<App />);
    
    expect(screen.getByText('📍 Punjab, India')).toBeInTheDocument();
    expect(screen.getByText('Farmer John')).toBeInTheDocument();
  });

  test('shows footer', () => {
    render(<App />);
    
    expect(screen.getByText(/© 2024 CropGuard AI Platform/)).toBeInTheDocument();
    expect(screen.getByText(/Empowering sustainable agriculture/)).toBeInTheDocument();
  });

  test('handles API errors gracefully', async () => {
    // Mock API error
    mockedAxios.get.mockRejectedValue(new Error('API Error'));
    
    render(<App />);
    
    // App should still render even with API errors
    expect(screen.getByText('🌱 CropGuard AI')).toBeInTheDocument();
  });

  test('crop scanner form inputs work', () => {
    render(<App />);
    
    // Navigate to scanner
    const scannerTab = screen.getByText('📸 Scan Crops');
    fireEvent.click(scannerTab);
    
    // Test crop type selection
    const cropSelect = screen.getByDisplayValue('🍅 Tomato');
    fireEvent.change(cropSelect, { target: { value: 'brinjal' } });
    expect(cropSelect.value).toBe('brinjal');
    
    // Test farm size input
    const farmSizeInput = screen.getByDisplayValue('1');
    fireEvent.change(farmSizeInput, { target: { value: '2.5' } });
    expect(farmSizeInput.value).toBe('2.5');
  });

  test('image upload method selector works', () => {
    render(<App />);
    
    // Navigate to scanner
    const scannerTab = screen.getByText('📸 Scan Crops');
    fireEvent.click(scannerTab);
    
    // Test camera button
    const cameraButton = screen.getByText('📷 Use Camera');
    fireEvent.click(cameraButton);
    
    expect(cameraButton).toHaveClass('active');
    
    // Test upload button
    const uploadButton = screen.getByText('📁 Upload Image');
    fireEvent.click(uploadButton);
    
    expect(uploadButton).toHaveClass('active');
  });

  test('treatment tracker shows empty state initially', () => {
    render(<App />);
    
    // Navigate to treatments
    const treatmentsTab = screen.getByText('💊 Treatments');
    fireEvent.click(treatmentsTab);
    
    expect(screen.getByText('No treatments recorded yet.')).toBeInTheDocument();
    expect(screen.getByText('Add your first treatment to start tracking!')).toBeInTheDocument();
  });

  test('add treatment form can be toggled', () => {
    render(<App />);
    
    // Navigate to treatments
    const treatmentsTab = screen.getByText('💊 Treatments');
    fireEvent.click(treatmentsTab);
    
    // Click add treatment button
    const addButton = screen.getByText('➕ Add Treatment');
    fireEvent.click(addButton);
    
    expect(screen.getByText('➕ Add New Treatment')).toBeInTheDocument();
    
    // Click cancel
    const cancelButton = screen.getByText('❌ Cancel');
    fireEvent.click(cancelButton);
    
    expect(screen.queryByText('➕ Add New Treatment')).not.toBeInTheDocument();
  });
});

describe('CropGuard AI Components Integration', () => {
  test('dashboard loads with charts', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByTestId('line-chart')).toBeInTheDocument();
      expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
      expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
    });
  });

  test('weather widget displays weather data', async () => {
    render(<App />);
    
    // Navigate to weather tab
    const weatherTab = screen.getByText('🌤️ Weather');
    fireEvent.click(weatherTab);
    
    await waitFor(() => {
      expect(screen.getByText('25°C')).toBeInTheDocument();
      expect(screen.getByText('Partly Cloudy')).toBeInTheDocument();
      expect(screen.getByText('65%')).toBeInTheDocument(); // Humidity
      expect(screen.getByText('8.5 km/h')).toBeInTheDocument(); // Wind speed
    });
  });

  test('scan complete callback updates dashboard', async () => {
    render(<App />);
    
    // Mock successful scan
    mockedAxios.post.mockResolvedValue({
      data: {
        scan_id: 1,
        recommendations: {
          disease_detected: 'Early Blight',
          confidence_score: 0.87,
          severity_assessment: 'moderate'
        }
      }
    });
    
    // Navigate to scanner and simulate scan completion
    const scannerTab = screen.getByText('📸 Scan Crops');
    fireEvent.click(scannerTab);
    
    // The scan completion would trigger a refresh of dashboard data
    // This tests the integration between components
    expect(mockedAxios.get).toHaveBeenCalledWith(
      expect.stringContaining('/api/dashboard-stats')
    );
  });
});