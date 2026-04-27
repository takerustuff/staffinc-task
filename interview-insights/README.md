# Interview Insights

> This MVP addresses the low candidate-to-client conversion rate in recruitment by identifying gaps between internal evaluation and client expectations. It analyzes candidate scores and qualitative feedback, adjusts scoring weights based on client context (Corporate, Startup, Consulting), and delivers actionable coaching recommendations to improve interview success rates. In the future, this can be enhanced with NLP models trained on historical rejection data to improve prediction accuracy.

---

## The Problem

Candidates pass internal screening but fail at the client interview stage. The reasons are usually the same — poor communication, lack of confidence, cultural mismatch, underprepared — but they are rarely caught early because internal evaluations are inconsistent and unstructured.

## The Solution

A structured analysis tool that:
- Scores candidates across 5 dimensions with client-type-adjusted weights
- Scans recruiter notes and client feedback for negative signal keywords
- Supports Pre-Interview (predict risk) and Post-Interview (explain failure) modes
- Returns a risk level, identified issues, and tailored coaching recommendations

---

## Architecture

```
Browser → React (Vercel) → FastAPI (Render) → Analyzer
```

## Stack

- Frontend: React 18 + Vite
- Backend: Python FastAPI + Pydantic
- Hosting: Vercel (frontend) + Render (backend)

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
# Set VITE_API_URL=http://localhost:8000 in .env.local
npm install
npm run dev
# http://localhost:5173
```

---

## Deployment

### Backend (Render)
- Root Directory: `interview-insights/backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
- Root Directory: `interview-insights/frontend`
- Env variable: `VITE_API_URL` = your Render URL
- Auto-deploys on push to `main`

---

## How the Analyzer Works

Scores are weighted by client type:

| Dimension      | Corporate | Startup | Consulting |
|----------------|-----------|---------|------------|
| Technical      | 25%       | 25%     | 30%        |
| Communication  | 30%       | 20%     | 30%        |
| Confidence     | 25%       | 25%     | 20%        |
| Cultural Fit   | 10%       | 20%     | 10%        |
| Internal Score | 10%       | 10%     | 10%        |

Prior client rejections apply a score penalty (−5 each, max −20).
Free-text fields are scanned for negative signal keywords across 5 categories: communication, confidence, technical, cultural fit, and preparation.

Risk levels: **LOW** (75–100) · **MEDIUM** (55–74) · **HIGH** (35–54) · **CRITICAL** (0–34)
