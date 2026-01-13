import { useState } from "react";

function Chatbot() {
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);

  const send = () => {
    if (!msg) return;
    setChat([...chat, "You: " + msg, "Bot: Stay on well-lit roads and avoid isolated areas."]);
    setMsg("");
  };

  return (
    <>
      {/* Floating Button */}
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
          zIndex: 1000
        }}
      >
        🤖
      </div>

      {/* Chat Window */}
      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "90px",
            right: "20px",
            width: "280px",
            background: "white",
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
            padding: "10px",
            zIndex: 1000
          }}
        >
          <h4>Safety Assistant</h4>

          <div style={{
            height: "120px",
            overflowY: "auto",
            border: "1px solid #ddd",
            padding: "5px",
            marginBottom: "5px"
          }}>
            {chat.map((c, i) => <p key={i}>{c}</p>)}
          </div>

          <input
            value={msg}
            onChange={e => setMsg(e.target.value)}
            placeholder="Ask something..."
            style={{ width: "95%", marginBottom: "5px" }}
          />

          <button onClick={send} style={{ width: "100%" }}>
            Send
          </button>
        </div>
      )}
    </>
  );
}

export default Chatbot;
