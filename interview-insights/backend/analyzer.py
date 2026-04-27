"""
Rule-based + weighted scoring analyzer.
Identifies failure patterns and generates actionable recommendations.

Supports:
- Client Type: Corporate / Startup / Consulting (adjusts score weights)
- Interview Mode: pre (predict risk) / post (explain failure)
"""

from dataclasses import dataclass


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
    client_type: str = "corporate"     # corporate | startup | consulting
    interview_mode: str = "pre"        # pre | post


@dataclass
class InsightResult:
    risk_level: str                # LOW / MEDIUM / HIGH / CRITICAL
    risk_score: float              # 0-100
    identified_issues: list[str]
    recommendations: list[str]
    summary: str
    score_breakdown: dict
    mode_label: str                # "Pre-Interview Risk Prediction" | "Post-Interview Failure Analysis"


# Base weights — overridden per client type
BASE_WEIGHTS = {
    "technical": 0.30,
    "communication": 0.25,
    "confidence": 0.20,
    "cultural_fit": 0.15,
    "internal": 0.10,
}

# Corporate: executive presence + communication matter most
CORPORATE_WEIGHTS = {
    "technical": 0.25,
    "communication": 0.30,
    "confidence": 0.25,
    "cultural_fit": 0.10,
    "internal": 0.10,
}

# Startup: adaptability + scrappiness — confidence and cultural fit weighted higher
STARTUP_WEIGHTS = {
    "technical": 0.25,
    "communication": 0.20,
    "confidence": 0.25,
    "cultural_fit": 0.20,
    "internal": 0.10,
}

# Consulting: communication and technical both critical
CONSULTING_WEIGHTS = {
    "technical": 0.30,
    "communication": 0.30,
    "confidence": 0.20,
    "cultural_fit": 0.10,
    "internal": 0.10,
}

CLIENT_WEIGHTS = {
    "corporate": CORPORATE_WEIGHTS,
    "startup": STARTUP_WEIGHTS,
    "consulting": CONSULTING_WEIGHTS,
}

RISK_THRESHOLDS = {
    "LOW": (75, 101),
    "MEDIUM": (55, 75),
    "HIGH": (35, 55),
    "CRITICAL": (0, 35),
}

