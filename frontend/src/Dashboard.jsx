import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Dashboard.css";

function formatDateForDisplay(dateStr) {
  if (!dateStr) return "N/A";

  // Try YYYYMMDD format (20251202)
  try {
    const year = dateStr.substring(0, 4);
    const month = dateStr.substring(4, 6);
    const day = dateStr.substring(6, 8);
    const date = new Date(year, month - 1, day);

    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return dateStr;
  }
}
/* ===============================
   Firestore ZIP lookup helper
   =============================== */
/*
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
}/*

/* ===============================
   Dashboard Component
   =============================== */
/*
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
*/

function Dashboard() {
  /* 🔹 NEW: Quick Search state */
  const location = useLocation();
  const navigate = useNavigate();
  const official = location.state?.official;

  // edge case
  if (!official) {
    return (
      <div
        className="dashboard"
        style={{ padding: "40px", textAlign: "center" }}
      >
        <h2>No data available</h2>
        <p>Please search for a representative first.</p>
        <button className="primary-btn" onClick={() => navigate("/")}>
          Go Back
        </button>
      </div>
    );
  }
  const district = official.districts?.[0];
  const transactions = official.transactions || [];
  const articles = official.articles || [];

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="dashboard-logo">
          <span className="logo-dot" />
          <span className="logo-text">polistock</span>
        </div>

        <nav className="dashboard-nav">
          <button className="nav-item nav-item-active">Overview</button>
          <button className="nav-item">Transactions</button>
          <button className="nav-item">News</button>
          <button className="nav-item" onClick={() => navigate("/")}>
            Search
          </button>
        </nav>

        <div className="dashboard-sidebar-footer">
          <span className="sidebar-footer-text">Viewing</span>
          <span className="sidebar-footer-name">{official.fullname}</span>
        </div>
      </aside>

      {/* Main content */}
      <div className="dashboard-main">
        {/* Header */}
        <header
          className="dashboard-header"
          style={{
            backgroundColor: official.party
              ?.toLowerCase()
              .includes("democratic")
              ? "#002147"
              : official.party?.toLowerCase().includes("republican")
                ? "#BB133E"
                : "var(--bg-card)",
          }}
        >
          <div>
            <h1
              className="dashboard-title"
              tyle={{
                color:
                  official.party?.toLowerCase().includes("democratic") ||
                  official.party?.toLowerCase().includes("republican")
                    ? "#ffffff"
                    : "var(--text-primary)",
              }}
            >
              {official.fullname}
            </h1>
            <p
              className="dashboard-subtitle"
              style={{
                color:
                  official.party?.toLowerCase().includes("democratic") ||
                  official.party?.toLowerCase().includes("republican")
                    ? "rgba(255, 255, 255, 0.85)"
                    : "var(--text-secondary)",
              }}
            >
              {official.party} • {official.chamber} • District{" "}
              {district?.district_code}
            </p>
          </div>

          <div className="dashboard-header-actions">
            <button className="outline-btn">Export</button>
            <button className="primary-btn" onClick={() => navigate("/")}>
              Search
            </button>
          </div>
        </header>

        {/* Main content area */}
        <main className="dashboard-content">
          {/* Profile Section */}
          <section className="profile-section">
            <div className="profile-avatar-wrapper">
              <div className="profile-avatar">
                {official.photo_url ? (
                  <img
                    src={official.photo_url}
                    alt={official.fullname}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      borderRadius: "15%",
                    }}
                  />
                ) : (
                  <span className="profile-initials">
                    {official.firstname?.[0]}
                    {official.lastname?.[0]}
                  </span>
                )}
              </div>
            </div>

            <div className="profile-text">
              <h2 className="profile-name">{official.fullname}</h2>
              <p className="profile-title">
                {official.party} • {official.chamber}
              </p>
              <p className="profile-description">
                Representing {district?.city}, {district?.state_name} (District{" "}
                {district?.district_code})
                <br />
                Term: {official.term_start} to {official.term_end}
                <br />
                Bioguide ID: {official.bioguide_id}
              </p>
            </div>
          </section>

          {/* Transactional Data */}
          <section className="info-section">
            <h2 className="info-section-title">Overview</h2>

            <div className="info-grid">
              <article className="info-card">
                <h3 className="info-card-title">Total Transactions</h3>
                <p
                  className="info-card-body"
                  style={{ fontSize: "32px", fontWeight: "bold" }}
                >
                  {transactions.length}
                </p>
                <p className="info-card-meta">Tracked stock trades</p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">District</h3>
                <p className="info-card-body">
                  {district?.state_code}-{district?.district_code}
                </p>
                <p className="info-card-meta">
                  {district?.city}, {district?.state_name}
                </p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">Party</h3>
                <p className="info-card-body">{official.party}</p>
                <p className="info-card-meta">{official.chamber}</p>
              </article>

              <article className="info-card">
                <h3 className="info-card-title">News Articles</h3>
                <p
                  className="info-card-body"
                  style={{ fontSize: "32px", fontWeight: "bold" }}
                >
                  {articles.length}
                </p>
                <p className="info-card-meta">Related news</p>
              </article>
            </div>
          </section>

          {/* Transactions Table */}
          {transactions.length > 0 && (
            <section className="info-section">
              <h2 className="info-section-title">Recent Transactions</h2>

              <div className="table-container">
                <table className="transactions-table">
                  <thead>
                    <tr>
                      <th>Company</th>
                      <th>Ticker</th>
                      <th>Type</th>
                      <th>Amount</th>
                      <th>Traded Date</th>
                      <th>Published</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((txn, idx) => (
                      <tr key={idx}>
                        <td>{txn.company}</td>
                        <td>{txn.ticker_symbol || "N/A"}</td>
                        <td>
                          <span
                            className={`transaction-badge ${txn.transaction_type?.toLowerCase()}`}
                          >
                            {txn.transaction_type}
                          </span>
                        </td>
                        <td>{txn.stock_price}</td>
                        <td>{formatDateForDisplay(txn.traded_date)}</td>
                        <td>{formatDateForDisplay(txn.published_date)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* News Articles */}

          {articles.length > 0 && (
            <section className="info-section">
              <h2 className="info-section-title">Related News</h2>

              <div className="info-grid">
                {articles.map((article, idx) => (
                  <article key={idx} className="info-card">
                    {article.article_image && (
                      <img
                        src={article.article_image}
                        alt={article.headline}
                        style={{
                          width: "100%",
                          height: "150px",
                          objectFit: "cover",
                          borderRadius: "8px",
                          marginBottom: "12px",
                        }}
                      />
                    )}
                    <h3 className="info-card-title">{article.headline}</h3>
                    <p className="info-card-body">{article.article_short}</p>
                    <p className="info-card-meta">
                      {article.article_start} to {article.article_end}
                    </p>
                  </article>
                ))}
              </div>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
export default Dashboard;
