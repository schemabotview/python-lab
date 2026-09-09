import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'

// Caches the Pyodide runtime for repeat visits. Registered after load so it
// never competes with the first paint, and failures are non-fatal — the app
// works fine without it, just with a slower cold start.
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    // Registering at <base>sw.js also scopes the worker to <base>, which is
    // exactly the subtree it caches.
    navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js`).catch(() => {});
  });
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
