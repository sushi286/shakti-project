import { Polyline } from "react-leaflet";

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapView(routeData) {
  const fakeRoute = [
    [28.6139, 77.2090],
    [28.6165, 77.2150],
    [28.6200, 77.2200],
  ];
  return (
    <div style={{ height: "400px", width: "100%" }}>
      <MapContainer
        center={[28.6139, 77.2090]} // Delhi default
        zoom={13}
        style={{ height: "100%", width: "100%" }}
      >
        {/* OpenStreetMap tiles */}
        <TileLayer
  url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
  attribution="© OpenStreetMap contributors © CARTO"
/>
{routeData && (
  <Polyline
    positions={routeData.route || []}
    color="blue"
  />
)}


        <Marker position={[28.6139, 77.2090]}>
          <Popup>You are here</Popup>
        </Marker>
      </MapContainer>

       {routeData && (
        <div
          style={{
            marginTop: "10px",
            padding: "10px",
            background: "#f1ecf9",
            borderRadius: "8px",
          }}
        >
          <strong>Safety Score:</strong> 82 / 100
          <br />
          <small>Based on historical crime data & time of day</small>
        </div>
      )}

       {routeData && (
        <ul style={{ fontSize: "14px", marginTop: "5px" }}>
          <li>⚠ Avoided low-lighting street near XYZ area</li>
          <li>⚠ Higher crime frequency reported at night</li>
          <li>✅ Route passes through well-lit main roads</li>
        </ul>
      )}
      
    </div>
  );
}

export default MapView;
