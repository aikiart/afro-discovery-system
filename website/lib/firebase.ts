import { initializeApp, getApps, getApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyChov-yTuzKJPFXyY8OWFlFv7Nq6-uwAQ4",
  authDomain: "afro-discovery-system.firebaseapp.com",
  projectId: "afro-discovery-system",
  storageBucket: "afro-discovery-system.firebasestorage.app",
  messagingSenderId: "735053823518",
  appId: "1:735053823518:web:21e3a74bb03b1b863c780f"
};

// Check if an app instance already exists before calling initializeApp
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

export const db = getFirestore(app);