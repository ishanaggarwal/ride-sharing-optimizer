"""
Flask API Server for Ride-Sharing Optimizer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from optimizer import RideSharingOptimizer
import random

app = Flask(__name__)
CORS(app)

optimizer = RideSharingOptimizer()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Ride-sharing optimizer API is running'})


@app.route('/api/optimize', methods=['POST'])
def optimize_rides():
    """
    Optimize ride-sharing matches
    Expected JSON format:
    {
        "riders": [
            {"id": 1, "pickup": [lat, lon], "dropoff": [lat, lon]},
            ...
        ],
        "drivers": [
            {"id": 1, "location": [lat, lon], "capacity": 4},
            ...
        ]
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        riders = data.get('riders', [])
        drivers = data.get('drivers', [])
        
        if not riders:
            return jsonify({'success': False, 'error': 'No riders provided'}), 400
        
        if not drivers:
            return jsonify({'success': False, 'error': 'No drivers provided'}), 400
        
        # Run optimization
        result = optimizer.optimize(riders, drivers)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-sample', methods=['GET'])
def generate_sample_data():
    """Generate sample riders and drivers for testing"""
    try:
        # Sample area: Manhattan, NYC (roughly)
        # Lat range: 40.70 to 40.80
        # Lon range: -74.02 to -73.93
        
        num_riders = int(request.args.get('riders', 8))
        num_drivers = int(request.args.get('drivers', 3))
        
        riders = []
        for i in range(num_riders):
            pickup_lat = round(random.uniform(40.70, 40.80), 6)
            pickup_lon = round(random.uniform(-74.02, -73.93), 6)
            
            # Dropoff within 0.02 degrees (roughly 2km)
            dropoff_lat = round(pickup_lat + random.uniform(-0.02, 0.02), 6)
            dropoff_lon = round(pickup_lon + random.uniform(-0.02, 0.02), 6)
            
            riders.append({
                'id': i + 1,
                'pickup': [pickup_lat, pickup_lon],
                'dropoff': [dropoff_lat, dropoff_lon]
            })
        
        drivers = []
        for i in range(num_drivers):
            driver_lat = round(random.uniform(40.70, 40.80), 6)
            driver_lon = round(random.uniform(-74.02, -73.93), 6)
            
            drivers.append({
                'id': i + 1,
                'location': [driver_lat, driver_lon],
                'capacity': random.randint(3, 5)
            })
        
        return jsonify({
            'success': True,
            'riders': riders,
            'drivers': drivers
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/calculate-savings', methods=['POST'])
def calculate_savings():
    """Calculate potential cost and time savings"""
    try:
        data = request.json
        riders = data.get('riders', [])
        
        if not riders:
            return jsonify({'success': False, 'error': 'No riders provided'}), 400
        
        # Calculate individual trip distances
        total_solo_distance = 0
        for rider in riders:
            pickup = rider['pickup']
            dropoff = rider['dropoff']
            
            # Simple distance calculation
            import math
            lat1, lon1 = math.radians(pickup[0]), math.radians(pickup[1])
            lat2, lon2 = math.radians(dropoff[0]), math.radians(dropoff[1])
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = 6371 * c  # Earth radius in km
            
            total_solo_distance += distance
        
        # Estimate carpooling savings (typically 30-50%)
        estimated_shared_distance = total_solo_distance * 0.65
        savings_percent = ((total_solo_distance - estimated_shared_distance) / total_solo_distance) * 100
        
        cost_per_km = 2.5
        solo_cost = total_solo_distance * cost_per_km
        shared_cost = estimated_shared_distance * cost_per_km
        
        return jsonify({
            'success': True,
            'solo_distance': round(total_solo_distance, 2),
            'estimated_shared_distance': round(estimated_shared_distance, 2),
            'savings_percent': round(savings_percent, 2),
            'solo_cost': round(solo_cost, 2),
            'shared_cost': round(shared_cost, 2),
            'cost_savings': round(solo_cost - shared_cost, 2)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚗 Ride-Sharing Optimizer API Server")
    print("="*60)
    print("\nStarting server on http://localhost:5001")
    print("\nAvailable endpoints:")
    print("  GET  /api/health           - Health check")
    print("  POST /api/optimize         - Optimize rides")
    print("  GET  /api/generate-sample  - Generate sample data")
    print("  POST /api/calculate-savings - Calculate savings")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
