function SOSButton({ contacts }) {

  const handleSOS = () => {
    if (contacts.length === 0) {
      alert("No emergency contacts added!");
      return;
    }

    const confirmSOS = window.confirm(
      "Are you sure you want to send SOS alert with live location?"
    );

    if (!confirmSOS) return;

    // Get live location
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;

        const mapLink = `https://maps.google.com/?q=${lat},${lng}`;

        let message = "🚨 SOS Alert Sent!\n\n";
        message += "Message sent to:\n";

        contacts.forEach((c) => {
          message += `${c.name} (${c.phone})\n`;
        });

        message += `\nMessage content:\n`;
        message += `"I am in danger. My live location is: ${mapLink}"`;

        alert(message);
      },
      () => {
        alert("Unable to fetch live location. Please enable GPS.");
      }
    );
  };

  return (
    <button
      onClick={handleSOS}
      style={{
        background: "red",
        color: "white",
        padding: "14px",
        borderRadius: "12px",
        width: "100%",
        fontWeight: "bold",
        fontSize: "16px",
      }}
    >
      🚨 SEND SOS ALERT
    </button>
  );
}

export default SOSButton;
