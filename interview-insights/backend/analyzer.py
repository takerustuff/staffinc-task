"""
Rule-based + weighted scoring analyzer.
Identifies failure patterns and generates actionable recommendations.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CandidateInput:
    name: str
    role: str
    internal_score: float          # 0-10
    technical_score: float         # 0-10
    communication_score: float     # 0-10
    confidence_score: float        # 0-10
    cultural_fit_score: float      # 0-10
    recruiter_notes: str
    client_feedback: str
    years_experience: int
    previous_client_rejections: int = 0


@dataclass
class InsightResult:
    risk_level: str                # LOW / MEDIUM / HIGH / CRITICAL
    risk_score: float              # 0-100
    identified_issues: list[str]
    recommendations: list[str]
    summary: str
    score_breakdown: dict


# Thresholds
SCORE_WEIGHTS = {
    "technical": 0.30,
    "communication": 0.25,
    "confidence": 0.20,
    "cultural_fit": 0.15,
    "internal": 0.10,
}

RISK_THRESHOLDS = {
    "LOW": (75, 100),
    "MEDIUM": (55, 75),
    "HIGH": (35, 55),
    "CRITICAL": (0, 35),
}

# Keywords that signal issues in free-text fields
NEGATIVE_SIGNALS = {
    "communication": ["unclear", "struggled to articulate", "verbose", "rambling",
                      "hard to follow", "poor communication", "didn't explain",
                      "confusing", "inarticulate"],
    "confidence": ["nervous", "hesitant", "unsure", "lacked confidence", "timid",
                   "uncertain", "second-guessed", "apologetic", "passive"],
    "technical": ["wrong answer", "couldn't solve", "failed technical", "no knowledge",
                  "outdated skills", "gaps in knowledge", "struggled with", "incorrect"],
    "cultural_fit": ["not a fit", "attitude", "arrogant", "dismissive", "poor attitude",
                     "unprofessional", "rude", "disengaged"],
    "preparation": ["unprepared", "didn't research", "no knowledge of company",
                    "hadn't read", "unaware of", "not familiar with"],
}


def _detect_text_issues(text: str) -> dict[str, list[str]]:
    """Scan free-text for negative signal keywords."""
    text_lower = text.lower()
    found: dict[str, list[str]] = {}
    for category, signals in NEGATIVE_SIGNALS.items():
        hits = [s for s in signals if s in text_lower]
        if hits:
            found[category] = hits
    return found


def _compute_weighted_score(candidate: CandidateInput) -> float:
    raw = (
        candidate.technical_score * SCORE_WEIGHTS["technical"] +
        candidate.communication_score * SCORE_WEIGHTS["communication"] +
        candidate.confidence_score * SCORE_WEIGHTS["confidence"] +
        candidate.cultural_fit_score * SCORE_WEIGHTS["cultural_fit"] +
        candidate.internal_score * SCORE_WEIGHTS["internal"]
    )
    # Normalise from 0-10 scale to 0-100
    return round(raw * 10, 1)


def _get_risk_level(score: float) -> str:
    for level, (low, high) in RISK_THRESHOLDS.items():
        if low <= score < high:
            return level
    return "CRITICAL"


def analyze(candidate: CandidateInput) -> InsightResult:
    weighted_score = _compute_weighted_score(candidate)

    # Penalise repeat rejections
    rejection_penalty = min(candidate.previous_client_rejections * 5, 20)
    adjusted_score = max(0, weighted_score - rejection_penalty)

    risk_level = _get_risk_level(adjusted_score)

    issues: list[str] = []
    recommendations: list[str] = []

    # --- Score-based issues ---
    if candidate.communication_score < 6:
        issues.append("Below-average communication score")
        recommendations.append(
            "Schedule mock client interviews focusing on structured storytelling (STAR method)."
        )

    if candidate.confidence_score < 6:
        issues.append("Low confidence indicators in scoring")
        recommendations.append(
            "Run confidence-building sessions; coach candidate to pause and think before answering rather than rushing."
        )

    if candidate.technical_score < 6:
        issues.append("Technical competency gaps identified")
        recommendations.append(
            "Provide targeted study materials for the role's core technical requirements and re-assess before next submission."
        )

    if candidate.cultural_fit_score < 6:
        issues.append("Cultural fit concerns flagged")
        recommendations.append(
            "Brief the candidate on the client's values and working style; review any attitude red flags with them directly."
        )

    if candidate.years_experience < 3 and candidate.technical_score < 7:
        issues.append("Limited experience combined with technical gaps increases risk")
        recommendations.append(
            "Consider whether this role is the right level; explore junior or associate positions with this client."
        )

    # --- Text-based issues ---
    combined_text = f"{candidate.recruiter_notes} {candidate.client_feedback}"
    text_issues = _detect_text_issues(combined_text)

    if "communication" in text_issues:
        if "Below-average communication score" not in issues:
            issues.append("Communication issues mentioned in feedback text")
            recommendations.append(
                "Client feedback highlights communication problems — prioritise presentation coaching."
            )

    if "confidence" in text_issues:
        if "Low confidence indicators in scoring" not in issues:
            issues.append("Confidence issues detected in feedback text")
            recommendations.append(
                "Address confidence signals noted by the client; consider a practice run with a senior recruiter acting as the client."
            )

    if "preparation" in text_issues:
        issues.append("Candidate appeared underprepared for the client interview")
        recommendations.append(
            "Implement a mandatory pre-interview briefing pack covering the client's business, recent news, and role expectations."
        )

    if "technical" in text_issues:
        if "Technical competency gaps identified" not in issues:
            issues.append("Technical shortcomings noted in client feedback")
            recommendations.append(
                "Review the specific technical areas flagged and arrange upskilling before resubmission."
            )

    if "cultural_fit" in text_issues:
        if "Cultural fit concerns flagged" not in issues:
            issues.append("Cultural or attitude concerns in client feedback")
            recommendations.append(
                "Have a candid conversation with the candidate about professionalism and client expectations."
            )

    if candidate.previous_client_rejections >= 2:
        issues.append(f"Candidate has {candidate.previous_client_rejections} prior client rejections")
        recommendations.append(
            "Conduct a structured debrief covering all previous rejections to identify a recurring pattern before any further submissions."
        )

    if not issues:
        issues.append("No major issues detected")
        recommendations.append(
            "Candidate profile looks strong. Ensure thorough client briefing and confirm logistics ahead of the interview."
        )

    # Build summary
    summary = _build_summary(candidate, risk_level, adjusted_score, issues)

    score_breakdown = {
        "technical": candidate.technical_score,
        "communication": candidate.communication_score,
        "confidence": candidate.confidence_score,
        "cultural_fit": candidate.cultural_fit_score,
        "internal": candidate.internal_score,
        "weighted_total": weighted_score,
        "rejection_penalty": rejection_penalty,
        "final_score": adjusted_score,
    }

    return InsightResult(
        risk_level=risk_level,
        risk_score=adjusted_score,
        identified_issues=issues,
        recommendations=recommendations,
        summary=summary,
        score_breakdown=score_breakdown,
    )


def _build_summary(candidate: CandidateInput, risk_level: str, score: float, issues: list[str]) -> str:
    level_desc = {
        "LOW": "a strong candidate with minor areas to watch",
        "MEDIUM": "a moderate-risk candidate who needs targeted coaching",
        "HIGH": "a high-risk submission requiring significant preparation",
        "CRITICAL": "a critical-risk candidate who should not be submitted without substantial remediation",
    }
    desc = level_desc.get(risk_level, "an unclassified risk profile")
    issue_count = len([i for i in issues if i != "No major issues detected"])
    return (
        f"{candidate.name} applying for {candidate.role} is {desc} "
        f"(risk score: {score}/100). "
        f"{issue_count} issue{'s' if issue_count != 1 else ''} identified across their profile."
    )
