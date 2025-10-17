// src/pages/LoginPage.jsx
import React, { useState } from "react";
import { api } from "../services/api";

export default function LoginPage({ onLogin }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      if (isRegistering) {
        const data = await api.register(username, password);
        if (data.msg) {
          setMessage("Registration successful! Please log in.");
          setIsRegistering(false);
        } else {
          setError(data.detail || "Registration failed.");
        }
      } else {
        const data = await api.login(username, password);
        if (data.access_token) {
          onLogin(data.access_token);
        } else {
          setError("Invalid credentials.");
        }
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">{isRegistering ? "Register" : "Login"}</h1>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="error-message">{error}</p>}
          {message && <p className="success-message">{message}</p>}

          <div className="login-actions">
            <button type="submit" className="btn btn-primary" style={{ width: "auto" }}>
              {isRegistering ? "Register" : "Sign In"}
            </button>

            <button
              type="button"
              onClick={() => {
                setIsRegistering(!isRegistering);
                setError("");
                setMessage("");
              }}
              className="btn-link"
            >
              {isRegistering ? "Already have an account?" : "Create an Account"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
