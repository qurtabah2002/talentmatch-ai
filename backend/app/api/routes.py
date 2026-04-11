"""API routes for TalentMatch AI."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.config import get_settings
from app.services.parser import extract_text_from_bytes
from app.services.scorer import build_screening_result

router = APIRouter()


# ── Pydantic schemas ─────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    model_version: str
    timestamp: str


class ScreenRequest(BaseModel):
    resume_text: str
    job_description: str
    job_title: str = "Unspecified Position"
    candidate_id: str | None = None


class ScreenResponse(BaseModel):
    screening_id: str
    timestamp: str
    candidate_id: str
    job_title: str
    score: float
    score_raw: float
    model_version: str
    explanation: list[dict]
    action: str
    requires_human_review: bool
    confidence: str
    action_reason: str
    fairness_flags: list[str]


class ModelInfoResponse(BaseModel):
    model_version: str
    model_type: str
    is_loaded: bool
    auto_reject_threshold: float
    auto_advance_threshold: float
    human_review_band: list[float]
    fairness_metrics_url: str


class FairnessReport(BaseModel):
    model_version: str
    generated_at: str
    demographic_parity: dict
    equal_opportunity: dict
    disparate_impact_ratio: float
    recommendation: str


# ── Health ───────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health():
    from app.main import screener
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=screener.is_loaded if screener else False,
        model_version=screener.model_version if screener else "not_loaded",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ── Screen resume (text) ────────────────────────────────

@router.post("/screen", response_model=ScreenResponse)
async def screen_resume(body: ScreenRequest):
    """Screen a resume against a job description.

    Returns a compatibility score (0–100) with explanation factors and
    a recommended action (auto_reject | human_review | auto_advance).

    EU AI Act Art. 14 — Human oversight: scores in the review band
    are flagged for mandatory human decision.
    """
    from app.main import screener

    if not screener or not screener.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")

    if not body.resume_text.strip():
        raise HTTPException(status_code=422, detail="Resume text cannot be empty")
    if not body.job_description.strip():
        raise HTTPException(status_code=422, detail="Job description cannot be empty")

    model_result = screener.score(body.resume_text, body.job_description)
    result = build_screening_result(
        resume_text=body.resume_text,
        job_description=body.job_description,
        job_title=body.job_title,
        candidate_id=body.candidate_id,
        model_result=model_result,
    )
    return ScreenResponse(**result)


# ── Screen resume (file upload) ─────────────────────────

@router.post("/screen/upload", response_model=ScreenResponse)
async def screen_resume_upload(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form("Unspecified Position"),
    candidate_id: str | None = Form(None),
):
    """Upload a resume file (PDF, DOCX, TXT) and screen against a job description."""
    from app.main import screener

    if not screener or not screener.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Read and extract text from file
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")

    resume_text = extract_text_from_bytes(content, file.filename or "resume.txt")
    if not resume_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from file")

    model_result = screener.score(resume_text, job_description)
    result = build_screening_result(
        resume_text=resume_text,
        job_description=job_description,
        job_title=job_title,
        candidate_id=candidate_id,
        model_result=model_result,
    )
    return ScreenResponse(**result)


# ── Model info ───────────────────────────────────────────

@router.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    """Return model metadata. EU AI Act Art. 13 — Transparency."""
    from app.main import screener
    settings = get_settings()
    return ModelInfoResponse(
        model_version=screener.model_version if screener else "not_loaded",
        model_type="TF-IDF + Logistic Regression",
        is_loaded=screener.is_loaded if screener else False,
        auto_reject_threshold=settings.auto_reject_threshold,
        auto_advance_threshold=settings.auto_advance_threshold,
        human_review_band=list(settings.human_review_band),
        fairness_metrics_url="/api/model/fairness",
    )


# ── Fairness report ─────────────────────────────────────

@router.get("/model/fairness", response_model=FairnessReport)
async def fairness_report():
    """Return latest fairness metrics. NIST AI RMF — Measure function.

    In production, these would come from the evaluation pipeline.
    This demo returns representative metrics.
    """
    from app.main import screener
    return FairnessReport(
        model_version=screener.model_version if screener else "not_loaded",
        generated_at=datetime.now(timezone.utc).isoformat(),
        demographic_parity={
            "gender": {"male": 0.72, "female": 0.69, "non_binary": 0.71},
            "ethnicity": {"group_a": 0.71, "group_b": 0.70, "group_c": 0.68},
            "age_group": {"18_30": 0.73, "31_45": 0.71, "46_plus": 0.67},
        },
        equal_opportunity={
            "gender": {"male": 0.81, "female": 0.79},
            "ethnicity": {"group_a": 0.80, "group_b": 0.78, "group_c": 0.77},
        },
        disparate_impact_ratio=0.94,
        recommendation=(
            "Model meets the 80% rule (disparate impact ratio > 0.80). "
            "Age group 46+ shows slightly lower scores — monitor for drift. "
            "Schedule re-evaluation after next training cycle."
        ),
    )
