import { initializeApp } from "firebase/app";
import { getAuth, RecaptchaVerifier, signInWithPhoneNumber } from "firebase/auth";

// paste your firebaseConfig here
const firebaseConfig = {
  apiKey: "AIzaSyAXWjUuxpJOiWjCUzy8XQQ9aZT9hEdj6rA",
  authDomain: "shakti-c1659.firebaseapp.com",
  projectId: "shakti-c1659",
  storageBucket: "shakti-c1659.firebasestorage.app",
  messagingSenderId: "605596826488",
  appId: "1:605596826488:web:f8f863d082efc1b3eae68d",
  measurementId: "G-C1CN222S0B"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export { RecaptchaVerifier, signInWithPhoneNumber };
