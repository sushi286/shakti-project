import { useState } from "react";
import Controls from "./components/Controls";
import MapView from "./components/MapView";
import Contacts from "./components/Contacts";
import Chatbot from "./components/Chatbot";
import SOSButton from "./components/SOSButton";
import Sidebar from "./components/Sidebar";
import "./App.css";

function App() {
  const [routeData, setRouteData] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      {/* Menu Button */}
      <div
        onClick={() => setMenuOpen(true)}
        style={{
           position: "fixed",
    top: "10px",
    left: "10px",
    fontSize: "26px",
    cursor: "pointer",
    zIndex: 3000,
    background: "white",
    padding: "6px 10px",
    borderRadius: "8px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
        }}
      >
        ☰


      </div>

      {/* Sidebar */}
      <Sidebar isOpen={menuOpen} closeSidebar={() => setMenuOpen(false)} />

      {/* Main Content */}
      <div className="app-container">
        <div className="header">
          <h2>SHAKTI – Smart Routes for Safer Journeys</h2>
          <p>AI-powered safety-first navigation for women & night commuters</p>
        </div>

       <div className="card">
  <Controls onRoute={setRouteData} />
</div>

<div className="card">
  <MapView routeData={routeData} />
</div>

        <div className="card"><SOSButton /></div>

        <Chatbot />
      </div>
    </>
  );
}

export default App;
