import React from "react";
import "./Dashboard.css";

function Dashboard() {
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
        {/* Top header */}
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
          {/* SECTION 1: Profile layout */}
          <section className="profile-section">
            <div className="profile-avatar-wrapper">
              <div className="profile-avatar">
                {/* You can replace this with an <img /> later */}
                <span className="profile-initials">JS</span>
              </div>
            </div>

            <div className="profile-text">
              <h2 className="profile-name">Demo User</h2>
              <p className="profile-title">Community Program Participant</p>
              <p className="profile-description">
                This area can be used to briefly describe the user, their role,
                or the purpose of this dashboard. Later, we can populate this with
                dynamic data from your API.
              </p>
            </div>
          </section>

          {/* SECTION 2: Info cards grid */}
          <section className="info-section">
            <h2 className="info-section-title">Key Information</h2>

            <div className="info-grid">
              {/* Card 1 */}
              <article className="info-card">
                <h3 className="info-card-title">Program Status</h3>
                <p className="info-card-body">
                  Currently enrolled in the Spring 2025 cohort with 3 sessions
                  completed and 2 upcoming.
                </p>
                <p className="info-card-meta">Last updated: Today</p>
              </article>

              {/* Card 2 */}
              <article className="info-card">
                <h3 className="info-card-title">Location Details</h3>
                <p className="info-card-body">
                  Based in New York, NY (10001). This information can later be
                  synced from your profile or submission data.
                </p>
                <p className="info-card-meta">Source: Profile form</p>
              </article>

              {/* Card 3 */}
              <article className="info-card">
                <h3 className="info-card-title">Recent Activity</h3>
                <p className="info-card-body">
                  Submitted an intake form, updated contact details, and viewed
                  the resource library this week.
                </p>
                <p className="info-card-meta">Activity window: Last 7 days</p>
              </article>

              {/* Card 4 */}
              <article className="info-card">
                <h3 className="info-card-title">Support Contact</h3>
                <p className="info-card-body">
                  Assigned to Case Manager: Jordan Lee. Contact via email or
                  in-app messaging for assistance.
                </p>
                <p className="info-card-meta">Response time: ~24 hours</p>
              </article>

              {/* Card 5 */}
              <article className="info-card">
                <h3 className="info-card-title">Upcoming Milestones</h3>
                <p className="info-card-body">
                  Orientation follow-up, mid-program check-in, and final
                  reflection survey are scheduled.
                </p>
                <p className="info-card-meta">Next milestone: In 5 days</p>
              </article>

              {/* Card 6 */}
              <article className="info-card">
                <h3 className="info-card-title">Resources Access</h3>
                <p className="info-card-body">
                  Access granted to learning modules, downloadable guides, and
                  community events calendar.
                </p>
                <p className="info-card-meta">Access level: Standard</p>
              </article>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
