import { useState } from "react";

function App() {
  // Prevent horizontal scroll
  document.body.style.overflowX = "hidden";

  const [role, setRole] = useState("");
  const [skills, setSkills] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runAgent = async () => {
    setLoading(true);
    setError("");
    setJobs([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/run-agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role,
          skills: skills.split(",").map(s => s.trim()),
          location: location.split(",").map(l => l.trim()),
        }),
      });

      if (!res.ok) throw new Error();
      const data = await res.json();
      setJobs(data.matched_jobs || []);
    } catch {
      setError("Backend not reachable");
    }

    setLoading(false);
  };

  const scoreBadge = (score) => {
    if (score >= 0.55) return ["High Match", "#22c55e"];
    if (score >= 0.4) return ["Good Match", "#38bdf8"];
    return ["Low Match", "#f87171"];
  };

  return (
    <div style={page}>
      <div style={container}>
        {/* HEADER */}
        <h1 style={title}>🤖 AI Job Agent</h1>
        <p style={subtitle}>
          Find high-match jobs automatically using Agentic AI
        </p>

        {/* INPUT CARD */}
        <div style={card}>
          <input
            style={input}
            placeholder="Role (e.g. Data Analyst)"
            value={role}
            onChange={e => setRole(e.target.value)}
          />

          <input
            style={input}
            placeholder="Skills (SQL, Python, Excel)"
            value={skills}
            onChange={e => setSkills(e.target.value)}
          />

          <input
            style={input}
            placeholder="Location (Bangalore, Remote)"
            value={location}
            onChange={e => setLocation(e.target.value)}
          />

          <button style={button} onClick={runAgent} disabled={loading}>
            {loading ? "Searching jobs..." : "Find Jobs"}
          </button>

          {error && <p style={{ color: "#ef4444" }}>{error}</p>}
        </div>

        {/* RESULTS */}
        <div style={{ marginTop: 50 }}>
          {jobs.map((job, i) => {
            const [label, color] = scoreBadge(job.score);

            return (
              <div key={i} style={card}>
                <div style={row}>
                  <h3 style={{ fontSize: 22 }}>{job.title}</h3>
                  <span style={{ ...badge, background: color }}>
                    {label}
                  </span>
                </div>

                <p><b>Company:</b> {job.company}</p>
                <p><b>Location:</b> {job.location}</p>

                <p style={{ color: "#0f172a", marginTop: 10 }}>
                  {job.description}
                </p>

                <p style={{ marginTop: 8 }}>
                  <b>Match Score:</b> {job.score}
                </p>

                {job.apply_link ? (
                  <a
                    href={job.apply_link}
                    target="_blank"
                    rel="noreferrer"
                    style={applyBtn}
                  >
                    Apply Now →
                  </a>
                ) : (
                  <p style={{ color: "#475569" }}>
                    Apply link not available
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ================= STYLES ================= */

const page = {
  minHeight: "100vh",
  width: "100vw",
  display: "flex",
  justifyContent: "center",
  alignItems: "flex-start",
  background: "linear-gradient(135deg, #e0f2fe, #bae6fd, #7dd3fc)",
  padding: "60px 24px",
};

const container = {
  width: "100%",
  maxWidth: "1200px", // 👈 bigger screen feel
};

const title = {
  textAlign: "center",
  fontSize: "clamp(34px, 6vw, 48px)",
  fontWeight: 800,
  color: "#0f172a",
};

const subtitle = {
  textAlign: "center",
  color: "#334155",
  marginBottom: 40,
  fontSize: 18,
};

const card = {
  background: "rgba(255,255,255,0.85)",
  backdropFilter: "blur(12px)",
  borderRadius: 18,
  padding: 28,
  marginBottom: 24,
  boxShadow: "0 20px 45px rgba(15,23,42,0.15)",
};

const input = {
  width: "100%",
  padding: 16,
  marginBottom: 14,
  borderRadius: 12,
  border: "1px solid #cbd5f5",
  fontSize: 16,
  outline: "none",
};

const button = {
  width: "100%",
  padding: 16,
  borderRadius: 14,
  background: "linear-gradient(90deg, #38bdf8, #6366f1)",
  color: "#fff",
  fontWeight: "bold",
  fontSize: 16,
  border: "none",
  cursor: "pointer",
};

const row = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: 8,
};

const badge = {
  padding: "6px 16px",
  borderRadius: 999,
  fontSize: 12,
  color: "#020617",
  fontWeight: "bold",
};

const applyBtn = {
  display: "inline-block",
  marginTop: 14,
  padding: "12px 20px",
  background: "linear-gradient(90deg, #22c55e, #4ade80)",
  color: "#022c22",
  borderRadius: 12,
  textDecoration: "none",
  fontWeight: "bold",
};

export default App;
