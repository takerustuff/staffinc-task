from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from analyzer import CandidateInput, analyze

app = FastAPI(title="Interview Insights API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten to your S3/CloudFront URL in production
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    name: str
    role: str
    internal_score: float = Field(..., ge=0, le=10)
    technical_score: float = Field(..., ge=0, le=10)
    communication_score: float = Field(..., ge=0, le=10)
    confidence_score: float = Field(..., ge=0, le=10)
    cultural_fit_score: float = Field(..., ge=0, le=10)
    recruiter_notes: str
    client_feedback: str
    years_experience: int = Field(..., ge=0)
    previous_client_rejections: int = Field(0, ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_candidate(req: AnalyzeRequest):
    candidate = CandidateInput(**req.model_dump())
    result = analyze(candidate)
    return {
        "risk_level": result.risk_level,
        "risk_score": result.risk_score,
        "identified_issues": result.identified_issues,
        "recommendations": result.recommendations,
        "summary": result.summary,
        "score_breakdown": result.score_breakdown,
    }
