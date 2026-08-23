function ResultCard({ result }) {
  if (!result) return null;

  const colorMap = {
    "Safe": "#2e7d32",
    "Suspicious": "#ed6c02",
    "High Risk": "#d32f2f",
  };

  const riskColor = colorMap[result.riskLevel] || "#555";

  return (
    <div
      style={{
        border: `2px solid ${riskColor}`,
        padding: "1rem 1.25rem",
        marginTop: "1.5rem",
        borderRadius: "10px",
        textAlign: "left",
      }}
    >
      <h3 style={{ color: riskColor, marginTop: 0 }}>
        {result.riskLevel} — Score: {result.score}/100
      </h3>
      {result.flaggedReasons && result.flaggedReasons.length > 0 ? (
        <ul>
          {result.flaggedReasons.map((reason, i) => (
            <li key={i}>{reason}</li>
          ))}
        </ul>
      ) : (
        <p>No red flags detected.</p>
      )}
    </div>
  );
}

export default ResultCard;