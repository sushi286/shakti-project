import { useState } from "react";
import { auth } from "../firebase";
import { signInWithEmailAndPassword } from "firebase/auth";

export default function EmailLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = () => {
    signInWithEmailAndPassword(auth, email, password)
      .then(() => alert("Logged in!"))
      .catch((err) => alert(err.message));
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>
      <input type="email" placeholder="Email"
        value={email} onChange={(e) => setEmail(e.target.value)} />
      <br /><br />
      <input type="password" placeholder="Password"
        value={password} onChange={(e) => setPassword(e.target.value)} />
      <br /><br />
      <button onClick={login}>Login</button>
    </div>
  );
}
