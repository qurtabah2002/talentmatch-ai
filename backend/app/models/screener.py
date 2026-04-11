"""Resume screening ML model wrapper.

Uses TF-IDF vectorisation + Logistic Regression to produce a
compatibility score between a resume and a job description.

Model card: docs/model_card.md
"""

from __future__ import annotations

import os
import pickle
from pathlib import Path

import structlog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

logger = structlog.get_logger(__name__)


class ResumeScreener:
    """Wraps a scikit-learn pipeline for resume–job matching."""

    def __init__(self) -> None:
        self.pipeline: Pipeline | None = None
        self.is_loaded: bool = False
        self.model_version: str = "0.0.0"

    # ── Load / Save ──────────────────────────────────────

    def load(self, path: str) -> None:
        """Load a pickled pipeline from disk. Falls back to a fresh model."""
        if Path(path).exists():
            with open(path, "rb") as f:
                data = pickle.load(f)  # noqa: S301
            self.pipeline = data.get("pipeline")
            self.model_version = data.get("version", "unknown")
            self.is_loaded = True
            logger.info("model_loaded", version=self.model_version, path=path)
        else:
            logger.warning("model_not_found", path=path)
            self._init_default()

    def save(self, path: str) -> None:
        """Persist pipeline to disk."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"pipeline": self.pipeline, "version": self.model_version}, f)
        logger.info("model_saved", path=path, version=self.model_version)

    # ── Predict ──────────────────────────────────────────

    def score(self, resume_text: str, job_description: str) -> dict:
        """Return a compatibility score (0–100) with explanation factors.

        EU AI Act Art. 13 — Transparency: the explanation factors provide
        insight into why a score was produced.
        """
        if not self.pipeline:
            self._init_default()

        combined = f"{resume_text} [SEP] {job_description}"

        # Get probability of positive class
        proba = self.pipeline.predict_proba([combined])[0]
        score_raw = float(proba[1]) if len(proba) > 1 else float(proba[0])
        score_pct = round(score_raw * 100, 1)

        # Extract top matching TF-IDF features as explanation
        explanation = self._explain(resume_text, job_description)

        return {
            "score": score_pct,
            "score_raw": score_raw,
            "model_version": self.model_version,
            "explanation": explanation,
        }

    def _explain(self, resume_text: str, job_description: str) -> list[dict]:
        """Extract top matching keywords as transparency factors."""
        try:
            vectorizer: TfidfVectorizer = self.pipeline.named_steps["tfidf"]
            feature_names = vectorizer.get_feature_names_out()

            resume_vec = vectorizer.transform([resume_text]).toarray()[0]
            job_vec = vectorizer.transform([job_description]).toarray()[0]

            # Find overlapping important terms
            overlap_scores = resume_vec * job_vec
            top_indices = overlap_scores.argsort()[-10:][::-1]

            factors = []
            for idx in top_indices:
                if overlap_scores[idx] > 0:
                    factors.append({
                        "term": feature_names[idx],
                        "weight": round(float(overlap_scores[idx]), 4),
                        "in_resume": bool(resume_vec[idx] > 0),
                        "in_job": bool(job_vec[idx] > 0),
                    })
            return factors[:5]
        except Exception:
            return []

    # ── Default model ────────────────────────────────────

    def _init_default(self) -> None:
        """Initialise a basic model with synthetic training data for demo."""
        logger.info("initializing_default_model")

        # Synthetic training pairs: (combined text, match label)
        texts = [
            "python machine learning tensorflow data science [SEP] senior data scientist python tensorflow",
            "java spring boot microservices aws [SEP] backend engineer java spring cloud",
            "react typescript nextjs frontend ui [SEP] frontend developer react typescript",
            "python flask sql analytics [SEP] senior data scientist python tensorflow",
            "marketing social media content [SEP] senior data scientist python tensorflow",
            "accounting bookkeeping excel [SEP] senior data scientist python tensorflow",
            "python pandas numpy sklearn ml [SEP] machine learning engineer python sklearn",
            "rust systems programming embedded [SEP] machine learning engineer python sklearn",
            "hr recruiting talent acquisition [SEP] machine learning engineer python sklearn",
            "javascript node express mongodb [SEP] fullstack developer javascript react node",
            "c++ embedded firmware iot [SEP] fullstack developer javascript react node",
            "sales crm pipeline revenue [SEP] fullstack developer javascript react node",
            "devops kubernetes docker ci cd terraform [SEP] devops engineer kubernetes docker aws",
            "nursing patient care medical [SEP] devops engineer kubernetes docker aws",
            "python data pipeline airflow spark etl [SEP] data engineer python spark airflow",
            "teaching curriculum education pedagogy [SEP] data engineer python spark airflow",
            "security penetration testing owasp compliance [SEP] security engineer owasp penetration testing",
            "cooking restaurant hospitality [SEP] security engineer owasp penetration testing",
        ]
        labels = [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english")),
            ("clf", LogisticRegression(max_iter=1000, C=1.0, class_weight="balanced")),
        ])
        self.pipeline.fit(texts, labels)
        self.model_version = "0.1.0-default"
        self.is_loaded = True
        logger.info("default_model_ready", version=self.model_version)
