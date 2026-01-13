import React, { useState } from "react";
import PhoneLogin from "./PhoneLogin";
import EmailLogin from "./EmailLogin";
import EmailSignup from "./EmailSignup";

export default function AuthPage() {
  const [activeTab, setActiveTab] = useState("phone");

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(135deg, #ffd5e5, #ffc6ff)"
    }}>
      <div style={{
        width: "380px",
        background: "white",
        padding: "30px",
        borderRadius: "15px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.15)",
      }}>

        <h2 style={{
          textAlign: "center",
          marginBottom: "20px",
          color: "#e91e63",
          fontWeight: "700"
        }}>
          Welcome to SHAKTI
        </h2>

        {/* TAB BUTTONS */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "25px",
        }}>
          <button
            onClick={() => setActiveTab("phone")}
            style={{
              flex: 1,
              padding: "10px",
              background: activeTab === "phone" ? "#e91e63" : "#ffe3ec",
              color: activeTab === "phone" ? "white" : "#e91e63",
              fontWeight: "bold",
              border: "none",
              borderRadius: "8px",
              marginRight: "5px",
              cursor: "pointer",
            }}
          >
            Phone
          </button>

          <button
            onClick={() => setActiveTab("email")}
            style={{
              flex: 1,
              padding: "10px",
              background: activeTab === "email" ? "#e91e63" : "#ffe3ec",
              color: activeTab === "email" ? "white" : "#e91e63",
              fontWeight: "bold",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              marginLeft: "5px",
            }}
          >
            Email
          </button>
        </div>

        {/* TAB CONTENT */}
        {activeTab === "phone" && (
          <div>
            <PhoneLogin />
          </div>
        )}

        {activeTab === "email" && (
          <div>
            <EmailSignup />
            <div style={{ height: "15px" }}></div>
            <EmailLogin />
          </div>
        )}
      </div>
    </div>
  );
}
