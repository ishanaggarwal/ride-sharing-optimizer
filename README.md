# 🚗 Optimized Ride-Sharing (Carpooling) Algorithm

An intelligent ride-sharing system that efficiently matches multiple riders heading in similar directions to minimize total travel time and cost using advanced optimization methods and machine learning.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🧮 Smart Matching Algorithm**: Uses OR-Tools for constraint programming and route optimization
- **🤖 ML-Based Clustering**: K-means clustering for geographical grouping of riders
- **🗺️ Real-time Routing**: Dynamic route calculation considering multiple pickup/dropoff points
- **💰 Cost Optimization**: Minimizes total travel distance and time while maximizing carpooling efficiency
- **🎨 Beautiful Interactive UI**: Modern React interface with real-time map visualization
- **📊 Live Metrics**: Real-time statistics on savings, costs, and environmental impact
- **🌍 Environmental Impact**: Calculates CO₂ savings and efficiency improvements

## 🏗️ Architecture

### Backend (Python/Flask)
- Route optimization using Google OR-Tools
- K-means clustering for geographical grouping
- Traveling Salesman Problem (TSP) solver for optimal routes
- RESTful API with 4 endpoints
- CORS enabled for cross-origin requests

### Frontend (React/Vite)
- Interactive map with Leaflet
- Real-time ride matching visualization
- Beautiful animations with Framer Motion
- Responsive design with Tailwind CSS
- Glass morphism UI effects

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- npm or yarn

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /tmp/ride-sharing-optimizer
```

2. **Install Python dependencies**
```bash
pip3 install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install
```

4. **Start the backend server**
```bash
python3 app.py
```
Backend will run on `http://localhost:5001`

5. **In a new terminal, start the frontend**
```bash
npm run dev
```
Frontend will run on `http://localhost:5173`

6. **Open your browser**
Navigate to `http://localhost:5173`

### 🎯 Quick Start Script
```bash
chmod +x setup.sh start.sh
./setup.sh   # Install dependencies
./start.sh   # Start both servers
```

## 💻 Usage

1. **Generate Sample Data**: Click the "Generate Sample" button to create random riders and drivers
2. **View the Map**: See riders (blue/purple markers) and drivers (green markers) on the interactive map
3. **Optimize Rides**: Click "Optimize Rides" to run the matching algorithm
4. **View Results**: See the optimized routes with different colors for each driver
5. **Check Metrics**: Review cost savings, distance reduction, and environmental impact

## 🔬 Algorithm Details

The optimization algorithm uses a multi-phase approach:

### 1. Geographical Clustering
- Groups riders by pickup location proximity
- Uses K-means algorithm from scikit-learn
- Number of clusters adapts to driver availability

### 2. Driver Assignment
- Assigns drivers to rider clusters
- Minimizes total driver-to-cluster distance
- Ensures balanced distribution

### 3. Route Optimization
- Solves Traveling Salesman Problem (TSP) for each driver
- Uses Google OR-Tools constraint programming solver
- Enforces pickup-before-dropoff constraints
- Respects vehicle capacity limits
- 5-second optimization time limit per route

### 4. Cost Calculation
- Calculates total distance using Haversine formula
- Compares shared vs. solo trip distances
- Computes cost savings at $2.50/km
- Estimates CO₂ reduction at 0.12kg/km

## 📊 API Endpoints

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Ride-sharing optimizer API is running"
}
```

### `POST /api/optimize`
Optimize ride-sharing matches

**Request:**
```json
{
  "riders": [
    {"id": 1, "pickup": [40.7589, -73.9851], "dropoff": [40.7614, -73.9776]}
  ],
  "drivers": [
    {"id": 1, "location": [40.7550, -73.9870], "capacity": 4}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "matches": [...],
  "metrics": {
    "total_riders": 8,
    "riders_matched": 8,
    "savings_percent": 35.2,
    "total_cost": 45.5
  }
}
```

### `GET /api/generate-sample`
Generate sample data for testing

**Query Parameters:**
- `riders` (optional): Number of riders (default: 8)
- `drivers` (optional): Number of drivers (default: 3)

### `POST /api/calculate-savings`
Calculate potential savings for a set of riders

## 🧪 Testing

Run the test suite:
```bash
python3 test_optimizer.py
```

Tests include:
- Basic optimization scenarios
- High capacity handling
- Edge cases (single rider)
- Clustering optimization
- Performance benchmarks

## 🛠️ Technology Stack

**Backend:**
- Python 3.13
- Flask 3.1 - Web framework
- OR-Tools 9.14 - Google's optimization tools
- NumPy 2.3 - Numerical computing
- Scikit-learn 1.7 - Machine learning
- SciPy 1.16 - Scientific computing
- Geopy 2.4 - Geographical calculations

**Frontend:**
- React 18.2 - UI framework
- Vite 5.0 - Build tool
- Tailwind CSS 3.4 - Styling
- Leaflet 1.9 - Interactive maps
- Framer Motion 10.16 - Animations
- Axios 1.6 - HTTP client
- Lucide React - Icon library

## 📁 Project Structure

```
ride-sharing-optimizer/
├── app.py                    # Flask API server
├── optimizer.py              # Core optimization algorithm
├── test_optimizer.py         # Test suite
├── requirements.txt          # Python dependencies
├── package.json             # Node.js dependencies
├── README.md                # This file
├── GUIDE.md                 # Comprehensive guide
├── PROJECT_SUMMARY.md       # Project completion summary
├── setup.sh                 # Setup script
├── start.sh                 # Start script
├── .gitignore              # Git ignore rules
├── index.html              # HTML template
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS configuration
└── src/
    ├── main.jsx            # React entry point
    ├── App.jsx             # Main application
    ├── index.css           # Global styles
    └── components/
        ├── MapView.jsx      # Interactive map component
        ├── StatsCard.jsx    # Statistics card component
        ├── ControlPanel.jsx # Control panel component
        └── ResultsPanel.jsx # Results display component
```

## 🎨 UI Components

- **Header**: Gradient logo, title, and controls
- **Stats Cards**: Live metrics with animations
- **Interactive Map**: Leaflet map with custom markers and routes
- **Control Panel**: Rider/driver management and optimization trigger
- **Results Panel**: Detailed optimization results and environmental impact

## 📈 Performance

- Handles 20+ riders efficiently
- Sub-second optimization for typical loads
- Real-time UI updates
- Smooth 60fps animations
- Responsive on all device sizes

## 🔮 Future Enhancements

- User authentication and profiles
- Real-time GPS tracking
- Payment processing integration
- Historical data analytics
- Mobile app version
- Multiple vehicle types
- Time window constraints
- Traffic-aware routing
- Machine learning demand prediction
- Driver ratings and reviews

## 📚 Documentation

- **README.md** (this file): Quick overview and setup
- **GUIDE.md**: Comprehensive user and developer guide
- **PROJECT_SUMMARY.md**: Complete project documentation
- **test_optimizer.py**: Example usage and testing

## 🐛 Troubleshooting

### Port conflicts
If port 5001 or 5173 is in use:
- Backend: Change port in `app.py`
- Frontend: Update `src/App.jsx` API_URL

### Dependencies not installing
```bash
# Python
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Node.js
rm -rf node_modules package-lock.json
npm install
```

### Map not loading
- Ensure backend is running
- Check browser console for CORS errors
- Verify API_URL in `src/App.jsx`

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google OR-Tools for optimization algorithms
- Leaflet for beautiful maps
- React and Vite communities
- All open-source contributors

---

**Made with ❤️ for efficient and sustainable transportation** 🚗✨
