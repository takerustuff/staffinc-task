import React, { useState } from "react";
import CandidateForm from "./components/CandidateForm";
import InsightsPanel from "./components/InsightsPanel";
import { analyzeCandidate } from "./api";
import styles from "./App.module.css";

const INITIAL_FORM = {
  name: "",
  role: "",
  internal_score: 7,
  technical_score: 7,
  communication_score: 7,
  confidence_score: 7,
  cultural_fit_score: 7,
  recruiter_notes: "",
  client_feedback: "",
  years_experience: 3,
  previous_client_rejections: 0,
  client_type: "corporate",
  interview_mode: "pre",
};

export default function App() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeCandidate(form);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setForm(INITIAL_FORM);
    setResult(null);
    setError(null);
  };

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.logo}>
          Interview <span className={styles.logoAccent}>Insights</span>
        </div>
        <p className={styles.tagline}>
          Candidate readiness analysis for client interviews
        </p>
      </header>

      <main className={styles.main}>
        {!result ? (
          <CandidateForm
            form={form}
            onChange={handleChange}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />
        ) : (
          <InsightsPanel result={result} candidate={form} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}
