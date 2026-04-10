"""Application configuration via environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "TalentMatch AI"
    environment: str = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    allowed_origins: list[str] = ["http://localhost:3001"]

    # ML Model
    model_path: str = "app/ml/data/model.pkl"
    min_score_threshold: float = 0.3
    max_candidates_per_job: int = 100

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "talentmatch-resume-screener"

    # Vigilens webhook
    vigilens_webhook_url: str = ""
    vigilens_webhook_secret: str = ""

    # Datadog
    datadog_api_key: str = ""
    datadog_app_key: str = ""

    # Human oversight
    auto_reject_threshold: float = 0.2
    auto_advance_threshold: float = 0.85
    human_review_band: tuple[float, float] = (0.2, 0.85)

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


def get_settings() -> Settings:
    return Settings()
