import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import "./App.css";
import Dashboard from "./Dashboard";

function LandingPage() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Later you can grab form data here and send it to an API
    // const formData = new FormData(e.target);
    // const email = formData.get("email");
    // ...

    navigate("/dashboard");
  };

  return (
    <div className="page">
      {/* Left: Form */}
      <div className="left-pane">
        <div className="form-card">
          <h1>Welcome Back</h1>
          <p className="subtitle">
            Sign in to continue to your dashboard.
          </p>

          <form onSubmit={handleSubmit}>

            <div className="field">
              <label htmlFor="state">State</label>
              <input
                id="state"
                name="state"
                type="text"
                placeholder="e.g. NY"
              />
            </div>

            <div className="field">
              <label htmlFor="city">City</label>
              <input
                id="city"
                name="city"
                type="text"
                placeholder="e.g. New York"
              />
            </div>

            <div className="field">
              <label htmlFor="zip">Zip Code</label>
              <input
                id="zip"
                name="zip"
                type="text"
                placeholder="e.g. 10001"
              />
            </div>

            <button type="submit" className="primary-btn">
              Sign In
            </button>
          </form>
        </div>
      </div>

      {/* Right: Image */}
      <div className="right-pane">
        <img
          src="https://via.placeholder.com/800x800"
          alt="App preview"
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
