import React from "react";
import ScoreBreakdown from "./ScoreBreakdown";
import styles from "./InsightsPanel.module.css";

const RISK_CONFIG = {
  LOW:      { color: "#276749", bg: "#f0fff4", border: "#9ae6b4", barColor: "#38a169" },
  MEDIUM:   { color: "#744210", bg: "#fffbeb", border: "#fcd34d", barColor: "#d69e2e" },
  HIGH:     { color: "#7b341e", bg: "#fff7ed", border: "#fdba74", barColor: "#dd6b20" },
  CRITICAL: { color: "#742a2a", bg: "#fff5f5", border: "#feb2b2", barColor: "#c53030" },
};

export default function InsightsPanel({ result, candidate, onReset }) {
  const cfg = RISK_CONFIG[result.risk_level] || RISK_CONFIG.MEDIUM;

  return (
    <div className={styles.panel}>

      {/* Risk header */}
      <div className={styles.riskCard} style={{ background: cfg.bg, borderColor: cfg.border }}>
        <div className={styles.riskMeta}>
          <span className={styles.modeLabel}>{result.mode_label}</span>
          <span className={styles.riskBadge} style={{ color: cfg.color, borderColor: cfg.border }}>
            {result.risk_level} RISK
          </span>
        </div>
        <div className={styles.riskBody}>
          <p className={styles.riskSummary}>{result.summary}</p>
          <div className={styles.riskScore} style={{ color: cfg.color }}>
            <span className={styles.scoreNum}>{result.risk_score}</span>
            <span className={styles.scoreMax}>/100</span>
          </div>
        </div>
      </div>

      {/* Score breakdown */}
      <ScoreBreakdown breakdown={result.score_breakdown} />

      {/* Issues */}
      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Identified Issues</h3>
        <ul className={styles.issueList}>
          {result.identified_issues.map((issue, i) => (
            <li key={i} className={styles.issueItem}>
              <span className={styles.issueDot} />
              {issue}
            </li>
          ))}
        </ul>
      </div>

      {/* Recommendations */}
      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Recommendations</h3>
        <ol className={styles.recList}>
          {result.recommendations.map((rec, i) => (
            <li key={i} className={styles.recItem}>
              <span className={styles.recNum}>{i + 1}</span>
              <span>{rec}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className={styles.footer}>
        <button className={styles.resetBtn} onClick={onReset}>
          Back to Form
        </button>
      </div>
    </div>
  );
}
