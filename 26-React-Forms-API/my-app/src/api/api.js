// src/api/api.js
import axios from "axios";

/**
 * Base URL is read from the Vite environment variable.
 * Fallback to localhost for safety during development.
 */
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Reusable Axios instance.
 * Every API call in the app should import this instead of `axios` directly.
 */
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 15000, // 15s — fail fast if backend is down
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

/* ------------------------------------------------------------------ */
/*  Request Interceptor — attach JWT token                            */
/* ------------------------------------------------------------------ */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // adjust key if your app uses a different one

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

/* ------------------------------------------------------------------ */
/*  Response Interceptor — normalize errors, handle 401               */
/* ------------------------------------------------------------------ */
api.interceptors.response.use(
  // Success — pass response straight through
  (response) => response,

  // Error — translate Axios errors into friendly, structured messages
  (error) => {
    let friendlyMessage = "Something went wrong. Please try again.";
    let status = null;

    if (error.response) {
      // Server responded with a status outside 2xx
      status = error.response.status;
      const data = error.response.data;

      switch (status) {
        case 400:
          friendlyMessage =
            data?.detail || "Invalid data. Please check your input.";
          break;
        case 401:
          friendlyMessage = "Session expired. Please login again.";
          // Optional: clear token and redirect to login
          localStorage.removeItem("token");
          // window.location.href = "/login"; // uncomment if you want auto-redirect
          break;
        case 403:
          friendlyMessage =
            "You do not have permission to perform this action.";
          break;
        case 404:
          friendlyMessage = data?.detail || "Requested resource not found.";
          break;
        case 422:
          // FastAPI validation error shape: { detail: [ { msg, loc }, ... ] }
          if (Array.isArray(data?.detail)) {
            friendlyMessage = data.detail
              .map((e) => e.msg)
              .join(", ");
          } else {
            friendlyMessage = data?.detail || "Validation failed.";
          }
          break;
        case 500:
          friendlyMessage = "Server error. Please try again later.";
          break;
        default:
          friendlyMessage = data?.detail || `Request failed (${status}).`;
      }
    } else if (error.request) {
      // Request was made but no response (backend down / network issue)
      friendlyMessage =
        "Unable to reach the server. Please check your connection.";
    } else {
      // Something went wrong setting up the request
      friendlyMessage = error.message || friendlyMessage;
    }

    // Reject with a clean, predictable shape
    return Promise.reject({
      status,
      message: friendlyMessage,
      original: error,
    });
  }
);

export default api;
export { BASE_URL };