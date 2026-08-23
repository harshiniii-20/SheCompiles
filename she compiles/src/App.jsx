import { useState } from "react";
import ScamCheckForm from "./components/ScamCheckForm";
import ResultCard from "./components/ResultCard";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <h1>🛡️ ScamCheck</h1>
      <p>Paste a job/internship posting to check its scam risk.</p>
      <ScamCheckForm onResult={setResult} />
      <ResultCard result={result} />
    </div>
  );
}

export default App;