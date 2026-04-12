"""Tests for the ML model and scoring pipeline."""

import pytest

from app.models.screener import ResumeScreener
from app.services.scorer import build_screening_result, determine_action


@pytest.fixture(scope="module")
def screener():
    s = ResumeScreener()
    s.load("app/ml/data/model.pkl")
    return s


class TestResumeScreener:
    def test_load_default_model(self, screener: ResumeScreener):
        assert screener.is_loaded
        assert screener.pipeline is not None

    def test_score_returns_required_fields(self, screener: ResumeScreener):
        result = screener.score(
            "python machine learning tensorflow data science",
            "data scientist requiring python tensorflow machine learning",
        )
        assert "score" in result
        assert "score_raw" in result
        assert "model_version" in result
        assert "explanation" in result

    def test_score_range(self, screener: ResumeScreener):
        result = screener.score(
            "python data science tensorflow deep learning",
            "data scientist requiring python tensorflow",
        )
        assert 0 <= result["score"] <= 100

    def test_high_match_scores_higher(self, screener: ResumeScreener):
        high = screener.score(
            "experienced python machine learning tensorflow pytorch data scientist",
            "senior data scientist with python tensorflow pytorch machine learning",
        )
        low = screener.score(
            "marketing sales customer support event planning",
            "senior data scientist with python tensorflow pytorch machine learning",
        )
        assert high["score"] > low["score"]

    def test_explanation_factors(self, screener: ResumeScreener):
        result = screener.score(
            "python tensorflow machine learning",
            "data scientist requiring python tensorflow",
        )
        assert isinstance(result["explanation"], list)
        for factor in result["explanation"]:
            assert "term" in factor
            assert "weight" in factor


class TestDetermineAction:
    def test_auto_reject(self):
        action = determine_action(15)
        assert action["action"] == "auto_reject"
        assert action["requires_human_review"] is False

    def test_human_review(self):
        action = determine_action(50)
        assert action["action"] == "human_review"
        assert action["requires_human_review"] is True

    def test_auto_advance(self):
        action = determine_action(90)
        assert action["action"] == "auto_advance"
        assert action["requires_human_review"] is False

    def test_boundary_reject(self):
        action = determine_action(20)
        assert action["action"] == "auto_reject"

    def test_boundary_advance(self):
        action = determine_action(85)
        assert action["action"] == "auto_advance"


class TestBuildScreeningResult:
    def test_result_structure(self, screener: ResumeScreener):
        model_result = screener.score("python developer", "python developer needed")
        result = build_screening_result(
            resume_text="python developer",
            job_description="python developer needed",
            job_title="Python Dev",
            candidate_id="test-001",
            model_result=model_result,
        )
        assert "screening_id" in result
        assert "timestamp" in result
        assert result["candidate_id"] == "test-001"
        assert result["job_title"] == "Python Dev"
        assert "fairness_flags" in result

    def test_anonymous_candidate(self, screener: ResumeScreener):
        model_result = screener.score("python", "python dev")
        result = build_screening_result(
            resume_text="python",
            job_description="python dev",
            job_title="Dev",
            candidate_id=None,
            model_result=model_result,
        )
        assert result["candidate_id"] == "anonymous"
