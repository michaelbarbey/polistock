import React, { useState } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { getUSStates, getCitiesOfState } from "./data/statesData";
import "./App.css";
import Dashboard from "./Dashboard";
import { getOfficialByAddress } from "./services/api"; // importing backend api

function LandingPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // fetch zip code data
  const handleZipChange = async (e) => {
    const zip = e.target.value;

    // 5 digit delimeter
    if (zip.length !== 5) return;

    setLoading(true);
    try {
      // calls Zippopotam no API required
      const response = await fetch(`https://api.zippopotam.us/us/${zip}`);

      if (!response.ok) throw new Error("Invalid Zip");

      const data = await response.json();
      const place = data.places[0];

      // corresponding state isocode and city name
      const stateCode = place["state abbreviation"];
      const cityName = place["place name"];

      // state name
      setSelectedState(stateCode);

      // city names based on location, manual update if needed
      const citiesList = await getCitiesOfState(stateCode);
      setCities(citiesList);

      // sets the specific city if changed manually
      const cityExists = citiesList.some((c) => c.name === cityName);
      if (!cityExists) {
        setCities((prev) =>
          [...prev, { name: cityName }].sort((a, b) =>
            a.name.localeCompare(b.name)
          )
        );
      }
      setSelectedCity(cityName);

      setError(""); //clears any old errors
    } catch (err) {
      console.error(err);
      setError("Could not find this Zip Code");
    } finally {
      setLoading(false);
    }
  };

  // dropdown menu
  const [selectedState, setSelectedState] = useState("");
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState("");

  //const states = getUSStates();
  const [states, setStates] = useState([]);
  React.useEffect(() => {
    try {
      const statesList = getUSStates();
      setStates(statesList);
    } catch (err) {
      console.error("Error loading states:", err);
      setError("Failed to load states data");
      setStates([]);
    }
  }, []);

  const handleStateChange = async (e) => {
    const stateCode = e.target.value;
    console.log("Selected state code:", stateCode);
    console.log("Type:", typeof stateCode);

    setSelectedState(stateCode);
    setSelectedCity("");
    setCities([]); // initializes as empty array

    if (stateCode) {
      try {
        console.log("Calling getCitiesOfState with:", stateCode);
        const stateCities = await getCitiesOfState(stateCode);

        console.log("Received cities:", stateCities);
        console.log("Is array?", Array.isArray(stateCities));

        // ensures it's an array
        if (Array.isArray(stateCities)) {
          setCities(stateCities);
        } else {
          console.error("Cities is not an array:", stateCities);
          setCities([]);
        }
      } catch (error) {
        console.error("Error loading cities:", error);
        setCities([]);
      }
    } else {
      setCities([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // gets form data
      const formData = new FormData(e.target);
      const address = {
        street: formData.get("street") || "",
        city: selectedCity,
        state: selectedState,
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
          <h1>polidemos</h1>
          <p className="subtitle">
            Find your congressional representative and track their stock trades.
          </p>

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="street">Street Address</label>
              <input
                id="street"
                name="street"
                type="text"
                placeholder="123 Sesame St"
              />
            </div>

            <div className="field">
              <label htmlFor="zip">Zip Code *</label>
              <input
                id="zip"
                name="zip"
                type="text"
                placeholder="90210"
                maxLength={5} // prevents typing more than 5 digits
                onChange={handleZipChange} // hooks up the new function
                required
              />
            </div>

            <div className="field">
              <label htmlFor="state">State *</label>
              <select
                id="state"
                name="state"
                value={selectedState}
                onChange={handleStateChange}
                required
                style={{
                  height: "45px",
                  width: "100%",
                  padding: "20px",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                  fontSize: "16px",
                }}
              >
                <option value="">Select a state</option>
                {states.map((state) => (
                  <option key={state.isoCode} value={state.isoCode}>
                    {state.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label htmlFor="city">City *</label>
              <select
                id="city"
                name="city"
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                disabled={!selectedState}
                required
                style={{
                  height: "45px",
                  width: "100%",
                  padding: "12px",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                  fontSize: "16px",
                  /*backgroundColor: !selectedState ? "#f5f5f5" : "white",*/
                }}
              >
                <option value="">
                  {selectedState ? "Select a city" : "Select a state first"}
                </option>
                {cities.map((city) => (
                  <option key={city.name} value={city.name}>
                    {city.name}
                  </option>
                ))}
              </select>
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
        <video autoPlay loop>
          <source
            src="https://cdn.openai.com/ctf-cdn/Research-Blog-16x9_Delivery.mp4"
            alt="Telescope"
            type="video/mp4"
          />
        </video>
      </div>
    </div>
  );
}

// export default LandingPage;
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
