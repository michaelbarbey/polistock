import React, { useState } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import Dashboard from "./Dashboard";
import { getOfficialByAddress } from "./services/api"; // importing backend api

function LandingPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // gets form data
      const formData = new FormData(e.target);
      const address = {
        street: formData.get("street") || "",
        city: formData.get("city"),
        state: formData.get("state"),
        zipcode: formData.get("zip"),
      };

      if (!address.city || !address.state || !address.zipcode) {
        setError("Please fill in all required fields");
        setLoading(false);
        return;
      }

      // calls backend api
      const officialData = await getOfficialByAddress(address);

      // navigate to dashboard
      navigate("/dashboard", { state: { official: officialData } });
    } catch (err) {
      setError(
        err.message || "Failed to fetch official data. Please try again."
      );
      setLoading(false);
    }
  };

  return (
    <div className="page">
      {/* Left: Form */}
      <div className="left-pane">
        <div className="form-card">
          <h1>polistock</h1>
          <p className="subtitle">
            Find your congressional representative and track their stock trades.
          </p>

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="street">Street Address </label>
              <input
                id="street"
                name="street"
                type="text"
                placeholder="123 Sesame St"
                required
              />
            </div>

            <div className="field">
              <label htmlFor="city">City</label>
              <input
                id="city"
                name="city"
                type="text"
                placeholder="Cupertino"
                required
              />
            </div>

            <div className="field">
              <label htmlFor="state">State</label>
              <input
                id="state"
                name="state"
                type="text"
                placeholder="California - CA"
                required
              />
            </div>

            <div className="field">
              <label htmlFor="zip">Zip Code</label>
              <input
                id="zip"
                name="zip"
                type="text"
                placeholder="10001"
                required
              />
            </div>

            {error && (
              <div
                style={{
                  padding: "12px",
                  backgroundColor: "#fee",
                  color: "#c33",
                  borderRadius: "8px",
                  marginBottom: "16px",
                }}
              >
                {error}
              </div>
            )}

            <button type="submit" className="primary-btn" disabled={loading}>
              {loading ? "Searching..." : "Search"}
            </button>
          </form>
        </div>
      </div>

      {/* Right: Image */}
      <div className="right-pane">
        <img
          src="https://via.placeholder.com/800x800"
          alt="Congressional Tracking"
        />
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
