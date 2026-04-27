# Interview Insights

A full-stack MVP that helps recruiters understand why candidates fail at the client interview stage and how to improve their chances.

## Architecture

```
Browser → React (S3 static site) → FastAPI (EC2) → Analyzer
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local — set VITE_API_URL=http://localhost:8000
npm install
npm run dev
```

## Deployment

### Backend (EC2)
1. Launch an EC2 instance (Amazon Linux 2 or Ubuntu), open port 8000 in the security group.
2. SCP the `backend/` folder and `infra/deploy-backend.sh` to the instance.
3. Run `./deploy-backend.sh`.

### Frontend (S3)
```bash
export S3_BUCKET=your-bucket-name
export VITE_API_URL=http://<ec2-public-ip>:8000
./infra/deploy-frontend.sh
```

Enable public access on the S3 bucket and attach a bucket policy allowing `s3:GetObject` for `*`.

## How the Analyzer Works

Scores are weighted and combined into a 0–100 risk score:

| Dimension      | Weight |
|----------------|--------|
| Technical      | 30%    |
| Communication  | 25%    |
| Confidence     | 20%    |
| Cultural Fit   | 15%    |
| Internal Score | 10%    |

Repeat client rejections apply a penalty (−5 per rejection, capped at −20).
Free-text fields (recruiter notes + client feedback) are scanned for negative signal keywords to surface issues not captured by scores alone.

Risk levels: **LOW** (75–100) · **MEDIUM** (55–75) · **HIGH** (35–55) · **CRITICAL** (0–35)
