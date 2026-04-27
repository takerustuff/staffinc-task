// Point this at your EC2 instance URL (or localhost for local dev)
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function analyzeCandidate(payload) {
  const res = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Analysis failed");
  }
  return res.json();
}
