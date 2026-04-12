"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.screener import ResumeScreener


@pytest.fixture(scope="module", autouse=True)
def load_model():
    """Load model before API tests."""
    import app.main as main_module
    screener = ResumeScreener()
    screener.load("app/ml/data/model.pkl")
    main_module.screener = screener
    yield


@pytest.fixture
def client():
    return TestClient(app)


class TestHealth:
    def test_health(self, client: TestClient):
        r = client.get("/api/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True


class TestScreenEndpoint:
    def test_screen_resume_text(self, client: TestClient):
        r = client.post("/api/screen", json={
            "resume_text": "experienced python developer with machine learning and tensorflow skills",
            "job_description": "senior data scientist requiring python tensorflow machine learning",
            "job_title": "Data Scientist",
            "candidate_id": "test-api-001",
        })
        assert r.status_code == 200
        data = r.json()
        assert "screening_id" in data
        assert 0 <= data["score"] <= 100
        assert data["action"] in ("auto_reject", "human_review", "auto_advance")
        assert isinstance(data["explanation"], list)
        assert isinstance(data["fairness_flags"], list)

    def test_screen_empty_resume(self, client: TestClient):
        r = client.post("/api/screen", json={
            "resume_text": "",
            "job_description": "some job",
        })
        assert r.status_code == 422

    def test_screen_empty_job(self, client: TestClient):
        r = client.post("/api/screen", json={
            "resume_text": "some resume",
            "job_description": "   ",
        })
        assert r.status_code == 422

    def test_screen_upload(self, client: TestClient):
        r = client.post(
            "/api/screen/upload",
            files={"file": ("resume.txt", b"python developer with ml experience", "text/plain")},
            data={"job_description": "python developer needed", "job_title": "Dev"},
        )
        assert r.status_code == 200
        data = r.json()
        assert "screening_id" in data


class TestModelInfo:
    def test_model_info(self, client: TestClient):
        r = client.get("/api/model/info")
        assert r.status_code == 200
        data = r.json()
        assert data["model_type"] == "TF-IDF + Logistic Regression"
        assert data["is_loaded"] is True
        assert len(data["human_review_band"]) == 2

    def test_fairness_report(self, client: TestClient):
        r = client.get("/api/model/fairness")
        assert r.status_code == 200
        data = r.json()
        assert "demographic_parity" in data
        assert "equal_opportunity" in data
        assert 0 <= data["disparate_impact_ratio"] <= 1
