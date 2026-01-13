import { useState } from "react";

function Sidebar({ isOpen, closeSidebar }) {
  const [location, setLocation] = useState(null);
  const [contacts, setContacts] = useState([]);
  const [name, setName] = useState("");

  const getLocation = () => {
    navigator.geolocation.getCurrentPosition((pos) => {
      setLocation({
        lat: pos.coords.latitude.toFixed(4),
        lng: pos.coords.longitude.toFixed(4),
      });
    });
  };

  const addContact = () => {
    if (!name) return;
    setContacts([...contacts, name]);
    setName("");
  };

  if (!isOpen) return null; // hide sidebar when closed

  return (
    <div style={styles.sidebar}>
      <button onClick={closeSidebar} style={styles.closeBtn}>✕</button>

      <h3>📍 Live Location</h3>
      <button onClick={getLocation}>Get My Location</button>

      {location && (
        <p>Lat: {location.lat}<br />Lng: {location.lng}</p>
      )}

      <hr />

      <h3>⭐ Favourite Contacts</h3>
      <input
        placeholder="Contact name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={addContact}>Add</button>

      <ul>
        {contacts.map((c, i) => <li key={i}>{c}</li>)}
      </ul>
    </div>
  );
}

const styles = {
 sidebar: {
  width: "260px",
  height: "100vh",
  background: "#f1ecf9",
  position: "fixed",
  top: 0,
  left: 0,
  padding: "60px 15px 15px 15px", // 👈 more space at top
  borderRight: "1px solid #ddd",
  zIndex: 2000,
},

  closeBtn: {
    float: "right",
    background: "none",
    border: "none",
    fontSize: "20px",
    cursor: "pointer",
  }
};

export default Sidebar;
