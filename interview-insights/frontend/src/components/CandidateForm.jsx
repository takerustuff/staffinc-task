import React from "react";
import ScoreSlider from "./ScoreSlider";
import styles from "./CandidateForm.module.css";

const SCORES = [
  { field: "internal_score", label: "Internal Score", hint: "Your agency's overall rating" },
  { field: "technical_score", label: "Technical Score", hint: "Role-specific technical ability" },
  { field: "communication_score", label: "Communication Score", hint: "Clarity and articulation" },
  { field: "confidence_score", label: "Confidence Score", hint: "Presence and self-assurance" },
  { field: "cultural_fit_score", label: "Cultural Fit Score", hint: "Alignment with client culture" },
];

export default function CandidateForm({ form, onChange, onSubmit, loading, error }) {
  return (
    <form className={styles.form} onSubmit={onSubmit} noValidate>
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Candidate Details</h2>
        <div className={styles.row}>
          <div className={styles.field}>
            <label htmlFor="name">Candidate Name</label>
            <input
              id="name"
              type="text"
              value={form.name}
              onChange={(e) => onChange("name", e.target.value)}
              placeholder="e.g. Alex Johnson"
              required
            />
          </div>
          <div className={styles.field}>
            <label htmlFor="role">Role Applied For</label>
            <input
              id="role"
              type="text"
              value={form.role}
              onChange={(e) => onChange("role", e.target.value)}
              placeholder="e.g. Senior Software Engineer"
              required
            />
          </div>
        </div>
        <div className={styles.row}>
          <div className={styles.field}>
            <label htmlFor="years_experience">Years of Experience</label>
            <input
              id="years_experience"
              type="number"
              min={0}
              max={40}
              value={form.years_experience}
              onChange={(e) => onChange("years_experience", parseInt(e.target.value) || 0)}
            />
          </div>
          <div className={styles.field}>
            <label htmlFor="previous_client_rejections">Prior Client Rejections</label>
            <input
              id="previous_client_rejections"
              type="number"
              min={0}
              max={20}
              value={form.previous_client_rejections}
              onChange={(e) => onChange("previous_client_rejections", parseInt(e.target.value) || 0)}
            />
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Scores (0 – 10)</h2>
        <div className={styles.sliders}>
          {SCORES.map(({ field, label, hint }) => (
            <ScoreSlider
              key={field}
              label={label}
              hint={hint}
              value={form[field]}
              onChange={(v) => onChange(field, v)}
            />
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Qualitative Feedback</h2>
        <div className={styles.field}>
          <label htmlFor="recruiter_notes">Recruiter Notes</label>
          <textarea
            id="recruiter_notes"
            rows={4}
            value={form.recruiter_notes}
            onChange={(e) => onChange("recruiter_notes", e.target.value)}
            placeholder="Your observations about the candidate before the client interview..."
          />
        </div>
        <div className={styles.field}>
          <label htmlFor="client_feedback">Client Feedback</label>
          <textarea
            id="client_feedback"
            rows={4}
            value={form.client_feedback}
            onChange={(e) => onChange("client_feedback", e.target.value)}
            placeholder="What the client said after the interview (if available)..."
          />
        </div>
      </section>

      {error && <p className={styles.error} role="alert">⚠ {error}</p>}

      <button type="submit" className={styles.submit} disabled={loading || !form.name || !form.role}>
        {loading ? "Analysing…" : "Analyse Candidate →"}
      </button>
    </form>
  );
}
