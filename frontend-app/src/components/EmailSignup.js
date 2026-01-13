import { useState } from "react";
import { auth } from "../firebase";
import { createUserWithEmailAndPassword } from "firebase/auth";

export default function EmailSignup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const signUp = () => {
    createUserWithEmailAndPassword(auth, email, password)
      .then(() => alert("Signup successful!"))
      .catch((err) => alert(err.message));
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Sign Up</h2>
      <input type="email" placeholder="Email"
        value={email} onChange={(e) => setEmail(e.target.value)} />
      <br /><br />
      <input type="password" placeholder="Password"
        value={password} onChange={(e) => setPassword(e.target.value)} />
      <br /><br />
      <button onClick={signUp}>Create Account</button>
    </div>
  );
}
