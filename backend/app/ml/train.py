"""Model training script with MLflow experiment tracking.

Usage:
    python -m app.ml.train

Logs metrics, parameters, and artifacts to MLflow for Vigilens evidence collection.
This is the script that generates evidence for NIST AI RMF Measure controls
and EU AI Act Art. 9 (risk management) requirements.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

from app.config import get_settings
from app.ml.evaluate import run_fairness_evaluation


def load_training_data() -> pd.DataFrame:
    """Load training data from CSV or generate synthetic dataset."""
    data_path = Path(__file__).parent / "data" / "training_data.csv"

    if data_path.exists():
        return pd.read_csv(data_path)

    # Generate synthetic training data for demo
    print("Generating synthetic training data...")
    records = _generate_synthetic_data()
    df = pd.DataFrame(records)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_path, index=False)
    print(f"Saved {len(df)} training samples to {data_path}")
    return df


def _generate_synthetic_data() -> list[dict]:
    """Generate realistic resume–job pairs for training."""
    skills_by_role = {
        "data_scientist": ["python", "machine learning", "tensorflow", "pytorch", "pandas", "statistics", "sql", "deep learning", "nlp", "computer vision"],
        "backend_engineer": ["java", "spring boot", "microservices", "aws", "docker", "kubernetes", "postgresql", "redis", "rest api", "graphql"],
        "frontend_developer": ["react", "typescript", "nextjs", "css", "html", "webpack", "testing", "accessibility", "responsive design", "figma"],
        "devops_engineer": ["kubernetes", "docker", "terraform", "ansible", "ci cd", "aws", "gcp", "monitoring", "linux", "bash"],
        "ml_engineer": ["python", "sklearn", "mlflow", "feature engineering", "model deployment", "docker", "spark", "airflow", "tensorflow", "production ml"],
        "security_engineer": ["owasp", "penetration testing", "security audit", "compliance", "encryption", "iam", "siem", "incident response", "vulnerability assessment", "zero trust"],
    }

    non_tech_skills = [
        "marketing", "sales", "accounting", "hr management", "content writing",
        "project management", "customer support", "graphic design", "teaching",
        "event planning", "real estate", "journalism", "nursing",
    ]

    records = []
    import random
    random.seed(42)

    for role, skills in skills_by_role.items():
        job_desc = f"{role.replace('_', ' ')} position requiring: {', '.join(skills[:6])}"

        # Positive matches (relevant resumes)
        for _ in range(15):
            n_skills = random.randint(3, 7)
            selected = random.sample(skills, min(n_skills, len(skills)))
            extra = random.sample(["communication", "teamwork", "agile", "leadership"], 2)
            resume = f"experienced professional with skills in {', '.join(selected + extra)}. {random.randint(2, 12)} years of experience."
            combined = f"{resume} [SEP] {job_desc}"
            records.append({"text": combined, "label": 1, "role": role})

        # Negative matches (irrelevant resumes)
        for _ in range(15):
            n_skills = random.randint(2, 5)
            selected = random.sample(non_tech_skills, n_skills)
            resume = f"professional background in {', '.join(selected)}. {random.randint(1, 10)} years of experience."
            combined = f"{resume} [SEP] {job_desc}"
            records.append({"text": combined, "label": 0, "role": role})

        # Partial matches (adjacent roles — harder cases)
        other_roles = [r for r in skills_by_role if r != role]
        for _ in range(5):
            other = random.choice(other_roles)
            other_skills = random.sample(skills_by_role[other], 4)
            overlap = random.sample(skills, 1)
            resume = f"professional with {', '.join(other_skills + overlap)} experience."
            combined = f"{resume} [SEP] {job_desc}"
            # Partial matches get label 0 (not a strong match)
            records.append({"text": combined, "label": 0, "role": role})

    return records


def train(
    max_features: int = 5000,
    ngram_range: tuple[int, int] = (1, 2),
    C: float = 1.0,
    test_size: float = 0.2,
):
    """Train the resume screener model and log to MLflow."""
    settings = get_settings()

    # Configure MLflow
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    df = load_training_data()
    X = df["text"].tolist()
    y = df["label"].tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y,
    )

    with mlflow.start_run(run_name="tfidf-logreg-training") as run:
        # Log parameters
        mlflow.log_param("max_features", max_features)
        mlflow.log_param("ngram_range", str(ngram_range))
        mlflow.log_param("C", C)
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))
        mlflow.log_param("model_type", "TF-IDF + Logistic Regression")

        # Build and train pipeline
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                stop_words="english",
            )),
            ("clf", LogisticRegression(
                max_iter=1000,
                C=C,
                class_weight="balanced",
                random_state=42,
            )),
        ])

        pipeline.fit(X_train, y_train)

        # Evaluate on test set
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("auc_roc", auc)

        # Cross-validation
        cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1")
        mlflow.log_metric("cv_f1_mean", cv_scores.mean())
        mlflow.log_metric("cv_f1_std", cv_scores.std())

        # Classification report as artifact
        report = classification_report(y_test, y_pred, output_dict=True)
        report_path = "/tmp/classification_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        mlflow.log_artifact(report_path)

        # Fairness evaluation (NIST AI RMF — Measure)
        fairness = run_fairness_evaluation(pipeline, X_test, y_test)
        mlflow.log_metric("disparate_impact_ratio", fairness["disparate_impact_ratio"])
        mlflow.log_metric("demographic_parity_diff", fairness["demographic_parity_diff"])

        fairness_path = "/tmp/fairness_report.json"
        with open(fairness_path, "w") as f:
            json.dump(fairness, f, indent=2)
        mlflow.log_artifact(fairness_path)

        # Log model
        mlflow.sklearn.log_model(pipeline, "model")

        # Save locally
        from app.models.screener import ResumeScreener
        screener = ResumeScreener()
        screener.pipeline = pipeline
        screener.model_version = f"1.0.0-{run.info.run_id[:8]}"
        screener.save(settings.model_path)

        print(f"\n{'=' * 60}")
        print(f"Training complete — MLflow Run ID: {run.info.run_id}")
        print(f"{'=' * 60}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"AUC-ROC:   {auc:.4f}")
        print(f"CV F1:     {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"Disparate Impact Ratio: {fairness['disparate_impact_ratio']:.4f}")
        print(f"Model saved to: {settings.model_path}")
        print(f"{'=' * 60}")

        return run.info.run_id


if __name__ == "__main__":
    train()
