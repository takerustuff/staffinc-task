import React from "react";
import styles from "./ScoreSlider.module.css";

function getColor(value) {
  if (value >= 8) return "#38a169";
  if (value >= 6) return "#d69e2e";
  return "#e53e3e";
}

export default function ScoreSlider({ label, hint, value, onChange }) {
  const color = getColor(value);
  return (
    <div className={styles.wrapper}>
      <div className={styles.top}>
        <div>
          <span className={styles.label}>{label}</span>
          {hint && <span className={styles.hint}>{hint}</span>}
        </div>
        <span className={styles.value} style={{ color }}>{value.toFixed(1)}</span>
      </div>
      <input
        type="range"
        min={0}
        max={10}
        step={0.5}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className={styles.slider}
        style={{ "--thumb-color": color }}
        aria-label={label}
      />
      <div className={styles.ticks}>
        <span>0</span><span>5</span><span>10</span>
      </div>
    </div>
  );
}
