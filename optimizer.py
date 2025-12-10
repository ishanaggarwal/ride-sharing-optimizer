"""
Optimized Ride-Sharing Algorithm
Uses OR-Tools for constraint programming and route optimization
"""

import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
from typing import List, Dict, Tuple, Optional


class Location:
    """Represents a geographical location"""
    def __init__(self, lat: float, lon: float, location_type: str, person_id: int = None):
        self.lat = lat
        self.lon = lon
        self.type = location_type  # 'pickup' or 'dropoff'
        self.person_id = person_id

    def to_dict(self):
        return {
            'lat': self.lat,
            'lon': self.lon,
            'type': self.type,
            'person_id': self.person_id
        }


class Rider:
    """Represents a rider with pickup and dropoff locations"""
    def __init__(self, rider_id: int, pickup: Tuple[float, float], 
                 dropoff: Tuple[float, float], max_wait_time: int = 15):
        self.id = rider_id
        self.pickup = Location(pickup[0], pickup[1], 'pickup', rider_id)
        self.dropoff = Location(dropoff[0], dropoff[1], 'dropoff', rider_id)
        self.max_wait_time = max_wait_time
        self.assigned_driver = None

    def to_dict(self):
        return {
            'id': self.id,
            'pickup': self.pickup.to_dict(),
            'dropoff': self.dropoff.to_dict(),
            'assigned_driver': self.assigned_driver
        }


class Driver:
    """Represents a driver with location and capacity"""
    def __init__(self, driver_id: int, location: Tuple[float, float], 
                 capacity: int = 4):
        self.id = driver_id
        self.location = Location(location[0], location[1], 'driver', driver_id)
        self.capacity = capacity
        self.assigned_riders = []
        self.route = []
        self.total_distance = 0

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location.to_dict(),
            'capacity': self.capacity,
            'assigned_riders': self.assigned_riders,
            'route': [loc.to_dict() for loc in self.route],
            'total_distance': self.total_distance
        }


