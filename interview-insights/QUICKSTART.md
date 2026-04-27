# Quick Start Guide

## Step 1: Start Backend

Open PowerShell/Terminal in the project folder:

```powershell
cd interview-insights/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

✅ Backend running at http://localhost:8000

---

## Step 2: Start Frontend

Open a NEW PowerShell/Terminal window:

```powershell
cd interview-insights/frontend
npm install
cp .env.example .env.local
npm run dev
```

✅ Frontend running at http://localhost:5173

Open http://localhost:5173 in your browser!

---

## Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed: `python --version`
- Try `python3` instead of `python`

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again

**Can't connect to backend?**
- Check `.env.local` has `VITE_API_URL=http://localhost:8000`
- Make sure backend is running (check http://localhost:8000/health)
