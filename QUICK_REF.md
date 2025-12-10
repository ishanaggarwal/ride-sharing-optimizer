# 🚀 Quick Reference Card

## Project Location
```
/tmp/ride-sharing-optimizer/
```

## 🌐 URLs
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

## ⚡ Quick Commands

### Start Servers
```bash
# Backend (Terminal 1)
python3 /tmp/ride-sharing-optimizer/app.py

# Frontend (Terminal 2)
cd /tmp/ride-sharing-optimizer && npm run dev
```

### Run Tests
```bash
python3 /tmp/ride-sharing-optimizer/test_optimizer.py
```

### Reinstall Dependencies
```bash
# Python
pip3 install -r /tmp/ride-sharing-optimizer/requirements.txt

# Node.js
cd /tmp/ride-sharing-optimizer && npm install
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/optimize` | Run optimization |
| GET | `/api/generate-sample` | Generate test data |
| POST | `/api/calculate-savings` | Calculate savings |

## 🎯 UI Usage Flow

1. **Open** → http://localhost:5173
2. **Click** → "Generate Sample" button
3. **Review** → Riders and drivers on map
4. **Click** → "Optimize Rides" button
5. **View** → Results with routes and metrics

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend server |
| `optimizer.py` | Optimization algorithm |
| `src/App.jsx` | Main React component |
| `src/components/MapView.jsx` | Interactive map |
| `requirements.txt` | Python dependencies |
| `package.json` | Node dependencies |

## 📦 Tech Stack

**Backend:**
- Python 3.13
- Flask 3.1
- OR-Tools 9.14
- Scikit-learn 1.7

**Frontend:**
- React 18.2
- Vite 5.0
- Tailwind CSS 3.4
- Leaflet 1.9

## 🎨 Map Legend

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Rider pickup |
| 🟣 Purple | Rider dropoff |
| 🟢 Green | Driver location |
| 🌈 Various | Optimized routes |

## 📈 Metrics Explained

- **Savings %**: Distance reduction vs solo trips
- **Cost**: Total cost at $2.50/km
- **Cost/Rider**: Shared cost per passenger
- **CO₂ Saved**: Environmental impact at 0.12kg/km

## 🐛 Troubleshooting

### Port in Use
```bash
# Change backend port in app.py
# Update API_URL in src/App.jsx
```

### Dependencies Error
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Map Not Loading
- Check backend is running
- Verify port 5001 is accessible
- Check browser console for errors

## 📚 Documentation

- `README.md` - Overview
- `GUIDE.md` - Detailed guide
- `PROJECT_SUMMARY.md` - Complete summary
- `UI_DESIGN.md` - Design reference

## 🎮 Keyboard Shortcuts

- **Ctrl+C** - Stop server
- **H + Enter** - Vite dev server help
- **R** - Restart Vite dev server

## 💡 Tips

1. Generate sample data first before optimizing
2. Remove/add riders to test different scenarios
3. Check the results panel for detailed breakdowns
4. Use the test suite to understand the algorithm
5. Backend auto-reloads on code changes

## 🔮 Next Steps

- [ ] Add user authentication
- [ ] Implement real-time tracking
- [ ] Add payment integration
- [ ] Create mobile app
- [ ] Add ML predictions

---

**Status**: ✅ READY TO USE

**Last Updated**: December 9, 2025
