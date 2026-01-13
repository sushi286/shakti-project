import Controls from "./components/Controls";
import MapView from "./components/MapView";
import Contacts from "./components/Contacts";
import Chatbot from "./components/Chatbot";
import SOSButton from "./components/SOSButton";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <div className="header">
        <h2>SHAKTI – Smart Routes for Safer Journeys</h2>
        <p>AI-powered safety-first navigation for women & night commuters</p>
      </div>

      <div className="card"><Controls /></div>
      <div className="card"><MapView /></div>
      <div className="card"><Contacts /></div>
      <div className="card"><Chatbot /></div>
      <div className="card"><SOSButton /></div>
    </div>
  );
}

export default App;