# Client-type specific coaching tips
CLIENT_TYPE_TIPS = {
    "corporate": {
        "communication": "For corporate clients, executive presence is critical — coach the candidate on formal communication, structured answers, and boardroom-ready delivery.",
        "confidence": "Corporate clients expect authority and decisiveness. Run mock interviews with a senior stakeholder to build executive presence.",
        "cultural_fit": "Brief the candidate on corporate hierarchy, dress code, and formal meeting etiquette expected by this client.",
    },
    "startup": {
        "communication": "Startup clients value directness and energy. Coach the candidate to be concise, show enthusiasm, and avoid corporate jargon.",
        "confidence": "Startups want self-starters. Coach the candidate to demonstrate initiative and comfort with ambiguity.",
        "cultural_fit": "Brief the candidate on the startup's mission, pace, and flat structure. Scrappiness and adaptability are key selling points.",
    },
    "consulting": {
        "communication": "Consulting clients expect structured, logical communication. Practice case-style answers and the Pyramid Principle.",
        "confidence": "Consulting environments are high-pressure. Run stress interviews to build composure under questioning.",
        "cultural_fit": "Brief the candidate on consulting culture — long hours, client-first mindset, and professional polish are non-negotiable.",
    },
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


def _get_weights(client_type: str) -> dict:
    return CLIENT_WEIGHTS.get(client_type.lower(), BASE_WEIGHTS)


def _compute_weighted_score(candidate: CandidateInput) -> float:
    weights = _get_weights(candidate.client_type)
    raw = (
        candidate.technical_score * weights["technical"] +
        candidate.communication_score * weights["communication"] +
        candidate.confidence_score * weights["confidence"] +
        candidate.cultural_fit_score * weights["cultural_fit"] +
        candidate.internal_score * weights["internal"]
    )
    return round(raw * 10, 1)


def _get_risk_level(score: float) -> str:
    for level, (low, high) in RISK_THRESHOLDS.items():
        if low <= score < high:
            return level
    return "CRITICAL"


def _get_tip(client_type: str, category: str, fallback: str) -> str:
    """Return client-type specific tip if available, else fallback."""
    return CLIENT_TYPE_TIPS.get(client_type.lower(), {}).get(category, fallback)


def analyze(candidate: CandidateInput) -> InsightResult:
    weighted_score = _compute_weighted_score(candidate)
    client_type = candidate.client_type.lower()
    is_post = candidate.interview_mode.lower() == "post"

    mode_label = (
        "Post-Interview Failure Analysis" if is_post
        else "Pre-Interview Risk Prediction"
    )

    # Penalise repeat rejections
    rejection_penalty = min(candidate.previous_client_rejections * 5, 20)
    adjusted_score = max(0, weighted_score - rejection_penalty)
    risk_level = _get_risk_level(adjusted_score)

    issues: list[str] = []
    recommendations: list[str] = []

    # --- Score-based issues (with client-type aware recommendations) ---
    if candidate.communication_score < 6:
        issues.append("Below-average communication score")
        recommendations.append(_get_tip(
            client_type, "communication",
            "Schedule mock client interviews focusing on structured storytelling (STAR method)."
        ))

    if candidate.confidence_score < 6:
        issues.append("Low confidence indicators in scoring")
        recommendations.append(_get_tip(
            client_type, "confidence",
            "Run confidence-building sessions; coach candidate to pause and think before answering rather than rushing."
        ))

    if candidate.technical_score < 6:
        issues.append("Technical competency gaps identified")
        recommendations.append(
            "Provide targeted study materials for the role's core technical requirements and re-assess before next submission."
        )

    if candidate.cultural_fit_score < 6:
        issues.append("Cultural fit concerns flagged")
        recommendations.append(_get_tip(
            client_type, "cultural_fit",
            "Brief the candidate on the client's values and working style; review any attitude red flags with them directly."
        ))

    if candidate.years_experience < 3 and candidate.technical_score < 7:
        issues.append("Limited experience combined with technical gaps increases risk")
        recommendations.append(
            "Consider whether this role is the right level; explore junior or associate positions with this client."
        )

    # --- Startup-specific check ---
    if client_type == "startup" and candidate.cultural_fit_score < 7:
        if "Cultural fit concerns flagged" not in issues:
            issues.append("Cultural fit below startup threshold (startups require higher adaptability)")
            recommendations.append(
                "Startup clients need candidates who thrive in fast-paced, ambiguous environments. "
                "Assess whether the candidate has demonstrated adaptability and self-direction in past roles."
            )

    # --- Corporate-specific check ---
    if client_type == "corporate" and candidate.communication_score < 7:
        if "Below-average communication score" not in issues:
            issues.append("Communication below corporate client threshold (executive presence required)")
            recommendations.append(
                "Corporate clients expect polished, boardroom-ready communication. "
                "Consider additional presentation coaching before submission."
            )

    # --- Text-based issues ---
    # In pre mode: scan recruiter notes only. In post mode: scan both.
    if is_post:
        scan_text = f"{candidate.recruiter_notes} {candidate.client_feedback}"
    else:
        scan_text = candidate.recruiter_notes

    text_issues = _detect_text_issues(scan_text)

    if "communication" in text_issues:
        if "Below-average communication score" not in issues and \
           "Communication below corporate client threshold (executive presence required)" not in issues:
            issues.append("Communication issues mentioned in feedback")
            recommendations.append(_get_tip(
                client_type, "communication",
                "Feedback highlights communication problems — prioritise presentation coaching."
            ))

    if "confidence" in text_issues:
        if "Low confidence indicators in scoring" not in issues:
            issues.append("Confidence issues detected in feedback")
            recommendations.append(_get_tip(
                client_type, "confidence",
                "Address confidence signals noted; consider a practice run with a senior recruiter acting as the client."
            ))

    if "preparation" in text_issues:
        issues.append("Candidate appeared underprepared for the client interview")
        recommendations.append(
            "Implement a mandatory pre-interview briefing pack covering the client's business, recent news, and role expectations."
        )

    if "technical" in text_issues:
        if "Technical competency gaps identified" not in issues:
            issues.append("Technical shortcomings noted in feedback")
            recommendations.append(
                "Review the specific technical areas flagged and arrange upskilling before resubmission."
            )

    if "cultural_fit" in text_issues:
        if "Cultural fit concerns flagged" not in issues:
            issues.append("Cultural or attitude concerns in feedback")
            recommendations.append(_get_tip(
                client_type, "cultural_fit",
                "Have a candid conversation with the candidate about professionalism and client expectations."
            ))

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

    summary = _build_summary(candidate, risk_level, adjusted_score, issues, is_post)

    weights_used = _get_weights(client_type)
    score_breakdown = {
        "technical": candidate.technical_score,
        "communication": candidate.communication_score,
        "confidence": candidate.confidence_score,
        "cultural_fit": candidate.cultural_fit_score,
        "internal": candidate.internal_score,
        "weighted_total": weighted_score,
        "rejection_penalty": rejection_penalty,
        "final_score": adjusted_score,
        "weights_used": weights_used,
        "client_type": client_type,
    }

    return InsightResult(
        risk_level=risk_level,
        risk_score=adjusted_score,
        identified_issues=issues,
        recommendations=recommendations,
        summary=summary,
        score_breakdown=score_breakdown,
        mode_label=mode_label,
    )


def _build_summary(candidate: CandidateInput, risk_level: str, score: float, issues: list[str], is_post: bool) -> str:
    level_desc = {
        "LOW": "a strong candidate with minor areas to watch",
        "MEDIUM": "a moderate-risk candidate who needs targeted coaching",
        "HIGH": "a high-risk submission requiring significant preparation",
        "CRITICAL": "a critical-risk candidate who should not be submitted without substantial remediation",
    }
    mode_prefix = "Post-interview analysis shows" if is_post else "Pre-interview prediction:"
    desc = level_desc.get(risk_level, "an unclassified risk profile")
    issue_count = len([i for i in issues if i != "No major issues detected"])
    client_label = candidate.client_type.capitalize()
    return (
        f"{mode_prefix} {candidate.name} applying for {candidate.role} "
        f"at a {client_label} client is {desc} "
        f"(risk score: {score}/100). "
        f"{issue_count} issue{'s' if issue_count != 1 else ''} identified."
    )
