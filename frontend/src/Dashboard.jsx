import React, { useState } from "react";
import { collection, query, where, getDocs, limit } from "firebase/firestore";
import { db } from "./firebase"; // adjust path if needed
import "./Dashboard.css";
 

/* ===============================
   Firestore ZIP lookup helper
   =============================== */
async function fetchZipLookup(zip) {
  const projectId = import.meta.env.VITE_FIRESTORE_PROJECT_ID;
  const apiKey = import.meta.env.VITE_FIRESTORE_API_KEY;
  const col = import.meta.env.VITE_FIRESTORE_ZIP_COLLECTION || "zip_lookup";

  if (!projectId || !apiKey) throw new Error("Missing Firestore env vars");

  const url =
    `https://firestore.googleapis.com/v1/projects/${projectId}` +
    `/databases/(default)/documents/${col}/${zip}?key=${apiKey}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("ZIP not found");
  const doc = await res.json();

  const f = doc?.fields || {};
  const s = (k) => f?.[k]?.stringValue ?? "";

  return {
    zip: s("zip"),
    fullName: s("fullName"),
    state: s("state"),
    party: s("party"),
    stateDistrictRaw: s("stateDistrictRaw"),
    bioguideId: s("bioguideId"),
  };
}

/* ===============================
   Dashboard Component
   =============================== */
function Dashboard() {
  /* 🔹 NEW: Quick Search state */
  const [zip, setZip] = useState("");
const [qsLoading, setQsLoading] = useState(false);
const [qsError, setQsError] = useState("");
const [qsResult, setQsResult] = useState(null);

async function handleQuickSearch(e) {
  e.preventDefault();
  setQsError("");
  setQsResult(null);

  const z = zip.trim();
  if (!z) {
    setQsError("Enter a ZIP code.");
    return;
  }

  setQsLoading(true);
  try {
    // IMPORTANT: collection name must match yours exactly
    const membersRef = collection(db, "members");

    // zipCode stored as STRING in Firestore? then compare to string z
    const q = query(membersRef, where("zipCode", "==", z), limit(1));
    const snap = await getDocs(q);

    if (snap.empty) {
      setQsError("No representative found for that ZIP.");
      return;
    }

    const data = snap.docs[0].data();

    // Display only what you want
    setQsResult({
      fullName: data.fullName,
      state: data.state,
      party: data.party,
      stateDistrictRaw: data.stateDistrictRaw,
    });
  } catch (err) {
    setQsError("Quick Search failed.");
  } finally {
    setQsLoading(false);
  }
}


  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="dashboard-logo">
          <span className="logo-dot" />
          <span className="logo-text">MyApp</span>
        </div>

        <nav className="dashboard-nav">
          <button className="nav-item nav-item-active">Overview</button>
          <button className="nav-item">Users</button>
          <button className="nav-item">Reports</button>
          <button className="nav-item">Settings</button>
        </nav>

        <div className="dashboard-sidebar-footer">
          <span className="sidebar-footer-text">Signed in as</span>
          <span className="sidebar-footer-name">Demo User</span>
        </div>
      </aside>

      {/* Main content */}
      <div className="dashboard-main">
        {/* Header */}
        <header className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Dashboard</h1>
            <p className="dashboard-subtitle">
              Welcome back. Here’s a quick snapshot of your profile and key info.
            </p>
          </div>

          <div className="dashboard-header-actions">
            <button className="outline-btn">Export</button>
            <button className="primary-btn">New Entry</button>
          </div>
        </header>

        {/* Main content area */}
        <main className="dashboard-content">

          {/* 🔹 NEW SECTION: Quick Search */}
          <section className="quick-search">
            <h2 className="info-section-title">Quick Search</h2>

            <form onSubmit={handleQuickSearch} style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12 }}>
              <input
                placeholder="ZIP Code (e.g. 10465)"
                value={zip}
                onChange={(e) => setZip(e.target.value)}
                style={{ padding: 10, borderRadius: 10 }}
              />

              <button className="primary-btn" type="submit" disabled={qsLoading}>
                {qsLoading ? "Searching..." : "Search"}
              </button>
            </form>

            {qsError && <p>{qsError}</p>}

            {qsResult && (
              <div>
                <p><strong>Name:</strong> {qsResult.fullName}</p>
                <p><strong>State:</strong> {qsResult.state}</p>
                <p><strong>Party:</strong> {qsResult.party}</p>
                <p><strong>District:</strong> {qsResult.stateDistrictRaw}</p>
              </div>
            )}
          </section>


          {/* SECTION 1: Profile layout */}
          <section className="profile-section">
            <div className="profile-avatar-wrapper">
              <div className="profile-avatar">
                <span className="profile-initials">JS</span>
              </div>
            </div>

            <div className="profile-text">
              <h2 className="profile-name">Demo User</h2>
              <p className="profile-title">Community Program Participant</p>
              <p className="profile-description">
                This area can be used to briefly describe the user, their role,
                or the purpose of this dashboard.
              </p>
            </div>
          </section>

          {/* SECTION 2: Info cards grid */}
          <section className="info-section">
            <h2 className="info-section-title">Key Information</h2>

            <div className="info-grid">
              <article className="info-card">
                <h3 className="info-card-title">Program Status</h3>
                <p className="info-card-body">
                  Currently enrolled in the Spring 2025 cohort.
                </p>
                <p className="info-card-meta">Last updated: Today</p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">Location Details</h3>
                <p className="info-card-body">
                  Based in New York, NY (10001).
                </p>
                <p className="info-card-meta">Source: Profile form</p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">Recent Activity</h3>
                <p className="info-card-body">
                  Submitted an intake form and updated contact details.
                </p>
                <p className="info-card-meta">Last 7 days</p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">Support Contact</h3>
                <p className="info-card-body">
                  Assigned Case Manager: Jordan Lee.
                </p>
                <p className="info-card-meta">~24h response</p>
              </article>
            </div>
          </section>

        </main>
      </div>
    </div>
  );
}

export default Dashboard;
