"""
Example usage and testing of the Ride-Sharing Optimizer
"""

from optimizer import RideSharingOptimizer

def test_basic_optimization():
    """Test basic optimization with sample data"""
    print("=" * 60)
    print("Test 1: Basic Optimization")
    print("=" * 60)
    
    optimizer = RideSharingOptimizer()
    
    # Sample riders (NYC area)
    riders = [
        {'id': 1, 'pickup': [40.7589, -73.9851], 'dropoff': [40.7614, -73.9776]},
        {'id': 2, 'pickup': [40.7580, -73.9855], 'dropoff': [40.7620, -73.9700]},
        {'id': 3, 'pickup': [40.7500, -73.9900], 'dropoff': [40.7650, -73.9750]},
        {'id': 4, 'pickup': [40.7520, -73.9880], 'dropoff': [40.7600, -73.9720]},
    ]
    
    # Sample drivers
    drivers = [
        {'id': 1, 'location': [40.7550, -73.9870], 'capacity': 4},
        {'id': 2, 'location': [40.7490, -73.9920], 'capacity': 3},
    ]
    
    result = optimizer.optimize(riders, drivers)
    
    print(f"\nSuccess: {result['success']}")
    print(f"\nMetrics:")
    for key, value in result['metrics'].items():
        print(f"  {key}: {value}")
    
    print(f"\nMatches: {len(result['matches'])}")
    for match in result['matches']:
        print(f"\n  Driver {match['driver_id']}:")
        print(f"    Assigned Riders: {[r['id'] for r in match['riders']]}")
        print(f"    Route Distance: {match['distance']} km")
        print(f"    Estimated Cost: ${match['cost']}")
        print(f"    Route Points: {len(match['route'])}")
    
    print("\n" + "=" * 60)
    return result

def test_high_capacity():
    """Test with many riders and few drivers"""
    print("\nTest 2: High Capacity Scenario")
    print("=" * 60)
    
    optimizer = RideSharingOptimizer()
    
    # Many riders
    riders = [
        {'id': i+1, 
         'pickup': [40.75 + i*0.01, -73.99 + i*0.005], 
         'dropoff': [40.76 + i*0.01, -73.98 + i*0.005]}
        for i in range(10)
    ]
    
    # Few drivers with high capacity
    drivers = [
        {'id': 1, 'location': [40.7550, -73.9870], 'capacity': 5},
        {'id': 2, 'location': [40.7600, -73.9900], 'capacity': 5},
    ]
    
    result = optimizer.optimize(riders, drivers)
    
    print(f"\nTotal Riders: {result['metrics']['total_riders']}")
    print(f"Riders Matched: {result['metrics']['riders_matched']}")
    print(f"Efficiency: {result['metrics']['savings_percent']:.2f}%")
    print(f"Cost Savings: ${(result['metrics']['solo_distance'] - result['metrics']['total_distance']) * 2.5:.2f}")
    
    print("\n" + "=" * 60)
    return result

def test_single_rider():
    """Test with single rider (edge case)"""
    print("\nTest 3: Single Rider Edge Case")
    print("=" * 60)
    
    optimizer = RideSharingOptimizer()
    
    riders = [
        {'id': 1, 'pickup': [40.7589, -73.9851], 'dropoff': [40.7614, -73.9776]},
    ]
    
    drivers = [
        {'id': 1, 'location': [40.7550, -73.9870], 'capacity': 4},
    ]
    
    result = optimizer.optimize(riders, drivers)
    
    print(f"\nSuccess: {result['success']}")
    print(f"Distance: {result['metrics']['total_distance']:.2f} km")
    print(f"Cost: ${result['metrics']['total_cost']:.2f}")
    
    print("\n" + "=" * 60)
    return result

def test_optimal_clustering():
    """Test clustering with multiple groups"""
    print("\nTest 4: Clustering Optimization")
    print("=" * 60)
    
    optimizer = RideSharingOptimizer()
    
    # Two distinct clusters of riders
    riders = [
        # Cluster 1 (Downtown)
        {'id': 1, 'pickup': [40.7200, -74.0000], 'dropoff': [40.7250, -73.9950]},
        {'id': 2, 'pickup': [40.7210, -73.9990], 'dropoff': [40.7260, -73.9940]},
        {'id': 3, 'pickup': [40.7205, -73.9995], 'dropoff': [40.7255, -73.9945]},
        
        # Cluster 2 (Uptown)
        {'id': 4, 'pickup': [40.7800, -73.9700], 'dropoff': [40.7850, -73.9650]},
        {'id': 5, 'pickup': [40.7810, -73.9690], 'dropoff': [40.7860, -73.9640]},
        {'id': 6, 'pickup': [40.7805, -73.9695], 'dropoff': [40.7855, -73.9645]},
    ]
    
    # Drivers positioned near each cluster
    drivers = [
        {'id': 1, 'location': [40.7205, -73.9990], 'capacity': 3},
        {'id': 2, 'location': [40.7805, -73.9695], 'capacity': 3},
    ]
    
    result = optimizer.optimize(riders, drivers)
    
    print(f"\nClustering Results:")
    print(f"Total Riders: {result['metrics']['total_riders']}")
    print(f"Total Drivers: {result['metrics']['total_drivers']}")
    print(f"Riders Matched: {result['metrics']['riders_matched']}")
    print(f"Savings: {result['metrics']['savings_percent']:.2f}%")
    
    for match in result['matches']:
        print(f"\nDriver {match['driver_id']}:")
        print(f"  Riders: {[r['id'] for r in match['riders']]}")
        print(f"  Distance: {match['distance']:.2f} km")
    
    print("\n" + "=" * 60)
    return result

def performance_benchmark():
    """Benchmark the optimization performance"""
    print("\nTest 5: Performance Benchmark")
    print("=" * 60)
    
    import time
    
    optimizer = RideSharingOptimizer()
    
    # Generate large dataset
    num_riders = 20
    num_drivers = 5
    
    riders = [
        {'id': i+1, 
         'pickup': [40.70 + i*0.005, -74.00 + i*0.003], 
         'dropoff': [40.71 + i*0.005, -73.99 + i*0.003]}
        for i in range(num_riders)
    ]
    
    drivers = [
        {'id': i+1, 
         'location': [40.705 + i*0.02, -73.995 + i*0.01], 
         'capacity': 4}
        for i in range(num_drivers)
    ]
    
    print(f"\nOptimizing {num_riders} riders with {num_drivers} drivers...")
    
    start_time = time.time()
    result = optimizer.optimize(riders, drivers)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    print(f"\nExecution Time: {execution_time:.3f} seconds")
    print(f"Riders per Second: {num_riders / execution_time:.2f}")
    print(f"Success: {result['success']}")
    print(f"Riders Matched: {result['metrics']['riders_matched']}/{num_riders}")
    print(f"Total Distance: {result['metrics']['total_distance']:.2f} km")
    print(f"Savings: {result['metrics']['savings_percent']:.2f}%")
    
    print("\n" + "=" * 60)
    return result

if __name__ == "__main__":
    print("\n🚗 Ride-Sharing Optimizer - Test Suite\n")
    
    # Run all tests
    test_basic_optimization()
    test_high_capacity()
    test_single_rider()
    test_optimal_clustering()
    performance_benchmark()
    
    print("\n✅ All tests completed!\n")
