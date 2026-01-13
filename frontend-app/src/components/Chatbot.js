import { useState } from "react";

function Chatbot() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Floating Toggle Button */}
      <div
        onClick={() => setOpen(!open)}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          width: "60px",
          height: "60px",
          borderRadius: "50%",
          background: "#5a2ca0",
          color: "white",
          fontSize: "28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
          zIndex: 3000,
        }}
      >
        🤖
      </div>

      {/* Botpress Chat Window */}
      {open && (
        <iframe
          title="Safety Assistant"
          src="https://cdn.botpress.cloud/webchat/v3.5/shareable.html?configUrl=https://files.bpcontent.cloud/2025/09/08/17/20250908171155-RB0CMY1U.json"
          style={{
            position: "fixed",
            bottom: "90px",
            right: "20px",
            width: "360px",
            height: "520px",
            border: "none",
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.3)",
            zIndex: 3000,
            background: "white",
          }}
        />
      )}
    </>
  );
}

export default Chatbot;
