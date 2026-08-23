import { useState } from "react";

function ScamCheckForm({ onResult }) {
  const [jobText, setJobText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/check-posting", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobText }),
      });
      const data = await response.json();
      onResult(data);
    } catch (err) {
      console.error("Error checking posting:", err);
      alert("Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        rows={8}
        placeholder="Paste the job/internship posting text here..."
        value={jobText}
        onChange={(e) => setJobText(e.target.value)}
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Checking..." : "Check for Scam"}
      </button>
    </form>
  );
}

export default ScamCheckForm;