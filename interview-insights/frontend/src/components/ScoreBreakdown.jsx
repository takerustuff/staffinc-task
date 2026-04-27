import React from "react";
import styles from "./ScoreBreakdown.module.css";

const LABELS = {
  technical: "Technical",
  communication: "Communication",
  confidence: "Confidence",
  cultural_fit: "Cultural Fit",
  internal: "Internal",
};

function Bar({ label, value }) {
  const pct = (value / 10) * 100;
  const color = value >= 8 ? "#38a169" : value >= 6 ? "#d69e2e" : "#e53e3e";
  return (
    <div className={styles.barRow}>
      <span className={styles.barLabel}>{label}</span>
      <div className={styles.barTrack}>
        <div className={styles.barFill} style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className={styles.barValue} style={{ color }}>{value.toFixed(1)}</span>
    </div>
  );
}

export default function ScoreBreakdown({ breakdown }) {
  return (
    <div className={styles.card}>
      <h3 className={styles.cardTitle}>Score Breakdown</h3>
      <div className={styles.bars}>
        {Object.entries(LABELS).map(([key, label]) => (
          <Bar key={key} label={label} value={breakdown[key]} />
        ))}
      </div>
      <div className={styles.footer}>
        <span>Weighted total: <strong>{breakdown.weighted_total}/100</strong></span>
        {breakdown.rejection_penalty > 0 && (
          <span className={styles.penalty}>
            Rejection penalty: −{breakdown.rejection_penalty}
          </span>
        )}
        <span>Final score: <strong>{breakdown.final_score}/100</strong></span>
      </div>
    </div>
  );
}
