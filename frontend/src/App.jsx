import React from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import Dashboard from "./Dashboard"
import "./App.css";

/* -------------------------
   Landing Page (Form)
-------------------------- */
function LandingPage() {
  const navigate = useNavigate();
  const [errors, setErrors] = React.useState({});

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const address1 = (formData.get("address1") || "").trim();
    const city = (formData.get("city") || "").trim();
    const state = (formData.get("state") || "").trim();
    const zip = (formData.get("zip") || "").trim();

    const newErrors = {};

    if (address1.length < 5) {
      newErrors.address1 = "Please enter a valid street address.";
    }

    if (!/^[A-Za-z\s.'-]+$/.test(city) || city.length < 2) {
      newErrors.city =
        "City must contain letters only (spaces, . ' - allowed).";
    }

    if (!/^[A-Za-z]{2}$/.test(state)) {
      newErrors.state = "State must be 2 letters (e.g., NY).";
    }

    if (!/^\d{5}$/.test(zip)) {
      newErrors.zip = "Zip must be 5 digits (e.g., 10001).";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) return;

    navigate("/dashboard");
  };

  return (
    <div className="page">
      <div className="left-pane">
        <div className="form-card">
          <h1>Welcome Back</h1>
          <p className="subtitle">
            Enter your information to continue to your dashboard.
          </p>

          <form onSubmit={handleSubmit} noValidate>
            {/* Street Address */}
            <div className="field">
              <label htmlFor="address1">Street Address</label>
              <input
                id="address1"
                name="address1"
                type="text"
                placeholder="123 Main St"
                className={errors.address1 ? "input-error" : ""}
              />
              {errors.address1 && (
                <div className="error">{errors.address1}</div>
              )}
            </div>


            {/* City */}
            <div className="field">
              <label htmlFor="city">City</label>
              <input
                id="city"
                name="city"
                type="text"
                placeholder="New York"
                className={errors.city ? "input-error" : ""}
                onChange={(e) => {
                  e.target.value = e.target.value.replace(
                    /[^A-Za-z\s.'-]/g,
                    ""
                  );
                }}
              />
              {errors.city && <div className="error">{errors.city}</div>}
            </div>

            {/* State */}
            <div className="field">
              <label htmlFor="state">State</label>
              <input
                id="state"
                name="state"
                type="text"
                placeholder="NY"
                maxLength={2}
                className={errors.state ? "input-error" : ""}
                onChange={(e) => {
                  e.target.value = e.target.value
                    .replace(/[^A-Za-z]/g, "")
                    .toUpperCase();
                }}
              />
              {errors.state && <div className="error">{errors.state}</div>}
            </div>

            {/* Zip Code */}
            <div className="field">
              <label htmlFor="zip">Zip Code</label>
              <input
                id="zip"
                name="zip"
                type="text"
                placeholder="10001"
                inputMode="numeric"
                maxLength={5}
                className={errors.zip ? "input-error" : ""}
                onChange={(e) => {
                  e.target.value = e.target.value.replace(/\D/g, "");
                }}
              />
              {errors.zip && <div className="error">{errors.zip}</div>}
            </div>

            <button type="submit" className="primary-btn">
              Continue
            </button>
          </form>
        </div>
      </div>

      <div className="right-pane">
        <img
          src="https://via.placeholder.com/800x800"
          alt="Application preview"
        />
      </div>
    </div>
  );
}

/* -------------------------
   App Router
-------------------------- */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}