import React, { useState } from "react";
import { auth, RecaptchaVerifier, signInWithPhoneNumber } from "../firebase";

function PhoneLogin() {
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");

  const generateRecaptcha = () => {
    if (!window.recaptchaVerifier) {
      window.recaptchaVerifier = new RecaptchaVerifier(
        auth,
        "recaptcha-container",
        {
          size: "invisible",
          callback: (response) => {
            console.log("Recaptcha Resolved");
          },
        }
      );
    }
  };

  const sendOTP = () => {
    if (phone.length < 10) return alert("Enter valid phone number");

    generateRecaptcha();
    const appVerifier = window.recaptchaVerifier;

    signInWithPhoneNumber(auth, phone, appVerifier)
      .then((confirmationResult) => {
        window.confirmationResult = confirmationResult;
        alert("OTP Sent!");
      })
      .catch((error) => {
        console.error(error);
        alert(error.message);
      });
  };

  const verifyOTP = () => {
    if (!otp) return alert("Enter OTP");

    window.confirmationResult
      .confirm(otp)
      .then((result) => {
        alert("Login Successful");
        console.log(result.user);
      })
      .catch((error) => {
        console.error(error);
        alert("Invalid OTP");
      });
  };

  return (
    <div style={{ padding: 20, background: "#ffd5e5", minHeight: "100vh" }}>
      <h1>Phone Login</h1>

      <input
        type="text"
        placeholder="+91XXXXXXXXXX"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <br /><br />

      <div id="recaptcha-container"></div>

      <button onClick={sendOTP}>Send OTP</button>
      <br /><br />

      <input
        type="text"
        placeholder="Enter OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
      />
      <br /><br />

      <button onClick={verifyOTP}>Verify OTP</button>
    </div>
  );
}

export default PhoneLogin;
