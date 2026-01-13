import { useState, useEffect } from "react";
import Controls from "./components/Controls";
import MapView from "./components/MapView";
import Contacts from "./components/Contacts"; // optional
import Chatbot from "./components/Chatbot";
import SOSButton from "./components/SOSButton";
import Sidebar from "./components/Sidebar";
import "./App.css";

import { auth } from "./firebase";
import { onAuthStateChanged, signOut } from "firebase/auth";

import AuthPage from "./components/AuthPage";

function App() {
<<<<<<< Updated upstream
  const [routeData, setRouteData] = useState(null);
=======
  const [user, setUser] = useState(null);
>>>>>>> Stashed changes
  const [menuOpen, setMenuOpen] = useState(false);

  // Track logged-in user
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  // If not logged in -> show the beautiful login UI
  if (!user) {
    return <AuthPage />;
  }

  // Logged in -> show full app
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

      {/* Logout Button */}
      <button
        onClick={() => signOut(auth)}
        style={{
          position: "fixed",
          top: "10px",
          right: "10px",
          fontSize: "14px",
          cursor: "pointer",
          zIndex: 3000,
          background: "white",
          padding: "6px 10px",
          borderRadius: "8px",
          boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
        }}
      >
        Logout
      </button>

      {/* Main App Content */}
      <div className="app-container">
        <div className="header">
          <h2>SHAKTI – Smart Routes for Safer Journeys</h2>
          <p>AI-powered safety-first navigation for women & night commuters</p>
        </div>

<<<<<<< Updated upstream
       <div className="card">
  <Controls onRoute={setRouteData} />
</div>

<div className="card">
  <MapView routeData={routeData} />
</div>

        <div className="card"><SOSButton /></div>
=======
        <div className="card">
          <Controls />
        </div>

        <div className="card">
          <MapView />
        </div>

        <div className="card">
          <SOSButton />
        </div>

        {/* Optional extra components */}
        {/* <div className="card"><Contacts /></div> */}
>>>>>>> Stashed changes

        <Chatbot />
      </div>
    </>
  );
}

export default App;
