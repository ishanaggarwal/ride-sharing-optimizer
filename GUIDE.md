# 🚗 Ride-Sharing Optimizer - Quick Start Guide

## ✅ Setup Complete!

Your ride-sharing optimization project is now running with:
- **Backend API**: http://localhost:5001
- **Frontend UI**: http://localhost:5173

## 📁 Project Structure

```
ride-sharing-optimizer/
├── app.py                    # Flask backend server
├── optimizer.py              # Core optimization algorithm
├── requirements.txt          # Python dependencies
├── package.json             # Node.js dependencies
├── src/
│   ├── App.jsx              # Main React application
│   ├── components/
│   │   ├── MapView.jsx      # Interactive Leaflet map
│   │   ├── StatsCard.jsx    # Statistics display cards
│   │   ├── ControlPanel.jsx # Control panel with riders/drivers list
│   │   └── ResultsPanel.jsx # Optimization results display
│   ├── index.css            # Global styles
│   └── main.jsx             # React entry point
├── index.html               # HTML template
├── vite.config.js          # Vite configuration
└── tailwind.config.js      # Tailwind CSS configuration
```

## 🎯 Features

### Optimization Algorithm
- **K-Means Clustering**: Groups riders by proximity
- **OR-Tools TSP Solver**: Optimizes driver routes
- **Constraint Programming**: Ensures capacity constraints
- **Distance Calculation**: Haversine formula for accurate distances

### Frontend Features
- **Interactive Map**: Real-time visualization with Leaflet
- **Dynamic UI**: Beautiful animations with Framer Motion
- **Responsive Design**: Works on all screen sizes
- **Real-time Updates**: Instant feedback on optimizations

## 🎮 How to Use

1. **Generate Sample Data**
   - Click "Generate Sample" button in the header
   - This creates random riders and drivers in NYC area

2. **View the Map**
   - 🔵 Blue markers = Rider pickups
   - 🟣 Purple markers = Rider dropoffs
   - 🟢 Green markers = Driver locations

3. **Optimize Rides**
   - Click "Optimize Rides" button in the Control Panel
   - Wait for the algorithm to compute optimal matches
   - View the results with colorful route lines on the map

4. **Analyze Results**
   - Check the stats cards for key metrics
   - Review the detailed results panel
   - See environmental impact calculations

## 🔧 API Endpoints

### GET `/api/health`
Health check endpoint

### POST `/api/optimize`
Optimize ride-sharing matches
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

### GET `/api/generate-sample`
Generate sample data for testing
Query params: `?riders=8&drivers=3`

### POST `/api/calculate-savings`
Calculate potential cost and time savings

## 🎨 UI Components

### Stats Cards
- Total Riders
- Total Drivers
- Savings Percentage
- Total Cost

### Map View
- Interactive Leaflet map
- Custom markers for pickups, dropoffs, and drivers
- Route visualization with different colors per driver
- Auto-zoom to fit all markers

### Control Panel
- Optimize Rides button
- List of all riders with details
- List of all drivers with details
- Remove riders/drivers functionality

### Results Panel
- Detailed optimization metrics
- Driver assignments
- Cost breakdown per driver
- Environmental impact calculations

## 🚀 Running the Application

### Start Both Servers
```bash
# Terminal 1 - Backend
python3 /tmp/ride-sharing-optimizer/app.py

# Terminal 2 - Frontend
cd /tmp/ride-sharing-optimizer
npm run dev
```

### Or Use the Start Script
```bash
cd /tmp/ride-sharing-optimizer
./start.sh
```

## 🧪 Testing the Algorithm

The optimizer uses several advanced techniques:

1. **Geographical Clustering**
   - Groups riders based on pickup locations
   - Uses K-means algorithm from scikit-learn

2. **Driver Assignment**
   - Assigns drivers to rider clusters
   - Minimizes total distance

3. **Route Optimization**
   - Uses Google OR-Tools routing solver
   - Solves Traveling Salesman Problem (TSP)
   - Respects pickup-before-dropoff constraints
   - Enforces vehicle capacity limits

4. **Cost Calculation**
   - Calculates distance-based costs
   - Compares with solo ride costs
   - Shows savings percentage

## 📊 Metrics Explained

- **Riders Matched**: Number of riders assigned to drivers
- **Distance Saved**: Kilometers saved vs solo rides
- **Savings Percent**: Efficiency improvement percentage
- **Cost Per Rider**: Average shared cost per passenger
- **CO₂ Saved**: Environmental impact (kg of CO₂)

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **OR-Tools**: Google's optimization tools
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning (K-means)
- **SciPy**: Scientific computing
- **Geopy**: Geographical distance calculations

### Frontend
- **React**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS
- **Leaflet**: Interactive maps
- **Framer Motion**: Animations
- **Axios**: HTTP client
- **Lucide React**: Icon library

## 🎯 Future Enhancements

Potential improvements:
- Real-time tracking integration
- User authentication system
- Payment processing
- Historical data analytics
- Mobile app version
- Multiple vehicle types
- Time window constraints
- Traffic-aware routing
- Machine learning for demand prediction

## 📝 Notes

- The sample data generates riders and drivers in Manhattan, NYC
- Distance calculations use the Haversine formula
- Cost is calculated at $2.50 per kilometer
- CO₂ savings estimated at 0.12 kg per kilometer
- Default driver capacity is 4 passengers

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5001 is available
- Ensure all Python dependencies are installed
- Run: `pip3 install -r requirements.txt`

### Frontend won't start
- Check if port 5173 is available
- Ensure Node modules are installed
- Run: `npm install`

### Map not loading
- Check browser console for errors
- Ensure backend is running on port 5001
- Check CORS settings in app.py

### Optimization fails
- Ensure at least 1 rider and 1 driver exist
- Check backend logs for errors
- Verify data format matches API expectations

## 📚 Learn More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OR-Tools Guide](https://developers.google.com/optimization)
- [React Documentation](https://react.dev/)
- [Leaflet Documentation](https://leafletjs.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Enjoy optimizing rides! 🚗✨**
