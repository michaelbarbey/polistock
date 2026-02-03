import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Dashboard.css";

function formatDateForDisplay(dateStr) {
  if (!dateStr) return "N/A";

  // date conversion
  try {
    if (dateStr.includes("-")) {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    }

    if (dateStr.length === 4) {
      return dateStr;
    }

    if (dateStr.length === 8) {
      const year = dateStr.substring(0, 4);
      const month = dateStr.substring(4, 6);
      const day = dateStr.substring(6, 8);
      const date = new Date(year, month - 1, day);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    }

    return dateStr;
  } catch (error) {
    console.error("Error formatting date:", dateStr, error);
    return dateStr;
  }
}

function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const official = location.state?.official;
  const [navbarHidden, setNavbarHidden] = useState(false);
  const [prevScrollPos, setPrevScrollPos] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollPos = window.pageYOffset;

      // shows navbar at the top of page
      if (currentScrollPos === 0) {
        setNavbarHidden(false);
        setPrevScrollPos(currentScrollPos);
        return;
      }

      // shows navbar when scrolling up, hides when scrolling down
      if (prevScrollPos > currentScrollPos) {
        setNavbarHidden(false);
      } else {
        setNavbarHidden(true);
      }
      setPrevScrollPos(currentScrollPos);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [prevScrollPos]);

  if (!official) {
    return (
      <div className="dashboard-no-data">
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
  // const articles = official.articles || [];

  // Somewhere near the top of your component where you get articles
  const articles = official.articles || [];
  console.log("First article data:", articles[0]);

  return (
    <div className="dashboard">
      {/* Top Navbar */}
      <nav
        className={`dashboard-navbar ${navbarHidden ? "hidden" : ""}`}
        style={{
          backgroundColor: official.party?.toLowerCase().includes("democratic")
            ? "#002147"
            : official.party?.toLowerCase().includes("republican")
              ? "#BB133E"
              : "var(--bg-card)",
        }}
      >
        <div className="navbar-container">
          <div className="navbar-left">
            <div className="navbar-logo">
              <img
                src="/logo.jpeg"
                alt="polidemos logo"
                style={{
                  height: "30px",
                  marginRight: "8px",
                  borderRadius: "8px",
                }}
              />
              <span className="logo-text">polidemos</span>
            </div>

            <div className="navbar-title">
              <h1
                style={{
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
          </div>
          <div className="navbar-actions">
            {/* <button
              className="outline-btn"
              style={{
                color:
                  official.party?.toLowerCase().includes("democratic") ||
                  official.party?.toLowerCase().includes("republican")
                    ? "#FFFFFF"
                    : "var(--text-primary)",
                borderColor:
                  official.party?.toLowerCase().includes("democratic") ||
                  official.party?.toLowerCase().includes("republican")
                    ? "rgba(255, 255, 255, 0.5)"
                    : "var(--border-color)",
              }}
            >
              Export Data
            </button> */}
            <button
              className="primary-btn"
              onClick={() => navigate("/")}
              style={{
                backgroundColor:
                  official.party?.toLowerCase().includes("democratic") ||
                  official.party?.toLowerCase().includes("republican")
                    ? "#ffffff"
                    : "var(--accent)",
                color: official.party?.toLowerCase().includes("democratic")
                  ? "#002147"
                  : official.party?.toLowerCase().includes("republican")
                    ? "#FF3A2F"
                    : "#ffffff",
              }}
            >
              New Search
            </button>
          </div>
        </div>
      </nav>

      {/* Main content */}
      <div className="dashboard-main">
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
                      objectFit: "scale-down",
                      borderWidth: "10px",
                      backgroundColor: official.party
                        ?.toLowerCase()
                        .includes("democratic")
                        ? "#2254B5"
                        : official.party?.toLowerCase().includes("republican")
                          ? "#952224"
                          : "var(--bg-card)",
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
              <h2>
                <a
                  href={official.contact?.website}
                  className="profile-name"
                  style={{
                    color:
                      official.party?.toLowerCase().includes("democratic") ||
                      official.party?.toLowerCase().includes("republican")
                        ? "var(--text-primary)"
                        : "var(--text-primary)",
                    // to include in next update: adjust hover color
                    onHover: official.party
                      ?.toLowerCase()
                      .includes("democratic")
                      ? "#002147"
                      : official.party?.toLowerCase().includes("republican")
                        ? "#BB133E"
                        : "var(--bg-card)",
                  }}
                >
                  {official.fullname}
                </a>
              </h2>
              <p className="profile-title">
                {official.party} • {official.chamber}
              </p>
              <p className="profile-description">
                Representing {district?.city}, {district?.state_name} (District{" "}
                {district?.district_code})
                <br />
                Term: {formatDateForDisplay(official.term_start)} to{" "}
                {formatDateForDisplay(official.term_end)}
                <br />
                Bioguide ID: {official.bioguide_id}
                <br />
                Phone Number: {official.contact?.phone_number || "N/A"}
                <br />
                Office Address: {official.contact?.office_address || "N/A"}
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

          {/* News Articles Section */}
          {articles.length > 0 && (
            <section className="info-section articles-section">
              <h2 className="info-section-title">Related News</h2>
              {/* desktop: grid of full-width image cards */}
              <div className="articles-grid desktop-only">
                {articles.map((article, index) => (
                  <a
                    key={index}
                    href={article.article_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="article-card-full"
                    onClick={(e) => {
                      console.log("Article clicked:", article.article_link);
                    }}
                    style={{
                      backgroundImage: article.article_image
                        ? `linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url(${article.article_image})`
                        : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    }}
                  >
                    <div className="article-overlay">
                      <h3 className="article-headline">{article.headline}</h3>
                      <p className="article-author">{article.author}</p>
                      <span className="article-read-more">Read Article →</span>
                    </div>
                  </a>
                ))}
              </div>

              {/* Mobile: Carousel */}
              <div className="articles-carousel mobile-only">
                <div className="carousel-container">
                  {articles.map((article, index) => (
                    <a
                      key={index}
                      href={article.article_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="article-card-mobile"
                      onClick={(e) => {
                        console.log("Article clicked:", article.article_link);
                      }}
                    >
                      {article.article_image && (
                        <div
                          className="article-image-mobile"
                          style={{
                            backgroundImage: `url(${article.article_image})`,
                          }}
                        />
                      )}
                      <div className="article-content-mobile">
                        <h3 className="article-headline-mobile">
                          {article.headline}
                        </h3>
                        <p className="article-snippet-mobile">
                          {article.article_short}
                        </p>
                        <div className="article-meta-mobile">
                          <span className="article-author-mobile">
                            {article.author}
                            <br></br>
                            <span className="article-date-mobile">
                              {formatDateForDisplay(article.article_start)}
                            </span>
                          </span>
                        </div>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
