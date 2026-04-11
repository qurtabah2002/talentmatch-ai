"""Scoring service — orchestrates the screening pipeline.

Implements human oversight requirements (EU AI Act Art. 14):
- Scores in the human_review_band require manual review
- Auto-reject and auto-advance thresholds are configurable
- All decisions are logged for audit
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog

from app.config import get_settings

logger = structlog.get_logger(__name__)


def determine_action(score: float) -> dict:
    """Map a score to a recommended action with human oversight flags.

    Returns:
        action: "auto_reject" | "human_review" | "auto_advance"
        requires_human_review: bool
        confidence: "low" | "medium" | "high"
    """
    settings = get_settings()

    if score <= settings.auto_reject_threshold * 100:
        return {
            "action": "auto_reject",
            "requires_human_review": False,
            "confidence": "high",
            "reason": "Score below minimum threshold",
        }

    if score >= settings.auto_advance_threshold * 100:
        return {
            "action": "auto_advance",
            "requires_human_review": False,
            "confidence": "high",
            "reason": "Strong match across all criteria",
        }

    # Middle band → human review required
    confidence = "medium" if score >= 50 else "low"
    return {
        "action": "human_review",
        "requires_human_review": True,
        "confidence": confidence,
        "reason": "Score in review band — human decision required",
    }


def build_screening_result(
    resume_text: str,
    job_description: str,
    job_title: str,
    candidate_id: str | None,
    model_result: dict,
) -> dict:
    """Assemble a complete screening result with audit metadata.

    EU AI Act Art. 12 — Records of all screening decisions.
    """
    score = model_result["score"]
    action = determine_action(score)

    result = {
        "screening_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate_id": candidate_id or "anonymous",
        "job_title": job_title,
        "score": score,
        "score_raw": model_result["score_raw"],
        "model_version": model_result["model_version"],
        "explanation": model_result["explanation"],
        "action": action["action"],
        "requires_human_review": action["requires_human_review"],
        "confidence": action["confidence"],
        "action_reason": action["reason"],
        # Bias monitoring metadata (NIST AI RMF — Measure)
        "fairness_flags": _check_fairness_flags(resume_text),
    }

    logger.info(
        "screening_completed",
        screening_id=result["screening_id"],
        score=score,
        action=action["action"],
        model_version=model_result["model_version"],
        requires_human_review=action["requires_human_review"],
    )

    return result


def _check_fairness_flags(resume_text: str) -> list[str]:
    """Flag potential fairness concerns for human reviewer.

    NIST AI RMF Measure 2.6 — Bias detection in inputs.
    """
    flags: list[str] = []
    text_lower = resume_text.lower()

    # Check if resume contains very little technical content (may disadvantage)
    word_count = len(text_lower.split())
    if word_count < 50:
        flags.append("short_resume_may_affect_score")

    # Check for non-English content that TF-IDF may not handle well
    ascii_ratio = sum(1 for c in text_lower if ord(c) < 128) / max(len(text_lower), 1)
    if ascii_ratio < 0.8:
        flags.append("multilingual_content_detected")

    return flags
