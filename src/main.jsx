import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

console.log("--> main.jsx started loading");

const rootElement = document.getElementById('root');

if (!rootElement) {
  console.error("CRITICAL ERROR: Could not find element with id 'root' in index.html");
} else {
  try {
    console.log("--> Mounting React root...");
    ReactDOM.createRoot(rootElement).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    console.log("--> React root mounted successfully");
  } catch (err) {
    console.error("CRITICAL ERROR during React rendering:", err);
  }
}