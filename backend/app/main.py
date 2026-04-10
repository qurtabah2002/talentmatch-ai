"""FastAPI application entry point."""

from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models.screener import ResumeScreener

logger = structlog.get_logger(__name__)

# Global model instance
screener: ResumeScreener | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model on startup."""
    global screener
    settings = get_settings()
    screener = ResumeScreener()
    screener.load(settings.model_path)
    logger.info("talentmatch_started", model_loaded=screener.is_loaded)
    yield
    logger.info("talentmatch_shutdown")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=(
            "AI-Powered Resume Screening & Candidate Matching. "
            "HIGH-RISK AI SYSTEM — EU AI Act Annex III, Category 4."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request logging + audit trail middleware
    @app.middleware("http")
    async def audit_log(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "http_request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=elapsed_ms,
        )

        # EU AI Act Art. 12 — Automatic logging of system operations
        response.headers["X-Request-Id"] = request_id
        return response

    from app.api.routes import router
    app.include_router(router, prefix="/api")

    return app


app = create_app()
