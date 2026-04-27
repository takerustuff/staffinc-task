import React from "react";
import ScoreBreakdown from "./ScoreBreakdown";
import styles from "./InsightsPanel.module.css";

const RISK_CONFIG = {
  LOW:      { color: "#38a169", bg: "#f0fff4", border: "#9ae6b4", emoji: "✅" },
  MEDIUM:   { color: "#d69e2e", bg: "#fffff0", border: "#faf089", emoji: "⚠️" },
  HIGH:     { color: "#dd6b20", bg: "#fffaf0", border: "#fbd38d", emoji: "🔶" },
  CRITICAL: { color: "#c53030", bg: "#fff5f5", border: "#feb2b2", emoji: "🚨" },
};

export default function InsightsPanel({ result, candidate, onReset }) {
  const cfg = RISK_CONFIG[result.risk_level] || RISK_CONFIG.MEDIUM;

  return (
    <div className={styles.panel}>
      {/* Risk badge */}
      <div className={styles.riskCard} style={{ background: cfg.bg, borderColor: cfg.border }}>
        <div className={styles.riskLeft}>
          <span className={styles.riskEmoji}>{cfg.emoji}</span>
          <div>
            <p className={styles.riskLabel}>Risk Level</p>
            <p className={styles.riskLevel} style={{ color: cfg.color }}>{result.risk_level}</p>
          </div>
        </div>
        <div className={styles.riskScore}>
          <span className={styles.scoreNum} style={{ color: cfg.color }}>{result.risk_score}</span>
          <span className={styles.scoreMax}>/100</span>
        </div>
      </div>

      {/* Summary */}
      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Summary</h3>
        <p className={styles.summary}>{result.summary}</p>
      </div>

      {/* Score breakdown */}
      <ScoreBreakdown breakdown={result.score_breakdown} />

      {/* Issues */}
      <div className={styles.card}>
        <h3 className={styles.cardTitle}>Identified Issues</h3>
        <ul className={styles.list}>
          {result.identified_issues.map((issue, i) => (
            <li key={i} className={styles.issueItem}>
              <span className={styles.bullet}>⚡</span>
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

      <button className={styles.resetBtn} onClick={onReset}>
        ← Analyse Another Candidate
      </button>
    </div>
  );
}
