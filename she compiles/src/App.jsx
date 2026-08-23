import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const examples = {
  scam: "Urgent! Apply now, no interview required, just pay a registration fee and contact us on WhatsApp",
  safe: "We are excited to offer a Software Engineering Internship. Please visit our website www.example.com to apply. Interviews will be conducted next week.",
};

function getRiskType(result) {
  const value = String(result?.riskLevel || "").toLowerCase();

  if (value.includes("high")) return "high";
  if (value.includes("medium") || value.includes("suspicious")) return "medium";

  return "safe";
}

function getScore(result, riskType) {
  const score = Number(result?.score);

  if (!Number.isNaN(score)) {
    return Math.min(100, Math.max(0, score));
  }

  if (riskType === "high") return 90;
  if (riskType === "medium") return 55;

  return 12;
}

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function checkMessage(event) {
    event.preventDefault();

    if (!message.trim()) {
      setError("Paste a message before analyzing it.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/check-posting`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          jobText: message,
        }),
      });

      if (!response.ok) {
        let errorMessage = `Server returned ${response.status}`;

        try {
          const errorData = await response.json();

          if (errorData?.detail) {
            errorMessage =
              typeof errorData.detail === "string"
                ? errorData.detail
                : JSON.stringify(errorData.detail);
          }
        } catch {
          // Use the default error message.
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();
      setResult(data);
    } catch (requestError) {
      console.error(requestError);

      setError(
        requestError.message ||
          "We could not connect to the scanner. Make sure the backend is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  function loadExample(example) {
    setMessage(example);
    setResult(null);
    setError("");
  }

  function clearScanner() {
    setMessage("");
    setResult(null);
    setError("");
  }

  const riskType = result ? getRiskType(result) : null;
  const score = result ? getScore(result, riskType) : null;
  const reasons = result?.flaggedReasons || [];

  const riskContent = {
    high: {
      label: "High Risk",
      title: "This message looks suspicious",
      description:
        "Several common recruitment-scam signals were detected. Do not send money or personal documents.",
      icon: "!",
      secondaryText: "Strong indicators of possible fraud",
    },
    medium: {
      label: "Suspicious",
      title: "Proceed with caution",
      description:
        "This message contains signals that should be verified before you respond.",
      icon: "!",
      secondaryText: "Verification is recommended",
    },
    safe: {
      label: "Low Risk",
      title: "No major warning signs detected",
      description:
        "The message appears relatively safe, but always verify the sender independently.",
      icon: "✓",
      secondaryText: "Few warning signals detected",
    },
  };

  const currentRisk = riskType ? riskContent[riskType] : null;

  return (
    <main className="app-shell">
      <div className="background-orb orb-one" />
      <div className="background-orb orb-two" />

      <nav className="topbar">
        <div className="brand">
          <div className="brand-mark">✓</div>
          <span>ScamCheck</span>
        </div>

        <span className="status-pill">
          <span className="status-dot" />
          Scam detection tool
        </span>
      </nav>

      <section className="hero">
        <p className="eyebrow">JOB MESSAGE SECURITY</p>

        <h1>Know before you trust.</h1>

        <p className="hero-text">
          Paste a job or recruitment message below. ScamCheck looks for
          pressure tactics, payment requests, and other warning signs.
        </p>
      </section>

      <section className="scanner-card">
        <div className="card-heading">
          <div>
            <p className="section-label">MESSAGE SCANNER</p>
            <h2>What did they send you?</h2>
          </div>

          <span className="step-count">01 / 01</span>
        </div>

        <form onSubmit={checkMessage}>
          <textarea
            value={message}
            onChange={(event) => {
              setMessage(event.target.value);
              setError("");
            }}
            placeholder="Paste the job offer, email, or WhatsApp message here..."
            maxLength={5000}
            aria-label="Message to scan"
          />

          <div className="input-footer">
            <span>{message.length} / 5000 characters</span>

            {message && (
              <button
                type="button"
                className="clear-link"
                onClick={clearScanner}
              >
                Clear
              </button>
            )}
          </div>

          <button className="scan-button" type="submit" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner" />
                Analyzing message...
              </>
            ) : (
              <>
                Analyze message
                <span className="button-arrow">→</span>
              </>
            )}
          </button>
        </form>

        <div className="examples">
          <span>Try an example:</span>

          <button type="button" onClick={() => loadExample(examples.scam)}>
            Suspicious message
          </button>

          <button type="button" onClick={() => loadExample(examples.safe)}>
            Safe message
          </button>
        </div>
      </section>

      {error && (
        <section className="error-card" role="alert">
          <span className="error-icon">!</span>

          <div>
            <strong>Something went wrong</strong>
            <p>{error}</p>
          </div>
        </section>
      )}

      {loading && (
        <section className="loading-card">
          <div className="loading-icon">
            <span className="spinner large" />
          </div>

          <div>
            <p className="section-label">SCANNING</p>
            <h2>Checking for warning signs...</h2>
            <p>
              Reviewing language, urgency, payment requests, and contact
              details.
            </p>
          </div>
        </section>
      )}

      {result && !loading && currentRisk && (
        <section className={`result-card ${riskType}`}>
          <div className="result-top">
            <div>
              <p className="section-label">SCAN COMPLETE</p>
              <h2>{currentRisk.title}</h2>

              <p className="result-description">
                {currentRisk.description}
              </p>
            </div>

            <div
              className="score-ring"
              style={{ "--score": `${score * 3.6}deg` }}
              aria-label={`Risk score ${score} out of 100`}
            >
              <div className="score-inner">
                <span>{score}</span>
                <small>/ 100</small>
              </div>
            </div>
          </div>

          <div className="risk-banner">
            <span className="risk-icon">{currentRisk.icon}</span>

            <div>
              <strong>{currentRisk.label}</strong>
              <span>{currentRisk.secondaryText}</span>
            </div>
          </div>

          {reasons.length > 0 && (
            <div className="findings">
              <p className="section-label">DETECTED WARNING SIGNS</p>

              <div className="finding-list">
                {reasons.map((reason, index) => (
                  <div className="finding" key={`${reason}-${index}`}>
                    <span className="finding-icon">
                      {riskType === "safe" ? "✓" : "×"}
                    </span>

                    <span>{String(reason)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="recommendation">
            <p className="section-label">RECOMMENDATION</p>

            <p>
              {riskType === "high"
                ? "Do not pay money, click unknown links, or share identity documents. Verify the employer through an official website."
                : riskType === "medium"
                  ? "Research the company, verify the sender, and avoid sharing sensitive information until the offer is confirmed."
                  : "Check the sender's email address and verify the organization independently before proceeding."}
            </p>
          </div>

          <p className="disclaimer">
            ScamCheck estimates risk based on message patterns. It cannot
            guarantee that a message is legitimate or fraudulent.
          </p>

          <button
            type="button"
            className="scan-again-button"
            onClick={clearScanner}
          >
            Analyze another message
          </button>
        </section>
      )}

      <footer className="footer">
        <span>ScamCheck</span>
        <span>Verify independently. Stay protected.</span>
      </footer>
    </main>
  );
}

export default App;