class RideSharingOptimizer:
    """Main optimizer class for ride-sharing algorithm"""
    
    def __init__(self):
        self.riders = []
        self.drivers = []
        self.distance_matrix = None
        
    def haversine_distance(self, loc1: Location, loc2: Location) -> float:
        """Calculate distance between two locations using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(loc1.lat), math.radians(loc1.lon)
        lat2, lon2 = math.radians(loc2.lat), math.radians(loc2.lon)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def calculate_distance_matrix(self, locations: List[Location]) -> np.ndarray:
        """Create distance matrix for all locations"""
        n = len(locations)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = self.haversine_distance(locations[i], locations[j])
        
        return matrix
    
    def cluster_riders(self, n_clusters: int = None) -> Dict[int, List[Rider]]:
        """Cluster riders based on pickup locations using K-means"""
        if not self.riders:
            return {}
        
        if n_clusters is None:
            n_clusters = min(len(self.drivers), len(self.riders))
        
        # Extract pickup coordinates
        pickup_coords = np.array([[r.pickup.lat, r.pickup.lon] for r in self.riders])
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pickup_coords)
        
        # Group riders by cluster
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.riders[idx])
        
        return clusters
    
    def assign_drivers_to_clusters(self, clusters: Dict[int, List[Rider]]) -> Dict[int, int]:
        """Assign drivers to rider clusters based on proximity"""
        if not self.drivers or not clusters:
            return {}
        
        # Calculate cluster centroids
        cluster_centroids = {}
        for cluster_id, riders in clusters.items():
            avg_lat = np.mean([r.pickup.lat for r in riders])
            avg_lon = np.mean([r.pickup.lon for r in riders])
            cluster_centroids[cluster_id] = Location(avg_lat, avg_lon, 'centroid')
        
        # Calculate distances from drivers to centroids
        driver_assignments = {}
        assigned_clusters = set()
        
        # Sort drivers and clusters for greedy assignment
        for driver in sorted(self.drivers, key=lambda d: d.id):
            best_cluster = None
            best_distance = float('inf')
            
            for cluster_id, centroid in cluster_centroids.items():
                if cluster_id in assigned_clusters:
                    continue
                    
                distance = self.haversine_distance(driver.location, centroid)
                if distance < best_distance:
                    best_distance = distance
                    best_cluster = cluster_id
            
            if best_cluster is not None:
                driver_assignments[driver.id] = best_cluster
                assigned_clusters.add(best_cluster)
        
        return driver_assignments
    
    def optimize_route_for_driver(self, driver: Driver, riders: List[Rider]) -> List[Location]:
        """Optimize route for a single driver using OR-Tools TSP solver"""
        if not riders:
            return []
        
        # Filter riders that fit in driver's capacity
        riders = riders[:driver.capacity]
        
        # Create list of locations (driver start, pickups, dropoffs)
        locations = [driver.location]
        location_map = {0: ('driver', driver.id)}
        
        idx = 1
        for rider in riders:
            locations.append(rider.pickup)
            location_map[idx] = ('pickup', rider.id)
            idx += 1
        
        for rider in riders:
            locations.append(rider.dropoff)
            location_map[idx] = ('dropoff', rider.id)
            idx += 1
        
        # Calculate distance matrix
        n = len(locations)
        distance_matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = int(self.haversine_distance(locations[i], locations[j]) * 1000)
        
        # Create routing model
        manager = pywrapcp.RoutingIndexManager(n, 1, 0)
        routing = pywrapcp.RoutingModel(manager)
        
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        # Add pickup-dropoff constraints
        for rider in riders:
            pickup_idx = None
            dropoff_idx = None
            
            for idx, (loc_type, loc_id) in location_map.items():
                if loc_type == 'pickup' and loc_id == rider.id:
                    pickup_idx = manager.NodeToIndex(idx)
                elif loc_type == 'dropoff' and loc_id == rider.id:
                    dropoff_idx = manager.NodeToIndex(idx)
            
            if pickup_idx is not None and dropoff_idx is not None:
                routing.AddPickupAndDelivery(pickup_idx, dropoff_idx)
                routing.solver().Add(
                    routing.VehicleVar(pickup_idx) == routing.VehicleVar(dropoff_idx)
                )
                routing.solver().Add(
                    routing.CumulVar(pickup_idx, 'time') <= 
                    routing.CumulVar(dropoff_idx, 'time')
                )
        
        # Add capacity constraint
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node in location_map:
                loc_type, _ = location_map[from_node]
                if loc_type == 'pickup':
                    return 1
                elif loc_type == 'dropoff':
                    return -1
            return 0
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            [driver.capacity],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity'
        )
        
        # Set search parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 5
        
        # Solve
        solution = routing.SolveWithParameters(search_parameters)
        
        if solution:
            route = []
            index = routing.Start(0)
            total_distance = 0
            
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(locations[node])
                
                next_index = solution.Value(routing.NextVar(index))
                next_node = manager.IndexToNode(next_index)
                total_distance += self.haversine_distance(locations[node], locations[next_node])
                
                index = next_index
            
            driver.total_distance = total_distance
            return route
        
        # Fallback: simple route if optimization fails
        route = [driver.location]
        for rider in riders:
            route.append(rider.pickup)
        for rider in riders:
            route.append(rider.dropoff)
        return route
    
    def optimize(self, riders: List[Dict], drivers: List[Dict]) -> Dict:
        """Main optimization function"""
        # Convert input to objects
        self.riders = [
            Rider(r['id'], tuple(r['pickup']), tuple(r['dropoff']))
            for r in riders
        ]
        self.drivers = [
            Driver(d['id'], tuple(d['location']), d.get('capacity', 4))
            for d in drivers
        ]
        
        if not self.riders or not self.drivers:
            return {
                'success': False,
                'message': 'Need at least one rider and one driver',
                'matches': []
            }
        
        # Step 1: Cluster riders
        n_clusters = min(len(self.drivers), len(self.riders))
        clusters = self.cluster_riders(n_clusters)
        
        # Step 2: Assign drivers to clusters
        driver_assignments = self.assign_drivers_to_clusters(clusters)
        
        # Step 3: Optimize routes for each driver
        matches = []
        total_distance = 0
        total_riders_matched = 0
        
        for driver in self.drivers:
            if driver.id in driver_assignments:
                cluster_id = driver_assignments[driver.id]
                assigned_riders = clusters[cluster_id]
                
                # Optimize route
                route = self.optimize_route_for_driver(driver, assigned_riders)
                driver.route = route
                driver.assigned_riders = [r.id for r in assigned_riders[:driver.capacity]]
                
                # Update rider assignments
                for rider in assigned_riders[:driver.capacity]:
                    rider.assigned_driver = driver.id
                
                total_distance += driver.total_distance
                total_riders_matched += len(driver.assigned_riders)
                
                matches.append({
                    'driver_id': driver.id,
                    'driver_location': driver.location.to_dict(),
                    'riders': [r.to_dict() for r in assigned_riders[:driver.capacity]],
                    'route': [loc.to_dict() for loc in route],
                    'distance': round(driver.total_distance, 2),
                    'cost': round(driver.total_distance * 2.5, 2)  # $2.5 per km
                })
        
        # Calculate efficiency metrics
        solo_distance = sum(
            self.haversine_distance(r.pickup, r.dropoff)
            for r in self.riders
        )
        
        savings_percent = ((solo_distance - total_distance) / solo_distance * 100) if solo_distance > 0 else 0
        
        return {
            'success': True,
            'matches': matches,
            'metrics': {
                'total_riders': len(self.riders),
                'total_drivers': len(self.drivers),
                'riders_matched': total_riders_matched,
                'total_distance': round(total_distance, 2),
                'solo_distance': round(solo_distance, 2),
                'savings_percent': round(savings_percent, 2),
                'total_cost': round(total_distance * 2.5, 2),
                'cost_per_rider': round((total_distance * 2.5) / total_riders_matched, 2) if total_riders_matched > 0 else 0
            }
        }


# Example usage
if __name__ == "__main__":
    optimizer = RideSharingOptimizer()
    
    # Sample data
    riders = [
        {'id': 1, 'pickup': [40.7589, -73.9851], 'dropoff': [40.7614, -73.9776]},
        {'id': 2, 'pickup': [40.7580, -73.9855], 'dropoff': [40.7620, -73.9700]},
        {'id': 3, 'pickup': [40.7500, -73.9900], 'dropoff': [40.7650, -73.9750]},
    ]
    
    drivers = [
        {'id': 1, 'location': [40.7550, -73.9870], 'capacity': 4},
        {'id': 2, 'location': [40.7490, -73.9920], 'capacity': 3},
    ]
    
    result = optimizer.optimize(riders, drivers)
    
    print("\n=== Optimization Results ===")
    print(f"Success: {result['success']}")
    print(f"\nMetrics:")
    for key, value in result['metrics'].items():
        print(f"  {key}: {value}")
    print(f"\nMatches: {len(result['matches'])}")
    for match in result['matches']:
        print(f"\nDriver {match['driver_id']}:")
        print(f"  Riders: {[r['id'] for r in match['riders']]}")
        print(f"  Distance: {match['distance']} km")
        print(f"  Cost: ${match['cost']}")
