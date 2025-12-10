import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default icon issue with Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons
const createCustomIcon = (color, symbol) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `
      <div style="
        background: ${color};
        width: 32px;
        height: 32px;
        border-radius: 50% 50% 50% 0;
        transform: rotate(-45deg);
        border: 3px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
      ">
        <span style="
          transform: rotate(45deg);
          color: white;
          font-weight: bold;
          font-size: 14px;
        ">${symbol}</span>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
  });
};

const pickupIcon = createCustomIcon('#0ea5e9', 'P');
const dropoffIcon = createCustomIcon('#d946ef', 'D');
const driverIcon = createCustomIcon('#10b981', 'C');

// Component to fit bounds when data changes
function FitBounds({ riders, drivers }) {
  const map = useMap();

  useEffect(() => {
    if (riders.length === 0 && drivers.length === 0) {
      map.setView([40.7589, -73.9851], 13);
      return;
    }

    const bounds = [];
    
    riders.forEach(rider => {
      bounds.push([rider.pickup[0], rider.pickup[1]]);
      bounds.push([rider.dropoff[0], rider.dropoff[1]]);
    });
    
    drivers.forEach(driver => {
      bounds.push([driver.location[0], driver.location[1]]);
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [riders, drivers, map]);

  return null;
}

const MapView = ({ riders, drivers, optimizationResult }) => {
  const defaultCenter = [40.7589, -73.9851]; // New York City
  const defaultZoom = 13;

  // Generate random colors for different driver routes
  const routeColors = [
    '#0ea5e9', '#d946ef', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'
  ];

  return (
    <div className="relative">
      <div className="absolute top-4 left-4 z-[1000] bg-slate-800/90 backdrop-blur-lg rounded-lg p-3 shadow-xl border border-slate-700/50">
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-primary-500"></div>
            <span>Pickup</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-accent-500"></div>
            <span>Dropoff</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-green-500"></div>
            <span>Driver</span>
          </div>
        </div>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: '600px', width: '100%' }}
        className="rounded-xl"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <FitBounds riders={riders} drivers={drivers} />

        {/* Render riders */}
        {riders.map((rider) => (
          <React.Fragment key={`rider-${rider.id}`}>
            <Marker position={rider.pickup} icon={pickupIcon}>
              <Popup>
                <div className="text-slate-900">
                  <strong>Rider {rider.id} - Pickup</strong>
                  <br />
                  Location: {rider.pickup[0].toFixed(4)}, {rider.pickup[1].toFixed(4)}
                </div>
              </Popup>
            </Marker>
            <Marker position={rider.dropoff} icon={dropoffIcon}>
              <Popup>
                <div className="text-slate-900">
                  <strong>Rider {rider.id} - Dropoff</strong>
                  <br />
                  Location: {rider.dropoff[0].toFixed(4)}, {rider.dropoff[1].toFixed(4)}
                </div>
              </Popup>
            </Marker>
            {!optimizationResult && (
              <Polyline
                positions={[rider.pickup, rider.dropoff]}
                color="#64748b"
                weight={2}
                opacity={0.5}
                dashArray="5, 10"
              />
            )}
          </React.Fragment>
        ))}

        {/* Render drivers */}
        {drivers.map((driver) => (
          <Marker key={`driver-${driver.id}`} position={driver.location} icon={driverIcon}>
            <Popup>
              <div className="text-slate-900">
                <strong>Driver {driver.id}</strong>
                <br />
                Capacity: {driver.capacity} passengers
                <br />
                Location: {driver.location[0].toFixed(4)}, {driver.location[1].toFixed(4)}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render optimized routes */}
        {optimizationResult && optimizationResult.matches.map((match, index) => {
          const color = routeColors[index % routeColors.length];
          const route = match.route.map(loc => [loc.lat, loc.lon]);

          return (
            <Polyline
              key={`route-${match.driver_id}`}
              positions={route}
              color={color}
              weight={4}
              opacity={0.8}
            />
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MapView;
